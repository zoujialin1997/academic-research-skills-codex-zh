# ARS-Codex 兼容性矩阵（Compatibility Matrix）

审计日期：2026-08-24

## 来源（Provenance）

| 表面 | 证据 |
|---|---|
| Codex 包仓库 | `academic-research-skills-codex` 发布提交前的当前工作树 |
| 上游 Claude Code 仓库 | 由 `skills/academic-research-suite/manifest.json` 跟踪 |
| 上游套件版本 | `v3.21.1` |
| 上游组件版本 | deep-research `2.12.1`；academic-paper `3.3.1`；academic-paper-reviewer `1.11.1`；academic-pipeline `3.21.1` |
| Codex 包版本 | `0.4.1` |
| 许可证 | 上游与 Codex 包均为 CC BY-NC 4.0 |
| 上游同步状态 | vendored `ars/` 内容同步至已签署的 ARS 发行版 `v3.21.1`（peeled commit `127ff85e4bbfcdd10b95040537b6c6bd7ad17aeb`）；保留 Codex 适配器 profile |
| Codex 专属适配器位置 | `skills/academic-research-suite/codex/` |

## 矩阵

| 能力 | 默认 Codex 状态 | 可选全运行时 Profile | 对齐级别 | 实现位置 | 验证方法 | 剩余风险 |
|---|---|---|---|---|---|---|
| 安装 / 更新 | 来自仓库 marketplace 的原生 `ars-codex-zh` 插件，保留直接 skill 安装作为替代 | 运行时不改变 profile | near | `.agents/plugins/marketplace.json`、`plugins/ars-codex-zh/`、`README.md` | plugin validator；`desktop-plugin-bundle` 闸门；`/skills` | marketplace 用户在重新安装更新前必须刷新 Git 快照 |
| `ars-*` 别名 | 根路由器模拟 Claude 命令意图 | 确定性 planner 发出相同别名路由元数据 | near | `SKILL.md`、`codex/full-runtime-manifest.json`、`codex/scripts/ars_codex_full_runtime.py` | adapter pytest；manifest 闸门 | 斜杠前缀输入仍可能被客户端拦截 |
| 模糊论文主题路由 | 根路由器将模糊论文主题发送至非生成 Socratic 收敛；未收敛绝不授权系统代写候选问题 | Planner 保留相同覆盖，并要求显式用户请求退出 | near | `SKILL.md`、`ars/deep-research/references/socratic_mode_protocol.md`、`codex/scripts/ars_codex_full_runtime.py` | adapter pytest；上游路由与非生成契约测试 | 冒烟场景之外自然语言路由仍是启发式的 |
| Agent 提示词 | `agents/*.md` 作为角色/阶段提示内联读取 | `codex/agents/*.md` 提供指向源提示词的选择加入 agent-team 模板 | near | `ars/*/agents/*.md`、`codex/agents/*.md` | manifest 闸门；reviewer 夹具闸门 | 实际子 agent 可用性取决于活动 Codex 运行时 |
| Agent 最小权限 | 受保护的顶级 agent `tools:` 白名单仍是角色边界；内联使用不扩大权限 | 派发的受保护角色不获得 Bash 或网络传输；dispatcher 拥有跨模型传输 | near | `ars/agents/*.md`、`ars/scripts/check_tools_allowlist.py`、`SKILL.md` | 上游 tools-allowlist lint 与测试 | 实际执行仍取决于活动 Codex 运行时的工具控制 |
| 数据访问声明 | 四个核心工作流均保留上游最脏输入 `raw` 声明；单独 vendored 的 experiment-agent 也钉定为 `raw` | 全运行时元数据保留声明而不将其变成权限 | near | `ars/scripts/check_data_access_level.py`、`ars/scripts/test_check_data_access_level.py`、`ars/experiment-agent/WORKFLOW.md` | 确定性数据访问 lint 与封闭变异测试 | 标注不是沙箱、降密、隔离证明或运行时权限边界 |
| 审稿人独立性 | 内联模式必须在综合前保留独立审稿人章节 | Agent-team planner 在编辑部综合前排列独立审稿人章节 | near | `codex/agents/paper-reviewer-panel.md`、`codex/tests/fixtures/reviewer_full_independent_sections.md` | reviewer 夹具闸门；adapter pytest | 内联运行依赖忠实保留章节边界 |
| 审稿人评分与来源诚实性 | 实时评审使用证据锚定的分类标准判断并保持 `NOT_CALIBRATED`；无分数、权重、总计、平均、排名或二元独立性声明 | 全运行时携带六个可观察面板来源轴，而不用置信度作为加权规则 | near | `ars/scripts/check_reviewer_scoring_honesty.py`、`ars/scripts/review_panel_provenance.py`、`codex/full-runtime-manifest.json` | 上游诚实性与来源测试；adapter manifest 验证 | 分类判断仍需要实质专家推理；来源不是独立性的证明 |
| 可执行面板综合 | 审稿人产物可用 vendored 封闭语法面板检查器检查 | Planner 将检查器暴露为评审质量门 | near | `ars/scripts/check_panel_synthesis.py`、`codex/full-runtime-manifest.json` | 上游面板检查器测试 | 检查器验证产物自洽性，而非实质正确性 |
| Hooks 与更新提醒 | 上游 Claude hooks 与 v3.18 SessionStart 更新检查器仅为元数据 | 默认禁用的只读 Codex hook 包；无自动上游更新检查 | partial | `ars/scripts/ars_update_check.sh`、`codex/hooks/hooks.json`、`codex/scripts/ars_codex_hook.py` | `hook-safety` 闸门；上游更新检查测试 | 插件用户刷新并重新添加 marketplace 包；直接 skill 用户重装或 pull |
| 模型路由 | 重型 `ars-full`、`ars-reviewer` 与 `ars-revision-coach` 路由无 v3.21.1 模型 frontmatter 并继承会话模型；轻路由保留 `sonnet` 元数据 | Planner 报告 `inherit` 或轻路由提示而不强制模型变更 | partial | `codex/full-runtime-manifest.json`、`codex/scripts/ars_codex_full_runtime.py` | adapter pytest；计划检查 | 与 Claude Code 模型钉定不等价 |
| ARS 模型分层 | 未设置时保留活动 Codex 模型 | Planner 将 `economy` / `quality-boost` 呈现为建议性元数据；仅当存在按派发模型选择时应用分类 | partial | `ars/shared/model_tiering.md`、`ars/scripts/model_tiering_manifest.json`、`codex/scripts/ars_codex_full_runtime.py` | 上游 tiering lint；adapter pytest | Codex 运行时可能不暴露相对层级或按派发模型控制 |
| Material Passport | 提示/流程加上 vendored 验证器 | 全运行时 manifest 将 passport 重置暴露为质量门 | near | `ars/scripts/check_passport_reset_contract.py`、`codex/full-runtime-manifest.json` | 上游验证器；adapter 闸门 | 运行时上下文隔离是程序性的，而非硬沙箱 |
| 研究工作流 profile 底座 | 默认关闭的确定性选择记录显式 profile 或可见 `field_general` 回退；稿件内容绝不用于推断研究家族 | Manifest 记录独立选项与契约测试，但不添加 planner 或管线 hook | partial | `ars/scripts/research_workflow_profile.py`、`ars/shared/contracts/research_workflow/`、`ars/shared/research_workflow_profiles/field_general.json` | 封闭 profile/schema/修正测试 | 行为证据为 `NOT_RUN`；不存在家族特定随附 profile、可用性结果或研究结果声明 |
| 查询分支台账 alpha | 精确标志 `ARS_INQUIRY_LEDGER=1` 启用本地持久事件台账；从第二分支开始发布，摘要仅在受限检查点出现 | Manifest 注册契约测试，但绝不自动设置标志或执行台账写入 | near | `ars/scripts/inquiry_branch_ledger.py`、`ars/shared/contracts/research_workflow/inquiry_branch_ledger.schema.json`、`ars/shared/contracts/passport/inquiry_ledger_ref.schema.json` | 封闭追加、路径、锁、恢复、过期原因与提示接线测试 | 默认关闭；作者事件是自证，不确立新颖性、正确性、价值、恢复收益或可用性声明 |
| 引文缓存时效与再验证 | 缓存验证保持默认；过期行仅建议性 | Planner 呈现阈值以及是否请求了实时再验证 | near | `ars/scripts/verification_cache.py`、`ars/scripts/verification_gate/`、`codex/scripts/ars_codex_full_runtime.py` | 上游 cache/gate 测试；adapter pytest | 实时再验证依赖外部文献服务 |
| 本地 PDF 读取完整性 | 本地读取的 PDF 在信任页面 anchor 前接收结构 preflight；`--classify-content` 可选添加进程隔离的文本/OCR 建议 | Planner 契约要求 Stage 1 sidecar、时效检查与独立的 FAIL/UNAVAILABLE 处理；分类绝不改变 `STRUCTURE_ONLY` 判定范围 | near | `ars/scripts/pdf_read_preflight.py`、`ars/scripts/pdf_content_classifier_worker.py`、`ars/requirements-pdf-content-classifier.txt` | 上游 preflight/classifier 测试；边界验证器 | 缺失可选依赖产生确定性 `UNAVAILABLE`；classifier 输出不是自动 OCR 或 anchor 闸门 |
| 人工已读范围 | 每个新标记要求用户拥有的 `read_scope`；显式 unknown 与遗留缺失范围保持 `coverage_unknown`，部分覆盖保持可见 | Orchestrator 携带范围并在每次定稿 pass 运行确定性 resolver | near | `ars/scripts/ars_mark_read.py`、`ars/scripts/human_read_attestation_resolver.py`、`ars/shared/contracts/passport/human_read_log.schema.json` | 上游 mark-read、resolver 与定稿器测试 | 用户自证不是阅读或理解的证明 |
| 修改 claim 漂移防护 | 每个修改轮次以建议性优先检查 claim 强度变化、守恒 token 与独立处置 sidecar | Planner 携带 Revision-Evidence Bundle，而不将处置视为作者裁定 | near | `ars/shared/references/claim_strength_ladder.md`、`ars/scripts/check_revision_token_conservation.py`、`ars/scripts/claim_strength_drift_disposition.py` | 上游变异、处置与 held-out 测量测试 | 语义授权仍需要审稿人与作者判断 |
| Promotion bakeoff 预注册 | sealed 承诺/揭示契约、保留的 2026-08-19 测量产物与封闭生命周期测试被 vendored | Manifest 仅注册封闭契约套件，绝不注册实时 fleet 或直接依赖历史的树验证器 | partial | `ars/scripts/check_promotion_bakeoff_preregistration.py`、`ars/shared/contracts/cross_model/promotion_bakeoff_sealed_*.schema.json`、`ars/evals/bakeoff/` | 临时仓库单元测试；仅上游全历史 `verify-tree` | 重新定根的 vendor 快照无法独立再证明上游公开 seal/reveal 时间线，或授权承载同意/成本的实时模型 fleet |
| 退化来源 | 机器可读注册表记录 21 个优雅退化机制及其下游效果，包括新索引的上游写范围防护 launcher 状态 | 全运行时元数据将注册表检查器注册为手动验证 | near | `ars/shared/contracts/degradation_registry.json`、`ars/scripts/check_degradation_registry.py` | 上游注册表测试 | 上游 Claude-hook 行此处仅为可追溯性；Codex 运行时故障仍要求诚实报告且无有效性声明 |
| 管线终端语义 | Stage 5 入口/完成与 Stage 6 decline/终止确认遵循钉定的上游契约 | Planner 暴露整文件边界锁 | near | `ars/academic-pipeline/WORKFLOW.md`、`ars/scripts/check_pipeline_boundary_semantics.py` | 上游边界测试 | 交互式客户端可能用不同自然语言表达确认 |
| 上游锁定来源 | `manifest.json` 钉定上游 commits | 质量门检查包 manifest 具有完整上游 SHA 与必需 included paths | near | `manifest.json`、`codex/scripts/ars_codex_quality_gates.py` | `upstream-lock` 闸门 | 未来上游同步仍需要审慎的 manifest 更新 |

