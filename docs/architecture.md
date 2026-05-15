---
title: 架构概览
description: NarrateFlow 技术架构与模块设计。
---

# 架构概览

## 技术栈

| 层级 | 技术 |
|------|------|
| UI 框架 | PySide6（Qt 6.5+）|
| AI 模型 | Qwen2.5-VL / DeepSeek-V4 / SenseVoice |
| 语音合成 | Edge-TTS / F5-TTS |
| 视频处理 | FFmpeg |
| 编程语言 | Python 3.10+ |

## 模块架构

```
NarrateFlow/
├── app/
│   ├── core/           # 核心应用：Application、配置、缓存、异常
│   ├── services/
│   │   ├── ai/         # AI 服务：LLM 管理、场景分析、语音合成
│   │   ├── video/      # 视频服务：提取、分组、合成
│   │   ├── export/     # 导出服务：MP4、剪映草稿
│   │   └── orchestration/  # 流程编排
│   ├── plugins/        # 插件系统
│   ├── api/            # REST API（可选）
│   └── ui/             # PySide6 界面
│       ├── windows/    # 独立窗口
│       ├── pages/      # 分页视图
│       └── components/ # 可复用组件
├── docs/               # VitePress 文档站
└── tests/              # 测试套件
```

## 核心流程

1. **视频上传** → FFmpeg 解析元数据
2. **场景理解** → Qwen2.5-VL 逐帧分析
3. **智能分组** → 视觉 + 声纹混合相似度
4. **情感选段** → 叙事完整 + 情感峰值
5. **解说生成** → DeepSeek-V4 生成文案
6. **配音合成** → Edge-TTS / F5-TTS
7. **视频导出** → FFmpeg 合并 + 字幕烧录
