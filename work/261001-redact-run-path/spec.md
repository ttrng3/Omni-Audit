# Spec

Status: approved by Ty 01/10: the footer by "Redact it", the folder-name and exposure redactions by "approve 7", the credential and hygiene detail by "Cut to count".

- `data/runs/2026-09-12.json`: in `html` only, the footer's "Private record: <folder> · scoreboard mirror: <file>" becomes "Private record: on Drive, not here."; the empty-folders tile's two folder names become "governance folders"; the watchlist row drops what one folder exposes (review #7: the same sanitisation rule); the credential lines (watchlist, exposure tile, action plan, decision box) and the hygiene list are cut to counts with "detail in the private record" (review #7 round 3; Ty's answer "Cut to count", 01/10). Every other key (score, pillars, guardrails, credential scan, drift, basis, ids) stays byte-identical in value.
- `docs/audit-refresh.md` (Sanitisation): the pre-write scan also greps for a folder path or a file name (clean = no output, exit 1) and aborts on a hit like a credential; folder names and finding details are read by eye; the 01/10 redaction is recorded as the only edit ever made to a past run's file.
- `CLAUDE.md`, the runbook's "What the routine may write" and `REVIEW.md`: each never-rewrite rule names that one exception. The runbook's scan is a concrete grep for paths and file names; a folder's bare name is read by eye. Later runs (09-25, 10-01) already carry no path, so the producer no longer writes one.
- Git history and this PR's diff keep the old footer, folder names, exposure note and credential lines (Ty's answer "Leave history", 01/10).
- Promise: parsed, the 2026-09-12 file differs from `main` only in `html`; no path or file name in any run's `html`; the page still renders all three runs.
