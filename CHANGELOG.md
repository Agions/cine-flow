## [4.0.1] - 2026-05-08

### 🐛 Bug Fixes

- **SecurityError 被静默吞噬**：`highlight_detector.py` 的 `_run_ffmpeg` 用 `except Exception` 吞掉了命令注入攻击被拦截的 `SecurityError` → 改为显式 catch 并 log WARNING
- **FFmpegTool 异常类型错误**：`ffmpeg_tool.py` 14处 catch `subprocess.CalledProcessError`，但实际抛出 `SecurityError` → 全部改为 `SecurityError`
- **VoiceGenerator 异常类型错误**：`_get_audio_duration` 方法 catch `CalledProcessError` 但实际抛 `SecurityError`

### 🧹 Code Cleanup

- **删除未使用接口文件**：移除 `app/core/interfaces/video_maker.py`（272行，0导入）和 `app/services/interfaces.py`（292行，0导入），合计 **-607行**
- **删除重复 Enum 定义**：`audio/__init__.py` 删除了 `BeatStrength`、`MusicSection`、`SyncStrategy`、`TransitionType` 的副本（已存在于子模块）
- **`TTSProvider._get_audio_duration` 去重**：统一到基类 `TTSProvider`，删除 EdgeTTSProvider / OpenAITTSProvider / F5TTSProvider 三个重复副本（-32行）
- **删除死方法**：`FFmpegTool.run_command`（-20行）、`_detect_audio_peaks` 中的死 `import json`、未使用的 `SceneConverter` 实例

### 📚 Documentation

- `ARCHITECTURE.md`：更新目录结构（反映删除的接口文件）、更新 `monologue_maker.py` 行数（658→578）、更新架构债务列表、更新测试状态（389 passed, 0 failed）

### 🔒 Security

- 所有 subprocess 调用统一收敛至 `SecureExecutor`，异常类型统一为 `SecurityError`，无遗漏

### 📊 质量指标

- Tests：**389 passed, 20 skipped, 2 warnings, 0 failed**

---

## [4.0.0] - 2026-04-21

### 🚀 全面重构 Phase 1-4

#### Phase 1：工程质量问题修复
- **animation_helper.py 异常处理**：4处 `except Exception: pass` → `logger.warning`，异常不再被吞掉
- **类型标注完善**：修复 `event_bus.py`、`cache_interface.py` 等文件类型错误
- **导入路径修复**：修正 `app/services/export/` 下 3 个文件的 4-dot 相对导入为 3-dot
- **测试稳定性**：修复 `test_llm_base.py` 断言（ProviderError 信息格式变更）
- **依赖补全**：安装 `openai`、`edge-tts` 依赖

#### Phase 2：UX 改善
- **step_upload.py**（重写 ~560行）：文件夹选择 + Ctrl 多选 + 3列缩略图网格 + 视频预览小窗 + QProgressBar 进度条 + 后台线程缩略图生成
- **step_group.py**（新增 ~520行）：分组预览卡片 + 拖拽合并/拆分 + 置信度颜色动态显示（>80%绿/60-80%黄/<60%红）+ 新建/删除分组
- **step_preview.py**（新增 ~520行）：解说文案分段预览 + 编辑模式 + 7种预设风格 + 角色参数自定义 + 实时字数统计

#### Phase 3：核心功能实现（TDD 驱动，39 tests）
- **SmartGrouper**（`app/services/video/grouping/smart_grouper.py`）：视觉+音频混合相似度分组（视觉权重0.7+音频权重0.3），层次聚类，9 tests ✅
- **FirstPersonExtractor**（`app/services/video/extraction/first_person_extractor.py`）：逐帧第一人称分析，9-60秒片段提取，10 tests ✅
- **EmotionPeakDetector**（`app/services/video/extraction/emotion_peak_detector.py`）：视觉复杂度+音频情绪峰值检测，9 tests ✅
- **SegmentSelector**（`app/services/video/selection/segment_selector.py`）：叙事完整+情感峰值混合选段策略，11 tests ✅

#### Phase 4：架构重构
- **模块化拆分**：`app/services/video/` 细分为 extraction/selection/grouping/tools/analyzers/loaders/cutters 7个子目录，统一 `__init__.py` 导出
- **AI Provider 插件化**：`app/services/ai/interfaces.py` 定义 `VisionProvider`/`LLMProvider`/`TTSProvider` 协议；`app/services/ai/registry.py` 实现 `ProviderRegistry` 单例 + YAML 配置热加载
- **测试覆盖**：新增 65 tests（video services 39 + ai registry 26）

