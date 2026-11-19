"""Curl straight quotes in visible text of every built page (dist/**/*.html).

Only text between tags changes; tags, attributes, <script>, <style>, <code>, <pre>
and <textarea> stay byte-identical. ' -> ’ (or ‘ when it opens a word), "..." -> “...”.
Strings that scripts render (inline <script> data and dist/**/*.js) only get the
letter'letter apostrophe curled, which never touches code syntax; both sides change
together, so string matches such as .replace("Buyer's custodian", …) keep working.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"script", "style", "code", "pre", "textarea"}
TOKEN = re.compile(r"(<!--.*?-->|<[^>]+>)", re.S)
APOS = re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])")


def curl(text, prev):
    out = []
    dq_open = True
    for ch in text:
        if ch == "'":
            out.append("‘" if (not prev or prev.isspace() or prev in "([{—-") else "’")
        elif ch == '"':
            out.append("“" if dq_open else "”")
            dq_open = not dq_open
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def fix(html):
    parts = TOKEN.split(html)
    skip, prev, n = [], "", 0
    for i, p in enumerate(parts):
        raw = skip and skip[-1] in ("script", "style")
        if raw:
            # Inside <script>/<style> only the matching end tag counts: anything tag-shaped is
            # text there (e.g. "<code>" inside JSON data) and must not open a new skip level.
            if i % 2 and re.match(r"</" + skip[-1] + r"\b", p, re.I):
                skip.pop()
                continue
            if skip[-1] == "script":
                new, k = APOS.subn("\u2019", p)
                parts[i], n = new, n + k
            continue
        if i % 2:  # tag or comment
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", p)
            if m:
                name = m.group(2).lower()
                if name in SKIP and not p.endswith("/>"):
                    if m.group(1):
                        if skip and skip[-1] == name:
                            skip.pop()
                    else:
                        skip.append(name)
            continue
        if skip or ("'" not in p and '"' not in p):
            if p.strip():
                prev = p.rstrip()[-1:]
            continue
        new = curl(p, prev if not p[:1].isspace() else " ")
        n += sum(a != b for a, b in zip(p, new))
        parts[i] = new
        prev = new.rstrip()[-1:]
    return "".join(parts), n


def main():
    total = 0
    for f in sorted((ROOT / "dist").rglob("*.html")):
        html = f.read_text()
        new, n = fix(html)
        if n:
            f.write_text(new)
            print(f"smart quotes: {f.relative_to(ROOT)} ({n})")
            total += n
    for f in sorted((ROOT / "dist").rglob("*.js")):
        if "vendor" in f.parts:  # third-party code stays as shipped
            continue
        js = f.read_text()
        new, n = APOS.subn("\u2019", js)
        if n:
            f.write_text(new)
            print(f"smart quotes: {f.relative_to(ROOT)} ({n})")
            total += n
    print("smart quotes total:", total)


if __name__ == "__main__":
    main()
