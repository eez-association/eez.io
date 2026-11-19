# Parity with live eez.io

The demo Home page (`/`) compared with published **eez.io**, which is the Framer project *EEZ Website*. Checked on 19 Nov 2026 at 1440 px wide: every text block (font, size, weight, colour, alignment), every link and target, images, animations and their triggers. The Framer project itself could not be opened (its connection wasn't loaded in the session), so anything changed in Framer but not yet published isn't covered.

Everything below is applied by `tools/live_parity.py` (Home) and `shared/` (Devcon bar and footer, all pages). `assemble.py` runs the parity step after each rebuild.

## Matched to live

| Area | Was in the demo | Now (as live) |
|---|---|---|
| Page background | Flat `#0A0A0A` | Green/purple wash down the page + 8 blurred colour glows (blur 130 px) |
| Headings (hero, all sections) | First word bold (800, white): "Activate **Ethereum**", "**What** you can build" | One light weight (300), no bold word |
| Build, Alliance, News headers | Left-aligned | Centred |
| Where EEZ stands | Five cards, left-aligned heading | Timeline (live `eeztl` component): gradient spine, light sweep every 3.4 s, pulsing ring on "In progress", columns rise in 80 ms apart once at 20% on screen; vertical on phones |
| Last progress step | "Many zones on Ethereum / Many zones composing…" | "Many chains on Ethereum / Many chains composing with Ethereum." |
| Text-only logos (beaverbuild, Colibri) | Suisse Intl 20 px (fallback font) / 12 px | Geist 500 16 px |
| Try on the testnet | Same tab | New tab |
| Footer (all pages) | Labels `#8f8f8f`, links 12 px, tagline 14 px | Labels `#9aa3b3`, links 13 px, tagline 13.5 px `#7a7a76`, © `#5e5e5a` |
| Footer → Brand and logo | `#` (dead) | eez.io/brand |

## Intentional differences (the proposal, copy and thumbnails from eez-merge-demo.vercel.app)

| Area | Live eez.io | Demo |
|---|---|---|
| Top menu | How it works · Use cases · Build · Alliance · Progress · News | Use cases ▾ · Developers ▾ · Get in touch → |
| Hero buttons | Build with us · Try on the testnet | Use cases → (/use-cases/all) · Start building (build.eez.io) |
| What you can build | Embedded carousel (same five cards and copy) | Same cards, plus "All use cases →" |
| Start where you are | 3 cards: Chain operators (Tally form), App builders (build.eez.io), Infrastructure operators (specs-draft) | 4 cards: Institutions, Chains, Apps, Infra → `/use-cases/*` |
| Join the Alliance | tally.so/r/NpLo4l | `/get-in-touch?intent=alliance` |
| Footer columns | Build · Alliance · News (Blog, Monthly updates, Press → /media, Brand and logo, Talks) · Follow | Use cases · Developers · News (News, Press and talks, Brand and logo) · Follow |
| One-call diagram | Animated SVG, plays at 40% on screen | Same SVG and colours, plays on hover / tap, "Hover to play" |
| Alliance | Vertical side labels, Join pill under heading | Same green / blue labels and box borders, placed above each grid with a line of text; Join under the first grid |
| Talk cards | Titles end in ↗; "All talks ↗" | No ↗ on titles; "All talks →" |
| Latest | October, September, Intro; live covers | September (Oct 1), August (Aug 20), Intro; landscape EEZ thumbnails |
| Devcon bar (all pages) | `↗` after each talk | `→` |

## Colours and styling

Matched to live by computed style (20 Nov 2026): heading highlight white, hero lede, header (transparent until scroll), Devcon bar, Build cards, Alliance borders and logos, play buttons, Latest cards, footer. Only the logo lockup size still differs.

## Still different (decide)

- **Build card size:** live titles are 26 px over 3 columns; the demo's 4 columns use 20 px.
- **Press and talks** goes to `/#news`; live splits it into Press (eez.io/media) and Talks (`/#news`).
- **Carousel caption:** live shows "Trade from your L2…" and "Click the card to open it" above the cards; the demo shows them below.