### 📊 质量指标
- Tests：294 → **294+65 passed**（+26 skipped）
- Pyright errors：294 → **287**

### 🏷️ Tags
- `v4.0.0` — 完整 Phase 1-4 改进

---

## [3.10.0] - 2026-04-19

### 🎨 UI 统一与组件化

- **设置页面设计系统升级**：`settings_page.py` 所有 QLabel/QPushButton/QLineEdit/QFrame 硬编码样式 → 替换为 `CF*` 组件体系（`CFLabel`、`CFButton`、`CFInput`、`CFCard`），消除 100+ 行硬编码 CSS
- **欢迎页颜色系统统一**：`welcome_screen.py` 旧 hex 色彩表 → 接入 OKLCH `Colors` 类，`QPainter` 绘制处使用 hex fallback，保持与主应用色彩一致
- **新增 CFToastNotification 组件**：`design_system.py` 新增 Toast 通知组件，支持 info/success/warning/error 四种类型，自动消失（默认 3s），右下角堆叠显示，交互动画接入 `AnimationHelper`
- **全 UI 色彩系统统一**：10 个文件 50+ 处 `setStyleSheet` 硬编码 hex 颜色 → `Colors` OKLCH 常量，涵盖 home_page、home_components、timeline、video_preview、export_monitor、properties_panel、main_window、theme_optimizer、pro_components、layout 等核心页面和组件

### 🐛 Bug Fixes

- **版本号修复**：settings_page.py 硬编码 `"版本 3.2.0"` → `"版本 3.9.0"`，pyproject.toml `3.8.1` → `3.9.0`

---

## [3.9.0] - 2026-04-19

### 🐛 Bug Fixes

- **P0 修复**：`LLMManager.ask()` / `generate_sync()` 返回 `None` 的问题 —— 原实现在 running loop 中返回 `(loop, future)` 元组而非实际结果，改为在新线程独立 loop 中运行，确保同步调用返回正确字符串
- **Provider 健康检查超时**：`BaseLLMProvider.health_check()` 原本是 `@abstractmethod` 但无默认实现，导致 provider 在网络超时时长阻塞；新增带 5s 超时的默认实现

### ⚡ 性能优化

- **请求去重**：`BaseLLMProvider.generate_batch()` 新增 `deduplicate=True` 参数，对相同 prompt+model+temperature 的请求只调用一次 API，大幅减少批量场景下的重复调用
- **磁盘持久化缓存**：新增 `LLMDiskCache` 类（`app/services/ai/cache.py`），基于 SQLite，重启后缓存不丢失，默认 TTL=24h，最大 500MB，自动 LRU 淘汰

### 🔧 代码质量

- **print → logger**：移除 `app/core/application.py`、`app/core/logger.py`、`app/utils/error_handler.py` 中的裸 `print()` 调用，统一改为 `logging.getLogger()` 输出
- **删除重复定义**：`BaseLLMProvider` 中重复的 `health_check` abstractmethod 声明已移除

# 更新日志

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.8.0] - 2026-04-14

### ⚡ 性能优化

- **Whisper 默认改为本地模式**：`SpeechSubtitleExtractor` 默认 `mode="local"` 替代 `"api"`，无需 API key，离线可用
- **Whisper 模型升级**：默认模型从 `"base"` 升为 `"medium"`，精度大幅提升
- **GPU 批处理加速**：`SpeechSubtitleExtractor` 和 `WhisperASRProvider` 均支持 `batch_size=8`，GPU 推理 **8.9x 加速**（faster-whisper benchmark）
- **LLM 请求缓存激活**：`RequestCache`（TTL=24h）接入 `BaseLLMProvider.generate_batch()`，重复 prompt 零 API 调用，所有 9 个 Provider 自动继承
- **CPU INT8 量化**：`faster-whisper` CPU 模式默认 INT8，2.4x 加速
- **移除死依赖**：`ffmpeg-python==0.2.0`（2019 年停更）从 requirements.txt 和 pyproject.toml 删除，减少安装体积

---

## [3.7.0] - 2026-04-13

### 🎨 UI 无障碍与动效优化

- **Focus-visible 修复**：`dark_theme.qss` 移除重复的 `:focus { outline: none }` 规则，键盘导航时正确显示焦点环
- **prefers-reduced-motion 支持**：`animation_helper.py` 添加跨平台系统减少动画偏好检测：
  - macOS: AppleReduceMotion
  - Windows: EaseOfAccess 显示动画选项
  - Linux: GTK/KDE 减少动画设置
  - 所有动画方法添加 `_get_reduced_duration()` 降级处理
  - 添加 `invalidate_cache()` 方法供设置变更时重置
