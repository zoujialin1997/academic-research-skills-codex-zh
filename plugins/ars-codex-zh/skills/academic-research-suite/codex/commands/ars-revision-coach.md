---
name: ars-revision-coach
description: ARS academic-paper `revision-coach`——同行评审路线图或来源可核算的真实委员会回复骨架
---

以 `revision-coach` 模式触发 `academic-paper` skill。普通审稿人意见产出修改路线图（Revision Roadmap）+ 回复信骨架，不实际写修改稿。当且仅当用户明确指明真实委员会或机构评审办公室时，使用 #668 委员会通信变体：保留 UTF-8 来源，发出独立关切追踪器与占位回复骨架，并运行其确定性完整性检查器。绝不从语气推断委员会权限，也绝不在该分支上发出 priority、severity、determination 或 Schema 11。在继承的会话模型上运行——v3.7.0 的 `opus` frontmatter 下限已在 2026-06 harness pass 中退役，因此更强的会话模型永远不会被静默降级。

模式参考：`MODE_REGISTRY.md` § academic-paper。
Skill 入口：`academic-paper/WORKFLOW.md`。
