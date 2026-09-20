/* Status pill, on every page: shown only when the SAROS status feed answers; any failure leaves it hidden.
   On Home the same feed refreshes every SAROS figure. Trials, FDA actions and feeds come from `loaders`; SEC-linked issuers and
   Phase-3 dates come from `kpi` (distinct CIKs; Phase 3 primary completions 0-180 days from the build). Without the feed, the dated
   snapshot values in the markup stand. */
(function () {
  var p = document.getElementById('saros-pill'); if (!p || !window.fetch) return;
  fetch('https://saros.gcarosso.bio/status.json', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (s) {
    var d = new Date(s.built); if (isNaN(d)) return;
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getUTCMonth()];
    document.getElementById('saros-pill-text').textContent = 'SAROS updated ' + d.getUTCDate() + ' ' + m; p.hidden = false;
    var L = s.loaders || {}, t = document.getElementById('saros-trials'), f = document.getElementById('saros-feeds');
    if (t && L.trials && L.trials.rows > 0) t.textContent = L.trials.rows.toLocaleString('en-US');
    if (f && Object.keys(L).length) f.textContent = Object.keys(L).length;
    var K = s.kpi || {}, when = d.getUTCDate() + ' ' + m + ' ' + d.getUTCFullYear();
    [['saros-phase3', 'p3_180', 'Phase 3 registered primary completions within 180 days of the SAROS build of ' + when + '. Includes stopped studies, matching the dashboard denominator.'],
     ['saros-sec', 'sec_issuers', 'Distinct SEC CIK identifiers across automatic and manual sponsor mappings, SAROS build of ' + when + '.']].forEach(function (x) {
      var e = document.getElementById(x[0]); if (e && K[x[1]] > 0) { e.textContent = K[x[1]].toLocaleString('en-US'); e.title = x[2]; } });
    [['saros-fda', 'fda']].forEach(function (x) { var e = document.getElementById(x[0]), r = L[x[1]] && L[x[1]].rows; if (e && r > 0) e.textContent = r.toLocaleString('en-US'); });
  }).catch(function () {});
})();
