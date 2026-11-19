// Tiny static server for dist/ with clean URLs (/status -> status.html), like Vercel cleanUrls.
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { join, extname, normalize } from "node:path";

const root = new URL("./dist/", import.meta.url).pathname;
const port = Number(process.env.PORT || 8895);
const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".woff2": "font/woff2", ".woff": "font/woff", ".ico": "image/x-icon", ".mp4": "video/mp4", ".webm": "video/webm" };

async function resolve(p) {
  for (const c of [p, p + ".html", join(p, "index.html")]) {
    try { if ((await stat(c)).isFile()) return c; } catch {}
  }
  return null;
}

createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  let path = decodeURIComponent(url.pathname);
  if (path.endsWith(".html")) { res.writeHead(308, { Location: path.slice(0, -5) + url.search }); return res.end(); }
  const file = await resolve(normalize(join(root, path)));
  if (!file || !file.startsWith(root)) { res.writeHead(404, { "content-type": "text/plain" }); return res.end("404 " + path); }
  res.writeHead(200, { "content-type": types[extname(file)] || "application/octet-stream", "cache-control": "no-store" });
  res.end(await readFile(file));
}).listen(port, () => console.log(`eez merge demo on http://localhost:${port}`));
