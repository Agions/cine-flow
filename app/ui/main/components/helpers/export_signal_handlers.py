#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导出面板信号处理器助手
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def create_export_signal_handlers(panel) -> dict:
    """
    创建导出面板的信号处理器

    Args:
        panel: ExportPanel instance

    Returns:
        dict with handler methods
    """
    from PySide6.QtWidgets import QMessageBox

    def on_export_started(task_id: str):
        panel.logger.info(f"Export started: {task_id}")
        panel.export_started.emit(task_id)

    def on_export_progress(task_id: str, progress: float):
        panel.logger.info(f"Export progress: {task_id} - {progress:.1f}%")
        panel.export_progress.emit(task_id, progress)

    def on_export_completed(task_id: str, output_path: str):
        panel.logger.info(f"Export completed: {task_id} -> {output_path}")
        panel.export_completed.emit(task_id, output_path)
        QMessageBox.information(panel, "成功", f"导出完成: {output_path}")

    def on_export_failed(task_id: str, error_message: str):
        panel.logger.error(f"Export failed: {task_id} - {error_message}")
        panel.export_failed.emit(task_id, error_message)
        QMessageBox.critical(panel, "错误", f"导出失败: {error_message}")

    return {
        'on_export_started': on_export_started,
        'on_export_progress': on_export_progress,
        'on_export_completed': on_export_completed,
        'on_export_failed': on_export_failed
    }


def connect_export_signals(panel):
    """连接导出面板的信号"""
    handlers = create_export_signal_handlers(panel)
    panel.export_system.export_started.connect(handlers['on_export_started'])
    panel.export_system.export_progress.connect(handlers['on_export_progress'])
    panel.export_system.export_completed.connect(handlers['on_export_completed'])
    panel.export_system.export_failed.connect(handlers['on_export_failed'])
