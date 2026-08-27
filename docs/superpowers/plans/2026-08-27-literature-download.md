# 文献检索与全文获取（ars-search / ars-download / ars-read）实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 ARS-Codex-zh 新增原生多源文献检索、合法下载与全文读取能力（`ars-search` / `ars-download` / `ars-read` 三个命令），零硬性依赖，并接入 deep-research 工作流。

**Architecture:** 在适配层新增一个纯标准库 Python 脚本 `codex/scripts/ars_codex_literature.py`（urllib 网络 + pypdf 可选 PDF 提取），通过三个 `codex/commands/ars-*.md` 命令配方暴露；SKILL.md 新增「文献检索与全文获取」小节与三行别名路由；`full-runtime-manifest.json` 登记三个命令（workflow 复用 `deep-research`，mode 为 `search` / `download` / `read`）；deep-research 团队指引声明使用这三个命令；版本升至 `1.1.0`（MINOR）。

**Tech Stack:** Python 3.12（标准库 urllib / json / xml.etree / zlib）、argparse、pytest、可选 pypdf；不新增任何第三方硬依赖；不改 `allowed-tools` 白名单（沿用 `Bash(python *)`）。

## Global Constraints

- **TDD is required.** 每个新行为遵循 RED-GREEN-REFACTOR：先写失败测试 → 运行确认失败 → 实现 → 运行确认通过。实现者报告须包含每项新行为的 TDD 证据（RED + GREEN）。
- **零硬性依赖**：网络只用 `urllib.request`；PDF 提取优先 `pypdf`，缺失时降级内置提取器（`force_fallback` 路径）。绝不新增 `requests` 等第三方依赖。
- **下载合法性边界**：默认只走合法开放获取（直接 / arXiv OA → Unpaywall）；Sci-Hub 仅在 `--allow-scihub` 显式传入时尝试；`download_pdf_by_doi` 的 `allow_scihub` 参数默认 `False`。
- **版本四处一致**：`VERSION`、`SKILL.md` 的 `metadata.version`、`skills/academic-research-suite/manifest.json` 的 `adapter_version`、`plugins/ars-codex-zh/.codex-plugin/plugin.json` 的 `version` 全部为 `1.1.0`。
- **双副本逐字节一致**：任何对 `skills/academic-research-suite/` 的改动都必须同步到 `plugins/ars-codex-zh/skills/`。
- **不改 `ars/` vendored 内容**；`model_hint` 必须为 `"sonnet"`（既有测试 `test_command_model_hints_match_upstream_frontmatter_semantics` 要求其余命令全部为 sonnet）；每条命令 `aliases` 数组必须有 2 个元素（既有测试用 `aliases[1]`）。
- **汉化风格**：命令配方与 SKILL.md 新增内容使用简体中文、平实的语言；专业术语首次出现附大白话解释。

## File Structure

| 文件 | 职责 | 动作 |
|---|---|---|
| `skills/academic-research-suite/codex/scripts/ars_codex_literature.py` | 搜索 / 下载 / 读取核心 + CLI | 新增 |
| `skills/academic-research-suite/codex/tests/test_literature.py` | mock 网络的单元测试 | 新增 |
| `skills/academic-research-suite/codex/commands/ars-search.md` | 检索命令配方 | 新增 |
| `skills/academic-research-suite/codex/commands/ars-download.md` | 下载命令配方 | 新增 |
| `skills/academic-research-suite/codex/commands/ars-read.md` | 读取命令配方 | 新增 |
| `skills/academic-research-suite/SKILL.md` | 新增小节 + 3 行别名 + 描述里补别名 | 修改 |
| `skills/academic-research-suite/codex/full-runtime-manifest.json` | 登记 3 个命令 + deep-research modes 补 3 个 | 修改 |
| `skills/academic-research-suite/codex/compatibility-matrix.md` | 新增一行「文献检索与下载」 | 修改 |
| `skills/academic-research-suite/codex/agents/deep-research-team.md` | 新增「文献获取」小节 | 修改 |
| `skills/academic-research-suite/manifest.json` | `adapter_version` → `1.1.0` | 修改 |
| `plugins/ars-codex-zh/.codex-plugin/plugin.json` | `version` → `1.1.0` | 修改 |
| `VERSION` | `1.1.0` | 修改 |
| `CHANGELOG.md` | 归档 `1.1.0` | 修改 |
| `README_ZH-CN.md` | 新增功能清单补一条 | 修改 |

所有 `skills/academic-research-suite/` 下的改动都必须镜像到 `plugins/ars-codex-zh/skills/`（Task 6 整体复制）。

---

### Task 1: 脚本骨架 + 多源检索子命令（TDD）

**Files:**
- Create: `skills/academic-research-suite/codex/tests/test_literature.py`
- Create: `skills/academic-research-suite/codex/scripts/ars_codex_literature.py`

**Interfaces:**
- Consumes: 无（首个任务）。
- Produces: 后续任务依赖的签名：
  - `normalize_doi(doi: str | None) -> str`
  - `normalize_title(title: str | None) -> str`
  - `_paper(**fields: Any) -> dict[str, Any]`
  - `_http_get_bytes(url: str, headers: dict | None = None, timeout: float = 30, retries: int = 3) -> tuple[bytes, dict[str, str]]`
  - `_http_get_json(url: str, headers: dict | None = None) -> Any`
  - `search_arxiv(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict]`
  - `search_pubmed(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict]`
  - `search_semantic_scholar(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict]`
  - `search_rxiv(server: str, query: str, max_results: int = 10, year_from: int | None = None) -> list[dict]`
  - `search_crossref(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict]`
  - `merge_paper_lists(lists: list[list[dict]]) -> list[dict]`
  - `SOURCE_FUNCS: dict[str, Callable]`（键：`arxiv`/`pubmed`/`semantic-scholar`/`biorxiv`/`medrxiv`/`crossref`）
  - `main(argv: list[str] | None = None) -> int`
- [ ] **Step 1: 写失败测试**

创建 `skills/academic-research-suite/codex/tests/test_literature.py`，内容：

