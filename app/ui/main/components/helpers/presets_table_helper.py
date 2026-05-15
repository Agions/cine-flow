#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导出预设表格助手
提供预设表格的创建和操作功能
"""

from typing import List, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget, QTableWidget
    from ....export.export_system import ExportPreset


def create_presets_table_widget(
    parent_widget: "QWidget",
    export_system,
    on_add_preset: Callable = None,
    on_edit_preset: Callable = None,
    on_delete_preset: Callable = None,
    on_refresh: Callable = None
) -> dict:
    """
    创建预设表格及其操作按钮

    Returns:
        dict with 'table' and 'buttons' widgets
    """
    from PySide6.QtWidgets import QTableWidget, QPushButton

    table = QTableWidget()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels([
        "预设名称", "格式", "分辨率", "比特率", "操作"
    ])
    table.horizontalHeader().setStretchLastSection(True)

    buttons = {
        'add': QPushButton("添加预设"),
        'edit': QPushButton("编辑预设"),
        'delete': QPushButton("删除预设"),
        'refresh': QPushButton("刷新")
    }

    if on_add_preset:
        buttons['add'].clicked.connect(on_add_preset)
    if on_edit_preset:
        buttons['edit'].clicked.connect(on_edit_preset)
    if on_delete_preset:
        buttons['delete'].clicked.connect(on_delete_preset)
    if on_refresh:
        buttons['refresh'].clicked.connect(on_refresh)

    return {
        'table': table,
        'buttons': buttons
    }


def populate_presets_table(table: "QTableWidget", presets: List["ExportPreset"],
                            on_edit: Callable = None, on_delete: Callable = None):
    """
    填充预设表格数据
    """
    from PySide6.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QPushButton

    table.setRowCount(len(presets))

    for i, preset in enumerate(presets):
        table.setItem(i, 0, QTableWidgetItem(preset.name))
        table.setItem(i, 1, QTableWidgetItem(preset.format.value))
        table.setItem(i, 2, QTableWidgetItem(f"{preset.resolution[0]}x{preset.resolution[1]}"))
        table.setItem(i, 3, QTableWidgetItem(f"{preset.bitrate} kbps"))

        # 操作按钮
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        edit_btn = QPushButton("编辑")
        if on_edit:
            edit_btn.clicked.connect(lambda checked, p=preset: on_edit(p))
        actions_layout.addWidget(edit_btn)

        delete_btn = QPushButton("删除")
        if on_delete:
            delete_btn.clicked.connect(lambda checked, p=preset: on_delete(p))
        actions_layout.addWidget(delete_btn)

        actions_layout.addStretch()
        table.setCellWidget(i, 4, actions_widget)
