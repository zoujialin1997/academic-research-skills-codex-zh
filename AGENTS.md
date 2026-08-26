# AGENTS.md

本文件为在此仓库内工作的编码 Agent（Codex / Claude 等）提供约束与约定，范围覆盖仓库根目录下的全部内容。

## 项目是什么

**ARS-Codex 中文适配镜像**（本仓库 `academic-research-skills-codex-zh`）：

- 上游项目：[Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex)（ARS-Codex，Codex 原生学术研究套件）
- 上游 ARS 内容源：[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)（Claude Code 版，被 vendored 内嵌）
- 当前版本：Codex 包 `1.0.1`，内嵌 ARS `v3.21.1`
- 本仓库本质是**同步镜像 + Codex 适配层**，git 历史以 `chore: sync ARS vX @ commit` 这类同步提交为主

## 目录结构

| 路径 | 说明 | 可否修改 |
|---|---|---|
| `skills/academic-research-suite/` | Codex skill 本体，入口为 `SKILL.md` | 适配层可改，`ars/` 除外 |
| `skills/academic-research-suite/SKILL.md` | Codex 路由器，skill 入口 | 适配层，汉化重点 |
| `skills/academic-research-suite/codex/` | Codex 专属适配层（agents / hooks / scripts / tests） | 适配层 |
| `skills/academic-research-suite/ars/` | **上游 vendored 内容**（5 个工作流 + docs / shared / references / templates / agents） | 禁止手工编辑 |
| `plugins/ars-codex-zh/` | 插件打包；其 `skills/` 是 `skills/` 的物化副本（非 symlink） | 与源保持逐字节一致 |
| `examples/` | Codex 平台示例 | 可改 |
| `scripts/` | 本仓库自有工具（非 vendored），如同步防护脚本 | 可改 |
| `README*.md` / `CHANGELOG.md` 等根文档 | 项目文档 | 可改 |

## 铁律

### 1. `ars/` 是上游 vendored 内容，禁止手工编辑
- 整个 `ars/` 来自上游 `academic-research-skills` 与 `experiment-agent` 的 fresh clone 拷贝
- 下次上游同步会**整体覆盖** `ars/`，任何手工改动都会丢失
- 唯一合法的更新方式是执行显式上游 sync（见「同步上游」）
- 涉及 `ars/` 的版本疑问一律以 `manifest.json` 的 `source_repositories[].commit` 锁定版本为准

### 2. 双副本必须保持一致
- `skills/academic-research-suite/` 与 `plugins/ars-codex-zh/skills/` 是同一内容的**两份物化副本**（非 symlink，Windows 兼容需要）
- 任何对 skill 的改动都必须同步到两边，否则插件安装内容会不一致
- 修改后必须验证两边逐字节一致（用防护脚本，见「同步上游」）

### 3. 版本一致性
- `VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version` 四者必须一致（当前 `1.0.1`）
- 这三个值跟踪 **Codex 包版本**，与内嵌 ARS 套件版本（由 `manifest.json` 的 source commit 跟踪）相互独立
- 升级包版本时必须四处同步更新（详见「版本管理」）

### 4. 汉化范围约定
- 汉化只做 **Codex 适配层**：`SKILL.md`、`codex/`、`plugins/ars-codex-zh/.codex-plugin/plugin.json`、`agents/openai.yaml`、`examples/`、根文档（`README_ZH-CN.md` 等）
- `ars/` 内的 references / templates / agent 角色提示词**保留英文原版**：避免与上游 sync 冲突，也避免降低提示词质量
- 中文 README 命名约定：`README_ZH-CN.md`（简体）、`README_ZH-TW.md`（繁体）、`README_JA.md`（日文）、`README.md`（英文）

### 5. 汉化适配层受同步保护（不可被覆盖）
- **同步的写入目标只能是 `skills/academic-research-suite/ars/`**；禁止把上游内容覆盖到 `skills/academic-research-suite/` 顶层或 `plugins/ars-codex-zh/` 的适配层文件上
- 以下「受保护文件」在每次同步后必须与同步前**逐字节一致**（只有有意编辑时才能改）：
  - `skills/academic-research-suite/SKILL.md`
  - `skills/academic-research-suite/agents/openai.yaml`
  - `skills/academic-research-suite/codex/`（整个目录）
  - `plugins/ars-codex-zh/.codex-plugin/plugin.json`
  - `examples/`（整个目录）
  - `README.md`、`README_ZH-CN.md`、`README_ZH-TW.md`、`README_JA.md`、`CHANGELOG.md`
- 用 `scripts/verify_localization_guard.py --check` 强制校验（失败即退出非零，禁止提交）

### 6. 上游改动后必须重新汉化适配
- 同步后，若上游改动了被适配内容所引用的文件，**必须对应地重新汉化适配**，不能只做保护性校验
- 何时触发：防护脚本的 `[DRIFT]` 报告列出「上游变更文件 → 引用它的适配文件」，凡引用关系命中的适配文件都要复查并更新
- 适配层内容来自上游「语义」而非「文本」——上游改了路由/模式/行为，即使适配文件没被物理覆盖，也要跟着改

