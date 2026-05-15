#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-save helper - QTimer isolated here so ProjectService stays headless-safe."""

import logging

logger = logging.getLogger(__name__)

# Lazy import to avoid hard PySide6 dependency in the module namespace
_QTimer = None

def _get_qtimer():
    global _QTimer
    if _QTimer is None:
        try:
            from PySide6.QtCore import QTimer
            _QTimer = QTimer
        except ImportError:
            _QTimer = None  # headless: no auto-save
    return _QTimer


class AutoSaveHelper:
    """Wraps QTimer auto-save for ProjectManager. No-op if QTimer unavailable."""

    def __init__(self, interval_ms: int = 60000):
        QTimer_cls = _get_qtimer()
        if QTimer_cls is None:
            self._timer = None
            self._project_service = None
            logger.debug("No QTimer — auto-save disabled")
            return

        self._timer = QTimer_cls()
        self._timer.timeout.connect(self._on_timeout)
        self._timer.start(interval_ms)
        self._project_service = None
        self.logger = logger

    def attach(self, project_service) -> None:
        """Set the service to check on each tick."""
        self._project_service = project_service

    def _on_timeout(self) -> None:
        if self._project_service is None:
            return
        current = self._project_service.current_project
        if current and current.is_modified:
            interval = current.settings.auto_save_interval
            if interval <= 0:
                return
            elapsed = (current.metadata.modified_at - current._saved_at).total_seconds()
            if elapsed >= interval:
                self._project_service.save_project(current.id, auto_save=True)

    def stop(self) -> None:
        if self._timer is not None:
            self._timer.stop()
