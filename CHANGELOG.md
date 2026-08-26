# Changelog

All notable changes to the Codex package are documented here.

## Unreleased

## [1.0.1] - 2026-08-27

### What's Changed
- Re-attributed the plugin author to `zoujialin1997` in the plugin manifest
  (`author` and `developerName`) so the published plugin is credited to this
  distribution's owner.
- Fixed install and support links to point at this distribution's repository
  (`zoujialin1997/academic-research-skills-codex-zh`) instead of the upstream
  repo: `codex plugin marketplace add`, Desktop marketplace source, direct
  skill-installer `--repo` in all four READMEs and `GETTING_STARTED_ZH-CN.md`,
  plus the `SECURITY.md` advisories / issues links and the plugin manifest
  `homepage` / `repository` / website / privacy / terms URLs.
- Updated the README set: added the `/ars-guide` alias row to all four READMEs,
  added a "中文版新增功能" section to `README_ZH-CN.md`, and added beginner-tutorial
  pointers to the EN / ZH-TW / JA READMEs.
- Bumped the Codex package version to `1.0.1` (PATCH) for the metadata /
  attribution corrections.

## [1.0.0] - 2026-08-27

### What's Changed
- **First stable release (1.0.0).** The Chinese adaptation layer has reached a
  stable, documented surface:
  - 0.2.0: fixed-option choice-card protocol (clickable selection in Plan mode).
  - 0.3.0: plain-language terms protocol (specialist terms explained in plain
    Chinese on first occurrence).
  - 0.4.0: Chinese beginner tutorial `GETTING_STARTED_ZH-CN.md`, a README entry
    link, a "新手引导" router section, and the `/ars-guide` interactive
    onboarding command.
  - 0.4.1: localized the tutorial and `/ars-guide` to Chinese-first example
    prompts with plain-language term explanations.
- Corrected stale version references across the README set, the compatibility
  matrix, `AGENTS.md`, and `LOCALIZATION_PLAN.md` to `1.0.0` (display /
  version-text consistency only).
- The four canonical version fields (`VERSION`, `SKILL.md` metadata,
  `manifest.json` adapter_version, `plugin.json`) are all `1.0.0`.

## [0.4.1] - 2026-08-27

### What's Changed
- Made the beginner tutorial and the `/ars-guide` interactive guide fully
  Chinese-first: all copy-paste example prompts are now natural Chinese requests,
  and specialist terms (Socratic scoping, IMRaD, literature review, systematic
  review, direct mode) carry plain-language Chinese explanations. This is a pure
  localization polish of the `0.4.0` beginner-guide feature; routing behavior is
  unchanged.
- Bumped the Codex package version to `0.4.1` (PATCH) for the localization fix.

## [0.4.0] - 2026-08-27

### What's Changed
- Added a Chinese beginner tutorial `GETTING_STARTED_ZH-CN.md` covering everything
  from installation to first use, the five typical scenarios with copy-paste
  example prompts, a full worked example, and the new interactive patterns; added
  a "新手从这里开始" entry link at the top of `README_ZH-CN.md` and updated its
  version badge to `v0.4.0`.
- Added a "新手引导" section to the `SKILL.md` router: when users say they are new,
  do not know how to use the plugin, or ask for a tutorial, the router recommends
  the tutorial and the `/ars-guide` interactive walkthrough; concrete tasks still
  route normally.
- Added the `/ars-guide` interactive onboarding command (`codex/commands/ars-guide.md`):
  asks what the user wants to do first via fixed-option selection, then offers a
  copy-paste example prompt for the chosen scenario and guides a first try, all
  following the choice-card and plain-language terms protocols.
- Bumped the Codex package version to `0.4.0` (MINOR) for the adapter behavior
  change.

## [0.3.0] - 2026-08-26

### What's Changed
- Added the plain-language terms protocol to the `SKILL.md` router:
  user-facing output now explains specialist terms in plain language on
  first occurrence (kept in parentheses after the original term), following
  the session language; the adaptation layer covers all `ars/` workflows
  without modifying vendored files.
