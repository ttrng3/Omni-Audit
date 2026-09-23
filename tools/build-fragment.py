#!/usr/bin/env python3
"""Derive the claude.ai artifact page from index.html.

The same markup cannot serve both surfaces. GitHub Pages needs a complete
document; the artifact service wraps whatever you publish in its own
<!doctype html><html><head>...</head><body>, so publishing a complete document
nests one inside another. The browser discards the inner <head>, every <style>
and <link> in it stops applying, and the page renders BLANK with no console
error — which gives you nothing to debug from.

So the artifact gets a FRAGMENT: everything from <title> onward, with no
doctype and no html/head/body tags. This script cuts it, and checks the result
rather than trusting the cut.

The data layer needs no change. Supporting files published alongside the page
are same-origin, so the renderer's relative `fetch('data/…')` resolves there
exactly as it does on Pages.

Usage:
    python3 tools/build-fragment.py [out]      # default: build/artifact.html
"""
import pathlib
import re
import sys

BANNED = re.compile(r"<!doctype|<html[\s>]|</html>|<head[\s>]|</head>|<body[\s>]|</body>", re.I)


def build(src="index.html"):
    doc = pathlib.Path(src).read_text(encoding="utf-8")

    start = doc.lower().find("<title>")
    if start < 0:
        sys.exit(f"{src}: no <title> — cannot find where the fragment starts")
    frag = doc[start:]

    # index.html ends with the wrapper's own closing tags; drop them.
    frag = re.sub(r"\s*</body>\s*</html>\s*$", "\n", frag, flags=re.I)

    leftover = BANNED.search(frag)
    if leftover:
        line = frag[:leftover.start()].count("\n") + 1
        sys.exit(f"{src}: document tag {leftover.group(0)!r} survives on line {line} "
                 "of the fragment — the artifact would render blank")
    return frag


def main(out="build/artifact.html"):
    frag = build()
    path = pathlib.Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frag, encoding="utf-8")
    print(f"{path}  {len(frag.encode()):,} bytes  (starts: {frag[:40]!r})")
    print("publish the data/ files FIRST, then this page on its own — a page sent in "
          "the same call as a large files payload has come back blank.")


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