- **EmptyState 组件统一**：`home_page.py` 内联空状态替换为 `MacEmptyStateV2` 统一组件

---

## [3.6.0] - 2026-04-11

### 🏗️ 架构升级

- **类型安全强化**：`models.py` Any: 89→0，Pydantic v2 替换 dataclass，7个新子类型
- **LLM Provider 统一抽象**：新建 `provider_models.py`（Pydantic 模型），修复 Hunyuan/Doubao `usage` 字段

### 🔧 代码优化与加固

- **P0 修复**：`step_upload.py` 裸 `except:pass` → 日志记录
- **P1 修复**：15处空 `except:pass` 统一加日志（8个文件）
- **P2 收尾**：`event_bus.py` 日志、`service_manager.py` 导入风格统一

### 🎨 UI 组件拆分

- **AIMonitorPanel 拆分**：1116行 → 657行主容器 + `monitor_widgets.py`(273行) + `monitor_pages.py`(265行)
- **ExportPanel 拆分**：936行 → 647行主容器 + `export_format_selector.py`(146行) + `export_progress.py`(179行)

### 📦 依赖与规范

- 添加缺失 `__init__.py`（`ai_enhancement/`、`video_tutorial/`）

---

## [3.5.0] - 2026-04-10

### 🎨 UI 全面重设计

- **创作向导重构 (Phase 1)**：3 步创作向导页面重设计
- **WizardPage 信号管理**：修复信号重复绑定 + StepPipeline 断开旧连接
- **StageCard 动画**：修复动画问题
- **CreationWizardPage 继承 BasePage**：main_window 对接新向导

### 🐛 Bug Fixes

- 导出路径传递 + Step3 显示草稿位置
- 向导页 3 处运行时问题修复
- 清理废弃页面代码

---

## [3.4.1] - 2026-04-09

### 🐛 Bug Fixes

- 修复 UI 重构后全部 3 处问题

---

## [3.4.0] - 2026-04-09

### 🎨 UI 重构 (P0/P1/P2/P3)

- **P0 核心交付**：全面 UI 重构 + 死代码清理
- OKLCH 色彩系统、OutCubic 缓动动画、专业设计规范

---

## [3.3.0] - 2026-04-08

### ⚡ 性能优化

- **Scene Detection**：视频场景检测性能改进

---

## [3.2.0] - 2026-04-05

### Changed
- **品牌重命名**: Voxplore → Voxplore，专注 AI 第一人称视频解说
- **产品定位重构**: 裁剪全部冗余功能（MashupMaker / BeatSyncMaker / CommentaryMaker / BatchProcessor 等），只保留 MonologueMaker 核心
- **模型升级**: Qwen2.5-VL（视频理解）+ DeepSeek-V4（解说生成）+ SenseVoice（ASR）+ Edge-TTS + F5-TTS（配音）
- **导出架构精简**: 移除 PremiereExporter / DaVinciExporter / FinalCutExporter / EDLExporter，只保留 DirectVideoExporter + JianyingExporter
- **文档全面更新**: README.md / docs/index.md / docs/README.md / SPEC.md 全部重写
- **在线文档**: FAQ 合并疑难排查内容

### Added
- **无头环境适配**: main.py / application_launcher.py 自动检测 offscreen 平台
- **libEGL 依赖**: 自动安装 EGL 图形库，解决无显示器环境运行问题

### Fixed
- **运行无反应**: 无 DISPLAY 环境下 Qt 应用静默退出的问题，自动设置 QT_QPA_PLATFORM=offscreen

## [3.1.1] - 2026-04-03

### Refactored
- **FFmpeg 工具统一**: 消除重复的 `_check_ffmpeg()` 和 `_get_video_duration()` 实现
  - 新增 `FFmpegTool.check_ffmpeg()` 方法
  - 统一从 `app/services/video_tools/ffmpeg_tool.py` 导出
  - 删除 144 行重复代码
- **TransitionType 枚举统一**: `mashup_maker.py` 改从 `transition_effects.py` 导入
- **PaceLevel 枚举值修复**: 从中文改为英文 (`"慢节奏"` → `"slow"` 等)
- **CachePolicy 改为正式 Enum**: `app/core/interfaces/cache_interface.py`

