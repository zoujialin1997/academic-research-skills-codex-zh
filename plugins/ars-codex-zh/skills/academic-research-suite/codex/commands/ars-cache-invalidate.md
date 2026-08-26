---
name: ars-cache-invalidate
description: ARS /ars-cache-invalidate——丢弃某个引文 key 的缓存验证条目
model: sonnet
---

使单个引文 key 的持久化验证缓存失效，使下一次管线运行实时对 Crossref / OpenAlex / Semantic Scholar / arXiv 重新验证，而不是返回过期的缓存判定。当引文元数据发生变化（例如预印本获得了已发表的 DOI）或先前验证看起来有误时使用。

该缓存（spec v3.11 #182 Delta 2）是 `~/.cache/ars/verification.db` 处的本地 SQLite 存储（可通过 `ARS_VERIFICATION_CACHE_PATH` 覆盖），以 `(citation_key, resolver_name, query_form)` 为键，TTL 为 90 天。本命令会删除该引文 key 的**每一条**缓存条目（全部四个 resolver、全部 query form）；其他引文不受影响。它是幂等的——对没有缓存行的 key 做失效会以 no-op 成功。

**失效级联（#541，无条件）**：失效后，下一个闸门会重新生成该引文的验证摘要行，并对引用它的声明重新运行 Phase E 审计判定——无条件执行（不保留任何基线用于 diff），涵盖存在状态、元数据与已检索证据。闸门处还会自动提示过期的缓存条目（`ARS_CACHE_STALE_ADVISORY_DAYS`，默认 30；通过 `ARS_CACHE_REVALIDATE=1` 选择实时重新验证）。

如需一次性使**整个**缓存失效（例如系统性 resolver 错误缓存了大量假阴性），直接删除数据库文件：`rm ~/.cache/ars/verification.db`。下次运行时会重建为空库。

实现：
```bash
python3 scripts/ars_cache_invalidate.py $ARGUMENTS
```

模式参考：`docs/design/2026-05-21-v3.10-182-promote-citation-gate-spec.md` §2 Delta 2。
