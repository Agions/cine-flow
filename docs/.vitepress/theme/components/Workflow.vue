<template>
  <section class="vp-workflow-section">
    <h2 class="vp-section-title">4 步创作流程</h2>
    <div class="vp-workflow">
      <div v-for="(step, i) in steps" :key="i" class="vp-workflow-step">
        <div class="vp-step-num">{{ i + 1 }}</div>
        <div class="vp-step-body">
          <div class="vp-step-title">{{ step.title }}</div>
          <div class="vp-step-desc">{{ step.desc }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  {
    title: '上传视频',
    desc: '文件夹选择 / Ctrl 多选，自动扫描 mp4/mov/avi/webm',
  },
  {
    title: '场景理解',
    desc: 'Qwen2.5-VL 逐帧分析，提取"我"的主体视角高光片段',
  },
  {
    title: '情感选段',
    desc: '叙事完整优先 + 情感峰值驱动，悬疑铺垫 → 高潮 → 共鸣',
  },
  {
    title: '解说 + 导出',
    desc: 'DeepSeek-V4 生成文案 + Edge-TTS 配音，MP4 / 剪映草稿输出',
  },
]
</script>

<style scoped>
.vp-workflow-section {
  margin: 48px 0;
  opacity: 0;
  animation: fade-up 0.6s ease 0.3s forwards;
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

.vp-workflow {
  display: flex;
  align-items: stretch;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.vp-workflow-step {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 18px 16px;
  min-width: 180px;
  flex: 1;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.vp-workflow-step:hover {
  border-color: rgba(10,132,255,0.3);
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.vp-step-num {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: rgba(10,132,255,0.12);
  border: 1px solid rgba(10,132,255,0.25);
  color: #0A84FF;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.vp-step-title {
  font-size: 14px;
  font-weight: 700;
  color: rgba(255,255,255,0.9);
  margin-bottom: 4px;
  letter-spacing: -0.01em;
}

.vp-step-desc {
  font-size: 12px;
  color: rgba(255,255,255,0.35);
  line-height: 1.5;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
