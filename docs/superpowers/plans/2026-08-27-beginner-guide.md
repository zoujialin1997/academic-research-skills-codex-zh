# 新手教程与交互式引导（Beginner Guide & Interactive On-Ramp）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 ARS-Codex 中文版新增「新手教程与交互式引导」：根教程文档 `GETTING_STARTED_ZH-CN.md` + `README_ZH-CN.md` 入口链接 + `SKILL.md`「新手引导」小节 + 交互式命令 `/ars-guide`；并将包版本升至 `0.4.0`（MINOR）。

**Architecture:** 通过修改适配层（`SKILL.md` 受保护文件 + `codex/commands/` 受保护树内新文件 + 根文档）落地新手引导能力，不改动 `ars/` 上游 vendored 内容。`SKILL.md` 新增「新手引导」小节（行为改动 → MINOR），别名路由表新增 `/ars-guide` 行，新增命令配方文件 `codex/commands/ars-guide.md`。根文档 `GETTING_STARTED_ZH-CN.md` 从零到会用完整教程，`README_ZH-CN.md` 顶部加入口链接与版本徽章更新。所有改动同步双副本（`skills/` ↔ `plugins/ars-codex-zh/skills/` 逐字节一致），版本四处同步 `0.4.0`，`CHANGELOG.md` 归档。全部在 `codex/beginner-guide` 分支 + worktree 完成，验证后合并回 `main`。

**Tech Stack:** Markdown（教程 / SKILL.md / 命令配方）、JSON（manifest.json / plugin.json）、Python 防护脚本 `scripts/verify_localization_guard.py`、pytest（`skills/academic-research-suite/codex/tests`）、git worktree。

## Global Constraints

- **验证纪律（本计划的 RED-GREEN）**：本改动是 Markdown/配置变更，无新增 Python 代码，因此不写单元测试；RED-GREEN 由仓库防护脚本承担：
  - 编辑受保护文件后 `python scripts/verify_localization_guard.py --check` 必须 FAIL（RED）；`--update` 记录新基线后 `--check` 必须 PASS（GREEN）。
  - 双副本逐字节一致由 guard 强制（`skills/academic-research-suite/` vs `plugins/ars-codex-zh/skills/`）。
  - 新增 `codex/commands/ars-guide.md` 属受保护树内新文件，须 `--update` 登记基线。
- **pytest 基线**：`python -m pytest skills/academic-research-suite/codex/tests` 预期 43 passed / 6 个既有失败（`test_quality_gates_all_pass` + 5 个 `test_topology_experiment`），这些失败与本次改动无关、禁止修复；门禁是「不新增失败」。
- **铁律**：禁止编辑 `skills/academic-research-suite/ars/` 任何文件；禁止修改 `ars/` 内 references / templates / agent 提示词。
- **版本一致性**：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`（源 + 插件副本）、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version` 必须全部为 `0.4.0`。
- **环境**：Windows + PowerShell；文本搜索优先 `rg`；codex CLI 不可用（WindowsApps 打包版拒绝访问），真实验证受限，以 guard + pytest + 文本一致性为准。
- **文件操作铁律（本仓库执行教训）**：所有 .NET 文件读写一律使用**绝对路径**；PowerShell 复制用 `Copy-Item -Path "<abs>\*"`（通配符需 `-Path` 而非 `-LiteralPath`）。
- **提交流程**：所有适配层改动在 `codex/beginner-guide` 分支 + worktree 完成，验证通过后合并回 `main`；设计/计划文档直接在 `main` 提交。

---

### Task 0: 建立 `codex/beginner-guide` worktree

**Files:** 无（纯 git 操作，在 `main` 工作区 `G:\academic-research-skills-codex-zh` 执行）

**Interfaces:**
- Consumes: `main` 当前 HEAD = `a62bbe1`（含设计规格；本计划提交后 HEAD 前移）。
- Produces: 新 worktree `G:\academic-research-skills-codex-zh.worktrees\beginner-guide`（分支 `codex/beginner-guide`），后续所有任务在此 worktree 内执行。

- [ ] **Step 1: 创建分支 + worktree**

