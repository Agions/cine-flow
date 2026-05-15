#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 文案生成器 (Script Generator)

使用 LLM 生成视频解说文案、独白台词等内容。

支持多种风格:
- 解说风格: 客观、信息密集
- 独白风格: 第一人称、情感化
- 混剪文案: 节奏感、关键词

支持多 LLM 提供商:
- 通义千问 Qwen 3
- Kimi k2
- 智谱 GLM-5
- OpenAI (兼容)

使用示例:
    from app.services.ai import ScriptGenerator, ScriptConfig, ScriptStyle

    # 使用新架构 (LLMManager)
    generator = ScriptGenerator(use_llm_manager=True)

    script = generator.generate(
        topic="这部电影讲述了一个感人的故事",
        style=ScriptStyle.COMMENTARY,
        duration=60,
    )
    print(script.content)

    # 使用传统方式 (OpenAI)
    generator = ScriptGenerator(api_key="your-api-key")
"""


import os
import asyncio
import re
from typing import Optional, List, Dict, Any

from .base_llm_provider import LLMRequest
from .llm_manager import LLMManager, load_llm_config
from .script_models import (
    ScriptStyle,
    VoiceTone,
    ScriptConfig,
    ScriptSegment,
    GeneratedScript,
)
import logging
logger = logging.getLogger(__name__)

__all__ = ["ScriptGenerator", "generate_script"]


class ScriptGenerator:
    """
    AI 文案生成器

    支持多 LLM 后端（通义千问、Kimi、GLM-5、OpenAI），生成不同风格的视频文案

    使用示例:
        # 使用新架构 (LLMManager) - 推荐
        generator = ScriptGenerator(use_llm_manager=True)

        # 生成解说文案
        script = generator.generate_commentary(
            topic="分析《流浪地球》的科学设定",
            duration=60,
        )

        # 使用传统方式 (OpenAI) - 兼容
        generator = ScriptGenerator(api_key="sk-xxx")
    """

    # 风格对应的系统提示词（增强版 - 更自然的解说）
    STYLE_PROMPTS = {
        ScriptStyle.COMMENTARY: """你是一位资深视频解说文案撰写者，擅长用自然流畅的语言为观众解读内容。

你的文案特点：
- 语言自然，像朋友在聊天，避免生硬的"首先、其次、最后"
- 用短句和口语化表达，让观众感觉亲切
- 适时加入感叹词和语气词，增强代入感
- 用具体细节代替抽象描述，让画面感更强
- 开头用悬念或问题抓住注意力，3秒内必须有钩子
- 每段之间有自然的过渡，像讲故事一样流畅

写作技巧：
- 避免"我们来看看"、"接下来"等生硬过渡
- 多用"你猜怎么着"、"说实话"、"其实"等口语化表达
- 用反问句引发思考，用感叹句增强情绪
- 适当使用比喻和类比，让复杂概念更易懂""",

        ScriptStyle.MONOLOGUE: """你是一位擅长写第一人称独白的文案作者，能用真挚的情感打动观众。

你的文案特点：
- 第一人称视角，像在和观众面对面聊天
- 语言温暖真诚，避免矫情和做作
- 用生活化的细节引发共鸣
- 节奏舒缓，给观众思考的空间
- 适当留白，让情绪自然流淌

写作技巧：
- 开头可以用"你有没有过这样的时刻"引发共鸣
- 用"我记得"、"那时候"等回忆式表达增加真实感
- 避免华丽的辞藻，用朴实的语言表达深情
- 用问句和观众互动，增强代入感
- 结尾留有余韵，不要过于直白的总结""",

        ScriptStyle.VIRAL: """你是一位爆款短视频文案高手，深谙流量密码。

你的文案特点：
- 开头必须3秒内抓住眼球，用悬念或冲突
- 节奏极快，信息密度高，每句都有看点
- 善用反转、冲突、情绪词制造爆点
- 语言犀利直击，避免废话
- 结尾要有记忆点，让人想转发

