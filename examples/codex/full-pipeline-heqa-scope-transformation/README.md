# Codex 平台管线冒烟遍历——HEQA 范围转换（HEQA Scope Transformation）

本目录按上游 ARS 仓库中 [`CONTRIBUTING.md § Platform ports` L55](https://github.com/Imbad0202/academic-research-skills/blob/main/CONTRIBUTING.md#platform-ports-community-maintained-only)
的要求提供 Codex 平台回归证据：**"在目标平台上至少运行一次完整的 `academic-pipeline`，并在 sibling 仓库的 `examples/` 路径下提交，以便检测回归。"**

## 诚实范围

这是**冒烟级管线遍历**，而非生产质量的全量运行。读者需要知道的取舍：

- **每个被路由的阶段都用了其工作流最轻量的模式**：Stage 2 = `outline-only`（非 `full`），Stage 3 = `quick`（单编辑，非 5 审稿人 + DA），Stage 4 = `revision-coach`（路线图，非正文重写）。
- **Stage 3'（再评审）与 Stage 4'（第二次修改循环）缺失。** ARS 架构允许最多 2 个修改循环；此遍历在一次后停止。
- **Stage 5（定稿）为导入而非本次运行产生。** `abstract.md` + `index.html` 来自 2026-05-10 的先前 `ars-codex` 研究会话。`stages/` 中的 Stage 1–4.5 + 6 转录于 2026-05-11 生成，专门为 L55 要求提供回归证据。
- **未演练跨模型验证（`ARS_CROSS_MODEL`）。**
- **未演练 `systematic-review` 与 `experiment-agent` 工作流。**

此遍历**确实**按 ARS 管线架构演示了：

1. 每次阶段转换的路由器分类都在本次运行中路由（Stages 1、2、3、4——可在每个阶段文件中验证）。此处未演练 Stage 5 路由，因为 Stage 5 产物导入自先前会话。
2. 两个 MANDATORY 学术诚信闸门（Stage 2.5 + 4.5）均按失败模式给出 PASS/HOLD 判定启用。
3. 跨阶段交接：Stage 3 评审关切 → Stage 4 路线图 → Stage 4.5 回归观察点。
4. Stage 6 过程摘要，带 6 维协作质量评分标准与架构性反讽警示。

这四项属性中任何一项的回归，都可通过重跑 `stages/` 中的各阶段提示来检测。

## 运行摘要

| 属性 | 值 |
|---|---|
| 目标平台 | Codex CLI |
| 运行器 | `codex` 0.130.0，通过 `codex exec --ephemeral --sandbox read-only` |
| 套件 skill | `$academic-research-suite`（单个 Codex skill，ars-* 别名） |
| 主题 | "From Compliance Assurance to Quality Intelligence: A Scope Transformation Matrix for HEQA in the Agentic AI Era" |
| 捕获 Stage 1–4.5 + 6 转录 | 2026-05-11 |
| Stage 5 产物（导入）日期 | 2026-05-10 |
| 近似成本 | 约 $1–2 OpenAI API（6 次 `codex exec` 调用，低推理，累计约 190k token） |

## 阶段映射

| 阶段 | 文件 | 判定 |
|---|---|---|
| 1 — research/socratic | `stages/stage1_research_socratic.md` | 路由器正确路由；3 个 FINER 对齐的收敛问题 |
| 2 — write/outline-only | `stages/stage2_write_outline.md` | 5 节大纲；应用理论论文结构模板 |
| 2.5 — integrity gate | `stages/stage2.5_integrity_gate.md` | 2 个 HOLD（提示编号模式 5 + 6 = 规范 Lu 2026 模式 6 + 7；编号披露见文件） |
| 3 — review/quick | `stages/stage3_review_quick.md` | Major Revision；3 个实质关切 |
| 4 — revision-coach | `stages/stage4_revision_roadmap.md` | 与 3 个评审关切对齐的 P1/P1/P2 路线图 |
| 4.5 — final integrity | `stages/stage4.5_final_integrity.md` | PASS，带 2 个起草观察点 |
| 5 — finalize | `abstract.md`、`index.html`（导入，2026-05-10） | 来自先前 `ars-codex` 会话的 Stage 5 产物，非本 2026-05-11 遍历产生 |
| 6 — process summary | `stages/stage6_process_summary.md` | 6 维评分 + 反讽警示 |

## 跨阶段回归信号

最强的回归信号出现在阶段转换处：

- **Stage 2.5 → Stage 3**：两个独立闸门标记了同一弱点（框架锁定 + 过度声称）。若未来运行显示 Stage 2.5 有 HOLD 但 Stage 3 未处理就 PASS，则审稿人路由已回归。
- **Stage 3 → Stage 4**：revision-coach 路线图条目必须与 Stage 3 关切一一对应。路线图条目 #1 / #2 / #3 与评审关切 #1 / #2 / #3 对齐。
- **Stage 4 → Stage 4.5**：最终诚信必须区分"已由修改清除"与"由修改引入的新观察点"。本次运行各产出两个——闸门在做二阶回归检测，而非仅重跑模式。

## 本次运行未证明的内容

- 未演练 `ARS_CROSS_MODEL` 跨模型验证（按 ars-codex README，需要外部提供商凭证与显式同意）。
- 未演练 `systematic-review` 模式（PRISMA）或 `experiment-agent` 工作流。
- 未运行 `academic-paper full` 模式（该模式会调用 v3.6.8 生成器-评估器两阶段契约闸门）。vendored 上游 commit `1d0c8625` 早于 v3.6.8——钉定的上游 commit 见 `../../../skills/academic-research-suite/manifest.json`。
- 转录是 `codex exec` 运行的**摘录**，而非字节等价复现。LLM 输出按设计不可字节复现（见上游 `shared/artifact_reproducibility_pattern.md`）。

## 如何重跑做回归检查

```bash
# 要求：已安装并认证 codex CLI；已安装 $academic-research-suite skill。
# 每个阶段独立；可重跑任一单个阶段检查该工作流。

cd /path/to/academic-research-skills-codex

# Stage 1 路由器检查（无 RQ → 必须路由到 deep-research socratic）
codex exec --ephemeral --sandbox read-only -c model_reasoning_effort=low \
  "$(cat examples/codex/full-pipeline-heqa-scope-transformation/stages/stage1_research_socratic.md | sed -n '/^## User prompt/,/^## Codex response/p' | sed '1d;$d' | sed 's/^```text$//;s/^```$//')"

# 对 stages 2, 2.5, 3, 4, 4.5 重复——每个阶段文件中有逐字用户提示。
```

以下情况可检测到回归：
- 同一提示的路由器分类变化。
- 诚信闸门跳过模式或停止产生 PASS/HOLD 判定。
- 阶段转换停止向前携带发现（例如 Stage 2.5 有 HOLD 且中间没有修改时 Stage 3 却 PASS）。
