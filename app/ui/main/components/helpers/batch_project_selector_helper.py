#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量项目选择器助手
提供批量导出项目列表的创建和操作功能
"""

from typing import Callable, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget, QTableWidget


def create_batch_projects_table(parent: "QWidget") -> "QTableWidget":
    """
    创建批量项目表格
    """
    from PySide6.QtWidgets import QTableWidget

    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels([
        "选择", "项目名称", "持续时间", "分辨率"
    ])
    table.horizontalHeader().setStretchLastSection(True)
    return table


def create_batch_export_tab(
    parent_widget: "QWidget",
    on_select_all: Callable = None,
    on_select_none: Callable = None,
    on_batch_export: Callable = None
) -> dict:
    """
    创建批量导出标签页

    Returns:
        dict with widgets
    """
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit,
        QPushButton, QHBoxLayout, QComboBox
    )

    widget = QWidget()
    layout = QVBoxLayout(widget)

    # 批量配置
    config_group = QGroupBox("批量配置")
    config_layout = QFormLayout(config_group)

    output_dir_edit = QLineEdit()
    output_dir_edit.setPlaceholderText("选择输出目录...")
    browse_btn = QPushButton("浏览")

    output_layout = QHBoxLayout()
    output_layout.addWidget(output_dir_edit, 1)
    output_layout.addWidget(browse_btn)

    preset_combo = QComboBox()
    preset_combo.setMinimumWidth(200)

    config_layout.addRow("输出目录:", output_layout)
    config_layout.addRow("导出预设:", preset_combo)

    # 项目列表
    projects_group = QGroupBox("项目列表")
    projects_layout = QVBoxLayout(projects_group)

    projects_table = create_batch_projects_table(parent_widget)
    projects_layout.addWidget(projects_table)

    # 批量操作按钮
    batch_actions_layout = QHBoxLayout()
    select_all_btn = QPushButton("全选")
    select_none_btn = QPushButton("全不选")
    batch_export_btn = QPushButton("批量导出")

    if on_select_all:
        select_all_btn.clicked.connect(on_select_all)
    if on_select_none:
        select_none_btn.clicked.connect(on_select_none)
    if on_batch_export:
        batch_export_btn.clicked.connect(on_batch_export)

    batch_actions_layout.addWidget(select_all_btn)
    batch_actions_layout.addWidget(select_none_btn)
    batch_actions_layout.addStretch()
    batch_actions_layout.addWidget(batch_export_btn)

    # 添加到布局
    layout.addWidget(config_group)
    layout.addWidget(projects_group)
    layout.addLayout(batch_actions_layout)
    layout.addStretch()

    return {
        'widget': widget,
        'output_dir_edit': output_dir_edit,
        'browse_btn': browse_btn,
        'preset_combo': preset_combo,
        'projects_table': projects_table,
        'select_all_btn': select_all_btn,
        'select_none_btn': select_none_btn,
        'batch_export_btn': batch_export_btn
    }


def get_selected_projects(projects_table) -> List[Dict[str, Any]]:
    """
    从项目表格获取选中的项目
    """
    from PySide6.QtCore import Qt

    selected_projects = []
    for i in range(projects_table.rowCount()):
        checkbox = projects_table.cellWidget(i, 0)
        if checkbox and checkbox.isChecked():
            selected_projects.append({
                "id": projects_table.item(i, 1).data(Qt.ItemDataRole.UserRole),
                "name": projects_table.item(i, 1).text(),
                "duration": projects_table.item(i, 2).text(),
                "resolution": projects_table.item(i, 3).text()
            })
    return selected_projects


def populate_batch_projects_table(table, projects: List[Dict[str, Any]]):
    """
    填充批量项目表格数据
    """
    from PySide6.QtWidgets import QCheckBox, QTableWidgetItem
    from PySide6.QtCore import Qt

    table.setRowCount(len(projects))
    for i, project in enumerate(projects):
        checkbox = QCheckBox()
        table.setCellWidget(i, 0, checkbox)

        name_item = QTableWidgetItem(project.get("name", ""))
        name_item.setData(Qt.ItemDataRole.UserRole, project.get("id"))
        table.setItem(i, 1, name_item)
        table.setItem(i, 2, QTableWidgetItem(project.get("duration", "00:00:00")))
        table.setItem(i, 3, QTableWidgetItem(project.get("resolution", "1920x1080")))
