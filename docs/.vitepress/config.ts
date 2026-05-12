import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Voxplore',
  description: 'AI 驱动的第一人称视频解说工具 — 上传视频，AI 代入主角视角，一键生成电影感配音解说。Qwen2.5-VL + DeepSeek-V4 + Edge-TTS。',
  base: '/Voxplore/',
  lang: 'zh-CN',
  cleanUrls: false,
  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/Voxplore/favicon.svg' }],
    ['meta', { name: 'keywords', content: 'AI视频解说,第一人称视频,自动配音,AI字幕,视频剪辑,Voxplore,DeepSeek,Qwen,Edge-TTS' }],
    ['meta', { name: 'author', content: 'Agions' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Voxplore — AI First-Person Video Narrator' }],
    ['meta', { property: 'og:description', content: '上传视频，AI 代入主角视角，一键生成电影感配音解说' }],
    ['meta', { property: 'og:url', content: 'https://agions.github.io/Voxplore/' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'twitter:title', content: 'Voxplore — AI First-Person Video Narrator' }],
    ['meta', { name: 'twitter:description', content: '上传视频，AI 代入主角视角，一键生成电影感配音解说' }],
    ['meta', { name: 'theme-color', content: '#070B12' }],
  ],

  markdown: { lineNumbers: false },

  themeConfig: {
    siteTitle: 'Voxplore',
    appearance: 'dark',

    nav: [
      { text: '首页', link: '/' },
      { text: '功能介绍', link: '/features' },
      { text: '快速开始', items: [
          { text: '5 分钟上手', link: '/guide/quick-start' },
          { text: '完整安装指南', link: '/guide/installation' },
          { text: 'AI 配置', link: '/guide/ai-configuration' },
      ]},
      { text: '教程', items: [
          { text: 'AI 工作流详解', link: '/guide/ai-video-guide' },
          { text: '导出格式', link: '/guide/exporting' },
          { text: '界面介绍', link: '/guide/interface' },
      ]},
      { text: '参考', items: [
          { text: 'AI 模型', link: '/ai-models' },
          { text: '模型更新', link: '/model-updates' },
          { text: '疑难排查', link: '/guide/troubleshooting' },
          { text: '架构概览', link: '/architecture' },
      ]},
      { text: '更多', items: [
          { text: '安全设计', link: '/security' },
          { text: '贡献指南', link: '/contributing' },
          { text: 'FAQ', link: '/faq' },
      ]},
      { text: 'GitHub', link: 'https://github.com/Agions/Voxplore' },
    ],

    sidebar: {
      '/guide/': [
        { text: '快速入门', items: [
            { text: '5 分钟快速开始', link: '/guide/quick-start' },
            { text: '完整安装指南', link: '/guide/installation' },
            { text: '界面介绍', link: '/guide/interface' },
        ]},
        { text: '核心教程', items: [
            { text: 'AI 工作流详解', link: '/guide/ai-video-guide' },
            { text: 'AI 配置指南', link: '/guide/ai-configuration' },
            { text: '导出格式', link: '/guide/exporting' },
        ]},
        { text: '疑难解答', items: [
            { text: '常见问题 FAQ', link: '/faq' },
            { text: '疑难排查', link: '/guide/troubleshooting' },
        ]},
      ],
      '/': [
        { text: '入门', items: [
            { text: '首页', link: '/' },
            { text: '快速开始', link: '/guide/quick-start' },
            { text: '功能介绍', link: '/features' },
        ]},
        { text: '快速开始', items: [
            { text: '5 分钟上手', link: '/guide/quick-start' },
            { text: '完整安装', link: '/guide/installation' },
            { text: '界面介绍', link: '/guide/interface' },
        ]},
        { text: 'AI 工作流', items: [
            { text: '工作流详解', link: '/guide/ai-video-guide' },
            { text: 'AI 模型配置', link: '/guide/ai-configuration' },
            { text: '导出格式', link: '/guide/exporting' },
        ]},
        { text: '参考', items: [
            { text: 'AI 模型', link: '/ai-models' },
            { text: '模型更新', link: '/model-updates' },
            { text: '架构概览', link: '/architecture' },
            { text: '安全设计', link: '/security' },
        ]},
        { text: '社区', items: [
            { text: '常见问题', link: '/faq' },
            { text: '贡献指南', link: '/contributing' },
            { text: '疑难排查', link: '/guide/troubleshooting' },
        ]},
      ],
    },

    editLink: {
      pattern: 'https://github.com/Agions/Voxplore/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页面',
    },

    lastUpdated: {
      text: '最后更新',
      formatOptions: { dateStyle: 'short', timeStyle: 'short' },
    },

    search: {
      provider: 'local',
      options: {
        placeholder: '搜索文档...',
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索文档' },
        },
      },
    },

    returnToTopLabel: '返回顶部',
    sidebarMenuLabel: '菜单',
    docFooter: { prev: '上一篇', next: '下一篇' },
    outline: { level: [2, 3], label: '目录' },
    socialLinks: [{ icon: 'github', link: 'https://github.com/Agions/Voxplore' }],
    footer: {
      message: 'MIT License · Copyright © 2025-2026 Agions',
      copyright: 'Voxplore — AI First-Person Video Narrator · 开源免费 · 隐私优先',
    },
  },
})
