// Intake scoper: answers -> tier, what applies, one next step.
// Runs in the browser. "Send the intake" opens the Tally form with these answers as hidden fields.
(function () {
  var form = document.getElementById('scoper');
  if (!form) return;

  var DOCS = 'https://docs.eez.io';
  var TIER = {
    ok: { label: 'Works today', cls: 'tier-ok' },
    mid: { label: 'Works with changes', cls: '' },
    pilot: { label: 'Pilot on testnet now', cls: '' },
    no: { label: 'Not yet', cls: 'tier-no' },
    read: { label: 'Read first', cls: '' }
  };

  function val(name) {
    var el = form.elements[name];
    return el ? el.value : '';
  }

  function scope() {
    var role = val('role');
    var r = { tier: 'mid', headline: '', applies: [], next: ['Read the protocol docs', DOCS] };

    if (role === 'institution') {
      var touch = val('touch');
      r.applies.push('Start on your own EEZ network on Chiado: your allowlist, your keys, no value at risk.');
      r.applies.push('Everything is public, including counterparties and sizes.');
      r.applies.push('Verification today is a single ECDSA attestation at threshold 1.');
      if (touch === 'value') {
        r.tier = 'pilot';
        r.headline = 'Pilot value moves on testnet now. Mainnet waits for a production proof system and an audit.';
        r.applies.push('On testnet, value moves through a test bridge. No mainnet date yet.');
      } else {
        r.headline = touch === 'read'
          ? 'Reads can be piloted now, with constraints your risk function will ask about.'
          : 'Start with reads; pilot value moves on testnet when you are ready.';
      }
      r.next = ['See the constraints', '/use-cases/institutions'];
    }

    if (role === 'chain') {
      var stage = val('stage'), stack = val('stack');
      if (stack === 'none') {
        r.tier = 'ok';
        r.headline = 'Launching a new chain? Start it inside EEZ.';
        r.applies.push('Register on L1 before you freeze genesis: the rollupId goes into genesis, so joining needs no hard fork.');
        r.applies.push('You run a composer, a proof signer and a deriver, plus an L1 gas budget.');
        r.next = ['See the steps', '/use-cases/chains#steps'];
        return r;
      }
      if (stage === 'devnet') {
        r.tier = 'ok';
        r.headline = 'Run your own EEZ network, or build against the EEZ-X Testnet.';
        r.next = ['Open the testnet', 'https://eez.dev'];
      } else {
        r.headline = stage === 'live'
          ? 'A live chain joins by hard fork, or a path agreed on the scoping call.'
          : 'Pre-launch is the cheapest moment to join.';
        r.next = ['See the eight steps', '/use-cases/scoping'];
      }
      r.applies.push(stage === 'live'
        ? 'Your L2 genesis takes the rollupId from registration, so a live chain forks after registering.'
        : 'Register on L1 before you freeze genesis. Step 2 must precede step 3.');
      r.applies.push('You run a composer, a proof signer and a deriver, plus an L1 gas budget.');
      if (stack === 'op' || stack === 'orbit' || stack === 'zk') {
        r.applies.push('Per-stack notes are written with the first design partner. None are published yet.');
      }
    }

    if (role === 'dapp') {
      var where = val('where'), auth = val('auth'), hot = val('hot'), sign = val('sign');
      if (where === 'other') {
        r.tier = 'no';
        r.headline = 'A call only lands on chains in the same EEZ registry.';
        r.applies.push('Your chain has to register first. That work starts with its rollup team.');
        r.next = ['Send your chain team here', '/use-cases/chains'];
      } else {
        if (where === 'l1') r.applies.push('Your L1 contract stays as it is. A contract on the EEZ chain calls it through a proxy.');
        if (auth !== 'no') r.applies.push('msg.sender is the proxy. Allowlist the source proxy, not the user.');
        if (hot !== 'no') r.applies.push('A write needs an entry verified in the same L1 block. If the state it depends on moves first, the call does not land.');
        if (sign === 'wallets') r.applies.push('Cross-chain calls must be estimated and sent through the composer front. You cannot guarantee that inside a wallet you do not control.');
        var changes = auth !== 'no' || hot !== 'no' || sign === 'wallets';
        r.tier = changes ? 'mid' : 'ok';
        r.headline = changes ? 'It works, with the changes below.' : 'Nothing in your answers blocks it.';
        r.next = changes ? ['Read the protocol docs', DOCS]
          : ['Deploy your first contract', 'https://build.eez.io/dapp-developers/qs6-deploy-your-own-contract.html'];
      }
    }

    if (role === 'infra') {
      var ir = val('infrarole');
      var INFRA = {
        indexer: ['ok', 'Add the chain ID and RPC.', ['Standard block, log and receipt methods.', 'EEZ-X Testnet 699169 · RollupX 696991.']],
        wallet: ['mid', 'Plain transfers work. Cross-chain calls need changes.', ['Route the call to the composer front, not a plain RPC.', 'Estimate through the same front; the estimate covers only the source transaction.', 'L1 → L2 fees include settlement.']],
        aa: ['mid', 'Plain user operations work. Cross-chain ones need changes.', ['A cross-chain user operation must be estimated and sent through the composer front.']],
        builder: ['mid', 'Inclusion is scoped per builder.', ['The composer posts batches to L1 and decides which entries land.']],
        node: ['mid', 'Run the follower node from the reference repo.', ['The eez-follower crate ships in eez-rollup0.', 'Or run a deriver to rebuild the chain from L1.']]
      }[ir];
      r.tier = INFRA[0];
      r.headline = INFRA[1];
      r.applies = INFRA[2];
      r.next = ['See your role', '/use-cases/infra'];
    }

    if (role === 'research') {
      r.tier = 'read';
      r.headline = 'Start with the protocol docs.';
      r.applies.push('The docs are pinned to a commit. Check it against the deployment you study.');
      r.next = ['Protocol docs', 'https://docs.eez.io'];
    }

    return r;
  }

  function render() {
    var role = val('role');
    var blocks = form.querySelectorAll('.when');
    for (var i = 0; i < blocks.length; i++) {
      blocks[i].hidden = blocks[i].getAttribute('data-for') !== role;
    }

    var r = scope();
    var tier = document.getElementById('tier');
    tier.textContent = TIER[r.tier].label;
    tier.className = 'tier-line ' + TIER[r.tier].cls;
    document.getElementById('headline').textContent = r.headline;

    var ul = document.getElementById('applies');
    ul.textContent = '';
    r.applies.forEach(function (t) {
      var li = document.createElement('li');
      li.textContent = t;
      ul.appendChild(li);
    });

    document.getElementById('next-label').textContent = r.next[0];
    document.getElementById('next').href = r.next[1];
    document.getElementById('send-label').textContent =
      r.tier === 'no' ? 'Tell me when it is ready' : 'Send the intake';
    last = { role: role, tier: TIER[r.tier].label, answers: answers() };
    sendHref();
  }

  // The intake itself is a Tally form (Gnosis Comms workspace). The scoper's
  // answers ride along as hidden fields; the respondent adds project and contact.
  var TALLY_ID = 'RWW79Q';
  var TALLY_URL = 'https://tally.so/r/' + TALLY_ID;
  var last = null;

  function answers() {
    var out = [];
    var inputs = form.querySelectorAll('.when:not([hidden]) input:checked, .when:not([hidden]) select');
    for (var i = 0; i < inputs.length; i++) out.push(inputs[i].name + '=' + inputs[i].value);
    return out.join('; ');
  }

  // first-touch source and the landing card that led here, kept for the visit by nav.js
  function visit(key) { try { return sessionStorage.getItem(key) || ''; } catch (e) { return ''; } }
  function field(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }

  function hidden() {
    return { role: last.role, tier: last.tier, answers: last.answers, page: 'intake',
      project: field('in-project'), reply: field('in-reply'),
      source: visit('eez-source') || 'direct', door: visit('eez-door') };
  }
  function sendHref() {
    if (last) document.getElementById('send').href = TALLY_URL + '?' + new URLSearchParams(hidden()).toString();
  }

  document.getElementById('send').addEventListener('click', function (e) {
    if (!window.Tally || !last) return; // no script: the link opens the form in a new tab
    e.preventDefault();
    window.Tally.openPopup(TALLY_ID, { layout: 'modal', width: 560, hiddenFields: hidden() });
  });

  // any radio can be preset from the URL, e.g. ?role=chain&stage=pre for a chain that hasn't launched
  new URLSearchParams(location.search).forEach(function (value, name) {
    var input = form.querySelector('input[type="radio"][name="' + CSS.escape(name) + '"][value="' + CSS.escape(value) + '"]');
    if (input) input.checked = true;
  });

  form.addEventListener('change', render);
  ['in-project', 'in-reply'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', sendHref);
  });
  render();
})();
