#!/usr/bin/env python3
"""Bring three parts of the demo home (dist/index.html) in line with live eez.io (Framer):

1. Page background: a soft green/purple wash plus eight blurred colour glows.
2. "One call away" diagram: the live animated SVG (plays when 40% is on screen, resets when it
   leaves) replaces the hover-to-play video card.
3. "Where EEZ stands": the live timeline (gradient spine, light sweep, pulsing in-progress dot,
   staggered rise-in once at 20% on screen) replaces the five cards.

Markup, CSS and timings are copied from the live Framer code components (hiwclip, eeztl),
read on 19 Nov 2026. Idempotent: skips if already applied. Run after assemble.py.
"""
import re, sys
from pathlib import Path

INDEX = Path(__file__).resolve().parent.parent / "dist/index.html"
MARK = "/* live-parity */"

# 1. background ---------------------------------------------------------------------------
# glows: (diameter px, left as px from page edge or "R<offset from centre>", top as % of page, colour)
GLOWS = [(821, -168, 0.0, "60,229,126,.13"), (859, "R54", 5.4, "84,66,205,.14"), (836, "R110", 24.0, "60,229,126,.13"),
         (895, -261, 32.5, "84,66,205,.14"), (833, -171, 52.0, "60,229,126,.13"), (877, "R37", 59.5, "98,131,189,.12"),
         (860, "R90", 80.0, "60,229,126,.13"), (831, -237, 87.5, "84,66,205,.14")]
def glow(d, left, top, rgba):
    l = f"calc(50% + {left[1:]}px)" if isinstance(left, str) else f"{left}px"
    return (f'<i style="width:{d}px;height:{d}px;left:{l};top:{top}%;'
            f'background:radial-gradient(circle,rgba({rgba}),transparent 62%)"></i>')
BG_HTML = '<div class="lp-bg" aria-hidden="true">' + "".join(glow(*g) for g in GLOWS) + "</div>"
BG_CSS = """
body{position:relative;z-index:0}
.lp-bg{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;
  background:linear-gradient(rgba(60,229,126,.06),rgba(84,66,205,.07) 28%,rgba(60,229,126,.055) 52%,rgba(84,66,205,.07) 76%,rgba(60,229,126,.06))}
.lp-bg i{position:absolute;border-radius:50%;filter:blur(130px)}
"""

