<template>
  <section class="vp-stack-section">
    <h2 class="vp-section-title">技术栈</h2>
    <div class="vp-stack-table">
      <div class="vp-stack-header">
        <div>模块</div>
        <div>模型 / 技术</div>
        <div>说明</div>
      </div>
      <div v-for="row in rows" :key="row.module" class="vp-stack-row">
        <div>
          <span :class="['vp-badge', `vp-badge--${row.color}`]">{{ row.module }}</span>
        </div>
        <div v-html="row.tech" />
        <div>{{ row.note }}</div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const rows = [
  { module: '分组', color: 'blue', tech: '<code>Qwen2.5-VL</code> + 声纹', note: '视觉 0.7 + 音频 0.3 混合相似度' },
  { module: '提取', color: 'blue', tech: '<code>Qwen2.5-VL</code>', note: '逐帧分析，主体视角判断，9–60 秒片段' },
  { module: '情感', color: 'purple', tech: '视觉 + 音频双维度', note: '画面信息密度 + 语调变化，综合评分排序' },
  { module: '解说', color: 'green', tech: '<code>DeepSeek-V4</code>', note: '代入"我"视角，7 种预设风格 + 角色设定' },
  { module: '配音', color: 'amber', tech: '<code>Edge-TTS</code> · <code>F5-TTS</code>', note: 'Edge 主流低延迟，F5 零样本音色克隆' },
  { module: '导出', color: 'red', tech: '<code>MP4</code> · <code>剪映草稿</code>', note: '合并版 + 高光片段双输出' },
]
</script>

<style scoped>
.vp-stack-section {
  margin: 48px 0;
  opacity: 0;
  animation: fade-up 0.6s ease 0.45s forwards;
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

.vp-stack-table {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  overflow: hidden;
}

.vp-stack-header,
.vp-stack-row {
  display: grid;
  grid-template-columns: 120px 1.5fr 2fr;
  padding: 11px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 13px;
  align-items: center;
  transition: background 0.15s;
}

.vp-stack-header {
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.3);
}

.vp-stack-row:last-child { border-bottom: none; }
.vp-stack-row:hover { background: rgba(255,255,255,0.02); }

.vp-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 700;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
}

.vp-badge--blue   { background: rgba(10,132,255,0.12); color: #0A84FF; border: 1px solid rgba(10,132,255,0.2); }
.vp-badge--purple { background: rgba(139,92,246,0.12); color: #8B5CF6; border: 1px solid rgba(139,92,246,0.2); }
.vp-badge--green  { background: rgba(16,185,129,0.12); color: #10B981; border: 1px solid rgba(16,185,129,0.2); }
.vp-badge--amber  { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.2); }
.vp-badge--red    { background: rgba(239,68,68,0.12); color: #EF4444; border: 1px solid rgba(239,68,68,0.2); }

:deep(code) {
  background: rgba(255,255,255,0.06);
  border-radius: 4px;
  padding: 1px 6px;
  font-size: 12px;
  font-family: 'SF Mono', 'Cascadia Code', monospace;
}

:deep(div:last-child) {
  color: rgba(255,255,255,0.35);
  font-size: 12px;
  line-height: 1.5;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
