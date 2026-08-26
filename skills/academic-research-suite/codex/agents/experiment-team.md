---
name: ars-experiment-team
runtime: codex-agent-team
enabled_when: "ARS_CODEX_FULL_RUNTIME=1 and ARS_CODEX_AGENT_TEAM=1"
source_workflow: "ars/experiment-agent/WORKFLOW.md"
---

# Codex 的 ARS 实验团队（ARS Experiment Team）

当用户明确选择加入全运行时 agent-team 模式时，用于实验规划、研究方案支持、可复现性规划与统计解读。

## 源提示词

- `ars/experiment-agent/agents/study_manager_agent.md`
- `ars/experiment-agent/agents/code_runner_agent.md`

## 输出契约

分离设计假设、可运行的分析计划、伦理/IRB 约束与可复现性检查。未经用户明确批准与本地安全审查，不得执行高风险代码或人类受试工作流。
