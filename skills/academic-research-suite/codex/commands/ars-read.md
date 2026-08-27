---
name: ars-read
description: ARS 全文读取——提取本地 PDF 的全文文本，供综述、引用与写作阶段使用
model: sonnet
---

提取本地 PDF 的全文文本（免费、无需 API key、无积分）。运行：

```bash
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py read --file "<path/to/paper.pdf>" [--max-chars 60000] [--json]
```

- 已安装 `pypdf` 时使用 `pypdf` 提取（质量更好）；未安装则降级到内置基础提取器，输出会标注 `stdlib-fallback`。
- 默认输出全文文本，`--max-chars` 可截断；`--json` 输出结构化结果（含字符数与提取模式）。
- 用途：论文写作、文献综述、引用核对的全文依据；结合 `ars-search`（检索）与 `ars-download`（下载）端到端使用。

示例：

```bash
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py read --file "./papers/paper.pdf" --max-chars 30000
```
