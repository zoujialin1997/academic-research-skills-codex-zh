---
name: ars-reviewer
description: ARS academic-paper-reviewer `full` 模式——模拟同行评审小组
---

以 `full` 模式触发 `academic-paper-reviewer` skill。当存在明确的替代模式时遵循之：`quick`、`methodology-focus`、`re-review`、`guided` 或 `calibration`。在继承的会话模型上运行——v3.7.0 的 `opus` frontmatter 下限已在 2026-06 harness pass 中退役，因此更强的会话模型永远不会被静默降级。

模式参考：`MODE_REGISTRY.md` § academic-paper-reviewer。
Skill 入口：`academic-paper-reviewer/WORKFLOW.md`。
