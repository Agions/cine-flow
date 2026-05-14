#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alert management - extracted from monitor_panel.py"""

import logging
import time as time_module
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main.components.monitor_models import AlertData

logger = logging.getLogger(__name__)


class MonitorAlertManager:
    """Manages alert lifecycle: generate, add, filter, clear."""

    def __init__(self, alerts: List["AlertData"]):
        self._alerts = alerts
        self.logger = logger

    def generate_alerts(
        self,
        service_health: dict,
    ) -> None:
        """Scan service health and generate new alerts for threshold violations."""
        current_time = time_module.time()

        for service_name, health in service_health.items():
            status_str = str(health.status)

            if status_str == "error":
                self._add_alert(
                    service_name=service_name,
                    level="error",
                    message="服务出现错误，请检查配置",
                    details={"error_rate": getattr(health, "error_rate", 0), "last_check": getattr(health, "last_check", None)},
                )

            elif getattr(health, "error_rate", 0) > 0.1:
                self._add_alert(
                    service_name=service_name,
                    level="warning",
                    message=f"错误率过高: {getattr(health, 'error_rate', 0):.1%}",
                    details={"error_rate": getattr(health, "error_rate", 0)},
                )

            elif getattr(health, "response_time", 0) > 5000:
                self._add_alert(
                    service_name=service_name,
                    level="warning",
                    message=f"响应时间过长: {getattr(health, 'response_time', 0):.1f}ms",
                    details={"response_time": getattr(health, "response_time", 0)},
                )

    def _add_alert(
        self,
        service_name: str,
        level: str,
        message: str,
        details: dict = None,
    ) -> None:
        """Add alert if not already present (5-minute deduplication window)."""
        now = time_module.time()
        for existing in self._alerts:
            if (existing.service_name == service_name
                    and existing.level == level
                    and existing.message == message
                    and not existing.resolved
                    and now - existing.timestamp < 300):
                return

        from app.ui.main.components.monitor_models import AlertData
        alert = AlertData(
            id=f"{service_name}_{level}_{int(now)}",
            service_name=service_name,
            level=level,
            message=message,
            timestamp=now,
            resolved=False,
            details=details or {},
        )
        self._alerts.append(alert)
        # Cap at 100 most-recent alerts
        if len(self._alerts) > 100:
            self._alerts[:] = self._alerts[-100:]

    def filter_by_level(
        self,
        alerts: List["AlertData"],
        filter_text: str,
    ) -> List["AlertData"]:
        """Return alerts matching the given level filter text."""
        level_map = {"信息": "info", "警告": "warning", "错误": "error", "严重": "critical"}
        if filter_text == "全部":
            return list(alerts)
        filter_level = level_map.get(filter_text)
        return [a for a in alerts if a.level == filter_level]

    def clear_resolved(self, alerts: List["AlertData"]) -> None:
        """Remove all resolved alerts in-place."""
        alerts[:] = [a for a in alerts if not a.resolved]
