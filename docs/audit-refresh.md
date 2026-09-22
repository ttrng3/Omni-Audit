# Omni-Audit — refresh runbook

Canonical. The routine prompt points here; where they disagree, this file wins.

## The chain

    Schedule → Routine → Google Drive API census → GitHub data files → Pages live
                                                          └→ Drive record written after

The GitHub page is never downstream of an artifact or a Drive handoff. The
routine measures, scores, and writes JSON into this repo. Pages serves it.

## What was wrong before 2026-09-22

Two separate faults, and together they made a dead dashboard look alive.

1. **No producer.** The only routine, confusingly named "Monthly Audit", was a
   *mirror* — its own prompt opens "You are the Audit GitHub mirror … You do
   NOT run the audit". It copied a Drive handoff that nothing regenerated. The
   audit that produced run 12-09 was not on any schedule.
2. **The mirror faked freshness.** It committed weekly as
   `publish audit scoreboard <date> (cloud mirror)`. The 09-14 and 09-21
   commits changed whitespace and one `</sub>` → `</div>` typo and nothing
   else. Score stayed 61 because it was literally the same run. All three
   `archive/status_*.html` files were copies of run 12-09.

The old watchdog watched `index.html`'s commit age, so it saw fresh commits and
reported healthy. Ten days of staleness were invisible.

## What the routine may write

    data/.last-check              every run, including quiet ones
    data/index.json               manifest: current, runs[] with score + pillars
    data/runs/<YYYY-MM-DD>.json   one file per audit run

Never `index.html` — it is a renderer holding no data. **Never rewrite a prior
run's file.** Each run is independent and immutable once written; the trend
chart is built from `runs[]` in the manifest, which is why score and pillars
live there.

## Scoring

Four pillars, 25 each, total 100. Basis v3 = full tree through the Drive API.
Every figure must trace to a census pull from this run. If nothing improved,
say so — do not inflate. `migrationIntegrityIndex` is tracked separately and is
not part of the 100.

## Sanitisation

This scoreboard is **public**. It carries score, per-pillar RAG and deltas,
trend, plain counts, guardrail PASS/FAIL, and the credential-scan count with
PASS/FAIL. It never carries a path, a filename, a finding detail, or a
credential. The full unsanitised record goes to Drive, not here.

Before writing, scan the run html for `github_pat_`, `ghp_`, `gho_`, `sk-`,
`AKIA`, `AIza`, `xoxb-`, `xoxp-`, `-----BEGIN`, and any inline `:password@` in
a URL. A hit aborts the write.

## Verifying a run — never fetch the live site

Confirm `main` moved using the commit sha the write returned, and read the file
back. Do **not** `curl` or `WebFetch` https://ttrng3.github.io/ from a routine:
cloud egress rejects it with `CONNECT 403`, and WebFetch then raises a
permission prompt nobody is there to answer, so the run parks at
`requires_action` with its work already committed. Pages propagation is not
observable from the sandbox — say so rather than claiming a success you did
not see.

## Credentials

The routine authenticates through the GitHub MCP tools its cloud session is
given. There is no PAT in this tree and the old Drive fallback
`93 Knowledge Base/_tools/gh_audit_pat.txt` is retired — do not read it.

## Case

The repo is `ttrng3/Omni-Audit` and the site is
https://ttrng3.github.io/Omni-Audit/ — capital O and A. The lowercase Pages URL
404s.