- Bumped the Codex package version to `0.3.0` (MINOR) for the adapter behavior
  change.

## [0.2.0] - 2026-08-26

### What's Changed
- Added the fixed-option choice-card protocol to the `SKILL.md` router:
  single-select questions with 2-3 fixed options render a clickable selection
  card in Plan mode (via `request_user_input`) and fall back to a numbered
  option list elsewhere; the adaptation layer covers questions from `ars/`
  workflows without modifying vendored files.
- Bumped the Codex package version to `0.2.0` (MINOR) for the adapter behavior
  change.

## [0.1.27] - 2026-08-24

### What's Changed
- Synced the vendored ARS suite to the signed `v3.21.1` release at
  `127ff85e4bbfcdd10b95040537b6c6bd7ad17aeb`.
- Added the default-off deterministic research-workflow profile substrate and
  opt-in `ARS_INQUIRY_LEDGER=1` branch-ledger alpha, preserving explicit
  selection, visible field-general fallback, append-only correction, bounded
  summaries, and non-destructive stale-state semantics.
- Vendored sealed preregistration contracts and hermetic tests for future model
  promotion bakeoffs, plus the retained GPT-5.6 Sol Codex-transport bakeoff
  evidence. The history-dependent tree verifier remains an upstream
  release-discipline tool because the vendored subtree has no upstream Git
  history.
- Adopted the Codex CLI 0.147.0 citation-transport repairs: authentication
  attestation may arrive on stdout or stderr, the provider schema omits
  unsupported `uniqueItems` while local duplicate rejection stays fail-closed,
  and the bounded search host remains available without widening the accepted
  event grammar.
- Added the source-backed review-criteria proving set, exact-profile source
  receipts, shared Markdown grammar, workflow-profile and inquiry-ledger
  runtimes, contracts, and hermetic tests.
- Preserved the single-root Codex router, `WORKFLOW.md` entrypoint and content
  lock overlays, inactive Claude-only validators, MiniMax compatibility layer,
  materialized Desktop plugin mirror, and separately pinned experiment-agent
  v1.1.0 tree.

## [0.1.26] - 2026-08-18

### What's Changed
- Synced the vendored ARS suite through the signed `v3.21.0` release at
  `2b639c12ee4e7c694a32336cc59dc2616e0d89fe`, rolling the unreleased
  v3.20.1 alignment into the same Codex package version.
- Added the default Socratic non-generation exit: non-convergence alone no
  longer authorizes system-authored research-question candidates.
- Adopted categorical, criterion-bound reviewer judgements, `NOT_CALIBRATED`
  live packages, and six-axis panel provenance while retiring numeric reviewer
  scores, weights, aggregates, and score trajectories.
- Added exact-span/raw-byte claim-registry coverage, claim-strength disposition
  sidecars, required scope for new human-read attestations, and a closed
  deterministic attestation resolver.
- Vendored the bounded claim-standing stance and blind ideation-assignment
  evaluation infrastructure with its consent, provenance, no-call, and
  unmeasured boundaries.
- Added the v3.21 claim-standing query-plan, affirmative-consent, freshness,
  transmission-ledger, and pipeline-wiring contracts. Eligibility remains an
  offer signal and never dispatches an external call.
- Vendored the canonical data-flow map, control-availability matrix,
  stage-capability matrix, risk register, governance statement, and their
  deterministic transparency checks.
- Documented the Codex bibliographic routing boundary: ordinary discovery and
  inline ingest use browsing; `ars-full` alone does not launch the four Python
  resolver clients; programmatic citation verification and claim-standing
  discovery retain separate explicit triggers.
- Preserved the single-root Codex router, `WORKFLOW.md` path adaptations,
  inactive Claude-only calibration and distribution-surface gates,
  materialized Desktop plugin mirror, and the separately pinned
  experiment-agent v1.1.0 tree.

