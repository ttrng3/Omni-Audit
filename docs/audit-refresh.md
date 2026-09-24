# Omni-Audit — refresh runbook

Canonical. The routine prompt points here; where they disagree, this file wins.

## The chain

    Schedule → Routine → Google Drive API census → GitHub data files → Pages live
                                                          └→ Drive record written after

The GitHub page is never downstream of an artifact or a Drive handoff. The
routine measures, scores, and writes JSON into this repo. Pages serves it.

## Who produces, who publishes

**The producer is Ty's scheduled task "Monthly Ecosystem Audit (cloud, v3.x
resolver)"**, monthly on the 1st. It censuses the workspace, scores the four
pillars, and writes its output to Google Drive
`93 Knowledge Base/Claude outputs/Audit/` (folderId
`1XJfVOVQyzZGFKC3au35TtMDDbcoEZe4-`) as `index.html` plus a dated
`<YYMMDD>_SYS_Audit_Ecosystem-Delta*.md`. **Nothing in this repo should ever
recompute a score.**

The routine attached to this repo is a **publisher only**. It carries the
producer's handoff into `data/`. It never censuses, never scores, never invents
a finding.

### Correction, 2026-09-22

An earlier version of this file claimed there was **no producer at all** and
that the audit "was not on any schedule". That was wrong. The producer exists;
it lives on the Scheduled-tasks surface, and it was missed because
`RemoteTrigger list` returns only 20 rows with `has_more: true` and ignores its
cursor. Do not trust a single page of that listing as a complete inventory.

A routine was briefly created here that ran its own census. It has been
converted to a publisher. If you ever find two things scoring this dashboard,
the publisher is the one that must yield.

## What was actually wrong before 2026-09-22

The old "Monthly Audit" routine was a *mirror* — its own prompt opens "You are
the Audit GitHub mirror … You do NOT run the audit" — and it **faked
freshness**. It committed weekly as `publish audit scoreboard <date> (cloud
mirror)`, but the 09-14 and 09-21 commits changed whitespace and one
`</sub>` → `</div>` typo and nothing else. The score stayed 61 because it was
literally the same run, and all three `archive/status_*.html` files were copies
of run 12-09.

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

## One surface, on purpose

    schedule → cloud routine → source → GitHub → Pages

**GitHub Pages is the only published surface.** Ty ruled on 2026-09-23 that he
wants control over what exists of his work, so there is no claude.ai artifact
copy of this dashboard: the Pages URL above is the address, full stop.

A mirror artifact existed for a few hours that day and was deleted. Do not
recreate one, and do not add an artifact URL to this repo. `tools/build-fragment.py`
is kept only because it is the one thing that can derive a standalone fragment
of this page if it is ever needed; nothing in the refresh calls it.

## Design layer

`index.html` is hand-written, not generated; its CSS lives inline there. Since
2026-09-24 it follows the `apple-design` skill (which replaced
ty-artifact-standard): HIG light tokens in the base sheet, then a
`<style id="apple-layer">` that adds card/float shadows, press feedback and the
contrast/motion queries. **Light only — Ty ruled 2026-09-24** (dark mode ran for one morning and was withdrawn): the page stays light whatever the viewer's system setting, and there is no dark theme. Do not add one back. Do not revert to the old warm palette either. Run HTML in `data/runs/*.json` must style itself with the page's
tokens (`var(--accent)`, `--warning`, `--critical`, `--ink`, `--muted`,
`--rule`, …), never raw hex, so the page stays on one palette.
