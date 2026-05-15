#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Settings validation - extracted from settings_manager.py"""

import logging
import re
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.settings_models import SettingDefinition

logger = logging.getLogger(__name__)


class SettingsValidator:
    """Validates setting values against definitions."""

    def __init__(self, settings_definitions: dict):
        self._defs = settings_definitions
        self.logger = logger

    def validate(self, key: str, value: Any) -> bool:
        """Return True if value is valid for the given setting key."""
        if key not in self._defs:
            return False

        definition = self._defs[key]
        return (
            self._check_type(definition, value)
            and self._check_range(definition, value)
            and self._check_options(definition, value)
            and self._check_custom(definition, key, value)
        )

    def _check_type(self, definition: "SettingDefinition", value: Any) -> bool:
        """Type-check value against definition.setting_type."""
        from app.core.settings_models import SettingType
        try:
            if definition.setting_type == SettingType.STRING:
                return isinstance(value, str)
            elif definition.setting_type == SettingType.INTEGER:
                return isinstance(value, int)
            elif definition.setting_type == SettingType.FLOAT:
                return isinstance(value, (int, float))
            elif definition.setting_type == SettingType.BOOLEAN:
                return isinstance(value, bool)
            elif definition.setting_type == SettingType.LIST:
                return isinstance(value, list)
            elif definition.setting_type == SettingType.DICT:
                return isinstance(value, dict)
        except Exception:
            pass
        return True  # Unknown type → pass through

    def _check_range(self, definition: "SettingDefinition", value: Any) -> bool:
        """Range check for numeric values."""
        if definition.min_value is not None and value < definition.min_value:
            return False
        if definition.max_value is not None and value > definition.max_value:
            return False
        return True

    def _check_options(self, definition: "SettingDefinition", value: Any) -> bool:
        """Option enumeration check."""
        if definition.options and value not in definition.options:
            return False
        return True

    def _check_custom(
        self,
        definition: "SettingDefinition",
        key: str,
        value: Any,
    ) -> bool:
        """Call a named custom validator method if defined."""
        if definition.validator:
            try:
                validator = getattr(self, definition.validator, None)
                if validator and not validator(value):
                    return False
            except Exception as e:
                self.logger.debug(f"Validator error for {key}: {e}")
                return False
        return True

    # -- Custom validators ----------------------------------------------------

    def validate_resolution(self, value: str) -> bool:
        """Validate resolution string like '1920x1080'."""
        if not isinstance(value, str):
            return False
        pattern = r'^\d{3,4}x\d{3,4}$'
        if not re.match(pattern, value):
            return False
        try:
            w, h = map(int, value.split('x'))
            return 0 < w <= 7680 and 0 < h <= 4320
        except Exception:
            return False

    def validate_path(self, value: str) -> bool:
        """Validate that path is safe (no ../ traversal)."""
        if not isinstance(value, str):
            return False
        if '..' in value or value.startswith('/') or ':' in value:
            return False
        return True

    def validate_color(self, value: str) -> bool:
        """Validate hex color string like '#FF5733'."""
        if not isinstance(value, str):
            return False
        return bool(re.match(r'^#[0-9A-Fa-f]{6}$', value))
