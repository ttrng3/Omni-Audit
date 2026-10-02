# Spec: path-grep

**Intent:** accepted 2026-10-02 · **Status:** draft

## Requirements
1. Before the path scan, remove each exempt phrase from the text. The exempt phrases are exact whole phrases, kept in one list (intent, answer (a)).
2. A phrase is removed only where it stands alone: not preceded or followed by a letter, a digit or a `/`. So "red/amber/green" inside a path ("Audit/red/amber/green/") is not removed, and the path still aborts.
3. A real path next to an exempt phrase still aborts the publish (Ty, 2026-10-02).
4. The scan's other two alternatives are unchanged: the file-name alternative, and the `/Users/`, `/home/`, `~/` alternative (Ty, 2026-10-02). The third alternative, the folder-path rule, is unchanged too. Only the input to it changes.
5. The scoreboard check in `tools/verify_live.py`, which carries its own copy of the pattern (`PATHISH`), applies the same list the same way.

## Design
- **The list.** One line in the runbook's "Sanitisation" section, and the same list as `EXEMPT` in `tools/verify_live.py`. It starts with one phrase: `red/amber/green`, the page's own RAG wording, matched case-insensitively.
  - Phrases with one slash ("pass/fail") need no entry, because the folder rule needs two slashes.
  - The three published runs contain no two-slash phrase today (checked 2026-10-02).
- **The runbook command.** The `grep` line stays byte for byte. In front of it, one `perl` stage removes the listed phrases where they stand alone:
  ```
  perl -pe 's{(?<![[:alnum:]/])(?:red/amber/green)(?![[:alnum:]/])}{ }gi' <run html> | grep -niE '<the pattern, unchanged>'
  ```
  - `perl` is on the cloud image and the Mac, and behaves the same on both.
  - `sed`'s case flag is GNU-only, and the Mac's shell `grep` is a ugrep wrapper. That's why the runbook also says to test the line with `/usr/bin/grep` on a Mac.
  - "Clean" stays the same: the line prints nothing and exits 1.
- **`tools/verify_live.py`.** `EXEMPT = ["red/amber/green"]` and one compiled regex with the same boundaries. The text is stripped before `PATHISH` counts, and `PATHISH` itself is unchanged.
- **`verification/scoreboard.md`.** One line under Traps naming the exemption list, and the Mac `grep` trap.
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
Run on the branch.
1. **The runbook line itself.** The `perl | /usr/bin/grep` line, copied from the runbook, runs on a fixed file of test lines.
   - **Each of these must hit:**
     - the real Drive path "93 Knowledge Base/Claude outputs/Audit/";
     - "Audit/red/amber/green/";
     - "red/amber/green/Audit/x/";
     - "red/amber/green 93 Knowledge Base/Claude outputs/Audit/" (a path next to the phrase);
     - "(Red/Amber/Green) Claude outputs/Audit/";
     - "/Users/someone", "~/notes", "report.md".
   - **Each of these must pass:**
     - "red/amber/green";
     - "Pillars: Red/Amber/Green.";
     - "(red/amber/green)";
     - "82/100";
     - "01/10/2026".
2. **The other two alternatives are unchanged.** `git diff` on the runbook shows the `grep` pattern string unchanged, and `PATHISH` in `verify_live.py` unchanged. The file-name and `/Users/`/`/home/`/`~/` test lines hit with and without the `perl` stage.
3. **`verify_live.py`.** The same test lines give the same hit or pass through its function as through the runbook line.
4. **The three published runs** still scan clean. `verify_live.py` on the branch exits 0.
5. **Then:** the reviewer, Ty's ship, and the verifier on `main`.

## Out of scope
- Folder names without a slash (read by eye, as the runbook already says).
- Any change to the secret list.
- Any change to the routine prompts.
