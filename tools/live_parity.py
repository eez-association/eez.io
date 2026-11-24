#!/usr/bin/env python3
"""Bring three parts of the demo home (dist/index.html) in line with live eez.io (Framer):

1. Page background: a soft green/purple wash plus eight blurred colour glows.
2. "One call away" diagram: the live animated SVG (same colours as eez.io). Like live, it plays
   once when it scrolls into view; a mouse hover replays it. No card lift or shadow.
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
# No filter:blur: a 130px blur on eight 850px shapes made the home page re-rasterise huge areas on every
# repaint and stall slower machines (2026-11-20). The soft falloff is drawn into the gradient instead:
# the shape grows by PAD on each side and fades through extra stops, which looks the same.
PAD = 240
def glow(d, left, top, rgba):
    l = f"calc(50% + {left[1:]}px)" if isinstance(left, str) else f"{left}px"
    rgb, a = rgba.rsplit(",", 1); a = float(a)
    c = lambda k: f"rgba({rgb},{a * k:.3f})"
    return (f'<i style="width:{d + 2 * PAD}px;height:{d + 2 * PAD}px;left:calc({l} - {PAD}px);top:calc({top}% - {PAD}px);'
            f'background:radial-gradient(circle closest-side,{c(.58)},{c(.48)} 30%,{c(.27)} 55%,{c(.09)} 78%,transparent)"></i>')
BG_HTML = '<div class="lp-bg" aria-hidden="true">' + "".join(glow(*g) for g in GLOWS) + "</div>"
BG_CSS = """
body{position:relative;z-index:0}
.lp-bg{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;
  background:linear-gradient(rgba(60,229,126,.06),rgba(84,66,205,.07) 28%,rgba(60,229,126,.055) 52%,rgba(84,66,205,.07) 76%,rgba(60,229,126,.06))}
