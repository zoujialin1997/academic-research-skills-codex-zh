---
name: ars-rebuttal-audit
description: ARS academic-paper `rebuttal-audit` 模式——对照审稿意见 QA 既有回复草稿
model: sonnet
---

以 `rebuttal-audit` 模式触发 `academic-paper` skill。评估**同时**需要审稿人意见**和**既有的回复/回应草稿。产出建议性 QA 报告（逐条意见覆盖 + 空白 + 风险标记）。**不**生成新的回复，也**不**发出 Schema 11 / Material Passport / 已验证状态（独立调用在管线之外运行）。保真度谱系，低监督。

如果只有审稿人意见（尚无草稿），请改用 `revision-coach`。

模式参考：`MODE_REGISTRY.md` § academic-paper。
Skill 入口：`academic-paper/WORKFLOW.md`。