### 7. 新加功能受同步保护（不可被上游同步直接覆盖）
- 适配层**新增的功能或内容**（如 `SKILL.md` 新增小节、`codex/` 新增文件/命令/参考、插件元数据、根文档新增章节）一律视为「受保护内容」
- 上游同步的写入目标只能是 `skills/academic-research-suite/ars/`（铁律 5）；同步与「重新汉化适配」都**不得直接覆盖、删除或回退**新加功能
- 上游改动命中新功能所引用文件时，按铁律 6 做**语义合并**：保留新功能，只同步适配上游语义变化，禁止回退到上游原版
- 新加的功能性文件若不在既有受保护清单内，必须登记进 `PROTECTED_TREES` 并 `python scripts/verify_localization_guard.py --update` 记录基线
- 包版本号（`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`、`plugin.json` 的 `version`）由人工维护，同步不得静默回退

## 同步上游

同步机制由 `skills/academic-research-suite/manifest.json` 记录（`source_repositories[]`、`generated_date`、`excluded_patterns`、`inactive_upstream_scripts`）。

### 同步边界（受保护内容）

| 内容 | 同步时 |
|---|---|
| `skills/academic-research-suite/ars/` | ✅ 唯一允许被上游整体覆盖的范围 |
| 铁律 5 列出的受保护文件（适配层 + 根文档） | ❌ 必须逐字节保留，绝不能被覆盖 |
| 铁律 7 的「新加功能」（适配层新增内容） | ❌ 不得被同步/重新适配覆盖、删除或回退；上游变更时语义合并 |
| `manifest.json` 的 `source_repositories` / `generated_date` | ⚠️ 同步会合法更新；但 `adapter_version` 需人工维护（铁律 3） |

### 同步流程

每次同步上游更新后，必须完成以下步骤：

1. 用上游 fresh clone 按 `manifest.json` 的 `included_paths` 重新拷贝 `ars/`（同时处理 `experiment-agent`）
2. 遵守 `excluded_patterns`（`.claude/`、`.claude-plugin/`、`docs/superpowers/`、showcase PDF、`*.log` 等）
3. 更新 `manifest.json`：写入新 commit、新 `generated_date`；上游新增脚本若在 Codex 环境不适用，须登记进 `inactive_upstream_scripts` 并说明原因
4. **刷新插件副本**：把整个 `skills/academic-research-suite/` 复制到 `plugins/ars-codex-zh/skills/`（必须整体复制以保留适配层，而不是只复制新的 `ars/`）
5. 校验版本一致性（铁律 3）
6. **重新汉化适配**（铁律 6，核心步骤）：
   - 运行 `python scripts/verify_localization_guard.py --check`，读取 `[DRIFT]` 报告
   - 按下方「重新适配映射表」逐个更新被引用的适配文件
7. 更新根 `CHANGELOG.md`、README，以及 `VERSION`（若包版本提升）
8. **记录新基线**：重新适配全部完成后运行 `python scripts/verify_localization_guard.py --update`（受保护文件 + 上游 ars 快照一起更新）
9. 再次运行 `python scripts/verify_localization_guard.py --check`，退出码必须为 0 才允许提交
10. 运行测试（见下）

**⚠️ 同步后复查**：汉化过的适配层没有被上游覆盖、新加功能未被覆盖或回退、双副本一致、版本号四处一致、重新适配完成、防护脚本通过。

### 重新适配映射表

| 上游变更 | 需要同步汉化适配的内容 |
|---|---|
| `ars/*/WORKFLOW.md` 新增 / 改名 / 路由变化 | `SKILL.md` 路由表、`codex/agents/*.md`、`codex/compatibility-matrix.md`、`codex/full-runtime-manifest.json` |
| `ars/commands/ars-*.md` 变化 | `SKILL.md` 别名路由表（`Claude-Style Alias Router`） |
| `ars/*/agents/*.md` 角色提示变化 | 引用它的 `codex/agents/*.md` 与 `SKILL.md` 映射 |
| 上游版本 / README / 变更说明变化 | `README_ZH-CN.md`、`README_ZH-TW.md`、`README_JA.md`、`CHANGELOG.md`、`VERSION`、`manifest.json` 的 `adapter_version` |
| 上游新增 / 变更脚本（Codex 不适用） | `manifest.json` 的 `inactive_upstream_scripts` 登记原因 |
| 其余 references / templates / docs 内容 | 通常无需汉化（保留英文原版），但需人工确认是否影响适配层语义 |

## Git Worktree 管理

### 原则
- `main` 分支 = 上游同步镜像 + 已合并的适配发布，保持干净可追溯
- 所有功能 / 汉化 / 重新适配工作都在**独立 worktree + 分支**上完成，完成并验证后合并回 `main`
- 上游同步（机械性操作）直接落在 `main`；需要判断或改适配层的内容一律走分支

### 分支命名
- 一律使用 `codex/<topic>` 前缀，例如：
  - `codex/zh-skill-router`（SKILL.md 汉化）
  - `codex/zh-plugin-strings`（plugin.json / openai.yaml 汉化）
  - `codex/re-adapt-v3.22`（同步后重新适配）
