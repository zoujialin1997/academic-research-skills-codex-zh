# ARS-Codex 全运行时适配器

本目录是 `academic-research-suite` 的 Codex 专属运行时适配器。vendored 的上游内容仍位于 `ars/` 下；除通过显式上游同步或文档化路径补丁外，不要手工编辑它。

## 运行时 Profile

默认行为保持内联：

```text
Use $academic-research-suite: ars-plan ...
```

根路由器读取相关的 `ars/*/WORKFLOW.md` 与 agent 提示文件，然后在当前 Codex 会话中执行该阶段。

全运行时行为为选择加入：

```bash
export ARS_CODEX_FULL_RUNTIME=1
export ARS_CODEX_AGENT_TEAM=1
export ARS_CODEX_HOOKS=1
```

- `ARS_CODEX_FULL_RUNTIME=1` 通过 `codex/scripts/ars_codex_full_runtime.py` 启用结构化命令路由与闸门规划。
- `ARS_CODEX_AGENT_TEAM=1` 允许使用 `codex/agents/` 下的模板进行 planner 驱动的 Codex agent-team 派发。
- `ARS_CODEX_HOOKS=1` 允许手动安装默认禁用的 `codex/hooks/` hook 包。

若某个标志缺失，适配器降级为内联角色提示执行，并必须报告该降级行为。

拓扑实验除了 agent-team 标志外还需要单独的双重选择加入：

```bash
export ARS_CODEX_TOPOLOGY_EXPERIMENT=1
export ARS_CODEX_TOPOLOGY_ARM=reviewer-five-panel
```

已注册的 arm 为 `inline-solo`、`reviewer-two-plus-synthesis`、`reviewer-five-panel`、`reviewer-full-seven` 与 `workflow-current`。单独的 arm 变量会被忽略。未知或对工作流不适用的 arm 失败关闭。任何实验都不改变内联默认，也不写入路由状态。

## 主要文件

- `full-runtime-manifest.json` 是适配器契约：命令别名、工作流映射、agent-team 规则、质量门、hook 包与已知退化。
- `scripts/ars_codex_full_runtime.py` 将请求转为确定性 JSON 计划。它是只读的，可安全在测试中运行。
- `scripts/ars_codex_quality_gates.py` 验证适配器打包、hook 安全、审稿人独立性夹具与上游锁定来源。
- `agents/*.md` 是 Codex 子 agent 模板。它们指向 vendored 的 ARS 源提示词，而非复制上游提示词正文。
- `commands/*.md` 是 `ars/commands/` 的中文覆盖提示配方；解析器优先读取此处，缺失时回退上游英文原版。
- `compatibility-matrix.md` 记录 Claude Code 对齐度、剩余差距与验证方法。
- `topology-experiment/` 包含冻结的 issue #37 队列、clean-room 外壳、每次运行资源回执、held-out 裁定与本地 go/no-go 报告。

## Agent-Team 语义

适配器不能承诺与 Claude Code Agent Team 逐字节一致。相反，它提供显式的 Codex 编排契约：

