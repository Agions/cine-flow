"""
AI 第一人称独白制作器 (Monologue Maker)

功能：原视频 + AI 独白配音 + 沉浸式字幕

工作流程:
    1. 分析原视频内容（SceneAnalyzer）
    2. 生成第一人称独白文案（ScriptGenerator + DeepSeek-V4）
    3. 生成情感化 AI 配音（VoiceGenerator + Edge-TTS）
    4. 生成电影级字幕（CaptionGenerator）
    5. 导出剪映草稿

使用示例:
    from app.services.video import MonologueMaker, MonologueProject

    maker = MonologueMaker()
    project = maker.create_project(
        source_video="input.mp4",
        context="深夜独自走在街头，回忆涌上心头",
        emotion="惆怅",
    )

    # 导出到剪映
    draft_path = maker.export_to_jianying(project, "/path/to/drafts")
"""

import re
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, List
from enum import Enum

from .base_maker import BaseVideoMaker
from .models.monologue import MonologueStyle, EmotionType, MonologueSegment
from .monologue_project import MonologueProject
from .emotion_engine import infer_emotion
from .av_sync_applier import AVSyncApplier
from ..ai.script_generator import ScriptGenerator, VoiceTone
from ..ai.voice_generator import VoiceGenerator, VoiceConfig
from ..ai.voice_models import VoiceStyle
from ..video_tools.caption_gen import CaptionGenerator
from ..video_tools.ffmpeg_tool import FFmpegTool
from ..export.jianying_models import JianyingDraft
from .track_builder import build_monologue_tracks, CAPTION_STYLES

logger = logging.getLogger(__name__)


__all__ = [
    "MonologueProject",
    "MonologueMaker",
    "create_monologue",
]

# MonologueProject 已迁移至 monologue_project.py


