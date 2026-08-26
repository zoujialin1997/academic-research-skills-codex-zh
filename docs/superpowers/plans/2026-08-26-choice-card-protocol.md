# 固定选项点选协议（Choice-Card Protocol）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 ARS-Codex 中文版新增「固定选项点选协议」：Plan 模式下 2-3 个固定选项的单选提问弹出点选卡片（`request_user_input`），其余情况降级为「编号列表 + 回复数字」；并将包版本升至 `0.2.0`（MINOR）。

**Architecture:** 通过修改适配层入口 `skills/academic-research-suite/SKILL.md`（受保护文件）新增全局协议小节并更新 `AskUserQuestion` 运行时映射行，使会话级指令自动覆盖 `ars/` 内所有工作流的固定选项提问（不改动 `ars/`）。同步双副本 `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（逐字节一致），并同步四处包版本号与 `CHANGELOG.md`。所有改动在 `codex/choice-card` 分支 + worktree 完成，验证后合并回 `main`。

**Tech Stack:** Markdown（SKILL.md）、JSON（manifest.json / plugin.json）、Python 防护脚本 `scripts/verify_localization_guard.py`、pytest（`skills/academic-research-suite/codex/tests`）、git worktree。

## Global Constraints

- **验证纪律（本计划的 RED-GREEN）**：本改动是 Markdown/配置变更，无新增代码，因此不写单元测试；RED-GREEN 由仓库防护脚本承担：
  - 编辑受保护文件后 `python scripts/verify_localization_guard.py --check` 必须 FAIL（RED）；`--update` 记录新基线后 `--check` 必须 PASS（GREEN）。
  - 双副本逐字节一致由 guard 强制（`skills/academic-research-suite/` vs `plugins/ars-codex-zh/skills/`）。
- **pytest 基线**：`python -m pytest skills/academic-research-suite/codex/tests` 预期 43 passed / 6 个既有失败（`test_quality_gates_all_pass` + 5 个 `test_topology_experiment`），这些失败与本次改动无关、禁止修复；门禁是「不新增失败」。
- **铁律**：禁止编辑 `skills/academic-research-suite/ars/` 任何文件；禁止修改 `ars/` 内 references / templates / agent 提示词。
- **版本一致性**：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version` 必须全部为 `0.2.0`（plugin.json 的 `version` 是 app 展示的包版本，随包版本联动）。
- **环境**：Windows + PowerShell；文本搜索优先 `rg`；codex CLI 不可用（WindowsApps 打包版拒绝访问），真实验证受限，以 guard + pytest + 文本一致性为准。
- **提交流程**：所有适配层改动在 `codex/choice-card` 分支 + worktree 完成，验证通过后合并回 `main`；设计/计划文档直接在 `main` 提交。

---

### Task 0: 建立 `codex/choice-card` worktree

**Files:** 无（纯 git 操作，在 `main` 工作区 `G:\academic-research-skills-codex-zh` 执行）

**Interfaces:**
- Consumes: `main` 当前 HEAD = `3f8a8d2`（含设计规格）。
- Produces: 新 worktree `G:\academic-research-skills-codex-zh.worktrees\choice-card`（分支 `codex/choice-card`），后续所有任务在此 worktree 内执行。

- [ ] **Step 1: 创建分支 + worktree**

```powershell
git -C "G:\academic-research-skills-codex-zh" worktree add -b codex/choice-card "G:\academic-research-skills-codex-zh.worktrees\choice-card" main
```

- [ ] **Step 2: 验证 worktree 状态**

```powershell
git -C "G:\academic-research-skills-codex-zh.worktrees\choice-card" status
git -C "G:\academic-research-skills-codex-zh.worktrees\choice-card" log --oneline -1
```

Expected: `On branch codex/choice-card`、clean、HEAD = `3f8a8d2 docs: add fixed-option choice-card protocol design spec`。

- [ ] **Step 3: 提交（无文件改动，仅确认）**

无需 commit；直接进入 Task 1。

---

### Task 1: `SKILL.md` 新增协议 + 更新 AskUserQuestion 映射 + metadata.version（双副本）

