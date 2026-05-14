#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Template file operations - extracted from project_template_manager.py"""

import json
import shutil
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class TemplateFileOps:
    """Handles template file copy/apply operations."""

    def __init__(self):
        self.logger = logger

    def copy_project_to_template(self, project_path: str, template_dir: Path) -> None:
        """Copy project files into a new template directory."""
        import os
        try:
            # Project config
            project_file = os.path.join(project_path, 'project.json')
            if os.path.exists(project_file):
                shutil.copy2(project_file, template_dir / 'project_template.json')

            # Media files
            media_source = Path(project_path) / 'media'
            if media_source.exists():
                shutil.copytree(media_source, template_dir / 'media', dirs_exist_ok=True)

            # Asset files
            assets_source = Path(project_path) / 'assets'
            if assets_source.exists():
                shutil.copytree(assets_source, template_dir / 'assets', dirs_exist_ok=True)
        except Exception as e:
            self.logger.error(f"Failed to copy project to template: {e}")

    def copy_template_to_project(
        self,
        template_path: Path,
        project_dir: Path,
        variables: Dict[str, Any],
    ) -> None:
        """Copy template skeleton into a new project, applying variable substitution."""
        # Template project file
        template_project_file = template_path / 'project_template.json'
        if template_project_file.exists():
            with open(template_project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)

            self._apply_variables(project_data, variables)

            if 'metadata' in project_data:
                project_data['metadata']['name'] = variables.get('project_name', 'Untitled Project')
                project_data['metadata']['created_at'] = datetime.now().isoformat()
                project_data['metadata']['modified_at'] = datetime.now().isoformat()

            with open(project_dir / 'project.json', 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)

        # Media
        media_source = template_path / 'media'
        if media_source.exists():
            shutil.copytree(media_source, project_dir / 'media', dirs_exist_ok=True)

        # Assets
        assets_source = template_path / 'assets'
        if assets_source.exists():
            shutil.copytree(assets_source, project_dir / 'assets', dirs_exist_ok=True)

        # Other files (skip metadata files)
        skip = {'project_template.json', 'template_metadata.json', 'template_info.json'}
        for file_path in template_path.rglob('*'):
            if file_path.is_file() and file_path.name not in skip:
                rel = file_path.relative_to(template_path)
                dest = project_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest)

    def _apply_variables(self, project_data: Dict[str, Any], variables: Dict[str, Any]) -> None:
        """Recursively substitute ${var} placeholders in project_data."""
        def replace(obj):
            if isinstance(obj, dict):
                return {k: replace(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace(item) for item in obj]
            elif isinstance(obj, str):
                for name, value in variables.items():
                    obj = obj.replace(f"${{{name}}}", str(value))
                return obj
            return obj
        replace(project_data)
