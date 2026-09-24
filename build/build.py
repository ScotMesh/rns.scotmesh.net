import json, pathlib

lock = json.loads(pathlib.Path('lockups.json').read_text())
sm = json.loads(pathlib.Path('scotmesh-lockups.json').read_text())

HEAD = '''<title>ScotMesh Backbone</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@400;600&display=swap">
<script>
  /* Apply the saved theme before anything paints. The page is designed for both;
     with nothing saved it follows the operating system. */
  (function () {
    try {
      var t = localStorage.getItem('rns-theme');
      if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
    } catch (e) { /* storage can be blocked; the OS setting still applies */ }
  })();
</script>
<style>
  /* ScotMesh brand tokens with the Reticulum network tint, per ScotMesh/branding.
     Dark-first: the bare :root carries Night, and light is the deliberate swap
     for both the unstamped and the explicitly stamped case. */
  :root {
    --night: #0A1424;
    --saltire: #005EB8;
    --mist: #E6EDF7;
    --signal: #F2B33D;
    --reticulum: #B199F4;
    --reticulum-deep: #6A51A4;

    --bg: var(--night);
    --well: #0C1729;
    --card: #101C30;
    --line: #22324D;
    --ink: var(--mist);
    --muted: #8FA2BD;
    --link: #7FB2EE;

    --accent: var(--reticulum);
    --chrome: var(--saltire);
    --chrome-ink: #7FB2EE;
    --on-accent: #120A22;
    --good: #65C281;
    --bad: #E4707A;

    --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
    --sans: "IBM Plex Sans Condensed", "Roboto Condensed", "Arial Narrow", system-ui, sans-serif;
    --shadow: 0 1px 0 rgba(255,255,255,.03), 0 12px 32px -18px rgba(0,0,0,.9);
    --wrap: 1140px;
  }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) {
      --bg: #F4F7FC; --well: #EAF0F9; --card: #FFF; --line: #D3DEEE;
      --ink: var(--night); --muted: #5A6B85; --link: var(--saltire);
      --accent: var(--reticulum-deep); --chrome-ink: var(--saltire); --on-accent: #FFF;
      --good: #05773B; --bad: #A61B28;
      --shadow: 0 1px 0 rgba(255,255,255,.7), 0 12px 28px -20px rgba(10,20,36,.45);
    }
  }
  :root[data-theme="light"] {
    --bg: #F4F7FC; --well: #EAF0F9; --card: #FFF; --line: #D3DEEE;
    --ink: var(--night); --muted: #5A6B85; --link: var(--saltire);
    --accent: var(--reticulum-deep); --chrome-ink: var(--saltire); --on-accent: #FFF;
    --good: #05773B; --bad: #A61B28;
    --shadow: 0 1px 0 rgba(255,255,255,.7), 0 12px 28px -20px rgba(10,20,36,.45);
  }

  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--ink);
    font-family: var(--sans); font-size: 16px; line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }
  .wrap { max-width: var(--wrap); margin-inline: auto; padding-inline: 20px; }
  h1, h2, h3 { font-family: var(--mono); font-weight: 600; margin: 0; text-wrap: balance; }
  a { color: var(--link); }
  code, .mono { font-family: var(--mono); }

  /* ---------------------------------------------------------------- header */
  .nav { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20;
    background: color-mix(in srgb, var(--bg) 92%, transparent);
    backdrop-filter: blur(8px); border-bottom: 1px solid var(--line); }
  .nav .wrap { display: flex; align-items: center; gap: 14px; min-height: 60px; flex-wrap: wrap; }
  .lockup { display: block; margin-right: auto; }
  .lockup svg { display: block; height: 34px; width: auto; }
  .lockup .on-light { display: none; }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) .lockup .on-light { display: block; }
    :root:not([data-theme="dark"]) .lockup .on-dark { display: none; }
  }
  :root[data-theme="light"] .lockup .on-light { display: block; }
  :root[data-theme="light"] .lockup .on-dark { display: none; }
  .nav nav { display: flex; align-items: center; gap: 4px; flex-wrap: wrap; }
  .nav nav a { font-family: var(--mono); font-size: 13.5px; text-decoration: none;
    color: var(--muted); padding: 7px 10px; border-radius: 6px; border: 1px solid transparent; }
  .nav nav a:hover { color: var(--ink); background: var(--well); }
  .theme-toggle { display: inline-flex; align-items: center; justify-content: center;
    width: 34px; height: 32px; padding: 0; margin-left: 2px; color: var(--muted);
    background: none; border: 1px solid transparent; border-radius: 6px; cursor: pointer; }
  .theme-toggle:hover { color: var(--ink); background: var(--well); }
  .theme-toggle .t-light { display: none; } .theme-toggle .t-dark { display: block; }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) .theme-toggle .t-dark { display: none; }
    :root:not([data-theme="dark"]) .theme-toggle .t-light { display: block; }
  }
  :root[data-theme="light"] .theme-toggle .t-dark { display: none; }
  :root[data-theme="light"] .theme-toggle .t-light { display: block; }
  :root[data-theme="dark"] .theme-toggle .t-dark { display: block; }
  :root[data-theme="dark"] .theme-toggle .t-light { display: none; }

  /* ------------------------------------------------------------------ hero
     The banner is always dark: the diagram is drawn on Night and the tokens
     below pin the dark palette for everything inside it, so it must paint its
     own background or in light mode this ink lands on a light page. */
  .hero { position: relative; overflow: hidden; border-bottom: 1px solid #22324D;
    color: var(--ink); background: var(--bg);
    --bg: #0A1424; --ink: #E6EDF7; --muted: #8FA2BD; --line: #22324D;
    --card: #101C30; --accent: #B199F4; --on-accent: #120A22; --good: #65C281; --bad: #E4707A; }
  .hero-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 520px);
    gap: 38px; align-items: center; padding-block: 56px 76px; }
  h1 { font-size: clamp(30px, 4.4vw, 46px); line-height: 1.07; letter-spacing: -0.01em; max-width: 18ch; }
  .lede { font-size: clamp(16px, 2.1vw, 19px); color: var(--muted); max-width: 54ch; margin: 14px 0 0; }
  .cta-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }
  .btn { display: inline-flex; align-items: center; gap: 8px; font-family: var(--mono);
    font-size: 14px; font-weight: 600; text-decoration: none; padding: 11px 17px;
    border-radius: 8px; border: 1px solid var(--line); color: var(--ink); background: var(--card); }
  .btn:hover { border-color: color-mix(in srgb, var(--accent) 55%, var(--line)); }
  .btn-primary { background: var(--chrome); border-color: var(--chrome); color: #fff; }
  .btn-primary:hover { border-color: #fff; }

  /* the live state of the node, as a line of chips */
  .state { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 22px; }
  .chip { display: inline-flex; align-items: center; gap: 7px; font-family: var(--mono);
    font-size: 12.5px; padding: 5px 11px; border-radius: 999px;
    border: 1px solid var(--line); background: var(--card); color: var(--muted); }
  .chip b { color: var(--ink); font-weight: 600; }
  .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--good); }
  .dot.off { background: var(--bad); }

  /* ------------------------------------------------------------- the figure */
  .figure { position: relative; }
  .paths { display: block; width: 100%; height: auto; }
  .fig-note { font-family: var(--mono); font-size: 11.5px; color: var(--muted);
    margin-top: 10px; text-align: center; }
  @media (prefers-reduced-motion: reduce) { .pulse { display: none; } }

  /* ------------------------------------------------------------------ stats */
  /* The strip hangs over the hero's bottom edge, the same as the sibling
     sites, so the section rule runs behind the tiles rather than under them. */
  .hero-stats { position: relative; z-index: 2; margin-top: -46px; }
  .hero-stats .wrap { display: grid; gap: 10px; }
  .stats { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px;
    padding-block: 0 26px; }
  .stat { background: var(--card); border: 1px solid var(--line); border-radius: 10px;
    padding: 14px 16px 13px; box-shadow: var(--shadow); display: grid; gap: 3px; }
  .stat-v { font-family: var(--mono); font-size: clamp(22px, 3vw, 30px); font-weight: 600; line-height: 1.05;
    font-variant-numeric: tabular-nums; }
  .stat-k { font-size: 13.5px; color: var(--muted); }
  .stat.is-live { background: var(--accent); border-color: var(--accent); }
  .stat.is-live .stat-v { color: var(--on-accent); }
  .stat.is-live .stat-k { color: color-mix(in srgb, var(--on-accent) 78%, transparent); }
  .stats-note { grid-column: 1 / -1; margin: 2px 0 0; font-size: 13px; color: var(--muted); }

  /* --------------------------------------------------------------- sections */
  section { border-bottom: 1px solid var(--line); }
  section.alt { background: var(--well); }
  .sec { padding-block: 52px; }
  .sec-head { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; margin-bottom: 24px; }
  .sec-head h2 { font-size: clamp(20px, 2.6vw, 26px); }
  .sec-head p { margin: 0; color: var(--muted); font-size: 14.5px; }

  .cards { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 12px;
    padding: 20px; box-shadow: var(--shadow); display: flex; flex-direction: column; gap: 10px; }
  .card.lead { border-color: color-mix(in srgb, var(--accent) 55%, var(--line)); }
  .card h3 { font-size: 16px; display: flex; align-items: center; gap: 9px; flex-wrap: wrap; }
  .card p { margin: 0; font-size: 14.5px; color: var(--muted); }
  .tag { font-family: var(--mono); font-size: 11px; font-weight: 400; letter-spacing: .04em;
    text-transform: uppercase; color: var(--accent);
    border: 1px solid color-mix(in srgb, var(--accent) 45%, transparent);
    border-radius: 999px; padding: 2px 8px; }
  pre { margin: 0; background: var(--well); border: 1px solid var(--line); border-radius: 8px;
    padding: 12px 13px; overflow-x: auto; font-family: var(--mono); font-size: 12.5px;
    line-height: 1.55; color: var(--ink); }
  :root[data-theme="dark"] pre, :root:not([data-theme="light"]) pre { background: #0A1424; }
  .steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 7px;
    font-size: 14.5px; color: var(--muted); }
  .steps li { display: flex; gap: 9px; }
  .steps b { color: var(--ink); font-weight: 600; }

  /* ---------------------------------------------------------------- tables */
  .scroller { overflow-x: auto; border: 1px solid var(--line); border-radius: 12px;
    background: var(--card); box-shadow: var(--shadow); }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { text-align: left; font-family: var(--mono); font-size: 11.5px; font-weight: 400;
    letter-spacing: .05em; text-transform: uppercase; color: var(--muted);
    padding: 12px 16px; border-bottom: 1px solid var(--line); white-space: nowrap; }
  td { padding: 13px 16px; border-bottom: 1px solid var(--line); vertical-align: top; }
  tr:last-child td { border-bottom: 0; }
  td .svc { font-weight: 600; display: block; }
  td .why { color: var(--muted); font-size: 13px; display: block; margin-top: 2px; }
  .hash { font-family: var(--mono); font-size: 12.5px; word-break: break-all; color: var(--accent); }
  .up, .down { font-family: var(--mono); font-size: 12.5px; display: inline-flex;
    align-items: center; gap: 6px; white-space: nowrap; }
  .up { color: var(--good); } .down { color: var(--bad); }

  /* ----------------------------------------------------------- radio profile */
  .profile { display: grid; grid-template-columns: repeat(5, minmax(0,1fr)); gap: 10px; }
  .val { background: var(--card); border: 1px solid var(--line); border-radius: 10px;
    padding: 15px 16px; box-shadow: var(--shadow); }
  .val .k { font-size: 12.5px; color: var(--muted); }
  .val .v { font-family: var(--mono); font-size: 17px; font-weight: 600; margin-top: 3px;
    font-variant-numeric: tabular-nums; }
  .warn { margin: 16px 0 0; padding: 13px 16px; font-size: 14.5px; color: var(--muted);
    border-left: 3px solid var(--signal); background: var(--card);
    border-radius: 0 8px 8px 0; }
  .warn b { color: var(--ink); }

  /* --------------------------------------------------------------- footer */
  footer { padding-block: 34px 44px; font-size: 14px; color: var(--muted); }
  .foot-grid { display: grid; grid-template-columns: 1.5fr repeat(3, minmax(0,1fr)); gap: 26px; }
  .foot-grid ul { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 6px; }
  .foot-grid a { color: var(--muted); text-decoration: none; }
  .foot-grid a:hover { color: var(--ink); }
  .lbl { font-family: var(--mono); font-size: 11.5px; letter-spacing: .05em;
    text-transform: uppercase; color: var(--muted); }

  /* the header is sticky, so an anchored section must stop clear of it */
  section[id] { scroll-margin-top: 72px; }
  html { scroll-behavior: smooth; }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

  .lockup-scotmesh { display: inline-block; }
  .lockup-scotmesh svg { display: block; height: 26px; width: auto; }
  .lockup-scotmesh .on-light { display: none; }
  @media (prefers-color-scheme: light) {
    :root:not([data-theme="dark"]) .lockup-scotmesh .on-light { display: block; }
    :root:not([data-theme="dark"]) .lockup-scotmesh .on-dark { display: none; }
  }
  :root[data-theme="light"] .lockup-scotmesh .on-light { display: block; }
  :root[data-theme="light"] .lockup-scotmesh .on-dark { display: none; }
  .foot-bar { grid-column: 1 / -1; display: flex; justify-content: space-between; gap: 14px; flex-wrap: wrap;
    margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--line); font-size: 13.5px; }
  .foot-bar .mono { font-family: var(--mono); }

  a:focus-visible, button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

  @media (max-width: 900px) {
    .hero-stats { margin-top: -36px; }
    .nav .wrap { padding-block: 10px; row-gap: 4px; }
    .hero-grid { grid-template-columns: 1fr; gap: 26px; padding-block: 38px 24px; }
    .stats { grid-template-columns: repeat(2, minmax(0,1fr)); }
    .cards { grid-template-columns: 1fr; }
    .profile { grid-template-columns: repeat(2, minmax(0,1fr)); }
    .foot-grid { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 540px) {
    .stats { grid-template-columns: 1fr 1fr; }
    .profile { grid-template-columns: 1fr 1fr; }
    .foot-grid { grid-template-columns: 1fr; }
  }
</style>'''


