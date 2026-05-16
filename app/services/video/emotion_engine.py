"""
EmotionEngine — 情感推断引擎

从 monologue_maker.py 拆分出来，专注文本情感分析和情感类型映射。
"""

import re
from typing import Dict

from .models.monologue import EmotionType


# 情感关键词库
_EMOTION_KEYWORDS: Dict[EmotionType, list] = {
    EmotionType.SAD: [
        "悲", "泪", "哭", "失去", "离别", "孤独", "寂寞",
        "难过", "伤心", "痛苦", "无奈", "遗憾", "惋惜", "怀念",
    ],
    EmotionType.HAPPY: [
        "开心", "快乐", "笑", "幸福", "美好", "温暖",
        "高兴", "喜悦", "兴奋", "期待", "惊喜", "满足", "感动",
    ],
    EmotionType.CALM: [
        "平静", "安宁", "静", "默", "沉思", "思考",
        "宁静", "淡然", "从容", "释然", "放下", "接受",
    ],
    EmotionType.TENDER: [
        "温柔", "爱", "思念", "想", "心", "情",
        "珍惜", "呵护", "陪伴", "守候", "牵挂", "眷恋",
    ],
    EmotionType.EXCITED: [
        "激动", "兴奋", "期待", "梦想", "未来",
        "挑战", "突破", "奋斗", "拼搏", "热血", "激情",
    ],
}

# 强度词
_INTENSITY_WORDS = {
    "very": ["非常", "特别", "极其", "十分", "格外", "异常"],
    "slightly": ["有点", "稍微", "略微", "一点", "些许"],
}

# 否定词
_NEGATION_PATTERNS = ["不", "没", "无", "非", "别", "休", "勿"]

# 基础情感映射
_EMOTION_MAP: Dict[str, EmotionType] = {
    "惆怅": EmotionType.SAD,
    "忧郁": EmotionType.SAD,
    "开心": EmotionType.HAPPY,
    "快乐": EmotionType.HAPPY,
    "平静": EmotionType.CALM,
    "温柔": EmotionType.TENDER,
    "excited": EmotionType.EXCITED,
    "激动": EmotionType.EXCITED,
    "思念": EmotionType.TENDER,
    "怀念": EmotionType.SAD,
    "感动": EmotionType.TENDER,
    "温暖": EmotionType.TENDER,
}


def infer_emotion(text: str, base_emotion: str) -> EmotionType:
    """
    根据文本内容推断情感类型。

    增强版 - 更智能的情感识别，支持否定词检测和强度修饰。

    Args:
        text: 待分析文本
        base_emotion: 基础情感（fallback 用）

    Returns:
        EmotionType: 推断出的情感类型
    """
    emotion_scores: Dict[EmotionType, float] = {}

    for emotion, keywords in _EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                # 检查否定词修饰
                negated = _is_negated(text, keyword)
                if negated:
                    score -= 0.5
                else:
                    score += 1
                    # 检查强度词
                    if any(very in text for very in _INTENSITY_WORDS["very"]):
                        score += 2

        if score != 0:
            emotion_scores[emotion] = score

    if emotion_scores:
        return max(emotion_scores.items(), key=lambda x: x[1])[0]

    return _EMOTION_MAP.get(base_emotion, EmotionType.NEUTRAL)


def _is_negated(text: str, keyword: str) -> bool:
    """检测关键词是否被否定词修饰"""
    for neg in _NEGATION_PATTERNS:
        negated_phrase = f"{neg}{keyword}"
        if negated_phrase in text:
            return True
        # 否定词在关键词前 2 字内
        neg_pos = text.find(neg)
        kw_pos = text.find(keyword)
        if neg_pos != -1 and kw_pos != -1 and 0 < kw_pos - neg_pos <= 2:
            return True
    return False


__all__ = ["infer_emotion", "EmotionType"]
