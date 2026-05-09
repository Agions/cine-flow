---
layout: home

title: Voxplore
titleTemplate: false

hero:
  name: Voxplore
  text: AI First-Person Video Narrator
  tagline: 批量上传视频 · AI 自动分组选段 · 一键生成电影感配音解说
  image:
    src: /logo.png
    alt: Voxplore
  actions:
    - theme: brand
      text: 快速开始 →
      link: /guide/quick-start
    - theme: alt
      text: 查看功能
      link: /features
    - theme: alt
      text: GitHub ⭐
      link: https://github.com/Agions/Voxplore

features:
  - icon:
      src: /icons/multi-video.svg
    title: 多视频智能合并
    details: 批量上传视频，AI 视觉+声纹混合分组，避免同一人重复生成解说
  - icon:
      src: /icons/monologue.svg
    title: 第一人称片段提取
    details: 逐帧分析画面，Qwen2.5-VL 判断"我"的视角，提取情感峰值高光片段
  - icon:
      src: /icons/emotion.svg
    title: 情感峰值驱动选段
    details: 叙事完整优先 + 情感峰值加权，悬疑铺垫 → 剧情高潮 → 情感共鸣
  - icon:
      src: /icons/module.svg
    title: 模块化成品输出
    details: 合并版完整叙事 + 高光片段单独发布，最大化内容分发效率
  - icon:
      src: /icons/style.svg
    title: 7 种情感风格
    details: 治愈/悬疑/励志/怀旧/浪漫/幽默/纪录片 + 角色设定自定义
  - icon:
      src: /icons/export.svg
    title: 多格式导出
    details: H.264/H.265 MP4 直出，或原生剪映草稿 JSON，无缝继续精剪
---

<div class="vp-home">

<!-- Hero Animations -->
<div class="vp-hero-animations">
  <div class="vp-float-card vp-float-1">
    <span class="vp-float-icon">🎬</span>
    <span class="vp-float-text">Qwen2.5-VL</span>
  </div>
  <div class="vp-float-card vp-float-2">
    <span class="vp-float-icon">🎙️</span>
    <span class="vp-float-text">DeepSeek-V4</span>
  </div>
  <div class="vp-float-card vp-float-3">
    <span class="vp-float-icon">✍️</span>
    <span class="vp-float-text">SenseVoice</span>
  </div>
</div>

<!-- Social Proof Bar -->
<div class="vp-proof-bar">
  <span class="vp-proof-item">
    <svg class="vp-proof-dot" viewBox="0 0 8 8" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="4" r="3.5" fill="#10B981"/></svg>
    v1.0.1 最新
  </span>
  <span class="vp-proof-sep">·</span>
  <span class="vp-proof-item">
    <svg class="vp-proof-dot" viewBox="0 0 8 8" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="4" r="3.5" fill="#0A84FF"/></svg>
    DeepSeek-V4 解说
  </span>
  <span class="vp-proof-sep">·</span>
  <span class="vp-proof-item">
    <svg class="vp-proof-dot" viewBox="0 0 8 8" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="4" r="3.5" fill="#8B5CF6"/></svg>
    SenseVoice ASR
  </span>
  <span class="vp-proof-sep">·</span>
  <span class="vp-proof-item">
    <svg class="vp-proof-dot" viewBox="0 0 8 8" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="4" r="3.5" fill="#F59E0B"/></svg>
    &lt;¥0.01 / 视频
  </span>
  <span class="vp-proof-sep">·</span>
  <span class="vp-proof-item">
    <svg class="vp-proof-dot" viewBox="0 0 8 8" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="4" r="3.5" fill="#EF4444"/></svg>
    MIT 开源
  </span>
</div>

