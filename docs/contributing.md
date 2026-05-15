---
title: 贡献指南
description: 如何参与 NarrateFlow 的开发和贡献。
---

# 贡献指南

## 开发环境

```bash
git clone https://github.com/Agions/NarrateFlow.git
cd NarrateFlow
pip install -r requirements.txt
python app/main.py
```

## 分支管理

- `main` — 稳定版本
- `refactor/*` — 重构与优化
- `feature/*` — 新功能开发

## 代码规范

- Python：遵循 PEP 8
- 提交信息：使用中文描述改动内容
- 测试：修改后运行 `pytest tests/` 验证

## Pull Request

1. Fork 本仓库
2. 创建功能分支
3. 编写测试用例
4. 提交并推送
5. 提交 Pull Request

## 问题反馈

- 缺陷请提交 [GitHub Issues](https://github.com/Agions/NarrateFlow/issues)
- 功能建议欢迎提交 Discussion
