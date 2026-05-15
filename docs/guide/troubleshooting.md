---
title: 疑难排查
description: Voxplore 常见问题与解决方案。
---

# 疑难排查

## 常见问题

### 视频上传失败

**可能原因：**
- 文件格式不支持（仅支持 mp4/mov/avi/webm）
- 文件损坏或编码不兼容

**解决方案：**
使用 FFmpeg 重新编码：
```bash
ffmpeg -i input.mkv -c:v libx264 -c:a aac output.mp4
```

### AI 分析耗时过长

**可能原因：**
- 网络连接不稳定
- API 限流

**解决方案：**
- 检查网络
- 减少同时分析的视频数量

### 配音无声

**可能原因：**
- Edge-TTS 未正确安装
- 系统音频输出被禁用

**解决方案：**
```bash
pip install edge-tts
```

### API Key 无效

**检查项：**
- Key 是否过期
- 是否正确设置环境变量
- 额度是否充足

---

更多问题请提交 [GitHub Issue](https://github.com/Agions/Voxplore/issues)。
