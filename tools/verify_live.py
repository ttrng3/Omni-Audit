#!/usr/bin/env python3
"""Machine half of verification/scoreboard.md: is what Pages serves what main says, and is main sound?

Run from an up-to-date checkout of main, on the Mac (never from a routine: runbook, live-site fetches):
  git pull --ff-only && python3 tools/verify_live.py --forbid WORD [WORD ...]

--forbid takes words that must not appear on a served file (another entity's name, a person's name or
handle that leaked before). The runner supplies them so the list can change without a PR; docs may name
the other entity's label. Without them the entity check fails rather than passing unchecked.

This script computes no score. It only checks that the published numbers agree with each other.
Prints one JSON object of verdicts and exits 0 only when every verdict is true.
Personal traces, Drive ids and preview tags are reported by count and file, never by value.
"""
import argparse, datetime as dt, glob, hashlib, html, json, pathlib, re, subprocess, sys, time, unicodedata, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://ttrng3.github.io/Omni-Audit/"
# Tracked but never served (.pages-allow); each must exist on main and answer 404 live.
PRIVATE = ["README.md", "CLAUDE.md", "REVIEW.md", "docs/audit-refresh.md", "data/.last-check", "tools/build-fragment.py",
           "tools/reconcile.py", "tools/verify_live.py", "verification/scoreboard.md", ".github/scripts/freshness.py",
           ".pages-allow"]
# Storage links, full email addresses, and bare handles (a word followed by an at-sign and no domain).
TRACES = re.compile(r"/personal(?=/)|sharepoint\.com|1drv\.ms|"
                    r"[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}|\b[a-z][a-z0-9._-]{2,}@(?![\w-])", re.I)
# Not people: GitHub's commit address, @UPPER@ markers, and the runbook's own "`:password@`" example.
BENIGN = re.compile(r"users\.noreply\.github\.com$|^[A-Z0-9_]+@$|^password@$")
DRIVE_ID = re.compile(r"(?<![A-Za-z0-9_-])(?:1[A-Za-z0-9_-]{32}(?:[A-Za-z0-9_-]{11})?|0B[A-Za-z0-9_-]{26})(?![A-Za-z0-9_-])")
PREVIEW_TAG = re.compile(r"(?<![\w-])\d{10}-[0-9a-f]{4}(?![\w-])")  # a Cowork preview version tag
# Runbook "Sanitisation": the run html carries no credential, no folder path and no file name.
SECRETS = re.compile(r"github_pat_|ghp_|gho_|sk-|AKIA|AIza|xoxb-|xoxp-|-----BEGIN|://[^\s/@]+:[^\s/@]+@")
PATHISH = re.compile(r"\b[\w-]+\.(?:md|json|py|xlsx|csv|html|js|txt|pdf)\b|(?:^|[\s(])(?:/Users/|/home/|~/|[A-Z]:\\)|\b\w[\w ]*/[\w ]+/")
# The one sanctioned edit to a past run (Ty, 2026-10-01: a path redacted from the footer). Nothing else may change.
SANCTIONED_EDITS = {"2026-09-12": {"html"}}
HEARTBEAT_MAX = 35  # pipeline-wiring's watchdog for this monthly pipeline (cron 0 3 1 * *)
DATA_MAX = 45       # MAX_DATA_AGE_DAYS default in .github/scripts/freshness.py


def get(path, tries=2):
    """One retry on a network error or a 5xx: a blip must not read as a mismatch."""
    url = f"{LIVE}{path}?v={int(time.time())}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verify-live"}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return get(path, tries - 1) if e.code >= 500 and tries > 1 else (e.code, b"")
    except Exception as e:
        return get(path, tries - 1) if tries > 1 else (str(e), b"")


