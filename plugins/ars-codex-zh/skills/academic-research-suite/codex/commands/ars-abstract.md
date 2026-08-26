---
name: ars-abstract
description: ARS academic-paper `abstract-only` 模式——双语摘要 + 关键词
model: sonnet
---

以 `abstract-only` 模式触发 `academic-paper` skill。产出双语（zh-TW + EN）摘要与关键词。保真度谱系，中监督。经管线调用时携带 v3.6.7 `report_compiler_agent` 的 PATTERN PROTECTION 层。

模式参考：`MODE_REGISTRY.md` § academic-paper。
Skill 入口：`academic-paper/WORKFLOW.md`。
