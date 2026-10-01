# Spec

Status: approved by Ty 01/10 (same answer as the intent).

- `data/runs/2026-09-12.json`: in `html` only, the footer's "Private record: <folder> · scoreboard mirror: <file>" becomes "Private record: on Drive, not here."; the empty-folders tile's two folder names become "governance folders"; the watchlist row drops what one folder exposes (review #7: the same sanitisation rule). Every other key (score, pillars, guardrails, credential scan, drift, basis, ids) stays byte-identical in value.
- `docs/audit-refresh.md` (Sanitisation): the pre-write scan also looks for a folder path, a folder's name or a file name and aborts on a hit like a credential; the 01/10 redaction is recorded as the only edit ever made to a past run's file.
- `CLAUDE.md`: the never-rewrite rule names that one exception.
- Git history keeps the old footer (Ty's 01/10 ruling for history).
- Promise: parsed, the 2026-09-12 file differs from `main` only in `html`; no path or file name in any run's `html`; the page still renders all three runs.