# 2. one-call diagram ---------------------------------------------------------------------
HIW_CSS = """
.hiwclip{position:relative;width:100%;aspect-ratio:880/419;background:transparent}
.hiwclip svg{display:block;width:100%;height:100%;overflow:visible}
.hiwclip .zlbl{fill:#6B6B66;font:12px 'Geist Mono',monospace;letter-spacing:.08em}
.hiwclip .lbl{fill:#6B6B66;font:11px 'Geist Mono',monospace;letter-spacing:.1em}
.hiwclip .box{fill:#0D0D0D;stroke:#2E2E2E;stroke-width:1}
.hiwclip .btxt{fill:#F5F5F0;font:500 15px 'Geist',sans-serif}
.hiwclip .calltrack{stroke:rgba(59,229,126,.28);stroke-width:2;fill:none}
.hiwclip .rettrack{stroke:#6589BC;stroke-opacity:.35;stroke-width:2;fill:none;stroke-dasharray:4 5}
.hiwclip .call{stroke:var(--accent,#3BE57E);stroke-width:3;fill:none;stroke-linecap:round;filter:drop-shadow(0 0 5px var(--accent,#3BE57E));stroke-dasharray:409;stroke-dashoffset:409}
.hiwclip .callhead{fill:var(--accent,#3BE57E);opacity:0}
.hiwclip .ret{stroke:url(#hiw-retgrad);stroke-width:3;fill:none;stroke-linecap:round;stroke-dasharray:7 6}
.hiwclip .retmaskline{stroke:#fff;stroke-width:12;fill:none;stroke-dasharray:349;stroke-dashoffset:349}
.hiwclip .rethead{fill:#6E5BD6;opacity:0}
.hiwclip .badge{opacity:0;transform:scale(.5);transform-box:fill-box;transform-origin:center}
.hiwclip .otxchip{fill:#0A0A0A;stroke:var(--accent,#3BE57E);stroke-opacity:.55;stroke-width:1}
.hiwclip .otx{fill:var(--accent,#3BE57E);font:600 12px 'Geist Mono',monospace;letter-spacing:.12em}
.hiwclip .otxg{opacity:0;transform:translateY(4px);transform-box:fill-box;transform-origin:center}
.hiwclip.hw-play .call{animation:hiw-draw .95s ease-in-out forwards}
.hiwclip.hw-play .callhead{animation:hiw-pop .2s ease .9s forwards}
.hiwclip.hw-play .retmaskline{animation:hiw-draw .9s ease-in-out 1.15s forwards}
.hiwclip.hw-play .rethead{animation:hiw-pop .2s ease 2.0s forwards}
.hiwclip.hw-play .bA{animation:hiw-pop .3s cubic-bezier(.3,1.5,.5,1) 2.1s forwards}
.hiwclip.hw-play .bB{animation:hiw-pop .3s cubic-bezier(.3,1.5,.5,1) 1.0s forwards}
.hiwclip.hw-play .otxg{animation:hiw-rise .5s cubic-bezier(.3,1,.4,1) 2.35s forwards}
@keyframes hiw-draw{to{stroke-dashoffset:0}}
@keyframes hiw-pop{to{opacity:1;transform:scale(1)}}
@keyframes hiw-rise{to{opacity:1;transform:translateY(0)}}
@media (prefers-reduced-motion:reduce){
  .hiwclip .call,.hiwclip .retmaskline{stroke-dashoffset:0!important;animation:none!important}
  .hiwclip .callhead,.hiwclip .rethead,.hiwclip .badge,.hiwclip .otxg{opacity:1!important;transform:none!important;animation:none!important}
}
#how .zone.zv.hiw{margin-top:44px}
"""
HIW_HTML = """<div class="zone zv hiw"><div class="hiwclip" id="hiw" role="img" aria-label="Smart contract A on an L2 calls smart contract B on L1; the return comes back and both settle in one transaction." style="--accent:#3BE57E"><svg viewBox="0 0 880 419" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false"><defs><pattern id="hiw-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0 H0 V40" fill="none" stroke="rgba(255,255,255,.028)" stroke-width="1"></path></pattern><linearGradient id="hiw-retgrad" x1="500" y1="315" x2="300" y2="157" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#3BE57E"></stop><stop offset=".55" stop-color="#6589BC"></stop><stop offset="1" stop-color="#6E5BD6"></stop></linearGradient><mask id="hiw-retmask"><path class="retmaskline" d="M500,315 H300 V166"></path></mask></defs><rect x="24" y="40" width="832" height="150" rx="12" fill="url(#hiw-grid)" stroke="#242424" stroke-width="1"></rect><rect x="24" y="230" width="832" height="150" rx="12" fill="url(#hiw-grid)" stroke="#242424" stroke-width="1"></rect><text class="zlbl" x="42" y="66">L2</text><text class="zlbl" x="42" y="256">L1</text><path class="calltrack" d="M380,124 H640 V273"></path><text class="lbl" x="512" y="112">CALL</text><path class="call" d="M380,124 H640 V273"></path><path class="callhead" d="M640,284 l-6,-11 l12,0 z"></path><path class="rettrack" d="M500,315 H300 V166"></path><text class="lbl" x="352" y="300">RETURN</text><path class="ret" d="M500,315 H300 V166" mask="url(#hiw-retmask)"></path><path class="rethead" d="M300,155 l-6,11 l12,0 z"></path><rect class="box" x="170" y="95" width="210" height="58" rx="11"></rect><text class="btxt" x="194" y="129">Smart Contract A</text><rect class="box" x="500" y="286" width="210" height="58" rx="11"></rect><text class="btxt" x="524" y="320">Smart Contract B</text><g class="badge bA"><circle cx="356" cy="111" r="9" fill="#3BE57E"></circle><path d="M352,111 l3,3 l6,-6" stroke="#0A0A0A" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></g><g class="badge bB"><circle cx="686" cy="302" r="9" fill="#3BE57E"></circle><path d="M682,302 l3,3 l6,-6" stroke="#0A0A0A" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></g><g class="otxg"><rect class="otxchip" x="344" y="196" width="192" height="28" rx="14"></rect><text class="otx" x="440" y="214" text-anchor="middle">[ ONE TRANSACTION ]</text></g></svg></div></div>
  """