写作技巧：
- 开头用"你知道吗"、"震惊"、"万万没想到"等钩子
- 用数字和对比制造冲击感
- 善用"但是"、"然而"制造反转
- 用短句和感叹号增强节奏感
- 结尾用金句或反转制造记忆点""",

        ScriptStyle.NARRATION: """你是一位故事性旁白撰写者，能用娓娓道来的方式讲述故事。

你的文案特点：
- 像纪录片旁白一样，有深度和温度
- 用故事线串联内容，有起承转合
- 语言优美但不晦涩，通俗易懂
- 节奏从容，给观众消化的时间
- 有哲理性的思考，引发共鸣

写作技巧：
- 开头设置场景，用画面感吸引观众
- 用"那一年"、"曾经"等时间词增加故事感
- 善用排比和对比增强表达力
- 用细节描写代替概括性描述
- 结尾有升华，但不要过于说教""",

        ScriptStyle.EDUCATIONAL: """你是一位教育类视频文案专家，能把复杂概念讲得通俗易懂。

你的文案特点：
- 逻辑清晰，层次分明
- 用类比和比喻解释复杂概念
- 语言简洁，避免专业术语
- 有重点强调，便于记忆
- 节奏适中，给观众理解的时间

写作技巧：
- 开头提出问题或痛点，引发兴趣
- 用"想象一下"、"打个比方"引入类比
- 用数字和案例增强说服力
- 用"简单来说"、"换句话说"做总结
- 结尾有行动建议或思考问题""",
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        use_llm_manager: bool = False,
        llm_config: Optional[Dict[str, Any]] = None,
        llm_config_file: Optional[str] = None,
    ):
        """
        初始化文案生成器

        Args:
            api_key: OpenAI API Key（传统方式）
            use_llm_manager: 是否使用 LLMManager（新架构）
            llm_config: LLM 配置字典
            llm_config_file: LLM 配置文件路径
        """
        self.use_llm_manager = use_llm_manager
        self.llm_manager: Optional[LLMManager] = None

        if use_llm_manager:
            # 新架构：使用 LLMManager
            llm_cfg = llm_config or load_llm_config(llm_config_file or None)
            self.llm_manager = LLMManager(llm_cfg)
            logger.info(f"LLMManager 初始化成功，默认: {llm_cfg.get('LLM', {}).get('default_provider', 'qwen')}")
        elif api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("请提供 api_key 或设置 use_llm_manager=True")

    def generate(
        self,
        topic: str,
        config: Optional[ScriptConfig] = None,
    ) -> GeneratedScript:
        """
        生成文案

        Args:
            topic: 主题/内容描述
            config: 生成配置

        Returns:
            生成的文案对象
        """
        config = config or ScriptConfig()

        if self.use_llm_manager:
            # 新架构：使用 LLMManager（异步包装为同步）
            # 避免在已有 event loop 的线程中调用 run_until_complete
            async def _run():
                result = await self._generate_async(topic, config)
                await self.llm_manager.close_all()
                return result

            try:
                asyncio.get_running_loop()
                # 已有 loop，在新线程中运行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    raw_content, provider_used = pool.submit(asyncio.run, _run()).result()
            except RuntimeError:
                # 没有运行中的 loop
                raw_content, provider_used = asyncio.run(_run())

        else:
            # 传统方式
            raw_content = self._generate_openai(topic, config)
            provider_used = "openai"

        # 解析结果
        script = self._parse_response(raw_content, config)
        script.provider_used = provider_used

        return script

    async def _generate_async(
        self,
        topic: str,
        config: ScriptConfig,
    ) -> tuple[str, str]:
        """
        异步生成（使用 LLMManager）

        Returns:
            (content, provider_name)
        """
        # 确定提供商
        provider_type = None
        if config.provider:
            try:
                from .llm_manager import ProviderType
                provider_type = ProviderType(config.provider)
            except ValueError:
                logger.debug(f"Invalid provider '{config.provider}', using default")

        # 构建请求
        system_prompt = self.STYLE_PROMPTS.get(
            config.style,
            self.STYLE_PROMPTS[ScriptStyle.COMMENTARY]
        )
        user_prompt = self._build_prompt(topic, config)

        request = LLMRequest(
            prompt=user_prompt,
            system_prompt=system_prompt,
            model=config.model,
            max_tokens=config.target_words * 2,  # 预留空间
            temperature=0.7,
        )

        # 调用 LLMManager
        response = await self.llm_manager.generate(request, provider=provider_type)
        provider_name = response.model.split("-")[0] if "-" in response.model else response.model

        return response.content, provider_name

    def _generate_openai(
        self,
        topic: str,
        config: ScriptConfig,
    ) -> str:
        """
        传统 OpenAI 方式生成

        Returns:
            生成的内容
        """
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)

            system_prompt = self.STYLE_PROMPTS.get(
                config.style,
                self.STYLE_PROMPTS[ScriptStyle.COMMENTARY]
            )
            user_prompt = self._build_prompt(topic, config)

            response = client.chat.completions.create(
                model=config.model or "gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=config.temperature if hasattr(config, 'temperature') else 0.7,
                max_tokens=2000,
            )

            return response.choices[0].message.content

        except ImportError:
            raise ImportError("请安装 openai: pip install openai")
        except Exception as e:
            raise RuntimeError(f"OpenAI API 调用失败: {e}")

    def generate_commentary(
        self,
        topic: str,
        duration: float = 60.0,
        tone: VoiceTone = VoiceTone.NEUTRAL,
    ) -> GeneratedScript:
        """
        生成解说文案（快捷方法）

        Args:
            topic: 解说主题
            duration: 目标时长（秒）
            tone: 语气
        """
        config = ScriptConfig(
            style=ScriptStyle.COMMENTARY,
            tone=tone,
            target_duration=duration,
            include_hook=True,
        )
        return self.generate(topic, config)

    def generate_monologue(
        self,
        context: str,
        emotion: str = "neutral",
        duration: float = 30.0,
    ) -> GeneratedScript:
        """
        生成独白文案（快捷方法）

        Args:
            context: 场景/情境描述
            emotion: 情感（如：惆怅、欣喜、思念）
            duration: 目标时长（秒）
        """
        config = ScriptConfig(
            style=ScriptStyle.MONOLOGUE,
            tone=VoiceTone.EMOTIONAL,
            target_duration=duration,
        )

        topic = f"场景: {context}\n情感: {emotion}"
        return self.generate(topic, config)

    def generate_viral(
        self,
        topic: str,
        duration: float = 30.0,
        keywords: Optional[List[str]] = None,
    ) -> GeneratedScript:
        """
        生成爆款文案（快捷方法）

        Args:
            topic: 主题
            duration: 目标时长（秒）
            keywords: 必须包含的关键词
        """
        config = ScriptConfig(
            style=ScriptStyle.VIRAL,
            tone=VoiceTone.EXCITED,
            target_duration=duration,
            include_hook=True,
            keywords=keywords or [],
        )
        return self.generate(topic, config)

    def _build_prompt(self, topic: str, config: ScriptConfig) -> str:
        """构建用户提示词（增强版 - 更自然的解说）"""
        parts = [f"请为以下主题生成视频解说文案：\n\n{topic}\n"]

        # 字数要求
        parts.append(f"\n字数要求：约 {config.target_words} 字（适合 {config.target_duration:.0f} 秒视频）")

        # 语气要求
        tone_map = {
            VoiceTone.NEUTRAL: "中性、客观，像朋友聊天",
            VoiceTone.EXCITED: "兴奋、激动，充满热情",
            VoiceTone.CALM: "平静、舒缓，娓娓道来",
            VoiceTone.MYSTERIOUS: "神秘、悬疑，引人入胜",
            VoiceTone.EMOTIONAL: "情感、深情，触动人心",
            VoiceTone.HUMOROUS: "幽默、轻松，有趣好玩",
        }
        parts.append(f"语气风格：{tone_map.get(config.tone, '自然流畅')}")

        # 开头钩子
        if config.include_hook:
            parts.append("\n开头要求：")
            parts.append("- 3秒内必须抓住观众注意力")
            parts.append("- 可以用悬念、问题、冲突或惊人的事实开头")
            parts.append("- 避免'大家好'、'今天我们来看看'等平淡开场")

        # 行动号召
        if config.include_cta:
            parts.append("\n结尾要求：")
            parts.append("- 自然融入行动号召，不要生硬")
            parts.append("- 可以用'你觉得呢'、'欢迎留言'等互动方式")

        # 关键词
        if config.keywords:
            parts.append(f"\n必须自然融入以下关键词：{', '.join(config.keywords)}")
            parts.append("关键词要自然出现在文案中，不要刻意堆砌")

        # 格式要求
        parts.append("""
