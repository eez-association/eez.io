// Link-preview images (1200x630) for every page, from tools/og/pages.json.
// Writes pages/assets/og/<id>.png, which the build copies to dist/assets/og/.
// Run after changing pages.json:  NODE_PATH=<dir with puppeteer> node tools/og/render.mjs
import { readFileSync, mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const puppeteer = require("puppeteer");
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const pages = JSON.parse(readFileSync(path.join(ROOT, "tools/og/pages.json"), "utf8"));
const lockup = `<img alt="" src="data:image/svg+xml;base64,${readFileSync(path.join(ROOT, "dist/assets/brand/eez-lockup.svg")).toString("base64")}">`;
const mark = readFileSync(path.join(ROOT, "dist/assets/brand/eez-mark.svg"), "utf8");
const OUT = path.join(ROOT, "pages/assets/og");
mkdirSync(OUT, { recursive: true });

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const html = (p) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;800&family=Geist+Mono:wght@400&display=block" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0}
body{width:1200px;height:630px;overflow:hidden;background:#0a0a0a;color:#fff;font-family:Geist,sans-serif;position:relative}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:48px 48px}
.glow{position:absolute;inset:0;background:radial-gradient(520px 420px at 82% 48%,rgba(59,229,126,.10),transparent 70%),radial-gradient(420px 360px at 78% 56%,rgba(84,66,205,.16),transparent 70%)}
.in{position:absolute;inset:72px 80px 64px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:18px}
.top img{height:44px;width:auto;display:block}
.top i{width:1px;height:30px;background:#2e2e2e}
.lab{font:400 17px/1 "Geist Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:#3be57e}
.head{margin-top:auto;max-width:${p.mark ? 640 : 1000}px}
h1{font:500 ${p.mark ? 96 : 64}px/1.06 Geist,sans-serif;letter-spacing:-.02em;color:#fff;text-wrap:balance}
h1 span{display:block;color:#8f8f8f}
${p.mark ? "h1{font-weight:300;color:#f2f2ec}h1 span{font-weight:800;color:#fff}" : ""}
p{margin-top:24px;font:400 26px/1.4 Geist,sans-serif;color:#c9cfda;max-width:${p.mark ? 600 : 900}px;text-wrap:pretty}
.foot{margin-top:auto;padding-top:40px;display:flex;justify-content:space-between;align-items:baseline;font:400 18px/1 "Geist Mono",monospace;letter-spacing:.06em}
.foot b{font-weight:400;color:#fff}.foot span{text-transform:uppercase;color:#8f8f8f;letter-spacing:.12em;font-size:15px}
.mark{position:absolute;right:110px;top:150px;height:330px}.mark svg{height:100%;width:auto}
</style></head><body><div class="grid"></div><div class="glow"></div>
${p.mark ? `<div class="mark">${mark}</div>` : ""}
<div class="in">
 <div class="top">${lockup}<i></i><span class="lab">${esc(p.label)}</span></div>
 <div class="head"><h1>${esc(p.h)} <span>${esc(p.lite)}</span></h1><p>${esc(p.sub)}</p></div>
 <div class="foot"><b>eez.io</b><span>${esc(p.foot || "Ethereum Economic Zone")}</span></div>
</div></body></html>`;

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1200, height: 630 });
for (const p of pages) {
  await page.setContent(html(p), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, `${p.id}.png`) });
  console.log("og:", p.id);
}
await browser.close();
