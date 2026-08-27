from __future__ import annotations

import importlib.util
import json
import pytest
import zlib
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

def test_extract_pdf_text_stdlib_fallback(tmp_path) -> None:
    mod = _load()
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(_minimal_pdf())
    result = mod.extract_pdf_text(str(pdf), force_fallback=True)
    assert result["mode"] == "stdlib-fallback"
    assert "Hello World" in result["text"]


def test_extract_pdf_text_uses_pypdf_when_available(tmp_path) -> None:
    pytest.importorskip("pypdf")
    from pypdf import PdfWriter
    import io as _io
    mod = _load()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = _io.BytesIO()
    writer.write(buf)
    pdf = tmp_path / "sample_pypdf.pdf"
    pdf.write_bytes(buf.getvalue())
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

