<template>
  <section class="vp-compare-section">
    <h2 class="vp-section-title">vs 传统视频解说</h2>
    <div class="vp-compare-grid">
      <div class="vp-compare-header">
        <div class="vp-compare-col-label" />
        <div class="vp-compare-col-old">传统方式</div>
        <div class="vp-compare-col-new">Voxplore</div>
      </div>
      <div v-for="row in rows" :key="row.label" class="vp-compare-row">
        <div class="vp-compare-col-label">{{ row.label }}</div>
        <div class="vp-compare-col-old">{{ row.old }}</div>
        <div class="vp-compare-col-new">{{ row.new }}</div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const rows = [
  { label: '制作时间', old: '30–120 分钟', new: '3–10 分钟' },
  { label: '配音成本', old: '¥50–500/分钟', new: '< ¥0.01/视频' },
  { label: '技术门槛', old: '专业剪辑 + 配音', new: '上传视频，一键完成' },
  { label: '隐私安全', old: '上传第三方平台', new: '视频永不上传云端' },
  { label: '字幕同步', old: '手动对齐，耗时费眼', new: 'TTS word-level，50ms 精度' },
  { label: '导出格式', old: '仅 MP4', new: 'MP4 + 剪映草稿 JSON' },
]
</script>

<style scoped>
.vp-compare-section {
  margin: 56px 0 48px;
  opacity: 0;
  animation: fade-up 0.6s ease 0.15s forwards;
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

.vp-compare-grid {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  overflow: hidden;
}

.vp-compare-header,
.vp-compare-row {
  display: grid;
  grid-template-columns: 1.5fr 2fr 2fr;
}

.vp-compare-header {
  background: rgba(255,255,255,0.03);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.3);
}

.vp-compare-header > div {
  padding: 10px 20px;
}

.vp-compare-col-label { padding: 12px 20px; }
.vp-compare-col-old   { padding: 12px 20px; }
.vp-compare-col-new   { padding: 12px 20px; }

.vp-compare-row {
  border-top: 1px solid rgba(255,255,255,0.05);
  transition: background 0.15s;
}

.vp-compare-row:hover {
  background: rgba(255,255,255,0.02);
}

.vp-compare-col-label {
  font-size: 13px;
  color: rgba(255,255,255,0.45);
  font-weight: 500;
}

.vp-compare-col-old {
  font-size: 13px;
  color: rgba(255,255,255,0.25);
  text-decoration: line-through;
  opacity: 0.7;
}

.vp-compare-col-new {
  font-size: 13px;
  font-weight: 600;
  color: #10B981;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .vp-compare-header,
  .vp-compare-row {
    grid-template-columns: 1fr 1fr;
  }
  .vp-compare-col-label { display: none; }
}
</style>
