# eez-merge-demo — inventory

Source: `dist/` (identical to https://eez-merge-demo.vercel.app, checked 19 Nov 2026). 9 pages: `/`, `/use-cases/institutions|chains|apps|infra|all|kit|scoping`, `/get-in-touch`.
↗ = opens a new tab. Relative paths are on eez.io.

## Issues found

| # | Where | Issue |
|---|---|---|
| 1 | Footer → Brand and logo (all pages) | Dead link: `#` |
| 2 | Home → Latest → September card | Shows a `[Date]` placeholder and links to `/blog`, not the post |
| 3 | Home → "Try on the testnet" | Opens in the same tab; every other external link opens a new tab |
| 4 | Get in touch → Send to the team | Demo only: validates, then shows "nothing was sent" |
| 5 | `use-cases/orbit.js`, `doors.js` | Shipped but not loaded by any page |
| 6 | Institutions page | Hidden empty link ("The one-ledger version:"), no href |

---

## 1. Links

### Shared header (every page)
| Element | Label | Goes to |
|---|---|---|
| Devcon bar | [ One Ethereum ] | youtube.com/watch?v=uvY3yww_1oY ↗ |
| Devcon bar | [ Real-time ZK proofs ] | youtube.com/watch?v=Mdneqyvvk7g ↗ |
| Logo | — | `/` |
| Use cases ▾ | Institutions · *Banks, funds and fintechs* | `/use-cases/institutions` |
| | Chains · *Rollup teams and new chains* | `/use-cases/chains` |
| | Apps · *Apps that call across chains* | `/use-cases/apps` |
| | Infra · *Infra providers and wallets* | `/use-cases/infra` |
| | All use cases · *Every use case, sorted by job* | `/use-cases/all` |
| Developers ▾ | Docs · *Protocol spec, guides and reference* | docs.eez.io ↗ |
| | Quickstarts · *Step-by-step walkthroughs* | build.eez.io ↗ |
| | Dashboard · *See calls settle on the testnet* | eez.dev/dashboard/ ↗ |
| | GitHub · *eez-association on GitHub* | github.com/eez-association ↗ |
| Button | Get in touch → | `/get-in-touch` |

The current page's menu item is marked (`aria-current`).

### Shared footer (every page)
| Column | Label | Goes to |
|---|---|---|
| Brand | Logo + "EEZ activates Ethereum as an economic operating system for composable zones." | `/` |
| Use cases | Institutions · Chains · Apps · Infra · All use cases | `/use-cases/…`, `/use-cases/all` |
| Developers | Docs ↗ · Quickstarts ↗ · Dashboard ↗ · GitHub ↗ | same as header |
| | Contribute a walkthrough ↗ | github.com/eez-association/eez-demos/blob/main/CONTRIBUTING.md |
| News | News | eez.io/blog |
| | Press and talks | `/#news` |
| | Brand and logo | `#` (dead, issue 1) |
| Follow | X ↗ | x.com/etheconomiczone |
| | GitHub ↗ | github.com/eez-association |
| — | © 2026 Ethereum Economic Zone. | — |

### Home `/`
| Section | Label | Goes to |
|---|---|---|
| Hero | Use cases → | `/use-cases/all` |
| Hero | Start building → | build.eez.io ↗ |
| What you can build | Try on the testnet → | eez.dev (same tab, issue 3) |
| What you can build | All use cases → | `/use-cases/all` |
| Carousel card panel | Try the swap demo (Swap on Ethereum liquidity) | rollupx.eez.dev/dashboard/#/cow-demo ↗ |
| | Try a cross-chain call (Public and private chains) | rollupx.eez.dev/dashboard/#/counter-demo ↗ |
| | Try the Safe demo (One account, every chain) | rollupx.eez.dev/dashboard/#/treasury-demo ↗ |
| | Try the post-quantum demo (Post-quantum keys) | rollupx.eez.dev/dashboard/#/falcon-demo ↗ |
| | Read the walkthroughs (Read Ethereum, no oracle) | build.eez.io ↗ |
| Start where you are | For institutions → | `/use-cases/institutions` |
| | For rollup teams → | `/use-cases/chains` |
| | For app developers → | `/use-cases/apps` |
| | For infra & wallets → | `/use-cases/infra` |
| Alliance | Join the Alliance | `/get-in-touch?intent=alliance` |
| Alliance | Partner logos (30) | not links |
| Hear it from the team | One Ethereum: Same Block, Every Chain | youtube.com/watch?v=uvY3yww_1oY ↗ |
| | EEZ: Building Synchronous Ethereum… | youtube.com/watch?v=Mdneqyvvk7g ↗ |
| | Vitalik Buterin on the EEZ (Epicenter) | youtube.com/watch?v=CK1FwcWdqMI ↗ |
| | Vitalik Buterin and Friederike Ernst (Dappcon) | youtube.com/watch?v=gfG-R8AOu0E ↗ |
| | All talks → | YouTube search "ethereum economic zone" ↗ |
| Latest | Monthly update · September 2026 | eez.io/blog ↗ (issue 2) |
| | Monthly update · August 2026 | eez.io/blog/monthly-update-august-2026 ↗ |
| | Introducing the Ethereum Economic Zone | eez.io/blog/introducing-the-eez ↗ |

### Use-case and contact pages (besides header/footer)
| Page | Label | Goes to |
|---|---|---|
| Institutions | All use cases → | `/use-cases/all?role=institutions` |
| | Get in touch → | `/get-in-touch?role=institution` |
| Chains | Joining, step by step → | `/use-cases/scoping` |
| | Get in touch → | `/get-in-touch?role=chain` |
| Apps | All use cases → | `/use-cases/all?role=dapps` |
| | Get in touch → | `/get-in-touch?role=dapp` |
| Infra | All use cases → | `/use-cases/all?role=infra` |
| | Get in touch → | `/get-in-touch?role=infra` |
| All use cases | Get in touch → | `/get-in-touch` |
| Scoping | Addresses → | `/use-cases/chains` |
| | Get in touch → | `/get-in-touch` |
| Kit | — | header/footer only |
| Get in touch | Docs → · Quickstarts → · Dashboard ↗ · GitHub ↗ (side panel) | docs.eez.io · build.eez.io · eez.dev/dashboard/ · github.com/eez-association, all ↗ |
| | Scoper "next step" link (changes with answers) | institutions → `/use-cases/institutions`; chains → `/use-cases/chains#steps`, `/use-cases/scoping`, `/use-cases/chains` or eez.dev; dapps → docs; infra → `/use-cases/infra`; research → docs.eez.io |

**URL parameters:**
- `?intent=alliance` preselects "Join the Alliance" and shows the Alliance questions.
- `?role=…` preselects "Integrate EEZ".
- On All use cases, `?role=` sets the filter chip (`institutions`, `chains`, `dapps` or `infra`).

### All use cases: 35 cards
Built from data in the page. Filter chips: All, Institutions, Chains, Dapps, Infra. Search box: `/` focuses it. Tags: *now* = Works today, *later* = After the audit, *coming* = Coming. A card link reads "Read more →", or "See it live →" for external links.

| Category | Use case | Status | Link |
|---|---|---|---|
| Risk and collateral | Margin call, priced live | now | `/use-cases/institutions#use-cases` |
| | Eligibility changes in a crisis | now | `/use-cases/institutions#use-cases` |
| | Liquidation check against L1 | now | — |
| | Collateral reallocation | later | `/use-cases/institutions#use-cases` |
| | Securities lending | later | — |
| | Intraday repo | later | `/use-cases/institutions#use-cases` |
| Compliance and access | Eligibility gate | now | — |
| | Sanctions check at trade time | now | `/use-cases/institutions#use-cases` |
| | Permission gate on L1 · Credential gating · Mint only against reserves | now | — |
| Prices and data | Oracle-free read | now | eez.dev/dashboard ↗ |
| | Reference pricing · Name lookup on L1 · Voting power from L1 · Publish once, read everywhere | now | — |
| Trading and liquidity | Run your own engine | now | — |
| | Unified liquidity | later | rollupx.eez.dev/dashboard/#/cow-demo ↗ |
| | Atomic arbitrage · Atomic redemption · Solver fills from L1 liquidity | later | — |
| | Shared order book across chains | coming | — |
| Payments and accounts | Key rotation once | now | rollupx.eez.dev/dashboard/#/treasury-demo ↗ |
| | Cross-chain calls in one signature · Show the real user | now | — |
| | Currency swap, both legs or neither | later | `/use-cases/institutions#use-cases` |
| | Treasury sweep · Payments in one signature · Settle where the money is | later | — |
| Chains and infrastructure | Call Ethereum from your chain | now | eez.dev/dashboard ↗ |
| | Your own EEZ network | now | — |
| | Keep what is yours | now | `/use-cases/chains` |
| | Serve users on EEZ chains | now | `/use-cases/infra` |
| | Reach other EEZ chains · Deploy once, call every chain | coming | — |

---

## 2. Animations

All of them respect reduced motion, which shows the final state with no motion.

### Shared
| Element | Trigger | Motion and timing |
|---|---|---|
| Header dropdowns | Hover (wide screens with a pointer), click, Enter, ↓ arrow | Opens instantly, no fade. Closes 250 ms after the pointer leaves; also closes on Esc or a click outside |
| Mobile menu (≤760 px) | Menu button | Opens and closes instantly |
| Pill button arrows | Hover | Arrow nudges, 0.2 s |

### Home
| Element | Trigger | Motion and timing |
|---|---|---|
| Hero Ethereum mark | Always | Floats up 10 px and back, 6 s ease-in-out, loops |
| Alliance logo strip | Always | Scrolls at 40 px/s and loops; slows to 12 px/s on hover (eases in about 0.25 s) |
| "One call away" diagram (a video) | Hover, focus or tap | Plays from 0; at rest it shows the 4.5 s frame. Tilts with the pointer (±2° / ±1.5°), 0.25 s |
| Carousel: centre card | Arrives in the centre while ≥40% of the carousel is on screen | Plays its animation after 450 ms. Stops when it leaves the centre or the carousel leaves the screen |
| Carousel: card animations | Hover, focus or tap (and the autoplay above) | Swap: 0.9 s in and out. Safe: 1.6 s in, 0.7 s out. Public and private chains, Post-quantum, Read Ethereum: 1.5 s in, 0.6 s out. Dashed lines march every 0.7 s while playing. Cards tilt with the pointer |
| Carousel: moving between cards | Drag (170 px per card), sideways wheel (60 px), arrows, dots, clicking a side card | Cards slide and scale (−6% per step), side cards fade; dots grow 0.3 s |
| Carousel: open a card | Click the centre card (touch: first tap plays, second tap opens), or Enter | Panel grows out of the card, 0.7 s `cubic-bezier(.22,.8,.2,1)`; text fades and rises after 0.25 s (0.4 to 0.5 s). Closes on ×, Esc, a click on the backdrop, or scrolling the carousel off screen |
| Start where you are cards | Hover | Border and background change, 0.22 s |
| Alliance partner tiles | Grid scrolls into view (35%), every time | Each tile bumps up 7 px and scales to 1.04 with a green border, 0.6 s overshoot, 45 ms apart in sequence |
| Alliance tile hover | Hover | Lifts 4 px, green border and glow, logo scales to 1.06, 0.25 s |
| Join the Alliance button | Hover or focus | Green gradient fills the button left to right, 0.5 s `cubic-bezier(.65,0,.35,1)`; arrow moves 6 px |
| Talk thumbnails | Hover | Image zooms, 0.5 s |
| Latest posts | Hover | Border colour, 0.2 s |

### Use-case pages
| Page and element | Trigger | Motion and timing |
|---|---|---|
| Institutions hero (transaction across Bank, Exchange, Ethereum, Custodian) | First time 35% is on screen, then loops | Waits 0.3 s. 4 steps light in turn: each line draws in 0.82 s, with 0.36 s and then 0.16 s gaps. Holds 3.2 s, lines retract in 0.7 s, pauses 0.5 s, repeats. Eased in and out |
| Chains hero (your chain → Ethereum apps → other EEZ chains) | Same | Your chain lights (0.26 s), line 0.82 s, 3 apps light (0.3 / 0.3 / 0.36 s), line 0.82 s, other chains (0.2 s). Holds 3.2 s, retracts 0.7 s, repeats |
| Apps hero (one app, three user groups) | Same | App lights (0.26 s), then 3 × (line 0.82 s + user box 0.2 s). Holds 3.2 s, retracts 0.7 s, repeats |
| Infra hero (stack → RPC chains → composer) | Same | States switch on at 0.2, 0.4, 0.8, 1.2, 1.6, 2.1 and 2.5 s; status at 2.7 s. Restarts every 6 s |
| Apps: step sequence diagram | First time 35% is on screen | Plays alone, 5.2 s per step. Each message line draws in 1.8 s; the caption crossfades in 0.18 s. Click a step or use the keys to jump |
| Institutions: process tabs | Click or arrow keys | Bar and title colour change, 0.2 s |
| Spotlight cards (Institutions 6, Apps 3, Infra 3) | Pointer move | A radial highlight follows the pointer; fades in 0.3 s |

---

## 3. Repeated elements

| Element | Where | Count | Contents |
|---|---|---|---|
| Section header | Every section | — | `[ EYEBROW ]` (mono, grey) + heading (Geist Light) |
| Pill button | Hero ×2, Try on the testnet, Get in touch | 7 on Home | Label + round arrow chip |
| Mono text link "… →" | All use cases, card links, All talks | — | Uppercase Geist Mono, green or white, arrow |
| Dropdown item | Header menus | 5 + 4 | Bold title + one-line grey description |
| Use-case carousel card | Home | 5 | Title, number (01–05), animated isometric diagram, 2 stat rows, panel text + demo link |
| Audience card | Start where you are | 4 | Isometric icon, title, one line, "For … →" link |
| Partner group | Alliance | 13 groups, 30 tiles | `[ Category ]` label + logo tiles; 2 bands: Adoption and Infrastructure partners |
| Progress card | Where EEZ stands | 5 | Status tag (Live, In progress, Planned, Horizon) + title + one line |
| Talk card | Hear it from the team | 4 | Thumbnail + duration, `TYPE · EVENT · DATE`, title ↗ |
| Post card | Latest | 3 | Cover image, date, title |
| Footer column | Footer | 4 | `[ Column ]` label + links |
| Use-case card | All use cases | 35 in 6 categories | Number, title, one line, roles, status tag, optional link |
| Filter chip | All use cases | 5 | Label + live count |
| Spotlight card | Institutions, Apps, Infra | 6 / 3 / 3 | Pointer-following highlight |
| Form section card | Get in touch | 5 (+3 in side panel) | `01`–`05` number + heading + fields |
| Intent option | Get in touch | 5 | Radio card: bold title + one line |