# 3. progress timeline --------------------------------------------------------------------
TL_CSS = """
#progress{text-align:center}
#progress > h2{margin-inline:auto}
#progress > h2 span{color:var(--white)}
.eeztl{--green:#3BE57E;--muted:#8F8F8F;--dim:#5E5E5A;--edge:#2E2E2E;position:relative;width:100%;font-family:"Geist",sans-serif;padding:0 0 80px;text-align:left}
.eeztl .tl{position:relative;margin-top:56px}
.eeztl .spine,.eeztl .sweep{opacity:0;transition:opacity .8s ease}
.eeztl.in .spine,.eeztl.in .sweep{opacity:1}
.eeztl .node{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .7s cubic-bezier(.25,1,.3,1)}
.eeztl.in .node{opacity:1;transform:none}
.eeztl.in .node:nth-child(2){transition-delay:.08s}
.eeztl.in .node:nth-child(3){transition-delay:.16s}
.eeztl.in .node:nth-child(4){transition-delay:.24s}
.eeztl.in .node:nth-child(5){transition-delay:.32s}
@media (prefers-reduced-motion:reduce){.eeztl .spine,.eeztl .sweep,.eeztl .node{opacity:1!important;transform:none!important;transition:none!important}}
.eeztl .spine{position:absolute;left:12px;right:10px;top:27px;height:2px;
  background:linear-gradient(90deg,var(--green) 0%,#6283bd 36%,rgba(68,57,203,.22) 52%,rgba(68,57,203,.1) 100%)}
.eeztl .spine::after{content:"";position:absolute;left:36%;right:0;top:0;height:2px;
  background-image:linear-gradient(90deg,var(--dim) 0 6px,transparent 6px 12px);background-size:12px 2px}
.eeztl .sweep{position:absolute;top:26px;left:12px;width:34%;height:4px;overflow:hidden;border-radius:2px;pointer-events:none}
.eeztl .sweep i{position:absolute;top:0;left:-30%;width:30%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.7),transparent);filter:blur(1px);animation:eeztl-sweep 3.4s cubic-bezier(.5,0,.5,1) infinite}
@keyframes eeztl-sweep{0%{left:-30%}62%,100%{left:120%}}
.eeztl .row{display:grid;grid-template-columns:repeat(5,1fr);gap:44px;position:relative}
.eeztl .node{position:relative;padding-top:84px}
.eeztl .dot{position:absolute;top:17px;left:0;width:24px;height:24px;border-radius:50%;background:#0A0A0A;border:2px solid var(--dim);display:grid;place-items:center}
.eeztl .dot.done{border-color:var(--green);background:var(--green)}
.eeztl .dot.done svg{width:12px;height:12px}
.eeztl .dot.live{border-color:var(--green);background:var(--green)}
.eeztl .dot.live::after{content:"";width:7px;height:7px;border-radius:50%;background:#06210f}
.eeztl .dot.live::before{content:"";position:absolute;inset:-5px;border-radius:50%;border:2px solid var(--green);opacity:.5;animation:eeztl-ring 2.2s ease-out infinite}
.eeztl .dot.plan{border-color:#3a3a3a}
.eeztl .dot.horizon{border-color:#333}
@keyframes eeztl-ring{0%{transform:scale(.7);opacity:.6}100%{transform:scale(1.9);opacity:0}}
.eeztl .pill{display:inline-block;font:500 11.5px/1 "Geist Mono",monospace;letter-spacing:.1em;text-transform:uppercase;padding:6px 12px;border-radius:100px;border:1px solid var(--edge);color:#9aa3b3}
.eeztl .pill.live{display:inline-flex;align-items:center;gap:6px;color:var(--green);border-color:rgba(59,229,126,.5)}
.eeztl .pill.live .sdot{width:6px;height:6px;border-radius:50%;background:var(--green)}
.eeztl .livebtn{display:inline-flex;align-items:center;gap:7px;padding:6px 13px 6px 10px;border-radius:100px;background:var(--green);color:#06210f;font:600 11.5px/1 "Geist Mono",monospace;letter-spacing:.1em;text-transform:uppercase}
.eeztl .livedot{position:relative;width:6px;height:6px;border-radius:50%;background:#06210f}
.eeztl .livedot::after{content:"";position:absolute;inset:-2px;border-radius:50%;border:1.5px solid #06210f;opacity:.6;animation:eeztl-ring 1.6s ease-out infinite}
.eeztl h3{margin:22px 0 0;font:600 21px/1.3 "Geist",sans-serif;letter-spacing:-.01em;color:#fff}
.eeztl .node.now h3{color:#fff}
.eeztl .node.fut h3{color:#cfcfcf}
.eeztl .node.horizon h3{color:#9a9a9a}
.eeztl p{margin:11px 0 0;font:400 15px/1.6 "Geist",sans-serif;color:var(--muted);max-width:19em}
.eeztl .node.horizon p{color:#6a6a6a}
@media (prefers-reduced-motion:reduce){.eeztl .sweep i,.eeztl .dot.live::before,.eeztl .livedot::after{animation:none}}
@media (max-width:809px){
  .eeztl .spine{left:9px;right:auto;top:10px;bottom:10px;width:2px;height:auto;
    background:linear-gradient(180deg,var(--green) 0%,#6283bd 30%,rgba(68,57,203,.18) 48%,rgba(68,57,203,.08) 100%)}
  .eeztl .spine::after{left:0;right:auto;top:30%;bottom:0;width:2px;height:auto;
    background-image:linear-gradient(180deg,var(--dim) 0 6px,transparent 6px 12px);background-size:2px 12px}
  .eeztl .sweep{display:none}
  .eeztl .row{grid-template-columns:1fr;gap:26px}
  .eeztl .node{padding:0 0 0 38px}
  .eeztl .dot{top:1px;left:0}
}
"""
CHECK = '<svg viewBox="0 0 12 12" fill="none"><path d="M2 6.5l2.5 2.5L10 3" stroke="#0A0A0A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
STEPS = [("live", "Live", "Ethereum Testnet", "Zones call Ethereum and each other, live on the devnet."),
         ("prog", "In progress", "Security audit", "Independent review of the core protocol."),
         ("plan", "Planned", "ZK proofs and real-time proving", "Zones are proven with ZK proofs, generated in real time."),
         ("plan", "Planned", "First general-purpose EEZ instance", "Gnosis Chain launches as the first EEZ instance."),
         ("horizon", "Horizon", "Many chains on Ethereum", "Many chains composing with Ethereum.")]