def age_days(stamp):
    """Days since an ISO stamp ('...Z', '+00:00', 3/6-digit fractions); None if unreadable."""
    try:
        t = dt.datetime.fromisoformat(stamp.strip().replace("Z", "+00:00"))
        t = t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
        return round((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 86400, 1)
    except (ValueError, AttributeError):
        return None


def text_of(s):
    """What a reader sees: entities decoded, tags removed."""
    return re.sub(r"<[^>]*>", " ", html.unescape(str(s or "")))


def norm(t):
    return unicodedata.normalize("NFC", text_of(t)).casefold()


def git(*args):
    """Raise on a git failure: an empty answer must never read as "nothing to check"."""
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", nargs="*", default=[])
    forbid = [norm(w) for w in ap.parse_args().forbid if w.strip()]
    v, info, live = {}, {}, {}

    try:
        d = json.loads((ROOT / "data/index.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        d, info["index_error"] = {}, str(e)
    d = d if isinstance(d, dict) else {}
    runs = [r for r in d.get("runs", []) if isinstance(r, dict)]
    ids = [str(r.get("id")) for r in runs]
    files = sorted(pathlib.Path(f).stem for f in glob.glob(str(ROOT / "data/runs/*.json")))
    loaded = {}
    for i in files:
        try:
            loaded[i] = json.loads((ROOT / f"data/runs/{i}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            loaded[i] = None

    v["runs_well_formed"] = bool(ids) and all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", i) for i in ids)
    v["runs_newest_first_unique"] = ids == sorted(ids, reverse=True) and len(set(ids)) == len(ids)
    v["current_is_newest"] = bool(ids) and d.get("current") == ids[0]
    v["run_files_match"] = sorted(ids) == files and all(loaded[i] is not None and loaded[i].get("id") == i for i in files)

    # The producer scores; here the published numbers only have to agree: score = sum of pillars, file = manifest.
    def agrees(r):
        f = loaded.get(str(r.get("id"))) or {}
        p = r.get("pillars") or {}
        return (all(isinstance(x, int) for x in p.values()) and isinstance(r.get("score"), int) and
                0 <= r["score"] <= 100 and r["score"] == sum(p.values()) and
                f.get("score") == r["score"] and f.get("pillars") == p)
    v["scores_agree"] = bool(runs) and all(agrees(r) for r in runs)

    # Runs are immutable once written: each file, parsed, equals its first committed version, except SANCTIONED_EDITS.
    changed = {}
    try:
        for i in files:
            first = git("log", "--diff-filter=A", "--format=%H", "--", f"data/runs/{i}.json").split()
            if not first or loaded[i] is None:
                continue
            orig = json.loads(git("show", f"{first[-1]}:data/runs/{i}.json"))
            diff = {k for k in set(orig) | set(loaded[i]) if orig.get(k) != loaded[i].get(k)} - SANCTIONED_EDITS.get(i, set())
            if diff:
                changed[i] = sorted(diff)
        v["runs_immutable"] = not changed
    except (subprocess.CalledProcessError, ValueError):
        v["runs_immutable"] = False
    info["runs_changed_keys"] = changed

    # Runbook "Sanitisation", on what a reader sees of each run.
    info["sanitisation_hits"] = {i: {"secrets": len(SECRETS.findall(r.get("html", ""))),
                                     "paths_or_files": len(PATHISH.findall(text_of(r.get("html", ""))))}
                                 for i, r in loaded.items() if r and (SECRETS.search(r.get("html", "")) or PATHISH.search(text_of(r.get("html", ""))))}
    v["runs_sanitised"] = not info["sanitisation_hits"]

    served = ["index.html", "data/index.json"] + [f"data/runs/{i}.json" for i in files]
    for p in served:
        st, body = get(p)
        live[p] = body
        info[p] = {"status": st, "live": hashlib.sha256(body).hexdigest()[:12],
                   "main": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12] if (ROOT / p).exists() else None}
    v["served_equals_main"] = all(info[p]["status"] == 200 and info[p]["live"] == info[p]["main"] for p in served)
    info["served_mismatch"] = [p for p in served if info[p]["status"] != 200 or info[p]["live"] != info[p]["main"]]
    for p in served:
        del info[p]

    work = sorted(glob.glob(str(ROOT / "work/*/intent.md")))[:1]  # any one work file, found at run time
    private = PRIVATE + [str(pathlib.Path(w).relative_to(ROOT)) for w in work]
    info["private_status"] = {p: get(p)[0] for p in private}
    info["private_missing_on_main"] = [p for p in private if not (ROOT / p).exists()] + ([] if work else ["work/*/intent.md"])
    v["private_not_served"] = all(s == 404 for s in info["private_status"].values()) and not info["private_missing_on_main"]

    beat = ((ROOT / "data/.last-check").read_text(encoding="utf-8").split() or [""])[0] if (ROOT / "data/.last-check").exists() else ""
    info["heartbeat_age_days"], info["data_age_days"] = age_days(beat), age_days(str(d.get("generatedUtc", "")))
    # -1 allows clock skew; a stamp further in the future (a wrong year) would otherwise pass forever.
    v["heartbeat_fresh"] = info["heartbeat_age_days"] is not None and -1 <= info["heartbeat_age_days"] <= HEARTBEAT_MAX
    v["data_fresh"] = info["data_age_days"] is not None and -1 <= info["data_age_days"] <= DATA_MAX

    # Served files, live and on main, then every other tracked text file on main (the repo is public).
    texts = {f"live:{p}": b.decode("utf-8", "replace") for p, b in live.items()}
    texts.update({f"main:{p}": (ROOT / p).read_text(encoding="utf-8") for p in served if (ROOT / p).exists()})
    info["unreadable"] = []
    try:
        tracked = [x for x in git("ls-files", "-z").split("\0") if x]
    except subprocess.CalledProcessError:
        tracked = []
    info["tracked_files"] = len(tracked)
    for p in tracked:
        if p in served:
            continue
        try:
            texts[f"main:{p}"] = (ROOT / p).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass  # binary file
        except OSError:
            info["unreadable"].append(p)
    v["all_tracked_read"] = bool(tracked) and not info["unreadable"]

    hits = {p: sum(1 for m in TRACES.finditer(t) if not BENIGN.search(m.group(0))) for p, t in texts.items()}
    info["traces"] = {p: n for p, n in hits.items() if n}
    v["no_personal_traces"] = not info["traces"]
    info["drive_ids_tracked"] = {k: len(DRIVE_ID.findall(t)) for k, t in texts.items() if DRIVE_ID.search(t)}
    v["no_drive_ids_tracked"] = not info["drive_ids_tracked"]
    info["preview_tags_tracked"] = {k: len(PREVIEW_TAG.findall(t)) for k, t in texts.items() if PREVIEW_TAG.search(t)}
    v["no_preview_tags_tracked"] = not info["preview_tags_tracked"]
    served_texts = [t for k, t in texts.items() if k.split(":", 1)[1] in served]
    info["forbid_checked"] = len(forbid)
    v["no_forbidden_words"] = bool(forbid) and not any(w in norm(t) for w in forbid for t in served_texts)

    print(json.dumps({"pass": all(v.values()), "verdicts": v, "info": info}, ensure_ascii=False, indent=1))
    sys.exit(0 if all(v.values()) else 1)


if __name__ == "__main__":
    main()
