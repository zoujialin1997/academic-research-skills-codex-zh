# ARS-Codex 中文版 · 新手快速上手

> 这是一份给新手的完整上手教程。想最快体验？直接看第 2 节「3 分钟起步」。
> 想看交互式引导？在对话里输入 `/ars-guide`，我会一步步带你走。

## 0. 一句话：这个插件能帮你做什么

ARS-Codex 是一个安装在 Codex（OpenAI 的编程与任务代理）里的学术研究套件。
它把「做研究、写论文、审论文」这一整套流程标准化，让 AI 帮你按专业学术工作流干活，
而不是东一句西一句地瞎答。它能帮你：

- **深度研究**：把模糊的想法收敛成可回答的研究问题，做文献综述、系统综述。
- **写论文**：从大纲、摘要到正文起草、引用格式、AI 使用声明，一条龙。
- **论文评审**：模拟审稿人、生成编辑部决定信、帮你修改后再送审。
- **完整管线**：从研究问题到成稿的端到端流程，带学术诚信检查。
- **实验规划**：代码实验、人类研究方案、统计解读、可复现性验证。

简单说：**你把想做的事用大白话说出来，剩下的流程化工作交给它。**

## 1. 安装要点

安装步骤详见 [`README_ZH-CN.md`](README_ZH-CN.md) 的「安装 ARS-Codex Plugin」章节，要点如下：

- 通过 Codex 添加 GitHub marketplace 并安装插件：
  `codex plugin marketplace add Imbad0202/academic-research-skills-codex --ref main`，然后
  `codex plugin add ars-codex-zh@ars-codex-zh`。
- 在 Codex Desktop 中也可以从 **Plugins** 添加本仓库，再安装 **ARS-Codex**。
- 安装后**打开一个新对话**，输入 `/skills` 应看到唯一一个 `academic-research-suite`（或 `ARS-Codex`）条目。
- 以后更新：`codex plugin marketplace upgrade ars-codex-zh` 后再 `codex plugin add ars-codex-zh@ars-codex-zh`。

## 2. 第一次使用：3 分钟起步

**不需要记任何命令。** 你只需要用自然语言描述你要做的事，套件会自动路由到合适的工作流。

最经典的起步方式是：描述一个你目前**还没有清晰研究问题**的论文主题——

```text
Use $academic-research-suite.

I want to write a paper on AI adoption in higher education quality assurance.
I do not yet have a clear research question.
```

预期会发生什么：

1. 套件识别出你的研究问题还不精确，自动进入 `deep-research` 的 **Socratic（苏格拉底式）收敛**模式。
2. 它会问你 3-5 个聚焦问题，帮你把模糊想法收敛成一个可回答的研究问题。
3. **在问题收敛之前，它不会急着给你写大纲或草稿**——这是有意设计，避免方向跑偏。

这就是最核心的上手动作：**有个想法 → 说出来 → 让 AI 先帮你问清楚。**

## 3. 五个典型场景怎么触发

每个场景都是一句话 + 示例提示词。可以直接复制替换成你的内容。

| 场景 | 触发方式 | 示例提示词（可直接复制） |
|---|---|---|
| 深度研究 / 文献综述 | 说要做一个综述或研究，但研究问题还没收敛 | `Use $academic-research-suite to build a systematic review protocol for AI in higher education QA.` |
| 写论文 | 已有大纲、笔记或草稿，要成文 | `Use $academic-research-suite to turn these notes into an IMRaD paper outline and drafting plan.` |
| 论文评审 | 要审一份稿件、模拟审稿人或出决定信 | `Use $academic-research-suite to review this manuscript and produce a journal-style decision letter.` |
| 完整管线 | 要从主题一路做到修改后的稿件 | `Use $academic-research-suite to run an end-to-end research-to-paper pipeline from topic to revised manuscript.` |
| 实验规划 | 要做代码实验、人类研究或统计解读 | `Use $academic-research-suite to plan a code experiment and define reproducibility checks.` |

**想要更精确的控制？** 用「使用模式」写法一次说清目标、现状、输出和约束：

```text
Use $academic-research-suite.

Goal: write a journal article.
Current materials: I have a literature matrix and rough findings, but no outline.
Output needed now: paper architecture and missing-evidence checklist.
Constraints: English, APA 7, higher education policy audience.
```