def paths_figure():
    """The hero's thesis: three real transports converging on one node.

    Not a map. Reticulum has no geography to draw — a destination is a hash,
    not a place — so the figure shows what the page is actually for: the ways
    in, and announces arriving along each of them.
    """
    W, H = 520, 340
    hubx, huby = 372, 170
    rows = [
        ('TCP', 'rns.scotmesh.net:4242', 74),
        ('I2P', 'a3pswrtv…b32.i2p', 170),
        ('LoRa', '869.4625 MHz', 266),
    ]
    out = ['<svg class="paths" viewBox="0 0 %d %d" role="img" aria-label="Three transports — TCP, I2P and 868 MHz LoRa — converging on the ScotMesh Backbone transport node, with announces arriving along each">' % (W, H)]
    # the lines first, so everything else sits over them
    for i, (name, addr, y) in enumerate(rows):
        d = 'M96 %d C 210 %d, 250 %d, %d %d' % (y, y, huby, hubx - 30, huby)
        out.append('<defs><path id="rns%d" d="%s"/></defs>' % (i, d))
        out.append('<path d="%s" fill="none" stroke="var(--accent)" stroke-opacity=".34" stroke-width="1.4"/>' % d)
    # the transports
    for i, (name, addr, y) in enumerate(rows):
        out.append('<g>')
        out.append('<rect x="8" y="%d" width="88" height="44" rx="9" fill="var(--card)" stroke="var(--line)"/>' % (y - 22))
        out.append('<text x="52" y="%d" text-anchor="middle" font-family="var(--mono)" font-size="15" font-weight="600" fill="var(--ink)">%s</text>' % (y - 2, name))
        out.append('<text x="52" y="%d" text-anchor="middle" font-family="var(--mono)" font-size="8.5" fill="var(--muted)">%s</text>' % (y + 12, addr))
        out.append('</g>')
    # the node
    out.append('<circle cx="%d" cy="%d" r="52" fill="none" stroke="var(--accent)" stroke-opacity=".20" stroke-width="1"/>' % (hubx, huby))
    out.append('<circle cx="%d" cy="%d" r="40" fill="none" stroke="var(--accent)" stroke-opacity=".32" stroke-width="1"/>' % (hubx, huby))
    out.append('<circle cx="%d" cy="%d" r="27" fill="var(--card)" stroke="var(--accent)" stroke-width="1.6"/>' % (hubx, huby))
    out.append('<circle cx="%d" cy="%d" r="6" fill="var(--accent)"/>' % (hubx, huby))
    out.append('<text x="%d" y="%d" text-anchor="middle" font-family="var(--mono)" font-size="11" font-weight="600" fill="var(--ink)">Backbone</text>' % (hubx, huby + 74))
    out.append('<text x="%d" y="%d" text-anchor="middle" font-family="var(--mono)" font-size="9" fill="var(--muted)">20b962cd…c47f319</text>' % (hubx, huby + 90))
    # announces arriving
    for i in range(len(rows)):
        dur, begin = 3.6 + i * 0.5, i * 0.9
        motion = '<animateMotion dur="%.2fs" begin="%.2fs" repeatCount="indefinite"><mpath href="#rns%d"/></animateMotion>' % (dur, begin, i)
        fade = '<animate attributeName="opacity" dur="%.2fs" begin="%.2fs" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;0.10;0.86;1"/>' % (dur, begin)
        out.append('<circle class="pulse" r="7" fill="var(--signal)" fill-opacity=".22" opacity="0">%s%s</circle>' % (motion, fade))
        out.append('<circle class="pulse" r="3" fill="var(--signal)" opacity="0">%s%s</circle>' % (motion, fade))
    out.append('</svg>')
    return ''.join(out)