- 不直接提交到 `main`，除非是机械性的上游同步提交

### Worktree 规范
- 位置：放在仓库目录之外，建议统一放在 `../academic-research-skills-codex-zh.worktrees/<branch-name>/`
- 一个 worktree 对应一个分支；**同一个受保护文件不要同时在两个 worktree 修改**（双副本一致性容易冲突）
- 防护脚本与测试都是 checkout 相对的，**合并前必须在各自 worktree 内通过**：
  ```powershell
  python scripts/verify_localization_guard.py --check
  python -m pytest skills/academic-research-suite/codex/tests
  ```
- 合并回 `main` 后清理：
  ```powershell
  git worktree remove ../academic-research-skills-codex-zh.worktrees/<branch-name>
  git branch -d <branch-name>
  git worktree prune
  ```
- 定期 `git worktree list` 检查，避免堆积未清理的 worktree

### 同步与 Worktree 配合
- 上游同步在 `main` 上完成（更新 `ars/`、`manifest.json`、插件副本、版本号）
- 重新适配：从最新 `main` 创建 `codex/re-adapt-vX` worktree → 在该 worktree 内完成「重新适配映射表」的更新 → 防护与测试通过 → 合并回 `main`
- 合并前 `main` 上不得残留未完成的适配工作

## 版本管理

### 双版本轴（互相独立）
| 版本 | 位置 | 更新时机 |
|---|---|---|
| **Codex 包版本** | `VERSION` + `SKILL.md` 的 `metadata.version` + `manifest.json` 的 `adapter_version` + `plugin.json` 的 `version`（四处必须一致） | 仅当本仓库自身有变更时 |
| **内嵌 ARS 套件版本** | `manifest.json` 的 `source_repositories[].commit` + `generated_date`（可参考上游 release tag，如 `v3.21.1`） | 仅上游同步时，由上游决定 |

### 语义化版本（针对 Codex 包版本）
- **PATCH**（`0.1.x`）：仅上游同步、纯汉化 / 文档、bugfix——不改适配层行为
- **MINOR**（`0.x.0`）：适配层行为变化——`SKILL.md` 路由改动、新增 workflow / 模式、agent 定义变化、汉化改变了路由行为
- **MAJOR**（`x.0.0`）：破坏性变更——skill 接口 / 契约不兼容

### 版本变更流程
1. 按语义化规则决定新版本号
2. **同一个 commit 内**同步更新四处：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version`
3. 更新 `CHANGELOG.md`：把 `Unreleased` 内容归档为 `## [x.y.z] - <日期>`，再新建空的 `Unreleased` 段
4. 打 tag：`git tag v0.1.28`（与 `VERSION` 一致）
5. `SKILL.md` 是受保护文件，版本变更后必须 `python scripts/verify_localization_guard.py --update` 再 `--check`

### 变更类型与版本影响
| 变更类型 | 版本影响 |
|---|---|
| 仅上游同步（`ars/` 内容更新，适配层未动） | PATCH，或并入下一次发布 |
| 纯汉化 / 文档（不改行为） | PATCH |
| 适配层路由 / 行为改动 | MINOR |
| 汉化但改变路由行为 | MINOR（不是 PATCH） |
| 破坏性契约变更 | MAJOR |

### CHANGELOG 纪律
- 所有用户可见变更在 `Unreleased` 段记录
- 发布时归档并标注日期，格式 `## [x.y.z] - <YYYY-MM-DD>`，变更点写在 `### What's Changed` 下
- 汉化变更同样记录（例如「将 SKILL.md 路由器汉化为简体中文」）

## 测试

- **同步防护校验**（每次同步后、提交前必跑）：
  ```powershell
  python scripts/verify_localization_guard.py --check
  ```
  - 校验受保护文件与 `scripts/localization_guard.manifest.json` 哈希一致
  - 校验 `skills/academic-research-suite/` 与 `plugins/ars-codex-zh/skills/` 逐字节一致
  - 对照 `scripts/upstream_baseline.json` 报告上游漂移（`[DRIFT]`）并列出需重新适配的文件
  - 仅在**重新适配完成后**用 `--update` 重新生成两个清单
- Codex 适配层测试（pytest）：
  ```powershell
  python -m pytest skills/academic-research-suite/codex/tests
  ```
- ARS 套件 CI 测试清单：`ars/scripts/run_ci_pytest_manifest.py`（引用 `ars/scripts/_ci_pytest_manifest.toml`）
- 环境：Windows + PowerShell；文本搜索优先 `rg`

## 工作约定

- 保持改动最小且聚焦，不重构无关代码
- 本仓库是独立发行版，不向任何上游仓库提交改动
- 汉化术语保持与既有中文文档一致（可参考已翻译的 `ars/README.zh-CN.md` 用词）
- 不添加版权/许可证头（除非明确要求）
- 不 `git commit` 或新建分支，除非用户明确要求（本规则例外见「Git Worktree 管理」，即按流程建立分支时需经用户确认）
