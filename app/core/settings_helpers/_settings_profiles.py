#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Profile management - extracted from settings_manager.py"""

import logging
from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.settings_models import ProjectSettingsProfile

logger = logging.getLogger(__name__)


class ProfileManager:
    """Manages settings profiles: create, apply, delete, filter."""

    def __init__(
        self,
        profiles: Dict[str, "ProjectSettingsProfile"],
        settings: Dict[str, Any],
        settings_definitions: Dict[str, Any],
    ):
        self._profiles = profiles
        self._settings = settings
        self._defs = settings_definitions
        self.logger = logger

    def create_profile(
        self,
        name: str,
        description: str,
        settings_filter: List[str] = None,
    ) -> bool:
        """Create a new profile snapshotting current settings."""
        from app.core.settings_models import ProjectSettingsProfile

        profile_settings = (
            {k: v for k, v in self._settings.items() if k in settings_filter}
            if settings_filter
            else deepcopy(self._settings)
        )
        profile = ProjectSettingsProfile(
            name=name,
            description=description,
            settings=profile_settings,
            created_at=datetime.now().isoformat(),
            modified_at=datetime.now().isoformat(),
        )
        self._profiles[name] = profile
        self.logger.info(f"Created profile: {name}")
        return True

    def apply_profile(
        self,
        profile_name: str,
    ) -> List[tuple]:
        """Apply a profile's settings to current settings. Returns list of (key, old, new)."""
        if profile_name not in self._profiles:
            return []

        profile = self._profiles[profile_name]
        from app.core.settings_helpers import SettingsValidator

        validator = SettingsValidator(self._defs)
        changes = []

        for key, value in profile.settings.items():
            if key in self._defs and validator.validate(key, value):
                old = self._settings.get(key)
                if old != value:
                    self._settings[key] = value
                    changes.append((key, old, value))

        self.logger.info(f"Applied profile: {profile_name}")
        return changes

    def delete_profile(self, profile_name: str) -> bool:
        """Delete a user profile. Returns False if builtin or missing."""
        if profile_name not in self._profiles:
            return False
        if getattr(self._profiles[profile_name], 'is_builtin', False):
            return False
        del self._profiles[profile_name]
        self.logger.info(f"Deleted profile: {profile_name}")
        return True

    def filter_by_tag(
        self,
        tag: str,
    ) -> List["ProjectSettingsProfile"]:
        """Return profiles matching the given tag."""
        return [
            p for p in self._profiles.values()
            if tag in (getattr(p, 'tags', []) or [])
        ]

    def search_profiles(
        self,
        query: str,
    ) -> List["ProjectSettingsProfile"]:
        """Full-text search across profile names and descriptions."""
        q = query.lower()
        return [
            p for p in self._profiles.values()
            if q in p.name.lower() or q in p.description.lower()
        ]
