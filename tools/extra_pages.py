"""Pages that exist only in this repo (not in the mockup or integrate sources): /brand and /media.

Each file in pages/*.html is a full document with three markers that get the shared parts:
<!--DEVCON-->, <!--HEADER--> and <!--FOOTER-->. Fonts, tokens.css, shell.css and shell.js are added
like on every other page, and pages/assets/ is copied into dist/assets/. Runs right after
live_parity.py, so the copy, audit, token and quote steps also process these pages.
"""
import shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from assemble import DEVCON, HEADER, FOOTER, FONTS, SHELL_HEAD, SHELL_JS  # noqa: E402

SRC, OUT = ROOT / "pages", ROOT / "dist"


def main():
    for page in sorted(SRC.glob("*.html")):
        html = page.read_text()
        for mark, part in (("<!--DEVCON-->", DEVCON), ("<!--HEADER-->", HEADER), ("<!--FOOTER-->", FOOTER)):
            if html.count(mark) != 1:
                sys.exit(f"extra_pages: {page.name} needs exactly one {mark}")
            html = html.replace(mark, part)
        html = html.replace("</head>", f"{FONTS}\n{SHELL_HEAD}\n</head>", 1)
        html = html.replace("</body>", f"{SHELL_JS}\n</body>", 1)
        (OUT / page.name).write_text(html)
    shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
    print("extra pages:", ", ".join(p.stem for p in sorted(SRC.glob("*.html"))))


if __name__ == "__main__":
    main()
