#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导出面板
提供完整的视频导出功能界面
"""

import os
from typing import Dict, List, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QGroupBox, QHBoxLayout,
    QComboBox, QPushButton, QMessageBox, QDialog
)
from PySide6.QtCore import Signal

from ...export.export_system import ExportPreset, ExportFormat
from ...core.logger import Logger

from .export_format_selector import ExportSettingsDialog
from .export_progress import ExportQueueWidget
from .helpers import (
    create_quick_export_tab,
    create_batch_export_tab,
    create_concurrent_settings_widget,
    get_concurrent_settings,
    create_presets_table_widget,
    populate_presets_table
)
from .helpers.export_validators import (
    validate_export_request,
    validate_batch_export_request,
    show_export_error
)


class ExportPanel(QWidget):
    """导出面板主类"""

    # 信号定义
    export_started = Signal(str)
    export_progress = Signal(str, float)
    export_completed = Signal(str, str)
    export_failed = Signal(str, str)

    def __init__(self, application, parent=None):
        super().__init__(parent)
        self.application = application
        self.export_system = application.export_system
        self.logger = Logger.get_logger(__name__)
        self.current_project_id = None
        self._init_tabs()
        self.connect_signals()

    def _init_tabs(self):
        """初始化所有标签页"""
        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()

        self._quick_export_tab = create_quick_export_tab(self)
        self._setup_quick_export_connections()
        self.tab_widget.addTab(self._quick_export_tab['widget'], "快速导出")

        self._batch_tab = create_batch_export_tab(
            self,
            on_select_all=self.select_all_projects,
            on_select_none=self.select_none_projects,
            on_batch_export=self.start_batch_export
        )
        self._batch_tab['browse_btn'].clicked.connect(self.browse_batch_output_dir)
        self.tab_widget.addTab(self._batch_tab['widget'], "批量导出")

        self._queue_tab = self._create_queue_tab()
        self.tab_widget.addTab(self._queue_tab, "队列管理")

        self._presets_tab = self._create_presets_tab()
        self.tab_widget.addTab(self._presets_tab['widget'], "预设管理")

        layout.addWidget(self.tab_widget)

    def _setup_quick_export_connections(self):
        """设置快速导出标签页的信号连接"""
        tab = self._quick_export_tab
        tab['browse_btn'].clicked.connect(self.browse_output_path)
        tab['export_btn'].clicked.connect(self.start_export)
        tab['export_youtube_btn'].clicked.connect(lambda: self.quick_export("youtube_1080p"))
        tab['export_tiktok_btn'].clicked.connect(lambda: self.quick_export("tiktok_video"))
        tab['export_instagram_btn'].clicked.connect(lambda: self.quick_export("instagram_reel"))
        tab['export_jianying_btn'].clicked.connect(lambda: self.quick_export("jianying_draft"))

    def _create_queue_tab(self) -> QWidget:
        """创建队列管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.queue_widget = ExportQueueWidget()
        layout.addWidget(self.queue_widget)
        self.queue_settings = create_concurrent_settings_widget(self, on_apply=self.apply_queue_settings)
        layout.addWidget(self.queue_settings['group'])
        layout.addWidget(self.queue_settings['apply_btn'])
        return widget

    def _create_presets_tab(self) -> dict:
        """创建预设管理标签页"""
        presets_tab = create_presets_table_widget(
            self, export_system=self.export_system,
            on_add_preset=self.add_preset, on_edit_preset=self.edit_preset,
            on_delete_preset=self.delete_preset, on_refresh=self.refresh_presets_table
        )
        presets_group = QGroupBox("导出预设")
        presets_layout = QVBoxLayout(presets_group)
        presets_layout.addWidget(presets_tab['table'])
        preset_actions_layout = QHBoxLayout()
        for btn in presets_tab['buttons'].values():
            preset_actions_layout.addWidget(btn)
        main_layout = QVBoxLayout()
        main_layout.addWidget(presets_group)
        main_layout.addLayout(preset_actions_layout)
        main_layout.addStretch()
        widget = QWidget()
        widget.setLayout(main_layout)
        return {'widget': widget, 'table': presets_tab['table']}

    def connect_signals(self):
        """连接信号"""
        self.export_system.export_started.connect(self.on_export_started)
        self.export_system.export_progress.connect(self.on_export_progress)
        self.export_system.export_completed.connect(self.on_export_completed)
        self.export_system.export_failed.connect(self.on_export_failed)
        self.queue_widget.task_action.connect(self.handle_queue_action)

    # -------------------------------------------------------------------------
    # Widget Accessors
    # -------------------------------------------------------------------------

    @property
    def project_name_label(self): return self._quick_export_tab['project_name_label']
    @property
    def project_duration_label(self): return self._quick_export_tab['project_duration_label']
    @property
    def project_resolution_label(self): return self._quick_export_tab['project_resolution_label']
    @property
    def preset_combo(self): return self._quick_export_tab['preset_combo']
    @property
    def output_path_edit(self): return self._quick_export_tab['output_path_edit']
    @property
    def batch_output_dir_edit(self): return self._batch_tab['output_dir_edit']
    @property
    def batch_preset_combo(self): return self._batch_tab['preset_combo']
    @property
    def batch_projects_table(self): return self._batch_tab['projects_table']
    @property
    def presets_table(self): return self._presets_tab['table']

    # -------------------------------------------------------------------------
    # Public API Methods
    # -------------------------------------------------------------------------

    def set_current_project(self, project_id: str, project_info: Dict[str, Any]):
        """设置当前项目"""
        self.current_project_id = project_id
        self.project_name_label.setText(project_info.get("name", "未知项目"))
        self.project_duration_label.setText(project_info.get("duration", "00:00:00"))
        self.project_resolution_label.setText(project_info.get("resolution", "1920x1080"))

    def refresh_presets(self):
        """刷新预设列表"""
        presets = self.export_system.get_presets()
        self.preset_combo.clear()
        self.batch_preset_combo.clear()
        for preset in presets:
            self.preset_combo.addItem(preset.name, preset.id)
            self.batch_preset_combo.addItem(preset.name, preset.id)

    def refresh_presets_table(self):
        """刷新预设表格"""
        populate_presets_table(self.presets_table, self.export_system.get_presets(),
                               on_edit=self.edit_preset_data, on_delete=self.delete_preset_data)

    def browse_output_path(self):
        """浏览输出路径"""
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "选择输出文件", "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv *.webm);;音频文件 (*.mp3 *.wav);;所有文件 (*)"
        )
        if file_path:
            self.output_path_edit.setText(file_path)

    def browse_batch_output_dir(self):
        """浏览批量输出目录"""
        from PySide6.QtWidgets import QFileDialog
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.batch_output_dir_edit.setText(dir_path)

    def quick_export(self, preset_id: str):
        """快速导出"""
        if not self.current_project_id:
            return QMessageBox.warning(self, "警告", "请先选择一个项目")
        self.start_export_with_preset(preset_id, f"{self.project_name_label.text()}_{preset_id}.mp4")

    def start_export(self):
        """开始导出"""
        valid, preset_id, output_path, _ = validate_export_request(
            self, self.current_project_id, self.preset_combo, self.output_path_edit
        )
        if valid:
            self.start_export_with_preset(preset_id, output_path)

    def start_export_with_preset(self, preset_id: str, output_path: str):
        """使用指定预设开始导出"""
        try:
            task_id = self.export_system.export_project(
                project_id=self.current_project_id, output_path=output_path, preset_id=preset_id,
                metadata={"project_name": self.project_name_label.text(),
                         "duration": self.project_duration_label.text(),
                         "resolution": self.project_resolution_label.text()}
            )
            QMessageBox.information(self, "成功", f"导出任务已添加到队列: {task_id}")
        except Exception as e:
            show_export_error(self, str(e))

    def start_batch_export(self):
        """开始批量导出"""
        valid, selected_projects, output_dir, preset_id = validate_batch_export_request(
            self, self.batch_projects_table, self.batch_output_dir_edit, self.batch_preset_combo
        )
        if not valid:
            return
        try:
            batch_configs = [
                {"project_id": p["id"], "output_path": os.path.join(output_dir, f"{p['name']}_{preset_id}.mp4"),
                 "preset_id": preset_id, "metadata": p}
                for p in selected_projects
            ]
            task_ids = self.export_system.export_batch(batch_configs)
            QMessageBox.information(self, "成功", f"已添加 {len(task_ids)} 个导出任务")
        except Exception as e:
            show_export_error(self, str(e))

    def select_all_projects(self):
        """全选项目"""
        for i in range(self.batch_projects_table.rowCount()):
            w = self.batch_projects_table.cellWidget(i, 0)
            if w: w.setChecked(True)

    def select_none_projects(self):
        """全不选项目"""
        for i in range(self.batch_projects_table.rowCount()):
            w = self.batch_projects_table.cellWidget(i, 0)
            if w: w.setChecked(False)

    def handle_queue_action(self, action: str, task_id: str):
        """处理队列操作"""
        try:
            handlers = {
                "start": (self.export_system.resume_export, "任务已恢复", "无法恢复该任务"),
                "pause": (self.export_system.pause_export, "任务已暂停", "无法暂停该任务"),
                "cancel": (self.export_system.cancel_export, "任务已取消", "无法取消该任务"),
                "remove": (self.export_system.remove_from_queue, None, None),
                "clear_completed": (self.export_system.clear_completed, "已完成任务已清除", None),
            }
            handler, success_msg, fail_msg = handlers.get(action, (None, None, None))
            if handler:
                result = handler(task_id)
                if action in ("start", "pause", "cancel"):
                    QMessageBox.information(self, "成功" if result else "警告", success_msg if result else fail_msg)
                elif action == "remove" and result:
                    self._refresh_queue_list()
                elif action == "clear_completed" and result:
                    self._refresh_queue_list()
                    QMessageBox.information(self, "成功", success_msg)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")

    def _refresh_queue_list(self):
        """刷新队列列表"""
        try:
            self.queue_widget.update_tasks(self.export_system.get_task_history())
        except Exception as e:
            self.logger.error(f"Failed to refresh queue list: {e}")

    def apply_queue_settings(self):
        """应用队列设置"""
        try:
            settings = get_concurrent_settings(self.queue_settings)
            self._apply_concurrent_limit(settings['max_concurrent'])
            if settings['auto_cleanup']:
                self._schedule_cleanup()
            QMessageBox.information(self, "成功", "队列设置已应用")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置应用失败: {str(e)}")

    def _apply_concurrent_limit(self, limit: int):
        try:
            self.export_system.set_concurrent_limit(limit)
        except AttributeError:
            pass

    def _schedule_cleanup(self):
        try:
            self.export_system.set_auto_cleanup(days=7)
        except AttributeError:
            pass

    def add_preset(self):
        """添加预设"""
        dialog = ExportSettingsDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_preset_data()
            res_str = data.get("resolution", "1920x1080")
            resolution = tuple(map(int, res_str.split("x"))) if "x" in res_str else (1920, 1080)
            new_preset = ExportPreset(
                name=data.get("name", "新预设"), description=data.get("description", ""),
                format=ExportFormat.MP4, resolution=resolution, fps=data.get("fps", 30),
                bitrate=int(data.get("bitrate", 8000)), audio_bitrate=int(data.get("audio_bitrate", 128)),
                codec="h264", audio_codec="aac",
            )
            self.export_system.add_preset(new_preset)
            self.refresh_presets()
            self.refresh_presets_table()
            QMessageBox.information(self, "成功", f"预设 '{new_preset.name}' 已添加")

    def edit_preset(self):
        """编辑预设"""
        row = self.presets_table.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "警告", "请选择要编辑的预设")
        preset_id = self._get_preset_id_from_row(row)
        if preset_id:
            self.edit_preset_data(self.export_system.get_preset(preset_id))

    def _get_preset_id_from_row(self, row: int) -> str:
        presets = self.export_system.get_presets()
        return presets[row].id if 0 <= row < len(presets) else None

    def edit_preset_data(self, preset: ExportPreset):
        """编辑预设数据"""
        if not preset:
            return
        dialog = ExportSettingsDialog(preset, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.export_system.update_preset(preset.id, dialog.get_preset_data())
            self.refresh_presets()
            QMessageBox.information(self, "成功", "预设已更新")

    def delete_preset(self):
        """删除预设"""
        row = self.presets_table.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "警告", "请选择要删除的预设")
        preset_id = self._get_preset_id_from_row(row)
        if preset_id:
            self.delete_preset_data(self.export_system.get_preset(preset_id))

    def delete_preset_data(self, preset: ExportPreset):
        """删除预设数据"""
        if not preset:
            return
        if QMessageBox.question(self, "确认删除", f"确定要删除预设 '{preset.name}' 吗？",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                 ) == QMessageBox.StandardButton.Yes:
            self.export_system.delete_preset(preset.id)
            self.refresh_presets()
            QMessageBox.information(self, "成功", "预设已删除")

    def update_queue_display(self):
        """更新队列显示"""
        try:
            self.queue_widget.update_tasks(self.export_system.get_task_history())
        except Exception as e:
            self.logger.error(f"Failed to update queue display: {e}")

    # -------------------------------------------------------------------------
    # Signal Handlers
    # -------------------------------------------------------------------------

    def on_export_started(self, task_id: str):
        self.logger.info(f"Export started: {task_id}")
        self.export_started.emit(task_id)

    def on_export_progress(self, task_id: str, progress: float):
        self.logger.info(f"Export progress: {task_id} - {progress:.1f}%")
        self.export_progress.emit(task_id, progress)

    def on_export_completed(self, task_id: str, output_path: str):
        self.logger.info(f"Export completed: {task_id} -> {output_path}")
        self.export_completed.emit(task_id, output_path)
        QMessageBox.information(self, "成功", f"导出完成: {output_path}")

    def on_export_failed(self, task_id: str, error_message: str):
        self.logger.error(f"Export failed: {task_id} - {error_message}")
        self.export_failed.emit(task_id, error_message)
        QMessageBox.critical(self, "错误", f"导出失败: {error_message}")

    # -------------------------------------------------------------------------
    # Lifecycle Methods
    # -------------------------------------------------------------------------

    def cleanup(self):
        """清理资源"""
        try:
            self.queue_widget.update_timer.stop()
        except RuntimeError as e:
            self.logger.debug(f"Timer already stopped: {e}")
        except Exception as e:
            self.logger.warning(f"Cleanup failed: {e}")

    def update_theme(self, is_dark: bool = True):
        """更新主题"""
        border = "#3a3a3a" if is_dark else "#d0d0d0"
        bg1 = "#1a1a1a" if is_dark else "#ffffff"
        bg2 = "#242424" if is_dark else "#f5f5f5"
        self.setStyleSheet(f"QGroupBox {{ border: 1px solid {border}; border-radius: 4px; margin-top: 8px; padding-top: 8px; }}"
                           f"QTableWidget {{ background-color: {bg1}; alternate-background-color: {bg2}; }}")