<!-- Comparison Table -->
<section class="vp-section">
  <h2 class="vp-section-title">vs 传统视频解说</h2>
  <div class="vp-compare">
    <div class="vp-compare-header">
      <div></div>
      <div><strong>传统方式</strong></div>
      <div><strong>Voxplore</strong></div>
    </div>
    <div class="vp-compare-row">
      <div class="vp-compare-label">制作时间</div>
      <div class="vp-compare-old">30–120 分钟</div>
      <div class="vp-compare-new">3–10 分钟</div>
    </div>
    <div class="vp-compare-row">
      <div class="vp-compare-label">配音成本</div>
      <div class="vp-compare-old">¥50–500/分钟</div>
      <div class="vp-compare-new">&lt;¥0.01/视频</div>
    </div>
    <div class="vp-compare-row">
      <div class="vp-compare-label">技术门槛</div>
      <div class="vp-compare-old">专业剪辑 + 配音</div>
      <div class="vp-compare-new">上传视频，一键完成</div>
    </div>
    <div class="vp-compare-row">
      <div class="vp-compare-label">隐私安全</div>
      <div class="vp-compare-old">上传第三方平台</div>
      <div class="vp-compare-new">视频永不上传云端</div>
    </div>
    <div class="vp-compare-row">
      <div class="vp-compare-label">字幕同步</div>
      <div class="vp-compare-old">手动对齐，耗时费眼</div>
      <div class="vp-compare-new">TTS word-level，50ms 精度</div>
    </div>
    <div class="vp-compare-row">
      <div class="vp-compare-label">导出格式</div>
      <div class="vp-compare-old">仅 MP4</div>
      <div class="vp-compare-new">MP4 + 剪映草稿 JSON</div>
    </div>
  </div>
</section>

<!-- Why Voxplore -->
<section class="vp-section">
  <h2 class="vp-section-title">为什么选择 Voxplore</h2>
  <div class="vp-why-grid">
    <div class="vp-why-card">
      <div class="vp-why-icon">⚡</div>
      <h3>3 分钟完成解说</h3>
      <p>从上传视频到导出成品，全流程自动化。AI 自动分析、自动写稿、自动配音，无需手动剪辑。</p>
    </div>
    <div class="vp-why-card">
      <div class="vp-why-icon">💰</div>
      <h3>不到一分钱一个视频</h3>
      <p>DeepSeek-V4 成本约 $0.1 / 1M tokens。处理一个 5 分钟视频成本不足 <strong>1 分钱</strong>。</p>
    </div>
    <div class="vp-why-card">
      <div class="vp-why-icon">🔒</div>
      <h3>视频永不上传云端</h3>
      <p>全部处理在本地完成。FFmpeg 本地合成，API 仅传输文字（解说稿），你的视频永远留在本机。</p>
    </div>
    <div class="vp-why-card">
      <div class="vp-why-icon">🎭</div>
      <h3>7 种情感风格</h3>
      <p>治愈 · 悬疑 · 励志 · 怀旧 · 浪漫 · 幽默 · 纪录片。AI 根据视频内容自动匹配最合适的解说语气。</p>
    </div>
  </div>
</section>

<!-- 4-Step Workflow -->
<section class="vp-section">
  <h2 class="vp-section-title">4 步创作流程</h2>
  <div class="vp-workflow">
    <div class="vp-workflow-step" data-step="1">
      <div class="vp-workflow-num">1</div>
      <div class="vp-workflow-body">
        <div class="vp-workflow-title">上传视频</div>
        <div class="vp-workflow-desc">文件夹选择 / Ctrl 多选，自动扫描 mp4/mov/avi/webm</div>
      </div>
    </div>
    <div class="vp-workflow-arrow">→</div>
    <div class="vp-workflow-step" data-step="2">
      <div class="vp-workflow-num">2</div>
      <div class="vp-workflow-body">
        <div class="vp-workflow-title">场景理解</div>
        <div class="vp-workflow-desc">Qwen2.5-VL 逐帧分析，提取"我"的主体视角高光片段</div>
      </div>
    </div>
    <div class="vp-workflow-arrow">→</div>
    <div class="vp-workflow-step" data-step="3">
      <div class="vp-workflow-num">3</div>
      <div class="vp-workflow-body">
        <div class="vp-workflow-title">情感选段</div>
        <div class="vp-workflow-desc">叙事完整优先 + 情感峰值驱动，悬疑铺垫 → 高潮 → 共鸣</div>
      </div>
    </div>
    <div class="vp-workflow-arrow">→</div>
    <div class="vp-workflow-step" data-step="4">
      <div class="vp-workflow-num">4</div>
      <div class="vp-workflow-body">
        <div class="vp-workflow-title">解说 + 导出</div>
        <div class="vp-workflow-desc">DeepSeek-V4 生成文案 + Edge-TTS 配音，MP4 / 剪映草稿输出</div>
      </div>
    </div>
  </div>