def node(st, label, title, body):
    cls = "node" + (" fut" if st in ("plan", "horizon") else "") + (" horizon" if st == "horizon" else "") + (" now" if st == "prog" else "")
    dot = {"live": "dot done", "prog": "dot live", "horizon": "dot horizon"}.get(st, "dot plan")
    tag = (f'<span class="livebtn"><span class="livedot"></span>{label}</span>' if st == "prog" else
           f'<span class="pill live"><span class="sdot"></span>{label}</span>' if st == "live" else f'<span class="pill">{label}</span>')
    return f'<div class="{cls}"><div class="{dot}">{CHECK if st == "live" else ""}</div>{tag}<h3>{title}</h3><p>{body}</p></div>'
TL_HTML = ('<div class="eeztl" id="eeztl"><div class="tl"><div class="spine"></div><div class="sweep"><i></i></div><div class="row">'
           + "".join(node(*s) for s in STEPS) + "</div></div></div>")
PROGRESS = f"""<section class="sec" id="progress">
  <p class="eb">[ Progress ]</p>
  <h2><span>Where</span> EEZ stands.</h2>
  {TL_HTML}
</section>"""

JS = """<script>
(() => {
  // live eez.io parity: the one-call diagram plays at 40% on screen and resets when it leaves;
  // the progress timeline rises in once at 20%
  const hiw = document.getElementById("hiw"), tl = document.getElementById("eeztl");
  if (!("IntersectionObserver" in window)) { hiw && hiw.classList.add("hw-play"); tl && tl.classList.add("in"); return; }
  if (hiw) new IntersectionObserver(es => es.forEach(e => hiw.classList.toggle("hw-play", e.isIntersecting)), { threshold: 0.4 }).observe(hiw);
  if (tl) { const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { tl.classList.add("in"); io.disconnect(); } }), { threshold: 0.2 }); io.observe(tl); }
})();
</script>"""

