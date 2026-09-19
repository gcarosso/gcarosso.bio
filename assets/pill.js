/* Status pill, on every page: shown only when the SAROS status feed answers; any failure leaves it hidden.
   On Home the same feed refreshes the SAROS figures in the numerals strip. */
(function () {
  var p = document.getElementById('saros-pill'); if (!p || !window.fetch) return;
  fetch('https://saros.gcarosso.bio/status.json', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (s) {
    var d = new Date(s.built); if (isNaN(d)) return;
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getUTCMonth()];
    document.getElementById('saros-pill-text').textContent = 'SAROS updated ' + d.getUTCDate() + ' ' + m; p.hidden = false;
    var L = s.loaders || {}, t = document.getElementById('saros-trials'), f = document.getElementById('saros-feeds');
    if (t && L.trials && L.trials.rows > 0) t.textContent = L.trials.rows.toLocaleString('en-US');
    if (f && Object.keys(L).length) f.textContent = Object.keys(L).length;
  }).catch(function () {});
})();
