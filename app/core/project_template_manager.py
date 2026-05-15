#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
项目模板管理器
提供项目模板的创建、管理和应用功能
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

from app.core._signals import QObject, Signal

from .project_manager import Project, ProjectType
from .config_manager import ConfigManager
from .template_models import TemplateInfo, TemplateCategory, TemplateMetadata
from .template_helpers import TemplateStorageIO, TemplateFileOps, TemplateCategorizer
from app.utils.time_utils import generate_timestamp_id


class ProjectTemplateManager(QObject):
    """项目模板管理器"""

    # 信号定义
    template_created = Signal(str)      # 模板创建信号
    template_updated = Signal(str)      # 模板更新信号
    template_deleted = Signal(str)      # 模板删除信号
    template_imported = Signal(str)     # 模板导入信号
    template_exported = Signal(str)     # 模板导出信号
    categories_updated = Signal()       # 类别更新信号
    error_occurred = Signal(str, str)   # 错误发生信号

    def __init__(self, config_manager: ConfigManager):
        super().__init__()

        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)

        # 目录设置
        self.templates_dir = Path.home() / "Voxplore" / "Templates"
        self.builtin_templates_dir = Path(__file__).parent / "templates"
        self.temp_dir = Path.home() / "Voxplore" / "Temp"

        # 模板存储
        self.templates: Dict[str, TemplateInfo] = {}
        self.categories: Dict[str, TemplateCategory] = {}

        # Helpers
        self._storage = TemplateStorageIO(self.templates_dir, self.builtin_templates_dir)
        self._file_ops = TemplateFileOps()
        self._categorizer = TemplateCategorizer(self.categories)

        # 初始化
        self._storage.ensure_directories(self.templates_dir, self.temp_dir)
        self._categorizer.init_categories()
        self._storage.load_templates(self.templates)
        self._storage.load_builtin_templates(self.templates, self.builtin_templates_dir)

    def _ensure_directories(self) -> None:
        """确保所需目录存在"""
        self._storage.ensure_directories(self.templates_dir, self.temp_dir)

    def _init_categories(self) -> None:
        """初始化模板类别"""
        self._categorizer.init_categories()

    def _load_templates(self) -> None:
        """加载用户模板"""
        self._storage.load_templates(self.templates)

    def _load_builtin_templates(self) -> None:
        """加载内置模板"""
        self._storage.load_builtin_templates(self.templates, self.builtin_templates_dir)

    def _save_templates(self) -> None:
        """保存模板信息"""
        self._storage.save_templates(self.templates)

    def _calculate_directory_size(self, directory: Path) -> int:
        """计算目录大小"""
        return self._storage.calculate_directory_size(directory)

    def create_template(self, project: Project, template_name: str, category: str,
                      description: str = "", tags: List[str] = None) -> Optional[str]:
        """从项目创建模板"""
        try:
            # 生成模板ID
            template_id = f"template_{generate_timestamp_id()}"

            # 创建模板目录
            template_dir = self.templates_dir / template_id
            template_dir.mkdir(parents=True, exist_ok=True)

            # 复制项目文件到模板目录
            self._copy_project_to_template(project.path, template_dir)

            # 创建模板元数据
            template_metadata = TemplateMetadata(
                name=template_name,
                description=description,
                author=project.metadata.author,
                version="1.0.1",
                category=category,
                tags=tags or []
            )

            # 保存模板元数据
            metadata_file = template_dir / "template_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(template_metadata.__dict__, f, indent=2, ensure_ascii=False)

            # 创建模板信息
            template_info = TemplateInfo(
                id=template_id,
                name=template_name,
                description=description,
                category=category,
                author=project.metadata.author,
                version="1.0.1",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                file_size=self._calculate_directory_size(template_dir),
                tags=tags or [],
                project_type=project.metadata.project_type
            )

            # 复制预览图（如果存在）
            if project.metadata.thumbnail_path and os.path.exists(project.metadata.thumbnail_path):
                preview_dest = template_dir / "preview.png"
                shutil.copy2(project.metadata.thumbnail_path, preview_dest)
                template_info.preview_image = str(preview_dest)

            # 保存模板信息
            self.templates[template_id] = template_info
            self._save_templates()

            self.template_created.emit(template_id)
            self.logger.info(f"Created template: {template_name} ({template_id})")
            return template_id

        except Exception as e:
            self.logger.error(f"Failed to create template from project {project.id}: {e}")
            self.error_occurred.emit("TEMPLATE_ERROR", f"创建模板失败: {str(e)}")
            return None

    def _copy_project_to_template(self, project_path: str, template_dir: Path) -> None:
        """复制项目文件到模板目录"""
        self._file_ops.copy_project_to_template(project_path, template_dir)

    def apply_template(self, template_id: str, project_name: str,
                      project_path: str, variables: Dict[str, Any] = None) -> bool:
        """应用模板创建项目"""
        try:
            if template_id not in self.templates:
                self.error_occurred.emit("TEMPLATE_ERROR", f"模板不存在: {template_id}")
                return False

            template_info = self.templates[template_id]

            # 确定模板路径
            if template_info.is_builtin:
                template_path = self.builtin_templates_dir / template_id
            else:
                template_path = self.templates_dir / template_id

            if not template_path.exists():
                self.error_occurred.emit("TEMPLATE_ERROR", f"模板文件不存在: {template_id}")
                return False

            # 创建项目目录
            project_dir = Path(project_path)
            project_dir.mkdir(parents=True, exist_ok=True)

            # 创建子目录
            subdirs = ['media', 'exports', 'backups', 'cache', 'assets']
            for subdir in subdirs:
                (project_dir / subdir).mkdir(exist_ok=True)

            # 复制模板文件
            self._copy_template_to_project(template_path, project_dir, variables or {})

            # 更新模板下载统计
            if not template_info.is_builtin:
                template_info.download_count += 1
                self._save_templates()

            self.logger.info(f"Applied template {template_id} to project {project_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to apply template {template_id}: {e}")
            self.error_occurred.emit("TEMPLATE_ERROR", f"应用模板失败: {str(e)}")
            return False

    def _copy_template_to_project(self, template_path: Path, project_dir: Path,
                                 variables: Dict[str, Any]) -> None:
        """复制模板文件到项目目录"""
        self._file_ops.copy_template_to_project(template_path, project_dir, variables)

    def _apply_variables_to_project(self, project_data: Dict[str, Any], variables: Dict[str, Any]) -> None:
        """应用变量到项目数据"""
        self._file_ops._apply_variables(project_data, variables)

    def update_template(self, template_id: str, updates: Dict[str, Any]) -> bool:
        """更新模板信息"""
        try:
            if template_id not in self.templates:
                return False

            template_info = self.templates[template_id]

            # 更新信息
            for key, value in updates.items():
                if hasattr(template_info, key):
                    setattr(template_info, key, value)

            template_info.updated_at = datetime.now()

            # 更新模板文件
            if not template_info.is_builtin:
                template_dir = self.templates_dir / template_id
                if template_dir.exists():
                    metadata_file = template_dir / "template_info.json"
                    with open(metadata_file, 'w') as f:
                        json.dump(template_info.to_dict(), f, indent=2)

            self._save_templates()
            self.template_updated.emit(template_id)
            self.logger.info(f"Updated template: {template_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update template {template_id}: {e}")
            return False

    def delete_template(self, template_id: str) -> bool:
        """删除模板"""
        try:
            if template_id not in self.templates:
                return False

            template_info = self.templates[template_id]

            # 不能删除内置模板
            if template_info.is_builtin:
                self.error_occurred.emit("TEMPLATE_ERROR", "不能删除内置模板")
                return False

            # 删除模板目录
            template_dir = self.templates_dir / template_id
            if template_dir.exists():
                shutil.rmtree(template_dir)

            # 从模板列表中移除
            del self.templates[template_id]
            self._save_templates()

            self.template_deleted.emit(template_id)
            self.logger.info(f"Deleted template: {template_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete template {template_id}: {e}")
            return False

    def get_template(self, template_id: str) -> Optional[TemplateInfo]:
        """获取模板信息"""
        return self.templates.get(template_id)

    def get_all_templates(self) -> List[TemplateInfo]:
        """获取所有模板"""
        return list(self.templates.values())

    def get_templates_by_category(self, category: str) -> List[TemplateInfo]:
        """按类别获取模板"""
        return [t for t in self.templates.values() if t.category == category]

    def get_templates_by_type(self, project_type: ProjectType) -> List[TemplateInfo]:
        """按类型获取模板"""
        return [t for t in self.templates.values() if t.project_type == project_type]

    def get_categories(self) -> List[TemplateCategory]:
        """获取所有类别"""
        return list(self.categories.values())

    def search_templates(self, query: str, category: str = None,
                        project_type: ProjectType = None) -> List[TemplateInfo]:
        """搜索模板"""
        results = []

        for template in self.templates.values():
            # 检查类别过滤
            if category and template.category != category:
                continue

            # 检查类型过滤
            if project_type and template.project_type != project_type:
                continue

            # 检查搜索条件
            query_lower = query.lower()
            if (query_lower in template.name.lower() or
                query_lower in template.description.lower() or
                any(query_lower in tag.lower() for tag in template.tags)):
                results.append(template)

        return results

    def export_template(self, template_id: str, export_path: str) -> bool:
        """导出模板"""
        try:
            if template_id not in self.templates:
                return False

            template_info = self.templates[template_id]

            # 确定模板路径
            if template_info.is_builtin:
                template_path = self.builtin_templates_dir / template_id
            else:
                template_path = self.templates_dir / template_id

            if not template_path.exists():
                return False

            # 创建ZIP文件
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 添加模板文件
                for file_path in template_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(template_path)
                        zipf.write(file_path, arcname)

                # 添加导出信息
                export_info = {
                    'template_info': template_info.to_dict(),
                    'exported_at': datetime.now().isoformat(),
                    'cineai_version': '2.0.0'
                }

                zipf.writestr('export_info.json', json.dumps(export_info, indent=2))

            self.template_exported.emit(template_id)
            self.logger.info(f"Exported template: {template_id} to {export_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to export template {template_id}: {e}")
            return False

    def import_template(self, import_path: str) -> Optional[str]:
        """导入模板"""
        try:
            # 创建临时目录
            temp_dir = self.temp_dir / f"template_import_{generate_timestamp_id()}"
            temp_dir.mkdir(parents=True, exist_ok=True)

            # 解压ZIP文件
            with zipfile.ZipFile(import_path, 'r') as zipf:
                zipf.extractall(temp_dir)

            # 检查导出信息
            export_info_file = temp_dir / 'export_info.json'
            if not export_info_file.exists():
                self.error_occurred.emit("TEMPLATE_ERROR", "无效的模板文件")
                return None

            with open(export_info_file, 'r') as f:
                export_info = json.load(f)

            template_data = export_info['template_info']
            template_info = TemplateInfo.from_dict(template_data)

            # 生成新模板ID
            template_id = f"imported_{generate_timestamp_id()}"
            template_info.id = template_id
            template_info.is_builtin = False
            template_info.updated_at = datetime.now()

            # 创建模板目录
            template_dir = self.templates_dir / template_id
            shutil.copytree(temp_dir, template_dir)

            # 更新模板信息文件
            info_file = template_dir / 'template_info.json'
            with open(info_file, 'w') as f:
                json.dump(template_info.to_dict(), f, indent=2)

            # 添加到模板列表
            self.templates[template_id] = template_info
            self._save_templates()

            # 清理临时目录
            shutil.rmtree(temp_dir)

            self.template_imported.emit(template_id)
            self.logger.info(f"Imported template: {template_id}")
            return template_id

        except Exception as e:
            self.logger.error(f"Failed to import template from {import_path}: {e}")
            self.error_occurred.emit("TEMPLATE_ERROR", f"导入模板失败: {str(e)}")
            return None

    def rate_template(self, template_id: str, rating: float) -> bool:
        """评分模板"""
        try:
            if template_id not in self.templates:
                return False

            template_info = self.templates[template_id]
            template_info.rating = max(0.0, min(5.0, rating))
            template_info.updated_at = datetime.now()

            self._save_templates()
            self.logger.info(f"Rated template {template_id}: {rating}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to rate template {template_id}: {e}")
            return False

    def get_template_statistics(self) -> Dict[str, Any]:
        """获取模板统计信息"""
        try:
            total_templates = len(self.templates)
            builtin_templates = len([t for t in self.templates.values() if t.is_builtin])
            user_templates = total_templates - builtin_templates

            # 按类别统计
            category_stats = {}
            for category in self.categories.values():
                count = len([t for t in self.templates.values() if t.category == category.name])
                category_stats[category.name] = count

            # 按类型统计
            type_stats = {}
            for project_type in ProjectType:
                count = len([t for t in self.templates.values() if t.project_type == project_type])
                type_stats[project_type.value] = count

            # 下载统计
            total_downloads = sum(t.download_count for t in self.templates.values())

            # 评分统计
            rated_templates = [t for t in self.templates.values() if t.rating > 0]
            avg_rating = sum(t.rating for t in rated_templates) / len(rated_templates) if rated_templates else 0.0

            return {
                'total_templates': total_templates,
                'builtin_templates': builtin_templates,
                'user_templates': user_templates,
                'category_stats': category_stats,
                'type_stats': type_stats,
                'total_downloads': total_downloads,
                'average_rating': avg_rating,
                'rated_templates_count': len(rated_templates)
            }

        except Exception as e:
            self.logger.error(f"Failed to get template statistics: {e}")
            return {}

    def validate_template(self, template_id: str) -> Dict[str, Any]:
        """验证模板完整性"""
        try:
            if template_id not in self.templates:
                return {'valid': False, 'errors': ['模板不存在']}

            template_info = self.templates[template_id]

            # 确定模板路径
            if template_info.is_builtin:
                template_path = self.builtin_templates_dir / template_id
            else:
                template_path = self.templates_dir / template_id

            if not template_path.exists():
                return {'valid': False, 'errors': ['模板目录不存在']}

            errors = []
            warnings = []

            # 检查必需文件
            required_files = ['project_template.json']
            for file_name in required_files:
                file_path = template_path / file_name
                if not file_path.exists():
                    errors.append(f"缺少必需文件: {file_name}")

            # 检查模板信息
            info_file = template_path / 'template_info.json'
            if not info_file.exists():
                warnings.append("缺少模板信息文件")

            # 检查文件大小
            actual_size = self._calculate_directory_size(template_path)
            if actual_size != template_info.file_size:
                warnings.append(f"文件大小不匹配: 预期 {template_info.file_size}, 实际 {actual_size}")

            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'actual_size': actual_size
            }

        except Exception as e:
            self.logger.error(f"Failed to validate template {template_id}: {e}")
            return {'valid': False, 'errors': [f"验证失败: {str(e)}"]}