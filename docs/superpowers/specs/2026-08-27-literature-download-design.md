# 设计规格：文献检索与全文获取（ars-search / ars-download / ars-read）

- **日期**：2026-08-27
- **状态**：已批准（用户 2026-08-27 确认）
- **目标版本**：Codex 包 `1.1.0`（MINOR）
- **仓库**：`academic-research-skills-codex-zh`
- **分支策略**：`codex/zh-literature` worktree 开发，验证后合并回 `main`

## 背景与动机

用户希望把其另一开源项目 `free-academic-search`（MIT，Node/TS monorepo）的文献下载能力整合进 ARS-Codex-zh。

调研结论：

- 本仓库（v1.0.1）当前**没有**文献检索 / 下载 / 全文读取能力。`ars/scripts/` 内的 arxiv / crossref / openalex / semantic_scholar / chinese_literature 客户端都是「引用核验」用的元数据 lookup，不提供搜索与下载；`pdf_read_preflight.py` 只做本地 PDF 结构校验，不提取全文。
- `free-academic-search` 的核心 `free-academic-core`（MIT，作者同为本仓库维护者）是纯 Node 库：多源搜索（Semantic Scholar / PubMed / arXiv / bioRxiv / medRxiv / DOI-Crossref / Unpaywall）、去重合并、按 DOI / URL 下载 PDF、PDF 文本提取。
- 本仓库适配层是 Python（`codex/scripts/*.py`），SKILL.md 的 `allowed-tools` 白名单只放行 `Bash(uv *)` / `Bash(python *)` / `Bash(python3 *)`，现有脚本纯标准库、零第三方依赖。
- 本机 Python 3.12 已装 pypdf / requests / yaml / jsonschema；`uv` 0.11 在白名单内。

## 目标

1. 为 ARS-Codex-zh 提供原生文献检索、合法下载、全文读取能力。
2. 保持零硬性依赖（标准库 `urllib` + `pypdf` 可选增强），不改 `allowed-tools` 白名单。
3. 遵循下载合法性边界：合法 OA 优先，Sci-Hub 显式可选（默认关）。
4. 与 deep-research 工作流联动，端到端打通「检索 → 下载 → 全文 → 写作」。
5. 遵循仓库治理：双副本逐字节一致、guard 保护、版本 MINOR `1.1.0`。

## 用户确认的决策

1. 整合形态：Python 原生移植到适配层（A）。
2. 能力范围：搜索 + 下载 + 全文读取（C）。
3. 依赖策略：零硬性依赖（A）——`urllib` 做网络，`pypdf` 可用则增强、缺失则降级。
4. 下载边界：合法 OA 优先 + Sci-Hub 显式可选、默认关（B）。
5. 工作流联动：新增命令 + deep-research 工作流联动（A）。
6. 版本：`1.1.0`（MINOR）。

## 前后效果差异

| 场景 | 改动前 | 改动后 |
|---|---|---|
| 找文献 | 无检索命令，靠 WebSearch / 外部技能 | `/ars-search` 多源检索 + 去重合并，返回带 DOI / PDF 链接的条目 |
| 下载 PDF | 无下载能力 | `/ars-download` 按 DOI / URL 下载合法 PDF 落盘 |
| 读全文 | 无全文提取 | `/ars-read` 本地 PDF → 文本，直接供写作 / 引用 |
| 文献综述 | 研究 agent 只能浏览网页与摘要 | deep-research 联动，综述阶段自动检索 + 下载 |
| 运行时要求 | 无 | 无新增（Python 标准库 + 可选 pypdf） |

## 架构与实现

### 新增脚本 `skills/academic-research-suite/codex/scripts/ars_codex_literature.py`

单个 Python 模块：CLI 子命令 + 可导入函数；纯标准库（`urllib.request`、`json`、`xml.etree.ElementTree`、`zlib`），`pypdf` 可选。

CLI 表面：

- `search --query <Q> [--sources arxiv,pubmed,semantic-scholar,biorxiv,medrxiv,crossref] [--max-results N] [--year-from YYYY] [--json|--markdown]`
- `download --doi <DOI> [--allow-scihub] [--out DIR] [--json]`
- `download --url <PDF_URL> [--out DIR] [--json]`
- `read --file <PDF> [--max-chars N] [--json]`

数据源与回退链：

- **搜索**：Semantic Scholar、PubMed（E-utilities）、arXiv（Atom XML）、bioRxiv / medRxiv（api.biorxiv.org）、Crossref（DOI / works）。统一归一化为 Paper 结构，按 DOI / arXiv ID / 归一化标题去重合并。
- **下载回退链**：`直接 / arXiv OA → Unpaywall 合法 OA → (仅 --allow-scihub) Sci-Hub`。Unpaywall 需要 email（环境变量 `ARS_UNPAYWALL_EMAIL`，默认占位）。
- **读取**：`pypdf` 可用则 `PdfReader` 提取；缺失则降级内置基础提取（zlib 解 FlateDecode + 文本操作符抽取），并在输出注明质量降级。