# The home already styles .call, .lbl, .badge, .box etc. for other parts, so the diagram's
# classes get an hw- prefix; html,body{height:100%} would cut the background at one screen.
HW = ["calltrack", "rettrack", "callhead", "retmaskline", "rethead", "otxchip", "otxg", "zlbl", "btxt",
      "badge", "call", "ret", "box", "lbl", "otx", "bA", "bB"]
def hw(text, in_html):
    for c in HW:
        if in_html:
            text = re.sub(r'(class="(?:[^"]* )?)' + c + r'(?=[ "])', r"\1hw-" + c, text)
            text = re.sub(r'(class="(?:[^"]* )?)' + c + r'(?=[ "])', r"\1hw-" + c, text)
        else:
            text = re.sub(r"\." + c + r"\b(?!-)", ".hw-" + c, text)
    return text
HIW_HTML = hw(HIW_HTML, True)
HIW_CSS = hw(HIW_CSS, False) + "\n#how .hiwclip svg{height:100%!important}\n"
BG_CSS += "\nhtml{height:auto;min-height:100%}body{height:auto;min-height:100%}\n"

# 4. the rest of the home, checked against published eez.io on 19 Nov 2026 -------------------
# Headings: one light weight, no bold first word. Build, Alliance and News headers centred.
# Alliance: vertical side labels (green / blue) instead of sub-headings; "Join the Alliance" is a
# pill under the heading. Talks: ↗ on titles. Latest: the three posts live shows.
REST_CSS = """
.hero h1 b,.sec > h2 b,#how .build > h2 b{font-weight:inherit;color:inherit}
#build > .eb,#build > h2,#alliance > .eb,#alliance > h2,#news > .eb,#news > h2{text-align:center;margin-inline:auto}
.mq .logo b{font:500 16px/1 var(--sans)}
.tile span,.tile span{font:500 16px/1 var(--sans);white-space:nowrap}
#alliance .join-row{display:flex;justify-content:center;margin-top:32px}
#alliance .tier{position:relative;margin-top:40px}
#alliance .tier .emap{margin-top:0}
#alliance .tierlbl{position:absolute;left:-41px;top:0;margin:0;transform:rotate(-90deg) translateX(-100%);transform-origin:0 0;white-space:nowrap;
  font:400 12.5px/16px var(--mono);letter-spacing:.1em;text-transform:uppercase}
#alliance .tierlbl.adopt{color:#3BE57E}#alliance .tierlbl.infra{color:#6E9BEE}
@media (max-width:1240px){#alliance .tierlbl{position:static;transform:none;margin:0 0 12px}}
.vid small{font-size:12px}
.th em{font-size:16px}
.posts{margin-top:24px;gap:24px}
.post{background:none;border:0;border-radius:0;padding:0;gap:0}
.post .pth{display:block;border:1px solid #1e1e1e;border-radius:14px;background:#111;overflow:hidden;aspect-ratio:363/227}
.post .pth img{width:100%;height:100%;aspect-ratio:auto;object-fit:cover;border-radius:0;transition:transform .5s ease}
.post:hover .pth img{transform:scale(1.03)}
.post small{margin-top:14px;font:400 12px/1.6 var(--mono);letter-spacing:.06em;color:#7a7a76}
.post b{margin-top:8px;font:500 15px/1.4 var(--sans);color:#f2f2ec}
"""
POSTS = [("post-oct-live.png", "6eL5F7RsHGKLg7lWz1fxn1YvgZU.png", "Update · Nov 9, 2026", "Monthly update — October &amp; Devcon Mumbai",
          "https://eez.io/blog/monthly-update---october-devcon-mumbai"),
         ("post-sep-live.png", "sXYqT2lUyIdJci0sPiOxxuFRYA.png", "Update · Oct 1, 2026", "Monthly update — September 2026",
          "https://eez.io/blog/monthly-update---september"),
         ("post-intro-live.png", "ElQPWQGOvp2LnMhhjsE3N9OYk6A.png", "About · Mar 29, 2026", "Introducing the Ethereum Economic Zone (EEZ)",
          "https://eez.io/blog/introducing-the-eez")]
