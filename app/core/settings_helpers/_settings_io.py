#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Settings I/O - extracted from settings_manager.py"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SettingsIO:
    """Handles settings and profiles persistence: load/save/merge."""

    def __init__(self, settings_file: str, profiles_file: str):
        self.settings_file = settings_file
        self.profiles_file = profiles_file
        self.logger = logger

    # -- Settings I/O --------------------------------------------------------

    def load_settings(
        self,
        settings: Dict[str, Any],
        settings_definitions: Dict[str, Any],
    ) -> None:
        """Load settings from file, applying defaults first, then overrides."""
        # Apply defaults
        for key, definition in settings_definitions.items():
            settings[key] = definition.default_value

        # Load from file
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                # Merge (file overrides defaults)
                for key, value in loaded.items():
                    if key in settings_definitions:
                        settings[key] = value
                self.logger.info("Project settings loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to load settings: {e}")

    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Persist settings (excluding builtin defaults) to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")

    def save_json_file(self, file_path: str, data: Any) -> None:
        """Write arbitrary data to a JSON file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save {file_path}: {e}")

    # -- Profile I/O ---------------------------------------------------------

    def load_profiles(
        self,
        profiles: Dict[str, Any],
        profiles_data: Dict[str, Any],
    ) -> None:
        """Populate profiles dict from JSON data."""
        try:
            for name, profile_data in profiles_data.items():
                from app.core.settings_models import ProjectSettingsProfile
                profile = ProjectSettingsProfile(**profile_data)
                profiles[name] = profile
            self.logger.info("Project profiles loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load profiles: {e}")

    def save_profiles(self, profiles: Dict[str, Any]) -> None:
        """Persist profiles (excluding builtin) to JSON."""
        try:
            os.makedirs(os.path.dirname(self.profiles_file), exist_ok=True)
            data = {
                name: p.to_dict()
                for name, p in profiles.items()
                if not getattr(p, 'is_builtin', False)
            }
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save profiles: {e}")

    def export_settings_to_file(
        self,
        settings: Dict[str, Any],
        profiles: Dict[str, Any],
        export_path: str,
        profile_name: str = None,
    ) -> bool:
        """Export current settings or a named profile to a JSON file."""
        try:
            export_data = {}
            if profile_name and profile_name in profiles:
                profile = profiles[profile_name]
                export_data = dict(profile.settings)
                export_data['_profile_name'] = profile_name
                export_data['_description'] = profile.description
            else:
                export_data = dict(settings)
                export_data['_profile_name'] = 'custom'
                export_data['_description'] = 'Custom settings export'

            Path(export_path).parent.mkdir(parents=True, exist_ok=True)
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Settings exported to {export_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export settings: {e}")
            return False

    def import_settings_from_file(
        self,
        settings: Dict[str, Any],
        settings_definitions: Dict[str, Any],
        import_path: str,
        merge: bool = True,
    ) -> bool:
        """Load settings from a JSON file, optionally merging with existing."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)

            imported.pop('_profile_name', None)
            imported.pop('_description', None)

            if merge:
                for key, value in imported.items():
                    if key in settings_definitions:
                        settings[key] = value
            else:
                settings.clear()
                for key, value in imported.items():
                    if key in settings_definitions:
                        settings[key] = value

            self.logger.info(f"Settings imported from {import_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to import settings: {e}")
            return False
