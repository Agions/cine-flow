#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
并发设置助手
提供并发和队列相关的设置控件
"""

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


def create_concurrent_settings_widget(
    parent_widget: "QWidget",
    initial_limit: int = 2,
    initial_auto_cleanup: bool = True,
    on_apply: Callable = None
) -> dict:
    """
    创建并发设置控件

    Returns:
        dict with widgets and values
    """
    from PySide6.QtWidgets import (
        QGroupBox, QFormLayout, QSpinBox, QCheckBox, QPushButton, QVBoxLayout
    )

    settings_group = QGroupBox("队列设置")
    settings_layout = QFormLayout(settings_group)

    max_concurrent_spin = QSpinBox()
    max_concurrent_spin.setRange(1, 8)
    max_concurrent_spin.setValue(initial_limit)

    auto_cleanup_check = QCheckBox("自动清理已完成任务")
    auto_cleanup_check.setChecked(initial_auto_cleanup)

    settings_layout.addRow("最大并发数:", max_concurrent_spin)
    settings_layout.addRow("自动清理:", auto_cleanup_check)

    apply_btn = QPushButton("应用设置")
    if on_apply:
        apply_btn.clicked.connect(on_apply)

    layout = QVBoxLayout()
    layout.addWidget(settings_group)
    layout.addWidget(apply_btn)

    return {
        'group': settings_group,
        'max_concurrent_spin': max_concurrent_spin,
        'auto_cleanup_check': auto_cleanup_check,
        'apply_btn': apply_btn,
        'layout': layout
    }


def get_concurrent_settings(settings: dict) -> dict:
    """
    获取并发设置值

    Args:
        settings: dict from create_concurrent_settings_widget

    Returns:
        dict with 'max_concurrent' and 'auto_cleanup'
    """
    return {
        'max_concurrent': settings['max_concurrent_spin'].value(),
        'auto_cleanup': settings['auto_cleanup_check'].isChecked()
    }
