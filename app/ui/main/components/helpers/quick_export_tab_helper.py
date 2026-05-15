#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速导出标签页助手
提供快速导出标签页的创建功能
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


def create_quick_export_tab(parent_widget: "QWidget") -> dict:
    """
    创建快速导出标签页

    Returns:
        dict with all widgets
    """
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel,
        QComboBox, QLineEdit, QPushButton, QHBoxLayout
    )

    widget = QWidget()
    layout = QVBoxLayout(widget)

    # 项目信息
    project_group = QGroupBox("项目信息")
    project_layout = QFormLayout(project_group)

    project_name_label = QLabel("未选择项目")
    project_duration_label = QLabel("00:00:00")
    project_resolution_label = QLabel("1920x1080")

    project_layout.addRow("项目名称:", project_name_label)
    project_layout.addRow("持续时间:", project_duration_label)
    project_layout.addRow("分辨率:", project_resolution_label)

    # 导出设置
    export_group = QGroupBox("导出设置")
    export_layout = QFormLayout(export_group)

    preset_combo = QComboBox()
    preset_combo.setMinimumWidth(200)

    output_path_edit = QLineEdit()
    output_path_edit.setPlaceholderText("选择输出路径...")
    browse_btn = QPushButton("浏览")

    output_layout = QHBoxLayout()
    output_layout.addWidget(output_path_edit, 1)
    output_layout.addWidget(browse_btn)

    export_layout.addRow("导出预设:", preset_combo)
    export_layout.addRow("输出路径:", output_layout)

    # 快速操作按钮
    quick_actions_group = QGroupBox("快速操作")
    quick_actions_layout = QHBoxLayout(quick_actions_group)

    export_youtube_btn = QPushButton("导出 YouTube")
    export_tiktok_btn = QPushButton("导出 TikTok")
    export_instagram_btn = QPushButton("导出 Instagram")
    export_jianying_btn = QPushButton("导出剪映草稿")

    quick_actions_layout.addWidget(export_youtube_btn)
    quick_actions_layout.addWidget(export_tiktok_btn)
    quick_actions_layout.addWidget(export_instagram_btn)
    quick_actions_layout.addWidget(export_jianying_btn)

    # 导出按钮
    export_btn = QPushButton("开始导出")
    export_btn.setMinimumHeight(40)

    # 添加到布局
    layout.addWidget(project_group)
    layout.addWidget(export_group)
    layout.addWidget(quick_actions_group)
    layout.addWidget(export_btn)
    layout.addStretch()

    return {
        'widget': widget,
        'project_name_label': project_name_label,
        'project_duration_label': project_duration_label,
        'project_resolution_label': project_resolution_label,
        'preset_combo': preset_combo,
        'output_path_edit': output_path_edit,
        'browse_btn': browse_btn,
        'export_youtube_btn': export_youtube_btn,
        'export_tiktok_btn': export_tiktok_btn,
        'export_instagram_btn': export_instagram_btn,
        'export_jianying_btn': export_jianying_btn,
        'export_btn': export_btn
    }
