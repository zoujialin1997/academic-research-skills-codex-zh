# 设计规格：固定选项点选协议（Choice-Card Protocol）

- **日期**：2026-08-26
- **状态**：已批准（用户 2026-08-26 确认）
- **目标版本**：Codex 包 `0.2.0`（MINOR）
- **仓库**：`academic-research-skills-codex-zh`
- **分支策略**：`codex/choice-card` worktree 开发，验证后合并回 `main`

## 背景与动机

用户希望把「引导用户回答固定选项多选一」的交互从打字改为弹出点选卡片，直接点选即可，不用打字。

调研结论：

- brainstorming 的弹出卡片是 Codex 系统级工具 `request_user_input` 渲染的，仅在 **Plan 模式**可用（本会话在 Default 模式调用被系统拒绝，现场验证）。
- 插件（`SKILL.md` / `codex/commands/` / `plugin.json`）无法注册原生 UI 卡片，只能通过指令让模型在工具可用时调用系统工具。
- `request_user_input` 每问最多 2-3 个选项，系统自动附带「Other」自由输入。
- 上游 `ars/shared/references/intent_clarification_protocol.md` 明确禁止调用 AskUserQuestion，采用 a-d 正文格式（3-4 个选项 + something else）。本功能是用户显式要求的适配层覆盖，不改 `ars/` 文件。

## 目标

1. Plan 模式下，2-3 个固定选项的单选提问弹出点选卡片。
2. 其他情况（非 Plan / 4+ 选项 / 多选 / 需补充说明）降级为「编号列表 + 回复数字」。
3. 覆盖 `ars/` 工作流内部所有提问，但不改动 `ars/` 文件。
4. 遵循仓库治理：双副本逐字节一致、guard 保护、版本 MINOR `0.2.0`。

## 用户确认的决策

1. 策略：混合降级（A）——Plan 模式弹卡片，其他模式编号降级。
2. 范围：全部固定选项单选提问（A）——通过适配层全局指令覆盖。
3. 配合方式：提问阶段切 Plan 模式（A）。
4. 实现方式：方案 1——`SKILL.md` 新增「固定选项点选协议」小节 + 更新 `AskUserQuestion` 映射行。
5. 版本：`0.2.0`（MINOR）。

## 前后效果差异

| 维度 | 改动前 | 改动后 |
|---|---|---|
| Plan 模式、2-3 选项单选 | 纯文本列表，打字回复 | 弹出点选卡片，直接点选 |
| 非 Plan / 4+ 选项 | 纯文本 a-d / 模式列表 | 统一编号列表，回复数字 |
| `ars/` 内部提问 | 上游正文格式 | 受会话级协议覆盖 |
| `[direct-mode]` | 保留 | 保留，不受影响 |

## 文件改动

- `skills/academic-research-suite/SKILL.md`（受保护文件）
- `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（双副本，逐字节一致）
- 版本三处：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version` → `0.2.0`
- `CHANGELOG.md`

### 1. 更新 `AskUserQuestion` 映射行

原：

`| AskUserQuestion | 提出简明澄清问题，或当当前模式可用时使用 Codex 的结构化用户输入工具。 |`

新：

`| AskUserQuestion | 提出简明澄清问题；固定选项单选提问遵循「固定选项点选协议」：Plan 模式弹点选卡片，否则编号列表。 |`

### 2. 新增「固定选项点选协议」小节（置于 `## 安全边界` 之前）

## 协议正文（写入 SKILL.md）

```markdown
## 固定选项点选协议

当需要用户从固定候选选项中单选一个时（覆盖 ars/ 工作流、codex/commands/ 与本路由中的提问），按以下方式呈现：

1. **检测**：候选为互斥的固定选项、单选、数量 2-3 个的提问才进入卡片路径；其余走编号降级。
2. **卡片路径（Plan 模式）**：若 request_user_input 工具可用，调用它弹出点选卡片：
   - 每个选项映射为 label（1-5 词短标签）与 description（一句话说明取舍）；
   - 推荐选项置于第一位并加「（推荐）」；系统自动附带 Other 自由输入；
   - 等待用户点选后再继续工作流。
3. **编号降级（其他情况）**：工具不可用、选项 ≥ 4 个、或多选/需补充说明时，输出编号列表：
   - 每项一行「编号. 选项名 —— 一句话说明」，末尾加「其他：请直接输入」；
   - 提示「请回复对应编号」。
4. **优先级**：本协议覆盖上游 intent_clarification_protocol.md 中「不使用 AskUserQuestion、选项放正文」的限制；不改动 ars/ 文件；[direct-mode] 跳过澄清入口保持不变。
```

## 边界（YAGNI）

- 不做：多选卡片、4+ 选项卡片、自由文本问题改造、`[direct-mode]` 改动。
- 苏格拉底收敛等开放性问题保持自由文本提问（不属于固定选项单选）。

## 版本变更（0.2.0，MINOR）

- 三处同步更新为 `0.2.0`：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`。
- `CHANGELOG.md`：将 `Unreleased` 归档为 `## [0.2.0] - 2026-08-26`，再新建空的 `Unreleased` 段。
- 打 tag：`git tag v0.2.0`。
- 受保护文件变更后：`python scripts/verify_localization_guard.py --update` 再 `--check`。

## 治理与流程

1. 在 `main` 上创建 `codex/choice-card` 分支 + worktree（`../academic-research-skills-codex-zh.worktrees/choice-card/`）。
2. 在 worktree 内完成双副本 `SKILL.md` 改动 + 版本三处 + `CHANGELOG.md`。
3. 验证：guard `--update` + `--check`、`python -m pytest skills/academic-research-suite/codex/tests`。
4. 合并回 `main`，清理 worktree。
5. 同步插件缓存 `plugins\cache\ars-codex-zh\ars-codex-zh\0.1.27\`，用户重启 Codex app 生效。
6. 真实验证受限（codex CLI 因 WindowsApps 打包版拒绝访问），以文本一致性 + guard + pytest 为准。

## 未决 / 风险

- 真卡片仅在 Plan 模式出现；用户需在提问阶段手动切 Plan 模式。
- 无法在本环境端到端验证卡片渲染，需用户重启 app 后人工确认。
- 4+ 选项（意图澄清 a-d、reviewer 6 模式）注定走编号降级，这是工具上限，非缺陷。
