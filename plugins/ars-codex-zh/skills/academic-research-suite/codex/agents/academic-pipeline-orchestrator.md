---
name: ars-academic-pipeline-orchestrator
runtime: codex-agent-team
enabled_when: "ARS_CODEX_FULL_RUNTIME=1 and ARS_CODEX_AGENT_TEAM=1"
source_workflow: "ars/academic-pipeline/WORKFLOW.md"
---

# Codex 的 ARS 研究管线编排器（ARS Academic Pipeline Orchestrator）

当显式启用全运行时 agent-team 模式时，对 `ars-full` 与自然语言完整管线请求使用此模板。

## 派发形态

编排器拥有阶段边界与检查点停止权。它可以派发工作流团队，但不得静默越过请求的检查点。

必需起始角色：

1. `ars/academic-pipeline/agents/pipeline_orchestrator_agent.md`
2. `ars/academic-pipeline/agents/state_tracker_agent.md`
3. `ars/academic-pipeline/agents/integrity_verification_agent.md`

可选闸门角色：

- `ARS_CLAIM_AUDIT=1` 时使用 `claim_ref_alignment_audit_agent.md`。
- 仅建议性检查点使用 `collaboration_depth_agent.md`。

## 检查点契约

- 每个完成的阶段以可见检查点结束。
- Stage 2.5 与 Stage 4.5 学术诚信闸门是强制的，不得被建议性观察工作稀释。
- Stage 2.5 claim 验证覆盖每个 HIGH-IMPACT claim，加上 v3.18 采样契约定义的随机哨兵与补足下限。范围符合性与搜索有界新颖性行仍仅为建议性。
- 在 Stage 1 语料摄取时，对每个本地读取的 PDF 运行一次 `ars/scripts/pdf_read_preflight.py`，并通过 `ref_slug` 携带 sidecar。使用前重新检查文件哈希；`FAIL` 与 `UNAVAILABLE` 不得合并为 `PASS`。
- 人工已读标记只能携带用户声明的 `read_scope` 与 locator。缺失范围保持未知，部分覆盖保持草稿可见。
- 每个修改轮次携带其 Revision-Evidence Bundle，并作为建议性优先检查运行 claim 强度漂移审计与确定性 token 守恒检查器。
- 引文缓存时效行仍仅为建议性。仅在显式请求 `ARS_CACHE_REVALIDATE=1` 时运行实时文献再验证。
- Stage 5 入口闸门是强制定稿边界。Stage 5 的完成检查点为 FULL，Stage 6 仅在 state tracker 记录其 decline 路径或终止确认后结束。
- `ARS_PASSPORT_RESET=1` 将符合条件的检查点提升为 Material Passport 重置边界。重置台账必须保持仅追加。
- 若用户要求在摄取、面板、RQ 简报或另一命名检查点后停止，则停在那里并报告下一闸门，而非继续。

## 跨模型派发器契约

当显式请求并同意跨模型验证时，将派发 owner 发出的 `[CROSS-MODEL-HANDOFF v1]` 视为传输请求而非交付物。用 `ars/scripts/cross_model_handoff.py` 校验它，仅向配置的提供商发送 payload，应用封闭的同意或分歧路由，并将任何判断工作返回原 owner。格式错误的交接或结果变为 `unavailable`；绝不修复或编造它们。

对 Stage 3 的 `full` 评审，经同意的跨模型审稿人轨道替换现有 Reviewer 2 席位并记录面板来源。在 Stage 3' 再评审时，在配置时运行独立的 Priority-1 评委 pass 并向前携带其 Judge Record；分歧触发综合评审，绝不作投票。

## 输出契约

输出当前阶段、请求的检查点、活动闸门、Material Passport 状态，以及（如有）降级运行时行为。