.lp-bg i{position:absolute;border-radius:50%}
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
@keyframes eeztl-sweep{0%{transform:translateX(0)}62%,100%{transform:translateX(500%)}}
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
         ("plan", "Planned", "ZK proofs and real\u2011time proving", "Zones are proven with ZK proofs, generated in real time."),
         ("plan", "Planned", "First general\u2011purpose EEZ instance", "Gnosis Chain launches as the first EEZ instance."),
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
  // the one-call diagram plays once when 40% of it is on screen (works on touch, no hover needed);
  // a mouse hover replays it after that. Reduced motion shows the finished frame (CSS).
  // The progress timeline rises in once at 20%.
  const hiw = document.getElementById("hiw"), tl = document.getElementById("eeztl");
  const play = () => { hiw.classList.remove("hw-play"); void hiw.offsetWidth; hiw.classList.add("hw-play"); };
  if (!("IntersectionObserver" in window)) { hiw && hiw.classList.add("hw-play"); tl && tl.classList.add("in"); return; }
  if (hiw && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let played = false, busy = false;
    hiw.addEventListener("animationend", e => { if (e.animationName === "hiw-rise") busy = false; });
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { played = busy = true; play(); io.disconnect(); }
    }), { threshold: 0.4 });
    io.observe(hiw);
    hiw.addEventListener("pointerenter", e => { if (e.pointerType === "mouse" && played && !busy) { busy = true; play(); } });
  }
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
# Copy, Alliance sub-headings and talk titles follow the demo (eez-merge-demo.vercel.app), 20 Nov 2026.
# Latest shows eez.io's three posts and covers (October, September, Intro).
REST_CSS = """
.hero h1 b,.sec > h2 b,#how .build > h2 b{font-weight:inherit;color:#fff}
#build > .eb,#build > h2,#alliance > .eb,#alliance > h2,#news > .eb,#news > h2{text-align:center;margin-inline:auto}
.mq .logo b{font:500 16px/1 var(--sans)}
.tile span,.tile span{font:500 16px/1 var(--sans);white-space:nowrap}
.vid small{font-size:12px;letter-spacing:.06em}
/* colour and design parity with live eez.io (computed styles, 20 Nov 2026) */
/* one token system: the home page's own names point at shared/tokens.css */
:root:root{--page:var(--eez-page);--card:var(--eez-surface);--panel:var(--eez-surface);--edge:var(--eez-line);--ln:var(--eez-line);--ln2:var(--eez-line-soft);
  --ink:var(--eez-ink-soft);--ink-dim:var(--eez-muted);--muted:var(--eez-muted);--ebc:var(--eez-label);--sub:var(--eez-heading);--ledec:var(--eez-body);--white:var(--eez-ink);--green:var(--eez-green)}
.hero .lede{max-width:520px;color:var(--eez-body)}
.pill span{font-size:11.5px;font-weight:500;letter-spacing:.02em}
.mq .logo b,.tile span{letter-spacing:-.02em}
.aud{background:linear-gradient(rgba(255,255,255,.016),rgba(0,0,0,0));border-color:var(--eez-line-soft);border-radius:var(--eez-radius-card)}
.aud .iso{height:96px;align-self:center;margin:8px 0 12px}
.aud h3{color:#fff;letter-spacing:-.01em}
.tierhd h3{font:400 12.5px/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase}
.tierhd.adopt h3{color:#3BE57E}.tierhd.infra h3{color:#6E9BEE}
.grp{background:none;border-color:rgba(255,255,255,.08)}
.tierhd.adopt + .emap .grp{border-color:rgba(59,229,126,.32)}
.tierhd.infra + .emap .grp{border-color:rgba(98,131,189,.4)}
.grp .eb{color:#9aa3b3}
.tile{background:none;border-color:transparent}
.tile:hover{border-color:rgba(255,255,255,.08)}
.play{background:rgba(0,0,0,.42);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.play::after{border-left-color:#fff}
.th em{letter-spacing:-.02em}
.posts{margin-top:24px;gap:24px}
.post{background:none;border:0;border-radius:0;padding:0;gap:0}
.post img{border:1px solid #1e1e1e;border-radius:14px;background:#111;aspect-ratio:363/227;transition:transform .5s ease}
.post small{margin-top:16px;font:400 12px/1.6 var(--mono);letter-spacing:.06em;color:#7a7a76}
.post b{margin-top:8px;font:500 15px/1.4 var(--sans);color:#f2f2ec}
.zone.zv .vcard{cursor:pointer}
.ringcap span{text-transform:uppercase}
.eeztl .node.horizon p{color:#8a8a85}
a.more{display:inline-flex;align-items:center;min-height:24px}
.skip{position:absolute;left:16px;top:-80px;z-index:300;padding:10px 14px;border-radius:8px;background:#fff;color:#0a0a0a;font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
.skip:focus{top:12px}
.aud .pill{max-width:100%}.aud .pill span{white-space:normal;text-align:left;line-height:1.35}.aud .pill i{flex:none}
.aud p{font-size:15.5px}
.zone.zv .cap .hv,.zone.zv .cap .tp{font:400 12px/1.6 var(--mono);letter-spacing:.06em;color:#7a7a76}
.th em{font-size:16px}
/* review 20 Nov 2026 ------------------------------------------------------------------- */
/* one-call diagram: plays on scroll; the hover card (lift, tilt, shadow, crosshair) is gone */
#how .zone.zv .vcard,#how .zone.zv .vcard.on{transform:none;box-shadow:none;cursor:default;transition:none}
/* Build cards: live's spacing and hover (padding 44/36/40 scaled to four columns, 28 px gaps,
   6 px lift with a green border, the icon rising with it) */
#build .auds{gap:20px}
@media (min-width:1200px){#build .aud .pill span{white-space:nowrap}}
#build .aud{padding:40px 26px 32px;gap:16px;transition:transform .5s cubic-bezier(.25,1,.3,1),border-color .25s}
#build .aud .iso{height:104px;margin:4px 0 20px;transition:transform .5s cubic-bezier(.25,1,.3,1)}
#build .aud:hover,#build .aud:focus-within{transform:translateY(-6px);border-color:rgba(59,229,126,.55)}
#build .aud:hover .iso,#build .aud:focus-within .iso{transform:translateY(-5px)}
@media (prefers-reduced-motion:reduce){#build .aud,#build .aud .iso{transition:none}#build .aud:hover,#build .aud:hover .iso,#build .aud:focus-within,#build .aud:focus-within .iso{transform:none}}
@media (max-width:600px){#build .aud{padding:32px 24px 28px}}
/* Alliance: live's layout. Join under the heading; each tier's label runs vertically in the
   left gutter beside its logos; one line of labels above the logos where there is no gutter. */
#alliance > .pill{display:flex;width:fit-content;margin:28px auto 0}
#alliance .tier{position:relative;margin-top:48px}
#alliance .tier + .tier{margin-top:40px}
#alliance .tier .emap{margin-top:14px}
#alliance .grp{padding:18px 16px 20px;gap:16px}
#alliance .tile{padding:0 6px}
@media (min-width:1240px){
  #alliance .tierhd{position:absolute;top:0;bottom:0;right:calc(100% + 22px);display:flex;align-items:center}
  #alliance .tierhd h3{writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap}
  #alliance .tier .emap{margin-top:0}
}
"""
# Alliance logos at equal visual weight: each logo's width comes from its trimmed box and ink
# density (sqrt of area, half a density correction), measured from the PNGs on 20 Nov 2026, then
# scaled so the widest fits a 96 px tile interior.
LOGO_W = {"aave": 81, "spark": 75, "cowswap": 91, "kyber": 96, "centrifuge": 72, "xstocks": 70, "monerium": 79,
          "bermuda-bay": 86, "ssv": 92, "linea": 69, "gnosis-chain": 87, "hydration": 86, "arkiv": 74, "consensys": 82, "octant": 68,
          "fileverse": 96, "gnosis": 63, "zisk": 52, "ethereum-foundation": 70, "nethermind": 96, "erigon": 85, "besu": 62,
          "flashbots": 86, "titan": 58, "eureka": 75, "blockscout": 88, "remix": 73, "safe": 66, "cometh": 63}
