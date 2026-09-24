"""Shared SEO head and structured data for the four ScotMesh sites."""
import json, datetime

ORG_ID = 'https://scotmesh.net/#org'
SAMEAS = ['https://scotmesh.uk/', 'https://wiki.scotmesh.uk/', 'https://discord.gg/ytxfyuDmSt',
          'https://www.facebook.com/groups/26406719398968062', 'https://www.facebook.com/groups/414401424386367',
          'https://github.com/ScotMesh']
ORG = {'@type': 'Organization', '@id': ORG_ID, 'name': 'ScotMesh', 'url': 'https://scotmesh.net/',
       'logo': {'@type': 'ImageObject', 'url': 'https://scotmesh.net/logo.png'},
       'description': 'Community-run mesh radio networks across Scotland: MeshCore, Meshtastic and Reticulum.',
       'areaServed': {'@type': 'Country', 'name': 'Scotland'}, 'sameAs': SAMEAS}

SITES = {
 'parent': dict(url='https://scotmesh.net/', name='ScotMesh', title='ScotMesh — Community Mesh Networks in Scotland',
     desc='ScotMesh is the community mesh network of Scotland: MeshCore, Meshtastic and Reticulum. What each network is, where the nodes are, live activity, and how to join.',
     og_title='ScotMesh — the community mesh networks of Scotland',
     og_desc='MeshCore, Meshtastic and Reticulum across Scotland: what each one is, where the nodes are, and how to join.',
     image='https://scotmesh.net/og.png', image_alt='ScotMesh: three meshes across Scotland, one community', theme='#0A1424',
     keywords='mesh network Scotland, MeshCore Scotland, Meshtastic Scotland, Reticulum Scotland, LoRa mesh Scotland, ScotMesh',
     about=['MeshCore', 'Meshtastic', 'Reticulum'], icons='<link rel="icon" href="/favicon.svg" type="image/svg+xml">'),
 'meshcore': dict(url='https://meshcore.scotmesh.net/', name='MeshCore in Scotland', title='MeshCore in Scotland — ScotMesh',
     desc="Scotland's MeshCore radio mesh: live map and packets, the settings that actually work here, and step-by-step guides for running a repeater or an observer.",
     og_title='MeshCore in Scotland', og_desc="Join Scotland's MeshCore mesh: the settings that work here, and how to run a repeater or an observer.",
     image='https://meshcore.scotmesh.net/og-image.png', image_alt='ScotMesh MeshCore', theme='#0A1424',
     keywords='MeshCore Scotland, MeshCore repeater Scotland, MeshCore 869.618, MeshCore scope sco, LoRa mesh Scotland, ScotMesh',
     about=['MeshCore'], icons=None),
 'meshtastic': dict(url='https://meshtastic.scotmesh.net/', name='Meshtastic in Scotland', title='Meshtastic in Scotland — ScotMesh',
     desc="Scotland's Meshtastic mesh: live nodes and packets heard today, the ScotMesh radio settings (EU_868, LongFast, hop limit 7), how to get on the air, and where the community talks.",
     og_title='Meshtastic in Scotland — The Original Scottish Mesh', og_desc="Scotland's Meshtastic network: live nodes and packets, the settings that work here, and how to get on the air.",
     image='https://meshtastic.scotmesh.net/og-image.png', image_alt='ScotMesh Meshtastic: The Original Scottish Mesh', theme='#0A1424',
     keywords='Meshtastic Scotland, Meshtastic EU_868, Meshtastic LongFast Scotland, Meshtastic nodes Scotland, LoRa mesh Scotland, ScotMesh',
     about=['Meshtastic'],
     icons='<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="/favicon.ico" sizes="32x32">\n<link rel="icon" href="/icons/favicon-32.png" sizes="32x32" type="image/png">\n<link rel="icon" href="/icons/favicon-16.png" sizes="16x16" type="image/png">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">'),
 'rns': dict(url='https://rns.scotmesh.net/', name='Reticulum in Scotland', title='Reticulum in Scotland — ScotMesh Backbone transport node',
     desc='ScotMesh Backbone: the public Reticulum transport node for Scotland. Connect over TCP (rns.scotmesh.net:4242) or I2P, no account needed; LXMF propagation, Nomad Network, chat hub and the ScotMesh 868 MHz LoRa settings.',
     og_title='Reticulum in Scotland — ScotMesh Backbone', og_desc='The public Reticulum transport node for Scotland. TCP rns.scotmesh.net:4242 or I2P, no registration, no account.',
     image='https://rns.scotmesh.net/og.png', image_alt='ScotMesh Backbone, the public Reticulum transport node for Scotland', theme='#0A1424',
     keywords='Reticulum Scotland, Reticulum transport node, RNS Scotland, LXMF propagation node, Nomad Network Scotland, RNode 868, ScotMesh',
     about=['Reticulum'], icons='<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">'),
}

def jsonld(key):
    s = SITES[key]
    site_id = s['url'] + '#website'
    graph = [ORG,
     {'@type': 'WebSite', '@id': site_id, 'url': s['url'], 'name': s['name'], 'inLanguage': 'en-GB', 'publisher': {'@id': ORG_ID}},
     {'@type': 'WebPage', '@id': s['url'] + '#webpage', 'url': s['url'], 'name': s['title'], 'description': s['desc'],
      'inLanguage': 'en-GB', 'isPartOf': {'@id': site_id},
      'about': [{'@type': 'Thing', 'name': a} for a in s['about']],
      'primaryImageOfPage': {'@type': 'ImageObject', 'url': s['image']},
      'spatialCoverage': {'@type': 'Place', 'name': 'Scotland'}}]
    if key != 'parent':
        graph[1]['isPartOf'] = {'@type': 'WebSite', '@id': 'https://scotmesh.net/#website', 'url': 'https://scotmesh.net/'}
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))

def head(key, extra=''):
    s = SITES[key]
    icons = s['icons'] or ''
    return '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="keywords" content="%(keywords)s">
<link rel="canonical" href="%(url)s">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="theme-color" content="%(theme)s">
<meta name="color-scheme" content="dark light">
<meta name="geo.region" content="GB-SCT">
<meta name="geo.placename" content="Scotland">
%(icons)s
<meta property="og:type" content="website">
<meta property="og:site_name" content="ScotMesh">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="%(og_title)s">
<meta property="og:description" content="%(og_desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(image)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%(image_alt)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(og_title)s">
<meta name="twitter:description" content="%(og_desc)s">
<meta name="twitter:image" content="%(image)s">
<meta name="twitter:image:alt" content="%(image_alt)s">
%(extra)s<script type="application/ld+json">%(ld)s</script>
''' % dict(s, icons=icons, extra=extra, ld=jsonld(key))

def robots(key, disallow=()):
    lines = ['User-agent: *', 'Allow: /'] + ['Disallow: %s' % d for d in disallow] + ['', 'Sitemap: %ssitemap.xml' % SITES[key]['url'], '']
    return '\n'.join(lines)

def sitemap(key, lastmod=None):
    lastmod = lastmod or datetime.date.today().isoformat()
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n</urlset>\n' % (SITES[key]['url'], lastmod))

def manifest(key, tint):
    s = SITES[key]
    return json.dumps({'name': s['name'], 'short_name': s['name'].split(' in ')[0], 'start_url': '/', 'display': 'browser',
                       'background_color': '#0A1424', 'theme_color': '#0A1424',
                       'icons': [{'src': '/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=1)
