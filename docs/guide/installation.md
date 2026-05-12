---
title: 安装指南
description: Voxplore 各平台完整安装步骤与依赖配置。
---

# 安装指南

---

## 系统要求

### 最低配置

| 组件 | 要求 |
|------|------|
| 操作系统 | Windows 10+ / macOS 11+ / Ubuntu 20.04+ |
| 内存 | 8 GB |
| 存储 | 10 GB 可用空间 |
| GPU | 可选（用于加速视频理解） |

### 推荐配置

| 组件 | 要求 |
|------|------|
| 内存 | 16 GB+ |
| 存储 | 50 GB+（处理大文件时需要）|
| GPU | NVIDIA GTX 1060+（显存 6GB+）|

---

## Windows 安装

### 下载安装包

1. 访问 [Releases](https://github.com/Agions/Voxplore/releases/latest)
2. 下载 `Voxplore-x.x.x-win.exe`
3. 双击运行，按提示完成安装

### 便携版

如需免安装版本，下载 `.zip` 便携版，解压后直接运行 `Voxplore.exe`。

---

## macOS 安装

### 下载安装包

1. 访问 [Releases](https://github.com/Agions/Voxplore/releases/latest)
2. 下载 `Voxplore-x.x.x.dmg`
3. 打开 DMG，将 Voxplore 拖入应用程序文件夹

### 首次运行

如果提示「无法验证开发者」：

1. 右键点击 Voxplore →「打开」
2. 弹出提示时点击「打开」

或在终端执行：
```bash
xattr -d com.apple.quarantine /Applications/Voxplore.app
```

---

## Linux 安装

### AppImage（推荐）

```bash
# 下载后添加执行权限
chmod +x Voxplore-x.x.x.AppImage
./Voxplore-x.x.x.AppImage
```

### 依赖安装

部分 Linux 发行版需要安装额外库：
```bash
sudo apt install fuse libfuse2 libegl1 libgl1 libxkbcommon0 libdbus-1-3
```

### 无头环境运行

Linux 服务器或 Docker 容器中，Voxplore 自动使用 `QT_QPA_PLATFORM=offscreen` 模式：

```bash
export QT_QPA_PLATFORM=offscreen
python3 app/main.py
```

---

## 从源码安装

### 克隆代码

```bash
git clone https://github.com/Agions/Voxplore.git
cd Voxplore
```

### 创建虚拟环境（推荐）

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
python app/main.py
```

---

## Docker 部署

### Dockerfile

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg libegl1 libgl1 libxkbcommon0 libdbus-1-3 libgtk-3-0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "app/main.py"]
```

### 构建与运行

```bash
docker build -t voxplore .
docker run -v /path/to/videos:/videos voxplore
```

---

## 依赖说明

### FFmpeg（必需）

Voxplore 使用 FFmpeg 进行视频处理。

| 系统 | 安装方式 |
|------|----------|
| Windows | 自动安装或从 [ffmpeg.org](https://ffmpeg.org) 下载 |
| macOS | `brew install ffmpeg` |
| Ubuntu | `sudo apt install ffmpeg` |

### Python 依赖

核心依赖（`requirements.txt`）：

| 包 | 说明 |
|----|------|
| PySide6 | Qt 6 桌面框架 |
| OpenCV | 视频处理 |
| moviepy | 视频编辑 |
| faster-whisper | 本地 ASR |
| edge-tts | 微软语音合成 |
| openai | API 调用 |

---

## 配置 AI API Key

详见 [AI 模型配置](../ai-models)。

### DeepSeek（解说生成）

```bash
export DEEPSEEK_API_KEY=sk-xxx...xxxx
```

### 阿里云百炼（视频理解）

```bash
export DASHSCOPE_API_KEY=sk-xxx...xxxx
```

---

## 故障排除

### Qt 平台插件加载失败

```bash
# Linux
sudo apt install libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0
```

### 音频设备未找到

Linux 无头环境中，确保设置了 `QT_QPA_PLATFORM=offscreen`。

### GPU 不可用

Voxplore 自动检测 CUDA。如需手动禁用：
```bash
export CUDA_VISIBLE_DEVICES=""
python app/main.py
```

---

## 下一步

- [快速开始](./quick-start) — 5 分钟上手
- [AI 模型配置](../ai-models) — API Key 配置
- [常见问题](../faq) — 问题解答
