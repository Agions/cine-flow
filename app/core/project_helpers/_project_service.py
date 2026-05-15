#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ProjectService - pure business logic layer, no Qt signals."""

import json
import logging
import os
import shutil
import zipfile
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import psutil

from app.core.project_models import (
    Project, ProjectType, ProjectMetadata,
)


logger = logging.getLogger(__name__)


class ProjectService:
    """
    Pure business logic for project management.

    No QObject, no Qt signals. Safe to use in headless / CI environments.
    """

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = logger
        self.projects: Dict[str, Project] = {}
        self.current_project: Optional[Project] = None
        self.templates: Dict[str, Project] = {}
        self.projects_dir = os.path.expanduser("~/Voxplore/Projects")
        self.templates_dir = os.path.expanduser("~/Voxplore/Templates")
        self.temp_dir = os.path.expanduser("~/Voxplore/Temp")
        self.recent_projects: List[str] = self._load_recent_projects()
        self._ensure_directories()
        self._load_templates()

    # -- Directory / recent projects --

    def _ensure_directories(self) -> None:
        for directory in [self.projects_dir, self.templates_dir, self.temp_dir]:
            os.makedirs(directory, exist_ok=True)

    def _load_recent_projects(self) -> List[str]:
        return self.config_manager.get('editor.recent_files', [])

    def _save_recent_projects(self) -> None:
        self.config_manager.set('editor.recent_files', self.recent_projects[:10])

    def _add_to_recent_projects(self, project_path: str) -> None:
        if project_path in self.recent_projects:
            self.recent_projects.remove(project_path)
        self.recent_projects.insert(0, project_path)
        self._save_recent_projects()

    # -- Lifecycle --

    def create_project(
        self,
        name: str,
        project_type: ProjectType = ProjectType.VIDEO_EDITING,
        description: str = "",
        template_id: Optional[str] = None,
    ) -> Optional[str]:
        project_id = str(uuid.uuid4())
        project_path = os.path.join(self.projects_dir, f"{name}_{project_id[:8]}")
        os.makedirs(project_path, exist_ok=True)
        for subdir in ['media', 'exports', 'backups', 'cache', 'assets']:
            os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

        metadata = ProjectMetadata(
            name=name,
            description=description,
            project_type=project_type,
            author=os.getlogin(),
        )
        project = Project(project_id, project_path, metadata)

        if template_id and template_id in self.templates:
            template = self.templates[template_id]
            project.settings = template.settings
            project.timeline = template.timeline

        if project.save():
            self.projects[project_id] = project
            self.current_project = project
            self._add_to_recent_projects(project_path)
            self.logger.info(f"Created project: {name} ({project_id})")
            return project_id

        shutil.rmtree(project_path)
        return None

    def open_project(self, project_path: str) -> Optional[str]:
        project_file = os.path.join(project_path, 'project.json')
        if not os.path.exists(project_file):
            self.logger.error(f"Project file not found: {project_path}")
            return None

        lock_file = os.path.join(project_path, '.lock')
        if os.path.exists(lock_file):
            try:
                with open(lock_file, 'r') as f:
                    pid = f.read().strip()
                if psutil.pid_exists(int(pid)):
                    self.logger.warning(f"Project locked by PID {pid}")
                    return None
            except ValueError:
                pass

        try:
            with open(project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            metadata = ProjectMetadata.from_dict(project_data['metadata'])
            project = Project(metadata.name, project_path, metadata)
            if project.load():
                self.projects[project.id] = project
                self.current_project = project
                self._add_to_recent_projects(project_path)
                with open(lock_file, 'w') as f:
                    f.write(str(os.getpid()))
                self.logger.info(f"Opened project: {metadata.name} ({project.id})")
                return project.id
        except Exception as e:
            self.logger.error(f"Failed to open project: {e}")

        return None

    def save_project(self, project_id: str, auto_save: bool = False) -> bool:
        if project_id not in self.projects:
            return False
        project = self.projects[project_id]

        if project.settings.backup_enabled and not auto_save:
            backup_path = project.create_backup()
            if backup_path:
                project.cleanup_old_backups(project.settings.backup_count)

        if project.save():
            if not auto_save:
                self.logger.info(f"Saved project: {project.metadata.name} ({project_id})")
            return True
        return False

    def close_project(self, project_id: str) -> bool:
        if project_id not in self.projects:
            return False
        project = self.projects[project_id]

        if project.is_modified:
            self.save_project(project_id)

        lock_file = os.path.join(project.path, '.lock')
        if os.path.exists(lock_file):
            os.remove(lock_file)

        if self.current_project and self.current_project.id == project_id:
            self.current_project = None

        self.logger.info(f"Closed project: {project.metadata.name} ({project_id})")
        return True

    def delete_project(self, project_id: str) -> bool:
        if project_id not in self.projects:
            return False
        project = self.projects[project_id]
        self.close_project(project_id)
        if os.path.exists(project.path):
            shutil.rmtree(project.path)
        del self.projects[project_id]
        if project.path in self.recent_projects:
            self.recent_projects.remove(project.path)
            self._save_recent_projects()
        self.logger.info(f"Deleted project: {project.metadata.name} ({project_id})")
        return True

    # -- Import / Export --

    def export_project(
        self,
        project_id: str,
        export_path: str,
        include_media: bool = True,
    ) -> bool:
        if project_id not in self.projects:
            return False
        project = self.projects[project_id]

        try:
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                project_file = os.path.join(project.path, 'project.json')
                if os.path.exists(project_file):
                    zipf.write(project_file, 'project.json')

                if include_media:
                    media_dir = os.path.join(project.path, 'media')
                    if os.path.exists(media_dir):
                        for root, _dirs, files in os.walk(media_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, project.path)
                                zipf.write(file_path, arcname)

                export_info = {
                    'exported_at': datetime.now().isoformat(),
                    'project_version': project.metadata.version,
                    'cineai_version': '2.0.0',
                    'include_media': include_media,
                }
                zipf.writestr('export_info.json', json.dumps(export_info, indent=2))

            self.logger.info(f"Exported project to: {export_path}")
            return True
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False

    def import_project(self, import_path: str) -> Optional[str]:
        if not os.path.exists(import_path):
            return None

        temp_extract_dir = os.path.join(self.temp_dir, f"import_{uuid.uuid4().hex[:8]}")
        try:
            with zipfile.ZipFile(import_path, 'r') as zipf:
                zipf.extractall(temp_extract_dir)

            project_file = os.path.join(temp_extract_dir, 'project.json')
            if not os.path.exists(project_file):
                self.logger.error("Invalid import: no project.json found")
                return None

            with open(project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            metadata = ProjectMetadata.from_dict(project_data['metadata'])

            new_project_id = str(uuid.uuid4())
            new_project_path = os.path.join(
                self.projects_dir, f"{metadata.name}_{new_project_id[:8]}"
            )
            os.makedirs(new_project_path, exist_ok=True)

            for item in os.listdir(temp_extract_dir):
                src = os.path.join(temp_extract_dir, item)
                dst = os.path.join(new_project_path, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)

            project = Project(metadata.name, new_project_path, metadata)
            if project.load():
                self.projects[project.id] = project
                self._add_to_recent_projects(new_project_path)
                self.logger.info(f"Imported project: {metadata.name}")
                return project.id

            return None
        except Exception as e:
            self.logger.error(f"Import failed: {e}")
            return None
        finally:
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)

    # -- Templates --

    def create_template(self, project_id: str, template_name: str) -> bool:
        if project_id not in self.projects:
            return False
        project = self.projects[project_id]

        template_id = str(uuid.uuid4())
        template_path = os.path.join(self.templates_dir, f"{template_name}_{template_id[:8]}")
        os.makedirs(template_path, exist_ok=True)

        try:
            shutil.copy2(
                os.path.join(project.path, 'project.json'),
                os.path.join(template_path, 'project.json'),
            )
            metadata = ProjectMetadata(
                name=template_name,
                description=f"Template from {project.metadata.name}",
                project_type=project.metadata.project_type,
                author=os.getlogin(),
            )
            template = Project(template_id, template_path, metadata)
            self.templates[template_id] = template
            self.logger.info(f"Created template: {template_name}")
            return True
        except Exception as e:
            self.logger.error(f"Template creation failed: {e}")
            if os.path.exists(template_path):
                shutil.rmtree(template_path)
            return False

    def _load_templates(self) -> None:
        if not os.path.exists(self.templates_dir):
            return
        try:
            for entry in os.listdir(self.templates_dir):
                entry_path = os.path.join(self.templates_dir, entry)
                if not os.path.isdir(entry_path):
                    continue
                project_file = os.path.join(entry_path, 'project.json')
                if not os.path.exists(project_file):
                    continue
                try:
                    with open(project_file, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                    metadata = ProjectMetadata.from_dict(project_data['metadata'])
                    template = Project(metadata.name, entry_path, metadata)
                    if template.load():
                        self.templates[template.id] = template
                except Exception:
                    logger.debug("Skip invalid template: %s", entry_path)
        except Exception as e:
            self.logger.warning(f"Template scan failed: {e}")

    # -- Queries --

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def get_current_project(self) -> Optional[Project]:
        return self.current_project

    def get_all_projects(self) -> List[Project]:
        return list(self.projects.values())

    def get_recent_projects(self) -> List[str]:
        return list(self.recent_projects)

    def get_templates(self) -> List[Project]:
        return list(self.templates.values())

    def cleanup(self) -> None:
        for project in list(self.projects.values()):
            if project.is_modified:
                project.save()
        self.projects.clear()
        self.current_project = None