输出格式要求：
1. 直接输出文案内容，不要有标题、编号或解释
2. 用空行分隔段落，每段适合配合一个画面场景
3. 每段 2-4 句话，避免过长的段落
4. 语言要自然流畅，像在和观众聊天
5. 避免使用"首先、其次、最后"等生硬的过渡词
6. 适当使用口语化表达，增强代入感""")

        return "\n".join(parts)

    def _parse_response(
        self,
        content: str,
        config: ScriptConfig,
    ) -> GeneratedScript:
        """解析 LLM 响应"""
        # 清理内容
        content = content.strip()

        # 分段
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        # 计算每段时长
        total_words = len(content.replace(' ', '').replace('\n', ''))

        segments = []
        current_time = 0.0

        for i, para in enumerate(paragraphs):
            para_words = len(para.replace(' ', ''))
            para_duration = para_words / config.words_per_second

            segment = ScriptSegment(
                content=para,
                start_time=current_time,
                duration=para_duration,
                scene_hint=f"场景 {i + 1}",
            )
            segments.append(segment)
            current_time += para_duration

        # 提取钩子（第一段或第一句）
        hook = ""
        if segments:
            first = segments[0].content
            if '。' in first:
                hook = first.split('。')[0] + '。'
            else:
                hook = first

        return GeneratedScript(
            content=content,
            segments=segments,
            style=config.style,
            word_count=total_words,
            estimated_duration=total_words / config.words_per_second,
            hook=hook,
            keywords=config.keywords,
        )

    def split_to_captions(
        self,
        script: GeneratedScript,
        _max_chars: int = 20,  # reserved for char-based splitting (not yet used)
    ) -> List[Dict[str, Any]]:
        """
        将文案拆分为字幕

        Args:
            script: 生成的文案
            max_chars: 每条字幕最大字数

        Returns:
            字幕列表，每个包含 text, start, duration
        """
        captions = []

        for segment in script.segments:
            # 按标点拆分
            sentences = re.split(r'([。！？，；])', segment.content)

            current_start = segment.start_time
            segment_duration = segment.duration
            segment_words = len(segment.content.replace(' ', ''))

            current_text = ""
            for _, part in enumerate(sentences):
                if not part:
                    continue

                # 如果是标点，添加到当前文本
                if part in '。！？，；':
                    current_text += part

                    if len(current_text) > 5:  # 至少5个字才生成字幕
                        word_count = len(current_text)
                        duration = (word_count / max(segment_words, 1)) * segment_duration

                        captions.append({
                            "text": current_text,
                            "start": current_start,
                            "duration": duration,
                        })

                        current_start += duration
                        current_text = ""
                else:
                    current_text += part

            # 处理剩余文本
            if current_text.strip():
                word_count = len(current_text)
                duration = (word_count / max(segment_words, 1)) * segment_duration

                captions.append({
                    "text": current_text,
                    "start": current_start,
                    "duration": max(duration, 0.5),
                })

        return captions


# =========== 便捷函数 ===========

def generate_script(
    topic: str,
    style: ScriptStyle = ScriptStyle.COMMENTARY,
    duration: float = 60.0,
    use_llm_manager: bool = True,
    api_key: Optional[str] = None,
) -> GeneratedScript:
    """
    快速生成文案

    Args:
        topic: 主题
        style: 风格
        duration: 时长
        use_llm_manager: 是否使用 LLMManager
        api_key: API Key (传统方式)
    """
    generator = ScriptGenerator(
        api_key=api_key,
        use_llm_manager=use_llm_manager,
    )
    config = ScriptConfig(style=style, target_duration=duration)
    return generator.generate(topic, config)