## 相对 Claude Code 的确切退化

- Codex 不注册原生 Claude 斜杠命令；`ars-*` 别名由根 skill 与可选全运行时 planner 解析。
- Codex 全运行时 agent-team 模式为选择加入且基于 planner/模板。内联执行保持默认。
- ARS-Codex 有自己的原生 Codex marketplace 包；Claude 专属插件命令、斜杠命令注册与 hook 生命周期不被复现。
- Claude Code `SessionStart` 与未来 `SubagentStop` hooks 不会自动安装。因此 v3.18 更新提醒保持非活动；Codex hook 包为手动且只读。
- 重型路由继承活动 Codex 会话模型；轻路由 `sonnet` frontmatter 保留为元数据。除非用户/运行时显式覆盖，两者都不改变模型。
- `ARS_MODEL_TIERING` 保留上游 agent 分类，但无法在无运行时模型覆盖时强制 economy 或 quality-boost 路由。
- 外部跨模型验证绝不静默模拟。
- 固定 Reviewer 2 轨道与 Priority-1 再评审评委 pass 需要外部提供商加上显式内容同意；否则发出所需的单家族或回退披露。
- 派发的 owner 角色自身不执行跨模型传输；派发 Codex 上下文在现有同意闸门之后校验规范外壳并仅传输其 payload。
- 受限 Codex 引文传输是显式仅引文选择器，需要 Codex CLI 0.147.0+、`ARS_CROSS_MODEL`、精确 `Logged in using ChatGPT` 认证与内容/成本同意；它绝不自动回退到 API 或扩展到审稿人调用。
- 仅请求 `ars-full` 不会在此适配器中启动四个 Python 文献 resolver 客户端。程序化引文验证需要单独显式请求；这是对上游脚本支持的 Stage 2.5/4.5 调用的有意运行时分歧。
- 可选 PDF 内容分类需要单独钉定的依赖。其输出仍为 `STRUCTURE_ONLY` 判定范围的建议；依赖缺失可见，不能被提升为结构 `PASS`。
- 来源绑定证据行、作者裁定记录、评审目标绑定、人类受试者轨迹与文献/预注册载体提供确定性来源，而非作者选择、机构批准、法律建议、完整性判定或干净文档证书。
- 引文传输不单独接受 `turn/completed`。它通过干净进程退出与两个输出 EOF 排空，因此迟到的格式错误或禁止事件仍可可见地使运行失败。
- vendored 快照保留 promotion-bakeoff 审计产物、模式与封闭测试，但因未 vendored 规范完整历史而无法独立再证明上游 Git seal/reveal 时间线。
