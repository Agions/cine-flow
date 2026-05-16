"""
AVSyncApplier — 音画同步应用器

从 monologue_maker.py 拆分出来，专注将 AVSyncEngine 的同步结果
应用到 MonologueProject 的各个 Segment 上。
"""

import logging
from typing import List

from .av_sync_engine import AVSyncEngine
from .models.monologue import MonologueSegment

logger = logging.getLogger(__name__)


class AVSyncApplier:
    """
    音画同步应用器

    负责:
    - 准备场景数据和句子时间戳
    - 调用 AVSyncEngine 执行同步
    - 将同步结果写回 project.segments
    """

    def __init__(self):
        self.av_sync_engine = AVSyncEngine()

    def apply_sync(
        self,
        segments: List[MonologueSegment],
        scenes: list,
        video_duration: float,
    ) -> None:
        """
        对项目 segments 应用音画同步。

        Args:
            segments: 独白片段列表（会被直接修改）
            scenes: 视频场景列表（每个场景有 start/end/description/keywords）
            video_duration: 视频总时长（秒）
        """
        # 准备场景数据
        video_scenes = []
        for scene in scenes:
            if hasattr(scene, 'start') and hasattr(scene, 'end'):
                video_scenes.append({
                    "start": scene.start,
                    "end": scene.end,
                    "description": getattr(scene, 'description', ''),
                    "keywords": getattr(scene, 'keywords', []) or [],
                })

        if not video_scenes:
            return

        # 准备句子时间戳
        sentence_timestamps = []
        scripts = []
        for seg in segments:
            scripts.append(seg.script)
            if seg.sentence_timestamps:
                for ts in seg.sentence_timestamps:
                    sentence_timestamps.append({
                        "text": ts.get("text", ""),
                        "start": ts.get("start", 0) + seg.audio_start if hasattr(seg, 'audio_start') else ts.get("start", 0),
                        "end": ts.get("end", 0) + seg.audio_start if hasattr(seg, 'audio_start') else ts.get("end", 0),
                    })
            else:
                sentence_timestamps.append({
                    "text": seg.script,
                    "start": 0,
                    "end": seg.audio_duration or 3.0,
                })

        # 执行同步
        syncs = self.av_sync_engine.sync(
            video_scenes=video_scenes,
            sentence_timestamps=sentence_timestamps,
            scripts=scripts,
        )

        # 更新片段的视频时间范围
        for i, sync in enumerate(syncs):
            if i < len(segments):
                seg = segments[i]
                seg.video_start = sync.video_start
                seg.video_end = sync.video_end
                # 记录同步质量
                if hasattr(seg, 'sync_info'):
                    seg.sync_info = {
                        "match_score": sync.match_score,
                        "sync_method": sync.sync_method,
                        "keywords": sync.keywords,
                    }

        logger.info(f"音画同步完成: {len(syncs)} 个片段已对齐")


__all__ = ["AVSyncApplier"]