## [0.1.25] - 2026-08-14

### What's Changed
- Synced the vendored ARS suite to the `v3.20.0` release at
  `3af9f03d5aadb0bca51af1440f20b5cbf97d6dba`.
- Added evidence-bound review and revision contracts, including durable
  evidence rows, author-confirmed review criteria, non-ranking revision
  roadmaps, author adjudication, and revision-evidence bundles.
- Added the contained, consent-gated Codex citation transport for narrow
  citation-integrity checks, plus stronger human-subjects authority boundaries.
- Vendored the optional sandboxed PDF content classifier as an advisory tool;
  it is not a required dependency and does not change structural PDF preflight.
- Adapted the v3.20 indirect-injection no-call envelope to verify its upstream
  suite commit through the package source lock when the nested vendor tree has
  no `.git` directory.
- Preserved the single-root Codex router, `WORKFLOW.md` entrypoint mapping,
  inactive Claude-only hooks, and separately vendored experiment-agent v1.1.0.

## [0.1.24] - 2026-08-06

### What's Changed
- Updated the separately vendored experiment-agent tree from
  `9b063fa895eaf1f63ac99ac03f924f8d31aa8d26` (pre-`v1.0.1`) to
  `e291e7dc7ca268b2de7e1a9cf23bc2eef5dc0651` (`v1.1.0`, upstream main head).
- Added the v1.1.0 session-resume capability for `study_manager_agent`: the
  study-state protocol (`references/study_state_protocol.md`), the
  `study_state.md` template and worked example, the session-resume design
  spec and implementation plan under `docs/`, and the expanded
  `study_manager_agent` resume flow.
- Preserved the experiment-agent `WORKFLOW.md` entrypoint rename with its
  Codex `data_access_level`/`task_type` frontmatter overlay; upstream
  `.claude/` and `.github/` dev files remain excluded. The ARS vendored tree
  is unchanged from 0.1.23 (still pinned at `5769d7b`).

### Notes
- This closes the experiment-agent half of the 2026-08-06 alignment; both
  vendored source repositories now track their upstream main heads.

## [0.1.23] - 2026-08-06

### What's Changed
- Updated the vendored ARS runtime from
  `828ef3b613b0e8b91830da3328a1e33d4eb5ab4c` (`v3.19.0`) to
  `5769d7b51adfba45593ad95721436fd114aaa735` (post-`v3.19.0` main,
  2026-08-06). No worktree or branch content is included — the pin is the
  upstream `main` head.
- Added the reviewer hardening track: the #574 role-scoped scoring contract
  with abstention and per-mode decision contracts, typed evidence anchors,
  coverage receipts and severity transport, the #576 three-gate Stage 3'
  re-review pre-commitment contract (schemas + synthesis checker +
  patch_digest), the #608 dispatch harness, the #609 empty-dissent rule, the
  #610 AR arithmetic-receipt grammar with the step-5 deterministic receipt
  calculator, and #611 protocol text-consistency locks.
- Vendored the new held-out eval sets and adjudicated cohorts (seeded
  defects, persuasion-invariance paired controls, #610 baseline/post
  cohorts), medical venue disclosure policies with fail-closed rendering and
  the Frontiers submission-action fix, the Chinese-literature resolver client
  and API protocol, CARE / STARD 2015 / TRIPOD+AI condensed guidance with a
  study-design routing sequence, and bare `/ars-*` alias frontmatter names.
- Vendored the community-maintained Pi wrapper (`pi/` + root `package.json`)
  and `.gitleaksignore` for traceability; the Pi wrapper targets upstream
  SKILL.md paths and is not a Codex entrypoint.
- Extended the `WORKFLOW.md` path adaptation to the new reviewer-contract
  lint family (decision contract, reviewer finding contract, reviewer role
  label, venue disclosure harness, and their tests); re-pinned the pipeline
  content locks after the overlay. Declared `check_calibration_tiers.py`
  inactive (it requires the non-vendored `.claude/CLAUDE.md`) and removed its
  entry from the vendored local pytest manifest.
