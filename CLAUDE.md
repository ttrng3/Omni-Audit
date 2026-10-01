# CLAUDE.md — Omni-Audit

OMNI's public Ecosystem Audit scoreboard, entity **OMNI**. Live: https://ttrng3.github.io/Omni-Audit/ (capital O and A; the lowercase URL 404s)

**If you are a scheduled routine** (the monthly run's publish part, or the 2nd-of-month fallback): follow the files your prompt names, `docs/audit-refresh.md` and `README.md`. They outrank this file. This file adds no step to a run.

## Commands
- Check `current` is in `runs[]` and every run has its file (a quick check, not full validation): `python3 -c "import json,os;d=json.load(open('data/index.json'));ids=[r['id'] for r in d['runs']];assert d['current'] in ids;assert all(os.path.exists('data/runs/%s.json'%i) for i in ids)"`
- Secret and path scan of `data/`: the runbook's own greps (`docs/audit-refresh.md`, "Sanitisation"); clean = no output and exit 1, a hit = exit 0, abort
- Build the Cowork preview page: `python3 tools/build-fragment.py` (writes `build/artifact.html`). When the routine refreshes the preview is set by its runbook, not here. Never send `index.html` itself to the preview; Pages does serve it.
- Compare two `data/` trees: `python3 tools/reconcile.py <dir-a> <dir-b>` (exit 0 = same)
- Freshness check, as the daily Action runs it: `python3 .github/scripts/freshness.py`

## Layout
- `index.html` is a hand-written renderer holding no data. A refresh never touches it or its stylesheet.
- Data: `data/index.json` (manifest: `current`, `runs[]` with score and pillars), `data/runs/<YYYY-MM-DD>.json` (one file per audit run, immutable once written), `data/.last-check` (heartbeat, not published).
- `.pages-allow` lists what Pages publishes; `.github/workflows/pages.yml` deploys only that. Every tracked file under a watched area needs a `.pages-allow` line (published, or `!` for known but not published); a new kind of file needs Ty's say-so and that line in its own PR first.
- `README.md` points to the runbook; `REVIEW.md` holds the reviewer's rules.

## Rules
- Changes reach `main` through a PR and Ty's ship. The only direct writes are the ones a routine's prompt and runbook allow.
- The runbook and README win over this file and any memory note.
- Nothing in this repo computes a score. The producer scores; this repo only carries its handoff. The publisher never scores.
- Never rewrite or delete a prior run's file under `data/runs/` (one sanctioned exception, 2026-10-01: runbook "Sanitisation").
- The scoreboard is public and sanitised: scores, RAG, deltas, counts and PASS/FAIL only; never a path, a filename, a finding detail or a credential.
- Light only (Ty, 2026-09-24). Run HTML uses the page's tokens (`var(--accent)`, `--warning`, …), never raw hex.
- Never write a Cowork preview URL or artifact id, a person's details or a secret into this public repo.
- Entity separation: this is OMNI. Never bring another company's data, names or numbers into this repo.

## Known mistakes
- The routine list API returns one page, says `has_more`, and ignores its cursor, so the producer was once declared missing from one page (2026-09-22).
- The old mirror routine committed whitespace-only changes weekly, so a commit-age watchdog read a stale score as fresh; `data/.last-check` and `generatedUtc` are what show freshness (2026-09-22).
- A publisher that fires before the day's handoff is written publishes nothing: the 2026-09-22 heartbeat found only the 09-12 run, and the page stayed on it until 2026-09-25 (2026-09-25).
- The Cowork preview was deleted on 2026-09-23 and again on 2026-09-25 by reading "no artifact link" as "no artifact", and rebuilt on 2026-09-26. The preview must exist; only its URL stays out of sight (2026-09-26).
- A ToolSearch miss was read as a missing tool, and a run silently skipped its artifact steps; attached tools never show in ToolSearch (2026-09-25).
- The old Drive PAT file is retired; the routine authenticates through the GitHub MCP tools (2026-09-22).
