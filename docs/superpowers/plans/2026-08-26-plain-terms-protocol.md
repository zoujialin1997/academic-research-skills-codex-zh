# 专业术语通俗解释协议（Plain-Language Terms Protocol）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 ARS-Codex 中文版新增「专业术语通俗解释协议」：面向用户的所有输出中，专业术语首次出现时用括号附一句大白话解释（纯指令、不建术语表）；并将包版本升至 `0.3.0`（MINOR）。

**Architecture:** 通过修改适配层入口 `skills/academic-research-suite/SKILL.md`（受保护文件）新增「专业术语通俗解释」小节（纯指令），使会话级指令自动覆盖 `ars/` 内所有工作流与命令的面向用户输出（不改动 `ars/`）。同步双副本 `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（逐字节一致），并同步四处包版本号与 `CHANGELOG.md`。所有改动在 `codex/plain-terms` 分支 + worktree 完成，验证后合并回 `main`。

**Tech Stack:** Markdown（SKILL.md）、JSON（manifest.json / plugin.json）、Python 防护脚本 `scripts/verify_localization_guard.py`、pytest（`skills/academic-research-suite/codex/tests`）、git worktree。

## Global Constraints

- **验证纪律（本计划的 RED-GREEN）**：本改动是 Markdown/配置变更，无新增代码，因此不写单元测试；RED-GREEN 由仓库防护脚本承担：
  - 编辑受保护文件后 `python scripts/verify_localization_guard.py --check` 必须 FAIL（RED）；`--update` 记录新基线后 `--check` 必须 PASS（GREEN）。
  - 双副本逐字节一致由 guard 强制（`skills/academic-research-suite/` vs `plugins/ars-codex-zh/skills/`）。
- **pytest 基线**：`python -m pytest skills/academic-research-suite/codex/tests` 预期 43 passed / 6 个既有失败（`test_quality_gates_all_pass` + 5 个 `test_topology_experiment`），这些失败与本次改动无关、禁止修复；门禁是「不新增失败」。
- **铁律**：禁止编辑 `skills/academic-research-suite/ars/` 任何文件；禁止修改 `ars/` 内 references / templates / agent 提示词。
- **版本一致性**：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version` 必须全部为 `0.3.0`。
- **环境**：Windows + PowerShell；文本搜索优先 `rg`；codex CLI 不可用（WindowsApps 打包版拒绝访问），真实验证受限，以 guard + pytest + 文本一致性为准。
- **文件操作铁律（本仓库执行教训）**：所有 .NET 文件读写（`[System.IO.File]::ReadAllText/WriteAllText`、`Get-FileHash`）一律使用**绝对路径**；PowerShell 复制用 `Copy-Item -Path "<abs>\*"`（通配符需 `-Path` 而非 `-LiteralPath`）。
- **提交流程**：所有适配层改动在 `codex/plain-terms` 分支 + worktree 完成，验证通过后合并回 `main`；设计/计划文档直接在 `main` 提交。

---

### Task 0: 建立 `codex/plain-terms` worktree

**Files:** 无（纯 git 操作，在 `main` 工作区 `G:\academic-research-skills-codex-zh` 执行）

**Interfaces:**
- Consumes: `main` 当前 HEAD = `7b14d1a`（含设计规格）。
- Produces: 新 worktree `G:\academic-research-skills-codex-zh.worktrees\plain-terms`（分支 `codex/plain-terms`），后续所有任务在此 worktree 内执行。

- [ ] **Step 1: 创建分支 + worktree**

```powershell
git -C "G:\academic-research-skills-codex-zh" worktree add -b codex/plain-terms "G:\academic-research-skills-codex-zh.worktrees\plain-terms" main
```

- [ ] **Step 2: 验证 worktree 状态**

```powershell
git -C "G:\academic-research-skills-codex-zh.worktrees\plain-terms" status
git -C "G:\academic-research-skills-codex-zh.worktrees\plain-terms" log --oneline -1
```

Expected: `On branch codex/plain-terms`、clean、HEAD = `7b14d1a docs: add plain-language terms protocol design spec`。

- [ ] **Step 3: 提交（无文件改动）**

