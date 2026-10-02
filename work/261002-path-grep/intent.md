# Intent: the run's path scan stops treating slash-separated words as a folder path

**Status:** accepted 2026-10-02
**Source:** chat, 2026-10-02 (follow-up logged 02/10 when the scoreboard protocol shipped)

**Problem.**
- `docs/audit-refresh.md`, "Sanitisation", has the routine scan the run html with one `grep -niE` before each write. A hit aborts the write. The pattern's third alternative is meant to catch a folder path (two `/` with words between them). It also matches ordinary prose.
- Tested 2026-10-02 with the system grep and with Python:
  - "red/amber/green" and "RAG: Red/Amber/Green" match;
  - "pass/fail/skip counts" matches;
  - "Drive folder 93 KB/Claude outputs/Audit" matches, which is correct;
  - "82/100" and "01/10/2026" do not match.
- So a run whose prose says "red/amber/green" would abort its own publish, and the scoreboard would go stale with no leak behind it.
- The three committed runs (`data/runs/`) don't trip it today.
- On this Mac, `grep` is a shell wrapper around ugrep, which matches neither the prose nor the real path. A hand check of this pattern on the Mac proves nothing; the routine runs GNU grep in the cloud.

**Outcome.** These can be checked:
- The scan still catches every path it catches today: the real Drive path and the file-name, `/Users/`, `/home/` and `~/` cases.
- It no longer matches slash-separated words in prose ("red/amber/green", "pass/fail/skip").
- Shown on a fixed list of should-catch and must-pass lines with GNU-compatible grep (the system grep, not the shell wrapper).
- The three committed runs still scan clean.

**Who and what is affected.**
- Repo Omni-Audit: `docs/audit-refresh.md` (the pattern), possibly `CLAUDE.md`'s command line and `verification/scoreboard.md` if they quote it.
- The monthly run's publish step and the 2nd-of-month fallback, which follow the runbook. Next run: 1 Nov.

**Constraints.**
- The scan must not get weaker on real paths: a missed path on this public page is worse than a false abort.
- Entity: OMNI only.
- No preview URL or ids in the repo.
- Past runs are never rewritten.
- Merge before the 1 Nov run, and not while a run is due.

**Open questions.**
1. Which fix? A pattern alone can't tell "red/amber/green" from a real folder path with no spaces, like "Audit/runs/2026/". Two options:
   (a) Remove a short, named list of known prose phrases ("red/amber/green", "pass/fail") from the text before the scan. The path rule stays as strong as today; a new phrase would still abort until it's added to the list.
   (b) Narrow the third alternative. Fewer false aborts, but some real paths would slip through.
   My recommendation is (a).
2. Does the routine's prompt quote the pattern itself? If it does, the prompt has to change with the PR. I'll check this in the spec, the same way as for gdsh.

**Answer (Ty, chat, 2026-10-02).** Option (a): remove a named list of prose phrases before the scan. For the spec: exemptions are exact whole phrases in one list. The promise must show that a real path placed next to an exempt phrase still aborts the publish, and that the guard's other two alternatives are unchanged.