```powershell
git -C "G:\academic-research-skills-codex-zh" worktree add -b codex/beginner-guide "G:\academic-research-skills-codex-zh.worktrees\beginner-guide" main
```

- [ ] **Step 2: 验证 worktree 状态**

```powershell
git -C "G:\academic-research-skills-codex-zh.worktrees\beginner-guide" status
git -C "G:\academic-research-skills-codex-zh.worktrees\beginner-guide" log --oneline -1
```

Expected: `On branch codex/beginner-guide`、clean、HEAD 为 `main` 当前 HEAD。

- [ ] **Step 3: 提交（无文件改动）**

无需 commit；直接进入 Task 1。

---

### Task 1: 根教程文档 + README 入口（受保护根文档）

**Files:**
- Add: `GETTING_STARTED_ZH-CN.md`（worktree 下绝对路径：`G:\academic-research-skills-codex-zh.worktrees\beginner-guide\GETTING_STARTED_ZH-CN.md`）
- Modify: `README_ZH-CN.md`（受保护）：顶部加「🚀 新手从这里开始」入口链接 + 版本徽章 `v0.1.27 → v0.4.0`

**Interfaces:**
- Consumes: 设计规格 `docs/superpowers/specs/2026-08-27-beginner-guide-design.md` 的教程大纲与「文件改动」。
- Produces: 根教程正文 + README 顶部入口。

- [ ] **Step 1: 新建教程正文**

按设计规格大纲写 `GETTING_STARTED_ZH-CN.md`（7 个章节）：