无需 commit；直接进入 Task 1。

---

### Task 1: `SKILL.md` 新增「专业术语通俗解释」小节 + metadata.version（双副本）

**Files:**
- Modify: `skills/academic-research-suite/SKILL.md`（worktree 下绝对路径：`G:\academic-research-skills-codex-zh.worktrees\plain-terms\skills\academic-research-suite\SKILL.md`）
- Modify: `plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md`（双副本，逐字节一致）

**Interfaces:**
- Consumes: 无前置任务产物（worktree 已就绪）。
- Produces: SKILL.md 中新增的「专业术语通俗解释」小节——模型侧行为契约（面向用户输出的术语首次出现加括号通俗解释）。

- [ ] **Step 1: 在源 SKILL.md 中新增「专业术语通俗解释」小节**

插入位置：紧邻「固定选项点选协议」小节（第 209 行）之后、`## 安全边界`（第 211 行）之前。

用绝对路径读取并替换（插入前检查目标 marker 存在）：

```powershell
$src = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\skills\academic-research-suite\SKILL.md"
$nl = "`r`n"
$text = [System.IO.File]::ReadAllText($src)
$section = '## 专业术语通俗解释' + $nl + $nl +
  '面向用户的所有输出（路由说明、工作流提问、模式选择、报告/评审输出）中，遇到专业术语时按以下方式处理：' + $nl + $nl +
  '1. **首次出现即解释**：同一术语在同一会话中首次出现时，紧跟术语后加括号附一句通俗解释。例如：元分析（把多篇独立研究的结果合并统计，得出更可靠的结论）。' + $nl +
  '2. **保留术语原文**：通俗解释是补充，不替换术语本身；解释用大白话，不超过一句话，且不引入新的专业词汇。' + $nl +
  '3. **跟随会话语言**：中文会话用中文解释，英文/韩文会话用对应语言解释。' + $nl +
  '4. **覆盖所有交互**：面向用户的提问与选项、工作流说明、模式名称、报告与评审结论中的术语都要解释；只供内部使用、用户不会直接看到的输出除外。' + $nl +
  '5. **按需展开**：用户表示仍不理解或要求详细说明时，可展开成一小段通俗说明，但不改变原意、不省略必要信息。'
$marker = $nl + '## 安全边界' + $nl
if (-not $text.Contains($marker)) { throw '安全边界 marker not found' }
$text = $text.Replace($marker, $nl + $section + $nl + $nl + '## 安全边界' + $nl)
[System.IO.File]::WriteAllText($src, $text, (New-Object System.Text.UTF8Encoding($false)))
Write-Output 'section inserted'
```

- [ ] **Step 2: 更新源 SKILL.md 的 `metadata.version` 与版本散文**

将 frontmatter 中的 `  version: "0.2.0"` 改为 `  version: "0.3.0"`；将「本 Codex 包版本为 `0.2.0`」改为「本 Codex 包版本为 `0.3.0`」。

```powershell
$text = [System.IO.File]::ReadAllText($src)
$text = $text.Replace('  version: "0.2.0"', '  version: "0.3.0"')
$text = $text.Replace('本 Codex 包版本为 `0.2.0`', '本 Codex 包版本为 `0.3.0`')
[System.IO.File]::WriteAllText($src, $text, (New-Object System.Text.UTF8Encoding($false)))
Write-Output 'version updated'
```

- [ ] **Step 3: 同步双副本（逐字节一致）**

```powershell
$src = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\skills\academic-research-suite\SKILL.md"
$dst = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\plugins\ars-codex-zh\skills\academic-research-suite\SKILL.md"
Copy-Item -LiteralPath $src -Destination $dst -Force
```

- [ ] **Step 4: 验证双副本逐字节一致**

```powershell
$h1 = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
$h2 = (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash
"IDENTICAL=$($h1 -eq $h2)"
```

Expected: `IDENTICAL=True`。

- [ ] **Step 5: 验证协议内容落位（两份都应有）**

