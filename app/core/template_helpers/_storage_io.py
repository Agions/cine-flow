#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Template storage and I/O - extracted from project_template_manager.py"""

import json
import logging
from pathlib import Path
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.project_template_manager import TemplateInfo

logger = logging.getLogger(__name__)


class TemplateStorageIO:
    """Handles template persistence: load/save user templates and builtin templates."""

    def __init__(self, templates_dir: Path, builtin_templates_dir: Path):
        self.templates_dir = templates_dir
        self.builtin_templates_dir = builtin_templates_dir
        self.logger = logger

    def load_templates(self, templates: Dict[str, "TemplateInfo"]) -> None:
        """Load user templates from templates.json index."""
        try:
            if not self.templates_dir.exists():
                return

            index_file = self.templates_dir / "templates.json"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    templates_data = json.load(f)
                    for template_id, template_data in templates_data.items():
                        from app.core.template_models import TemplateInfo as TI
                        template_info = TI.from_dict(template_data)
                        templates[template_id] = template_info

            self.logger.info(f"Loaded {len(templates)} user templates")
        except Exception as e:
            self.logger.error(f"Failed to load templates: {e}")

    def load_builtin_templates(
        self,
        templates: Dict[str, "TemplateInfo"],
        builtin_templates_dir: Path,
    ) -> None:
        """Scan builtin templates directory and add any not already loaded."""
        try:
            if not builtin_templates_dir.exists():
                return

            from app.core.template_models import TemplateInfo as TI

            for template_dir in builtin_templates_dir.iterdir():
                if not template_dir.is_dir():
                    continue
                info_file = template_dir / "template_info.json"
                if not info_file.exists():
                    continue
                try:
                    with open(info_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    template_info = TI.from_dict(template_data)
                    template_info.is_builtin = True
                    if template_info.id not in templates:
                        templates[template_info.id] = template_info
                except Exception as e:
                    self.logger.warning(f"Failed to load builtin template {template_dir}: {e}")

            self.logger.info(
                f"Loaded {sum(1 for t in templates.values() if t.is_builtin)} builtin templates"
            )
        except Exception as e:
            self.logger.error(f"Failed to load builtin templates: {e}")

    def save_templates(self, templates: Dict[str, "TemplateInfo"]) -> None:
        """Serialize user (non-builtin) templates to templates.json."""
        try:
            index_file = self.templates_dir / "templates.json"
            data = {
                tid: t.to_dict()
                for tid, t in templates.items()
                if not t.is_builtin
            }
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save templates: {e}")

    def ensure_directories(self, templates_dir: Path, temp_dir: Path) -> None:
        """Create required directories if they don't exist."""
        for directory in [templates_dir, temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def calculate_directory_size(self, directory: Path) -> int:
        """Sum the size of all files under directory."""
        import os
        try:
            total_size = 0
            for dirpath, _, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
            return total_size
        except Exception as e:
            self.logger.error(f"Failed to calculate directory size: {e}")
            return 0
