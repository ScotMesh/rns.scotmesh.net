/* Live state for rns.scotmesh.net.
 *
 * The page ships with the last known figures in the HTML, so it reads correctly
 * before this runs and still reads correctly if status.json is stale or gone.
 * Everything here replaces those values in place.
 *
 * status.json is rewritten every two minutes by scotmesh-rns-status.timer.
 */
(function () {
  'use strict';

  var SRC = '/status.json';
  var REFRESH = 120000;

  function el(id) { return document.getElementById(id); }

  function setStat(name, value) {
    var v = document.querySelector('[data-stat="' + name + '"] .stat-v');
    if (v) v.textContent = value;
  }

  /* Uptime as the largest unit that still says something useful: days once
   * there are any, hours before that. A transport node that has been up for
   * weeks should not be reported in hours. */
  function uptime(seconds) {
    if (!seconds || seconds < 0) return '—';
    var d = Math.floor(seconds / 86400);
    if (d >= 1) return d + 'd';
    var h = Math.floor(seconds / 3600);
    if (h >= 1) return h + 'h';
    return Math.max(1, Math.floor(seconds / 60)) + 'm';
  }

  function apply(d) {
    var online = d.online !== false;

    var chip = el('c-online');
    if (chip) {
      var dot = chip.querySelector('.dot');
      if (dot) dot.className = online ? 'dot' : 'dot off';
      var word = chip.querySelector('b');
      if (word) word.textContent = online ? 'Online' : 'Offline';
    }

    var clients = typeof d.clients === 'number' ? d.clients : null;
    if (clients !== null) {
      setStat('clients', String(clients));
      if (el('s-clients')) el('s-clients').textContent = String(clients);
    }

    var up = uptime(d.transport_uptime_s);
    setStat('uptime', up);
    if (el('s-uptime')) el('s-uptime').textContent = up;

    var services = d.services || {};
    var names = Object.keys(services);
    var running = names.filter(function (k) { return services[k]; }).length;
    if (names.length && el('s-services')) {
      el('s-services').textContent = running + '/' + names.length;
    }

    var peers = d.peers || {};
    var hosts = Object.keys(peers);
    var linked = hosts.filter(function (h) { return peers[h]; }).length;
    if (hosts.length) setStat('peers', linked + '/' + hosts.length);

    // Each row carries the key status.json uses, so a renamed peer simply keeps
    // the figure the page shipped with rather than showing the wrong state.
    document.querySelectorAll('tr[data-peer]').forEach(function (row) {
      var host = row.getAttribute('data-peer');
      if (!(host in peers)) return;
      var cell = row.querySelector('.link-state');
      if (!cell) return;
      cell.innerHTML = peers[host]
        ? '<span class="up"><span class="dot"></span>Linked</span>'
        : '<span class="down"><span class="dot off"></span>Down</span>';
    });
  }

  function load() {
    fetch(SRC + '?t=' + Date.now(), { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error(r.status)); })
      .then(apply)
      .catch(function () { /* keep the figures the page shipped with */ });
  }

  load();
  setInterval(load, REFRESH);
})();