```powershell
rg -n "专业术语通俗解释|首次出现即解释" "$src"
rg -n "专业术语通俗解释|首次出现即解释" "$dst"
rg -n 'version: "0\.3\.0"|本 Codex 包版本为 `0\.3\.0`' "$src"
```

Expected: 每份都能命中小节标题与规则；metadata.version 与版本散文为 `0.3.0`。

- [ ] **Step 6: RED 验证 —— guard 应检测到受保护文件变更**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\plain-terms"
python scripts/verify_localization_guard.py --check
```

Expected: 退出码非 0，输出包含 `[FAIL] protected file changed: skills/academic-research-suite/SKILL.md`（RED 成立）。

- [ ] **Step 7: GREEN 验证 —— 刷新基线后 guard 通过**

```powershell
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: `--check` 退出码 0、输出 `[OK]`。

- [ ] **Step 8: 提交**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\plain-terms"
git add skills/academic-research-suite/SKILL.md plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md scripts/localization_guard.manifest.json scripts/upstream_baseline.json
git commit -m "feat: add plain-language terms protocol to SKILL.md router"
```

---

### Task 2: 包版本 `0.3.0` 联动 + CHANGELOG

**Files:**
- Modify: `VERSION`
- Modify: `skills/academic-research-suite/manifest.json`（`adapter_version`）
- Modify: `plugins/ars-codex-zh/skills/academic-research-suite/manifest.json`（双副本）
- Modify: `plugins/ars-codex-zh/.codex-plugin/plugin.json`（`version`）
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1 已更新 `SKILL.md` 的 `metadata.version` 为 `0.3.0`。
- Produces: 四处包版本号一致为 `0.3.0`；CHANGELOG 归档 `[0.3.0] - 2026-08-26` 并新建空 `Unreleased`。

- [ ] **Step 1: 更新 `VERSION`（保留 CRLF 结尾）**

```powershell
$v = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\VERSION"
[System.IO.File]::WriteAllText($v, "0.3.0`r`n", (New-Object System.Text.UTF8Encoding($false)))
```

- [ ] **Step 2: 更新 `manifest.json` 的 `adapter_version`（源 + 插件副本）**

将两份 `manifest.json` 中的 `"adapter_version": "0.2.0",` 逐字改为 `"adapter_version": "0.3.0",`（保留其余 JSON 结构与缩进），再同步副本：

```powershell
$m1 = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\skills\academic-research-suite\manifest.json"
$m2 = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\plugins\ars-codex-zh\skills\academic-research-suite\manifest.json"
$mt = [System.IO.File]::ReadAllText($m1)
if (-not $mt.Contains('"adapter_version": "0.2.0",')) { throw 'adapter_version not found' }
$mt = $mt.Replace('"adapter_version": "0.2.0",', '"adapter_version": "0.3.0",')
[System.IO.File]::WriteAllText($m1, $mt, (New-Object System.Text.UTF8Encoding($false)))
Copy-Item -LiteralPath $m1 -Destination $m2 -Force
```

- [ ] **Step 3: 更新 `plugin.json` 的 `version`**

将 `plugins\ars-codex-zh\.codex-plugin\plugin.json` 中的 `"version": "0.2.0",` 改为 `"version": "0.3.0",`：

```powershell
$pj = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\plugins\ars-codex-zh\.codex-plugin\plugin.json"
$pt = [System.IO.File]::ReadAllText($pj)
if (-not $pt.Contains('"version": "0.2.0",')) { throw 'plugin version not found' }
$pt = $pt.Replace('"version": "0.2.0",', '"version": "0.3.0",')
[System.IO.File]::WriteAllText($pj, $pt, (New-Object System.Text.UTF8Encoding($false)))
```

- [ ] **Step 4: 更新 `CHANGELOG.md`**

将当前：

```
## Unreleased

## [0.2.0] - 2026-08-26
```

替换为：

```
## Unreleased

## [0.3.0] - 2026-08-26

### What's Changed
- Added the plain-language terms protocol to the `SKILL.md` router:
  user-facing output now explains specialist terms in plain language on
  first occurrence (kept in parentheses after the original term), following
  the session language; the adaptation layer covers all `ars/` workflows
  without modifying vendored files.
