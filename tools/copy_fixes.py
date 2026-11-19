"""Copy standards for every built page (dist/), agreed 20 Nov 2026.

- Audiences: Institutions · Chains · Apps · Infra, one name each, and "and" instead of "&".
- "zone" stays only in the name Ethereum Economic Zone; elsewhere "chain". EEZ network / instance -> EEZ chain.
- "Testnet" -> "Devnet" (Chiado keeps "testnet": it is Gnosis's public testnet).
- Status labels: Live · Devnet only · Planned. "Works with changes", "As designed" and the home roadmap stay.
- Two reworded lines (Institutions, Chains).

Each pair must match at least once, so a source change fails the build instead of silently
skipping a fix. Runs after live_parity.py and before smart_quotes.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

FIXES = [
    # audiences
    ("Rollup teams and new chains", "Public, private and new chains"),
    ("Infra providers and wallets", "Nodes, provers and wallets"),
    ("EEZ for rollup teams", "EEZ for chains"),
    ("For rollup teams", "For chains"),
    ("A rollup team or new chain", "A chain"),
    ("That work starts with its rollup team.", "That work starts with its team."),
    ("EEZ for dapp developers", "EEZ for apps"),
    ("For dapp developers", "For apps"),
    ("For app developers", "For apps"),
    ("A dapp developer", "An app"),
    ("chain, institution, dapp or infra", "chain, institution, app or infra"),
    ('aria-pressed="false">Dapps<', 'aria-pressed="false">Apps<'),
    ('dapps: "Dapps"', 'dapps: "Apps"'),
    ("EEZ for infra and wallets", "EEZ for infrastructure operators and wallets"),
    ("For infra &amp; wallets", "For infrastructure operators and wallets"),
    # the home card button keeps it short; the Infra page keeps the full name
    ("<span>For infrastructure operators and wallets</span>", "<span>For infra and wallets</span>"),
    ("Infra or wallet", "Infra"),
    # zone -> chain (the name Ethereum Economic Zone is untouched)
    ("operating system for composable zones.", "operating system for composable chains."),
    ("Zones stay cheap and fast", "Chains stay cheap and fast"),
    ("a zone can call Ethereum and use the answer", "a chain can call Ethereum and use the answer"),
    ("at a zone's speed and cost", "at a chain's speed and cost"),
    ("a cheap, fast zone without a bridge", "a cheap, fast chain without a bridge"),
    ("a walled bank zone", "a walled bank chain"),
    ("and a bank zone", "and a bank chain"),
    ("and bank zones keep", "and bank chains keep"),
    ('label: "Bank zone"', 'label: "Bank chain"'),
    ("permissioned zones like a bank", "permissioned chains like a bank"),
    ("Zones call Ethereum and each other", "Chains call Ethereum and each other"),
    ("Zones are proven with ZK proofs", "Chains are proven with ZK proofs"),
    ("Your own EEZ network", "Your own EEZ chain"),
    ("own EEZ network on Chiado", "own EEZ chain on Chiado"),
    ("A testnet EEZ network to pilot on.", "A devnet EEZ chain to pilot on."),
    ("Run your own EEZ network", "Run your own EEZ chain"),
    ("general‑purpose EEZ instance", "general‑purpose EEZ chain"),
    ("the first EEZ instance", "the first EEZ chain"),
    # testnet -> devnet
    ("EEZ-X Testnet", "EEZ-X Devnet"),
    ("See calls settle on the testnet", "See calls settle on the devnet"),
    ("piloted on testnet now", "piloted on devnet now"),
    ("Try on the testnet", "Try on the devnet"),
    ("<h3>Ethereum Testnet</h3>", "<h3>Ethereum Devnet</h3>"),
    ('<span class="eez-badge">Testnet</span>', '<span class="eez-badge">Devnet</span>'),
    ("Pilot on testnet now", "Devnet only"),
    ("Pilot value moves on testnet now", "Pilot value moves on devnet now"),
    ("On testnet, value moves", "On devnet, value moves"),
    ("pilot value moves on testnet when", "pilot value moves on devnet when"),
    ("Open the testnet", "Open the devnet"),
    ("<h3>Pilot on testnet</h3>", "<h3>Pilot on devnet</h3>"),
    # status labels: Live · Devnet only · Planned
    ("Works today", "Live"),
    ("Works now", "Live"),
    ("Pilot now", "Devnet only"),
    ("After the audit", "Planned"),
    ('coming: "Coming"', 'coming: "Planned"'),
    ("Coming soon.", "Planned."),
    ("(coming soon)", "(planned)"),
    ("Conformance kit · coming soon", "Conformance kit · Planned"),
    # "Before you commit" boxes: status, not a warning
    ('<h2 class="doc-h2">Before you commit</h2>', '<h2 class="doc-h2">Where it stands today</h2>'),
    ('<span class="cmp-eyebrow">Plan for these</span><h3>In progress</h3>', '<span class="cmp-eyebrow">Next</span><h3>In progress</h3>'),
    ('<span class="cmp-eyebrow">Plan for these</span><h3>What changes</h3>', '<span class="cmp-eyebrow">Good to know</span><h3>What changes</h3>'),
    ("Today's gaps by role.", "What runs now and what comes next, by role."),
    # no em-dashes in visible copy (they read as AI-written)
    ('<b id="l9done">—</b>', '<b id="l9done">Waiting</b>'),
    ('l9.textContent = ok ? "$1,784" : "—";', 'l9.textContent = ok ? "$1,784" : "Waiting";'),
    ("A chain that can carry cross-chain work — or a hard fork", "A chain that can carry cross-chain work, or a hard fork"),
    ("before you can pin your L2 genesis — for a live chain, a hard fork after a counter you do not control.",
     "before you can pin your L2 genesis. On a live chain, that means a hard fork after a counter you do not control."),
    ('li::before { content: "—";', 'li::before { content: "·";'),
    ('li::before{content:"—";', 'li::before{content:"·";'),
    # reworded lines
    ("<h3>One question before we scope</h3>", "<h3>Tell us what you run</h3>"),
    ("<p>Which role, and which chain. The scoper tells you what applies before you send anything.</p>",
     "<p>Which role you play and which chains you serve. We'll come back with what applies to your setup and where to start.</p>"),
    ("<h3>Which contract, which chain</h3>", "<h3>Tell us what you're building</h3>"),
    ("<p>Answer three questions and the scoper tells you whether your pattern works today, with changes, or not yet.</p>",
     "<p>Which contract, and which chains it should reach. We'll come back with what works today and what it takes.</p>"),
    ("<h3>Three answers decide the call</h3>", "<h3>Whether or not it's right for you depends on three things.</h3>"),
    ("Do you run a sequencer, and are you pre-launch or live?", "Do you run a sequencer? And are you pre-launch or live?"),
]


def main():
    files = [f for f in DIST.rglob("*") if f.suffix in {".html", ".js", ".json", ".css"} and "vendor" not in f.parts]
    text = {f: f.read_text() for f in files}
    missing = []
    for old, new in FIXES:
        if old == new:
            continue
        hits = 0
        for f, s in text.items():
            n = s.count(old)
            if n:
                text[f] = s.replace(old, new)
                hits += n
        if not hits:
            missing.append(old)
    for f, s in text.items():
        if s != f.read_text():
            f.write_text(s)
    if missing:
        sys.exit("copy_fixes: not found: " + " | ".join(missing))
    print(f"copy fixes: {len(FIXES)} applied")


if __name__ == "__main__":
    main()
