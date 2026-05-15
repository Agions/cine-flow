# NarrateFlow

<p align="center">
  <img src="docs/public/favicon.svg" width="80" alt="NarrateFlow" />
</p>

<p align="center">

[![License: MIT](https://img.shields.io/github/license/Agions/NarrateFlow?style=flat-square&color=MIT-blue)
](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=FFD43B)
](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Qt-6.5%2B-41C845?style=flat-square&logo=qt&logoColor=41C845)
](https://qt.io/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-silver?style=flat-square&color=silver)
](https://github.com/Agions/NarrateFlow)
[![Release](https://img.shields.io/github/v/release/Agions/NarrateFlow?include_prereleases&style=flat-square&color=10B981)
](https://github.com/Agions/NarrateFlow/releases/latest)
[![Build](https://img.shields.io/github/actions/workflow/status/Agions/NarrateFlow/build.yml?style=flat-square&logo=github-actions)
](https://github.com/Agions/NarrateFlow/actions)

</p>

> **NarrateFlow** — 批量上传视频，AI 自动分组选段，一键生成电影感第一人称配音解说。
>
> 短剧 / 影视 / Vlog，一键变成"我在现场"的专业叙事视频。

**成本**：< ¥0.01 / 视频（DeepSeek-V4）
**隐私**：视频永不上传云端，全本地处理

---

## 定位

NarrateFlow 是一款专注于**第一人称视角视频解说**的 AI 工具。用户上传一段视频，AI 自动判断"我是谁"，从视频中提取该人物出现的片段，生成电影感配音解说。

适用于：短剧二次创作、影视解说、Vlog 故事化改造等场景。

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 🎬 **多视频智能合并** | 批量上传，AI 视觉+声纹混合分组，避免同一人重复解说 |
| 👤 **第一人称片段提取** | Qwen2.5-VL 逐帧分析，提取"我"的视角高光片段（9–60 秒） |
| 💡 **情感峰值驱动选段** | 叙事完整优先 + 情感峰值加权排序 |
| 🎙️ **7 种情感风格** | 治愈 / 悬疑 / 励志 / 怀旧 / 浪漫 / 幽默 / 纪录片 |
| ✍️ **精准字幕** | TTS word-level，音字同步 50ms 精度 |
| 📦 **模块化成品输出** | 合并版（完整叙事）+ 高光片段（单独分发） |
| 🖥️ **剪映草稿导出** | 原生 JSON，无缝导入剪映继续精剪 |
| 🌐 **全本地运行** | 视频永不上传云端 |

---

## 4 步创作流程

```
批量上传视频（文件夹 / Ctrl 多选）
    │
    ▼
┌────────────────────────────────────────────┐
│  Step 1 · 场景理解                           │
│  Qwen2.5-VL 逐帧分析，提取"我"的主体视角       │
└────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────┐
│  Step 2 · 智能分组                           │
│  视觉 embedding（0.7）+ 声纹（0.3）混合相似度  │
└────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────┐
│  Step 3 · 叙事选段                           │
│  叙事完整优先 + 情感峰值驱动                   │
│  悬疑铺垫 → 剧情高潮 → 情感共鸣               │
└────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────┐
│  Step 4 · 解说生成 + 导出                     │
│  DeepSeek-V4 + Edge-TTS / F5-TTS            │
│  MP4（H.264/H.265）/ 剪映草稿 JSON            │
└────────────────────────────────────────────┘
```

---

## 技术栈

| 模块 | 模型 / 技术 | 说明 |
|------|-----------|------|
| 智能分组 | **Qwen2.5-VL** + 声纹 | 视觉 0.7 + 音频 0.3 混合相似度 |
| 第一人称提取 | **Qwen2.5-VL** | 逐帧分析，主体视角判断 |
| 解说生成 | **DeepSeek-V4** | 第一人称视角，7 种预设风格 |
| 语音识别 | **SenseVoice** | 阿里 FunAudioLLM，本地 ASR |
| 配音合成 | **Edge-TTS** · **F5-TTS** | Edge 主流低延迟，F5 音色克隆 |
| 字幕 | TTS word-level timing | 50ms 以内精度 |
| UI 框架 | **PySide6** Qt 6.5+ | OKLCH Design System |

---

## 快速开始

### 下载安装包

访问 [Releases](https://github.com/Agions/NarrateFlow/releases/latest) 下载 Windows `.exe` / macOS `.dmg` / Linux `.AppImage`。

### 从源码运行

```bash
git clone https://github.com/Agions/NarrateFlow.git
cd NarrateFlow
pip install -r requirements.txt
python app/main.py
```

### 配置 AI（最低只需一个 Key）

```bash
# DeepSeek（解说生成主力，推荐）
export DEEPSEEK_API_KEY="sk-..."

# 阿里云百炼（视频理解，备选）
export DASHSCOPE_API_KEY="..."

# 不配置时：Edge-TTS 配音合成等基础功能仍可正常使用
```

---

## 文档

| 文档 | 说明 |
|------|------|
| [快速开始](docs/guide/quick-start.md) | 5 分钟上手 |
| [功能详解](docs/features.md) | 全部功能说明 |
| [AI 模型配置](docs/ai-models.md) | 各模型配置指南 |
| [配置参考](docs/config.md) | 环境变量与配置文件 |
| [常见问题](docs/faq.md) | FAQ 与疑难排查 |

---

## 许可证

[MIT License](LICENSE) · Copyright © 2025-2026 [Agions](https://github.com/Agions)
