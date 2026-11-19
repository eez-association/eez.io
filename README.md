# eez.io

The next eez.io: the home page, the use-case pages, Get in touch, Brand and Media, as one static site with one header, footer and colour system. Built from two source repos plus this repo's own pages, and published on GitHub Pages.

Preview: https://eez-association.github.io/eez.io/

## Pages
| Path | What | Source |
|---|---|---|
| `/` | Home | `eez-website-mockup`, matched to live eez.io |
| `/use-cases/institutions`, `chains`, `apps`, `infra`, `all` | Use cases by audience | `eez-integrate-site` |
| `/use-cases/scoping`, `/use-cases/kit` | Joining steps, integration kit | `eez-integrate-site` |
| `/get-in-touch` | Contact form | `eez-integrate-site` + `shared/get-in-touch.main.html` |
| `/brand`, `/media` | Logo downloads, press and talks | `pages/` (this repo) |

The blog stays on Framer; Latest cards and the News link point there.

## Build
```
rm -rf _src && mkdir _src && cd _src
gh repo clone 0xarmagan/eez-website-mockup mockup -- --depth 1
gh repo clone 0xarmagan/eez-integrate-site integrate -- --depth 1
(cd integrate && npm ci && npm run build) && cd ..
python3 assemble.py           # → dist/
PORT=8885 node serve.mjs      # http://localhost:8885
```
The two source repos are private; `dist/` is committed, so the site deploys without them.

`assemble.py` copies both sources into `dist/`, swaps in the shared header and footer, then runs these steps in order. Each step stops the build if something it expects is missing.

| Step | Does |
|---|---|
| `tools/live_parity.py` | Home matches live eez.io: background, one-call diagram, progress timeline, Latest posts |
| `tools/extra_pages.py` | Builds `pages/*.html` (Brand, Media) with the shared parts |
| `tools/copy_fixes.py` | Agreed copy: audience names, chain not zone, devnet, Live / Devnet only / Planned, no em-dashes |
| `tools/hero_fixes.py` | Infra diagram uses the same line animation as Apps and Chains |
| `tools/audit_fixes.py` | Skip link, heading order, lazy images, image sizes |
| `tools/tokens_fix.py` | Hard-coded colours → tokens from `shared/tokens.css` |
| `tools/smart_quotes.py` | Curly quotes and apostrophes in visible text |

## Where to change things
- **Colours, lines, radii:** `shared/tokens.css` (every page reads it)
- **Header, footer, Devcon bar:** `shared/header.html`, `footer.html`, `devcon.html`, styles in `shared/shell.css`
- **Wording on source pages:** add a before → after pair to `tools/copy_fixes.py`
- **Latest posts on Home:** the `POSTS` list in `tools/live_parity.py`; covers go in `tools/live-media/`
- **New page of our own:** a full HTML file in `pages/` with `<!--DEVCON-->`, `<!--HEADER-->`, `<!--FOOTER-->`; its files in `pages/assets/`

Then run `python3 assemble.py`, check the preview and open a pull request.

## Deploy
Every push to `main` publishes `dist/` to GitHub Pages: `tools/pages.py` adds the repo path to root links (`/eez.io/...`), a `noindex` tag and `.nojekyll`. Once the repo variable `CUSTOM_DOMAIN` is set (e.g. `eez.io`), links drop the prefix and a `CNAME` is written.

## Notes
- [PARITY.md](PARITY.md): how Home compares with live eez.io
- [INVENTORY.md](INVENTORY.md): links, animations and components (written at the start; partly out of date)
- `.impeccable/config.json`: design-checker exceptions, each with its reason