**Files:**
- Modify: `skills/academic-research-suite/SKILL.md`（在 worktree 路径下）
- Modify: `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（双副本，逐字节一致）

**Interfaces:**
- Consumes: 无前置任务产物（worktree 已就绪）。
- Produces: SKILL.md 中新增的「固定选项点选协议」小节与新的 `AskUserQuestion` 映射行——这是后续所有任务验证的协议契约（模型侧行为：2-3 选项单选 → Plan 模式弹卡片，否则编号列表）。

- [ ] **Step 1: 在源 SKILL.md 中替换 `AskUserQuestion` 映射行**

文件：`skills\academic-research-suite\SKILL.md`，位于「## Codex 运行时映射」表格内。

将：

```
| AskUserQuestion | 提出简明澄清问题，或当当前模式可用时使用 Codex 的结构化用户输入工具。 |
```

替换为：

```
| AskUserQuestion | 提出简明澄清问题；固定选项单选提问遵循「固定选项点选协议」：Plan 模式弹点选卡片，否则编号列表。 |
```

- [ ] **Step 2: 在源 SKILL.md 中新增「固定选项点选协议」小节**

插入位置：紧邻 `## 安全边界` 之前（即在「ARS v3.21.1 契约诚实性边界」小节内容之后、`## 安全边界` 标题之前）。

插入的完整内容：

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

- [ ] **Step 3: 更新源 SKILL.md 的 `metadata.version`**

将 frontmatter 中的 `  version: "0.1.27"` 改为 `  version: "0.2.0"`。

- [ ] **Step 4: 同步双副本（逐字节一致）**

```powershell
$src = "G:\academic-research-skills-codex-zh.worktrees\choice-card\skills\academic-research-suite\SKILL.md"
$dst = "G:\academic-research-skills-codex-zh.worktrees\choice-card\plugins\ars-codex-zh\skills\academic-research-suite\SKILL.md"
Copy-Item -LiteralPath $src -Destination $dst -Force
```

- [ ] **Step 5: 验证双副本逐字节一致**

```powershell
$h1 = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
$h2 = (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash
"$h1"; "$h2"; if ($h1 -eq $h2) { "IDENTICAL" } else { "MISMATCH" }
```

Expected: 两次哈希相同、输出 `IDENTICAL`。

- [ ] **Step 6: 验证协议内容落位（两份都应有）**

```powershell
rg -n "固定选项点选协议|Plan 模式弹点选卡片" "G:\academic-research-skills-codex-zh.worktrees\choice-card\skills\academic-research-suite\SKILL.md"
rg -n "固定选项点选协议|Plan 模式弹点选卡片" "G:\academic-research-skills-codex-zh.worktrees\choice-card\plugins\ars-codex-zh\skills\academic-research-suite\SKILL.md"
rg -n 'version: "0.2.0"' "G:\academic-research-skills-codex-zh.worktrees\choice-card\skills\academic-research-suite\SKILL.md"
```

Expected: 每份都能命中协议标题与映射行；metadata.version 为 `0.2.0`。

- [ ] **Step 7: RED 验证 —— guard 应检测到受保护文件变更**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\choice-card"
python scripts/verify_localization_guard.py --check
```

Expected: 退出码非 0，输出包含 `[FAIL] protected file changed: skills/academic-research-suite/SKILL.md` 或双副本哈希变化（RED 成立）。

- [ ] **Step 8: GREEN 验证 —— 刷新基线后 guard 通过**

```powershell
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: `--update` 写入新基线（含 SKILL.md 新哈希）；`--check` 退出码 0、输出 `[OK]`。

- [ ] **Step 9: 提交**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\choice-card"
git add skills/academic-research-suite/SKILL.md plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md scripts/localization_guard.manifest.json scripts/upstream_baseline.json
git commit -m "feat: add fixed-option choice-card protocol to SKILL.md router"
```

---

### Task 2: 包版本 `0.2.0` 联动 + CHANGELOG

**Files:**
- Modify: `VERSION`
- Modify: `skills/academic-research-suite/manifest.json`（`adapter_version`）
- Modify: `plugins/ars-codex-zh/skills/academic-research-suite/manifest.json`（双副本）
- Modify: `plugins/ars-codex-zh/.codex-plugin/plugin.json`（`version`）
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1 已更新 `SKILL.md` 的 `metadata.version` 为 `0.2.0`。
- Produces: 四处包版本号一致为 `0.2.0`；CHANGELOG 归档 `[0.2.0] - 2026-08-26` 并新建空 `Unreleased`。

- [ ] **Step 1: 更新 `VERSION`**

```powershell
Set-Content -LiteralPath "G:\academic-research-skills-codex-zh.worktrees\choice-card\VERSION" -Value "0.2.0" -Encoding ASCII
```

- [ ] **Step 2: 更新 `manifest.json` 的 `adapter_version`（源 + 插件副本）**

将两份 `manifest.json` 中的 `"adapter_version": "0.1.27",` 逐字改为 `"adapter_version": "0.2.0",`（保留其余 JSON 结构与缩进），再同步副本：

```powershell
$m1 = "G:\academic-research-skills-codex-zh.worktrees\choice-card\skills\academic-research-suite\manifest.json"
$m2 = "G:\academic-research-skills-codex-zh.worktrees\choice-card\plugins\ars-codex-zh\skills\academic-research-suite\manifest.json"
# 用编辑器把两处的 adapter_version 改为 0.2.0 后：
Copy-Item -LiteralPath $m1 -Destination $m2 -Force
```

- [ ] **Step 3: 更新 `plugin.json` 的 `version`**

将 `plugins\ars-codex-zh\.codex-plugin\plugin.json` 中的 `"version": "0.1.27"` 改为 `"version": "0.2.0"`。

- [ ] **Step 4: 更新 `CHANGELOG.md`**

将当前空的：

```
## Unreleased