</section>

<!-- Tech Stack -->
<section class="vp-section">
  <h2 class="vp-section-title">技术栈</h2>
  <div class="vp-arch-table">
    <div class="vp-arch-row vp-arch-header">
      <div>模块</div><div>模型 / 技术</div><div>说明</div>
    </div>
    <div class="vp-arch-row">
      <div><span class="vp-arch-badge">分组</span></div>
      <div><code>Qwen2.5-VL</code> + 声纹</div>
      <div>视觉 0.7 + 音频 0.3 混合相似度</div>
    </div>
    <div class="vp-arch-row">
      <div><span class="vp-arch-badge">提取</span></div>
      <div><code>Qwen2.5-VL</code></div>
      <div>逐帧分析，主体视角判断，9–60 秒片段</div>
    </div>
    <div class="vp-arch-row">
      <div><span class="vp-arch-badge">情感</span></div>
      <div>视觉 + 音频双维度</div>
      <div>画面信息密度 + 语调变化，综合评分排序</div>
    </div>
    <div class="vp-arch-row">
      <div><span class="vp-arch-badge">解说</span></div>
      <div><code>DeepSeek-V4</code></div>
      <div>代入"我"视角，7 种预设风格 + 角色设定</div>
    </div>
    <div class="vp-arch-row">
      <div><span class="vp-arch-badge">配音</span></div>
      <div><code>Edge-TTS</code> · <code>F5-TTS</code></div>
      <div>Edge 主流低延迟，F5 零样本音色克隆</div>
    </div>
    <div class="vp-arch-row">
      <div><span class="vp-arch-badge">导出</span></div>
      <div><code>MP4</code> · <code>剪映草稿</code></div>
      <div>合并版 + 高光片段双输出</div>
    </div>
  </div>
</section>

<!-- Quick Start Cards -->
<section class="vp-section">
  <h2 class="vp-section-title">快速开始</h2>
  <div class="vp-start-grid">
    <a href="/guide/quick-start" class="vp-start-card">
      <div class="vp-start-icon">🚀</div>
      <div class="vp-start-title">5 分钟快速上手</div>
      <div class="vp-start-desc">下载安装包 / Homebrew / 源码运行，三种方式任选</div>
      <div class="vp-start-arrow">→</div>
    </a>
    <a href="/guide/quick-start#配置-api-key" class="vp-start-card">
      <div class="vp-start-icon">🔑</div>
      <div class="vp-start-title">配置 DeepSeek API</div>
      <div class="vp-start-desc">每月约 ¥7 足够，处理一个 5 分钟视频不足 1 分钱</div>
      <div class="vp-start-arrow">→</div>
    </a>
    <a href="/features" class="vp-start-card">
      <div class="vp-start-icon">📖</div>
      <div class="vp-start-title">功能详解</div>
      <div class="vp-start-desc">情感风格、字幕样式、导出格式、硬件要求全解析</div>
      <div class="vp-start-arrow">→</div>
    </a>
  </div>
</section>

<!-- Stats Footer -->
<div class="vp-stats-row">
  <div class="vp-stat">
    <div class="vp-stat-val">v1.0.1</div>
    <div class="vp-stat-lbl">最新版本</div>
  </div>
  <div class="vp-stat-sep">|</div>
  <div class="vp-stat">
    <div class="vp-stat-val">MIT</div>
    <div class="vp-stat-lbl">开源协议</div>
  </div>
  <div class="vp-stat-sep">|</div>
  <div class="vp-stat">
    <div class="vp-stat-val">Python 3.10+</div>
    <div class="vp-stat-lbl">跨平台</div>
  </div>
  <div class="vp-stat-sep">|</div>
  <div class="vp-stat">
    <div class="vp-stat-val">PySide6</div>
    <div class="vp-stat-lbl">Qt 桌面端</div>
  </div>
  <div class="vp-stat-sep">|</div>
  <div class="vp-stat">
    <div class="vp-stat-val">&lt;¥0.01</div>
    <div class="vp-stat-lbl">单视频成本</div>
  </div>
</div>

</div>

<style>
/* ============================================
   Voxplore Home — Design System
   简约科技风 · OKLCH暗色 · 动画优先
   ============================================ */

