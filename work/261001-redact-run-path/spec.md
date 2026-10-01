# Spec

Status: approved by Ty 01/10: the footer by "Redact it", the folder-name and exposure redactions added in review #7 by "approve 7".

- `data/runs/2026-09-12.json`: in `html` only, the footer's "Private record: <folder> · scoreboard mirror: <file>" becomes "Private record: on Drive, not here."; the empty-folders tile's two folder names become "governance folders"; the watchlist row drops what one folder exposes (review #7: the same sanitisation rule). Every other key (score, pillars, guardrails, credential scan, drift, basis, ids) stays byte-identical in value.
- `docs/audit-refresh.md` (Sanitisation): the pre-write scan also looks for a folder path, a folder's name or a file name and aborts on a hit like a credential; the 01/10 redaction is recorded as the only edit ever made to a past run's file.
- `CLAUDE.md`, the runbook's "What the routine may write" and `REVIEW.md`: each never-rewrite rule names that one exception. The runbook's scan is a concrete grep for paths and file names; a folder's bare name is read by eye. Later runs (09-25, 10-01) already carry no path, so the producer no longer writes one.
- Git history keeps the old footer (Ty's 01/10 ruling for history).
- Promise: parsed, the 2026-09-12 file differs from `main` only in `html`; no path or file name in any run's `html`; the page still renders all three runs.
