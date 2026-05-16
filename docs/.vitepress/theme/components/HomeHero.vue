<template>
  <section class="vp-home-hero">
    <!-- Ambient Glow -->
    <div class="vp-glow-bg" />

    <!-- Floating Tags -->
    <div class="vp-float-tags">
      <div class="vp-tag vp-tag--green">
        <span class="vp-tag-dot" />v1.0.1 最新
      </div>
      <div class="vp-tag vp-tag--blue">
        <span class="vp-tag-dot" />DeepSeek-V4 解说
      </div>
      <div class="vp-tag vp-tag--purple">
        <span class="vp-tag-dot" />SenseVoice ASR
      </div>
      <div class="vp-tag vp-tag--amber">
        <span class="vp-tag-dot" />&lt;¥0.01 / 视频
      </div>
      <div class="vp-tag vp-tag--red">
        <span class="vp-tag-dot" />MIT 开源
      </div>
    </div>

    <!-- Hero Text -->
    <div class="vp-hero-text">
      <div class="vp-hero-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="#F59E0B"/></svg>
        AI First-Person Video Narrator
      </div>
      <h1 class="vp-hero-title">
        <span class="vp-gradient-text">Voxplore</span>
      </h1>
      <p class="vp-hero-tagline">批量上传视频 · AI 自动分组选段 · 一键生成电影感配音解说</p>
      <p class="vp-hero-sub">从上传到成品，3 分钟完成。视频永不上传云端，成本不足一分钱。</p>
    </div>

    <!-- CTA Buttons -->
    <div class="vp-hero-cta">
      <a href="/guide/quick-start" class="vp-btn vp-btn--primary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M13 7L18 12L13 17M6 12H18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        快速开始
      </a>
      <a href="/features" class="vp-btn vp-btn--secondary">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        功能详解
      </a>
      <a href="https://github.com/Agions/Voxplore" class="vp-btn vp-btn--ghost" target="_blank">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
        GitHub
      </a>
    </div>
  </section>
</template>

<style scoped>
.vp-home-hero {
  position: relative;
  text-align: center;
  padding: 80px 24px 64px;
  max-width: 900px;
  margin: 0 auto;
  overflow: hidden;
}

.vp-glow-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 50% at 50% -10%, rgba(10, 132, 255, 0.12) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 30% 60%, rgba(139, 92, 246, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse 50% 40% at 70% 70%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
  pointer-events: none;
  animation: glow-pulse 8s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.7; transform: scale(1); }
  50%       { opacity: 1;   transform: scale(1.05); }
}

/* Tags */
.vp-float-tags {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 36px;
  animation: fade-up 0.5s ease both;
}

.vp-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.03em;
  font-family: 'SF Mono', 'Cascadia Code', 'JetBrains Mono', monospace;
  backdrop-filter: blur(8px);
  border: 1px solid transparent;
}

.vp-tag-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
  animation: pulse-dot 2s ease-in-out infinite;
}

.vp-tag--green  { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.25); color: #10B981; }
.vp-tag--blue   { background: rgba(10,132,255,0.1);  border-color: rgba(10,132,255,0.25);  color: #0A84FF; }
.vp-tag--purple { background: rgba(139,92,246,0.1);  border-color: rgba(139,92,246,0.25);  color: #8B5CF6; }
.vp-tag--amber  { background: rgba(245,158,11,0.1);  border-color: rgba(245,158,11,0.25);  color: #F59E0B; }
.vp-tag--red    { background: rgba(239,68,68,0.1);   border-color: rgba(239,68,68,0.25);   color: #EF4444; }

.vp-tag--green  .vp-tag-dot { background: #10B981; box-shadow: 0 0 6px rgba(16,185,129,0.6); }
.vp-tag--blue   .vp-tag-dot { background: #0A84FF; box-shadow: 0 0 6px rgba(10,132,255,0.6); }
.vp-tag--purple .vp-tag-dot { background: #8B5CF6; box-shadow: 0 0 6px rgba(139,92,246,0.6); }
.vp-tag--amber  .vp-tag-dot { background: #F59E0B; box-shadow: 0 0 6px rgba(245,158,11,0.6); }
.vp-tag--red    .vp-tag-dot { background: #EF4444; box-shadow: 0 0 6px rgba(239,68,68,0.6); }

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.8); }
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Hero Text */
.vp-hero-text {
  position: relative;
  z-index: 1;
  margin-bottom: 36px;
  animation: fade-up 0.6s ease 0.1s both;
}

.vp-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  background: rgba(245,158,11,0.08);
  border: 1px solid rgba(245,158,11,0.25);
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  color: #F59E0B;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 20px;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
}

.vp-hero-title {
  font-size: clamp(3rem, 8vw, 5.5rem) !important;
  font-weight: 900 !important;
  letter-spacing: -0.04em !important;
  line-height: 1.05 !important;
  margin: 0 0 16px !important;
}

.vp-gradient-text {
  background: linear-gradient(135deg, #0A84FF 0%, #8B5CF6 40%, #10B981 70%, #0A84FF 100%);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-shift 6s ease-in-out infinite;
}

@keyframes gradient-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.vp-hero-tagline {
  font-size: clamp(1rem, 2.5vw, 1.2rem) !important;
  font-weight: 600 !important;
  color: rgba(255,255,255,0.7) !important;
  letter-spacing: 0.04em;
  margin: 0 0 12px !important;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
}

.vp-hero-sub {
  font-size: clamp(0.9rem, 2vw, 1rem);
  color: rgba(255,255,255,0.4);
  margin: 0;
  line-height: 1.6;
}

/* CTA */
.vp-hero-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
  animation: fade-up 0.6s ease 0.2s both;
}

.vp-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  white-space: nowrap;
  border: 1px solid transparent;
  position: relative;
  overflow: hidden;
}

.vp-btn::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%   { left: -100%; }
  50%, 100% { left: 150%; }
}

.vp-btn--primary {
  background: #0A84FF;
  color: white;
  box-shadow: 0 4px 16px rgba(10,132,255,0.35), inset 0 1px 0 rgba(255,255,255,0.1);
}

.vp-btn--primary:hover {
  background: #2196FF;
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(10,132,255,0.5), inset 0 1px 0 rgba(255,255,255,0.15);
}

.vp-btn--secondary {
  background: rgba(255,255,255,0.04);
  color: rgba(255,255,255,0.8);
  border-color: rgba(255,255,255,0.1);
}

.vp-btn--secondary:hover {
  background: rgba(255,255,255,0.08);
  border-color: rgba(255,255,255,0.2);
  transform: translateY(-1px);
}

.vp-btn--ghost {
  background: transparent;
  color: rgba(255,255,255,0.4);
  border-color: rgba(255,255,255,0.08);
}

.vp-btn--ghost:hover {
  background: rgba(255,255,255,0.04);
  color: rgba(255,255,255,0.7);
  border-color: rgba(255,255,255,0.15);
}
</style>