/* Animations */
@keyframes float-1 {
  0%, 100% { transform: translateY(0px) rotate(-3deg); }
  50% { transform: translateY(-12px) rotate(3deg); }
}
@keyframes float-2 {
  0%, 100% { transform: translateY(0px) rotate(2deg); }
  50% { transform: translateY(-8px) rotate(-2deg); }
}
@keyframes float-3 {
  0%, 100% { transform: translateY(0px) rotate(-2deg); }
  50% { transform: translateY(-10px) rotate(4deg); }
}
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes slide-right {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse-ring {
  0%   { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70%  { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Hero Animations */
.vp-home .vp-hero-animations {
  position: relative;
  height: 80px;
  margin-bottom: 24px;
}
.vp-home .vp-float-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  font-size: 12px;
  color: rgba(255,255,255,0.7);
  backdrop-filter: blur(8px);
  opacity: 0;
  animation: fade-in 0.5s ease forwards;
}
.vp-home .vp-float-card .vp-float-icon { font-size: 16px; }
.vp-home .vp-float-1 {
  left: 10%;
  top: 10px;
  animation-delay: 0.6s;
  animation-name: float-1;
  animation-duration: 4s;
  animation-fill-mode: forwards;
}
.vp-home .vp-float-2 {
  left: 40%;
  top: 0;
  animation-delay: 0.9s;
  animation-name: float-2;
  animation-duration: 5s;
  animation-fill-mode: forwards;
}
.vp-home .vp-float-3 {
  right: 10%;
  top: 20px;
  animation-delay: 1.2s;
  animation-name: float-3;
  animation-duration: 3.5s;
  animation-fill-mode: forwards;
}

/* Proof Bar */
.vp-home .vp-proof-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 40px;
  font-size: 13px;
  color: rgba(255,255,255,0.55);
  opacity: 0;
  animation: fade-in 0.5s ease 0.15s forwards;
}
.vp-home .vp-proof-item {
  display: flex;
  align-items: center;
  gap: 5px;
}
.vp-home .vp-proof-dot {
  width: 7px;
  height: 7px;
  flex-shrink: 0;
}
.vp-home .vp-proof-sep { opacity: 0.3; }

/* Section */
.vp-home .vp-section {
  margin: 56px 0;
  opacity: 0;
  animation: fade-up 0.5s ease forwards;
}
.vp-home .vp-section:nth-child(3) { animation-delay: 0.2s; }
.vp-home .vp-section:nth-child(4) { animation-delay: 0.3s; }
.vp-home .vp-section:nth-child(5) { animation-delay: 0.4s; }
.vp-home .vp-section:nth-child(6) { animation-delay: 0.5s; }
.vp-home .vp-section:nth-child(7) { animation-delay: 0.6s; }

.vp-home .vp-section-title {
  font-size: 20px;
  font-weight: 700;
  color: #f0f0f0;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  letter-spacing: -0.01em;
}

/* Comparison Table */
.vp-home .vp-compare {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  overflow: hidden;
}
.vp-home .vp-compare-header,
.vp-home .vp-compare-row {
  display: grid;
  grid-template-columns: 2fr 2fr 2fr;
  gap: 0;
}
.vp-home .vp-compare-header {
  background: rgba(255,255,255,0.04);
  font-size: 13px;
  padding: 10px 20px;
}
.vp-home .vp-compare-row {
  padding: 12px 20px;
  border-top: 1px solid rgba(255,255,255,0.05);
  transition: background 0.15s;
}
.vp-home .vp-compare-row:hover { background: rgba(255,255,255,0.025); }
.vp-home .vp-compare-label {
  font-size: 14px;
  color: rgba(255,255,255,0.5);
}
.vp-home .vp-compare-old {
  font-size: 14px;
  color: rgba(255,255,255,0.35);
  text-decoration: line-through;
}
.vp-home .vp-compare-new {
  font-size: 14px;
  font-weight: 600;
  color: #10B981;
}

/* Why Grid */
.vp-home .vp-why-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
.vp-home .vp-why-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 20px;
  transition: border-color 0.2s, transform 0.2s;
}
.vp-home .vp-why-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  transform: translateY(-2px);
}
.vp-home .vp-why-icon {
  font-size: 28px;
  margin-bottom: 12px;
}
.vp-home .vp-why-card h3 {
  font-size: 15px;
  font-weight: 700;
  color: #f0f0f0;
  margin-bottom: 8px;
}
.vp-home .vp-why-card p {
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  line-height: 1.6;
  margin: 0;
}

