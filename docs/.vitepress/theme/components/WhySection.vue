<template>
  <section class="vp-why-section">
    <h2 class="vp-section-title">为什么选择 Voxplore</h2>
    <div class="vp-why-grid">
      <div v-for="card in cards" :key="card.icon" class="vp-why-card">
        <div class="vp-why-icon">{{ card.icon }}</div>
        <div class="vp-why-body">
          <h3>{{ card.title }}</h3>
          <p v-html="card.desc" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const cards = [
  {
    icon: '⚡',
    title: '3 分钟完成解说',
    desc: '从上传视频到导出成品，全流程自动化。AI 自动分析、自动写稿、自动配音，无需手动剪辑。',
  },
  {
    icon: '💰',
    title: '不到一分钱一个视频',
    desc: 'DeepSeek-V4 成本约 $0.1 / 1M tokens。处理一个 5 分钟视频成本不足 <strong>1 分钱</strong>。',
  },
  {
    icon: '🔒',
    title: '视频永不上传云端',
    desc: '全部处理在本地完成。FFmpeg 本地合成，API 仅传输文字（解说稿），你的视频永远留在本机。',
  },
  {
    icon: '🎭',
    title: '7 种情感风格',
    desc: '治愈 · 悬疑 · 励志 · 怀旧 · 浪漫 · 幽默 · 纪录片。AI 根据视频内容自动匹配最合适的解说语气。',
  },
]
</script>

<style scoped>
.vp-why-section {
  margin: 48px 0;
  opacity: 0;
  animation: fade-up 0.6s ease 0.35s forwards;
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

.vp-why-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.vp-why-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 20px;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}

.vp-why-card:hover {
  border-color: rgba(10,132,255,0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.vp-why-icon {
  font-size: 24px;
  flex-shrink: 0;
  line-height: 1;
  margin-top: 2px;
}

.vp-why-body h3 {
  font-size: 14px;
  font-weight: 700;
  color: rgba(255,255,255,0.9);
  margin: 0 0 8px;
  letter-spacing: -0.01em;
}

.vp-why-body p {
  font-size: 12px;
  color: rgba(255,255,255,0.4);
  line-height: 1.65;
  margin: 0;
}

.vp-why-body :deep(strong) {
  color: #0A84FF;
  font-weight: 700;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
