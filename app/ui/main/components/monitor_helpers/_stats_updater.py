#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stats and performance updaters - extracted from monitor_panel.py"""

import logging
import random

logger = logging.getLogger(__name__)


def update_stats(panel):
    """Update statistics for overview and usage tables."""
    try:
        if not panel.ai_service_manager:
            return

        summary = panel.ai_service_manager.get_summary()

        # Update overview page stats
        if hasattr(panel, 'service_stats_label'):
            panel.service_stats_label.setText(f"{summary['active_services']}/{summary['total_services']}")
            panel.requests_stats_label.setText(str(summary['total_requests']))

            # Calculate success rate
            total_requests = summary.get('total_requests', 0)
            successful_requests = summary.get('successful_requests', 0)
            success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 100
            panel.success_stats_label.setText(f"{success_rate:.1f}%")

            # Calculate average response time
            avg_response_time = calculate_avg_response_time(panel)
            panel.response_stats_label.setText(f"{avg_response_time:.1f}ms")

            panel.cost_stats_label.setText(f"¥{summary['total_cost']:.2f}")
            panel.alerts_stats_label.setText(str(len([a for a in panel.alerts if not a.resolved])))

        # Update usage table
        update_usage_table(panel)

    except Exception as e:
        panel.logger.error(f"更新统计数据失败: {e}")


def calculate_avg_response_time(panel) -> float:
    """Calculate average response time across all services."""
    try:
        if not panel.ai_service_manager:
            return 0.0

        total_time = 0
        count = 0

        for health in panel.ai_service_manager.service_health.values():
            if health.response_time > 0:
                total_time += health.response_time
                count += 1

        return total_time / count if count > 0 else 0.0

    except Exception as e:
        panel.logger.error(f"计算平均响应时间失败: {e}")
        return 0.0


def update_usage_table(panel):
    """Update usage statistics table."""
    try:
        if not panel.ai_service_manager:
            return

        stats = panel.ai_service_manager.usage_stats
        panel.usage_table.setRowCount(len(stats))

        for row, (service_name, stat) in enumerate(stats.items()):
            panel.usage_table.setItem(row, 0, QTableWidgetItem(service_name))
            panel.usage_table.setItem(row, 1, QTableWidgetItem(str(stat.total_requests)))
            panel.usage_table.setItem(row, 2, QTableWidgetItem(str(stat.successful_requests)))
            panel.usage_table.setItem(row, 3, QTableWidgetItem(str(stat.failed_requests)))
            panel.usage_table.setItem(row, 4, QTableWidgetItem(f"¥{stat.total_cost:.2f}"))

    except Exception as e:
        panel.logger.error(f"更新使用量表格失败: {e}")


def update_performance_data(panel):
    """Update performance charts with current metrics."""
    try:
        if not panel.ai_service_manager:
            return

        # Calculate current metrics
        response_time = calculate_avg_response_time(panel)
        error_rate = calculate_error_rate(panel)
        throughput = calculate_throughput(panel)

        # Update charts
        panel.response_time_chart.add_data_point(response_time)
        panel.error_rate_chart.add_data_point(error_rate * 100)
        panel.throughput_chart.add_data_point(throughput)

        panel.response_trend_chart.add_data_point(response_time)
        panel.error_trend_chart.add_data_point(error_rate * 100)
        panel.throughput_trend_chart.add_data_point(throughput)

        # Simulate CPU usage
        cpu_usage = random.uniform(10, 80)
        panel.cpu_usage_chart.add_data_point(cpu_usage)

    except Exception as e:
        panel.logger.error(f"更新性能数据失败: {e}")


def calculate_error_rate(panel) -> float:
    """Calculate overall error rate across all services."""
    try:
        if not panel.ai_service_manager:
            return 0.0

        total_errors = 0
        total_requests = 0

        for health in panel.ai_service_manager.service_health.values():
            total_errors += health.error_count
            total_requests += health.success_count + health.error_count

        return total_errors / total_requests if total_requests > 0 else 0.0

    except Exception as e:
        panel.logger.error(f"计算错误率失败: {e}")
        return 0.0


def calculate_throughput(panel) -> float:
    """Calculate throughput (requests per hour)."""
    try:
        if not panel.ai_service_manager:
            return 0.0

        total_requests = sum(
            stat.total_requests for stat in panel.ai_service_manager.usage_stats.values()
        )
        return total_requests / 3600  # Assuming stats cover 1 hour

    except Exception as e:
        panel.logger.error(f"计算吞吐量失败: {e}")
        return 0.0


from PySide6.QtWidgets import QTableWidgetItem  # noqa: E402
