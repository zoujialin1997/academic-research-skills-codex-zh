---
name: ars-search
description: ARS 多源文献检索——Semantic Scholar / PubMed / arXiv / bioRxiv / medRxiv / Crossref，去重合并后返回带 DOI / PDF 链接的条目
model: sonnet
---

多源学术文献检索（免费、无需 API key、无积分）。运行：

```bash
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py search --query "<检索词>" [--sources arxiv,pubmed,semantic-scholar,biorxiv,medrxiv,crossref] [--max-results 10] [--year-from 2020] [--json]
```

- 默认覆盖全部六个数据源，结果按 DOI / arXiv ID / 标题去重合并。
- 输出 Markdown 条目列表（作者 / 年份 / 期刊 / DOI / 开放 PDF 链接 / 摘要），`--json` 可切换为结构化 JSON。
- 用途：深度研究、文献综述、系统综述、引文收集的检索入口；检索后可用 `ars-download` 下载合法全文，用 `ars-read` 提取文本。

示例：

```bash
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py search --query "distributed optimization" --sources arxiv,semantic-scholar --max-results 20
```

约束：仅调用各数据源官方公开接口并遵守其限速；个别数据源暂不可用时命令会降级并提示，属正常现象。