ADDRESSES = [
    ('Transport node', 'TCP', 'rns.scotmesh.net:4242', 'Any Reticulum client'),
    ('Transport node', 'I2P', 'a3pswrtvpuro62ijhb7lwdt2n6aqgajglof27ynbonynmolzlz7q.b32.i2p', 'Any client, via a local i2pd'),
    ('Chat hub', 'RRC', '004e5a15da221d9a236b0e8d74195f13',
     'MeshChatX, Ratspeak, rrc-tui, WeeChat — then <code>/join scotmesh</code>'),
    ('Propagation node', 'LXMF', 'c283b754e0acc11ce48d2f5e29167e0c',
     'Sideband, MeshChatX, Nomad Network — usually picked up automatically'),
    ('Nomad Network node', '', '10a839df2c50635bcb0c8a299b9ca0f8:/page/index.mu',
     '<code>nomadnet</code>, MeshChatX'),
    ('Transport instance', '', '20b962cd814444f7812e409e7c47f319',
     'What you see in <code>rnpath</code> and on node maps'),
]

PEERS = [
    ('rebelnet.uk', 'TCP 4242', 'London, England', True),
    ('rns.cybercore.uk', 'TCP 4242', 'Bilston, England', False),
    ('rmap.world', 'TCP 4242', 'France', True),
    ('loj5ofd3a5b5suefcrasn5cnidgofeftnpnko6ym5wkamllrucga.b32.i2p', 'I2P', 'Northern Ireland', False),
]