- Preserved the single-root-skill layout, `WORKFLOW.md` entrypoint mapping,
  Codex provider/content/consent boundaries, nested-distribution validator
  adaptations, macOS/Python compatibility patches, and materialized Desktop
  plugin bundle.

### Notes
- This sync pins upstream `main` at `5769d7b` (44 commits past `v3.19.0`);
  the upstream suite version remains 3.19.0 until the next ARS release tag.

## [0.1.22] - 2026-07-22

### What's Changed
- Updated the vendored ARS runtime from
  `bbc0659272a511b422f6856cd6f44b6ccb2ac213` (`v3.18.0`) to
  `828ef3b613b0e8b91830da3328a1e33d4eb5ab4c` (`v3.19.0`).
- Added the local-PDF read-integrity preflight and sidecar contract, optional
  human-read `read_scope` attestations with partial-coverage handling, and
  revision-round claim-drift guards built from the claim-strength ladder and
  deterministic token-conservation checker.
- Vendored the new human-read ledger schema, revision evidence and held-out
  measurement set, plus the PDF/read-scope design records and associated test
  coverage.
- Preserved the single-root-skill layout, `WORKFLOW.md` entrypoint mapping,
  Codex provider/content/consent boundaries, nested-distribution validator
  adaptations, macOS/Python compatibility patches, and materialized Desktop
  plugin bundle. Re-pinned the pipeline content lock after the v3.19 overlay.

### Notes
- This sync pins the exact ARS release tag `v3.19.0`.

## [0.1.21] - 2026-07-18

### Changed
- Renamed the Codex plugin identity, marketplace, and plugin directory to
  `ars-codex` so the Codex-native sibling is clearly distinguished from the
  upstream Claude Code ARS distribution.
- Updated the plugin display name to `ARS-Codex` and added CLI-first
  marketplace installation instructions for external users.
- Kept the bundled skill identifier `$academic-research-suite` stable to avoid
  breaking existing Codex workflow prompts and direct skill installations.

## [0.1.20] - 2026-07-18

### What's Changed
- Updated the vendored ARS runtime from
  `039d94f670c47d996ca919d37b8753b0a8d4a140` (`v3.17.0`) to
  `bbc0659272a511b422f6856cd6f44b6ccb2ac213` (`v3.18.0`).
- Added the fixed-seat cross-model Reviewer 2 track, independent re-review
  judge pass and Judge Record, cache-age advisories with opt-in live
  re-validation, high-impact-first claim sampling, scope-conformance and
  search-bounded novelty advisories, and the held-out pipeline robustness set.
- Preserved Codex provider/content/consent boundaries: external reviewer and
  judge tracks are never simulated, single-family or fallback execution is
  disclosed, and live cache re-validation stays tied to explicit verification
  work.
- Vendored the upstream SessionStart update checker for traceability and tests
  without installing it as a Codex hook. Preserved the single-root-skill
  layout, `WORKFLOW.md` entrypoint mapping, nested-distribution validator
  patches, macOS/Python compatibility patches, and the materialized Desktop
  plugin bundle.

### Notes
- This sync pins the exact ARS release tag `v3.18.0`.

## [0.1.19] - 2026-07-17

### What's Changed
- Updated the vendored ARS runtime from
  `73c898c842afae3f163ac571dfa098c72d7c82af` (`v3.16.0`) to
  `039d94f670c47d996ca919d37b8753b0a8d4a140` (`v3.17.0`).
- Added the canonical cross-model handoff envelope and dispatcher contract,
  least-privilege tools allowlists, executable panel-synthesis validation,
  pinned Stage 5/6 boundary semantics, the machine-readable degradation
  registry, and hermetic citation-gate transport fixtures.
- Mapped dispatched cross-model transport to the Codex dispatching context,
  preserved explicit provider/content/consent gates, and exposed the new
  upstream validators in the optional full-runtime manifest.
