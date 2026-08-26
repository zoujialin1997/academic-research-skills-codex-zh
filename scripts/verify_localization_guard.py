#!/usr/bin/env python3
"""Verify the Chinese localization adaptation layer survives upstream syncs.

The vendored ARS suite under skills/academic-research-suite/ars/ is replaced
wholesale by every upstream sync. This tool protects the hand-maintained
localization / Codex adaptation layer (SKILL.md router, codex/ adapter,
plugin display strings, examples, and root docs) from being accidentally
overwritten during that process, and it enforces that upstream changes to
vendored content are re-adapted before the next commit.

Usage:
    python scripts/verify_localization_guard.py            # check (default)
    python scripts/verify_localization_guard.py --update   # refresh manifests
    python scripts/verify_localization_guard.py --quiet    # failures only

Check failures (non-zero exit) mean one of:
  1. a protected adaptation-layer file changed outside an intentional edit
     (run --update only after an intentional edit);
  2. the plugin copy under plugins/ars-codex-zh/skills/ drifted from the source
     skill tree (refresh it after every sync); or
  3. upstream vendored content changed since the last recorded baseline, so the
     corresponding adaptation must be re-checked and re-adapted (then run
     --update to record the new baseline).

--update records:
  * SHA-256 hashes of every protected adaptation-layer file, and
  * a baseline snapshot (upstream commit + per-file hashes) of the vendored
    ars/ tree that the current adaptation was validated against.
Run --update only after the adaptation is intentionally complete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GUARD_MANIFEST = Path(__file__).resolve().parent / "localization_guard.manifest.json"
UPSTREAM_BASELINE = Path(__file__).resolve().parent / "upstream_baseline.json"
# Transient / ignored paths and suffixes that must never enter manifests or
# cause drift (mirrors .gitignore). Kept out of protected files and the
# upstream snapshot so pytest caches and editor temp files are invisible.
IGNORED_DIRS = {"__pycache__", ".pytest_cache", ".context", ".mypy_cache", ".ruff_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".pyc~", ".tmp", ".swp"}

# Paths (relative to REPO_ROOT) that belong to the localization / Codex
# adaptation layer and must never be replaced by an upstream sync.
PROTECTED_TREES = [
    "skills/academic-research-suite/SKILL.md",
    "skills/academic-research-suite/agents/openai.yaml",
    "skills/academic-research-suite/codex",
    "plugins/ars-codex-zh/.codex-plugin/plugin.json",
    "examples",
    "README.md",
    "README_ZH-CN.md",
    "README_ZH-TW.md",
    "README_JA.md",
    "CHANGELOG.md",
    "GETTING_STARTED_ZH-CN.md",
]

# Adapted files that reference vendored upstream paths; used to flag which
# re-adaptation is needed when an upstream file changes.
ADAPTATION_REFERENCE_FILES = [
    "skills/academic-research-suite/SKILL.md",
    "skills/academic-research-suite/codex",
    "README.md",
    "README_ZH-CN.md",
    "README_ZH-TW.md",
    "README_JA.md",
    "CHANGELOG.md",
    "GETTING_STARTED_ZH-CN.md",
    "examples",
]

SOURCE_SKILL = REPO_ROOT / "skills/academic-research-suite"
PLUGIN_SKILL = REPO_ROOT / "plugins/ars-codex-zh/skills/academic-research-suite"
UPSTREAM_ROOT = SOURCE_SKILL / "ars"
SKILL_MANIFEST = SOURCE_SKILL / "manifest.json"


def is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    if parts & IGNORED_DIRS:
        return True
    return path.suffix.lower() in IGNORED_SUFFIXES
def sha256_file(path: Path) -> str:
    """SHA-256 of a file with line endings normalized (CRLF/CR -> LF).

    Keeps hashes stable across checkouts so guard results do not depend on
    core.autocrlf or the OS line-ending convention.
    """
    with path.open("rb") as handle:
        data = handle.read().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def iter_protected_files() -> list[Path]:
    files: list[Path] = []
    for rel in PROTECTED_TREES:
        candidate = REPO_ROOT / rel
        if candidate.is_file():
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(sorted(item for item in candidate.rglob("*") if item.is_file() and not is_ignored(item)))
        else:
            files.append(candidate)  # missing path: fail loudly
    return files


def build_guard_manifest() -> dict[str, str]:
    manifest: dict[str, str] = {}
    for path in iter_protected_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        manifest[rel] = sha256_file(path) if path.exists() else "MISSING"
    return dict(sorted(manifest.items()))


def snapshot_upstream() -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in UPSTREAM_ROOT.rglob("*"):
        if path.is_file() and not is_ignored(path):
            snapshot[path.relative_to(REPO_ROOT).as_posix()] = sha256_file(path)
    return snapshot


def current_upstream_commit() -> tuple[str, str]:
    data = json.loads(SKILL_MANIFEST.read_text(encoding="utf-8"))
    repos = data.get("source_repositories", [])
    commit = repos[0].get("commit", "unknown") if repos else "unknown"
    date = data.get("generated_date", "")
    return commit, date


def check_guard_manifest(quiet: bool) -> bool:
    if not GUARD_MANIFEST.exists():
        print(f"guard manifest missing: {GUARD_MANIFEST.name} (run --update)")
        return False
    expected = json.loads(GUARD_MANIFEST.read_text(encoding="utf-8"))
    ok = True
    for rel, want in expected.items():
        path = REPO_ROOT / rel
        got = sha256_file(path) if path.exists() else "MISSING"
        if got != want:
            ok = False
            print(f"[FAIL] protected file changed: {rel}")
    for path in iter_protected_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel not in expected:
            ok = False
            print(f"[FAIL] protected file not recorded (run --update): {rel}")
    if ok and not quiet:
        print(f"[OK] {len(expected)} protected files intact")
    return ok


def check_dual_copy(quiet: bool) -> bool:
    src_files = {
        path.relative_to(SOURCE_SKILL).as_posix(): path
        for path in SOURCE_SKILL.rglob("*")
        if path.is_file() and not is_ignored(path)
    }
    dst_files = {
        path.relative_to(PLUGIN_SKILL).as_posix(): path
        for path in PLUGIN_SKILL.rglob("*")
        if path.is_file() and not is_ignored(path)
    }
    ok = True
    for rel, src in sorted(src_files.items()):
        dst = PLUGIN_SKILL / rel
        if not dst.exists() or sha256_file(src) != sha256_file(dst):
            ok = False
            print(f"[FAIL] plugin copy out of sync: {rel}")
    for rel in sorted(dst_files):
        if rel not in src_files:
            ok = False
            print(f"[FAIL] plugin copy has extra file: {rel}")
    if ok and not quiet:
        print(f"[OK] plugin copy matches source skill tree ({len(src_files)} files)")
    return ok


def find_references(ars_rel: str) -> list[str]:
    refs: list[str] = []
    for rel in ADAPTATION_REFERENCE_FILES:
        path = REPO_ROOT / rel
        if path.is_file() and not is_ignored(path):
            targets = [path]
        elif path.is_dir():
            targets = sorted(item for item in path.rglob("*") if item.is_file() and not is_ignored(item))
        else:
            continue
        for target in targets:
            try:
                text = target.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if ars_rel in text:
                refs.append(target.relative_to(REPO_ROOT).as_posix())
    return refs


def check_upstream_drift(quiet: bool) -> bool:
    if not UPSTREAM_BASELINE.exists():
        print(f"upstream baseline missing: {UPSTREAM_BASELINE.name} (run --update)")
        return False
    baseline = json.loads(UPSTREAM_BASELINE.read_text(encoding="utf-8"))
    baseline_files = baseline.get("files", {})
    current = snapshot_upstream()
    changed = {
        rel
        for rel in set(baseline_files) | set(current)
        if baseline_files.get(rel) != current.get(rel)
    }
    commit_now, date_now = current_upstream_commit()
    commit_before = baseline.get("upstream_commit", "")
    if not changed and commit_now == commit_before:
        if not quiet:
            print(f"[OK] upstream content unchanged since baseline @ {commit_before[:12]}")
        return True
    print(f"[DRIFT] upstream content changed since baseline @ {commit_before[:12]} "
          f"-> now @ {commit_now[:12]} ({date_now}); re-adaptation required:")
    for rel in sorted(changed):
        key = rel[len("skills/academic-research-suite/ars/"):]
        refs = find_references(key)
        if refs:
            print(f"  - {key}")
            print(f"      referenced by adapted files: {', '.join(refs)}")
        else:
            print(f"  - {key}  (no adapted file references it by path)")
    print("  after re-adapting, run --update to record the new baseline")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true",
                        help="refresh manifests after intentional adaptation edits")
    parser.add_argument("--quiet", action="store_true",
                        help="print only failures")
    parser.add_argument("--check", action="store_true",
                        help="explicit check mode (default; kept for documented workflows)")
    args = parser.parse_args()

    if args.update:
        commit, date = current_upstream_commit()
        guard = build_guard_manifest()
        GUARD_MANIFEST.write_text(
            json.dumps(guard, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        baseline = {
            "upstream_commit": commit,
            "generated_date": date,
            "files": snapshot_upstream(),
        }
        UPSTREAM_BASELINE.write_text(
            json.dumps(baseline, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] wrote {len(guard)} protected-file hashes and upstream baseline @ {commit[:12]} "
              f"({len(baseline['files'])} ars files)")
        return 0

    ok = True
    ok = check_guard_manifest(args.quiet) and ok
    ok = check_dual_copy(args.quiet) and ok
    ok = check_upstream_drift(args.quiet) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
