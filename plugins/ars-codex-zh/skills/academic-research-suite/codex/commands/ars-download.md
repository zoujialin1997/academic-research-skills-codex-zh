---
name: ars-download
description: ARS 合法文献下载——按 DOI 或 PDF URL 下载 PDF；默认只走合法开放获取，Sci-Hub 需显式 --allow-scihub
model: sonnet
---

按 DOI 或 PDF URL 下载 PDF 到本地（免费、无需 API key、无积分）。运行：

```bash
# 按 DOI 下载（合法 OA 优先：直接 / Unpaywall；显式 --allow-scihub 才尝试 Sci-Hub）
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py download --doi "10.xxxx/yyyy" [--out ./papers] [--allow-scihub] [--json]

# 按 PDF URL 直接下载
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py download --url "https://.../paper.pdf" [--out ./papers]
```

- 回退链：直接 / arXiv OA → Unpaywall 合法 OA →（仅显式 `--allow-scihub`）Sci-Hub。
- `--allow-scihub` 默认关；启用时命令会输出风险提示，请确保你对该内容拥有合法访问权。
- 下载结果保存到 `--out` 目录，输出保存路径与来源渠道。

示例：

```bash
python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py download --doi "10.1109/TAC.2023.3339435" --out ./papers
```

约束：本命令只走合法渠道；对付费墙内容无开放副本时请勿绕行付费墙。