- Preserved the single-root-skill layout, `WORKFLOW.md` entrypoint renaming,
  nested-distribution validator patches, macOS/Python compatibility patches,
  and the materialized Codex Desktop plugin bundle. The pipeline-orchestrator
  content-lock hash changes only for the Codex `WORKFLOW.md` path overlay.

### Notes
- This sync pins the exact ARS release tag `v3.17.0`.

## [0.1.18] - 2026-07-13

### What's Changed
- Updated the vendored ARS runtime from
  `f86d68a80a6fd05bf51688ff39297ea603eda912` (`v3.15.0`) to
  `73c898c842afae3f163ac571dfa098c72d7c82af` (`v3.16.0`).
- Added upstream model tiering, risk-stratified cross-model verification and
  blind disagreement checkpoints, GPT-5.6 Sol provisional verifier support,
  API retrieval hardening, CARS introduction/title guidance, WP advisory
  evaluation updates, Korean routing triggers, and `THIRD_PARTY.md`.
- Propagated Korean intent boundaries into the Codex router and planner, kept
  model tiering advisory unless per-dispatch Codex model selection exists, and
  retained explicit consent for all external cross-model uploads.
- Preserved the single-root-skill layout, `WORKFLOW.md` entrypoint renaming,
  nested-distribution validator patches, macOS compatibility patches, and the
  materialized Codex Desktop plugin bundle.

### Notes
- This sync pins the exact ARS release tag `v3.16.0`.

## [0.1.17] - 2026-07-04

### What's Changed
- Updated the vendored ARS runtime from
  `8157a15b3bfad94af5c3ac4d7a79d5a9362622f4` (`v3.14.0`) to
  `f86d68a80a6fd05bf51688ff39297ea603eda912` (`v3.15.0`).
- Added upstream ARS v3.15 release content, including release-gate hardening,
  command-invariants and changelog coverage checks, prompt-debt retirement
  round 2, defrift locks, SETUP cross-model parity checks, and the
  `tools/release-discipline` snapshot.
- Preserved Codex packaging behavior: one root router skill, vendored workflow
  entry files named `WORKFLOW.md`, excluded Claude/plugin loader files,
  Codex-specific spec-consistency adaptations, Python 3.9 compatibility patches,
  and the materialized Codex Desktop plugin bundle.

### Notes
- This sync pins the exact ARS release tag `v3.15.0`.

## [0.1.16] - 2026-07-02

### What's Changed
- Updated the vendored ARS runtime from
  `17c518b286e48bbcd19fa7d05ec4f7d2aeb01641` (`v3.13.0-5-g17c518b`,
  ARS main after the platform-port reminder update) to
  `8157a15b3bfad94af5c3ac4d7a79d5a9362622f4` (`v3.14.0`).
- Added upstream ARS v3.14 release content, including eval-harness PR comment
  rendering, prompt-debt retirement updates, the July harness-retirement audit,
  release-aligned README/CITATION/MODE_REGISTRY surfaces, and refreshed setup
  and architecture docs.
- Preserved Codex packaging behavior: one root router skill, vendored workflow
  entry files named `WORKFLOW.md`, excluded Claude/plugin loader files,
  Codex-specific spec-consistency adaptations, and the materialized Codex
  Desktop plugin bundle.

### Notes
- This sync pins the exact ARS release tag `v3.14.0`, not post-release
  `ars/main`.

## [0.1.15] - 2026-06-29

### What's Changed
- Updated the vendored ARS runtime from
  `c22c17eed8a5753aa60681be9734919f2e2f5b42` (`v3.13.0-2-gc22c17e`,
  ARS main after GitHub Copilot documentation updates) to
  `17c518b286e48bbcd19fa7d05ec4f7d2aeb01641` (`v3.13.0-5-g17c518b`,
  current ARS main).
- Added the native-reviewed upstream Korean README and its spec-consistency
  lint coverage while preserving Codex-specific nested-distribution patches.