- 审稿人评审团在综合前产出独立审稿人章节；
- 除非被证据与严重性解决，综合保留少数派与异议发现；
- 管线编排在请求的检查点停止；
- 重型 `ars-full`、`ars-reviewer` 与 `ars-revision-coach` 路由继承活动会话模型，因为 v3.21.1 未给它们模型 frontmatter；轻路由 `sonnet` 提示仍是上游元数据，不强制 Codex 模型；
- ARS v3.21.1 将模型分层保留为建议性元数据；仅当 Codex 运行时提供显式按派发模型选择时应用它；
- 规范跨模型交接由派发上下文验证与传输，而非由最小权限 owner 角色；
- 固定 Reviewer 2 底座替换与 Priority-1 再评审评委 pass 仅在显式提供商配置与内容同意后运行；
- `ARS_CROSS_MODEL_TRANSPORT=codex` 仅为一个引用的 Stage 2.5 / 4.5 引文检查显式选择受限的 ChatGPT 订阅传输；它需要 Codex CLI 0.147.0 或更新、`ARS_CROSS_MODEL`、stdout 或 stderr 上的精确 `Logged in using ChatGPT` 认证，以及提供商/内容/成本同意。提供商模式省略不受支持的 `uniqueItems`，而本地重复拒绝保持失败关闭；`code_mode` 仍禁用，但独立搜索所需的有界 host 在封闭事件语法下仍可用。它不接受调用方编写的提示或路径，也没有自动 API 回退或 reviewer/DA/校准/再评审/交接范围；
- 受限引文传输将 `turn/completed` 视为临时的，仅在接受前完成干净进程退出并到达 stdout/stderr EOF；迟到的禁止或格式错误事件与 drain 失败仍是可见失败；
- 引文缓存时效仍仅为建议性，而实时再验证为选择加入并在路由计划中呈现；
- 本地 PDF 在信任页面 anchor 之前使用结构读取完整性 preflight；v3.20 `--classify-content` 扩展为选择加入、进程隔离、单独钉定且仅建议性，`STRUCTURE_ONLY` 判定范围，无自动 OCR/anchor 闸门；
- 人工已读自证仍归用户所有；每个新标记都要求显式 `read_scope`，部分覆盖状态保持可见；
- 修改轮次保留 claim 强度阶梯与确定性 token 守恒建议性检查；
- Phase E 证据行保持来源绑定并保留现有判定；非排名路线图需要单独显式作者裁定 sidecar，而可选跨运行裁定活动为本地且仅建议性；
- 评审目标上下文由作者确认，标准指针在形成性、内部与外部评审中保持一致，不影响完整性判定、编辑部算术、检查点或作者分诊。随附的 MSR 2027/SIGSOFT 证明集演示一条精确 profile 来源绑定路径，而非 venue 或学科覆盖；
- 人类受试者权限保持评审伦理与数据保护两轴分离，未决状态可见；输出绝不模拟 IRB/REC、法律裁定、机构授权或就绪决定；
- 文献/撤稿与预注册一致性载体保留来源、时效、分歧与退化，而不会成为干净文档证书、协议副本或同意记录；
- 研究工作流 profile 底座保持默认关闭且确定性：显式选择或可见 `field_general` 回退被记录，不推断或添加 planner/管线 hook，行为证据保持 `NOT_RUN`；
- `ARS_INQUIRY_LEDGER=1` 仅启用本地选择加入的分支台账 alpha；适配器绝不自动设置它，作者事件、有界摘要、过期原因、路径锁与恢复回执不产生网络权限或结果声明；
- v3.21.1 数据流、控制可用性、阶段能力、风险与治理透明度表面与其确定性验证器一起保持可用，而不会变成有效性或认证声明；
- v3.21.1 sealed promotion-bakeoff 契约与封闭测试可用，但直接 `verify-tree` 仍仅上游可用，因为此重新定根快照缺少完整的规范上游 Git 历史；
- 评审团、21 行退化注册表、工具白名单与管线边界验证器仍作为 vendored 质量门可用；
- 上游 v3.18 SessionStart 更新提醒被 vendored 但不由 Codex hook 包执行；
- 内联模式保持可用且为默认。

规范拓扑计划记录节点依赖与边级信息共享。审稿人席位在综合前无法读取同行输出；七节点审稿人 arm 是一个 field configurer、五个盲审席位与一个综合器，而非七个审稿人。

## 验证

从仓库根目录运行适配器冒烟/对齐检查：

```bash
python3 skills/academic-research-suite/codex/scripts/ars_codex_quality_gates.py all
python3 -m pytest skills/academic-research-suite/codex/tests
python3 skills/academic-research-suite/codex/scripts/ars_codex_topology_experiment.py validate --require-runs
```

按需从 vendored ARS 根目录运行上游验证器：

```bash
cd skills/academic-research-suite/ars
python3 -m pytest scripts/test_codex_router_policy.py
python3 scripts/check_passport_reset_contract.py
python3 scripts/check_v3_9_2_phase_boundary.py
python3 scripts/check_cross_model_handoff_contract.py
python3 scripts/check_degradation_registry.py
python3 scripts/check_pipeline_boundary_semantics.py
python3 scripts/check_tools_allowlist.py
python3 scripts/check_data_flows.py
python3 scripts/check_control_availability.py
python3 scripts/check_stage_capability_matrix.py
python3 scripts/check_risk_register.py
python3 -m pytest scripts/test_verification_cache.py scripts/test_verification_gate.py
python3 -m pytest scripts/test_ars_update_check.py
python3 -m pytest scripts/test_pdf_read_preflight.py scripts/test_ars_mark_read.py
python3 -m pytest scripts/test_check_revision_token_conservation.py
python3 -m pytest scripts/test_cross_model_codex_transport.py
python3 scripts/check_630_codex_subscription_transport.py
python3 scripts/check_evidence_row_integration.py
python3 scripts/check_670_revision_roadmap_integration.py
python3 scripts/check_684_review_criteria_binding.py
python3 scripts/check_human_subjects_output_contract.py
python3 scripts/check_bibliographic_integrity_signals.py
python3 scripts/check_cross_document_consistency_advisory_integration.py
python3 -m pytest scripts/test_research_workflow_profile.py scripts/test_inquiry_branch_ledger.py
python3 -m pytest scripts/test_check_data_access_level.py scripts/test_review_criteria_binding.py
python3 -m pytest scripts/test_check_promotion_bakeoff_preregistration.py
```

不要从该 vendored 根目录运行 `check_promotion_bakeoff_preregistration.py verify-tree`；该命令需要完整的规范上游历史。
