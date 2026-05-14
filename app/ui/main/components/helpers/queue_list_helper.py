#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导出队列助手
提供队列列表的创建和操作功能
"""

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


def create_queue_settings_widget(
    parent_widget: "QWidget",
    max_concurrent: int = 2,
    auto_cleanup: bool = True,
    on_apply: Callable = None
) -> dict:
    """
    创建队列设置控件

    Returns:
        dict with 'max_concurrent_spin', 'auto_cleanup_check', 'apply_btn', 'group'
    """
    from PySide6.QtWidgets import QGroupBox, QFormLayout, QSpinBox, QCheckBox, QPushButton, QVBoxLayout

    settings_group = QGroupBox("队列设置")
    settings_layout = QFormLayout(settings_group)

    max_concurrent_spin = QSpinBox()
    max_concurrent_spin.setRange(1, 8)
    max_concurrent_spin.setValue(max_concurrent)

    auto_cleanup_check = QCheckBox("自动清理已完成任务")
    auto_cleanup_check.setChecked(auto_cleanup)

    apply_btn = QPushButton("应用设置")
    if on_apply:
        apply_btn.clicked.connect(on_apply)

    settings_layout.addRow("最大并发数:", max_concurrent_spin)
    settings_layout.addRow("自动清理:", auto_cleanup_check)

    content_layout = QVBoxLayout()
    content_layout.addWidget(settings_group)
    content_layout.addWidget(apply_btn)

    return {
        'max_concurrent_spin': max_concurrent_spin,
        'auto_cleanup_check': auto_cleanup_check,
        'apply_btn': apply_btn,
        'group': settings_group,
        'content_layout': content_layout
    }


def create_queue_tab_widget(parent_widget: "QWidget", queue_widget, on_apply_settings: Callable = None) -> QWidget:
    """
    创建队列管理标签页

    Args:
        parent_widget: Parent widget
        queue_widget: ExportQueueWidget instance
        on_apply_settings: Callback for apply settings button
    """
    from PySide6.QtWidgets import QWidget, QVBoxLayout

    widget = QWidget()
    layout = QVBoxLayout(widget)

    # 队列状态
    layout.addWidget(queue_widget)

    # 队列设置
    settings = create_queue_settings_widget(
        parent_widget,
        on_apply=on_apply_settings
    )

    layout.addWidget(settings['group'])
    layout.addWidget(settings['apply_btn'])

    return widget
