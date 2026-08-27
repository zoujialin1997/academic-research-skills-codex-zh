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
