# Spec: path-grep

**Approved:** 2026-10-02 (Ty, in chat)

**Simplest version approved:** 2026-10-02 (Ty, in chat), after six review rounds on the boundary design kept finding new edges. It replaces the earlier post-review design; that history is in the PR's commits. Ty's terms: a multi-slash path next to the phrase still aborts, and the three accepted limits are listed in the protocol in one place. Limits accepted by Ty: a tag inside a path around the phrase, and an entity-encoded slash beside it (both 2026-10-02); the phrase-slash class (approved with this version).

**Intent:** accepted 2026-10-02 · **Status:** approved

## Requirements
1. Before the path scan, each exempt phrase is replaced by the word `RAG`. The phrases are exact whole phrases (word-bounded, so never part of a longer word such as "Covered/Amber/Green") and matched in any case, kept in one list per copy: `red/amber/green`, `pass/fail/skip` (intent, answer (a); the intent's Outcome).
2. A phrase's own slashes never count toward a path. Every other character is scanned exactly as before: the `grep` pattern is unchanged, and so is `PATHISH`.
3. A path with two linked slashes of its own still aborts, whether it sits next to the phrase or around it (Ty, 2026-10-02).
4. The scan fails safe: "clean" is no output at all (stdout or stderr) and exit 1, so an unreadable run html or a missing `perl` aborts.
5. `tools/verify_live.py` applies the same list the same way.
6. The three accepted limits are listed in one place in `verification/scoreboard.md`.

## Design
- **The runbook line.** No pipe:
  ```
  r=; t=$(mktemp) && perl -CSD -e 'my $p = shift; -f $p or die "scan input: not a file\n"; open(my $f, "<", $p) or die "scan input: $!\n"; while (<$f>) { s{\b(?:red/amber/green|pass/fail/skip)\b}{RAG}gi; print }' "<run html>" > "$t" && { grep -niE '<the pattern, unchanged>' "$t"; r=$?; } || r=${r:-2}; rm -f "$t"; (exit $r)
  ```
  - `perl` dies unless the input is a readable regular file (a directory is refused).
  - The temp file is fresh and is removed after the result is read.
  - The path is quoted, so a space in it can't break the scan.
  - A failure before `grep` (no temp file, an unreadable run html) exits 2, never the clean code 1.
  - On a Mac, test with `/usr/bin/grep`: the shell's `grep` is a ugrep wrapper.
- **`tools/verify_live.py`.** `EXEMPT` with the same two phrases. `EXEMPT_RE` is their alternation between word boundaries, case-insensitive. Each phrase is replaced by `RAG` on the raw string, then `text_of`, then `PATHISH`.
- **`verification/scoreboard.md`.**
  - Sanctioned substitutes: one entry with the rule and the three accepted limits.
  - Limit 1 is still flagged after publish by `runs_sanitised`, because `verify_live.py` reads text with tags removed. It did the same on `main` for any tag-split path.
  - Traps: the two lists must match, the clean rule, and the Mac `grep`.
- **Repo `CLAUDE.md`.** The command line states the clean rule.
- **To add a phrase later:** one PR that edits both lists, with Ty's ship.

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
| Runbook "Sanitisation": a path or file name aborts the write | Each exempt phrase becomes `RAG` before the scan | Exact whole phrases only (word-bounded); a path around the phrase still aborts through its own slashes; the three cases where it doesn't are Ty's accepted limits |
| Repo `CLAUDE.md` command line "Secret and path scan of `data/`: the runbook's own greps" | Its clean rule changes | Edited: "no output at all (stdout or stderr) and exit 1" |
| "Past runs are never rewritten" | No run file changes | No conflict |
| Artifact-mirror contract | The page and the preview are unchanged | No conflict |

## Security (secure-pages, 2026-10-02)
```
1 Secrets ........ PASS (tree 0 files, history 0)
2 Visibility ..... PUBLIC — PASS: the change adds no data
3 Pages .......... PASS: Actions workflow; allowlist serves index.html, data/index.json, data/runs/*.json; unchanged
4 Supabase ....... N/A
Verdict: safe to ship; the scan ignores only the two named phrases' own slashes
```

## Promise
Run on the branch, with the runbook's line taken from the file and run as written using `/usr/bin/grep`; `verify_live.py`'s function on the same lines.
1. **Must abort, in both copies** (19 lines):
   - "Covered/Amber/Green/", "Bypass/Fail/Skip/" and "Scared/Amber/Greenhouse/" (the phrase inside a longer word is not exempt);
   - the real Drive path, and the same path next to the phrase on either side ("93 Knowledge Base/Claude outputs/Audit/ red/amber/green");
   - "(Red/Amber/Green) Claude outputs/Audit/";
   - "Audit/red/amber/green/", "red/amber/green/Audit/x/", "red/amber/green.md" and "x.red/amber/green/y/";
   - "Audit/pass/fail/skip/" and "(red/amber/green)/Audit/";
   - `<td>Audit/red/amber/green/x/</td>` and `<p>93 Knowledge Base/Claude outputs/Audit/</p>`;
   - "/Users/someone", "/home/x", "~/notes" and "report.md".
2. **Must be clean, in both copies** (13 lines):
   - "red/amber/green", "Pillars: Red/Amber/Green.", "(red/amber/green)" and "Tổng: red/amber/green.";
   - "PASS/FAIL/SKIP" and "guardrails pass/fail/skip: 3/0/0";
   - "82/100" and "01/10/2026";
   - `<td>red/amber/green</td>`, `<b>Red/Amber/Green</b>`, `<li>pass/fail/skip</li>`, `<span class="rag">red/amber/green</span>: 4 pillars` and `<br/>Red/Amber/Green`.
3. **The accepted limits behave as recorded:**
   - the runbook line passes all five example lines;
   - `verify_live.py` passes four of them and flags limit 1.
4. **Failure paths:** a missing run html aborts.
5. **Unchanged:** the `grep` pattern is byte-identical to `main`'s, and no `PATHISH` line changed.
6. **The three published runs** scan clean. `verify_live.py --forbid …` on the branch exits 0.
7. **Then:** the reviewer, Ty's ship, and the verifier on `main`.

## Out of scope
- Folder names without a slash (read by eye, as the runbook already says).
- Any change to the secret list.
- Any change to the routine prompts.

## Follow-up after merge (review on the merged code, 2026-10-03)
Ty asked for a review of d554fe3 before shipping; his message arrived after the merge (ea40908, identical tree), so the review ran on the merged code. Its two Mediums are fixed in a follow-up PR, under this folder:
- The runbook now says what `<run html>` is: a file on disk with the html exactly as published (not JSON-escaped, not a pipe or `/dev/stdin`).
- `verify_live.py` gains `exempt_lists_match`, which fails unless the runbook's perl phrases equal `EXEMPT`; checked both ways on the branch.
Its Lows: the PR #9 description's `set -e` line was stale and is removed; the `CLAUDE.md` scope wording ("each run's html, one file at a time") is recorded here as part of the design.
