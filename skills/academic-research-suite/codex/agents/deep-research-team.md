---
name: ars-deep-research-team
runtime: codex-agent-team
enabled_when: "ARS_CODEX_FULL_RUNTIME=1 and ARS_CODEX_AGENT_TEAM=1"
source_workflow: "ars/deep-research/WORKFLOW.md"
---

# Codex 的 ARS 深度研究团队（ARS Deep Research Team）

当显式启用全运行时 agent-team 模式时，用于 `deep-research` 模式。否则从相同源提示词内联执行各角色。

## 派发形态

- `socratic` 模式以 `socratic_mentor_agent.md` 与 `research_question_agent.md` 开始；在研究问题精确之前，不得产出大纲或草稿。
- `lit-review` 与 `systematic-review` 模式以 `bibliography_agent.md`、`source_verification_agent.md` 与 `synthesis_agent.md` 开始。
- `fact-check` 模式以 `source_verification_agent.md` 开始，并保持已验证 / 未验证 / 矛盾声明分离。
- `full` 模式在 RQ 简报稳定后可并行化文献、来源验证、偏倚风险、伦理与 devil's advocate 工作。
- 若显式启用且已同意的 design-freeze owner 发出 `[CROSS-MODEL-HANDOFF v1]`，团队派发器用 `ars/scripts/cross_model_handoff.py` 校验它，仅发送 payload，并将分歧结果返回原 owner 判断。格式错误的交接或结果降级为 `unavailable`。

## 输出契约

每个 agent 工作产物必须标注证据、推断与建议。当前事实与引文需要对权威来源验证，或显式标记为未验证。