- Added the upstream platform-port reminder workflow and pull request template
  reminder text in the vendored traceability copy.

### Notes
- This sync pins ARS `main`, not an exact upstream tag. The nearest upstream tag
  remains `v3.13.0`.

## [0.1.14] - 2026-06-21

### Fixed
- Replaced the Codex Desktop plugin's `skills` symlink with a materialized
  bundled `skills/academic-research-suite` directory so Windows plugin caches
  register the bundled skill reliably.
- Added a package quality gate that fails if the Desktop plugin bundle reverts
  to symlink-based skill packaging.

## [0.1.13] - 2026-06-20

### What's Changed
- Updated the vendored ARS runtime from
  `529c6d25a3778843fb94edf9f03eda4cd7e0f416` (`v3.12.0-19-g529c6d2`,
  ARS main after the submission-package verifier slices) to
  `c22c17eed8a5753aa60681be9734919f2e2f5b42` (`v3.13.0-2-gc22c17e`,
  ARS main after the GitHub Copilot documentation updates).
- Added upstream ARS v3.12.1 and v3.13 mainline content, including
  reviewer-response triage modes, diff/patch revision mode adoption,
  format-profile support, provider-agnostic cross-model verification,
  Windows hook portability, Socratic adjacent-framing probe support,
  CITATION metadata, and repository instruction docs.
- Added Codex alias coverage for `ars-3w` and `ars-rebuttal-audit` in both
  the root router and the optional full-runtime planner.
- Preserved Codex packaging behavior: one root router skill, vendored workflow
  entry files named `WORKFLOW.md`, excluded Claude/plugin loader files,
  preserved nested upstream `.github` and root `agents` mirrors as inactive
  traceability/self-test fixtures, Codex setup/architecture overlays at the
  package root, nested-path lint adaptations, macOS Bash 3.2 audit wrapper
  compatibility, and explicit cross-model consent boundaries.

### Notes
- This sync pins ARS `main`, not an exact upstream tag. The nearest upstream tag
  is `v3.13.0`.

## [0.1.12] - 2026-06-11

### What's Changed
- Updated the vendored ARS runtime from
  `2560a072386d4b1a035e5a40ed24ce1edbc0a356` (`v3.11.1`) to
  `529c6d25a3778843fb94edf9f03eda4cd7e0f416` (`v3.12.0-19-g529c6d2`,
  ARS main after the submission-package verifier slices).
- Added upstream ARS v3.12 and post-tag mainline content, including
  sub-claim decomposition, cross-paper contradiction inventory, figure/table
  fidelity, experiment provenance intake, field-norm severity calibration,
  surface-form parity checks, repository hygiene config, and the submission
  package verifier.
- Added Codex alias coverage for `ars-cache-invalidate`.
- Preserved Codex packaging behavior: one root router skill, vendored workflow
  entry files named `WORKFLOW.md`, Codex setup/architecture overlays, excluded
  Claude/plugin loader files, nested-path lint adaptations, macOS Bash 3.2
  audit wrapper compatibility, and explicit cross-model consent boundaries.

### Notes
- This sync pins ARS `main`, not an exact upstream tag. The nearest upstream tag
  is `v3.12.0`.

## [0.1.11] - 2026-06-06

