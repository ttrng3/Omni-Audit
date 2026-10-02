# Spec: path-grep

**Approved:** 2026-10-02 (Ty, in chat)

**Changed after review, 2026-10-02 (reviewer High + Mediums on #9), recorded so the spec matches the diff:** the scan no longer pipes `perl` into `grep`. `perl` opens the run html itself (a failed open stops it), writes a temp file, and `grep` runs only after it succeeds; "clean" is now no output at all and exit 1, so an unreadable file or a missing `perl` aborts. The list gains `pass/fail/skip` (named in the intent's Outcome). The boundary also refuses a phrase followed by `.` or `-` plus a letter or slash, or preceded by a letter or slash plus `.` or `-`, so the phrase can't lend its slashes to a path or file name ("red/amber/green.md" still aborts). The two lists are described as two copies that must match.

**Intent:** accepted 2026-10-02 · **Status:** approved

## Requirements
1. Before the path scan, remove each exempt phrase from the text. The exempt phrases are exact whole phrases, kept in one list (intent, answer (a)).
2. A phrase is removed only where it stands alone: not preceded or followed by a letter, a digit or a `/`. So "red/amber/green" inside a path ("Audit/red/amber/green/") is not removed, and the path still aborts.
3. A real path next to an exempt phrase still aborts the publish (Ty, 2026-10-02).
4. The scan's other two alternatives are unchanged: the file-name alternative, and the `/Users/`, `/home/`, `~/` alternative (Ty, 2026-10-02). The third alternative, the folder-path rule, is unchanged too. Only the input to it changes.
5. The scoreboard check in `tools/verify_live.py`, which carries its own copy of the pattern (`PATHISH`), applies the same list the same way.

## Design
- **The list.** Exact whole phrases, matched case-insensitively: `red/amber/green` (the page's RAG wording) and `pass/fail/skip` (named in the intent). They're kept in two copies that must match: the runbook's `perl` group and `EXEMPT` in `tools/verify_live.py`. The three published runs contain no two-slash phrase today (checked 2026-10-02).
- **Standing alone.** A phrase is removed only when no letter, digit or `/` touches it, and no `.` or `-` followed by a letter or `/` follows it (or precedes it after a letter or `/`). So a phrase can't lend its slashes to a path or a file name: "red/amber/green.md" and "Audit/red/amber/green/" still abort. `-CSD` and `\w` make a Vietnamese letter count as a letter in perl, as it does in Python.
- **The runbook command.** No pipe. `perl` opens the run html itself and dies if it can't, writes the cleaned text to a temp file, and the unchanged `grep` runs on it only after (`&&`):
  ```
  perl -CSD -e 'open(my $f, "<", shift) or die "scan input: $!\n"; while (<$f>) { s{…}{ }gi; print }' "<run html>" > /tmp/omni-audit-scan.txt && grep -niE '<the pattern, unchanged>' /tmp/omni-audit-scan.txt
  ```
  - **"Clean"** is no output at all (stdout or stderr) and exit 1. An unreadable file (rc 2) or a missing `perl` (rc 127) aborts.
  - **Quoting.** The path is quoted, so a space in it can't break the scan.
  - **Mac note.** On a Mac, test with `/usr/bin/grep`: the shell's `grep` is a ugrep wrapper.
- **`tools/verify_live.py`.** `EXEMPT` plus one compiled regex with the same boundaries, applied before `PATHISH` counts. `PATHISH` is unchanged.
- **`verification/scoreboard.md`.** Traps: the two lists, the clean rule, the Mac `grep`. Sanctioned substitutes: a listed phrase wrapped in markup inside a path is not caught (the same blind spot as any tag-split path).
- **To add a phrase later:** one PR that edits both lists, with Ty's ship. No catch-all patterns.

## Ty's checks
- **Do the routine prompts quote the pattern? No (Verified 2026-10-02, both prompts read live with `RemoteTrigger get`).**
  - The producer ("Monthly system run", `0 3 1 * *`, next 1 Nov 03:00 UTC) and the fallback (`0 1 2 * *`, next 2 Nov 01:00 UTC) both name `docs/audit-refresh.md` as canonical and say "the files win".
  - The fallback's own STEP 4 lists secret strings only.
  - So the runbook and the check change together, and no prompt changes.
- **Merge window.** Ship before the 1 Nov run, and not while a run is due. There's no run before 1 Nov.

## Conflicts
Loaded:
- kernel "standing-instructions.md";
- repo `CLAUDE.md`;
- `REVIEW.md` by reference;
- the artifact-mirror contract (memory);
- entity separation;
- secure-pages (below).

Not loaded: "ty-report-standard" and "apple-design". Nothing on the page changes.

| Rule (by name) | What in the design touches it | Resolution |
|---|---|---|
| Runbook "Sanitisation": a path or file name aborts the write | An exempt phrase is removed before the scan | Only exact whole phrases, never inside a path (requirement 2); the promise proves a neighbouring path still aborts |
| Repo `CLAUDE.md` command line "Secret and path scan of `data/`: the runbook's own greps" | It points to the runbook, so it stays true | No edit needed |
| "Past runs are never rewritten" | No run file changes | No conflict |
| Artifact-mirror contract | The page and the preview are unchanged | No conflict |

## Security (secure-pages, 2026-10-02)
```
1 Secrets ........ PASS (tree 0 files, history 0)
2 Visibility ..... PUBLIC — PASS: the change adds no data
3 Pages .......... PASS: Actions workflow; allowlist serves index.html, data/index.json, data/runs/*.json; unchanged
4 Supabase ....... N/A
Verdict: safe to ship; the change narrows nothing but one named phrase
```

## Promise
Run on the branch, with the runbook's line taken from the file and run as written using `/usr/bin/grep`.
1. **Must abort:**
   - the real Drive path "93 Knowledge Base/Claude outputs/Audit/";
   - "Audit/red/amber/green/" and "red/amber/green/Audit/x/";
   - a path next to "red/amber/green" and next to "(Red/Amber/Green)";
   - "red/amber/green.md", "red/amber/green-x/" and "x.red/amber/green/y/";
   - "Audit/pass/fail/skip/";
   - "/Users/someone", "~/notes" and "report.md".
2. **Must be clean:**
   - "red/amber/green", "Pillars: Red/Amber/Green.", "(red/amber/green)" and "Tổng: red/amber/green.";
   - "PASS/FAIL/SKIP" and "guardrails pass/fail/skip: 3/0/0";
   - "82/100" and "01/10/2026".
3. **Failure paths abort:** a missing run html, and a missing `perl`. A run html whose path has a space scans normally.
4. **The other two alternatives are unchanged:** the `grep` pattern is byte-identical to main's, and no `PATHISH` line changed.
5. **Agreement:** `verify_live.py`'s function agrees with the runbook on every line.
6. **The three published runs** scan clean. `verify_live.py --forbid …` on the branch exits 0.
7. **Then:** the reviewer, Ty's ship, and the verifier on `main`.

## Out of scope
- Folder names without a slash (read by eye, as the runbook already says).
- Any change to the secret list.
- Any change to the routine prompts.
