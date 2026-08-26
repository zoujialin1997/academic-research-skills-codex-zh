---
name: ars-guide
description: ARS 新手交互式引导——不进入具体工作流，带新手一步步上手
---

以交互式引导响应新手求助（「新手教程」「怎么用」「guide」等），**不进入具体工作流**。全程遵守「固定选项点选协议」与「专业术语通俗解释」。

## 流程

1. **欢迎一行**：先给一句友好的开场，说明本插件是学术研究套件，能帮你做深度研究、写论文、论文评审、文献综述、实验规划。

2. **问目标（固定选项）**：用「固定选项点选协议」提问「你现在最想先做哪件事？」（Plan 模式弹点选卡片，否则编号列表）：
   - 深度研究（把模糊想法收敛成研究问题、做文献综述）
   - 写论文（大纲、摘要、正文起草、引用格式）
   - 论文评审（模拟审稿人、出编辑部决定信）
   - 文献综述（系统检索与综合某一主题的研究）
   - 完整管线（从研究问题一路做到修改后的稿件）
   - 只想先了解（先看教程，不马上动手）

3. **按所选场景给示例提示词**：给出**一句可直接复制**的示例提示词 + 一行说明它会触发哪个工作流（参见「工作流路由」表）。

4. **问下一步（固定选项）**：再问「要不要现在试试？」（现在试 / 换场景 / 结束）：
   - 现在试：引导用户把示例提示词发出来，并提示套件会自动路由。
   - 换场景：回到步骤 2 重新选场景。
   - 结束：收尾，推荐 `GETTING_STARTED_ZH-CN.md` 教程与 README 参考手册。

## 五场景示例提示词速查

| 场景 | 示例提示词（可直接复制） | 触发工作流 |
|---|---|---|
| 深度研究 | `Use $academic-research-suite to build a systematic review protocol for AI in higher education QA.` | `deep-research` |
| 写论文 | `Use $academic-research-suite to turn these notes into an IMRaD paper outline and drafting plan.` | `academic-paper` |
| 论文评审 | `Use $academic-research-suite to review this manuscript and produce a journal-style decision letter.` | `academic-paper-reviewer` |
| 文献综述 | `Use $academic-research-suite to help me plan a systematic literature review on AI adoption in higher education quality assurance.` | `deep-research` |
| 完整管线 | `Use $academic-research-suite to run an end-to-end research-to-paper pipeline from topic to revised manuscript.` | `academic-pipeline` |

## 约束

- 本命令只做引导，不执行具体工作流；用户一旦给出具体任务，交由「工作流路由」正常处理。
- 对专业术语（如「文献综述」「系统综述」「Socratic 收敛」）首次出现时附一句大白话解释。
- 不要求用户具备学术背景；用词平实，少堆术语。
