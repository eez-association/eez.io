# eez.io + integrate merge demo

Local demo of the Figma proposal ("EEZ Customer Journey" → 2 · Proposed site): integrate's pages live under eez.io with one shared header and footer.

- `/` — eez.io home from `0xarmagan/eez-website-mockup` (stands in for Framer). New header, hero buttons "Use cases" / "Start building", four audience doors, "All use cases →" under the carousel, shared footer.
- `/use-cases/institutions|chains|apps|infra|all|kit|scoping`, `/status`, `/get-in-touch` — pages from `0xarmagan/eez-integrate-site` (built `dist/`), integrate header/footer swapped for the shared ones, links remapped.

## Rebuild
```
rm -rf _src && mkdir _src && cd _src
gh repo clone 0xarmagan/eez-website-mockup mockup -- --depth 1
gh repo clone 0xarmagan/eez-integrate-site integrate -- --depth 1
(cd integrate && npm ci && npm run build) && cd ..
python3 assemble.py
PORT=8885 node serve.mjs      # http://localhost:8885
```

## GitHub Pages
Every push to `main` runs `.github/workflows/pages.yml`: `tools/pages.py` copies `dist/` to `_site/`, puts the repo path (`/<repo>`) in front of every root link, adds a noindex tag and `.nojekyll`, then deploys. The path follows the repo name, so it keeps working after a transfer to another org. For a custom domain, set the repo variable `CUSTOM_DOMAIN` (e.g. `eez.io`) and the links drop the prefix.

Local check: `BASE=/eez.io python3 tools/pages.py`

Full link, animation and component list: [INVENTORY.md](INVENTORY.md).

## Files
- `shared/` — header, footer, Devcon bar, shell.css/js, logo (the one source for both origins)
- `assemble.py` — copies + rewrites both sources into `dist/`
- `serve.mjs` — static server with clean URLs (like Vercel `cleanUrls`)

In production the same split would be Framer Multi Site rewrites (see `agent-mesh/outputs/eez-io-integrate-merge-plan.md`).
