"""Turn the artifact page into the document served at rns.scotmesh.net.

Two differences from the artifact, and no others: the artifact host supplies the
document skeleton and we must supply our own, and the site self-hosts its fonts
rather than pulling them from Google — which is how the current site already
works, and one less third party between a reader and a page about privacy.
"""
import pathlib, re
import seo

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

# the artifact's <title> is a gallery name; seo.head() supplies the site's own
page = re.sub(r'<title>.*?</title>\s*', '', page, count=1)

PRELOADS = '''<link rel="preload" href="/fonts/ibm-plex-mono-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ibm-plex-sans-condensed-400.woff2" as="font" type="font/woff2" crossorigin>
'''
HEAD_EXTRA = seo.head('rns', extra=PRELOADS)

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
root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'index.html'
out.write_text(doc)
(root / 'robots.txt').write_text(seo.robots('rns', disallow=['/status.json']))
(root / 'sitemap.xml').write_text(seo.sitemap('rns'))
print('wrote %s (%.0f KB)' % (out.name, len(doc) / 1024))