RADIO = [('Frequency', '869.4625 MHz'), ('Bandwidth', '125 kHz'), ('Spreading factor', 'SF9'),
         ('Coding rate', '4/5'), ('TX power', '22 dBm')]


def rows_addresses():
    out = []
    for svc, kind, addr, use in ADDRESSES:
        label = svc + (' <span class="why">%s</span>' % kind if kind else '')
        out.append('<tr><td><span class="svc">%s</span>%s</td><td class="hash">%s</td>'
                   '<td class="why" style="margin:0">%s</td></tr>'
                   % (svc, ('<span class="why">%s</span>' % kind) if kind else '', addr, use))
    return ''.join(out)


def rows_peers():
    out = []
    for host, transport, where, up in PEERS:
        state = ('<span class="up"><span class="dot"></span>Linked</span>' if up
                 else '<span class="down"><span class="dot off"></span>Down</span>')
        out.append('<tr data-peer="%s"><td class="hash" style="color:var(--ink)">%s</td><td class="mono">%s</td>'
                   '<td>%s</td><td class="link-state">%s</td></tr>' % (host, host, transport, where, state))
    return ''.join(out)


BODY = '''
<header class="nav">
  <div class="wrap">
    <a class="lockup" href="#top" aria-label="ScotMesh Reticulum — home">__DARK____LIGHT__</a>
    <nav aria-label="Primary">
      <a href="#connect">Connect</a>
      <a href="#addresses">Addresses</a>
      <a href="#radio">Radio</a>
      <a href="#peers">Peers</a>
      <a href="https://wiki.scotmesh.net/" target="_blank" rel="noopener">Wiki</a>
      <a href="https://discord.gg/ytxfyuDmSt" target="_blank" rel="noopener">Discord</a>
      <button type="button" id="theme-toggle" class="theme-toggle" aria-label="Switch to light theme" title="Switch theme">
        <svg class="t-dark" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.2 4.2l1.6 1.6M18.2 18.2l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.2 19.8l1.6-1.6M18.2 5.8l1.6-1.6"/></svg>
        <svg class="t-light" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8.2 8.2 0 0 1 9.5 4 8.3 8.3 0 1 0 20 14.5Z"/></svg>
      </button>
    </nav>
  </div>
</header>

<main id="top">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Scotland's way into Reticulum.</h1>
      <p class="lede">
        A public transport node, open to anyone — no registration, no account, no key
        to exchange. Point a client at it and you are on the network; every link is
        encrypted end to end, and this node cannot read a byte of what it carries.
      </p>
      <div class="cta-row">
        <a class="btn btn-primary" href="#connect">Connect a client</a>
        <a class="btn" href="https://wiki.scotmesh.net/wiki/Connecting_to_ScotMesh" target="_blank" rel="noopener">Start from nothing</a>
      </div>
      <div class="state" id="state">
        <span class="chip" id="c-online"><span class="dot"></span><b>Online</b></span>
        <span class="chip"><b id="s-clients">162</b> clients</span>
        <span class="chip">up <b id="s-uptime">14d</b></span>
        <span class="chip"><b id="s-services">5/5</b> services</span>
      </div>
    </div>
    <div class="figure">
      __FIGURE__
      <p class="fig-note">Three ways in, one network. Announces arrive on all of them.</p>
    </div>
  </div>
</section>

<div class="hero-stats">
  <div class="wrap">
    <div class="stats">
      <div class="stat is-live" data-stat="clients"><span class="stat-v">162</span><span class="stat-k">Clients connected</span></div>
      <div class="stat" data-stat="uptime"><span class="stat-v">14d</span><span class="stat-k">Transport uptime</span></div>
      <div class="stat" data-stat="peers"><span class="stat-v">2/4</span><span class="stat-k">Peers linked</span></div>
      <div class="stat"><span class="stat-v">2&nbsp;GB</span><span class="stat-k">Message store</span></div>
      <p class="stats-note">
        Clients, uptime and peer links come from <code>status.json</code>, checked every
        two minutes; the store is a fixed 2&nbsp;GB. Hosted in Dalgety Bay, Fife, on a dynamic
        address — always connect by hostname, never by IP.
      </p>
    </div>
  </div>
</div>


<section id="connect">
  <div class="wrap sec">
    <div class="sec-head">
      <h2>Three ways in</h2>
      <p>Pick one. They all land on the same network.</p>
    </div>
    <div class="cards">
      <div class="card lead">
        <h3>MeshChatX <span class="tag">easiest</span></h3>
        <p>One app for messaging, files, voice and pages, and it manages its own Reticulum
           config. Windows, macOS, Linux, Android.</p>
        <ul class="steps">
          <li><b>1</b><span>Download it and open it</span></li>
          <li><b>2</b><span>Interfaces → Add Interface → TCPClientInterface</span></li>
          <li><b>3</b><span>Host <code>rns.scotmesh.net</code>, port <code>4242</code>, save, restart</span></li>
        </ul>
        <p>The interface comes up within seconds and announces start arriving straight away.</p>
      </div>
      <div class="card">
        <h3>Config file <span class="tag">already running</span></h3>
        <p>Add this to the <code>[interfaces]</code> section of <code>~/.reticulum/config</code>,
           restart, then check with <code>rnstatus</code>.</p>
<pre>[[ScotMesh Backbone]]
  type = TCPClientInterface
  enabled = yes
  target_host = rns.scotmesh.net
  target_port = 4242</pre>
        <p>Nothing to approve and no key exchange — that is what Reticulum does by default.</p>
      </div>
      <div class="card">
        <h3>I2P <span class="tag">behind CGNAT</span></h3>
        <p>No port forwarding at either end. Needs a local I2P router with SAMv3 on;
           <code>apt install i2pd</code> is enough.</p>
<pre>[[ScotMesh I2P]]
  type = I2PInterface
  enabled = yes
  peers = a3pswrtvpuro62ijhb7…b32.i2p</pre>
        <p>Give it a few minutes on first start: I2P builds tunnels before the interface
           comes up, so it sits as <b>Down</b> for a while. That is normal, not a fault —
           <a href="https://wiki.scotmesh.net/wiki/Access_over_I2P" target="_blank" rel="noopener">more on the wiki</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="alt" id="addresses">
  <div class="wrap sec">
    <div class="sec-head">
      <h2>Addresses</h2>
      <p>Everything this node runs. Most clients find these by announce anyway.</p>
    </div>
    <div class="scroller">
      <table>
        <thead><tr><th>Service</th><th>Address</th><th>Use it with</th></tr></thead>
        <tbody>__ADDRESSES__</tbody>
      </table>
    </div>
  </div>
</section>

<section id="radio">
  <div class="wrap sec">
    <div class="sec-head">
      <h2>ScotMesh 868</h2>
      <p>One profile. Every radio must match all five exactly.</p>
    </div>
    <div class="profile">__RADIO__</div>
    <p class="warn">
      <b>A radio that differs on any one of these is not weakly connected — it is deaf,
      and nothing reports an error.</b> The first gateway runs at Cadham in Fife, carrying
      869.4625 MHz into the backbone. Coverage is local to that mast today; build to these
      settings and your radio joins the moment it is in range of one.
    </p>
    <div class="cards" style="margin-top:22px; grid-template-columns: repeat(2, minmax(0,1fr))">
      <div class="card lead">
        <h3>Flash a radio <span class="tag">in the browser</span></h3>
        <p>Chrome or Edge on a desktop and a USB cable — the ScotMesh Flasher does the rest.
           An <b>RNode</b> for a computer or phone, where the app you connect it to sets the
           radio profile.</p>
        <p style="margin-top:auto"><a class="btn btn-primary" href="https://rnode.scotmesh.net/" target="_blank" rel="noopener">Open the Flasher</a></p>
      </div>
      <div class="card">
        <h3>Build a standalone node</h3>
        <p>The same flasher builds a <b>microReticulum node</b>: a self-contained transport
           node for a solar box or a hilltop, provisioned with the ScotMesh profile, a name
           and your management identity.</p>
        <p>Boards, Bluetooth pairing and the config-file form of these settings are on the
           <a href="https://wiki.scotmesh.net/wiki/RNode" target="_blank" rel="noopener">RNode page</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="alt" id="peers">
  <div class="wrap sec">
    <div class="sec-head">
      <h2>Who we peer with</h2>
      <p>Whose infrastructure your traffic transits. Link state is what this node sees now.</p>
    </div>
    <div class="scroller">
      <table>
        <thead><tr><th>Peer</th><th>Transport</th><th>Location</th><th>Link</th></tr></thead>
        <tbody>__PEERS__</tbody>
      </table>
    </div>
    <p class="warn" style="border-left-color: var(--accent)">
      <b>Want to peer with us?</b> Point a <code>TCPClientInterface</code> at
      <code>rns.scotmesh.net:4242</code>, or use the I2P address, then say so on Discord or
      in the <code>scotmesh</code> room so we can peer back. A transport node relays only
      encrypted traffic and cannot read what passes through it — peering costs you a config
      line and nothing else. UK and Irish links especially welcome.
    </p>
  </div>
</section>
</main>

<footer>
  <div class="wrap foot-grid">
    <div>
      <a class="lockup-scotmesh" href="https://scotmesh.net/" aria-label="ScotMesh, all networks">__SM_DARK____SM_LIGHT__</a>
      <p style="margin:12px 0 0; max-width:34ch">
        Reticulum is one of three networks ScotMesh runs across Scotland, alongside
        MeshCore and Meshtastic. Community-run, open to anyone.
      </p>
    </div>
    <div>
      <span class="lbl">Reticulum</span>
      <ul>
        <li><a href="https://reticulum.network/manual/" target="_blank" rel="noopener">Reticulum manual</a></li>
        <li><a href="https://rnode.scotmesh.net/" target="_blank" rel="noopener">ScotMesh Flasher</a></li>
        <li><a href="https://wiki.scotmesh.net/wiki/Known_bugs_and_workarounds" target="_blank" rel="noopener">Known bugs</a></li>
        <li><a href="/status.json">status.json</a></li>
      </ul>
    </div>
    <div>
      <span class="lbl">Community</span>
      <ul>
        <li><a href="https://scotmesh.uk/" target="_blank" rel="noopener">Main site &amp; forum</a></li>
        <li><a href="https://wiki.scotmesh.net/" target="_blank" rel="noopener">Community wiki</a></li>
        <li><a href="https://discord.gg/ytxfyuDmSt" target="_blank" rel="noopener">Discord</a></li>
      </ul>
    </div>
    <div>
      <span class="lbl">Networks</span>
      <ul>
        <li><a href="https://meshcore.scotmesh.net/" target="_blank" rel="noopener">MeshCore in Scotland</a></li>
        <li><a href="https://meshtastic.scotmesh.net/" target="_blank" rel="noopener">Meshtastic in Scotland</a></li>
        <li><a href="https://rns.scotmesh.net/" target="_blank" rel="noopener">Reticulum in Scotland</a></li>
      </ul>
    </div>
    <div class="foot-bar">
      <span>Reticulum in Scotland, part of <a href="https://scotmesh.net/">ScotMesh</a></span>
      <span class="mono">Peer locations from IP geolocation &mdash; indicative only</span>
    </div>
  </div>
</footer>

<script>
  (function () {
    var root = document.documentElement;
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    function current() {
      var set = root.getAttribute('data-theme');
      if (set === 'light' || set === 'dark') return set;
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    function label() {
      btn.setAttribute('aria-label', current() === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    }
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('rns-theme', next); } catch (e) { /* not fatal */ }
      label();
    });
    label();
  })();
</script>
'''

radio_html = ''.join('<div class="val"><div class="k">%s</div><div class="v">%s</div></div>' % kv for kv in RADIO)

body = BODY
for token, value in (('__DARK__', lock['dark']), ('__LIGHT__', lock['light']),
                     ('__SM_DARK__', sm['dark']), ('__SM_LIGHT__', sm['light']),
                     ('__FIGURE__', paths_figure()), ('__ADDRESSES__', rows_addresses()),
                     ('__PEERS__', rows_peers()), ('__RADIO__', radio_html)):
    assert token in body, token
    body = body.replace(token, value)
page = HEAD + body
pathlib.Path('page.html').write_text(page)
print('written %.0f KB' % (len(page) / 1024))
