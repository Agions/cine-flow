#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Services table and status - extracted from monitor_panel.py"""

import logging
from PySide6.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QColor

from ....services import ServiceStatus

logger = logging.getLogger(__name__)


def update_services_status(panel):
    """Update service status - wrapper for status list and table."""
    try:
        if not panel.ai_service_manager:
            return
        update_services_status_list(panel)
        update_services_table(panel)
    except Exception as e:
        panel.logger.error(f"更新服务状态失败: {e}")


def update_services_status_list(panel):
    """Update the overview services status list."""
    try:
        # Clear existing widgets
        while panel.services_status_layout.count():
            item = panel.services_status_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new service status widgets
        if panel.ai_service_manager:
            from .monitor_widgets import ServiceStatusWidget
            for service_name, health in panel.ai_service_manager.service_health.items():
                status_widget = ServiceStatusWidget(
                    service_name, health.status, health.__dict__
                )
                panel.services_status_layout.addWidget(status_widget)

    except Exception as e:
        panel.logger.error(f"更新服务状态列表失败: {e}")


def update_services_table(panel):
    """Update the services detail table."""
    try:
        if not panel.ai_service_manager:
            return

        services = panel.ai_service_manager.get_all_services()
        panel.services_table.setRowCount(len(services))

        for row, (service_name, _) in enumerate(services.items()):
            health = panel.ai_service_manager.get_service_health(service_name)
            stats = panel.ai_service_manager.get_usage_stats(service_name)

            # Service name
            panel.services_table.setItem(row, 0, QTableWidgetItem(service_name))

            # Status
            status_item = QTableWidgetItem(health.status.value if health else "未知")
            status_color = _get_service_status_color(health)
            status_item.setBackground(QColor(status_color))
            panel.services_table.setItem(row, 1, status_item)

            # Response time
            response_time = health.response_time if health else 0
            panel.services_table.setItem(row, 2, QTableWidgetItem(f"{response_time:.1f}ms"))

            # Error rate
            error_rate = health.error_rate if health else 0
            panel.services_table.setItem(row, 3, QTableWidgetItem(f"{error_rate:.1%}"))

            # Success rate
            success_rate = (stats.successful_requests / stats.total_requests * 100) if stats and stats.total_requests > 0 else 100
            panel.services_table.setItem(row, 4, QTableWidgetItem(f"{success_rate:.1f}%"))

            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)

            test_btn = QPushButton("测试")
            test_btn.setFixedSize(60, 24)
            test_btn.clicked.connect(lambda checked, sn=service_name: panel._test_service(sn))
            actions_layout.addWidget(test_btn)

            details_btn = QPushButton("详情")
            details_btn.setFixedSize(60, 24)
            details_btn.clicked.connect(lambda checked, sn=service_name: panel._show_service_details(sn))
            actions_layout.addWidget(details_btn)

            panel.services_table.setCellWidget(row, 5, actions_widget)

    except Exception as e:
        panel.logger.error(f"更新服务表格失败: {e}")


def _get_service_status_color(health) -> str:
    """Get color for service status."""
    if not health:
        return "#888888"
    return {
        ServiceStatus.ACTIVE: "#52c41a",
        ServiceStatus.INACTIVE: "#888888",
        ServiceStatus.ERROR: "#ff4d4f",
        ServiceStatus.MAINTENANCE: "#faad14"
    }.get(health.status, "#888888")
