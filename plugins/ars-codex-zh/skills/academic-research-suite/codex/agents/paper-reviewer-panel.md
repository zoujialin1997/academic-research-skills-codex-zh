---
name: ars-paper-reviewer-panel
runtime: codex-agent-team
enabled_when: "ARS_CODEX_FULL_RUNTIME=1 and ARS_CODEX_AGENT_TEAM=1"
source_workflow: "ars/academic-paper-reviewer/WORKFLOW.md"
---

# Codex 的 ARS 论文审稿人评审团（ARS Paper Reviewer Panel）

仅在选择加入的全运行时 agent-team 模式中使用此模板。在内联模式中，读取相同源文件并在当前会话中产出相同章节。

## 源提示词

读取 `ars/academic-paper-reviewer/WORKFLOW.md`，然后派发或模拟以下角色：

1. `ars/academic-paper-reviewer/agents/field_analyst_agent.md`
2. `ars/academic-paper-reviewer/agents/eic_agent.md`
3. `ars/academic-paper-reviewer/agents/methodology_reviewer_agent.md`
4. `ars/academic-paper-reviewer/agents/domain_reviewer_agent.md`
5. `ars/academic-paper-reviewer/agents/perspective_reviewer_agent.md`
6. `ars/academic-paper-reviewer/agents/devils_advocate_reviewer_agent.md`
7. `ars/academic-paper-reviewer/agents/editorial_synthesizer_agent.md`

## 独立性契约

- 在编辑部综合之前，先产出方法论、领域、跨学科与 devil's advocate 审稿人章节。
- 在两位独立审稿人都完成各自章节之前，不得将一位独立审稿人的草稿输出暴露给另一位审稿人。
- 编辑部综合器可以看到所有已完成的审稿人章节。
- 综合必须保留少数派与异议发现，除非其按严重性与证据显式解决。
- Devil's advocate 的关切不能被多数票抹除。记录每个关切是被保留、降级还是拒绝，以及原因。
- 当完整评审团契约激活时，对结构化审稿人与综合产物运行 `ars/scripts/check_panel_synthesis.py`。

## 跨模型派发器契约

若显式启用且已同意的审稿人 owner 发出 `[CROSS-MODEL-HANDOFF v1]`，评审团派发器校验该外壳并仅传输其 payload。同意机械式填充；分歧或全返回的 DA 结果回到原 owner。格式错误的外壳或结果降级为 `unavailable`，绝不被视为普通评审。

仅在 `full` 模式中，当提供商已配置且用户同意发送稿件时，将 `domain_reviewer_agent` 作为跨模型家族的 Reviewer 2 运行。这是固定五席位评审团内的底座替换，而非增加的第六位审稿人。保留两次调用的 sprint 契约边界，不计算跨家族聚合，并填充决定信的 Review Panel Provenance 块。若派发失败或轨道未激活，使用主家族并披露回退或单家族限制。

在 `re-review` 中，仅在主判定提交后，对每个 Priority 1 路线图条目应用独立跨模型判定 pass。分歧是综合评审触发，绝非投票或自动覆盖。发出 Judge Record，当该 pass 未配置或完全不可用时，绝不省略单家族披露。

## 输出契约

`full` 模式输出必须按顺序包含以下顶级章节：

1. `Independent Reviewer: Methodology`
2. `Independent Reviewer: Domain`
3. `Independent Reviewer: Interdisciplinary`
4. `Independent Reviewer: Devil's Advocate`
5. `Editorial Synthesis`
6. `Decision Letter`
7. `Revision Roadmap`

决定信在 `full` 模式中必须包含 v3.18 Review Panel Provenance 块。

若 Codex 子 agent 不可用，声明 `agent_team_degraded: inline` 并保持相同章节顺序。
