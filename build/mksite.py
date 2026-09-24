"""Turn the artifact page into the document served at rns.scotmesh.net.

Two differences from the artifact, and no others: the artifact host supplies the
document skeleton and we must supply our own, and the site self-hosts its fonts
rather than pulling them from Google — which is how the current site already
works, and one less third party between a reader and a page about privacy.
"""
import pathlib, re

page = (pathlib.Path(__file__).resolve().parent / 'page.html').read_text()

FONTS = '''<style>
/* IBM Plex, self-hosted — already on the box under /fonts. */
@font-face{font-family:"IBM Plex Mono";font-weight:400;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-mono-400.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Mono";font-weight:600;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-mono-600.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Sans Condensed";font-weight:400;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-sans-condensed-400.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Sans Condensed";font-weight:600;font-style:normal;font-display:swap;src:url(/fonts/ibm-plex-sans-condensed-600.woff2) format("woff2")}
</style>'''

# drop the Google Fonts link and its preconnects
page = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', page)
page = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">', FONTS, page, count=1)
assert 'fonts.googleapis.com' not in page, 'a Google Fonts reference survived'
assert '@font-face' in page

# the artifact's <title> is a gallery name; the site wants the descriptive one
page = page.replace('<title>ScotMesh Backbone</title>',
                    '<title>ScotMesh Backbone — public Reticulum transport node for Scotland</title>', 1)

HEAD_EXTRA = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="canonical" href="https://rns.scotmesh.net/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="description" content="ScotMesh Backbone: a public Reticulum transport node in Scotland. TCP rns.scotmesh.net:4242, I2P, chat hub, LXMF propagation node, Nomad Network node and the ScotMesh LoRa settings.">
<meta name="theme-color" content="#0A1424">
<meta name="color-scheme" content="dark light">
<meta property="og:title" content="ScotMesh Backbone">
<meta property="og:description" content="The public Reticulum transport node for Scotland. TCP rns.scotmesh.net:4242 or I2P, no registration, no account.">
<meta property="og:image" content="https://rns.scotmesh.net/og.png">
<meta property="og:url" content="https://rns.scotmesh.net/">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/ibm-plex-mono-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ibm-plex-sans-condensed-400.woff2" as="font" type="font/woff2" crossorigin>
'''

# the artifact skeleton pads :root by the safe-area insets; supply that here
RESET = '''<style>
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>'''

head_end = page.index('</style>') + len('</style>')
head, body = page[:head_end], page[head_end:]

doc = ('<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n' + HEAD_EXTRA + head + '\n' + RESET +
       '\n</head>\n<body>\n' + body.strip() +
       '\n<script src="/app.js" defer></script>\n</body>\n</html>\n')

# The repo is flat: the served files sit at the root, beside the fonts and
# icons that are not generated. app.js is hand-written and lives there too.
out = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
out.write_text(doc)
print('wrote %s (%.0f KB)' % (out.name, len(doc) / 1024))
