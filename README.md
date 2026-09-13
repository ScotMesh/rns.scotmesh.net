![ScotMesh](https://raw.githubusercontent.com/ScotMesh/branding/main/social/readme-header.png)

# rns.scotmesh.net

Source for [rns.scotmesh.net](https://rns.scotmesh.net/). Static HTML served by nginx, no build step.

Deploy by copying everything except this README and `.git` into the site's web root.

`status.json` is not in this repo. It is written on the server every 2 minutes from `rnstatus -j` and systemd, and the page reads it from its own origin (scotmesh.net reads it cross-origin, so keep CORS open on it).

Brand assets (logo, colours, fonts) come from [ScotMesh/branding](https://github.com/ScotMesh/branding).
