![ScotMesh](https://raw.githubusercontent.com/ScotMesh/branding/main/networks/reticulum/readme-header.png)

# rns.scotmesh.net

Source for [rns.scotmesh.net](https://rns.scotmesh.net/) — the ScotMesh Backbone,
a public Reticulum transport node for Scotland. Static HTML served by nginx.

## Layout

```
index.html        the page as served — generated, do not hand-edit
app.js            replaces the shipped figures from /status.json every 2 minutes
build/build.py    the page's content and design; writes build/page.html
build/mksite.py   wraps build/page.html as index.html
fonts/, *.svg, *.png, status.html   served as-is, not generated
```

`build.py` holds the copy, the tables and the hero figure, and writes
`build/page.html`. `mksite.py` turns that into `index.html`: it adds the document
skeleton, swaps Google Fonts for the self-hosted IBM Plex in `fonts/`, and
restores the title, description, canonical, og tags and icons.

```bash
cd build && python3 build.py && python3 mksite.py
```

That reproduces `index.html` byte for byte, so a rebuild with no source change is
a no-op in `git status`.

## Deploying

Copy the two generated files — `index.html` and `app.js` — into the site's web
root on the server. The fonts, icons and `og.png` only need copying when they
change.

Nothing is built on the server: no Docker, no Node, no package installs. It is a
small box and the Reticulum daemons need the memory.

## Live data

`status.json` is not in this repo. It is written on the server every 2 minutes
from `rnstatus -j` and systemd, and the page reads it from its own origin
(scotmesh.net reads it cross-origin, so keep CORS open on it). `status.html` is
the embeddable status strip built from the same file.

It carries `online`, `clients`, `peers{host: bool}`, `i2p`, `services{rnsd, lxmd,
nomadnet, i2pd, rrc-hub}` and `transport_uptime_s`. `index.html` ships with the
last known figures so the page reads correctly before `app.js` runs, or if the
feed is stale or gone; `app.js` then replaces them in place. Peer rows carry
`data-peer` with the key `status.json` uses, so a renamed peer keeps its shipped
figure rather than showing another peer's state.

## Design

The same system as meshcore.scotmesh.net and meshtastic.scotmesh.net — brand
tokens, IBM Plex, and the network lockup in its light and dark forms, from
[ScotMesh/branding](https://github.com/ScotMesh/branding).

The hero is deliberately **not** a map. Reticulum has no geography to draw: a
destination is a hash, not a place. It shows the three transports that actually
reach this node — TCP, I2P and 868 MHz LoRa — converging on it, with announces
arriving along each.

The wiki for this site is **wiki.scotmesh.net**, not the `wiki.scotmesh.uk` the
other two ScotMesh sites use. Both hosts resolve and serve, so a wrong link fails
silently rather than 404ing.
