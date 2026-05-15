#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
剪映草稿导出器 (Jianying Exporter)

将 Voxplore 项目导出为剪映草稿格式，实现与剪映的完美对接。

剪映草稿结构:
    drafts/
    └── {project_name}/
        ├── draft_content.json     # 主要内容
        ├── draft_meta_info.json   # 元信息
        └── 素材文件...

使用示例:
    from app.services.export import JianyingExporter

    exporter = JianyingExporter()
    draft_path = exporter.export(project, output_dir)
    logger.info(f"草稿已导出: {draft_path}")

数据模型已拆分到 jianying_models.py，导出器保持单一职责。
"""

import logging
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, Dict, Any

from .jianying_models import (
    TrackType,
    TimeRange,
    Track,
    Segment,
    VideoMaterial,
    AudioMaterial,
    TextMaterial,
    JianyingDraft,
    JianyingConfig,
    CanvasConfig,
    CANVAS_PRESETS,
)
from .export_utils import safe_filename, BaseExporter, get_video_duration, get_video_resolution


logger = logging.getLogger(__name__)


__all__ = [
    "JianyingExporter",
]


class JianyingExporter(BaseExporter[JianyingDraft, JianyingConfig]):
    """
    剪映草稿导出器

    将项目导出为剪映可识别的草稿格式

    使用示例:
        exporter = JianyingExporter()

        # 创建草稿
        draft = exporter.create_draft("我的视频")

        # 添加视频轨道
        video_track = Track(type=TrackType.VIDEO)
        video_material = VideoMaterial(path="/path/to/video.mp4", duration=5000000)
        draft.add_video(video_material)

        video_segment = Segment(
            material_id=video_material.id,
            target_timerange=TimeRange.from_seconds(0, 5),
            source_timerange=TimeRange.from_seconds(0, 5),
        )
        video_track.add_segment(video_segment)
        draft.add_track(video_track)

        # 导出
        draft_path = exporter.export(draft, "/path/to/output")
    """

    def __init__(self, config: Optional[JianyingConfig] = None):
        super().__init__(config or JianyingConfig())

    def create_project(self, name: str) -> JianyingDraft:
        """实现基类抽象方法（别名为 create_draft）"""
        return self.create_draft(name)

    def export_project(self, project: JianyingDraft, output_dir: str) -> str:
        """实现基类抽象方法（别名为 export）"""
        return self.export(project, output_dir)

    def create_draft(self, name: str) -> JianyingDraft:
        """创建新草稿"""
        canvas_config = self._get_canvas_config(self.config.canvas_ratio)

        return JianyingDraft(
            name=name,
            canvas_config=canvas_config,
            version=self.config.version,
        )

    def _get_canvas_config(self, ratio: str) -> CanvasConfig:
        """根据比例获取画布配置"""
        return CANVAS_PRESETS.get(ratio) or CANVAS_PRESETS["9:16"]

    def export(
        self,
        draft: JianyingDraft,
        output_dir: str,
        progress_callback=None,
    ) -> str:
        """
        导出草稿到指定目录

        Args:
            draft: 剪映草稿对象
            output_dir: 输出目录（剪映草稿目录）
            progress_callback: 进度回调 fn(phase: str, progress: float)

        Returns:
            草稿文件夹路径
        """
        def _report(phase: str, p: float):
            if progress_callback:
                progress_callback(phase, p)

        output_path = Path(output_dir)

        # 创建草稿文件夹（使用项目名称）
        safe_name = safe_filename(draft.name)
        draft_folder = output_path / safe_name
        draft_folder.mkdir(parents=True, exist_ok=True)

        # 复制素材（如果启用）
        if self.config.copy_materials:
            _report("复制素材", 0.0)
            self._copy_materials(draft, draft_folder)
            _report("复制素材", 1.0)

        # 生成 draft_content.json
        _report("生成草稿配置", 0.0)
        content = draft.to_draft_content()
        content_path = draft_folder / "draft_content.json"
        self._write_json(content_path, content)
        _report("生成草稿配置", 1.0)

        # 生成 draft_meta_info.json
        _report("写入元信息", 0.0)
        meta = draft.to_draft_meta_info()
        meta["draft_root_path"] = str(draft_folder)
        meta_path = draft_folder / "draft_meta_info.json"
        self._write_json(meta_path, meta)
        _report("写入元信息", 1.0)

        return str(draft_folder)

    def _get_or_create_track(
        self,
        draft: JianyingDraft,
        track_type: TrackType,
        attribute: int = 0,
    ) -> Track:
        """获取指定类型的已有轨道，或创建新轨道

        Args:
            draft: 草稿对象
            track_type: 轨道类型（VIDEO/AUDIO）
            attribute: 轨道属性（VIDEO 轨道默认为 1）

        Returns:
            轨道对象
        """
        track = next((t for t in draft.tracks if t.type == track_type), None)
        if track:
            return track
        new_track = Track(type=track_type, attribute=attribute)
        draft.add_track(new_track)
        return new_track

    def _compute_next_track_start(
        self,
        draft: JianyingDraft,
        track_type: TrackType,
    ) -> float:
        """计算自动 target_start：沿用指定轨道末尾时间

        Args:
            draft: 草稿对象
            track_type: 轨道类型

        Returns:
            目标时间轴开始位置（秒），默认 0
        """
        track = next((t for t in draft.tracks if t.type == track_type), None)
        if not track or not track.segments:
            return 0.0
        last_seg = track.segments[-1]
        return (last_seg.target_timerange.start + last_seg.target_timerange.duration) / 1_000_000

    def _add_segment(
        self,
        draft: JianyingDraft,
        track_type: TrackType,
        material: Any,
        source_timerange: TimeRange,
        target_timerange: TimeRange,
        volume: Optional[float] = None,
        caption_info: Optional[Dict] = None,
        attribute: int = 0,
    ) -> Segment:
        """统一的片段添加逻辑"""
        track = self._get_or_create_track(draft, track_type, attribute=attribute)
        segment = Segment(
            material_id=material.id,
            source_timerange=source_timerange,
            target_timerange=target_timerange,
        )
        if volume is not None:
            segment.volume = volume
        if caption_info is not None:
            segment.caption_info = caption_info
        track.add_segment(segment)
        return segment

    def _copy_materials(self, draft: JianyingDraft, draft_folder: Path) -> None:
        """复制素材到草稿目录（并行化以提升大文件性能）"""
        materials_folder = draft_folder / "materials"
        materials_folder.mkdir(exist_ok=True)

        def _copy_single(src_path: str, materials_folder: Path) -> Optional[str]:
            """复制单个素材，返回新路径"""
            src = Path(src_path)
            if not src.exists():
                return None
            dst = materials_folder / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
            return str(dst)

        # 收集所有待复制的素材
        tasks = [
            material.path
            for material in draft.materials.videos + draft.materials.audios
            if material.path
        ]

        # 并行复制所有素材
        if tasks:
            results: Dict[str, str] = {}
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    executor.submit(_copy_single, src, materials_folder): src
                    for src in tasks
                }
                for future in as_completed(futures):
                    src = futures[future]
                    try:
                        new_path = future.result()
                        if new_path:
                            results[src] = new_path
                    except Exception as e:
                        logger.warning(f"素材复制失败 {src}: {e}")

            # 更新路径为相对路径
            for material in draft.materials.videos + draft.materials.audios:
                if material.path and material.path in results:
                    material.path = results[material.path]

    def add_video_segment(
        self,
        draft: JianyingDraft,
        video_path: str,
        start: float,
        duration: float,
        target_start: float = None,
    ) -> Segment:
        """
        便捷方法：添加视频片段

        Args:
            draft: 草稿对象
            video_path: 视频文件路径
            start: 源视频开始时间（秒）
            duration: 持续时间（秒）
            target_start: 目标时间轴开始位置（秒），默认为自动计算

        Returns:
            创建的片段对象
        """
        # 获取视频信息
        video_info = self._get_video_info(video_path)

        # 创建素材
        material = VideoMaterial(
            path=video_path,
            duration=video_info.get('duration', TimeRange.from_seconds(0, duration).duration),
            width=video_info.get('width', 1920),
            height=video_info.get('height', 1080),
        )
        draft.add_video(material)

        # 计算目标开始时间（自动沿用轨道末尾，或创建新轨道）
        if target_start is None:
            target_start = self._compute_next_track_start(draft, TrackType.VIDEO)

        return self._add_segment(
            draft,
            TrackType.VIDEO,
            material,
            TimeRange.from_seconds(start, duration),
            TimeRange.from_seconds(target_start, duration),
            attribute=1,
        )

    def add_audio_segment(
        self,
        draft: JianyingDraft,
        audio_path: str,
        start: float,
        duration: float,
        target_start: float = 0,
        volume: float = 1.0,
    ) -> Segment:
        """
        便捷方法：添加音频片段

        Args:
            draft: 草稿对象
            audio_path: 音频文件路径
            start: 源音频开始时间（秒）
            duration: 持续时间（秒）
            target_start: 目标时间轴开始位置（秒）
            volume: 音量（0.0 - 1.0）

        Returns:
            创建的片段对象
        """
        material = AudioMaterial(
            path=audio_path,
            duration=TimeRange.from_seconds(0, duration).duration,
            name=Path(audio_path).stem,
        )
        draft.add_audio(material)

        return self._add_segment(
            draft,
            TrackType.AUDIO,
            material,
            TimeRange.from_seconds(start, duration),
            TimeRange.from_seconds(target_start, duration),
            volume=volume,
        )

    def add_caption(
        self,
        draft: JianyingDraft,
        text: str,
        start: float,
        duration: float,
        font_size: float = 8.0,
        font_color: str = "#FFFFFF",
    ) -> Segment:
        """
        便捷方法：添加字幕

        Args:
            draft: 草稿对象
            text: 字幕文本
            start: 开始时间（秒）
            duration: 持续时间（秒）
            font_size: 字体大小（剪映相对尺寸，默认8.0）
            font_color: 字体颜色（十六进制）

        Returns:
            创建的片段对象
        """
        material = TextMaterial(
            content=text,
            font_size=font_size,
            font_color=font_color,
        )
        draft.add_text(material)

        return self._add_segment(
            draft,
            TrackType.TEXT,
            material,
            TimeRange.from_seconds(0, duration),
            TimeRange.from_seconds(start, duration),
            caption_info={
                "content": text,
                "font_size": font_size,
                "font_color": font_color,
            },
        )

    def _get_video_info(self, video_path: str) -> dict:
        """获取视频基本信息（宽高、时长）"""
        try:
            width, height = get_video_resolution(video_path)
            duration = get_video_duration(video_path)
            return {
                'width': width,
                'height': height,
                'duration': TimeRange.from_seconds(0, duration).duration,
            }
        except Exception as e:
            logger.error(f"获取视频信息失败: {e}")
            return {'width': 1920, 'height': 1080, 'duration': 0}
