# REVIEW.md

What the reviewer agent (`agents/reviewer.md` in claude-config) checks on every PR to this repo. The three passes run in order, each in full. The last section holds this repo's own rules.

This file is never served: it is not in `.pages-allow`.

## Severity
- **Critical:** it will break something live or publish something it must not. A secret or token, personal data by value in a public repo, a newly served path that shouldn't be, a broken deploy, data loss, a gate bypass.
- **High:** wrong behaviour that will show up. A bug on a path that runs, a broken reference, a diff that does something other than what the PR says, a house rule broken in a way Ty would have to undo.
- **Medium:** it's wrong but contained. An edge case that isn't hit yet, a doc that disagrees with the code, a missing test for a changed behaviour.
- **Low:** clarity, naming, a stale comment.

When unsure between two levels, pick the higher one and say why.

## Pass 1: Bugs
- [ ] Logic: off-by-one, inverted condition, wrong variable, an unreachable branch, loop bounds.
- [ ] Edge cases: empty input, a missing file, a first run, a name with spaces or accents, a timezone (Hanoi is UTC+7; cron is UTC).
- [ ] References resolve: every path, heading anchor, script flag, workflow job name and file named in the diff exists in `files/` or in the base.
- [ ] Shell: quoting, `set -e` interactions, `$?` after a pipe, BSD vs GNU flags (the Mac runs BSD tools).
- [ ] Syntax: YAML, JSON, Python (3.9 on the Mac: no `match`, no `X | Y` types), HTML.
- [ ] The diff does what the PR description says, and nothing it doesn't say.

## Pass 2: Security
- [ ] Secrets by pattern: `ghp_`, `github_pat_`, `sk-`, `sk-ant-`, `AKIA`, `xox[bp]-`, private-key headers, `eyJ…` JWTs (a Supabase **service_role** JWT is always Critical), passwords in URLs, `?token=`/`?key=` in a link.
- [ ] Personal data **by value** in a public repo: a name with money, a phone number, an email address, an account number, an ID number. Referring to where the value lives is fine; the value itself isn't.
- [ ] Anything newly published: a path added to `.pages-allow`, or any new file in a repo still on legacy Pages.
- [ ] Workflow permissions widened (`permissions:`, `pull_request_target`, `secrets: inherit`), or a new third-party action not pinned to a sha.
- [ ] Test fixtures build fake secrets at run time; a token-shaped string typed into a file is a finding even if it's fake.

## Pass 3: House rules
- [ ] **Never by value:** a sensitive value is referenced, not quoted, in any file of a public repo, including `work/` docs.
- [ ] **Artifact mirror contract:** no Cowork preview URL and no artifact id in anything public or anything Ty is shown. (A registry row that records an id on the private Drive mount is the exception.)
- [ ] **Entity separation:** OMNI and ECOPM data, names and numbers never cross into each other's repo or page.
- [ ] **One change per `work/` folder:** the PR names its `work/<yymmdd>-<slug>/`; `intent.md` says accepted; `spec.md` says approved; the diff matches the spec's promise, with nothing extra.
- [ ] **`gate/` untouched** while it is frozen (until 2026-10-05).
- [ ] **One PR per merge command:** nothing in the diff merges or batches PRs (`gh pr merge` in a loop, the merge API).
- [ ] **Verify before you assert:** every number in a doc or page has a source named beside it or in its section.

## Repo-specific rules
Rules specific to Omni-Audit. **Every standing ruling in the README and in `docs/audit-refresh.md` (the runbook, which outranks the routine prompt) applies as well; a PR that breaks one is High.** The lines below are the ones most often at risk.

- **Nothing in this repo computes a score.** The producer scores; the routine here only publishes its handoff (runbook, "Who produces, who publishes"). Code or a routine instruction that recomputes, adjusts or invents a score, pillar or finding is High.
- **What a refresh writes.** Only `data/.last-check`, `data/index.json` and `data/runs/<YYYY-MM-DD>.json` (runbook, "What the routine may write"). A refresh that touches `index.html` is High: it is a renderer holding no data.
- **Run files are immutable.** A diff that edits or deletes an existing `data/runs/*.json` is High; the trend is built from `runs[]` in the manifest.
- **The scoreboard is public and sanitised.** It carries scores, RAG, deltas, counts and PASS/FAIL only, never a path, a filename, a finding detail or a credential (runbook, "Sanitisation"). Any of those in `data/` is **Critical**. The secret patterns listed there abort a write; a diff that weakens that scan is High.
- **Run HTML uses the page's tokens** (`var(--accent)`, `--warning`, `--critical`, `--ink`, `--muted`, `--rule`), never raw hex (runbook, "Design layer").
- **Light only, ruled 2026-09-24 by Ty.** No dark theme, and no return to the old warm palette (runbook, "Design layer").
- **Case.** The repo and site are `Omni-Audit`, capital O and A; the lowercase Pages URL 404s (runbook, "Case"). A lowercase link is High.
- **Never fetch the live site from a routine.** A routine instruction that curls or web-fetches `https://ttrng3.github.io/` is High: the run parks at `requires_action` (runbook, "Verifying a run").
- **No credentials.** No PAT in the tree; the retired Drive PAT path must not be read (runbook, "Credentials"). A token or a token-in-URL push is Critical.
- **One address, one preview.** `https://ttrng3.github.io/Omni-Audit/` is the only link. A Cowork preview URL or artifact id anywhere in the repo is **Critical** (the repo is public). The preview itself must never be deleted (runbook, "One address, one preview").
- **Don't widen what is published.** A new path in `.pages-allow`, or a new kind of data in `data/`, is High and needs Ty.
