# 设计规格：新手教程与交互式引导（Beginner Guide & Interactive On-Ramp）

- **日期**：2026-08-27
- **状态**：已批准（用户 2026-08-27 确认）
- **目标版本**：Codex 包 `0.4.0`（MINOR）
- **仓库**：`academic-research-skills-codex-zh`
- **分支策略**：`codex/beginner-guide` worktree 开发，验证后合并回 `main`

## 背景与动机

功能验收通过后，用户反馈：对于新手，仍不知道怎样正确使用这个插件（不知道从哪开始、怎么触发各工作流、什么时候该用什么模式）。需要一个新手教程，并提供插件内交互式引导。

调研结论：

- 仓库目前**没有面向新手的教程**；`README_ZH-CN.md` 的「使用方法」章节是参考手册式（别名表、模式说明、冒烟测试），不是逐步上手指南。
- `ars/QUICKSTART.md` 是上游 Claude Code 版的英文快速入门（vendored，禁止修改），内容可参考但不可改。
- 适配层（`SKILL.md` / `codex/`）与根文档可自由落地；`codex/` 与 `README_ZH-CN.md` 均在受保护清单内。

## 目标

1. 提供完整的中文新手教程文档，从零到会用。
2. 插件内提供交互式引导（`/ars-guide`），在聊天中逐步带新手走一遍。
3. 模型遇到新手求助时主动推荐教程与 `/ars-guide`。
4. 遵循仓库治理：双副本逐字节一致、guard 保护、版本 MINOR `0.4.0`。

## 用户确认的决策

1. 教程形态：独立文档 + `README_ZH-CN.md` 入口链接（A）。
2. 内容范围：从零到会用的完整上手（A）——插件是什么、安装、首次使用、5 个场景、完整示例、新交互说明、常见误区。
3. 插件感知：文档 + 插件引用（B）——`SKILL.md` 加「新手引导」小节，属行为改动，升 MINOR。
4. 附加：插件内交互式引导（`/ars-guide` 命令）。
5. 实现方式：方案 1（三件套）——根文档 + SKILL.md 引用规则 + `/ars-guide` 命令。
6. 版本：`0.4.0`（MINOR）。

## 前后效果差异

| 场景 | 改动前 | 改动后 |
|---|---|---|
| 新手找教程 | 只有参考手册式 README | `GETTING_STARTED_ZH-CN.md` 完整教程 + README 顶部入口 |
| 新手问「怎么用」 | 模型按既有路由自行回答 | 推荐教程 + 引导 `/ars-guide` 交互走查 |
| 聊天内想先看看 | 无从下手 | `/ars-guide`：点选卡片问想做什么 → 给示例提示词 → 引导试跑 |
| 具体任务 | 正常路由 | 不受影响，仍按「工作流路由」处理 |

## 文件改动

- 新增 `GETTING_STARTED_ZH-CN.md`（根文档，教程正文）。
- 修改 `README_ZH-CN.md`（受保护）：顶部加「🚀 新手从这里开始」入口链接。
- 修改 `skills/academic-research-suite/SKILL.md` + 插件双副本（受保护）：新增「新手引导」小节 + 别名路由表加 `/ars-guide` 行。
- 新增 `skills/academic-research-suite/codex/commands/ars-guide.md` + 插件双副本（`codex/` 受保护树内新文件）。
- 版本四处 `0.3.0 → 0.4.0`：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`（源 + 插件副本）、`plugin.json` 的 `version`。
- `CHANGELOG.md`。

## 教程大纲（GETTING_STARTED_ZH-CN.md）

```
# ARS-Codex 中文版 · 新手快速上手
## 0. 一句话：这个插件能帮你做什么
## 1. 安装要点（指向 README 安装章节）
## 2. 第一次使用：3 分钟起步（自然语言直接说需求即可触发）
## 3. 五个典型场景怎么触发（深度研究 / 写论文 / 论文评审 / 文献综述 / 完整管线，各配示例提示词）
## 4. 走一遍完整示例（论文规划：Socratic 收敛 → 大纲 → 写作 → 评审）
## 5. 你会遇到的新交互（Plan 模式点选卡片 / 编号列表 / 术语通俗解释）
## 6. 常见误区与技巧（模糊主题先进 Socratic；[direct-mode] 可跳过；提问阶段切 Plan 模式；材料给全；安全边界）
## 7. 更多资源（README / /ars-guide / 各工作流文档）
```

## SKILL.md「新手引导」小节（写入内容）

```markdown
## 新手引导

当用户表示自己是新手、不知道如何使用本插件、或请求教程/帮助时：

1. 推荐 `GETTING_STARTED_ZH-CN.md`（仓库新手教程），并引导其使用 `/ars-guide` 交互式走查。
2. 若用户直接说「新手教程」「怎么用」「guide」等，以 `/ars-guide` 的交互式走查响应：先问用户想做什么（固定选项，遵循「固定选项点选协议」），再按所选场景给出一句可直接复制的示例提示词与简要说明。
3. 不改变既有工作流路由；用户给出具体任务时仍按「工作流路由」正常处理。
```

别名路由表新增行：

`| /ars-guide, ars-guide | codex/commands/ars-guide.md | 新手交互式引导（不进入具体工作流） |`

## /ars-guide 命令配方（codex/commands/ars-guide.md）

- 欢迎一行 → 用固定选项问「你现在最想先做哪件事？」（Plan 模式弹卡片/否则编号）：深度研究 / 写论文 / 论文评审 / 文献综述 / 完整管线 / 只想先了解。
- 按所选场景给一句可直接复制的示例提示词 + 一行说明触发哪个工作流。
- 再问「要不要现在试试？」（固定选项：现在试 / 换场景 / 结束）→ 引导继续或收尾推荐教程。
- 全程遵守「专业术语通俗解释」与「固定选项点选协议」。

## 边界（YAGNI）

- 不做：教程多语言版（本版仅简体中文，其他语言后续再说）、不新增专门 agent、不改 `ars/` 文件、不改既有工作流路由逻辑。
- 根文档不随插件安装；插件内引导由 `/ars-guide` 命令承担（避免教程内容双份）。

## 版本变更（0.4.0，MINOR）

- 四处同步更新为 `0.4.0`：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`（源 + 插件副本）、`plugin.json` 的 `version`。
- `CHANGELOG.md`：归档 `## [0.4.0] - 2026-08-27`，新建空 `Unreleased`。
- 打 tag：`git tag v0.4.0`。
- 受保护文件变更后：`python scripts/verify_localization_guard.py --update` 再 `--check`。

## 治理与流程

1. 在 `main` 上创建 `codex/beginner-guide` 分支 + worktree（`../academic-research-skills-codex-zh.worktrees/beginner-guide/`）。
2. 在 worktree 内完成：根文档、README 入口、SKILL.md 小节 + 别名行（双副本）、新命令（双副本）、版本四处、CHANGELOG。
3. 验证：guard `--update` + `--check`、`python -m pytest skills/academic-research-suite/codex/tests`。
4. 合并回 `main`，清理 worktree。
5. 同步插件缓存 `plugins\cache\ars-codex-zh\ars-codex-zh\0.4.0\`，用户重启 Codex app 生效。
6. 真实验证受限（codex CLI 不可用），以文本一致性 + guard + pytest 为准。

## 未决 / 风险

- 教程措辞与示例提示词质量依赖人工审阅；无法在本环境端到端验证 `/ars-guide` 实际交互，需用户重启后人工确认。
- 根文档 `GETTING_STARTED_ZH-CN.md` 不随插件安装，新手需通过仓库/README 或 `/ars-guide` 获取引导。
