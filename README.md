# eez.io merge demo

eez.io home plus the integrate use-case pages, under one shared header and footer.

Live: https://0xarmagan.github.io/eez.io/

- `/`: eez.io home (stands in for Framer)
- `/use-cases/*`, `/get-in-touch`: pages from `eez-integrate-site`

## Build
```
rm -rf _src && mkdir _src && cd _src
gh repo clone 0xarmagan/eez-website-mockup mockup -- --depth 1
gh repo clone 0xarmagan/eez-integrate-site integrate -- --depth 1
(cd integrate && npm ci && npm run build) && cd ..
python3 assemble.py           # → dist/, then live parity + smart quotes
PORT=8885 node serve.mjs      # http://localhost:8885
```

## Deploy
Every push to `main` publishes `dist/` to GitHub Pages (`tools/pages.py`). Set the repo variable `CUSTOM_DOMAIN` to serve from a domain.

## More
- [PARITY.md](PARITY.md): differences from live eez.io
- [INVENTORY.md](INVENTORY.md): links, animations, components