## [0.1.27] - 2026-08-24
```

替换为：

```
## Unreleased

## [0.2.0] - 2026-08-26

### What's Changed
- Added the fixed-option choice-card protocol to the `SKILL.md` router:
  single-select questions with 2-3 fixed options render a clickable selection
  card in Plan mode (via `request_user_input`) and fall back to a numbered
  option list elsewhere; the adaptation layer covers questions from `ars/`
  workflows without modifying vendored files.
- Bumped the Codex package version to `0.2.0` (MINOR) for the adapter behavior
  change.

## [0.1.27] - 2026-08-24
```

- [ ] **Step 5: 验证版本一致性**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\choice-card"
Get-Content VERSION
rg -n 'version: "0.2.0"' skills/academic-research-suite/SKILL.md
rg -n 'adapter_version' skills/academic-research-suite/manifest.json plugins/ars-codex-zh/skills/academic-research-suite/manifest.json
rg -n '"version"' plugins/ars-codex-zh/.codex-plugin/plugin.json
rg -n "0\.1\.27" VERSION skills/academic-research-suite/SKILL.md skills/academic-research-suite/manifest.json plugins/ars-codex-zh/.codex-plugin/plugin.json
```

Expected: VERSION=`0.2.0`；SKILL.md metadata.version=`0.2.0`；两份 manifest adapter_version=`0.2.0`；plugin.json version=`0.2.0`；最后一个 rg 无输出（无残留 `0.1.27`）。

- [ ] **Step 6: 双副本 + guard 基线刷新**

```powershell
$h1 = (Get-FileHash -LiteralPath "skills\academic-research-suite\manifest.json" -Algorithm SHA256).Hash
$h2 = (Get-FileHash -LiteralPath "plugins\ars-codex-zh\skills\academic-research-suite\manifest.json" -Algorithm SHA256).Hash
if ($h1 -eq $h2) { "IDENTICAL" } else { "MISMATCH" }
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: `IDENTICAL`；`--check` 退出码 0。

- [ ] **Step 7: 提交**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\choice-card"
git add VERSION CHANGELOG.md skills/academic-research-suite/manifest.json plugins/ars-codex-zh/skills/academic-research-suite/manifest.json plugins/ars-codex-zh/.codex-plugin/plugin.json scripts/localization_guard.manifest.json scripts/upstream_baseline.json
git commit -m "chore: bump package version to 0.2.0 for choice-card feature"
```

---

### Task 3: 全量验证门（guard + pytest + 一致性冒烟）

**Files:** 无（只读验证）

**Interfaces:**
- Consumes: Task 1 + Task 2 的产物。
- Produces: 通过验证的 worktree 状态，可供合并回 `main`。

- [ ] **Step 1: guard 终检**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\choice-card"
python scripts/verify_localization_guard.py --check
```

Expected: 退出码 0，`[OK]`（受保护文件 + 双副本一致、上游锁定不变）。

- [ ] **Step 2: pytest 回归**

```powershell
python -m pytest skills/academic-research-suite/codex/tests
```

Expected: 43 passed；仅 6 个既有失败（`test_quality_gates_all_pass` + 5 个 `test_topology_experiment`）；不新增任何失败。

- [ ] **Step 3: 一致性冒烟**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\choice-card"
git status --short
rg -n "固定选项点选协议" skills/academic-research-suite/SKILL.md plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md
git diff --stat HEAD
```

