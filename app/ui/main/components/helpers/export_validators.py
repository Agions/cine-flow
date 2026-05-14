#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导出验证助手
提供导出相关的验证逻辑
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


def validate_export_request(
    parent_widget: "QWidget",
    current_project_id: str,
    preset_combo,
    output_path_edit
) -> tuple:
    """
    验证导出请求

    Returns:
        tuple of (is_valid, preset_id, output_path, error_message)
    """
    from PySide6.QtWidgets import QMessageBox

    if not current_project_id:
        QMessageBox.warning(parent_widget, "警告", "请先选择一个项目")
        return False, None, None, "No project selected"

    output_path = output_path_edit.text()
    if not output_path:
        QMessageBox.warning(parent_widget, "警告", "请选择输出路径")
        return False, None, None, "No output path"

    preset_id = preset_combo.currentData()
    if not preset_id:
        QMessageBox.warning(parent_widget, "警告", "请选择导出预设")
        return False, None, None, "No preset selected"

    return True, preset_id, output_path, None


def validate_batch_export_request(
    parent_widget: "QWidget",
    batch_projects_table,
    batch_output_dir_edit,
    batch_preset_combo
) -> tuple:
    """
    验证批量导出请求

    Returns:
        tuple of (is_valid, selected_projects, output_dir, preset_id)
    """
    from PySide6.QtWidgets import QMessageBox

    selected_projects = get_selected_projects_from_table(batch_projects_table)
    if not selected_projects:
        QMessageBox.warning(parent_widget, "警告", "请选择要导出的项目")
        return False, None, None, None

    output_dir = batch_output_dir_edit.text()
    if not output_dir:
        QMessageBox.warning(parent_widget, "警告", "请选择输出目录")
        return False, None, None, None

    preset_id = batch_preset_combo.currentData()
    if not preset_id:
        QMessageBox.warning(parent_widget, "警告", "请选择导出预设")
        return False, None, None, None

    return True, selected_projects, output_dir, preset_id


def get_selected_projects_from_table(table) -> list:
    """从项目表格获取选中的项目"""
    from PySide6.QtCore import Qt

    selected = []
    for i in range(table.rowCount()):
        checkbox = table.cellWidget(i, 0)
        if checkbox and checkbox.isChecked():
            selected.append({
                "id": table.item(i, 1).data(Qt.ItemDataRole.UserRole),
                "name": table.item(i, 1).text(),
                "duration": table.item(i, 2).text(),
                "resolution": table.item(i, 3).text()
            })
    return selected


def show_export_success(parent_widget: "QWidget", message: str):
    """显示导出成功消息"""
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.information(parent_widget, "成功", message)


def show_export_error(parent_widget: "QWidget", error: str):
    """显示导出错误消息"""
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.critical(parent_widget, "错误", f"导出失败: {error}")


def show_operation_error(parent_widget: "QWidget", operation: str, error: str):
    """显示操作错误消息"""
    from PySide6.QtWidgets import QMessageBox
    QMessageBox.critical(parent_widget, "错误", f"{operation}失败: {error}")
