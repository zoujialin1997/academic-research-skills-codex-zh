# 设计规格：专业术语通俗解释协议（Plain-Language Terms Protocol）

- **日期**：2026-08-26
- **状态**：已批准（用户 2026-08-26 确认）
- **目标版本**：Codex 包 `0.3.0`（MINOR）
- **仓库**：`academic-research-skills-codex-zh`
- **分支策略**：`codex/plain-terms` worktree 开发，验证后合并回 `main`

## 背景与动机

原项目与用户交互时会大量出现专业词汇、概念与定义（如 Socratic、fidelity、calibration、meta-analysis、RQ、R&R、IMRaD、PRISMA 等），用户可能并非专业人士，难以理解。目标是在不改变语义的前提下，为用户添加适当的通俗易懂解释。

调研结论：

- `ars/` 内已有的术语表（`hei_domain_glossary.md`、`irb_terminology_glossary.md`、`psychometric_terminology_glossary.md`）是**面向模型内部的领域规范**（调查设计、人类受试、心理测量），不是面向用户的通俗解释，且位于 `ars/`（上游 vendored，禁止修改）。
- 用户会接触术语的场景：SKILL.md 路由说明、工作流提问、模式选择（fidelity/balanced/originality、calibration、quick…）、报告/评审输出。
- 适配层（`SKILL.md` / `codex/`）是唯一可落地扩展点，可仿照「固定选项点选协议」加全局指令，会话级自动覆盖 `ars/` 工作流（不改 `ars/`）。

## 目标

1. 面向用户的所有输出中，专业术语首次出现时用括号附一句通俗解释。
2. 保留术语原文，解释为补充；用大白话、不超过一句话、不引入新术语。
3. 跟随会话语言（中文会话用中文解释，英文/韩文用对应语言）。
4. 不改动 `ars/` 文件；遵循仓库治理（双副本、guard、版本 MINOR `0.3.0`）。

## 用户确认的决策

1. 覆盖范围：所有面向用户的输出（A）——路由说明、工作流提问、模式选择、报告/评审输出。
2. 解释形式：术语后括号一句通俗解释，首次出现解释一次（A）。
3. 实现机制：纯指令（B）——不建术语表，由模型按规则自行解释。
4. 实现方式：方案 1——`SKILL.md` 新增「专业术语通俗解释」小节（纯指令，无新增文件）。
5. 版本：`0.3.0`（MINOR）。

## 前后效果差异

| 场景 | 改动前 | 改动后 |
|---|---|---|
| Socratic 模式路由 | 「先用 Socratic 模式收敛你的研究问题」 | 「先用 Socratic 模式（像苏格拉底提问一样，用问题引导你逐步想清楚研究问题）收敛方向」 |
| reviewer 模式选择 | 「快速评估（quick，fidelity）」 | 「快速评估（quick，15 分钟快速看一遍给出要点）」 |
| 报告/评审输出 | 术语直接出现 | 首次出现带括号通俗解释 |
| 英文/韩文会话 | 无解释 | 用会话语言解释 |

## 文件改动

- `skills/academic-research-suite/SKILL.md`（受保护文件）
- `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（双副本，逐字节一致）
- 版本四处：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`（源 + 插件副本）、`plugin.json` 的 `version` → `0.3.0`
- `CHANGELOG.md`

新增小节位置：紧邻「固定选项点选协议」之后、`## 安全边界` 之前。

## 协议正文（写入 SKILL.md）

```markdown
## 专业术语通俗解释

面向用户的所有输出（路由说明、工作流提问、模式选择、报告/评审输出）中，遇到专业术语时按以下方式处理：

1. **首次出现即解释**：同一术语在同一会话中首次出现时，紧跟术语后加括号附一句通俗解释。例如：元分析（把多篇独立研究的结果合并统计，得出更可靠的结论）。
2. **保留术语原文**：通俗解释是补充，不替换术语本身；解释用大白话，不超过一句话，且不引入新的专业词汇。
3. **跟随会话语言**：中文会话用中文解释，英文/韩文会话用对应语言解释。
4. **覆盖所有交互**：面向用户的提问与选项、工作流说明、模式名称、报告与评审结论中的术语都要解释；只供内部使用、用户不会直接看到的输出除外。
5. **按需展开**：用户表示仍不理解或要求详细说明时，可展开成一小段通俗说明，但不改变原意、不省略必要信息。
```

## 边界（YAGNI）

- 不做：不建术语表（纯指令）、不做术语抽取工具、不改 `ars/` 文件、不解释面向开发者而非用户的内部契约/文件路径。
- 术语定义：用户不易理解的学术/评审/统计/工作流词（Socratic、fidelity、calibration、meta-analysis、RQ、R&R、IMRaD、PRISMA 等）；日常词不解释。

## 版本变更（0.3.0，MINOR）

- 四处同步更新为 `0.3.0`：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`（源 + 插件副本）、`plugin.json` 的 `version`。
- `CHANGELOG.md`：将 `Unreleased` 归档为 `## [0.3.0] - 2026-08-26`，再新建空的 `Unreleased` 段。
- 打 tag：`git tag v0.3.0`。
- 受保护文件变更后：`python scripts/verify_localization_guard.py --update` 再 `--check`。

## 治理与流程

1. 在 `main` 上创建 `codex/plain-terms` 分支 + worktree（`../academic-research-skills-codex-zh.worktrees/plain-terms/`）。
2. 在 worktree 内完成双副本 `SKILL.md` 改动 + 版本四处 + `CHANGELOG.md`。
3. 验证：guard `--update` + `--check`、`python -m pytest skills/academic-research-suite/codex/tests`。
4. 合并回 `main`，清理 worktree。
5. 同步插件缓存 `plugins\cache\ars-codex-zh\ars-codex-zh\0.3.0\`，用户重启 Codex app 生效。
6. 真实验证受限（codex CLI 不可用），以文本一致性 + guard + pytest 为准。

## 未决 / 风险

- 解释措辞由模型把握，无法保证每次完全一致（用户已接受纯指令方案）。
- 无法在本环境端到端验证实际交互效果，需用户重启 app 后人工确认。