```python
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

CODEX_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = CODEX_ROOT / "scripts" / "ars_codex_literature.py"


def _load():
    spec = importlib.util.spec_from_file_location("ars_codex_literature", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _fake_bytes(payload: bytes):
    def _get_bytes(url, headers=None, timeout=30, retries=3):
        return payload, {}
    return _get_bytes


ARXIV_ATOM = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2401.00001v1</id>
    <title>  A Test Paper On Distributed Optimization  </title>
    <published>2024-01-01T00:00:00Z</published>
    <author><name>Alice</name></author>
    <author><name>Bob</name></author>
  </entry>
</feed>
"""

PUBMED_ESEARCH = json.dumps({"esearchresult": {"idlist": ["12345"]}}).encode("utf-8")
PUBMED_ESUMMARY = json.dumps({
    "result": {
        "12345": {
            "title": "A PubMed Test Paper",
            "authors": [{"name": "Carol"}],
            "pubdate": "2023 Apr",
            "elocationid": "doi 10.1000/pm",
        }
    }
}).encode("utf-8")
S2_JSON = json.dumps({
    "data": [{
        "paperId": "abc123",
        "title": "An S2 Test Paper",
        "authors": [{"name": "Dan"}],
        "year": 2022,
        "externalIds": {"DOI": "10.1000/s2", "ArXiv": "2201.11111"},
        "openAccessPdf": {"url": "https://oa.example/s2.pdf"},
        "venue": "Some Journal",
        "citationCount": 5,
        "url": "https://www.semanticscholar.org/paper/abc123",
        "abstract": "An abstract.",
    }]
}).encode("utf-8")
CROSSREF_JSON = json.dumps({
    "message": {"items": [{
        "DOI": "10.1000/cr",
        "title": ["A Crossref Test Paper"],
        "author": [{"given": "Eve", "family": "Zhao"}],
        "issued": {"date-parts": [[2021]]},
        "container-title": ["Journal of Testing"],
        "URL": "https://doi.org/10.1000/cr",
    }]}
}).encode("utf-8")
RXIV_JSON = json.dumps({
    "collection": [{
        "title": "A bioRxiv Test Paper",
        "doi": "10.1101/2020.01.01.000001",
        "authors": "Frank; Grace",
        "date": "2020-01-01",
    }]
}).encode("utf-8")
def test_normalize_doi_strips_prefixes() -> None:
    mod = _load()
    assert mod.normalize_doi("https://doi.org/10.1000/XYZ") == "10.1000/xyz"
    assert mod.normalize_doi("doi:10.1000/XYZ") == "10.1000/xyz"
    assert mod.normalize_doi("10.1000/xyz") == "10.1000/xyz"


def test_search_arxiv_parses_atom(monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(ARXIV_ATOM))
    monkeypatch.setattr(mod, "ARXIV_MIN_INTERVAL", 0)
    papers = mod.search_arxiv("distributed optimization", max_results=5)
    assert len(papers) == 1
    paper = papers[0]
    assert paper["source"] == "arxiv"
    assert paper["arxivId"] == "2401.00001v1"
    assert paper["title"] == "A Test Paper On Distributed Optimization"
    assert paper["authors"] == ["Alice", "Bob"]
    assert paper["year"] == 2024
    assert paper["pdfUrl"] == "https://arxiv.org/pdf/2401.00001v1"


def test_search_pubmed_parses_esummary(monkeypatch) -> None:
    mod = _load()

    def _get(url, **kw):
        if "esearch.fcgi" in url:
            return PUBMED_ESEARCH, {}
        return PUBMED_ESUMMARY, {}

    monkeypatch.setattr(mod, "_http_get_bytes", _get)
    papers = mod.search_pubmed("diabetes", max_results=5)
    assert len(papers) == 1
    paper = papers[0]
    assert paper["source"] == "pubmed"
    assert paper["pmid"] == "12345"
    assert paper["title"] == "A PubMed Test Paper"
    assert paper["doi"] == "10.1000/pm"
    assert paper["year"] == 2023


def test_search_semantic_scholar_parses_json(monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(S2_JSON))
    papers = mod.search_semantic_scholar("transformers", max_results=5)
    assert len(papers) == 1
    paper = papers[0]
    assert paper["source"] == "semantic-scholar"
    assert paper["title"] == "An S2 Test Paper"
    assert paper["doi"] == "10.1000/s2"
    assert paper["arxivId"] == "2201.11111"
    assert paper["openAccessPdf"] == "https://oa.example/s2.pdf"


def test_search_crossref_parses_json(monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(CROSSREF_JSON))
    papers = mod.search_crossref("climate", max_results=5)
    assert len(papers) == 1
    paper = papers[0]
    assert paper["source"] == "crossref"
    assert paper["doi"] == "10.1000/cr"
    assert paper["title"] == "A Crossref Test Paper"
    assert paper["authors"] == ["Eve Zhao"]
    assert paper["year"] == 2021


def test_search_rxiv_parses_json(monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(RXIV_JSON))
    papers = mod.search_rxiv("biorxiv", "genome", max_results=5)
    assert len(papers) == 1
    paper = papers[0]
    assert paper["source"] == "biorxiv"
    assert paper["title"] == "A bioRxiv Test Paper"
    assert paper["authors"] == ["Frank", "Grace"]
    assert paper["doi"] == "10.1101/2020.01.01.000001"


def test_merge_dedupes_and_enriches() -> None:
    mod = _load()
    first = mod._paper(source="arxiv", id="1", title="Same Title", doi="10.1000/x", arxivId="2001.1")
    second = mod._paper(source="crossref", id="2", title="Same Title", authors=["A", "B"], doi="10.1000/X", year=2020)
    merged = mod.merge_paper_lists([[first], [second]])
    assert len(merged) == 1
    assert merged[0]["authors"] == ["A", "B"]
    assert merged[0]["year"] == 2020


def test_cli_search_prints_markdown(monkeypatch, capsys) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(ARXIV_ATOM))
    monkeypatch.setattr(mod, "ARXIV_MIN_INTERVAL", 0)
    rc = mod.main(["search", "--query", "distributed optimization", "--sources", "arxiv"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "A Test Paper On Distributed Optimization" in out
```
- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest skills/academic-research-suite/codex/tests/test_literature.py -v`
Expected: 全部报错（`ars_codex_literature.py` 不存在 → `FileNotFoundError` / collection error）。

- [ ] **Step 3: 写最小实现**

创建 `skills/academic-research-suite/codex/scripts/ars_codex_literature.py`，内容：

```python
#!/usr/bin/env python3
"""ARS-Codex literature search, download, and full-text read.

Free multi-source academic search + legal open-access download + PDF text
extraction. No API key, no credits. Pure standard library (urllib); pypdf is
used when available for better PDF text extraction, with a built-in degraded
extractor otherwise.

Adapted from the design of zoujialin1997/free-academic-search (MIT). Download
boundary: legal open access first (direct / arXiv OA -> Unpaywall legal OA);
Sci-Hub is only attempted via the explicit --allow-scihub flag.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable

DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
ARXIV_MIN_INTERVAL = 3.0
USER_AGENT = (
    "ARS-Codex-ZH/1.1.0 (academic research; "
    "mailto:free-academic-search@users.noreply.github.com)"
)

PAPER_FIELDS = [
    "source", "id", "title", "authors", "year", "date", "venue",
    "citationCount", "doi", "pmid", "arxivId", "url", "pdfUrl",
    "openAccessPdf", "abstract", "externalIds", "categories",
]


class LiteratureError(Exception):
    """A user-visible literature operation failure."""


def _paper(**fields: Any) -> dict[str, Any]:
    paper: dict[str, Any] = {key: fields.get(key) for key in PAPER_FIELDS}
    paper["authors"] = paper["authors"] or []
    return paper


def normalize_doi(doi: str | None) -> str:
    text = (doi or "").strip().lower()
    for prefix in (
        "doi:",
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
    ):
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    return urllib.parse.unquote(text).strip()


def normalize_title(title: str | None) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (title or "").lower())


def _http_get_bytes(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> tuple[bytes, dict[str, str]]:
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), {k: v for k, v in resp.headers.items()}
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise LiteratureError(f"HTTP {exc.code} for {url}") from exc
        except urllib.error.URLError as exc:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise LiteratureError(f"network error for {url}: {exc.reason}") from exc
    raise LiteratureError(f"request failed after {retries} attempts: {url}")


def _http_get_json(url: str, headers: dict[str, str] | None = None) -> Any:
    data, _ = _http_get_bytes(url, headers=headers)
    return json.loads(data.decode("utf-8", "replace"))


# --- search sources ---------------------------------------------------------
def search_arxiv(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict[str, Any]]:
    time.sleep(ARXIV_MIN_INTERVAL)  # arXiv ToU pacing floor
    params = {"search_query": f"all:{query}", "start": 0, "max_results": max_results}
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    data, _ = _http_get_bytes(url)
    root = ET.fromstring(data)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    papers: list[dict[str, Any]] = []
    for entry in root.findall("a:entry", ns):
        id_url = entry.findtext("a:id", "", ns) or ""
        arxiv_id = id_url.rsplit("/", 1)[-1] if id_url else ""
        title = " ".join((entry.findtext("a:title", "", ns) or "").split())
        authors = [a.findtext("a:name", "", ns) or "" for a in entry.findall("a:author", ns)]
        published = entry.findtext("a:published", "", ns) or ""
        year = int(published[:4]) if len(published) >= 4 else None
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else ""
        papers.append(
            _paper(source="arxiv", id=arxiv_id, title=title, authors=authors,
                   year=year, arxivId=arxiv_id, url=id_url, pdfUrl=pdf_url)
        )
    return papers


def search_pubmed(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict[str, Any]]:
    term = query
    if year_from:
        term = f"{term} AND {year_from}:3000[dp]"
    esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": term, "retmax": max_results, "retmode": "json"}
    )
    payload = _http_get_json(esearch)
    pmids = payload.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return []
    esummary = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}
    )
    summary = _http_get_json(esummary)
    result = summary.get("result", {})
    papers: list[dict[str, Any]] = []
    for pmid in pmids:
        item = result.get(pmid, {})
        authors = [a.get("name", "") for a in item.get("authors", [])]
        year = None
        m = re.match(r"(\d{4})", item.get("pubdate", ""))
        if m:
            year = int(m.group(1))
        doi = ""
        eloc = item.get("elocationid", "") or ""
        if eloc.startswith("doi "):
            doi = eloc[4:]
        papers.append(
            _paper(source="pubmed", id=pmid, title=item.get("title", ""), authors=authors,
                   year=year, pmid=pmid, doi=doi,
                   url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
        )
    return papers


def search_semantic_scholar(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict[str, Any]]:
    fields = "title,authors,year,externalIds,openAccessPdf,abstract,venue,citationCount,url"
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
        {"query": query, "limit": max_results, "fields": fields}
    )
    payload = _http_get_json(url)
    papers: list[dict[str, Any]] = []
    for item in payload.get("data", []):
        external = item.get("externalIds") or {}
        arxiv_id = external.get("ArXiv") or ""
        pmid = external.get("PubMed") or ""
        pdf_url = (item.get("openAccessPdf") or {}).get("url", "")
        papers.append(
            _paper(source="semantic-scholar", id=str(item.get("paperId", "")),
                   title=item.get("title", ""),
                   authors=[a.get("name", "") for a in (item.get("authors") or [])],
                   year=item.get("year"), venue=item.get("venue"),
                   citationCount=item.get("citationCount"),
                   doi=external.get("DOI", ""), pmid=str(pmid) if pmid else "",
                   arxivId=arxiv_id, url=item.get("url", ""), openAccessPdf=pdf_url,
                   abstract=item.get("abstract", ""))
        )
    return papers
def search_rxiv(server: str, query: str, max_results: int = 10, year_from: int | None = None) -> list[dict[str, Any]]:
    if server not in {"biorxiv", "medrxiv"}:
        raise LiteratureError(f"unsupported rxiv server: {server}")
    url = f"https://api.biorxiv.org/details/{server}/{urllib.parse.quote(query)}/0/{max_results}"
    payload = _http_get_json(url)
    papers: list[dict[str, Any]] = []
    for item in payload.get("collection", []):
        year = None
        if item.get("date"):
            year = int(item["date"][:4])
        doi = item.get("doi", "") or ""
        authors = [a.strip() for a in (item.get("authors", "") or "").split(";") if a.strip()]
        papers.append(
            _paper(source=server, id=doi, title=item.get("title", ""), authors=authors,
                   year=year, doi=doi,
                   url=f"https://doi.org/{doi}" if doi else "")
        )
    return papers


def search_crossref(query: str, max_results: int = 10, year_from: int | None = None) -> list[dict[str, Any]]:
    params = {"query": query, "rows": max_results,
              "select": "DOI,title,author,issued,container-title,URL"}
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    payload = _http_get_json(url, headers={"mailto": "free-academic-search@users.noreply.github.com"})
    papers: list[dict[str, Any]] = []
    for item in payload.get("message", {}).get("items", []):
        year = None
        issued = (item.get("issued") or {}).get("date-parts") or []
        if issued and issued[0] and issued[0][0]:
            year = issued[0][0]
        authors = []
        for a in item.get("author", []):
            name = (a.get("given", "") + " " + a.get("family", "")).strip()
            if name:
                authors.append(name)
        title_list = item.get("title") or [""]
        papers.append(
            _paper(source="crossref", id=item.get("DOI", ""), title=title_list[0] if title_list else "",
                   authors=authors, year=year, venue=(item.get("container-title") or [""])[0],
                   doi=item.get("DOI", ""), url=item.get("URL", ""))
        )
    return papers


SOURCE_FUNCS: dict[str, Callable[..., list[dict[str, Any]]]] = {
    "arxiv": search_arxiv,
    "pubmed": search_pubmed,
    "semantic-scholar": search_semantic_scholar,
    "biorxiv": lambda q, **kw: search_rxiv("biorxiv", q, **kw),
    "medrxiv": lambda q, **kw: search_rxiv("medrxiv", q, **kw),
    "crossref": search_crossref,
}


def merge_paper_lists(lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    seen_doi: dict[str, dict[str, Any]] = {}
    seen_arxiv: dict[str, dict[str, Any]] = {}
    seen_title: dict[str, dict[str, Any]] = {}
    merged: list[dict[str, Any]] = []
    for lst in lists:
        for paper in lst:
            key: tuple[str, str] | None = None
            if paper.get("doi"):
                key = ("doi", normalize_doi(paper["doi"]))
            elif paper.get("arxivId"):
                key = ("arxiv", paper["arxivId"].lower())
            elif paper.get("title"):
                key = ("title", normalize_title(paper["title"]))
            if not key:
                merged.append(paper)
                continue
            bucket = {"doi": seen_doi, "arxiv": seen_arxiv, "title": seen_title}[key[0]]
            if key in bucket:
                base = bucket[key]
                for field in PAPER_FIELDS:
                    if not base.get(field) and paper.get(field):
                        base[field] = paper[field]
            else:
                bucket[key] = paper
                merged.append(paper)
    return merged


# --- CLI --------------------------------------------------------------------


def _format_search_markdown(results: list[dict[str, Any]]) -> str:
    if not results:
        return "（未检索到结果）"
    lines = [f"共 {len(results)} 条去重后的结果：", ""]
    for i, paper in enumerate(results, start=1):
        lines.append(f"### {i}. {paper.get('title') or '(无标题)'}")
        authors = "、".join(paper.get("authors") or []) or "（作者未知）"
        year = paper.get("year")
        venue = paper.get("venue") or ""
        bits = [authors]
        if year:
            bits.append(str(year))
        if venue:
            bits.append(venue)
        lines.append(f"- 作者/年份/期刊：{'；'.join(bits)}")
        lines.append(f"- 来源：{paper.get('source')}")
        if paper.get("doi"):
            lines.append(f"- DOI：`{paper['doi']}`")
        if paper.get("arxivId"):
            lines.append(f"- arXiv ID：`{paper['arxivId']}`")
        if paper.get("pdfUrl") or paper.get("openAccessPdf"):
            lines.append(f"- 开放 PDF：{paper.get('pdfUrl') or paper.get('openAccessPdf')}")
        if paper.get("url"):
            lines.append(f"- 链接：{paper['url']}")
        if paper.get("abstract"):
            lines.append(f"- 摘要：{paper['abstract'][:200]}")
        lines.append("")
    return "\n".join(lines)
def cmd_search(args: argparse.Namespace) -> int:
    sources = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in sources if s not in SOURCE_FUNCS]
    if unknown:
        print(json.dumps({"error": f"unknown sources: {', '.join(unknown)}"}, ensure_ascii=False))
        return 2
    lists: list[list[dict[str, Any]]] = []
    warnings: list[str] = []
    for source in sources:
        try:
            lists.append(SOURCE_FUNCS[source](args.query, max_results=args.max_results, year_from=args.year_from))
        except Exception as exc:
            warnings.append(f"{source}: {exc}")
    merged = merge_paper_lists(lists)
    if args.json:
        print(json.dumps({"query": args.query, "sources": sources, "total": len(merged),
                          "warnings": warnings, "papers": merged}, ensure_ascii=False))
    else:
        if warnings:
            print("（部分数据源失败）")
            for warning in warnings:
                print(f"- {warning}")
            print()
        print(_format_search_markdown(merged))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ars_codex_literature",
                                     description="ARS-Codex 文献检索 / 下载 / 全文读取")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="多源文献检索")
    p_search.add_argument("--query", required=True, help="检索词")
    p_search.add_argument("--sources", default="arxiv,pubmed,semantic-scholar,biorxiv,medrxiv,crossref",
                          help="逗号分隔的数据源")
    p_search.add_argument("--max-results", type=int, default=10)
    p_search.add_argument("--year-from", type=int, default=None)
    p_search.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "search":
        return cmd_search(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 运行确认通过**

Run: `python -m pytest skills/academic-research-suite/codex/tests/test_literature.py -v`
Expected: 8 passed（`normalize_doi` + 5 个数据源解析 + merge + `test_cli_search_prints_markdown`）。

- [ ] **Step 5: 提交**

```bash
git add skills/academic-research-suite/codex/scripts/ars_codex_literature.py skills/academic-research-suite/codex/tests/test_literature.py
git commit -m "feat: add multi-source literature search (ars-search)"
```
---

### Task 2: 下载子命令（TDD）

**Files:**
- Modify: `skills/academic-research-suite/codex/tests/test_literature.py`（追加下载测试）
- Modify: `skills/academic-research-suite/codex/scripts/ars_codex_literature.py`（新增下载区段）

**Interfaces:**
- Consumes: Task 1 的 `normalize_doi`、`_http_get_bytes`、`LiteratureError`、`main`/`build_parser`。
- Produces:
  - `is_pdf_payload(data: bytes) -> bool`
  - `SCIHUB_MIRRORS: list[str]`
  - `DEFAULT_UNPAYWALL_EMAIL: str`
  - `_save_pdf(data: bytes, out_dir: str | Path, filename: str) -> dict[str, Any]`
  - `download_pdf_by_url(url: str, out_dir: str | Path, filename: str | None = None) -> dict[str, Any]`（返回含 `ok`/`path`/`bytes`/`source_url`）
  - `lookup_unpaywall(doi: str, email: str | None = None) -> str | None`
  - `_download_scihub(doi: str, out_dir: str | Path) -> dict[str, Any]`
  - `download_pdf_by_doi(doi: str, out_dir: str | Path, allow_scihub: bool = False, unpaywall_email: str | None = None) -> dict[str, Any]`（返回含 `via`：`direct`/`unpaywall`/`scihub`）

- [ ] **Step 1: 写失败测试**

在 `skills/academic-research-suite/codex/tests/test_literature.py` 顶部把 `import json` 改为：

```python
import json
import pytest
```

（即新增一行 `import pytest`。）然后在文件末尾追加：

```python
def test_is_pdf_payload() -> None:
    mod = _load()
    assert mod.is_pdf_payload(b"%PDF-1.4\n...") is True
    assert mod.is_pdf_payload(b"<html>") is False


def test_download_by_url_writes_pdf(tmp_path, monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(b"%PDF-1.4\nx"))
    result = mod.download_pdf_by_url("https://example.com/paper.pdf", str(tmp_path))
    assert result["ok"] is True
    assert (tmp_path / "paper.pdf").read_bytes() == b"%PDF-1.4\nx"
    assert result["bytes"] == 10


def test_download_by_url_rejects_non_pdf(tmp_path, monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", _fake_bytes(b"<html>"))
    with pytest.raises(mod.LiteratureError):
        mod.download_pdf_by_url("https://example.com/paper", str(tmp_path))


def test_download_by_doi_uses_unpaywall_when_direct_not_pdf(tmp_path, monkeypatch) -> None:
    mod = _load()
    calls: list[str] = []

    def _get(url, **kw):
        calls.append(url)
        return b"<html>not a pdf</html>", {}

    monkeypatch.setattr(mod, "_http_get_bytes", _get)
    monkeypatch.setattr(mod, "lookup_unpaywall", lambda doi, email=None: "https://oa.example/paper.pdf")
    monkeypatch.setattr(mod, "download_pdf_by_url",
                        lambda url, out_dir, filename=None: {"ok": True, "path": str(tmp_path / "f.pdf"),
                                                             "bytes": 3, "source_url": url})
    result = mod.download_pdf_by_doi("10.1000/123", str(tmp_path))
    assert result["via"] == "unpaywall"
    assert any("doi.org" in c for c in calls)


def test_download_by_doi_refuses_scihub_by_default(tmp_path, monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", lambda url, **kw: (b"<html></html>", {}))
    monkeypatch.setattr(mod, "lookup_unpaywall", lambda doi, email=None: None)

    def bad(*a, **k):
        raise AssertionError("scihub must not be called by default")

    monkeypatch.setattr(mod, "_download_scihub", bad)
    with pytest.raises(mod.LiteratureError):
        mod.download_pdf_by_doi("10.1000/123", str(tmp_path))


def test_download_by_doi_calls_scihub_when_opted_in(tmp_path, monkeypatch) -> None:
    mod = _load()
    monkeypatch.setattr(mod, "_http_get_bytes", lambda url, **kw: (b"<html></html>", {}))
    monkeypatch.setattr(mod, "lookup_unpaywall", lambda doi, email=None: None)
    monkeypatch.setattr(mod, "_download_scihub",
                        lambda doi, out_dir: {"ok": True, "path": str(tmp_path / "s.pdf"),
                                              "bytes": 3, "source_url": "scihub://x"})
    result = mod.download_pdf_by_doi("10.1000/123", str(tmp_path), allow_scihub=True)
    assert result["via"] == "scihub"


def test_cli_download_requires_doi_or_url(capsys) -> None:
    mod = _load()
    rc = mod.main(["download"])
    assert rc != 0
```
- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest skills/academic-research-suite/codex/tests/test_literature.py -v`
Expected: 新增 7 个测试失败（`AttributeError: module has no attribute 'is_pdf_payload'` 等），原有 8 个通过。

- [ ] **Step 3: 写最小实现**

在 `skills/academic-research-suite/codex/scripts/ars_codex_literature.py` 中：

（a）模块常量区（`PAPER_FIELDS` 之后）追加：

```python
SCIHUB_MIRRORS = ["https://sci-hub.se", "https://sci-hub.st", "https://sci-hub.ru"]
DEFAULT_UNPAYWALL_EMAIL = "free-academic-search@users.noreply.github.com"
```

（b）在 `normalize_title` 之后、`# --- search sources ---` 之前追加：

```python
def is_pdf_payload(data: bytes) -> bool:
    return data[:5] == b"%PDF-"
```

（c）在 `merge_paper_lists` 与 `# --- CLI ---` 之间插入下载区段：

```python
# --- download ---------------------------------------------------------------


def _save_pdf(data: bytes, out_dir: str | Path, filename: str) -> dict[str, Any]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / filename
    dest.write_bytes(data)
    return {"ok": True, "path": str(dest), "bytes": len(data)}


def download_pdf_by_url(url: str, out_dir: str | Path, filename: str | None = None) -> dict[str, Any]:
    data, _ = _http_get_bytes(url)
    if not is_pdf_payload(data):
        raise LiteratureError(f"not a PDF payload from {url}")
    name = filename or (url.rsplit("/", 1)[-1].split("?")[0] or "paper.pdf")
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    result = _save_pdf(data, out_dir, name)
    result["source_url"] = url
    return result


def lookup_unpaywall(doi: str, email: str | None = None) -> str | None:
    email = email or os.environ.get("ARS_UNPAYWALL_EMAIL") or DEFAULT_UNPAYWALL_EMAIL
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(normalize_doi(doi))}?email={urllib.parse.quote(email)}"
    payload = _http_get_json(url)
    best = payload.get("best_oa_location") or {}
    return best.get("url_for_pdf") or best.get("url")


def _download_scihub(doi: str, out_dir: str | Path) -> dict[str, Any]:
    encoded = urllib.parse.quote(normalize_doi(doi), safe="")
    for mirror in SCIHUB_MIRRORS:
        try:
            page_url = f"{mirror}/{encoded}"
            html, _ = _http_get_bytes(page_url)
            text = html.decode("utf-8", "replace")
            match = re.search(r'(?:<iframe[^>]+src|<embed[^>]+src)="([^"]+\.pdf[^"]*)"', text, re.I)
            if not match:
                continue
            pdf_url = urllib.parse.urljoin(page_url, match.group(1))
            return download_pdf_by_url(pdf_url, out_dir, filename=f"{normalize_doi(doi).replace('/', '_')}.pdf")
        except (LiteratureError, urllib.error.URLError):
            continue
    raise LiteratureError("Sci-Hub download failed on all mirrors")


def download_pdf_by_doi(
    doi: str,
    out_dir: str | Path,
    allow_scihub: bool = False,
    unpaywall_email: str | None = None,
) -> dict[str, Any]:
    norm = normalize_doi(doi)
    filename = f"{norm.replace('/', '_')}.pdf"
    # 1. direct resolver -> PDF
    try:
        direct = f"https://doi.org/{urllib.parse.quote(norm, safe='')}"
        data, _ = _http_get_bytes(direct)
        if is_pdf_payload(data):
            result = _save_pdf(data, out_dir, filename)
            result["via"] = "direct"
            result["source_url"] = direct
            return result
    except LiteratureError:
        pass
    # 2. Unpaywall legal OA
    try:
        oa_url = lookup_unpaywall(norm, unpaywall_email)
        if oa_url:
            result = download_pdf_by_url(oa_url, out_dir, filename=filename)
            result["via"] = "unpaywall"
            return result
    except LiteratureError:
        pass
    # 3. Sci-Hub (opt-in only)
    if allow_scihub:
        try:
            result = _download_scihub(norm, out_dir)
            result["via"] = "scihub"
            return result
        except LiteratureError:
            pass
    raise LiteratureError(
        f"no downloadable PDF found for DOI {norm} "
        "(legal OA only; pass --allow-scihub to try Sci-Hub)"
    )
```
（d）`cmd_search` 之后、`build_parser` 之前追加：

```python
def cmd_download(args: argparse.Namespace) -> int:
    try:
        if args.doi:
            result = download_pdf_by_doi(args.doi, args.out, allow_scihub=args.allow_scihub,
                                         unpaywall_email=args.unpaywall_email)
        elif args.url:
            result = download_pdf_by_url(args.url, args.out)
        else:
            raise LiteratureError("需要 --doi 或 --url 参数")
    except LiteratureError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    if result.get("via") == "scihub":
        print("注意：本次下载经由 Sci-Hub，请确保你对该内容拥有合法访问权。", file=sys.stderr)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"已下载 PDF：{result['path']}（{result['bytes']} 字节，来源：{result.get('source_url')}，渠道：{result.get('via', 'url')}）")
    return 0
```

（e）`build_parser` 中 `p_search` 之后追加：

```python
    p_download = sub.add_parser("download", help="下载 PDF")
    p_download.add_argument("--doi", default=None, help="DOI")
    p_download.add_argument("--url", default=None, help="PDF URL")
    p_download.add_argument("--out", default=".", help="输出目录")
    p_download.add_argument("--allow-scihub", action="store_true",
                            help="显式允许 Sci-Hub 回退（默认关；请确保合法访问权）")
    p_download.add_argument("--unpaywall-email", default=None)
    p_download.add_argument("--json", action="store_true")
```

（f）`main` 中 `if args.command == "search":` 之后追加：

```python
    if args.command == "download":
        return cmd_download(args)
```

（g）模块顶部导入区把 `import json` 改为：

```python
import json
import os
```

- [ ] **Step 4: 运行确认通过**

Run: `python -m pytest skills/academic-research-suite/codex/tests/test_literature.py -v`
Expected: 15 passed。

- [ ] **Step 5: 提交**

```bash
git add skills/academic-research-suite/codex/scripts/ars_codex_literature.py skills/academic-research-suite/codex/tests/test_literature.py
git commit -m "feat: add legal-OA-first PDF download (ars-download)"
```
---

### Task 3: 读取子命令（TDD）

**Files:**
- Modify: `skills/academic-research-suite/codex/tests/test_literature.py`（追加读取测试）
- Modify: `skills/academic-research-suite/codex/scripts/ars_codex_literature.py`（新增读取区段）

**Interfaces:**
- Consumes: Task 1-2 的 `main`/`build_parser`/`LiteratureError`。
- Produces:
  - `extract_pdf_text(path: str | Path, max_chars: int | None = None, force_fallback: bool = False) -> dict[str, Any]`（返回含 `path`/`chars`/`mode`/`text`，`mode` ∈ {`pypdf`, `stdlib-fallback`}）
  - `_extract_pdf_text_stdlib(data: bytes) -> str`

- [ ] **Step 1: 写失败测试**

在 `skills/academic-research-suite/codex/tests/test_literature.py` 顶部把 `import json` 改为：

```python
import json
import zlib
```

在 `RXIV_JSON` 常量之后追加辅助函数：

```python
def _minimal_pdf() -> bytes:
    content = zlib.compress(b"BT (Hello World) Tj ET")
    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n"
        b"4 0 obj<</Length " + str(len(content)).encode() + b"/Filter/FlateDecode>>stream\n"
        + content + b"\nendstream\nendobj\n"
        b"trailer<</Root 1 0 R>>\n%%EOF\n"
    )
    return pdf
```

在文件末尾追加：

```python
def test_extract_pdf_text_stdlib_fallback(tmp_path) -> None:
    mod = _load()
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(_minimal_pdf())
    result = mod.extract_pdf_text(str(pdf), force_fallback=True)
    assert result["mode"] == "stdlib-fallback"
    assert "Hello World" in result["text"]


def test_extract_pdf_text_uses_pypdf_when_available(tmp_path) -> None:
    pytest.importorskip("pypdf")
    mod = _load()
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(_minimal_pdf())
    result = mod.extract_pdf_text(str(pdf))
    assert result["mode"] == "pypdf"


def test_cli_read_prints_text(tmp_path, monkeypatch, capsys) -> None:
    mod = _load()
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(_minimal_pdf())
    monkeypatch.setattr(mod, "extract_pdf_text",
                        lambda path, max_chars=None, force_fallback=False: {
                            "path": str(pdf), "chars": 11, "mode": "stdlib-fallback",
                            "text": "Hello World"})
    rc = mod.main(["read", "--file", str(pdf)])
    assert rc == 0
    assert "Hello World" in capsys.readouterr().out
```
- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest skills/academic-research-suite/codex/tests/test_literature.py -v`
Expected: 新增 3 个失败（`AttributeError: module has no attribute 'extract_pdf_text'` 等），原有 15 个通过。

- [ ] **Step 3: 写最小实现**

在 `skills/academic-research-suite/codex/scripts/ars_codex_literature.py` 中：

（a）`# --- download ---` 区段之后、`# --- CLI ---` 之前插入读取区段：

```python
# --- read -------------------------------------------------------------------


_TEXT_OP_RE = re.compile(r"\((?:\\.|[^\\()])*\)\s*Tj|(?:\((?:\\.|[^\\()])*\)\s*)+TJ")
_ESCAPE_MAP = {"n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f",
               "(": "(", ")": ")", "\\": "\\"}


def _extract_pdf_text_stdlib(data: bytes) -> str:
    out: list[str] = []
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        raw = match.group(1)
        try:
            content = zlib.decompress(raw)
        except Exception:
            content = raw
        text = content.decode("latin-1", "replace")
        for op in _TEXT_OP_RE.finditer(text):
            for chunk in re.findall(r"\((?:\\.|[^\\()])*\)", op.group(0)):
                inner = chunk[1:-1]
                inner = re.sub(
                    r"\\(.)",
                    lambda m: _ESCAPE_MAP.get(m.group(1), m.group(1)),
                    inner,
                )
                out.append(inner)
    return "".join(out)


def extract_pdf_text(
    path: str | Path,
    max_chars: int | None = None,
    force_fallback: bool = False,
) -> dict[str, Any]:
    data = Path(path).read_bytes()
    text = ""
    mode = "stdlib-fallback"
    if not force_fallback:
        try:
            import io
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            mode = "pypdf"
        except Exception:
            text = ""
            mode = "stdlib-fallback"
    if mode == "stdlib-fallback":
        text = _extract_pdf_text_stdlib(data)
    if max_chars is not None:
        text = text[:max_chars]
    return {"path": str(path), "chars": len(text), "mode": mode, "text": text}
```

（b）`cmd_download` 之后、`build_parser` 之前追加：

```python
def cmd_read(args: argparse.Namespace) -> int:
    try:
        result = extract_pdf_text(args.file, max_chars=args.max_chars, force_fallback=args.force_fallback)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"提取模式：{result['mode']}；字符数：{result['chars']}")
        print("--- 全文 ---")
        print(result["text"])
    return 0
```

（c）`build_parser` 中 `p_download` 之后追加：

```python
    p_read = sub.add_parser("read", help="本地 PDF 全文提取")
    p_read.add_argument("--file", required=True, help="PDF 文件路径")
    p_read.add_argument("--max-chars", type=int, default=None)
    p_read.add_argument("--force-fallback", action="store_true", help="强制使用内置降级提取器")
    p_read.add_argument("--json", action="store_true")
```

（d）`main` 中 `if args.command == "download":` 之后追加：

```python
    if args.command == "read":
        return cmd_read(args)
```

- [ ] **Step 4: 运行确认通过**

Run: `python -m pytest skills/academic-research-suite/codex/tests/test_literature.py -v`
Expected: 18 passed。

- [ ] **Step 5: 提交**

```bash
git add skills/academic-research-suite/codex/scripts/ars_codex_literature.py skills/academic-research-suite/codex/tests/test_literature.py
git commit -m "feat: add local PDF full-text extraction (ars-read)"
```
---

### Task 4: 命令配方 + SKILL.md + manifest + matrix + deep-research 联动

**Files:**
- Create: `skills/academic-research-suite/codex/commands/ars-search.md`
- Create: `skills/academic-research-suite/codex/commands/ars-download.md`
- Create: `skills/academic-research-suite/codex/commands/ars-read.md`
- Modify: `skills/academic-research-suite/SKILL.md`
- Modify: `skills/academic-research-suite/codex/full-runtime-manifest.json`
- Modify: `skills/academic-research-suite/codex/compatibility-matrix.md`
- Modify: `skills/academic-research-suite/codex/agents/deep-research-team.md`

**Interfaces:** 无新 Python 接口；依赖 Task 1-3 产生的命令别名与 `model_hint: "sonnet"`。

- [ ] **Step 1: 新增三个命令配方**

创建 `skills/academic-research-suite/codex/commands/ars-search.md`：

````markdown
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
````

创建 `skills/academic-research-suite/codex/commands/ars-download.md`：

````markdown
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
````

创建 `skills/academic-research-suite/codex/commands/ars-read.md`：

````markdown
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
````
- [ ] **Step 2: 更新 SKILL.md**

在 `skills/academic-research-suite/SKILL.md` 中：

（a）frontmatter 的 `description` 里「也用于 Claude 风格 ARS 命令别名」的别名清单中，把 `ars-rebuttal-audit, /ars-full。` 改为 `ars-rebuttal-audit, ars-search, ars-download, ars-read, /ars-full。`。

（b）在「Claude 风格别名路由」表格中 `ars-full` 行之后追加三行：

```markdown
| `/ars-search`, `ars-search` | `codex/commands/ars-search.md` | 多源文献检索（Semantic Scholar / PubMed / arXiv / bioRxiv / medRxiv / Crossref），去重合并后返回带 DOI / PDF 链接的条目 |
| `/ars-download`, `ars-download` | `codex/commands/ars-download.md` | 按 DOI 或 PDF URL 下载合法 PDF；默认只走合法开放获取，`--allow-scihub` 显式开启 Sci-Hub 回退 |
| `/ars-read`, `ars-read` | `codex/commands/ars-read.md` | 本地 PDF 全文提取，供综述、引用与写作阶段使用 |
```

（c）在「Claude 风格别名路由」小节之后、「Codex 运行时映射」小节之前插入新小节：

````markdown
## 文献检索与全文获取

本包原生提供免费的多源文献检索、合法下载与全文读取能力（无需 API key / 积分），
通过 `ars-search` / `ars-download` / `ars-read` 三个命令触发：

- `/ars-search`：跨 Semantic Scholar、PubMed、arXiv、bioRxiv、medRxiv、Crossref 多源检索，
  去重合并后返回带 DOI / PDF 链接的条目列表。
- `/ars-download`：按 DOI 或 PDF URL 下载 PDF 到本地。默认只走合法开放获取
  （直接 / arXiv OA → Unpaywall 合法 OA）；仅当用户显式传入 `--allow-scihub` 时才回退到
  Sci-Hub（请确保你对该内容拥有合法访问权）。
- `/ars-read`：提取本地 PDF 的全文文本，供综述、引用与写作阶段使用。

联动规则：在 `deep-research` 的 `lit-review` / `systematic-review` / `full` 模式及论文写作的
文献阶段，需要真实文献时优先使用 `ars-search` 检索、`ars-download` 下载合法全文、
`ars-read` 提取文本，再交给对应 agent 综合。

运行时：命令通过 `python3 skills/academic-research-suite/codex/scripts/ars_codex_literature.py ...`
调用，零第三方硬依赖；PDF 文本提取在已安装 `pypdf` 时质量更好。
````
- [ ] **Step 3: 更新 full-runtime-manifest.json**

在 `skills/academic-research-suite/codex/full-runtime-manifest.json` 的 `commands` 数组末尾（`ars-cache-invalidate` 行之后、`]` 之前）追加三个条目：

```json
    ,
    {"aliases": ["/ars-search", "ars-search"], "recipe": "codex/commands/ars-search.md", "workflow": "deep-research", "mode": "search", "model_hint": "sonnet"},
    {"aliases": ["/ars-download", "ars-download"], "recipe": "codex/commands/ars-download.md", "workflow": "deep-research", "mode": "download", "model_hint": "sonnet"},
    {"aliases": ["/ars-read", "ars-read"], "recipe": "codex/commands/ars-read.md", "workflow": "deep-research", "mode": "read", "model_hint": "sonnet"}
```

同时把 `workflows.deep-research.modes` 数组改为：

```json
      "modes": ["full", "quick", "socratic", "review", "lit-review", "three-way-scan", "fact-check", "systematic-review", "search", "download", "read"],
```

- [ ] **Step 4: 更新 compatibility-matrix.md**

在 `skills/academic-research-suite/codex/compatibility-matrix.md` 的矩阵表格末尾追加一行：

```markdown
| 文献检索 / 下载 / 读取 | 适配层新增 `ars-search` / `ars-download` / `ars-read`（上游仅做引用核验，不做全文检索与下载） | 全运行时 manifest 登记同一命令路由 | new | `codex/scripts/ars_codex_literature.py`、`codex/commands/ars-*.md`、`SKILL.md` | adapter pytest（mock 网络） | 真实网络响应与速率限制需真实环境冒烟；Sci-Hub 默认关 |
```

- [ ] **Step 5: 更新 deep-research-team.md**

在 `skills/academic-research-suite/codex/agents/deep-research-team.md` 末尾追加：

````markdown
## 文献获取

`lit-review` / `systematic-review` / `full` 模式需要真实文献时，优先使用适配层
`ars-search` / `ars-download` / `ars-read` 命令（用法见 `SKILL.md`「文献检索与全文获取」）：
先 `ars-search` 检索，再 `ars-download` 下载合法全文，`ars-read` 提取文本后交给对应 agent 综合。
下载默认只走合法开放获取渠道；Sci-Hub 需用户显式同意后才可尝试。
````

- [ ] **Step 6: 运行验证**

Run: `python -m pytest skills/academic-research-suite/codex/tests`
Expected: 既有 43 个通过保持不变，新增 18 个全部通过，6 个既有失败保持原样（不新增失败）。含 `test_command_model_hints_match_upstream_frontmatter_semantics` 与 `test_announce_reports_canonical_aliases_without_slashes`。

- [ ] **Step 7: 提交**

```bash
git add skills/academic-research-suite/codex/commands/ skills/academic-research-suite/SKILL.md skills/academic-research-suite/codex/full-runtime-manifest.json skills/academic-research-suite/codex/compatibility-matrix.md skills/academic-research-suite/codex/agents/deep-research-team.md
git commit -m "feat: register ars-search/ars-download/ars-read in router, manifest, and research guidance"
```
---

### Task 5: 版本提升至 1.1.0 + CHANGELOG + README

**Files:**
- Modify: `VERSION`
- Modify: `skills/academic-research-suite/SKILL.md`（`metadata.version`）
- Modify: `skills/academic-research-suite/manifest.json`（`adapter_version`）
- Modify: `plugins/ars-codex-zh/.codex-plugin/plugin.json`（`version`）
- Modify: `CHANGELOG.md`
- Modify: `README_ZH-CN.md`

**Interfaces:** 无。

- [ ] **Step 1: 四处版本号改为 1.1.0**

- `VERSION`：内容改为 `1.1.0`。
- `skills/academic-research-suite/SKILL.md`：`metadata.version` 由 `"1.0.1"` 改为 `"1.1.0"`。
- `skills/academic-research-suite/manifest.json`：`adapter_version` 由 `"1.0.1"` 改为 `"1.1.0"`。
- `plugins/ars-codex-zh/.codex-plugin/plugin.json`：`version` 由 `"1.0.1"` 改为 `"1.1.0"`。

- [ ] **Step 2: CHANGELOG.md 归档**

把 `## Unreleased` 段改为：

```markdown
## Unreleased

## [1.1.0] - 2026-08-27

### What's Changed
- Added native literature search / legal download / full-text read commands:
  `ars-search` (multi-source search across Semantic Scholar, PubMed, arXiv,
  bioRxiv/medRxiv, Crossref, with dedupe/merge), `ars-download` (DOI/URL → PDF,
  legal open-access first, Sci-Hub only via explicit `--allow-scihub`), and
  `ars-read` (local PDF text extraction, `pypdf` when available with a built-in
  degraded fallback). Zero hard third-party dependencies (stdlib `urllib`).
- Wired the three commands into the deep-research workflow guidance and the
  full-runtime manifest, and documented them in the SKILL.md router, the
  compatibility matrix, and the Chinese README.
- Bumped the Codex package version to `1.1.0` (MINOR) for the new adapter-layer
  behavior.
```

- [ ] **Step 3: README_ZH-CN.md 新增功能清单**

在 `README_ZH-CN.md` 的「中文版新增功能」清单末尾追加一条：

```markdown
- **文献检索 / 下载 / 全文读取**：对话内可用 `ars-search` 跨多源检索文献、`ars-download` 下载合法开放获取 PDF、`ars-read` 提取本地 PDF 全文（无需 API key；Sci-Hub 默认关闭，仅显式 `--allow-scihub` 才启用）。
```

同时把该小节标题 `## 中文版新增功能（v1.0.0）` 改为 `## 中文版新增功能（v1.1.0）`。

- [ ] **Step 4: 运行验证**

Run: `python -m pytest skills/academic-research-suite/codex/tests`
Expected: 全部通过（版本一致性由 `ars_codex_quality_gates.check_manifest` 校验，本任务后应通过）。

- [ ] **Step 5: 提交**

```bash
git add VERSION skills/academic-research-suite/SKILL.md skills/academic-research-suite/manifest.json plugins/ars-codex-zh/.codex-plugin/plugin.json CHANGELOG.md README_ZH-CN.md
git commit -m "chore: bump package version to 1.1.0 for literature search/download/read"
```
---

### Task 6: 双副本同步 + 防护基线 + 全量验证

**Files:**
- Modify: `plugins/ars-codex-zh/skills/`（整体复制 `skills/academic-research-suite/` 覆盖之）
- Modify: `scripts/localization_guard.manifest.json`（由 guard `--update` 生成）
- Modify: `scripts/upstream_baseline.json`（由 guard `--update` 生成）

**Interfaces:** 无新代码。

- [ ] **Step 1: 同步插件副本**

从仓库根目录运行（PowerShell）：

```powershell
robocopy ".\skills\academic-research-suite" ".\plugins\ars-codex-zh\skills\academic-research-suite" /MIR /NFL /NDL /NJH /NJS /NP
```

Expected: 退出码 0 或 1（1 = 有文件被复制，属正常）；两边逐字节一致。

- [ ] **Step 2: 更新防护基线**

Run: `python scripts/verify_localization_guard.py --update`
Expected: 输出写入受保护文件哈希与上游基线；`[OK] wrote ... protected-file hashes and upstream baseline @ <commit>`。

- [ ] **Step 3: 防护校验**

Run: `python scripts/verify_localization_guard.py --check`
Expected: 退出码 0；无 `[FAIL]`；无 `[DRIFT]` 报出「上游变更文件 → 适配文件」命中（新增命令不引用上游 `ars/` 文件，故不应有 drift）。

- [ ] **Step 4: 双副本一致性校验**

Run: `python scripts/verify_localization_guard.py --check`
Expected: 校验输出包含插件副本与源一致（guard 内置该检查）。

- [ ] **Step 5: 全量测试**

Run: `python -m pytest skills/academic-research-suite/codex/tests`
Expected: 既有 43 个通过保持不变，新增 18 个测试全部通过，6 个既有失败保持原样（不新增失败）。

- [ ] **Step 6: 提交**

```bash
git add -A
git commit -m "chore: sync plugin copy and refresh localization guard baseline for v1.1.0"
```

---

## Execution Handoff

计划完成。实现者在 `codex/zh-literature` worktree 内按任务顺序执行（先创建 worktree：`git worktree add -b codex/zh-literature ../academic-research-skills-codex-zh.worktrees/zh-literature main`），每任务 TDD 后提交；完成后按仓库治理合并回 `main`、打 tag `v1.1.0`、推送，并同步插件缓存。

## Self-Review

- Spec 覆盖：搜索（Task 1）、下载（Task 2）、读取（Task 3）、命令 + SKILL.md + manifest + matrix + deep-research 联动（Task 4）、版本 1.1.0 + CHANGELOG + README（Task 5）、双副本 + guard（Task 6）。全部 spec 小节均有对应任务。
- 占位符扫描：无 TBD/TODO。
- 类型一致性：`download_pdf_by_doi` / `download_pdf_by_url` / `extract_pdf_text` 等签名在测试与实现中一致；`via` 取值与测试断言一致；命令 `aliases[1]` 与 `model_hint: "sonnet"` 满足既有测试约束。

