"""
MonologueProject — 独白视频项目数据模型

从 monologue_maker.py 拆分出来，专注项目持久化和数据管理。
"""

import json
from enum import Enum
from pathlib import Path
from typing import Optional, List

from .base_maker import BaseProject
from .models.monologue import MonologueStyle, MonologueSegment


class MonologueProject(BaseProject):
    """独白视频项目"""

    # 独白内容
    context: str = ""
    emotion: str = ""
    full_script: str = ""
    segments: List[MonologueSegment] = []

    # 配置
    style: MonologueStyle = MonologueStyle.MELANCHOLIC
    voice_config = None
    caption_style: str = "cinematic"

    @property
    def total_duration(self) -> float:
        """总时长"""
        return sum(seg.audio_duration for seg in self.segments)

    def __init__(
        self,
        id: str = "",
        name: str = "新建项目",
        source_video: str = "",
        video_duration: float = 0.0,
        output_dir: str = "",
        scenes=None,
        context: str = "",
        emotion: str = "",
        full_script: str = "",
        segments=None,
        style=None,
        voice_config=None,
        caption_style: str = "cinematic",
    ):
        super().__init__(
            id=id,
            name=name,
            source_video=source_video,
            video_duration=video_duration,
            output_dir=output_dir,
            scenes=scenes or [],
        )
        self.context = context
        self.emotion = emotion
        self.full_script = full_script
        self.segments = segments or []
        self.style = style if style is not None else MonologueStyle.MELANCHOLIC
        self.voice_config = voice_config
        self.caption_style = caption_style

    # ------------------------------------------------------------------ #
    #  持久化 (.narrafiilm JSON)                                        #
    # ------------------------------------------------------------------ #

    def save(self, path: Optional[str] = None) -> str:
        """
        将项目保存为 .narrafiilm 文件（JSON）。

        Args:
            path: 保存路径，默认 <output_dir>/<name>.narrafiilm

        Returns:
            实际保存的文件路径
        """
        save_path = Path(path) if path else Path(self.output_dir) / f"{self.name}.narrafiilm"
        save_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": "1.0",
            "type": "monologue",
            "id": self.id,
            "name": self.name,
            "source_video": self.source_video,
            "video_duration": self.video_duration,
            "output_dir": self.output_dir,
            "context": self.context,
            "emotion": self.emotion,
            "full_script": self.full_script,
            "style": self.style.value if isinstance(self.style, Enum) else self.style,
            "caption_style": self.caption_style,
            "segments": [
                {
                    "script": seg.script,
                    "emotion": seg.emotion.value if isinstance(seg.emotion, Enum) else seg.emotion,
                    "video_start": seg.video_start,
                    "video_end": seg.video_end,
                    "audio_path": seg.audio_path,
                    "audio_duration": seg.audio_duration,
                    "captions": seg.captions,
                }
                for seg in self.segments
            ],
        }

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(save_path)

    @classmethod
    def load(cls, path: str) -> "MonologueProject":
        """
        从 .narrafiilm 文件加载项目。

        Args:
            path: .narrafiilm 文件路径

        Returns:
            MonologueProject 实例
        """
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        segments = [
            MonologueSegment(
                script=seg["script"],
                emotion=seg["emotion"],
                video_start=seg["video_start"],
                video_end=seg["video_end"],
                audio_path=seg.get("audio_path", ""),
                audio_duration=seg.get("audio_duration", 0.0),
                captions=seg.get("captions", []),
            )
            for seg in data.get("segments", [])
        ]

        style_val = data.get("style", "melancholic")
        if isinstance(style_val, str):
            try:
                style = MonologueStyle(style_val)
            except ValueError:
                style = MonologueStyle.MELANCHOLIC
        else:
            style = MonologueStyle.MELANCHOLIC

        return cls(
            id=data.get("id", ""),
            name=data.get("name", "新建项目"),
            source_video=data.get("source_video", ""),
            video_duration=data.get("video_duration", 0.0),
            output_dir=data.get("output_dir", ""),
            context=data.get("context", ""),
            emotion=data.get("emotion", ""),
            full_script=data.get("full_script", ""),
            style=style,
            caption_style=data.get("caption_style", "cinematic"),
            segments=segments,
        )


__all__ = ["MonologueProject"]