/* Workflow */
.vp-home .vp-workflow {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 8px;
}
.vp-home .vp-workflow-step {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 16px;
  flex: 1;
  min-width: 160px;
  transition: border-color 0.2s, transform 0.2s;
}
.vp-home .vp-workflow-step:hover {
  border-color: rgba(10, 132, 255, 0.4);
  transform: translateY(-1px);
}
.vp-home .vp-workflow-num {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0A84FF, #8B5CF6);
  color: #fff;
  font-weight: 800;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  animation: pulse-ring 2.5s infinite;
}
.vp-home .vp-workflow-body { flex: 1; }
.vp-home .vp-workflow-title {
  font-size: 14px;
  font-weight: 700;
  color: #f0f0f0;
  margin-bottom: 4px;
}
.vp-home .vp-workflow-desc {
  font-size: 12px;
  color: rgba(255,255,255,0.45);
  line-height: 1.4;
}
.vp-home .vp-workflow-arrow {
  color: rgba(255,255,255,0.2);
  font-size: 18px;
  flex-shrink: 0;
  padding: 0 4px;
}

/* Architecture Table */
.vp-home .vp-arch-table {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  overflow: hidden;
}
.vp-home .vp-arch-row {
  display: grid;
  grid-template-columns: 100px 200px 1fr;
  gap: 16px;
  padding: 10px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 13px;
  align-items: center;
  transition: background 0.15s;
}
.vp-home .vp-arch-row:last-child { border-bottom: none; }
.vp-home .vp-arch-row:hover { background: rgba(255,255,255,0.025); }
.vp-home .vp-arch-header {
  font-size: 12px;
  font-weight: 600;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  background: rgba(255,255,255,0.03);
}
.vp-home .vp-arch-badge {
  display: inline-block;
  padding: 2px 8px;
  background: rgba(10, 132, 255, 0.15);
  border: 1px solid rgba(10, 132, 255, 0.25);
  border-radius: 6px;
  font-size: 11px;
  color: #0A84FF;
  font-weight: 600;
}
.vp-home .vp-arch-row code {
  font-size: 12px;
  background: rgba(255,255,255,0.06);
  padding: 2px 6px;
  border-radius: 4px;
  color: #a5d6ff;
}
.vp-home .vp-arch-row > div:last-child {
  color: rgba(255,255,255,0.5);
}

/* Start Cards */
.vp-home .vp-start-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}
.vp-home .vp-start-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 16px;
  text-decoration: none !important;
  transition: border-color 0.2s, transform 0.2s, background 0.2s;
  position: relative;
  overflow: hidden;
}
.vp-home .vp-start-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #0A84FF, #8B5CF6);
  opacity: 0;
  transition: opacity 0.2s;
}
.vp-home .vp-start-card:hover {
  border-color: rgba(10, 132, 255, 0.35);
  background: rgba(255,255,255,0.05);
  transform: translateY(-2px);
}
.vp-home .vp-start-card:hover::before { opacity: 1; }
.vp-home .vp-start-icon { font-size: 22px; }
.vp-home .vp-start-title {
  font-size: 14px;
  font-weight: 700;
  color: #f0f0f0;
}
.vp-home .vp-start-desc {
  font-size: 12px;
  color: rgba(255,255,255,0.45);
  line-height: 1.5;
  flex: 1;
}
.vp-home .vp-start-arrow {
  font-size: 14px;
  color: #0A84FF;
  transition: transform 0.2s;
}
.vp-home .vp-start-card:hover .vp-start-arrow { transform: translateX(4px); }

