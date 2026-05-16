<template>
  <section class="vp-start-section">
    <h2 class="vp-section-title">快速开始</h2>
    <div class="vp-start-grid">
      <a v-for="card in cards" :key="card.title" :href="card.link" class="vp-start-card">
        <div class="vp-start-icon">{{ card.icon }}</div>
        <div class="vp-start-body">
          <div class="vp-start-title">{{ card.title }}</div>
          <div class="vp-start-desc">{{ card.desc }}</div>
        </div>
        <div class="vp-start-arrow">→</div>
      </a>
    </div>
  </section>
</template>

<script setup lang="ts">
const cards = [
  {
    icon: '🚀',
    title: '5 分钟快速上手',
    desc: '下载安装包 / Homebrew / 源码运行，三种方式任选',
    link: '/guide/quick-start',
  },
  {
    icon: '🔑',
    title: '配置 DeepSeek API',
    desc: '每月约 ¥7 足够，处理一个 5 分钟视频不足 1 分钱',
    link: '/guide/quick-start#配置-api-key',
  },
  {
    icon: '📖',
    title: '功能详解',
    desc: '情感风格、字幕样式、导出格式、硬件要求全解析',
    link: '/features',
  },
]
</script>

<style scoped>
.vp-start-section {
  margin: 48px 0 0;
  opacity: 0;
  animation: fade-up 0.6s ease 0.5s forwards;
}

.vp-section-title {
  font-size: 22px !important;
  font-weight: 800 !important;
  letter-spacing: -0.03em !important;
  color: var(--nf-text) !important;
  margin: 0 0 24px !important;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  background: linear-gradient(90deg, #E2E8F5 0%, #8BA3C0 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
}

.vp-start-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.vp-start-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 16px 18px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  position: relative;
}

.vp-start-card:hover {
  border-color: rgba(10,132,255,0.4);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.vp-start-icon {
  font-size: 22px;
  flex-shrink: 0;
  line-height: 1;
}

.vp-start-body {
  flex: 1;
  min-width: 0;
}

.vp-start-title {
  font-size: 14px;
  font-weight: 700;
  color: rgba(255,255,255,0.9);
  margin-bottom: 4px;
  letter-spacing: -0.01em;
}

.vp-start-desc {
  font-size: 12px;
  color: rgba(255,255,255,0.35);
  line-height: 1.4;
}

.vp-start-arrow {
  font-size: 16px;
  color: rgba(10,132,255,0.6);
  flex-shrink: 0;
  transition: transform 0.2s, color 0.2s;
}

.vp-start-card:hover .vp-start-arrow {
  transform: translateX(4px);
  color: #0A84FF;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
