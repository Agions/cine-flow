#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Template categorization - extracted from project_template_manager.py"""

import logging
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.template_models import TemplateCategory, TemplateInfo

logger = logging.getLogger(__name__)


class TemplateCategorizer:
    """Handles template category management and filtering."""

    def __init__(self, categories: Dict[str, "TemplateCategory"]):
        self._categories = categories
        self.logger = logger

    def init_categories(self) -> None:
        """Populate the categories dict with defaults."""
        from app.core.template_models import TemplateCategory

        defaults = [
            TemplateCategory("video_editing", "视频编辑", "video", "#4CAF50"),
            TemplateCategory("ai_enhancement", "AI增强", "auto_awesome", "#9C27B0"),
            TemplateCategory("compilation", "视频集锦", "movie", "#FF5722"),
            TemplateCategory("commentary", "视频解说", "record_voice_over", "#2196F3"),
            TemplateCategory("social_media", "社交媒体", "share", "#00BCD4"),
            TemplateCategory("education", "教育培训", "school", "#FF9800"),
            TemplateCategory("business", "商务展示", "business", "#607D8B"),
            TemplateCategory("personal", "个人创作", "person", "#E91E63"),
        ]
        for cat in defaults:
            self._categories[cat.name] = cat

    def get_categories(self) -> List["TemplateCategory"]:
        """Return all categories."""
        return list(self._categories.values())

    def filter_by_category(
        self,
        templates: Dict[str, "TemplateInfo"],
        category: str,
    ) -> List["TemplateInfo"]:
        """Return templates belonging to a given category name."""
        return [t for t in templates.values() if t.category == category]

    def filter_by_type(
        self,
        templates: Dict[str, "TemplateInfo"],
        project_type: str,
    ) -> List["TemplateInfo"]:
        """Return templates matching a project type."""
        return [t for t in templates.values() if t.project_type == project_type]

    def search(
        self,
        templates: Dict[str, "TemplateInfo"],
        query: str,
        category: str = None,
    ) -> List["TemplateInfo"]:
        """Full-text search across template names/descriptions/tags."""
        q = query.lower()
        results = [
            t for t in templates.values()
            if q in t.name.lower() or q in t.description.lower()
            or any(q in tag.lower() for tag in t.tags)
        ]
        if category:
            results = [t for t in results if t.category == category]
        return results
