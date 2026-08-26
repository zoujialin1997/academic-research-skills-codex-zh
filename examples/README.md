# ars-codex-zh 示例（examples）

面向 `$academic-research-suite` skill 的 Codex 平台示例，按[上游 CONTRIBUTING.md § Platform ports L55](https://github.com/Imbad0202/academic-research-skills/blob/main/CONTRIBUTING.md#platform-ports-community-maintained-only)
的回归证据要求提供。

| 目录 | 用途 |
|---|---|
| [`codex/full-pipeline-heqa-scope-transformation/`](codex/full-pipeline-heqa-scope-transformation/) | 一次 Codex 平台 `academic-pipeline` **冒烟遍历**——在 Codex CLI 0.130.0 上通过 `codex exec` 于 2026-05-11 路由 6 个阶段（1、2、2.5、3、4、4.5+6）；Stage 5 产物导入自 2026-05-10 的先前 `ars-codex` 会话。两个 MANDATORY 学术诚信闸门均已启用。完整的诚实范围声明见该目录 README。 |

> 注：与 vendored 的 `skills/academic-research-suite/ars/*/examples/` 目录区分——后者是作为工作流内容复制的上游 Claude Code 示例，不是 Codex 平台证据。