```text
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

示例提示词与章节内容直接复用设计规格与既有 README 素材，措辞参照 `ars/README.zh-CN.md` 的既有中文术语。

- [ ] **Step 2: README 加入口 + 更新版本徽章**

在 `README_ZH-CN.md` 第 7 行语言链接附近（顶部）插入入口链接，并更新第 3 行徽章：

```markdown
[![Version](https://img.shields.io/badge/version-v0.4.0-blue)](VERSION)
🚀 新手从这里开始 → [《新手快速上手》](GETTING_STARTED_ZH-CN.md)
```

- [ ] **Step 3: 双副本无涉及（根文档只有一份）；运行 guard 刷新基线**

```powershell
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: `--update` 成功；`--check` 退出码 0（GREEN）。根文档改动记录进受保护基线，同时双副本（尚未改动）保持一致。

- [ ] **Step 4: 提交 Task 1**

```powershell
git add GETTING_STARTED_ZH-CN.md README_ZH-CN.md
git add scripts/verify_localization_guard.py
git commit -m "docs: add beginner guide and README entry link"
```

---

### Task 2: `SKILL.md`「新手引导」小节 + 别名行 + `/ars-guide` 命令（双副本）

**Files:**
- Modify: `skills/academic-research-suite/SKILL.md`（worktree 绝对路径）+ 插件副本 `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（逐字节一致）
- Add: `skills/academic-research-suite/codex/commands/ars-guide.md` + 插件副本 `plugins/ars-codex-zh/skills/academic-research-suite/codex/commands/ars-guide.md`（逐字节一致）

**Interfaces:**
- Consumes: 设计规格中「SKILL.md 新手引导小节」「别名路由表新增行」「/ars-guide 命令配方」。
- Produces: 会话级新手引导规则 + 可调用的交互式引导命令（受保护树内新文件）。

- [ ] **Step 1: SKILL.md 新增「新手引导」小节**

在「工作流路由」之后、「固定选项点选协议」之前插入：

```markdown
## 新手引导

当用户表示自己是新手、不知道如何使用本插件、或请求教程/帮助时：

1. 推荐 `GETTING_STARTED_ZH-CN.md`（仓库新手教程），并引导其使用 `/ars-guide` 交互式走查。
2. 若用户直接说「新手教程」「怎么用」「guide」等，以 `/ars-guide` 的交互式走查响应：先问用户想做什么（固定选项，遵循「固定选项点选协议」），再按所选场景给出一句可直接复制的示例提示词与简要说明。
3. 不改变既有工作流路由；用户给出具体任务时仍按「工作流路由」正常处理。
```

- [ ] **Step 2: 别名路由表新增 `/ars-guide` 行**

在 `## Claude 风格别名路由` 表末尾（`/ars-full` 行之后）新增：

```markdown
| /ars-guide, ars-guide | codex/commands/ars-guide.md | 新手交互式引导（不进入具体工作流） |
```

- [ ] **Step 3: 新增 `/ars-guide` 命令配方**

新建 `codex/commands/ars-guide.md`，按设计规格配方：

- 欢迎一行 → 用固定选项问「你现在最想先做哪件事？」（Plan 模式弹卡片/否则编号）：深度研究 / 写论文 / 论文评审 / 文献综述 / 完整管线 / 只想先了解。
- 按所选场景给一句可直接复制的示例提示词 + 一行说明触发哪个工作流。
- 再问「要不要现在试试？」（固定选项：现在试 / 换场景 / 结束）→ 引导继续或收尾推荐教程。
- 全程遵守「专业术语通俗解释」与「固定选项点选协议」。

- [ ] **Step 4: 同步双副本（整体复制 `skills/academic-research-suite/` → 插件副本）**

```powershell
Copy-Item -Path "G:\academic-research-skills-codex-zh.worktrees\beginner-guide\skills\academic-research-suite\*" -Destination "G:\academic-research-skills-codex-zh.worktrees\beginner-guide\plugins\ars-codex-zh\skills\academic-research-suite\" -Recurse -Force
```

- [ ] **Step 5: 双副本逐字节校验（guard 覆盖）+ 刷新基线**

```powershell
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: 双副本一致、`--check` GREEN。新文件 `codex/commands/ars-guide.md` 已登记基线。

- [ ] **Step 6: 提交 Task 2**

```powershell
git add -A
git commit -m "feat: add beginner guide section and interactive /ars-guide command"
```

---

### Task 3: 版本联动 `0.4.0` + CHANGELOG

**Files:**
- Modify: `VERSION`、`skills/academic-research-suite/SKILL.md` 的 `metadata.version`、`skills/academic-research-suite/manifest.json` 的 `adapter_version`、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version`、`plugins/ars-codex-zh/skills/academic-research-suite/manifest.json` 的 `adapter_version`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: 铁律 3 版本一致性 + 语义化版本（MINOR = 行为改动）。
- Produces: 四处版本 `0.4.0` 一致 + CHANGELOG 归档。

- [ ] **Step 1: 四处版本同步 `0.3.0 → 0.4.0`**

用 `rg -n "0\.3\.0"` 全仓定位后逐一更新（注意 `metadata.version`、`adapter_version`、`plugin.json version`、`VERSION`）。插件副本 `plugins/ars-codex-zh/skills/.../manifest.json` 与源一致；`plugins/ars-codex-zh/.codex-plugin/plugin.json` 单独更新。

- [ ] **Step 2: CHANGELOG 归档**

`## [0.4.0] - 2026-08-27`，`### What's Changed` 下记录：新手教程文档、README 入口、SKILL.md「新手引导」小节、`/ars-guide` 交互式引导命令；新建空 `Unreleased` 段。

- [ ] **Step 3: 同步双副本（manifest 变更后整体复制）+ guard 刷新**

```powershell
Copy-Item -Path "G:\academic-research-skills-codex-zh.worktrees\beginner-guide\skills\academic-research-suite\*" -Destination "G:\academic-research-skills-codex-zh.worktrees\beginner-guide\plugins\ars-codex-zh\skills\academic-research-suite\" -Recurse -Force
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: 双副本一致、四处版本 `0.4.0`、`--check` GREEN。

- [ ] **Step 4: 提交 Task 3**

```powershell
git add -A
git commit -m "chore: bump package version to 0.4.0 for beginner guide feature"
```

---

### Task 4: 全量验证门

**Files:** 无（只运行校验）。

**Interfaces:**
- Consumes: Task 1-3 的全部改动。
- Produces: GREEN 证明。

- [ ] **Step 1: guard `--check`（必须退出码 0）**

```powershell
python scripts/verify_localization_guard.py --check
```

Expected: 退出码 0、无 `[DRIFT]` 报错、双副本逐字节一致、受保护文件与基线一致。

- [ ] **Step 2: pytest 门禁（不新增失败）**

```powershell
python -m pytest skills/academic-research-suite/codex/tests
```

Expected: 43 passed / 6 既有失败（`test_quality_gates_all_pass` + 5 个 `test_topology_experiment`），无新增失败。

- [ ] **Step 3: 版本四处一致性冒烟**

```powershell
rg -n "0\.3\.0" "G:\academic-research-skills-codex-zh.worktrees\beginner-guide" --glob "!docs/**" --glob "!GETTING_STARTED_ZH-CN.md"
```

Expected: 无输出（受保护范围已全部 `0.4.0`）。

- [ ] **Step 4: 收尾提交（如有遗留，无则跳过）**

```powershell
git status
```

Expected: clean；若 dirty 则补充提交。

---

### Task 5: 合并回 `main` + tag + 清理

**Files:** 无（纯 git 操作）。

**Interfaces:**
- Consumes: `codex/beginner-guide` 分支的 Task 1-4 成果。
- Produces: `main` 上的合并提交 + tag `v0.4.0` + worktree 清理。

- [ ] **Step 1: 回到 `main` 并合并（--no-ff）**

```powershell
git -C "G:\academic-research-skills-codex-zh" merge --no-ff codex/beginner-guide -m "Merge branch 'codex/beginner-guide': beginner guide and interactive on-ramp"
```

- [ ] **Step 2: `main` 上再跑一遍 guard `--check` + pytest**

```powershell
python scripts/verify_localization_guard.py --check
python -m pytest skills/academic-research-suite/codex/tests
```

Expected: guard GREEN；pytest 不新增失败。

- [ ] **Step 3: 打 tag `v0.4.0`**

```powershell
git tag v0.4.0
```

- [ ] **Step 4: 清理 worktree 与分支**

```powershell
git -C "G:\academic-research-skills-codex-zh" worktree remove "G:\academic-research-skills-codex-zh.worktrees\beginner-guide"
git -C "G:\academic-research-skills-codex-zh" branch -d codex/beginner-guide
git -C "G:\academic-research-skills-codex-zh" worktree prune
git -C "G:\academic-research-skills-codex-zh" worktree list
```

Expected: 只剩 `main` 一个 worktree；分支已删除。

---

### Task 6: 插件缓存同步 `0.4.0` + 重启验收

**Files:**
- Modify: 插件缓存 `C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\0.4.0\`（从仓库 `plugins/ars-codex-zh/` 同步）

**Interfaces:**
- Consumes: `main` 合并后的插件目录 `plugins/ars-codex-zh/`。
- Produces: 用户重启 Codex app 后可安装/加载 v0.4.0 插件。

- [ ] **Step 1: 同步插件缓存**

将 `plugins/ars-codex-zh/` 整体复制到缓存 `...\0.4.0\`（参照上次 v0.3.0 的做法，先确认缓存路径结构）。

- [ ] **Step 2: 提示用户重启验收**

重启 Codex app → 确认插件版本 `0.4.0`、`/ars-guide` 可用、教程引用生效。真实验证受限，最终以用户人工确认为准。

---

## Definition of Done

- [ ] `GETTING_STARTED_ZH-CN.md` 存在且内容完整（7 章）。
- [ ] `README_ZH-CN.md` 顶部有教程入口 + 徽章 `v0.4.0`。
- [ ] `SKILL.md` 含「新手引导」小节 + 别名路由 `/ars-guide` 行。
- [ ] `codex/commands/ars-guide.md` 存在（双副本逐字节一致）。
- [ ] 版本四处一致 `0.4.0`；`CHANGELOG.md` 归档 `0.4.0`。
- [ ] guard `--update` 后 `--check` 退出码 0；pytest 不新增失败。
- [ ] 已合并回 `main`、tag `v0.4.0`、worktree 清理完毕。
- [ ] 插件缓存已同步 `0.4.0`，等待用户重启验收。
