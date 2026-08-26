---
name: ars-unmark-read
description: ARS /ars-unmark-read——撤销一条或多条引文 key 的用户自证已读信号
model: sonnet
---

撤销先前为指定引文 key 记录的 `USER_ATTESTED_READ` 声明。按 v3.6.8 spec §3.6 firm rule 3，会话作用域同级文件 `<passport-stem>_human_read_log.yaml` 是追加式的：撤销会在匹配条目上写入 `rescinded_at: <ISO 8601>` 字段而非删除它，使审计重放能重建用户的信号轨迹。下一次 finalizer 通过会把每个被撤销 slug 的依赖覆盖 `<!--ref:slug ok-->` 降级回 `<!--ref:slug LOW-WARN-->`。

派发 agent 在执行前用会话上下文中的活动 Material Passport 路径替换下面的 `<path>`（保留引号，使含空格的路径仍作为单个参数）。CLI 要求 citation_key 存在于 `literature_corpus[]` 中**且**在读日志中有一条未撤销的先验标记；否则以规范 `[ARS-MARK-READ ERROR: ...]` 消息硬失败。

实现：
```bash
python3 scripts/ars_mark_read.py $ARGUMENTS --passport-path "<path>" --unmark
```

模式参考：`docs/design/2026-04-30-ars-v3.6.8-trust-provenance-and-drift-transparency-spec.md` §3.6 + Step 7。