/* Stats Row */
.vp-home .vp-stats-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-top: 48px;
  padding: 20px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  opacity: 0;
  animation: fade-up 0.5s ease 0.7s forwards;
}
.vp-home .vp-stat {
  flex: 1;
  text-align: center;
}
.vp-home .vp-stat-val {
  font-size: 18px;
  font-weight: 800;
  color: #f0f0f0;
  letter-spacing: -0.02em;
}
.vp-home .vp-stat-lbl {
  font-size: 11px;
  color: rgba(255,255,255,0.35);
  margin-top: 2px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.vp-home .vp-stat-sep {
  color: rgba(255,255,255,0.1);
  font-size: 18px;
}

/* Responsive */
@media (max-width: 640px) {
  .vp-home .vp-workflow { flex-direction: column; align-items: stretch; }
  .vp-home .vp-workflow-arrow { transform: rotate(90deg); text-align: center; }
  .vp-home .vp-arch-row { grid-template-columns: 80px 1fr; }
  .vp-home .vp-arch-row > div:last-child { grid-column: 1 / -1; padding-top: 4px; }
  .vp-home .vp-stats-row { flex-wrap: wrap; gap: 12px; }
  .vp-home .vp-stat-sep { display: none; }
  .vp-home .vp-float-card { display: none; }
}
</style>

<script setup>
import { onMounted } from 'vue'

const prefersDark = typeof window !== 'undefined' ? window.matchMedia('(prefers-color-scheme: dark)').matches : true
const root = typeof document !== 'undefined' ? document.documentElement : null

// Inject design tokens for this page
if (root) {
  root.style.setProperty('--vp-c-brand-1', '#10B981')
  root.style.setProperty('--vp-c-brand-2', '#059669')
  root.style.setProperty('--vp-c-brand-3', '#0A84FF')
}

onMounted(() => {
  // Stagger workflow steps
  const steps = document.querySelectorAll('.vp-workflow-step')
  steps.forEach((el, i) => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(14px)'
    el.style.transition = `opacity 0.4s ease ${0.1 + i * 0.1}s, transform 0.4s ease ${0.1 + i * 0.1}s`
    requestAnimationFrame(() => {
      el.style.opacity = '1'
      el.style.transform = 'translateY(0)'
    })
  })

  // Stagger why cards
  const cards = document.querySelectorAll('.vp-why-card')
  cards.forEach((el, i) => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(12px)'
    el.style.transition = `opacity 0.35s ease ${0.15 + i * 0.08}s, transform 0.35s ease ${0.15 + i * 0.08}s`
    requestAnimationFrame(() => {
      el.style.opacity = '1'
      el.style.transform = 'translateY(0)'
    })
  })

  // Stagger start cards
  const starts = document.querySelectorAll('.vp-start-card')
  starts.forEach((el, i) => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(10px)'
    el.style.transition = `opacity 0.35s ease ${0.2 + i * 0.08}s, transform 0.35s ease ${0.2 + i * 0.08}s`
    requestAnimationFrame(() => {
      el.style.opacity = '1'
      el.style.transform = 'translateY(0)'
    })
  })

  // Compare rows
  const rows = document.querySelectorAll('.vp-compare-row')
  rows.forEach((el, i) => {
    el.style.opacity = '0'
    el.style.transform = 'translateX(-10px)'
    el.style.transition = `opacity 0.3s ease ${0.25 + i * 0.06}s, transform 0.3s ease ${0.25 + i * 0.06}s`
    requestAnimationFrame(() => {
      el.style.opacity = '1'
      el.style.transform = 'translateX(0)'
    })
  })

  // Arch rows
  const archRows = document.querySelectorAll('.vp-arch-row:not(.vp-arch-header)')
  archRows.forEach((el, i) => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(8px)'
    el.style.transition = `opacity 0.3s ease ${0.35 + i * 0.05}s, transform 0.3s ease ${0.35 + i * 0.05}s`
    requestAnimationFrame(() => {
      el.style.opacity = '1'
      el.style.transform = 'translateY(0)'
    })
  })

  // Proof bar
  const proofBar = document.querySelector('.vp-proof-bar')
  if (proofBar) {
    proofBar.style.opacity = '0'
    proofBar.style.transform = 'translateY(-8px)'
    proofBar.style.transition = 'opacity 0.4s ease 0.1s, transform 0.4s ease 0.1s'
    requestAnimationFrame(() => {
      proofBar.style.opacity = '1'
      proofBar.style.transform = 'translateY(0)'
    })
  }

  // Stats row
  const stats = document.querySelector('.vp-stats-row')
  if (stats) {
    stats.style.opacity = '0'
    stats.style.transform = 'translateY(10px)'
    stats.style.transition = 'opacity 0.4s ease 0.6s, transform 0.4s ease 0.6s'
    requestAnimationFrame(() => {
      stats.style.opacity = '1'
      stats.style.transform = 'translateY(0)'
    })
  }
})
</script>