POSTS = [("post-oct-live.jpg", "6eL5F7RsHGKLg7lWz1fxn1YvgZU.png", "Update · Nov 9, 2026", "Monthly update · October and Devcon Mumbai",
          "/blog/monthly-update---october-devcon-mumbai"),
         ("post-sep-live.jpg", "sXYqT2lUyIdJci0sPiOxxuFRYA.png", "Update · Oct 1, 2026", "Monthly update · September 2026",
          "/blog/monthly-update---september"),
         ("post-intro-live.jpg", "ElQPWQGOvp2LnMhhjsE3N9OYk6A.png", "About · Mar 29, 2026", "Introducing the Ethereum Economic Zone (EEZ)",
          "/blog/introducing-the-eez")]
POSTS_HTML = '<div class="posts">' + "".join(
    f'<a class="post" href="{u}"><img src="assets/media/{f}" alt="" loading="lazy">'
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
    # Alliance sub-headings: green / blue labels like live; Join as the live pill
    sub(r'<div class="tierhd"><h3>Adoption partners', '<div class="tierhd adopt"><h3>Adoption partners')
    sub(r'<div class="tierhd"><h3>Infrastructure partners', '<div class="tierhd infra"><h3>Infrastructure partners')
    # Alliance layout like live (review 20 Nov 2026): Join sits under the heading, the tier
    # labels lose their line of text (they run vertically beside the logos)
    sub(r'\s*<div class="row"><div class="grp join"[^>]*><a class="mbtn" href="/get-in-touch\?intent=alliance">[\s\S]*?</a></div></div>', '')
    sub(r'(<section class="sec" id="alliance">[\s\S]*?</h2>)',
        r'\1\n  <a class="pill" href="/get-in-touch?intent=alliance"><span>Join the Alliance</span><i aria-hidden="true">→</i></a>')
    sub(r'(<div class="tierhd (?:adopt|infra)"><h3>[^<]*</h3>)<p>[^<]*</p>', r'\1', count=2)
    for name, w in LOGO_W.items():
        sub(r'(src="assets/logos/' + re.escape(name) + r'\.png\?v=\d+"[^>]*style="--w:)\d+px', rf'\g<1>{w}px')
    # Use-case carousel: the click fixes live eez.io already has (its srcdoc, read 21 Nov 2026).
    # 1. A newly centred card lights up after 100 ms, not 450: the slot no longer drops to dark
    #    between the old card leaving and the new one playing (the "blink" on select).
    sub(r'(play\(cur\); \}, )450\)', r'\g<1>100)')
    # 2. A pointerup within 400 ms of opening can't close the panel it just opened.
    sub(r'let cur = 0, pos = 0, open = false;', 'let cur = 0, pos = 0, open = false, openedAt = 0;')
    sub(r'if \(open\) return; open = true; ring\.classList\.add\("tall"\);',
        'if (open) return; open = true; openedAt = performance.now(); ring.classList.add("tall");')
    sub(r'if \(e\.target === detail\) closeCard\(\);', 'if (e.target === detail && performance.now() - openedAt > 400) closeCard();')
    # 3. Tap-to-play first only on touch screens; a touch laptop or pen opens like a mouse click.
    sub(r'if \(e\.pointerType !== "mouse" && tapped !== cur\)', 'if (touchUI && e.pointerType !== "mouse" && tapped !== cur)')
    # Latest: the three posts eez.io shows (October, September, Intro) with eez.io's covers
    sub(r'<div class="posts">[\s\S]*?</div>', lambda m: POSTS_HTML)
    return s

def copy_media():
    # eez.io's covers, pre-flattened onto the card colour (#111) and trimmed of their soft edge, so no
    # transparent pixels turn white: tools/live-media/<id>.jpg, 726 px wide (2x the ~363 px card)
    import shutil
    src, dst = INDEX.parent.parent / "tools/live-media", INDEX.parent / "assets/media"
    for f, orig, *_ in POSTS:
        shutil.copyfile(src / orig.replace(".png", ".jpg"), dst / f)

def main():
    s = INDEX.read_text()
    if MARK in s:
        print("live parity already applied"); return
    clip = HIW_HTML[HIW_HTML.index('<div class="hiwclip'):HIW_HTML.rindex('</div>')]
    s, n = re.subn(r'(<div class="zone zv">)<p class="eb g">\[ One transaction \]</p>(<div class="vcard" tabindex="0">)<video[\s\S]*?</video>',
                   lambda m: m[1] + m[2] + clip, s, count=1)
    if n != 1: sys.exit("one-call video card not found")
    # auto-play replaces hover-to-play: no caption, no focusable card
    s, n = re.subn(r'(<div class="zone zv">)<div class="vcard" tabindex="0">([\s\S]*?</div></div>)<p class="cap">[\s\S]*?</p>',
                   r'\1<div class="vcard">\2', s, count=1)
    if n != 1: sys.exit("one-call caption not found")
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
