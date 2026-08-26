---
name: ars-disclosure
description: ARS academic-paper `disclosure` 模式——期刊适用性/状态包或政策锚点渲染
model: sonnet
---

以独立 `disclosure` 模式触发 `academic-paper` skill。Agent 9 在渲染前必须加载 `academic-paper/references/disclosure_mode_protocol.md`；通用格式化器 disclosure 不能作为回退。默认期刊路径返回 `REQUIRED`、`ACTION_ONLY`、`NOT_REQUIRED` 或 `UNKNOWN` 适用性，并在需要时给出显式的带类型 halt 状态（支持 15 个政策目标：ICLR / NeurIPS / Nature / Science / ACL / EMNLP，以及医学出版目标——ICMJE / NEJM / The Lancet / JAMA / BMJ / PLOS / Frontiers / 出版社级 中华护理杂志社 / 期刊级 国际眼科杂志）。`--policy-anchor` 路径使用其独立的锚点特定渲染器。保真度谱系，低监督。

模式参考：`MODE_REGISTRY.md` § academic-paper。
Skill 入口：`academic-paper/WORKFLOW.md`。
