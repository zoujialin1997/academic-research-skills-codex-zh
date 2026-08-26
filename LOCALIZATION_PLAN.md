# ARS-Codex 适配层汉化方案（Localization Plan）

> 文档状态：**P0/P1 已交付，P2 命令覆盖层已落地（v1 完成）**
> 所属分支：`codex/zh-adapter-layer`
> 适用仓库：`academic-research-skills-codex-zh`（ARS-Codex 中文适配镜像，Codex 包 `1.0.1` / 内嵌 ARS `v3.21.1`）

---

## 一、目标与原则

**目标**：让中文用户在 Codex 中「安装看到中文、触发说中文、交互读中文」，同时**不改变任何功能语义、不触碰上游 vendored 内容**。

**五项原则**
1. **只动 Codex 适配层**：`SKILL.md`、`codex/`、`plugin.json`、`openai.yaml`、`examples/`、根文档；`ars/` 深层（references / templates / 角色提示词 / schema）保留英文原版。
2. **触发语义不破坏**：中文触发词是**新增**，英文、韩文触发全部保留。
3. **行为不变**：路由规则、安全边界、模式逻辑原样保留，只翻译呈现语言。
4. **术语统一**：按本文档「术语表」执行，全库一致。
5. **双副本 + 防护**：每步改动同步 `skills/` 与 `plugins/`，过 `scripts/verify_localization_guard.py --check` 与 pytest。

---

## 二、逐文件范围（按优先级分层）

| 优先级 | 文件 | 现状 | 汉化动作 |
|---|---|---|---|
| P0 | `plugins/ars-codex-zh/.codex-plugin/plugin.json` | 英文 | 插件市场展示文案中文化 |
| P0 | `skills/academic-research-suite/agents/openai.yaml` | 英文 | 展示名 / 默认提示中文化 |
| P0 | `skills/academic-research-suite/SKILL.md` | 英文（路由描述无中文触发） | 描述加中文触发词；正文全中文 |
| P1 | `skills/academic-research-suite/codex/README.md`、`codex/agents/*.md`（5 个）、`codex/compatibility-matrix.md` | 英文 | 中文化 |
| P1 | `examples/`（README + 各 stage 文件） | 英文 | 中文示例说明 |
| P1 | 根 `README_ZH-CN.md` | 已存在但夹杂英文术语 | 润色 + 术语统一 + 与 `README.md` 同步 |
| P2 | `ars/commands/ars-*.md`（16 个） | 英文（vendored） | **已完成**：`codex/commands/` 中文覆盖层，路由优先覆盖、缺失回退上游 |
| — | `ars/` 其余内容 | 英文 | **不汉化**（上游保护） |

### P2 决策点：命令提示词（ars/commands）

`ars/commands/*` 位于 vendored 目录，直接修改违反 AGENTS.md 铁律 1（`ars/` 禁止手工编辑）。

**推荐方案（已执行，v1 落地）**：
- 在 `codex/commands/` 放 16 个中文版命令提示词（与 `ars/commands/` 同名）
- 修改 `SKILL.md` 别名路由与 `ars_codex_full_runtime.py` 解析器：**优先读 `codex/commands/`，缺失回退 `ars/commands/`**
- 好处：命令提示中文化的同时完全不碰上游，同步时零冲突；未来上游新增命令未覆盖前自动回退英文原版

---

## 三、术语表（全库统一用词）

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| Socratic mode | 苏格拉底引导模式 | manuscript | 稿件 |
| deep research | 深度研究 | peer review | 同行评审 |
| literature review | 文献综述 | integrity gate | 学术诚信闸门 |
| systematic review | 系统综述 | workflow / pipeline | 工作流 / 研究管线 |
| meta-analysis | 元分析 | agent | 智能体（agent） |
| research question | 研究问题 | handoff | 交接 |
| revision coach | 修改辅导 | citation check | 引用核查 |
| IMRaD / APA 7.0 / PRISMA | 保留原文 | evidence row | 证据行 |
| research gap | 研究空白 | mode | 模式 |
| scoping | 研究范围收敛 | consent | 同意 / 授权 |

> 约定：无法找到贴切中文、或中文易产生歧义的术语，采用「中文（英文原词）」形式首现，之后单用中文。

---

## 四、前后效果对比（Before / After）

### 1. 插件市场安装界面（plugin.json）
- **前**：`shortDescription: "Codex-native research, writing, review, and experiment workflows."`；默认提示 `"Plan my academic paper from rough research notes."` 等（全英文）。
- **后**：`shortDescription: "面向 Codex 的深度研究、学术写作、稿件评审与实验规划工作流。"`；默认提示 `「根据我的研究笔记规划学术论文。」`、`「像期刊审稿人一样评审我的稿件。」`、`「构建文献综述并识别研究空白。」`。