- Bumped the Codex package version to `0.3.0` (MINOR) for the adapter behavior
  change.

## [0.2.0] - 2026-08-26
```

实现（用文件实际换行符构造，CHANGELOG 为 CRLF）：

```powershell
$ch = "G:\academic-research-skills-codex-zh.worktrees\plain-terms\CHANGELOG.md"
$nl = "`r`n"
$ct = [System.IO.File]::ReadAllText($ch)
$oldBlock = '## Unreleased' + $nl + $nl + '## [0.2.0] - 2026-08-26'
$newBlock = '## Unreleased' + $nl + $nl + '## [0.3.0] - 2026-08-26' + $nl + $nl +
  '### What''s Changed' + $nl +
  '- Added the plain-language terms protocol to the `SKILL.md` router:' + $nl +
  '  user-facing output now explains specialist terms in plain language on' + $nl +
  '  first occurrence (kept in parentheses after the original term), following' + $nl +
  '  the session language; the adaptation layer covers all `ars/` workflows' + $nl +
  '  without modifying vendored files.' + $nl +
  '- Bumped the Codex package version to `0.3.0` (MINOR) for the adapter behavior' + $nl +
  '  change.' + $nl + $nl + '## [0.2.0] - 2026-08-26'
if (-not $ct.Contains($oldBlock)) { throw 'CHANGELOG block not found' }
$ct = $ct.Replace($oldBlock, $newBlock)
[System.IO.File]::WriteAllText($ch, $ct, (New-Object System.Text.UTF8Encoding($false)))
```

- [ ] **Step 5: 验证版本一致性**

```powershell
$w = "G:\academic-research-skills-codex-zh.worktrees\plain-terms"
rg -n "0\.2\.0" "$w\VERSION" "$w\skills\academic-research-suite\SKILL.md" "$w\skills\academic-research-suite\manifest.json" "$w\plugins\ars-codex-zh\skills\academic-research-suite\manifest.json" "$w\plugins\ars-codex-zh\.codex-plugin\plugin.json"
Get-Content "$w\VERSION"
```

Expected: 最后一个 rg 无输出（无残留 `0.2.0`）；VERSION=`0.3.0`；SKILL.md metadata.version=`0.3.0`；两份 manifest adapter_version=`0.3.0`；plugin.json version=`0.3.0`。

- [ ] **Step 6: 双副本 + guard 基线刷新**

```powershell
$h1=(Get-FileHash -LiteralPath "$w\skills\academic-research-suite\manifest.json" -Algorithm SHA256).Hash
$h2=(Get-FileHash -LiteralPath "$w\plugins\ars-codex-zh\skills\academic-research-suite\manifest.json" -Algorithm SHA256).Hash
"IDENTICAL=$($h1 -eq $h2)"
cd "$w"
python scripts/verify_localization_guard.py --update
python scripts/verify_localization_guard.py --check
```

Expected: `IDENTICAL=True`；`--check` 退出码 0。

- [ ] **Step 7: 提交**

```powershell
cd "$w"
git add VERSION CHANGELOG.md skills/academic-research-suite/manifest.json plugins/ars-codex-zh/skills/academic-research-suite/manifest.json plugins/ars-codex-zh/.codex-plugin/plugin.json scripts/localization_guard.manifest.json scripts/upstream_baseline.json
git commit -m "chore: bump package version to 0.3.0 for plain-terms feature"
```

---

### Task 3: 全量验证门（guard + pytest + 一致性冒烟）

**Files:** 无（只读验证）

**Interfaces:**
- Consumes: Task 1 + Task 2 的产物。
- Produces: 通过验证的 worktree 状态，可供合并回 `main`。

- [ ] **Step 1: guard 终检**

```powershell
cd "G:\academic-research-skills-codex-zh.worktrees\plain-terms"
python scripts/verify_localization_guard.py --check
```

Expected: 退出码 0，`[OK]`。

- [ ] **Step 2: pytest 回归**

```powershell
python -m pytest skills/academic-research-suite/codex/tests
```

Expected: 43 passed；仅 6 个既有失败（`test_quality_gates_all_pass` + 5 个 `test_topology_experiment`）；不新增任何失败。

- [ ] **Step 3: 一致性冒烟**

```powershell
git status --short
rg -n "专业术语通俗解释" skills/academic-research-suite/SKILL.md plugins/ars-codex-zh/skills/academic-research-suite/SKILL.md
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
- Consumes: Task 3 通过的 `codex/plain-terms` 分支。
- Produces: `main` 更新为功能完成态；`v0.3.0` tag；无残留 worktree。

