# 更新日志

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2026-05-09

### 🐛 Bug Fixes

- 修复 CI/CD workflow 配置问题
- 移除代码中的未使用变量和无效 f-string 前缀
- 修正 README.md 中的 logo 图片路径

### 📝 Documentation

- 更新 badges 使用标准 flat-square 样式
- 修正 logo 图片路径

---

## [1.0.0] - 2026-05-09

> 此版本汇总了 NarrateFlow 从初始化到 v4.x 的所有历史变更，作为 1.0.0 基线版本归档。

### 🚀 核心功能

- **AI 视频解说生成** (Monologue Maker)：Qwen2.5-VL 视频理解 + DeepSeek-V4 解说生成 + SenseVoice ASR + Edge-TTS/F5-TTS 配音
- **AI 视频混剪** (Mashup Maker)：智能分组 + 情绪峰值检测 + 视角映射
- **导出支持**：DirectVideoExporter (MP4/MOV/GIF) + JianyingExporter (剪映草稿)
- **导出预设**：B站 (1080P 60fps)、YouTube (4K 60fps)、Twitter、TikTok、微信

### 🎨 UI/UX

- **OKLCH 色彩系统**：感知均匀色彩空间，亮度和色度解耦
- **OutCubic 动效**：页面切换滑入动画 (220-280ms)
- **脉冲指示器**：活动步骤动画
- **专业布局 v4**：200px 玻璃态侧边栏 + 48px 顶部工具栏 + 56px 页面标题栏
- **设置页面组件化**：CF* 组件体系替代硬编码样式
- **Toast 通知系统**：info/success/warning/error 四种类型，自动消失

### ⚡ 性能优化

- **Whisper 本地模式**：faster-whisper medium 模型，GPU batch_size=8，CPU INT8 量化
- **LLM 磁盘缓存**：SQLite 持久化，TTL=24h，最大 500MB，LRU 淘汰
- **请求去重**：相同 prompt+model+temperature 只调用一次 API
- **场景检测**：scenedetect 优化

### 🔒 安全

- **SecureExecutor**：所有 subprocess 调用统一经安全策略校验
- **PBKDF2**：HMAC 迭代次数 480,000 (OWASP 标准)
- **SecurityError 统一**：所有 ffmpeg/系统调用异常类型统一

### 📦 架构

- **Provider 插件化**：VisionProvider / LLMProvider / TTSProvider 协议 + ProviderRegistry 单例 + YAML 热加载
- **模块化拆分**：video services 分为 extraction/selection/grouping/tools/analyzers/loaders/cutters 7 个子目录
- **TDD 驱动**：39 tests 覆盖核心服务 (SmartGrouper, FirstPersonExtractor, EmotionPeakDetector, SegmentSelector)
- **PySide6 迁移**：从 PyQt6 迁移至 PySide6 (LGPL)

### 📊 质量指标

- Tests：**389 passed, 20 skipped, 2 warnings, 0 failed**
- Ruff Lint：All checks passed
- 死代码清理：删除 820+ 行冗余代码

### 🐛 Bug Fixes (历史累积)

- LLMManager 同步调用返回 None 问题修复
- Provider 健康检查超时 (5s) 修复
- FFmpegTool/SecureExecutor 异常类型错误 (CalledProcessError → SecurityError) 修复
- SecurityError 被静默吞噬问题修复
- Whisper 批处理 GPU 加速修复
- 无头环境 (offscreen) 兼容修复
- 缩略图缓存 LRU 逻辑修复
- 版本号显示错误修复 (3.2.0 → 3.9.0)
- 裸 `except:pass` 问题全面清理

---

## 历史版本 (归档)

以下为历史发布版本的原始条目，详情见 GitHub Releases。

| 版本 | 日期 | 说明 |
|------|------|------|
| v4.0.1 | 2026-05-08 | SecurityError 修复 + 死代码清理 |
| v4.0.0 | 2026-04-21 | Phase 1-4 全面重构 (TDD + Provider 插件化) |
| v3.10.0 | 2026-04-19 | UI 统一与组件化 |
| v3.9.0 | 2026-04-19 | LLM 磁盘缓存 + 性能优化 |
| v3.8.0 | 2026-04-14 | Whisper 本地化 + GPU 加速 |
| v3.7.0 | 2026-04-13 | UI 无障碍 + 减少动画偏好支持 |
| v3.6.0 | 2026-04-11 | 类型安全强化 + Pydantic v2 |
| v3.5.0 | 2026-04-10 | 创作向导重构 Phase 1 |
| v3.4.1 | 2026-04-09 | UI 重构 Bug 修复 |
| v3.4.0 | 2026-04-09 | OKLCH + OutCubic 专业设计规范 |
| v3.3.0 | 2026-04-08 | 场景检测性能改进 |
| v3.2.0 | 2026-04-05 | 品牌重命名 + 产品定位重构 |
| v3.1.1 | 2026-04-03 | FFmpeg 工具统一 + 缓存修复 |
| v3.1.0 | 2026-03-23 | PyQt6 → PySide6 迁移 |
| v3.0.0 | 2026-03-08 | AI 创作模式 (解说/混剪/独白) |
| v2.0.0 | 2025-XX-XX | 基础 AI 功能 + 视频导出 |
| v1.0.0 | 2024-XX-XX | 项目初始化 + 基础 UI 框架 |
