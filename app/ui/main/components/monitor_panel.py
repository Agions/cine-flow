#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI状态监控面板
实时监控AI服务的运行状态、性能指标和使用情况
"""

from typing import Dict, List
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget,
    QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import QTimer, Signal, Qt

from ....core.logger import Logger
from ....core.icon_manager import get_icon
from ....core.application import Application

from .monitor_models import MonitorMode, AlertData
from .monitor_widgets import AlertWidget
from .monitor_pages import MonitorPages
from .monitor_helpers import (
    MonitorAlertManager,
    update_services_status,
    update_services_status_list,
    update_services_table as _update_services_table_impl,
    update_stats,
    update_usage_table,
    update_performance_data,
    calculate_avg_response_time,
    calculate_error_rate,
    calculate_throughput,
)


class AIMonitorPanel(QWidget):
    """AI状态监控面板"""

    # 信号定义
    service_selected = Signal(str)
    alert_selected = Signal(AlertData)
    refresh_requested = Signal()

    def __init__(self, application: Application):
        super().__init__()
        self.application = application
        self.logger = application.get_service(Logger)
        self.ai_service_manager = None
        self.current_mode = MonitorMode.OVERVIEW
        self.alerts: List[AlertData] = []
        self.performance_data: Dict[str, List[float]] = {}

        # Alert manager helper
        self._alert_manager = MonitorAlertManager(self.alerts)

        # 获取AI服务管理器
        self._get_ai_service_manager()

        # 定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_monitor_data)
        self.update_timer.start(5000)  # 5秒更新一次

        # 页面创建助手
        self.pages = MonitorPages(self)

        self._init_ui()
        self._setup_connections()

    def _get_ai_service_manager(self):
        """获取AI服务管理器"""
        try:
            self.ai_service_manager = self.application.get_service_by_name("ai_service_manager")
            if not self.ai_service_manager:
                self.logger.warning("AI服务管理器未注册")
        except Exception as e:
            self.logger.error(f"获取AI服务管理器失败: {e}")

    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 模式切换栏
        mode_bar = QFrame()
        mode_bar.setFrameShape(QFrame.Shape.StyledPanel)
        mode_bar.setProperty("class", "monitor-mode-bar")
        mode_layout = QHBoxLayout(mode_bar)
        mode_layout.setContentsMargins(10, 10, 10, 10)

        # 模式按钮
        mode_buttons = []
        mode_list = [
            (MonitorMode.OVERVIEW, "概览"),
            (MonitorMode.SERVICES, "服务"),
            (MonitorMode.PERFORMANCE, "性能"),
            (MonitorMode.USAGE, "使用量"),
            (MonitorMode.ALERTS, "告警"),
        ]
        for mode_key, mode_text in mode_list:
            btn = QPushButton(mode_text)
            btn.setFixedSize(80, 30)
            btn.setCheckable(True)
            btn.setProperty("class", "monitor-mode-button")
            btn.clicked.connect(lambda checked, m=mode_key: self._switch_mode(m))
            mode_layout.addWidget(btn)
            mode_buttons.append(btn)

        # 设置默认按钮
        mode_buttons[0].setChecked(True)
        mode_buttons[0].setProperty("class", "monitor-mode-button active")
        self.mode_buttons = mode_buttons

        mode_layout.addStretch()

        # 刷新按钮
        refresh_btn = QPushButton(get_icon("refresh", 16), "刷新")
        refresh_btn.setFixedSize(80, 30)
        refresh_btn.setProperty("class", "monitor-refresh-button")
        refresh_btn.clicked.connect(self._refresh_data)
        mode_layout.addWidget(refresh_btn)

        layout.addWidget(mode_bar)

        # 内容区域
        self.content_stack = QStackedWidget()
        self.content_stack.setProperty("class", "monitor-content-stack")

        # 创建各个模式的内容页面
        self.overview_page = self.pages.create_overview_page()
        self.services_page = self.pages.create_services_page()
        self.performance_page = self.pages.create_performance_page()
        self.usage_page = self.pages.create_usage_page()
        self.alerts_page = self.pages.create_alerts_page()

        self.content_stack.addWidget(self.overview_page)
        self.content_stack.addWidget(self.services_page)
        self.content_stack.addWidget(self.performance_page)
        self.content_stack.addWidget(self.usage_page)
        self.content_stack.addWidget(self.alerts_page)

        layout.addWidget(self.content_stack)

    def _get_mode_text(self, mode) -> str:
        """获取模式文本"""
        mode_texts = {
            MonitorMode.OVERVIEW: "概览",
            MonitorMode.SERVICES: "服务",
            MonitorMode.PERFORMANCE: "性能",
            MonitorMode.USAGE: "使用量",
            MonitorMode.ALERTS: "告警"
        }
        return mode_texts.get(mode, "未知")

    def _switch_mode(self, mode):
        """切换模式"""
        self.current_mode = mode

        # 更新按钮状态
        for btn in self.mode_buttons:
            btn.setChecked(btn.text() == self._get_mode_text(mode))

        # 切换页面
        page_index = {
            MonitorMode.OVERVIEW: 0,
            MonitorMode.SERVICES: 1,
            MonitorMode.PERFORMANCE: 2,
            MonitorMode.USAGE: 3,
            MonitorMode.ALERTS: 4
        }.get(mode, 0)

        self.content_stack.setCurrentIndex(page_index)

    def _setup_connections(self):
        """设置信号连接"""
        # 连接AI服务管理器信号
        if self.ai_service_manager:
            self.ai_service_manager.service_health_updated.connect(self._on_service_health_updated)
            self.ai_service_manager.stats_updated.connect(self._on_stats_updated)

    # -------------------------------------------------------------------------
    # Data Update Methods
    # -------------------------------------------------------------------------

    def _update_monitor_data(self):
        """更新监控数据"""
        try:
            if not self.ai_service_manager:
                return

            # 更新服务状态
            self._update_services_status()

            # 更新统计数据
            self._update_stats()

            # 更新性能数据
            self._update_performance_data()

            # 更新告警
            self._update_alerts()

        except Exception as e:
            self.logger.error(f"更新监控数据失败: {e}")

    def _update_services_status(self):
        """Update service status (delegated)"""
        update_services_status(self)

    def _update_services_status_list(self):
        """Update service status list (delegated)"""
        update_services_status_list(self)

    def _update_services_table(self):
        """Update services table (delegated)"""
        _update_services_table_impl(self)

    def _update_stats(self):
        """Update statistics (delegated)"""
        update_stats(self)

    def _calculate_avg_response_time(self) -> float:
        """Calculate average response time (delegated)"""
        return calculate_avg_response_time(self)

    def _update_usage_table(self):
        """Update usage table (delegated)"""
        update_usage_table(self)

    def _update_performance_data(self):
        """Update performance data (delegated)"""
        update_performance_data(self)

    def _calculate_error_rate(self) -> float:
        """Calculate error rate (delegated)"""
        return calculate_error_rate(self)

    def _calculate_throughput(self) -> float:
        """Calculate throughput (delegated)"""
        return calculate_throughput(self)

    # -------------------------------------------------------------------------
    # Alert Methods
    # -------------------------------------------------------------------------

    def _update_alerts(self):
        """更新告警"""
        try:
            if not self.ai_service_manager:
                return

            # 生成告警
            self._generate_alerts()

            # 更新告警列表
            self._update_alerts_list()

        except Exception as e:
            self.logger.error(f"更新告警失败: {e}")

    def _generate_alerts(self):
        """生成告警"""
        try:
            if not self.ai_service_manager:
                return
            self._alert_manager.generate_alerts(
                self.ai_service_manager.service_health,
            )
        except Exception as e:
            self.logger.error(f"生成告警失败: {e}")

    def _add_alert(self, alert: AlertData):
        """添加告警（保持向后兼容）"""
        self._alert_manager._add_alert(
            service_name=alert.service_name,
            level=alert.level,
            message=alert.message,
            details=alert.details,
        )

    def _update_alerts_list(self):
        """更新告警列表"""
        try:
            # 清除现有部件
            while self.alerts_layout.count():
                item = self.alerts_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # 获取过滤器
            filter_text = self.alert_filter_combo.currentText()
            if filter_text == "全部":
                filtered_alerts = self.alerts
            else:
                level_map = {
                    "信息": "info",
                    "警告": "warning",
                    "错误": "error",
                    "严重": "critical"
                }
                filter_level = level_map.get(filter_text)
                filtered_alerts = [a for a in self.alerts if a.level == filter_level]

            # 按时间排序
            filtered_alerts.sort(key=lambda x: x.timestamp, reverse=True)

            # 添加告警部件
            for alert in filtered_alerts[:20]:  # 只显示最近20个
                alert_widget = AlertWidget(alert)
                alert_widget.alert_clicked.connect(self.alert_selected)
                self.alerts_layout.addWidget(alert_widget)

            if not filtered_alerts:
                no_alerts_label = QLabel("暂无告警")
                no_alerts_label.setProperty("class", "no-alerts-label")
                no_alerts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.alerts_layout.addWidget(no_alerts_label)

        except Exception as e:
            self.logger.error(f"更新告警列表失败: {e}")

    def _filter_alerts(self, filter_text: str):
        """过滤告警"""
        self._update_alerts_list()

    def _clear_resolved_alerts(self):
        """清除已解决的告警"""
        self.alerts = [a for a in self.alerts if not a.resolved]
        self._update_alerts_list()

    # -------------------------------------------------------------------------
    # Service Actions
    # -------------------------------------------------------------------------

    def _test_service(self, service_name: str):
        """测试服务"""
        try:
            if self.ai_service_manager:
                # 测试第一个配置的模型
                configured_models = self.ai_service_manager.get_configured_models()
                if service_name in configured_models and configured_models[service_name]:
                    model_id = configured_models[service_name][0]
                    success = self.ai_service_manager.test_connection(service_name, model_id)

                    if success:
                        QMessageBox.information(self, "测试成功", f"{service_name} 连接测试成功")
                    else:
                        QMessageBox.warning(self, "测试失败", f"{service_name} 连接测试失败")
                else:
                    QMessageBox.warning(self, "未配置", f"{service_name} 未配置模型")
        except Exception as e:
            QMessageBox.critical(self, "测试错误", f"测试服务失败: {e}")

    def _show_service_details(self, service_name: str):
        """显示服务详情"""
        try:
            if not self.ai_service_manager:
                return

            health = self.ai_service_manager.get_service_health(service_name)
            stats = self.ai_service_manager.get_usage_stats(service_name)

            rt = f"{health.response_time:.1f}ms" if health else "N/A"
            er = f"{health.error_rate:.1%}" if health else "N/A"
            last_check = datetime.fromtimestamp(health.last_check).strftime('%Y-%m-%d %H:%M:%S') if health else "N/A"
            success_count = stats.successful_requests if stats else 0
            total_count = stats.total_requests if stats else 0
            cost = f"¥{stats.total_cost:.2f}" if stats else "N/A"

            details = (
                f"服务名称: {service_name}\n"
                f"状态: {(health.status.value if health else '未知')}\n"
                f"响应时间: {rt}\n"
                f"错误率: {er}\n"
                f"成功率: {success_count}/{total_count}\n"
                f"总成本: {cost}\n"
                f"最后检查: {last_check}"
            )

            QMessageBox.information(self, "服务详情", details)

        except Exception as e:
            QMessageBox.critical(self, "详情错误", f"获取服务详情失败: {e}")

    # -------------------------------------------------------------------------
    # Signal Handlers & Lifecycle
    # -------------------------------------------------------------------------

    def _refresh_data(self):
        """刷新数据"""
        self._update_monitor_data()

    def _on_service_health_updated(self, service_name: str, health_data: object):
        """服务健康状态更新处理"""
        self._update_services_status()

    def _on_stats_updated(self, stats: object):
        """统计数据更新处理"""
        self._update_stats()

    def refresh(self):
        """刷新面板"""
        self._update_monitor_data()

    def cleanup(self):
        """清理资源"""
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()

    def __del__(self):
        """析构函数"""
        self.cleanup()
