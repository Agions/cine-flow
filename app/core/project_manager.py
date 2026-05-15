#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voxplore 项目管理器

提供完整的项目生命周期管理功能

架构：
- ProjectService : 纯业务逻辑层（无 Qt 依赖，可用于 headless/CI）
- ProjectManager  : QObject + ProjectService（带 Qt 信号）
"""

import functools
import os
import json
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from app.core._signals import QObject, Signal
from app.core.config_manager import ConfigManager
from app.core.secure_key_manager import get_secure_key_manager
from app.core.models.project_models import (
    ProjectType,
    ProjectMetadata, ProjectSettings,
    ProjectMedia, ProjectTimeline,
)
from app.core.project_helpers import ProjectService, AutoSaveHelper
from app.utils.time_utils import generate_timestamp_id


# ─── 错误处理装饰器 ────────────────────────────────────────────
def _handle_project_error(action_code: str, action_name: str):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except Exception as e:
                self.logger.error(f"Failed to {action_name}: {e}")
                self.error_occurred.emit(
                    f"{action_code}_ERROR", f"{action_name}失败: {str(e)}"
                )
                hints = {'bool': False, 'str': None}
                ret_type = method.__annotations__.get('return', '')
                return hints.get(
                    str(ret_type).split("'")[1] if "'" in str(ret_type) else '', False
                )
        return wrapper
    return decorator


# ─── Project (数据模型) ─────────────────────────────────────────

class Project:
    """项目数据模型"""

    def __init__(self, project_id: str, project_path: str, metadata: ProjectMetadata):
        self.id = project_id
        self.path = project_path
        self.metadata = metadata
        self.settings = ProjectSettings()
        self.media_files: Dict[str, ProjectMedia] = {}
        self.timeline = ProjectTimeline()
        self.is_modified = False
        self.is_loaded = False

    def add_media_file(self, media_file: ProjectMedia) -> None:
        self.media_files[media_file.id] = media_file
        self.is_modified = True
        self.metadata.modified_at = datetime.now()

    def remove_media_file(self, media_id: str) -> bool:
        if media_id in self.media_files:
            del self.media_files[media_id]
            self.is_modified = True
            self.metadata.modified_at = datetime.now()
            return True
        return False

    def get_media_file(self, media_id: str) -> Optional[ProjectMedia]:
        return self.media_files.get(media_id)

    def get_all_media_files(self) -> List[ProjectMedia]:
        return list(self.media_files.values())

    def update_settings(self, settings: Dict[str, Any]) -> None:
        for key, value in settings.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
            else:
                self.settings.custom_settings[key] = value
        self.is_modified = True
        self.metadata.modified_at = datetime.now()

    def save(self) -> bool:
        from dataclasses import asdict
        try:
            project_data = {
                'metadata': self.metadata.to_dict(),
                'settings': asdict(self.settings),
                'media_files': {k: v.to_dict() for k, v in self.media_files.items()},
                'timeline': self.timeline.to_dict(),
                'version': '2.0.0'
            }
            project_file = os.path.join(self.path, 'project.json')
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            lock_file = os.path.join(self.path, '.lock')
            with open(lock_file, 'w') as f:
                f.write(str(os.getpid()))
            self.is_modified = False
            return True
        except Exception as e:
            logging.error(f"Failed to save project {self.id}: {e}")
            return False

    def load(self) -> bool:
        try:
            project_file = os.path.join(self.path, 'project.json')
            if not os.path.exists(project_file):
                return False
            with open(project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            self.metadata = ProjectMetadata.from_dict(project_data['metadata'])
            self.settings = ProjectSettings(**project_data.get('settings', {}))
            self.media_files.clear()
            for media_id, media_data in project_data.get('media_files', {}).items():
                self.media_files[media_id] = ProjectMedia.from_dict(media_data)
            self.timeline = ProjectTimeline.from_dict(project_data.get('timeline', {}))
            self.is_loaded = True
            self.is_modified = False
            return True
        except Exception as e:
            logging.error(f"Failed to load project {self.id}: {e}")
            return False

    def create_backup(self) -> Optional[str]:
        try:
            timestamp = generate_timestamp_id()
            backup_name = f"backup_{timestamp}"
            backup_path = os.path.join(self.path, 'backups', backup_name)
            os.makedirs(backup_path, exist_ok=True)
            shutil.copy2(
                os.path.join(self.path, 'project.json'),
                os.path.join(backup_path, 'project.json')
            )
            backup_info = {
                'timestamp': timestamp,
                'created_at': datetime.now().isoformat(),
                'project_version': self.metadata.version,
                'description': f"自动备份 - {timestamp}"
            }
            with open(os.path.join(backup_path, 'backup_info.json'), 'w') as f:
                json.dump(backup_info, f, indent=2)
            return backup_path
        except Exception as e:
            logging.error(f"Failed to create backup for project {self.id}: {e}")
            return None

    def cleanup_old_backups(self, keep_count: int = 10) -> None:
        try:
            backup_dir = os.path.join(self.path, 'backups')
            if not os.path.exists(backup_dir):
                return
            backups = []
            for backup_name in os.listdir(backup_dir):
                backup_path = os.path.join(backup_dir, backup_name)
                if os.path.isdir(backup_path):
                    info_file = os.path.join(backup_path, 'backup_info.json')
                    if os.path.exists(info_file):
                        try:
                            with open(info_file, 'r') as f:
                                backup_info = json.load(f)
                            backups.append((backup_path, backup_info['timestamp']))
                        except Exception:
                            pass
            backups.sort(key=lambda x: x[1], reverse=True)
            for backup_path, _ in backups[keep_count:]:
                shutil.rmtree(backup_path)
        except Exception as e:
            logging.error(f"Failed to cleanup backups for project {self.id}: {e}")


# ─── ProjectManager: QObject 信号层 + ProjectService 业务逻辑 ─────

class ProjectManager(QObject, ProjectService):
    """
    项目管理器 - 组合 QObject 信号 + ProjectService 纯业务逻辑

    所有业务逻辑直接委托自 ProjectService，信号在调用点显式 emit。
    """

    # Qt signals (only on QObject side)
    project_created = Signal(str)
    project_opened = Signal(str)
    project_saved = Signal(str)
    project_closed = Signal(str)
    project_deleted = Signal(str)
    project_imported = Signal(str)
    project_exported = Signal(str)
    recent_projects_updated = Signal(list)
    error_occurred = Signal(str, str)

    def __init__(self, config_manager: ConfigManager):
        QObject.__init__(self)
        ProjectService.__init__(self, config_manager)
        self.logger = logging.getLogger(__name__)
        self.secure_key_manager = get_secure_key_manager()
        self._auto_save = AutoSaveHelper()
        self._auto_save.attach(self)

    # ── Signal-emitting wrappers ────────────────────────────────

    def create_project(
        self,
        name: str,
        project_type: ProjectType = ProjectType.VIDEO_EDITING,
        description: str = "",
        template_id: Optional[str] = None,
    ) -> Optional[str]:
        result = ProjectService.create_project(
            self, name, project_type, description, template_id
        )
        if result:
            self.project_created.emit(result)
        return result

    def open_project(self, project_path: str) -> Optional[str]:
        result = ProjectService.open_project(self, project_path)
        if result:
            self.project_opened.emit(result)
        return result

    def save_project(self, project_id: str, auto_save: bool = False) -> bool:
        result = ProjectService.save_project(self, project_id, auto_save)
        if result:
            self.project_saved.emit(project_id)
        return result

    def close_project(self, project_id: str) -> bool:
        result = ProjectService.close_project(self, project_id)
        if result:
            self.project_closed.emit(project_id)
        return result

    def delete_project(self, project_id: str) -> bool:
        result = ProjectService.delete_project(self, project_id)
        if result:
            self.project_deleted.emit(project_id)
        return result

    def export_project(
        self,
        project_id: str,
        export_path: str,
        include_media: bool = True,
    ) -> bool:
        result = ProjectService.export_project(self, project_id, export_path, include_media)
        if result:
            self.project_exported.emit(project_id)
        return result

    def import_project(self, import_path: str) -> Optional[str]:
        result = ProjectService.import_project(self, import_path)
        if result:
            self.project_imported.emit(result)
        return result

    # ── Recent projects (signals on write) ──────────────────────

    def _add_to_recent_projects(self, project_path: str) -> None:
        ProjectService._add_to_recent_projects(self, project_path)
        self.recent_projects_updated.emit(self.recent_projects[:10])

    # ── Delegate queries directly (no signals needed) ──────────

    def get_project(self, project_id: str) -> Optional[Project]:
        return ProjectService.get_project(self, project_id)

    def get_current_project(self) -> Optional[Project]:
        return ProjectService.get_current_project(self)

    def get_all_projects(self) -> List[Project]:
        return ProjectService.get_all_projects(self)

    def get_recent_projects(self) -> List[str]:
        return ProjectService.get_recent_projects(self)

    def get_templates(self) -> List[Project]:
        return ProjectService.get_templates(self)

    def cleanup(self) -> None:
        ProjectService.cleanup(self)
        self._auto_save.stop()