Expected: worktree clean；两份 SKILL.md 均有协议小节；`git diff --stat HEAD` 为空（已全部提交）。

- [ ] **Step 4: 确认无遗漏改动**

```powershell
git log --oneline -3
```

Expected: 最新两条为 Task 1、Task 2 的提交。

---

### Task 4: 合并回 `main` + tag + 清理 worktree

**Files:** 无（在 `main` 工作区 `G:\academic-research-skills-codex-zh` 执行）

**Interfaces:**
- Consumes: Task 3 通过的 `codex/choice-card` 分支。
- Produces: `main` 更新为功能完成态；`v0.2.0` tag；无残留 worktree。

- [ ] **Step 1: 合并到 `main`**

```powershell
git -C "G:\academic-research-skills-codex-zh" merge codex/choice-card
```

Expected: 快进合并（main 未移动），`git -C "G:\academic-research-skills-codex-zh" log --oneline -3` 显示合并提交。

- [ ] **Step 2: main 上复验（checkout 相对）**

```powershell
cd "G:\academic-research-skills-codex-zh"
python scripts/verify_localization_guard.py --check
python -m pytest skills/academic-research-suite/codex/tests
```

Expected: guard 退出码 0；pytest 43 passed / 6 既有失败，无新增。

- [ ] **Step 3: 打 tag**

```powershell
git -C "G:\academic-research-skills-codex-zh" tag v0.2.0
git -C "G:\academic-research-skills-codex-zh" tag --list "v0.2.0"
```

Expected: `v0.2.0` 存在。

- [ ] **Step 4: 清理 worktree 与分支**

```powershell
git -C "G:\academic-research-skills-codex-zh" worktree remove "G:\academic-research-skills-codex-zh.worktrees\choice-card"
git -C "G:\academic-research-skills-codex-zh" branch -d codex/choice-card
git -C "G:\academic-research-skills-codex-zh" worktree prune
git -C "G:\academic-research-skills-codex-zh" worktree list
```

Expected: `worktree list` 仅显示 `G:/academic-research-skills-codex-zh [main]`。

---

### Task 5: 同步已安装插件缓存 + 用户重启生效（部署）

**Files:** `C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\` 下的缓存目录（仓库外）

**Interfaces:**
- Consumes: `main` 上已合并的 `plugins/ars-codex-zh`（version `0.2.0`）。
- Produces: app 重启后加载 `0.2.0` 插件；旧 `0.1.27` 缓存退役。

- [ ] **Step 1: 创建 `0.2.0` 缓存副本（逐字节一致）**

```powershell
$repoPlugin = "G:\academic-research-skills-codex-zh\plugins\ars-codex-zh"
$newCache = "C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\0.2.0"
New-Item -ItemType Directory -Force -Path $newCache | Out-Null
Copy-Item -LiteralPath (Join-Path $repoPlugin "*") -Destination $newCache -Recurse -Force
```

- [ ] **Step 2: 校验缓存与仓库逐字节一致**

```powershell
$r = Get-ChildItem -LiteralPath $repoPlugin -Recurse -File | ForEach-Object { [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.IO.File]::ReadAllBytes($_.FullName)) }
# 对照 $newCache 下同名文件哈希，全部一致才算通过；也可用：
git -C "G:\academic-research-skills-codex-zh" status --porcelain plugins/ars-codex-zh
```

Expected: 缓存文件与仓库 `plugins/ars-codex-zh` 哈希一致。

- [ ] **Step 3: 退役旧缓存 `0.1.27`（可选但推荐）**

先确认目标路径绝对路径在缓存目录内：

```powershell
$oldCache = "C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\0.1.27"
(Resolve-Path -LiteralPath $oldCache).Path
```

Expected: 解析后的绝对路径以 `C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\` 开头，确认后删除该目录（仅删除 `0.1.27` 目录本身）。

- [ ] **Step 4: 用户重启 Codex app 并人工验收**

请用户重启 Codex 桌面应用（旧插件 `0.1.27` 卸载、`0.2.0` 加载）。验收：
1. 在 Plan 模式下运行任一 ARS 工作流，遇到 2-3 个固定选项的单选提问 → 应弹出点选卡片。
2. 在 Default 模式运行 → 应为「编号列表 + 回复数字」。
3. 4+ 选项（如 reviewer 模式）→ 编号列表降级（预期行为）。
