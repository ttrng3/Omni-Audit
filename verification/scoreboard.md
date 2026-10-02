# Verification: the audit scoreboard

## Promise

Every file https://ttrng3.github.io/Omni-Audit/ serves (the page, `index.json`, every run file) is byte-identical to `main`. The manifest lists well-formed run dates, newest first, `current` is the newest, and each run has its file carrying its own id. Each run's score is an integer from 0 to 100 equal to the sum of its pillars, and the run file agrees with the manifest. No run file has changed since it was first written, apart from the one redaction Ty sanctioned on 2026-10-01. No string anywhere in a run file or the manifest carries a credential, a folder path or a file name. The page renders the current run. No private file, personal link, email address, account handle, Drive id or Cowork preview tag sits in any served or tracked file, and no word from another entity is served. The Cowork preview carries `main`'s data or the last run's.

## Clean state

```bash
cd ~/Projects/Omni-Audit && git checkout main && git pull --ff-only
```
Run on the Mac, never from a routine (runbook, "Verifying a run — never fetch the live site"). Run after the monthly publish (cron `0 3 1 * *` UTC = 10:00 Hanoi on the 1st, per pipeline-wiring's `collect_status.py` on 01/10), after the 2nd-of-month fallback, or after any merge, once the merge's Pages run is green (`gh run list -w "Pages (allowlist)" -L1`).

## Steps

1. **Repo and live site.** `python3 tools/verify_live.py --forbid <words>` → exit 0 and `"pass": true`. The words come from the runner's own notes (the other entity's name, any person's name or handle that leaked before). They are never written into this repo. Without `--forbid` the entity verdict fails on purpose.
2. **Live page in Chrome.** Open https://ttrng3.github.io/Omni-Audit/ and run the script under Invariants. Expected: the page shows the current run's label and score; no load-error message; no link to a storage host; no file name in the visible text.
3. **Console.** Reload, then read errors for `TypeError|ReferenceError|Uncaught|SyntaxError`. Expected: none.
4. **Preview.** Get the preview link from the publisher routine's prompt (`RemoteTrigger get`). Never write it here. Find the last run: `c=$(git log --first-parent --format='%h %s' -- data/index.json | grep -v ' (#[0-9]*)$' | grep -v '^[0-9a-f]* Merge ' | head -1 | cut -d' ' -f1)`. `Artifact list` the preview's files and `Artifact read` `data/index.json` and the current run's file. Expected: the page fragment plus the data files `main` or `$c` holds, nothing else; each file read has the sha256 of `main`'s copy (`shasum -a 256 <path>`) or `$c`'s (`git show $c:<path> | shasum -a 256`).

## Invariants

Step 1 prints these verdicts, all of which must be true: `runs_well_formed`, `runs_newest_first_unique`, `current_is_newest`, `current_month_published` (from 06:00 UTC on the 2nd, after the fallback's slot, `current` must be this month's run), `run_files_match`, `scores_agree`, `runs_immutable` (each run file, parsed, equals its first committed version; `SANCTIONED_EDITS` allows one key of one run to equal exactly #7's final redacted text, pinned by its sha256), `runs_sanitised` (runbook "Sanitisation": no credential, folder path or file name in any string of any run file or the manifest), `served_equals_main`, `private_not_served`, `heartbeat_fresh` (≤ 35 days, pipeline-wiring's watchdog for this monthly pipeline), `data_fresh` (≤ 45 days, `freshness.py`'s `MAX_DATA_AGE_DAYS` default), `all_tracked_read`, `no_personal_traces`, `no_drive_ids_tracked`, `no_preview_tags_tracked`, `no_forbidden_words`.

Step 2, in the page (no query strings in the fetches: the browser tool blocks them):
```js
await new Promise(r=>setTimeout(r,2500));
const idx=await fetch('data/index.json').then(r=>r.json());
const cur=idx.runs.find(r=>r.id===idx.current);
const dash=s=>s.replace(/[\u2010\u2011\u2012\u2013]/g,'-');
const page=dash(document.body.innerText), app=document.getElementById('app').innerText;
JSON.stringify({current_label_shown:page.includes(dash(cur.label)), current_score_shown:new RegExp('(^|[^0-9])'+cur.score+'([^0-9]|$)').test(app),
  no_load_error:!app.includes('data/index.json'),
  no_storage_links:!document.querySelector('a[href*="sharepoint"],a[href*="1drv"],a[href*="drive.google"],a[href*="personal/"]'),
  no_file_names:!/\b[\w-]+\.(md|json|py|xlsx|csv|html|js|txt|pdf)\b/.test(page)})
```
All of them must be true.

## Adversary

- **A stranger on the public scoreboard.** `runs_sanitised` and step 2's `no_file_names`: the 12/09 run showed a Drive folder, the mirror's file name, two control folders and what one exposes, until Ty had them redacted on 01/10 (#7). `private_not_served`: README, CLAUDE.md, REVIEW.md, the runbook, the heartbeat, the three `tools/` scripts, this protocol, one `work/` file found at run time, `freshness.py` and `.pages-allow` all exist on `main` and answer 404 live. `no_personal_traces`, `no_drive_ids_tracked` and `no_preview_tags_tracked` read every served file live and on `main` and every other tracked text file (the repo is public), reporting by count and file, never by value.
- **A publisher that rewrites history.** `runs_immutable`: any key of any past run that differs from its first commit, outside `SANCTIONED_EDITS`, fails.
- **A handoff whose numbers do not add up, or a publisher that edits a score.** `scores_agree` (score = sum of pillars, file = manifest). This script computes no score.
- **A publisher that fires before the day's handoff** (22/09: the page stayed on an old run). `current_month_published`: once the 2nd-of-month fallback has had its slot, an old `current` fails. (`heartbeat_fresh` and `data_fresh` alone would pass for weeks.)
- **Another entity's data.** `no_forbidden_words` on served files, as a reader sees them.

## Sanctioned substitutes

- The forbidden word list is passed on the command line, so it can change without a PR. It cannot catch a name nobody has listed. It reads served files only: REVIEW.md's own entity-separation rule names the other entity's label, so a repo-wide word check would fail on the rule itself.
- The manifest's `pages` and `repo` keys are left out of the sanitisation scan: they hold the public addresses themselves.
- A folder's bare name (a word like "Legal" with no slash) cannot be told from prose by a pattern, so `runs_sanitised` catches paths and file names only; folder names are read by eye in the run's tiles and watchlist.
- The preview cannot be fetched by a script, so step 4 is done by the runner with `Artifact list` and `Artifact read`.

## Evidence

- The JSON from step 1 and the JSON from step 2.
- One screenshot (`save_to_disk: true`) of the page with the current run.
- For step 4: the preview's file list and the hashes read.

## Not covered

- Whether the producer's scores are right: this repo carries the handoff and never scores (CLAUDE.md).
- A bare folder name in a run's prose (see Sanctioned substitutes).
- Git history still holds the 12/09 footer and folder names removed on 01/10 (Ty ruled to leave history, 01/10).

## Traps

- The script adds a cache-busting query to every request, so a `served_equals_main` failure straight after a merge means the Pages run has not finished: wait for it to go green, then re-run. Each request retries once on a network error or a 5xx.
- The 01/10 run file has two commits (a trailing newline fixed three minutes later in the same run). `runs_immutable` compares parsed JSON, so whitespace never counts.
- The browser tool refuses fetches with a query string, so step 2 fetches plain paths (01/10).
- The run label sits in the page header, outside `#app`, and the page draws its hyphens as non-breaking (U+2011); step 2 reads the whole page and folds hyphens before comparing (01/10).
- The runbook quotes `:password@` as an example of what to scan for; the trace check allows that one string by name.
- The path scan ignores exact whole phrases, kept in two lists that must match: the runbook's `perl` step and `EXEMPT` in `tools/verify_live.py` ("red/amber/green", "pass/fail/skip" on 02/10), and only where they stand alone; a listed phrase inside a path or a file name still counts. The runbook's scan is clean only with no output at all and exit 1, so an unreadable run html aborts. On a Mac, test the runbook's line with `/usr/bin/grep`: the shell's `grep` is a ugrep wrapper that matches neither the prose nor a real path (02/10).
