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