- [ ] **Step 1: 合并到 `main`**

```powershell
git -C "G:\academic-research-skills-codex-zh" merge codex/plain-terms
```

Expected: 快进合并（main 未移动）。

- [ ] **Step 2: main 上复验（checkout 相对）**

```powershell
cd "G:\academic-research-skills-codex-zh"
python scripts/verify_localization_guard.py --check
python -m pytest skills/academic-research-suite/codex/tests
```

Expected: guard 退出码 0；pytest 43 passed / 6 既有失败，无新增。

- [ ] **Step 3: 打 tag**

```powershell
git -C "G:\academic-research-skills-codex-zh" tag v0.3.0
git -C "G:\academic-research-skills-codex-zh" tag --list "v0.3.0"
```

Expected: `v0.3.0` 存在。

- [ ] **Step 4: 清理 worktree 与分支**

```powershell
git -C "G:\academic-research-skills-codex-zh" worktree remove "G:\academic-research-skills-codex-zh.worktrees\plain-terms"
git -C "G:\academic-research-skills-codex-zh" branch -d codex/plain-terms
git -C "G:\academic-research-skills-codex-zh" worktree prune
git -C "G:\academic-research-skills-codex-zh" worktree list
```

Expected: `worktree list` 仅显示 `G:/academic-research-skills-codex-zh [main]`。

---

### Task 5: 同步已安装插件缓存 + 用户重启生效（部署）

**Files:** `C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\` 下的缓存目录（仓库外）

**Interfaces:**
- Consumes: `main` 上已合并的 `plugins/ars-codex-zh`（version `0.3.0`）。
- Produces: app 重启后加载 `0.3.0` 插件。

- [ ] **Step 1: 创建 `0.3.0` 缓存副本（逐字节一致）**

```powershell
$repoPlugin = "G:\academic-research-skills-codex-zh\plugins\ars-codex-zh"
$newCache = "C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\0.3.0"
New-Item -ItemType Directory -Force -Path $newCache | Out-Null
Copy-Item -Path "$repoPlugin\*" -Destination $newCache -Recurse -Force
```

注意：通配符复制必须用 `-Path`（`-LiteralPath` 会把 `*` 当字面路径）。

- [ ] **Step 2: 校验缓存与仓库逐字节一致**

```powershell
$mismatch=0; $count=0
foreach ($f in (Get-ChildItem -LiteralPath $repoPlugin -Recurse -File)) {
  $rel = $f.FullName.Substring($repoPlugin.Length).TrimStart([char]92)
  $dst = Join-Path $newCache $rel
  if (-not (Test-Path -LiteralPath $dst)) { Write-Output "MISSING: $rel"; $mismatch++ }
  elseif ((Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash) { Write-Output "MISMATCH: $rel"; $mismatch++ }
  $count++
}
Write-Output "compared $count files, mismatches=$mismatch"
```

Expected: `compared 2385 files, mismatches=0`。

- [ ] **Step 3: 退役旧缓存（可选）**

历史遗留的 `0.1.27`、`0.2.0` 缓存目录可手动清理（删除路径位于 `C:\Users\Administrator\.codex\plugins\cache\ars-codex-zh\ars-codex-zh\` 下，需人工确认后删除；系统策略可能拦截仓库外递归删除）。

- [ ] **Step 4: 用户重启 Codex app 并人工验收**

请用户重启 Codex 桌面应用（`0.3.0` 插件加载）。验收：
1. 中文会话中，Socratic 模式路由、模式选择、报告/评审输出里专业术语首次出现带括号通俗解释。
2. 术语原文保留、解释为一句大白话。
3. 英文/韩文会话用对应语言解释。
