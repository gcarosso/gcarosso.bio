(function () {
  var dialog, opener;
  function open(trigger) {
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'example-dialog';
      dialog.setAttribute('aria-labelledby', 'example-dialog-title');
      dialog.innerHTML = '<div class="example-dialog-bar"><span id="example-dialog-title">Conclave · Example run</span><button type="button" class="example-dialog-close" aria-label="Close example run">Close ×</button></div><iframe title="Original example run viewer" src="/assets/example-run.html"></iframe>';
      document.body.appendChild(dialog);
      dialog.querySelector('button').addEventListener('click', function () { dialog.close(); });
      dialog.addEventListener('click', function (e) { if (e.target === dialog) { var r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
      dialog.addEventListener('close', function () { document.documentElement.classList.remove('example-open'); if (location.hash === '#example-run') history.replaceState(null, '', location.pathname + location.search); if (opener) opener.focus(); });
      dialog.querySelector('iframe').addEventListener('load', function () {
        this.contentDocument.addEventListener('keydown', function (e) { if (e.key === 'Escape') { e.preventDefault(); dialog.close(); } });
      });
    }
    if (dialog.open) return;
    opener = trigger || document.querySelector('[data-example-run]');
    dialog.showModal();
    document.documentElement.classList.add('example-open');
  }
  document.querySelectorAll('[data-example-run]').forEach(function (a) { a.addEventListener('click', function (e) { if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); open(a); }); });
  window.addEventListener('hashchange', function () { if (location.hash === '#example-run') open(); });
  if (location.hash === '#example-run') open();
})();
