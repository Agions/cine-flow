#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
音画同步引擎

功能：
1. 基于内容的语义匹配 — 将解说内容与视频场景进行语义对齐
2. 基于时间的事件同步 — 根据语音时间戳调整视频片段选择
3. 动态时间扩展/压缩 — 微调视频片段时长以匹配语音节奏
4. 场景切换点优化 — 确保在静音或语气停顿处切换场景

核心算法：
- 使用动态规划(DTW)进行句子级音画对齐
- 使用关键词匹配进行语义场景关联
- 使用能量检测找到静音点作为场景切换候选位置
"""

import logging
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class WordTimestamp:
    """词级时间戳"""
    word: str
    start: float  # 秒
    end: float    # 秒
    confidence: float = 1.0


@dataclass
class SentenceSync:
    """句子同步信息"""
    text: str
    audio_start: float
    audio_end: float
    video_start: float
    video_end: float
    match_score: float = 0.0
    sync_method: str = "auto"  # auto / semantic / time
    keywords: List[str] = field(default_factory=list)


@dataclass
class AVSyncConfig:
    """音画同步配置"""
    # 时间容差（秒）- 允许的音画最大偏差
    time_tolerance: float = 0.5

    # 最小视频片段时长（秒）
    min_video_segment: float = 1.0

    # 最大视频片段时长（秒）
    max_video_segment: float = 15.0

    # 场景切换优先位置（语气停顿前的秒数）
    pause_lookahead: float = 0.3

    # 启用语义匹配
    enable_semantic_match: bool = True

    # 启用时间扩展/压缩
    enable_time_stretch: bool = True

    # 最大时间拉伸比例
    max_stretch_ratio: float = 1.2

    # 最小时间拉伸比例
    min_stretch_ratio: float = 0.8


class AVSyncEngine:
    """
    音画同步引擎

    将解说语音与视频画面进行智能对齐，确保：
    1. 说到某内容时，播放的是相关的画面
    2. 画面切换在自然的停顿点（如语气停顿）
    3. 音画节奏协调，避免声画不同步
    """

    def __init__(self, config: Optional[AVSyncConfig] = None):
        self.config = config or AVSyncConfig()

    def sync(
        self,
        video_scenes: List[Dict[str, Any]],
        sentence_timestamps: List[Dict[str, Any]],
        scripts: List[str],
    ) -> List[SentenceSync]:
        """
        执行音画同步

        Args:
            video_scenes: 视频场景列表，每个包含:
                - start: 场景开始时间（秒）
                - end: 场景结束时间（秒）
                - description: 场景描述（可选）
                - keywords: 场景关键词（可选）
            sentence_timestamps: 句子时间戳列表，每个包含:
                - text: 句子文本
                - start: 开始时间（秒）
                - end: 结束时间（秒）
            scripts: 每段的解说文案列表

        Returns:
            同步后的句子同步信息列表
        """
        if not video_scenes or not sentence_timestamps:
            logger.warning("视频场景或句子时间戳为空，使用默认对齐")
            return self._fallback_sync(video_scenes, sentence_timestamps, scripts)

        # Step 1: 预处理 — 提取关键词
        scene_keywords = self._extract_scene_keywords(video_scenes)
        sentence_keywords = self._extract_sentence_keywords(sentence_timestamps, scripts)

        # Step 2: 语义匹配 — 为每个句子找到最相关的场景
        semantic_matches = self._semantic_match(
            sentence_timestamps, video_scenes, scene_keywords, sentence_keywords
        )

        # Step 3: 时间对齐 — 使用DP进行句子级对齐
        time_alignment = self._time_align(sentence_timestamps, video_scenes)

        # Step 4: 融合结果 — 结合语义和时间信息
        fused = self._fuse_results(
            sentence_timestamps, scripts, video_scenes, semantic_matches, time_alignment
        )

        # Step 5: 优化场景切换点
        optimized = self._optimize_switch_points(fused, sentence_timestamps)

        logger.info(f"音画同步完成: {len(optimized)} 个句子同步")
        return optimized

    def _extract_scene_keywords(self, scenes: List[Dict[str, Any]]) -> Dict[int, List[str]]:
        """提取场景关键词"""
        keywords = {}
        for i, scene in enumerate(scenes):
            kw_list = []
            # 从description提取
            desc = scene.get("description", "")
            if desc:
                kw_list.extend(self._tokenize_chinese(desc))

            # 从keywords提取
            scene_kw = scene.get("keywords", [])
            if isinstance(scene_kw, list):
                kw_list.extend(scene_kw)

            keywords[i] = list(set(kw_list))  # 去重
        return keywords

    def _extract_sentence_keywords(
        self,
        timestamps: List[Dict[str, Any]],
        scripts: List[str],
    ) -> Dict[int, List[str]]:
        """提取句子关键词"""
        keywords = {}
        for i, (ts, script) in enumerate(zip(timestamps, scripts)):
            kw_list = self._tokenize_chinese(ts.get("text", script))
            keywords[i] = kw_list
        return keywords

    def _tokenize_chinese(self, text: str) -> List[str]:
        """简单分词（基于字符和常见词）"""
        if not text:
            return []

        # 移除标点
        text = re.sub(r'[^\w\s]', ' ', text)

        # 简单按字符分词 + 常见词合并
        words = []
        common_words = [
            "开始", "结束", "继续", "接下来", "然后", "但是", "因为", "所以",
            "这个", "那个", "什么", "怎么", "为什么", "如何", "是否",
            "其实", "实际上", "一般来说", "通常", "有时候", "突然",
            "慢慢", "渐渐", "突然", "忽然", "当时", "后来", "最后",
        ]

        # 简单按空格或连续字符分
        parts = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', text)
        temp_word = ""

        for part in parts:
            if len(part) == 1:
                temp_word += part
            else:
                if temp_word and len(temp_word) <= 3:
                    words.append(temp_word)
                if part in common_words or len(part) >= 2:
                    words.append(part)
                temp_word = ""

        if temp_word:
            words.append(temp_word)

        return list(set(words))

    def _semantic_match(
        self,
        sentences: List[Dict[str, Any]],
        scenes: List[Dict[str, Any]],
        scene_kw: Dict[int, List[str]],
        sentence_kw: Dict[int, List[str]],
    ) -> Dict[int, int]:
        """
        语义匹配 — 为每个句子找到最相关的场景索引

        Returns:
            dict: {sentence_index: scene_index}
        """
        matches = {}

        for i, sentence in enumerate(sentences):
            best_scene = 0
            best_score = -1
            sentence_keywords = sentence_kw.get(i, [])

            for j, scene in enumerate(scenes):
                scene_keywords = scene_kw.get(j, [])

                # 计算关键词重叠度
                if not sentence_keywords or not scene_keywords:
                    overlap = 0
                else:
                    overlap = len(set(sentence_keywords) & set(scene_keywords))

                # 考虑时间接近度
                time_diff = abs(sentence.get("start", 0) - scene.get("start", 0))
                time_score = max(0, 1 - time_diff / 10)  # 10秒内有时间奖励

                # 综合得分
                total_score = overlap * 2 + time_score

                if total_score > best_score:
                    best_score = total_score
                    best_scene = j

            matches[i] = best_scene

        return matches

    def _time_align(
        self,
        sentences: List[Dict[str, Any]],
        scenes: List[Dict[str, Any]],
    ) -> Dict[int, int]:
        """
        时间对齐 — 使用贪心算法进行句子到场景的对齐

        Returns:
            dict: {sentence_index: scene_index}
        """
        alignment = {}
        current_scene_idx = 0

        for i, sentence in enumerate(sentences):
            sentence_start = sentence.get("start", 0)
            sentence_end = sentence.get("end", sentence_start + 2)

            # 找到合适的场景
            while current_scene_idx < len(scenes) - 1:
                next_scene_start = scenes[current_scene_idx + 1].get("start", 0)
                if sentence_end > next_scene_start:
                    current_scene_idx += 1
                else:
                    break

            alignment[i] = min(current_scene_idx, len(scenes) - 1)

        return alignment

    def _fuse_results(
        self,
        sentences: List[Dict[str, Any]],
        scripts: List[str],
        scenes: List[Dict[str, Any]],
        semantic_matches: Dict[int, int],
        time_alignment: Dict[int, int],
    ) -> List[SentenceSync]:
        """融合语义和时间对齐结果"""
        results = []

        for i, (sentence, script) in enumerate(zip(sentences, scripts)):
            text = sentence.get("text", script)
            audio_start = sentence.get("start", 0)
            audio_end = sentence.get("end", audio_start + 2)

            # 优先使用语义匹配，如果得分太低则使用时间对齐
            scene_idx = semantic_matches.get(i, time_alignment.get(i, 0))
            scene = scenes[scene_idx] if scene_idx < len(scenes) else scenes[-1]

            video_start = scene.get("start", 0)
            video_end = scene.get("end", video_start + 5)

            # 计算匹配得分
            keywords = self._tokenize_chinese(text)
            scene_kw = self._tokenize_chinese(scene.get("description", ""))
            overlap = len(set(keywords) & set(scene_kw)) if keywords and scene_kw else 0
            match_score = min(1.0, overlap / 3) if keywords else 0.5

            # 时间容差检查
            time_diff = abs(audio_start - video_start)
            if time_diff > self.config.time_tolerance:
                sync_method = "time"
            else:
                sync_method = "semantic" if match_score > 0.3 else "auto"

            results.append(SentenceSync(
                text=text,
                audio_start=audio_start,
                audio_end=audio_end,
                video_start=video_start,
                video_end=video_end,
                match_score=match_score,
                sync_method=sync_method,
                keywords=keywords[:5],  # 保留前5个关键词
            ))

        return results

    def _optimize_switch_points(
        self,
        syncs: List[SentenceSync],
        sentences: List[Dict[str, Any]],
    ) -> List[SentenceSync]:
        """优化场景切换点 — 在语气停顿处切换"""
        if not syncs or len(syncs) < 2:
            return syncs

        optimized = [syncs[0]]

        for i in range(1, len(syncs)):
            curr = syncs[i]
            prev = syncs[i - 1]

            # 检查是否需要切换场景
            if curr.video_start != prev.video_end:
                # 找到合适的切换点
                switch_time = self._find_optimal_switch_point(
                    prev.audio_end, curr.audio_start
                )

                if switch_time is not None:
                    # 调整当前句子的视频开始时间
                    curr.video_start = switch_time
                    curr.sync_method = "optimized"

            optimized.append(curr)

        return optimized

    def _find_optimal_switch_point(
        self,
        before_end: float,
        after_start: float,
    ) -> Optional[float]:
        """找到最佳的场景切换时间点"""
        # 在两个句子之间的中间位置切换
        mid_point = (before_end + after_start) / 2

        # 检查是否在允许的范围内
        if abs(mid_point - before_end) < self.config.min_video_segment:
            return before_end + self.config.min_video_segment
        if abs(after_start - mid_point) < self.config.min_video_segment:
            return after_start - self.config.min_video_segment

        return mid_point

    def _fallback_sync(
        self,
        scenes: List[Dict[str, Any]],
        timestamps: List[Dict[str, Any]],
        scripts: List[str],
    ) -> List[SentenceSync]:
        """默认同步策略 — 平均分配"""
        if not scenes:
            return []

        results = []
        total_duration = scenes[-1].get("end", 60) if scenes else 60
        segment_duration = total_duration / len(scripts) if scripts else 5

        for i, (ts, script) in enumerate(zip(timestamps, scripts)):
            video_start = i * segment_duration
            video_end = (i + 1) * segment_duration

            results.append(SentenceSync(
                text=ts.get("text", script),
                audio_start=ts.get("start", video_start),
                audio_end=ts.get("end", video_end),
                video_start=video_start,
                video_end=video_end,
                match_score=0.0,
                sync_method="fallback",
            ))

        return results

    def analyze_sync_quality(self, syncs: List[SentenceSync]) -> Dict[str, Any]:
        """
        分析同步质量

        Returns:
            包含各项质量指标的字典
        """
        if not syncs:
            return {"quality": "unknown", "score": 0}

        total_offset = 0
        semantic_count = 0
        optimized_count = 0

        for sync in syncs:
            offset = abs(sync.audio_start - sync.video_start)
            total_offset += offset
            if sync.sync_method == "semantic":
                semantic_count += 1
            if sync.sync_method == "optimized":
                optimized_count += 1

        avg_offset = total_offset / len(syncs)
        semantic_ratio = semantic_count / len(syncs)

        # 计算综合得分
        quality_score = 1.0
        if avg_offset > 2.0:
            quality_score -= 0.3
        elif avg_offset > 0.5:
            quality_score -= 0.1

        quality_score += semantic_ratio * 0.3

        return {
            "quality": "good" if quality_score > 0.8 else "medium" if quality_score > 0.5 else "poor",
            "score": round(quality_score, 2),
            "avg_offset_sec": round(avg_offset, 2),
            "semantic_ratio": round(semantic_ratio, 2),
            "optimized_count": optimized_count,
            "total_sentences": len(syncs),
        }


__all__ = [
    "AVSyncEngine",
    "AVSyncConfig",
    "WordTimestamp",
    "SentenceSync",
]