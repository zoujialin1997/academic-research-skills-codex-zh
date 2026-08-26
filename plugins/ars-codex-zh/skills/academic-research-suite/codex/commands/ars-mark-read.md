---
name: ars-mark-read
description: ARS /ars-mark-read——为一条或多条引文 key 记录用户自证的已读信号
model: sonnet
---

记录用户对支撑指定引文 key 的来源的 `USER_ATTESTED_READ` 声明。这是用户陈述，不是证明某人确实阅读或理解来源的独立证据。仅当声明的范围覆盖该引文的锚点时，finalizer 才可将 `<!--ref:slug LOW-WARN-->` 提升为 `<!--ref:slug ok-->`。按 v3.6.8 spec §3.6，该信号存储在活动 Material Passport 旁的会话作用域同级文件 `<passport-stem>_human_read_log.yaml` 中；`literature_corpus[]` 归适配器所有，绝不因携带阅读状态而被改写。

派发 agent 在执行前用会话上下文中的活动 Material Passport 路径替换下面的 `<path>`（保留引号，使含空格的路径仍作为单个参数）。CLI 处理校验（citation_key 必须存在于 `literature_corpus[]`；未命中时发出 `[ARS-MARK-READ ERROR: citation_key '<slug>' not in literature_corpus[]]` 并拒绝写入）、4 项 fail-fast 环境检查（无活动 passport / 找不到 passport / 父目录不可读 / 读日志不可写），以及按 §3.6 firm rule 3 的追加写入。

每次新标记都需要阅读范围（#738；仅声明——照实传递用户陈述，绝不推断）：`--scope {full_text,sections,abstract_only,toc_only,unknown}` 记录声明的覆盖范围；`--locator "<text>"`（可重复，需 `--scope sections`）指定已读章节/页；`--note "<text>"` 自由文本（需 `--scope`）。用户无法说明覆盖范围时使用 `--scope unknown`。仅遗留账本记录接受缺失的 scope。显式 `unknown` 与遗留的缺失 scope 保持为 `coverage_unknown`；它们承认该声明，但绝不能将有锚点的引文提升为 `ok`。页码覆盖要求显式 `page`、`p.` 或 `pp.` locator——裸数字和 `section <n>` 一律不算页码范围。`scripts/human_read_attestation_resolver.py` 中的确定性解析器严格校验当前账本，并在每次 finalizer 通过时计算临时路由判定；其输出不是持久化的审计回执。

实现：
```bash
python3 scripts/ars_mark_read.py $ARGUMENTS --passport-path "<path>"
```

模式参考：`docs/design/2026-04-30-ars-v3.6.8-trust-provenance-and-drift-transparency-spec.md` §3.6 + Step 7。