class MonologueMaker(BaseVideoMaker[MonologueProject]):
    """
    AI 第一人称独白制作器

    将原视频转换为带有沉浸式独白的视频

    使用示例:
        maker = MonologueMaker()

        # 创建项目
        project = maker.create_project(
            source_video="night_walk.mp4",
            context="深夜独自走在雨后的街道上",
            emotion="惆怅",
            style=MonologueStyle.MELANCHOLIC,
        )

        # 生成独白
        maker.generate_script(project)

        # 生成配音
        maker.generate_voice(project)

        # 生成字幕
        maker.generate_captions(project)

        # 导出到剪映
        draft_path = maker.export_to_jianying(project, "/path/to/drafts")
    """

    # 风格对应的配置
    STYLE_CONFIG = {
        MonologueStyle.MELANCHOLIC: {
            "tone": VoiceTone.CALM,
            "voice_style": VoiceStyle.NARRATION,
            "rate": 0.9,
            "prompt_hint": "忧郁、沉思、内心独白",
        },
        MonologueStyle.INSPIRATIONAL: {
            "tone": VoiceTone.EXCITED,
            "voice_style": VoiceStyle.NARRATION,
            "rate": 1.0,
            "prompt_hint": "励志、向上、充满力量",
        },
        MonologueStyle.ROMANTIC: {
            "tone": VoiceTone.EMOTIONAL,
            "voice_style": VoiceStyle.CONVERSATIONAL,
            "rate": 0.95,
            "prompt_hint": "温柔、浪漫、深情",
        },
        MonologueStyle.MYSTERIOUS: {
            "tone": VoiceTone.MYSTERIOUS,
            "voice_style": VoiceStyle.WHISPERING,
            "rate": 0.85,
            "prompt_hint": "神秘、悬疑、低沉",
        },
        MonologueStyle.NOSTALGIC: {
            "tone": VoiceTone.CALM,
            "voice_style": VoiceStyle.NARRATION,
            "rate": 0.9,
            "prompt_hint": "怀旧、追忆、温暖",
        },
        MonologueStyle.PHILOSOPHICAL: {
            "tone": VoiceTone.CALM,
            "voice_style": VoiceStyle.NARRATION,
            "rate": 0.88,
            "prompt_hint": "深邃、哲思、引人深思",
        },
        MonologueStyle.HEALING: {
            "tone": VoiceTone.CALM,
            "voice_style": VoiceStyle.CONVERSATIONAL,
            "rate": 0.92,
            "prompt_hint": "治愈、温暖、安慰",
        },
    }

    def __init__(
        self,
        voice_provider: str = "edge",
    ):
        super().__init__()
        self.voice_provider = voice_provider

        self.voice_generator = VoiceGenerator(provider=voice_provider)
        self.script_generator = ScriptGenerator(use_llm_manager=True)
        self.caption_generator = CaptionGenerator()
        self.av_sync_applier = AVSyncApplier()

    def create_project(
        self,
        source_video: str,
        context: str,
        emotion: str = "neutral",
        name: Optional[str] = None,
        style: MonologueStyle = MonologueStyle.MELANCHOLIC,
        output_dir: Optional[str] = None,
        **kwargs,
    ) -> MonologueProject:
        """创建独白项目"""
        project = MonologueProject(
            context=context,
            emotion=emotion,
            style=style,
        )

        self._report_progress("分析视频", 0.0)
        self._init_project(project, source_video, name, output_dir)

        # Fallback: 无场景时用 ffprobe 获取视频时长
        if project.video_duration <= 0:
            try:
                project.video_duration = FFmpegTool.get_duration(source_video) or 0.0
            except Exception as e:
                logger.warning(f"Failed to get video duration for {source_video}: {e}")
                project.video_duration = 0.0

        self._report_progress("分析视频", 1.0)

        return project

    def generate_script(
        self,
        project: MonologueProject,
        custom_script: Optional[str] = None,
    ) -> None:
        """
        生成独白文案

        Args:
            project: 项目对象
            custom_script: 自定义文案
        """
        self._report_progress("生成独白", 0.0)

        if custom_script:
            project.full_script = custom_script
        else:
            # 复用预建的 script_generator（避免每次重新加载配置）
            result = self.script_generator.generate_monologue(
                context=project.context,
                emotion=project.emotion,
                duration=project.video_duration,
            )
            project.full_script = result.content

        # 分段
        self._segment_script(project)

        # 音画同步 — 确保解说内容与画面匹配
        if project.scenes and project.segments:
            self.av_sync_applier.apply_sync(
                segments=project.segments,
                scenes=project.scenes,
                video_duration=project.video_duration,
            )

        self._report_progress("生成独白", 1.0)

    def _segment_script(self, project: MonologueProject) -> None:
        """将独白分段 — 支持空白行和中文句末标点双重拆分"""
        # 优先按空白行分段，否则按中文句末标点分
        paragraphs = [p.strip() for p in project.full_script.split('\n\n') if p.strip()]

        if len(paragraphs) <= 1:
            # 按句末标点拆分（保留标点）
            parts = re.split(r'([。！？\?!]+)', project.full_script)
            merged = []
            for i in range(0, len(parts) - 1, 2):
                text = parts[i] + (parts[i + 1] if i + 1 < len(parts) else '')
                if text.strip():
                    merged.append(text.strip())
            # 合并过短的碎片
            if merged and len(merged) > 3:
                paragraphs = []
                buf = ""
                for p in merged:
                    buf += p
                    if len(buf) >= 30:
                        paragraphs.append(buf)
                        buf = ""
                if buf:
                    paragraphs.append(buf)
            elif merged:
                paragraphs = merged

        if not paragraphs:
            paragraphs = [project.full_script]

        # 按时间顺序整理有效场景（跳过无效）
        valid_scenes = [s for s in project.scenes if s and s.end > s.start]
        n_scenes = len(valid_scenes)

        project.segments = []
        for i, para in enumerate(paragraphs):
            # 按时间比例分配段落到场景（避免取模循环导致长场景被跳过）
            if n_scenes > 0:
                # 计算段落在总字数中的比例位置
                para_ratio = (i + 0.5) / len(paragraphs)
                # 找到对应时间点的场景
                target_time = para_ratio * project.video_duration
                scene_idx = 0
                for j, scene in enumerate(valid_scenes):
                    if scene.start <= target_time < scene.end:
                        scene_idx = j
                        break
                    elif target_time >= scene.end:
                        scene_idx = j  # 落在当前场景之后
                scene = valid_scenes[min(scene_idx, n_scenes - 1)]
            else:
                scene = None

            # 根据内容推断情感
            emotion = infer_emotion(para, project.emotion)

            seg_duration = project.video_duration / len(paragraphs) if paragraphs else 10.0
            segment = MonologueSegment(
                script=para,
                emotion=emotion,
                video_start=scene.start if scene else i * seg_duration,
                video_end=scene.end if scene else (i + 1) * seg_duration,
            )
            project.segments.append(segment)

    def generate_voice(
        self,
        project: MonologueProject,
        voice_config: Optional[VoiceConfig] = None,
    ) -> None:
        """
        生成 AI 配音（并行多 segment，max_workers=4）

        Args:
            project: 项目对象
            voice_config: 配音配置
        """
        style_cfg = self.STYLE_CONFIG.get(
            project.style,
            self.STYLE_CONFIG[MonologueStyle.MELANCHOLIC]
        )

        if voice_config:
            project.voice_config = voice_config
        else:
            project.voice_config = VoiceConfig(
                style=style_cfg["voice_style"],
                rate=style_cfg["rate"],
            )

        output_dir = Path(project.output_dir) / "audio"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 准备任务列表
        tasks = [
            (i, seg, str(output_dir / f"monologue_{i:03d}.mp3"))
            for i, seg in enumerate(project.segments)
        ]

        results: dict[int, tuple[str, float, list]] = {}
        done_count = 0

        def _generate_one(i: int, segment: MonologueSegment, audio_path: str):
            config = VoiceConfig(
                voice_id=project.voice_config.voice_id,
                rate=project.voice_config.rate,
            )
            result = self.voice_generator.generate(
                text=segment.script,
                output_path=audio_path,
                config=config,
            )
            return i, result.audio_path, result.duration, result.sentence_timestamps or []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(_generate_one, i, seg, path): i
                for i, seg, path in tasks
            }
            for future in as_completed(futures):
                i, audio_path, duration = future.result()
                results[i] = (audio_path, duration)
                done_count += 1
                self._report_progress("生成配音", done_count / len(tasks))

        for i, segment in enumerate(project.segments):
            if i in results:
                segment.audio_path, segment.audio_duration, segment.sentence_timestamps = results[i]

        self._report_progress("生成配音", 1.0)

    def generate_captions(
        self,
        project: MonologueProject,
        style: str = "cinematic",
    ) -> None:
        """
        生成电影级字幕

        Args:
            project: 项目对象
            style: 字幕风格 (cinematic, minimal, expressive)
        """
        self._report_progress("生成字幕", 0.0)

        project.caption_style = style
        caption_cfg = CAPTION_STYLES.get(style, CAPTION_STYLES["cinematic"])

        current_time = 0.0

        for i, segment in enumerate(project.segments):
            segment.captions = []

            # 优先使用 EdgeTTS 真实句子时间戳
            if segment.sentence_timestamps:
                for ts in segment.sentence_timestamps:
                    segment.captions.append({
                        "text": ts["text"],
                        "start": current_time + ts["start"],
                        "duration": max(ts["end"] - ts["start"], 0.5),
                        "style": caption_cfg,
                        "emotion": segment.emotion.value,
                    })
            else:
                # 回退：按中文句末标点拆分并按字符数估算时长
                parts = re.split(r'([。！？\u3001])', segment.script)
                segment_words = max(len(segment.script.replace(' ', '')), 1)

                current_start = current_time
                current_text = ""

                for part in parts:
                    if not part:
                        continue
                    if part in ('，', '；'):
                        current_text += part
                        continue
                    if part in ('。', '！', '？'):
                        current_text += part
                        if len(current_text.strip()) >= 2:
                            word_count = len(current_text)
                            duration = (word_count / segment_words) * segment.audio_duration
                            segment.captions.append({
                                "text": current_text,
                                "start": current_start,
                                "duration": max(duration, 0.5),
                                "style": caption_cfg,
                                "emotion": segment.emotion.value,
                            })
                            current_start += duration
                            current_text = ""
                    else:
                        current_text += part

                if current_text.strip() and len(current_text.strip()) >= 2:
                    word_count = len(current_text)
                    duration = (word_count / segment_words) * segment.audio_duration
                    segment.captions.append({
                        "text": current_text,
                        "start": current_start,
                        "duration": max(duration, 0.5),
                        "style": caption_cfg,
                        "emotion": segment.emotion.value,
                    })

            current_time += segment.audio_duration
            self._report_progress("生成字幕", (i + 1) / len(project.segments))

        self._report_progress("生成字幕", 1.0)

    def _build_jianying_tracks(self, draft: JianyingDraft, project: MonologueProject) -> None:
        """构建独白视频的剪映轨道"""
        build_monologue_tracks(
            draft=draft,
            source_video=project.source_video,
            video_duration=project.video_duration,
            segments=project.segments,
            caption_style=project.caption_style,
        )

    # ------------------------------------------------------------------ #
    #  辅助方法                                                           #
    # ------------------------------------------------------------------ #

# =========== 便捷函数 ===========

def create_monologue(
    source_video: str,
    context: str,
    emotion: str,
    output_jianying_dir: str,
    style: MonologueStyle = MonologueStyle.MELANCHOLIC,
) -> str:
    """
    一键创建独白视频

    Args:
        source_video: 源视频
        context: 场景描述
        emotion: 情感
        output_jianying_dir: 剪映草稿目录
        style: 独白风格

    Returns:
        剪映草稿路径
    """
    maker = MonologueMaker()

    project = maker.create_project(
        source_video=source_video,
        context=context,
        emotion=emotion,
        style=style,
    )

    maker.generate_script(project)
    maker.generate_voice(project)
    maker.generate_captions(project)

    return maker.export_to_jianying(project, output_jianying_dir)