### What's Changed
- Updated the vendored ARS runtime from
  `ca5b713d9d802af85d4c74552604b062a618b1c1` (`v3.11.0` plus the first
  post-tag #310 follow-up fixes) to
  `2560a072386d4b1a035e5a40ed24ce1edbc0a356` (`v3.11.1`).
- In plain terms: this brings the Codex package up to the ARS patch release
  that cleaned up the first wave of post-ship problems after v3.11.0. The main
  changes are correctness and hardening fixes for citation verification,
  domain evidence profiles, eval thresholds, policy markers, provenance joins,
  and edge cases around schema-valid security-boundary inputs.
- Preserved the Codex packaging layer: one root router skill, vendored
  workflow entry files named `WORKFLOW.md`, Codex setup/architecture overlays,
  excluded Claude/plugin loader files, package-specific lint adaptations, and
  the explicit cross-model consent boundary.
- Kept local Codex validation runnable on macOS Python 3.9 by avoiding
  Python-3.11-only standard-library assumptions in the vendored test utilities
  and by using the active Python executable in adapter subprocess tests.

### Notes
- No new Codex package feature was added. This is a vendor sync plus metadata
  release so Codex users get the same v3.11.1 runtime fixes as upstream ARS.

## [0.1.10] - 2026-06-04

### Added
- Added an optional Codex full-runtime adapter profile under
  `skills/academic-research-suite/codex/`, including deterministic route
  planning, Codex agent-team templates, a disabled-by-default hook pack, and
  adapter quality gates. Default ARS Codex behavior remains inline role-prompt
  execution.

### Changed
- Vendored upstream ARS from `4c38571798da4b1ed604ec2c1e01a6f66a7de5a7`
  (`v3.10.0` plus release-manifest alignment) to
  `ca5b713d9d802af85d4c74552604b062a618b1c1` (`v3.11.0` plus post-tag #310
  follow-up fixes).
- Added ARS v3.11 runtime content, including the deterministic citation
  verification gate, arXiv resolver, persistent verification cache, citation
  verification summary contract, standalone verification gate API, and
  `ars-cache-invalidate` command recipe.
- Kept Codex-specific overlays: single root router skill, `WORKFLOW.md`
  vendored workflow entry files, Codex setup/architecture docs, nested-path lint
  patches, excluded showcase PDFs, macOS Bash 3.2 audit wrapper compatibility,
  and explicit cross-model consent boundaries.

### Security
- Added Codex security boundaries for untrusted research inputs, cross-model
  consent, local adapter filesystem handling, and fixed-host bibliographic API
  lookups.

## [0.1.9] - 2026-06-01

### Changed
- Vendored upstream ARS from `96b82e82142dc95f117595c207d3e150b078e411` (`v3.9.4.2`) to `4c38571798da4b1ed604ec2c1e01a6f66a7de5a7` (`v3.10.0` plus release-manifest alignment).
- Added ARS v3.10 runtime content, including the triangulation policy layer, eval harness/gold sets, Schema 11 commitment-ledger refactor, domain-evidence/version-family updates, and scoped-write guard scripts.
- Added newly vendored upstream `README.zh-CN.md`, `README.ja-JP.md`, `evals/`, `conftest.py`, and new `ars-*` command recipes.
- Kept Codex-specific overlays: single root router skill, `WORKFLOW.md` vendored workflow entry files, Codex setup/architecture docs, nested-path lint patches, excluded showcase PDFs, and macOS Bash 3.2 audit wrapper compatibility.
- Clarified beginner install instructions by using `python3` in command
  examples and documenting the `python` fallback when it points to Python 3.
- Added community acknowledgements for beginner-install feedback and issue
  discussion support.

## [0.1.8] - 2026-05-19

### Changed
- Vendored upstream ARS from `74413a42571867abece7b8b76f7a24ac472ab2a0` (`v3.9.0`) to `96b82e82142dc95f117595c207d3e150b078e411` (`v3.9.4.2`).
- Added ARS v3.9.1 client hardening, v3.9.2 phase-boundary routing discipline, v3.9.3 shared client utilities, and v3.9.4/v3.9.4.1 temporal verification runtime content.
- Kept Codex-specific overlays: single root router skill, `WORKFLOW.md` vendored workflow entry files, Codex setup/architecture docs, nested-path lint patches, and macOS Bash 3.2 audit wrapper compatibility.

### Notes
- Upstream v3.9.4.2 changes only `.github` CI/release-gate files, which are intentionally excluded from this Codex package. The manifest still pins the exact v3.9.4.2 commit for provenance.

## [0.1.7] - 2026-05-17

### Changed
- Aligned the Codex package with upstream ARS `v3.9.0`.
