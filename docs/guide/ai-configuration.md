---
title: AI 模型配置指南
description: Voxplore 支持的 AI 模型一览与配置方法。
---

# AI 模型配置指南

Voxplore 支持多种 AI 模型，可根据需求自由组合。

## 支持的模型

### 视频理解模型

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| **Qwen2.5-VL** | 阿里通义千问视觉大模型，支持视频帧级分析 | 推荐主力 |
| **Qwen-VL** | 通义千问视觉基础版 | 备选 / 低配 |

### 大语言模型

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| **DeepSeek-V4** | 高性价比，支持长上下文 | 推荐主力 |
| **DeepSeek-V3** | 稳定版 | 备选 |
| **GPT-4o** | OpenAI 最新多模态模型 | 高质量需求 |

### 语音识别（ASR）

| 模型 | 说明 | 部署方式 |
|------|------|----------|
| **SenseVoice** | 阿里 FunAudioLLM，本地运行 | 本地（推荐）|
| **Whisper** | OpenAI 开源 ASR | 本地 |

### 语音合成（TTS）

| 模型 | 说明 | 特点 |
|------|------|------|
| **Edge-TTS** | 微软 Edge 语音合成 | 低延迟、多音色 |
| **F5-TTS** | 零样本音色克隆 | 支持自定义音色 |

## 配置方式

### 环境变量

```bash
# DeepSeek（解说生成主力）
export DEEPSEEK_API_KEY="sk-..."

# 阿里云百炼（视频理解 + ASR）
export DASHSCOPE_API_KEY="..."
```

### 最低配置

只需配置 `DEEPSEEK_API_KEY`，即可使用：
- DeepSeek-V4 解说生成
- Edge-TTS 配音合成

其他模型为可选增强。

## 进阶配置

### SenseVoice 本地部署

```bash
pip install FunAudioLLM
```

### F5-TTS 音色克隆

配置自定义音色参考音频，获得更个性化的配音效果。
