---
title: 快速开始
description: Voxplore 5 分钟快速上手指南，从下载安装到生成第一个视频解说。
---

# 快速开始

5 分钟内完成从安装到生成第一个视频解说的全流程。

---

## 下载安装

### Windows

1. 访问 [Releases](https://github.com/Agions/Voxplore/releases/latest) 下载 `Voxplore-x.x.x-win.exe`
2. 双击运行，按提示完成安装
3. 从开始菜单启动 Voxplore

### macOS

1. 访问 [Releases](https://github.com/Agions/Voxplore/releases/latest) 下载 `Voxplore-x.x.x.dmg`
2. 打开 DMG，将 Voxplore 拖入应用程序
3. 首次运行右键点击 →「打开」→ 确认

> 如果提示"无法验证开发者"，见 [FAQ](../faq#macos-提示无法打开因为无法验证开发者)

### Linux

```bash
chmod +x Voxplore-x.x.x.AppImage
./Voxplore-x.x.x.AppImage
```

如缺少依赖：`sudo apt install fuse libfuse2 libegl1 libgl1 libxkbcommon0 libdbus-1-3`

### 从源码运行

```bash
git clone https://github.com/Agions/Voxplore.git
cd Voxplore
pip install -r requirements.txt
python app/main.py
```

---

## 配置 API Key

### DeepSeek（推荐）

1. 访问 [platform.deepseek.com](https://platform.deepseek.com) 注册账号
2. 在「API Keys」页面创建新 Key
3. 在 Voxplore 设置中填入，或设置环境变量：

```bash
export DEEPSEEK_API_KEY=sk-xxx...xxxx
```

> **费用**：DeepSeek-V4 价格约为 GPT-4o 的 **1/50**，处理一个 5 分钟视频不足 **1 分钱**。

### 阿里云百炼（视频理解）

```bash
export DASHSCOPE_API_KEY=sk-xxx...xxxx
```

> 访问 [bailian.console.aliyun.com](https://bailian.console.aliyun.com) 开通服务。

### 无 API Key 也能用

即使不配置任何 API Key，Voxplore 仍可：
- 使用本地 FFmpeg 处理视频
- 使用 Edge-TTS 免费配音合成
- 手动编辑解说稿

---

## 首次使用

### Step 1：创建项目

启动 Voxplore 后，点击「新建项目」，输入项目名称。

### Step 2：上传视频

| 方式 | 操作 |
|------|------|
| 文件夹选择 | 点击「选择文件夹」，AI 自动扫描所有视频 |
| Ctrl 多选 | 按住 Ctrl 点击多个视频文件 |
| 拖拽 | 直接将视频文件拖入窗口 |

支持格式：MP4、MOV、AVI、MKV、WebM

### Step 3：等待 AI 分析

| 阶段 | 说明 | 参考时间 |
|------|------|----------|
| 场景理解 | Qwen2.5-VL 逐帧分析 | 3–5 分钟 |
| 智能分组 | 视觉+声纹混合相似度 | 2–3 分钟 |
| 情感检测 | 识别画面高潮片段 | 1–2 分钟 |

> 使用 GPU 可将视频理解时间缩短 **5 倍**。

### Step 4：生成解说

1. 选择情感风格（治愈/悬疑/励志/怀旧/浪漫/幽默/纪录片）
2. 点击「生成解说」
3. AI 自动生成第一人称解说稿
4. 可手动编辑解说内容

### Step 5：导出成品

| 格式 | 说明 |
|------|------|
| MP4（H.264） | 兼容性最好，跨平台播放 |
| MP4（H.265） | 体积小约 40%，老设备可能不兼容 |
| 剪映草稿 | JSON 格式，导入剪映继续精剪 |

---

## 4 步工作流总览

```
上传视频 → AI 分析 → 生成解说 → 导出成品
   │          │           │          │
   ▼          ▼           ▼          ▼
 文件夹/    场景理解     DeepSeek   MP4/
 多选       智能分组     -V4        剪映
            情感峰值     Edge-TTS
```

---

## 常见问题

### 报错「API Key 无效」

1. 确认 Key 已正确复制（注意无多余空格）
2. 检查 Key 是否已过期或额度用完
3. 确认使用的是正确的 Key 类型（DeepSeek 用 DeepSeek Key）

### 处理很慢怎么办

- **使用 GPU**：设置 → AI 配置 → 启用 GPU 加速
- **减少抽帧密度**：设置 → 场景理解 → 抽帧间隔，改为 2 秒
- **降低分辨率**：1080p → 720p

详见 [常见问题](../faq)。

---

## 下一步

- [功能详解](../features) — 了解全部功能
- [AI 模型配置](../ai-models) — 各模型配置指南
- [导出格式](./exporting) — 详细导出参数
- [常见问题](../faq) — 问题解答