### 2. skill 触发（SKILL.md frontmatter description）
- **前**：路由描述只有英文 + 韩文触发词（`논문 심사…`）；中文用户依赖 `ars/` 内 WORKFLOW 的繁体中文触发词兜底，路由不精确。
- **后**：描述中文化，新增中文触发词（`深度研究、文献综述、系统综述、元分析、论文写作、稿件评审、同行评审、实验规划、研究问题收敛…`），英/韩触发保留——中文提问命中率显著提升。

### 3. 对话交互（SKILL.md 正文）
- **前**：用户说「我想写一篇论文，题目还没定」→ 路由器以英文输出「routing to deep-research socratic mode…」。
- **后**：首条回复中文「我先把请求路由到深度研究的苏格拉底引导模式，因为研究问题还不够精确…」，随后用中文提出 3-5 个收敛问题；路由表、别名表（`ars-plan` / `ars-outline` / `ars-reviewer`…）、运行时映射全部中文。

### 4. 命令提示（ars-*.md）
- **前**：`/ars-plan` 读到的提示词全英文。
- **后**：`codex/commands/` 中文覆盖层已落地——`/ars-plan` 优先读到中文提示词；未覆盖的新命令回退上游英文 `ars/commands/`。SKILL.md 路由表与 `full-runtime` 解析器均实现「优先覆盖、缺失回退」。

### 5. 示例（examples/）
- **前**：英文 README 与 stage 说明，中文用户难以对照。
- **后**：中文分步讲解完整管线（研究范围收敛 → 写作 → 诚信闸门 → 评审 → 终稿）。

### 6. 根 README_ZH-CN.md
- **前**：已翻译但夹杂 `sibling`、`plugin`、`runtime adapter`、`workflow` 等未翻译术语，机器翻译痕迹明显。
- **后**：术语按术语表统一（如「Codex 原生姊妹版」），中文通顺，与 `README.md` 内容同步。

### 7. codex/ 适配层（README + 5 个 agent 团队模板）
- **前**：全英文。
- **后**：中文说明全运行时开关（`ARS_CODEX_FULL_RUNTIME` / `ARS_CODEX_AGENT_TEAM` / `ARS_CODEX_HOOKS`）、agent 团队分工、质量门，便于中文维护者理解。

---

## 五、明确「不汉化」的边界

- `ars/` 内全部：agent 角色提示词、templates、references、docs、schema、scripts、tests——保留英文原版（保证上游同步零冲突、学术提示质量不变）。
- **学术产出语言不变**：生成的论文 / 综述 / 报告默认仍按学术规范（用户可另行要求中文输出，但那是运行期行为，不属本次适配范围）。

---

## 六、实施顺序

1. **P0-a**：`plugin.json` 展示文案
2. **P0-b**：`openai.yaml` 展示文案
3. **P0-c**：`SKILL.md` 路由器（核心，量最大）
4. **P1-a**：`codex/` 适配层文档 + agent 模板
5. **P1-b**：`examples/`
6. **P1-c**：`README_ZH-CN.md` 润色
7. **P2（已完成）**：`codex/commands/` 中文覆盖层（16 个命令）

## 七、每步完成标准（验证）

1. 双副本同步：`skills/academic-research-suite/` 与 `plugins/ars-codex-zh/skills/` 逐字节一致
2. 防护脚本：`python scripts/verify_localization_guard.py --check` 退出码为 0
3. 适配层测试：`python -m pytest skills/academic-research-suite/codex/tests`
4. 中文冒烟：用中文提问逐一触发各工作流（深度研究 / 论文写作 / 稿件评审 / 完整管线 / 实验规划）
   > 注：结构级校验（触发词、路径、解析器回退）已通过；真实 `codex exec` 中文端到端冒烟需在可运行 codex CLI 的机器上安装 skill 后执行。

> 注意：受保护文件（含 `SKILL.md`、`plugin.json`）改动属有意编辑，完成后需 `python scripts/verify_localization_guard.py --update` 记录新基线。

---

## 八、风险与缓解

| 风险 | 缓解 |
|---|---|
| 翻译时误改行为语义（把规则一起改坏） | 严格对照原文翻译，不改写逻辑；防护脚本 + pytest 兜底 |
| 术语不一致 | 按术语表执行，收尾统一检查 |
| 上游 sync 覆盖 / 冲突 | 已由 AGENTS.md + 防护脚本解决（适配层受保护 + `[DRIFT]` 重新适配机制） |
| 命令提示词无法直接汉化（vendored） | P2 决策点：`codex/commands/` 覆盖层方案 |
| 双副本不同步 | 每步强制双副本一致性校验 |

---

## 附：引用文档

- `AGENTS.md`（铁律、同步流程、Git Worktree 管理、版本管理、测试）
- `scripts/verify_localization_guard.py`（同步防护脚本）
- `skills/academic-research-suite/manifest.json`（上游同步记录）