### Fixed
- **代码质量**: 
  - 修复 56 个 API 设计问题测试
  - 修复所有 lint 错误 (ruff check 全绿)
  - pytest asyncio 配置完善 (asyncio_mode = auto)
  - 安装 pytest-asyncio 消除警告
- **测试覆盖**: 新增 `tests/test_llm_cache.py` (23 个测试用例)
- **缩略图缓存** (`thumbnail_cache.py`):
  - 修复 LRU 驱逐逻辑：按 mtime 而非 path 字母排序
  - 修复缓存重启后 video_path 全丢失：新增 JSON 索引持久化
  - 修复 async 函数未真正 await：改为同步函数 + 新增 `generate_thumbnail_async`
  - 缓存命中时更新 mtime 以保证 LRU 准确性

### Chores
- **死代码清理**:
  - 删除 `app/utils/video_utils.py` (未使用)
  - 删除 `app/core/templates/project_templates.py` (未使用)
  - 删除 `app/config/config.py` (与 core/config_manager 重复)
  - 删除对应测试文件
  - 共删除 820 行

---

## [3.1.0] - 2026-03-23

### Changed
- **UI 框架迁移**: PyQt6 → PySide6 (LGPL 授权，商业友好)
- **依赖更新**: 
  - PyQt6 → PySide6>=6.6.0
  - 新增 Shiboken6>=6.6.0

### Fixed
- **代码审核修复**:
  - `EventBus.subscribe()` bug (访问未定义变量)
  - `SecureKeyManager` 无限循环问题
  - `ServiceContainer` 无效异常处理
  - 所有 LLM Provider 添加 `response.raise_for_status()`
  - 修复 `LLMResponse` 字段错误 (`usage` → `tokens_used`)
  - 修复安全模块无效转义序列
  
- **合规化修复**:
  - 删除重复文件 (`macos_theme_manager.py`, `macos_components.py`)
  - 187 个文件添加 MIT 版权头
  - PBKDF2 迭代次数提升至 480,000 (OWASP 标准)
  - DEBUG print 语句替换为 `logger.debug()`

### Security
- PBKDF2HMAC iterations: 100,000 → 480,000
- 添加 `__slots__` 建议到文档
- 完善异常处理和安全验证

### Documentation
- 更新 README.md (PySide6)
- 更新 ARCHITECTURE.md
- 更新 docs/README_EN.md
- 更新 docs/getting-started.md
- 更新 docs/features.md
- 添加合规化检测报告

---

## [3.0.0] - 2026-03-08

### Added
- **AI 创作模式**
  - 🎙️ AI 视频解说 (Commentary Maker)
  - 🎵 AI 视频混剪 (Mashup Maker)
  - 🎭 AI 第一人称独白 (Monologue Maker)

- **AI 模型支持**
  - OpenAI GPT-4o / GPT-5
  - Anthropic Claude Sonnet 4.5
  - Google Gemini 3.1 Flash/Pro
  - 阿里云 Qwen 3.5 / Max
  - DeepSeek R1 / V3.2
  - 智谱 GLM-5
  - 月之暗面 Kimi K2.5
  - 字节豆包 Doubao Pro/Lite
  - 腾讯混元 Hunyuan Pro
  - Edge TTS / OpenAI TTS

- **导出预设**
  - B站 (1080P 60fps)
  - YouTube (4K 60fps)
  - Twitter (1080P 压缩)
  - TikTok (竖屏)
  - 微信 (压缩)

- **UI 组件库**
  - GradientButton 渐变按钮
  - GlassCard 玻璃卡片
  - StatCard 统计卡片
  - ProgressRing 环形进度条

- **工具模块**
  - 懒加载 (LazyLoader)
  - 内存缓存 (MemoryCache)
  - 性能监控 (PerformanceMonitor)
  - 国际化 (I18n)
  - 后台任务 (TaskManager)
  - 视频工具 (VideoUtils)
  - 统一配置 (ConfigManager)
  - 统一日志 (Logger)

- **测试**
  - E2E 集成测试
  - 性能基准测试

### Changed
- UI 升级到 V3.0 专业暗色主题
- 可折叠导航栏
- 主题切换修复
- 代码重构，减少重复

### Fixed
- GitHub Actions CI/CD
- GitHub Pages 部署

---

## [2.0.0] - 2025-XX-XX

### Added
- 基础 AI 功能
- 视频导出

---

## [1.0.0] - 2024-XX-XX

### Added
- 项目初始化
- 基础 UI 框架