POSTS_HTML = '<div class="posts">' + "".join(
    f'<a class="post" href="{u}" target="_blank" rel="noopener"><span class="pth"><img src="assets/media/{f}" alt="" loading="lazy"></span>'
    f'<small>{m}</small><b>{t}</b></a>' for f, _, m, t, u in POSTS) + "</div>"
DEVCON = (INDEX.parent.parent / "shared/devcon.html").read_text().strip()

def rest(s):
    def sub(pat, new, count=1, flags=0):
        nonlocal s
        s, n = re.subn(pat, new, s, count=count, flags=flags)
        if n == 0: sys.exit(f"pattern not found: {pat[:60]}")
    # Devcon bar: same as every other page (shared/devcon.html)
    sub(r'<div class="devcon">[\s\S]*?</div>', lambda m: DEVCON)
    # Try on the testnet opens a new tab, like every other external link
    sub(r'<a class="pill" href="https://eez.dev/">', '<a class="pill" href="https://eez.dev/" target="_blank" rel="noopener">')
    # Alliance: pill under the heading, vertical labels, no join row / sub-headings
    sub(r'<div class="row"><div class="grp join"[\s\S]*?</a></div></div>', '')
    sub(r'(<h2><b>The teams</b> building on the commons\.</h2>)',
        r'\1\n  <div class="join-row"><a class="pill" href="/get-in-touch?intent=alliance"><span>Join the Alliance</span><i aria-hidden="true">→</i></a></div>')
    sub(r'<div class="tierhd"><h3>Adoption partners</h3><p>[^<]*</p></div>', '<p class="tierlbl adopt">Adoption partners</p>')
    sub(r'<div class="tierhd"><h3>Infrastructure partners</h3><p>[^<]*</p></div>', '<p class="tierlbl infra">Infrastructure partners</p>')
    # Talks: ↗ on titles and on All talks
    s = re.sub(r'(<a class="vid"[^>]*>[\s\S]*?<b>)([^<]*)(</b>)', lambda m: m[1] + m[2] + "&nbsp;↗" + m[3], s)
    sub(r'All talks →', 'All talks ↗')
    # Latest: the three posts on live eez.io
    sub(r'<div class="posts">[\s\S]*?</div>', lambda m: POSTS_HTML)
    return s

def copy_media():
    import shutil
    src, dst = INDEX.parent.parent / "tools/live-media", INDEX.parent / "assets/media"
    for f, orig, *_ in POSTS:
        shutil.copyfile(src / orig, dst / f)

def main():
    s = INDEX.read_text()
    if MARK in s:
        print("live parity already applied"); return
    a = s.index('<div class="zone zv">'); b = s.index('<div class="build" id="use-cases">')
    s = s[:a] + HIW_HTML + s[b:]
    s, n = re.subn(r'<section class="sec" id="progress">[\s\S]*?</section>', PROGRESS, s, count=1)
    if n != 1: sys.exit("progress section not found")
    s = rest(s)
    copy_media()
    s = s.replace("</head>", f"<style>{MARK}{BG_CSS}{HIW_CSS}{TL_CSS}{REST_CSS}</style>\n</head>", 1)
    s = s.replace("<body>", "<body>\n" + BG_HTML, 1)
    s = s.replace("</body>", JS + "\n</body>", 1)
    INDEX.write_text(s)
    print("live parity applied to", INDEX)

if __name__ == "__main__":
    main()
