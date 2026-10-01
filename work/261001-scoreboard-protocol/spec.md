# Spec

Status: approved by Ty 01/10 ("approve 8", in chat).

- `verification/scoreboard.md`: promise, clean state, 4 steps (script, live page in Chrome, console, preview), invariants, adversary, sanctioned substitutes, evidence, not covered, traps.
- `tools/verify_live.py` (stdlib only, not served): 17 verdicts as JSON, exit 0 only when all pass: well-formed run dates, newest first, unique; `current` is the newest and, from 06:00 UTC on the 2nd, this month's run; a file per run carrying its id; score = sum of pillars and file = manifest (the script computes no score); every run file, parsed, equals its first commit except that the 2026-09-12 html may equal exactly #7's redacted text (pinned by sha256); no credential, path or file name in any string of any run file or the manifest; live equals `main`; private files exist and 404; heartbeat ≤ 35 days and data ≤ 45 days; every tracked text file read; no personal traces, Drive ids or preview tags; forbidden words absent from served files.
- No change to the page, data, `.pages-allow` or runbook (those are in #7).
- Promise: once #7 is merged, step 1 prints `"pass": true` against the live site and step 2 prints five trues; each drill breakage fails its own verdict and an untouched copy passes.