## 4. 走一遍完整示例：从想法到论文

以「写一篇关于 AI 赋能高校质量保障的论文」为例，走完整流程：

**第 1 步 · 收敛研究问题（Socratic）**

```text
Use $academic-research-suite.
I want to write a paper on AI adoption in higher education quality assurance.
I do not yet have a clear research question.
```

→ 进入 `socratic` 模式，回答它的 3-5 个聚焦问题，直到收敛出一个研究问题（RQ）。

**第 2 步 · 生成大纲**

研究问题明确后，让套件进入论文规划与大纲：

```text
Use $academic-research-suite to plan this paper and produce an outline.
My research question is: [你收敛出的 RQ]。请给出 IMRaD 结构的大纲和缺失证据清单。
```

**第 3 步 · 起草正文**

```text
Use $academic-research-suite to draft the Introduction and Methods sections from my approved outline.
```

**第 4 步 · 自检与修改**

写完后让套件检查引用完整性与写作质量，并按审稿视角修改：

```text
Use $academic-research-suite to review my draft: check citation integrity and likely reviewer concerns, then revise.
```

> 提示：也可以直接要求端到端管线 `academic-pipeline`，它会带完整性检查、评审、修改和最终检查一路走完；建议分阶段设置检查点，而不是一口气静默跑完。

## 5. 你会遇到的新交互

ARS-Codex 中文版在交互上有几个贴心设计，第一次遇到别慌：

- **固定选项点选卡片**：当套件需要你从几个选项里选一个时（比如「你想先做哪件事？」），在 Codex 的 Plan 模式下会弹出**点选卡片**，直接点选即可，不用打字。如果不在 Plan 模式，它会给出带编号的选项列表，你回复数字即可。
- **专业术语通俗解释**：面向你的输出中，专业术语第一次出现时，会用括号附一句大白话解释。比如「文献综述（把某一主题下已有的研究汇总、梳理、找出空白的综述）」。
- **明确的工作流路由提示**：套件会先告诉你「你的请求被路由到哪个工作流、为什么」，让你知道它在按什么流程走，而不是黑箱操作。

## 6. 常见误区与技巧

- **误区：主题模糊就直接要大纲。** 套件会拒绝并先进 Socratic 收敛。正确的做法：模糊主题时，先让它帮你收敛研究问题，不要催它写大纲。
- **技巧：想跳过收敛直接写。** 如果你已有清晰研究问题、已批准框架或完整材料，可以在提示词里说明，例如加 `[direct-mode]`，套件就会直接进入大纲/起草，不走 Socratic。
- **技巧：提问阶段切到 Plan 模式。** 当你看到套件在向你提问、需要你从固定选项里选时，切到 Plan 模式可以弹出点选卡片，点选比打字更省事。
- **技巧：把材料一次给全。** 有文献矩阵、笔记、草稿、审稿意见、输出约束，尽量在一次请求里说清楚（参考第 3 节的「使用模式」写法），套件就能少问几轮、质量更高。
- **误区：担心它会自动联网乱查。** Web/源码验证只在涉及当前或外部事实时使用，且会引用来源；无法验证的内容会明确标记为「未验证」，而不是编造。
- **边界：跨模型验证默认关闭。** 除非你明确要求并配置，套件不会把内容发给第三方模型。

## 7. 更多资源

- [`README_ZH-CN.md`](README_ZH-CN.md)：完整参考手册（安装、别名表、模式说明、冒烟测试）。
- **`/ars-guide`**：对话内交互式引导，一步步带你选场景、拿示例提示词。
- 各工作流文档：`skills/academic-research-suite/ars/deep-research/WORKFLOW.md`、
  `ars/academic-paper/WORKFLOW.md`、`ars/academic-paper-reviewer/WORKFLOW.md`、
  `ars/academic-pipeline/WORKFLOW.md`、`ars/experiment-agent/WORKFLOW.md`。
- 版本与变更：`CHANGELOG.md`。

---

**还卡住了？** 在对话里直接输入 `/ars-guide`，或说「我是新手，怎么用这个插件？」，我会带你走一遍。