合规与稳健性：

- Sci-Hub 仅 `--allow-scihub` 显式开启、默认关；开启时命令输出提示风险。
- 各源遵循限速：arXiv 3s 间隔、429 退避重试（镜像上游客户端）；合理超时；错误归一化输出。
- 输出默认 Markdown（人 / agent 可读），`--json` 供程序化使用。

### 新增命令（`codex/commands/`，中文优先）

- `ars-search.md`：多源文献检索。说明用法、可选参数、示例提示词。
- `ars-download.md`：按 DOI 或 PDF URL 下载；说明合法 OA 优先与 `--allow-scihub` 风险提示。
- `ars-read.md`：本地 PDF 全文提取，供写作 / 引用阶段使用。

### SKILL.md 更新

- 新增「文献检索与全文获取」小节：描述三个命令 + deep-research 联动规则。
- 别名路由表补 `ars-search` / `ars-download` / `ars-read` 三行。
- `allowed-tools` 不改。

### deep-research 工作流联动

- 更新 `codex/agents/deep-research-team.md` 适配指引：文献综述 / 深度研究阶段，需要真实文献时优先用 `ars-search` 检索、`ars-download` 下载合法全文、`ars-read` 提取文本。
- 同步登记 `codex/compatibility-matrix.md` 与 `codex/full-runtime-manifest.json`。

### 测试 `codex/tests/test_literature.py`

- mock HTTP（不发起真实请求）：多源解析（Atom / JSON）、归一化与去重合并、下载回退链顺序、Sci-Hub 默认关 / 显式开、PDF 提取降级（pypdf 缺失路径）。

## 文件改动

- 新增 `skills/academic-research-suite/codex/scripts/ars_codex_literature.py`（源 + 插件副本）。
- 新增 `skills/academic-research-suite/codex/commands/ars-search.md` / `ars-download.md` / `ars-read.md`（源 + 插件副本）。
- 新增 `skills/academic-research-suite/codex/tests/test_literature.py`（源 + 插件副本）。
- 修改 `skills/academic-research-suite/SKILL.md`（源 + 插件副本）。
- 修改 `skills/academic-research-suite/codex/agents/deep-research-team.md`、`compatibility-matrix.md`、`full-runtime-manifest.json`（源 + 插件副本）。
- 修改 `skills/academic-research-suite/manifest.json` 的 `adapter_version`（源 + 插件副本）。
- 修改 `plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version`。
- 修改 `VERSION`、`CHANGELOG.md`、`README_ZH-CN.md`（新增命令入口）。

## 边界（YAGNI）

- 不做：不内嵌整个 `free-academic-search` 仓库、不引入 Node 运行时、不改 `allowed-tools` 白名单、不新增独立 workflow（只加命令）、不改 `ars/` vendored 内容、命令暂不做多语言版。
- 下载仅覆盖合法渠道（Sci-Hub 默认关，需显式 `--allow-scihub`）。

## 版本变更（1.1.0，MINOR）

- 四处同步更新为 `1.1.0`：`VERSION`、`SKILL.md` 的 `metadata.version`、`manifest.json` 的 `adapter_version`（源 + 插件副本）、`plugin.json` 的 `version`。
- `CHANGELOG.md`：归档 `## [1.1.0] - 2026-08-27`，新建空 `Unreleased`。
- 打 tag：`git tag v1.1.0`。
- 受保护文件变更后：`python scripts/verify_localization_guard.py --update` 再 `--check`。

## 治理与流程

1. 在 `main` 上创建 `codex/zh-literature` 分支 + worktree（`../academic-research-skills-codex-zh.worktrees/zh-literature/`）。
2. 在 worktree 内完成：脚本、命令、SKILL.md、deep-research 联动、版本四处、CHANGELOG、README。
3. 验证：guard `--update` + `--check`、`python -m pytest skills/academic-research-suite/codex/tests`。
4. 合并回 `main`，清理 worktree。
5. 同步插件缓存 `plugins\cache\ars-codex-zh\ars-codex-zh\1.1.0\`，用户重启 Codex app 生效。
6. 真实验证受限（需真实网络 / PDF），以 mock 测试 + 本地冒烟为准。

## 未决 / 风险

- 真实 API 响应差异与速率限制需在真实网络冒烟中确认（可在 dev 环境人工验证）。
- PDF 降级提取器质量低于 pypdf，`read` 输出可能不完整；优先提示安装 pypdf。
- 本机已装 pypdf / requests，但最终用户环境未知；脚本保持零硬依赖以兼容。
- 许可：`free-academic-search` 为 MIT（作者同为 zoujialin1997），以移植 / 参考形式纳入本 CC BY-NC 4.0 仓库；实现中保留对上游项目的致谢与许可证声明。
