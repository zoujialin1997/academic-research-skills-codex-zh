---
name: ars-academic-paper-team
runtime: codex-agent-team
enabled_when: "ARS_CODEX_FULL_RUNTIME=1 and ARS_CODEX_AGENT_TEAM=1"
source_workflow: "ars/academic-paper/WORKFLOW.md"
---

# Codex 的 ARS 学术论文团队（ARS Academic Paper Team）

用于选择加入全运行时 agent-team 模式下的 `academic-paper` 模式。内联模式仍为默认回退。

## 派发形态

- `plan` 模式使用 `socratic_mentor_agent.md`、`intake_agent.md` 与 `structure_architect_agent.md`；产出计划与缺失证据映射，而非完整草稿。
- `outline-only` 使用 `structure_architect_agent.md` 与 `argument_builder_agent.md`。
- `full` 模式保留上游的生成器/评估器契约：`draft_writer_agent.md` 必须先提交起草计划再进行自评，`peer_reviewer_agent.md` 必须在草稿可见之后评估。
- `citation-check` 使用 `citation_compliance_agent.md`，必须分离缺失、不匹配、不可验证与仅格式类的引文问题。
- `format-convert` 使用 `formatter_agent.md`；当上游启用了 claim audit 模式时，未解决的高警告 claim 审计注释仍为阻塞项。

## 输出契约

保留 Material Passport 字段、引文 locator、claim 审计注释与 venue 披露要求。不要从模型记忆中添加不受支持的声明；显式标记材料缺口。
