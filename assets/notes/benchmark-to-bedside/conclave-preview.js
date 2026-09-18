(() => {
  const trigger = document.getElementById('conclave-preview-trigger');
  const preview = document.getElementById('conclave-preview');
  if (!trigger || !preview) return;
  let closeTimer;
  const clearClose = () => window.clearTimeout(closeTimer);
  const hide = () => { clearClose(); preview.hidden = true; };
  const position = () => {
    if (preview.hidden) return;
    const anchor = trigger.getBoundingClientRect();
    const width = document.documentElement.clientWidth;
    const height = window.innerHeight;
    const margin = 16;
    const gap = 8;
    if (anchor.bottom < 0 || anchor.top > height) { hide(); return; }
    const below = Math.max(0, height - anchor.bottom - margin - gap);
    const above = Math.max(0, anchor.top - margin - gap);
    const placeBelow = below >= preview.scrollHeight || below >= above;
    preview.style.maxHeight = `${Math.max(1, placeBelow ? below : above)}px`;
    const card = preview.getBoundingClientRect();
    const top = placeBelow ? anchor.bottom + gap : anchor.top - card.height - gap;
    preview.style.left = `${Math.max(margin, Math.min(anchor.left, width - card.width - margin))}px`;
    preview.style.top = `${Math.max(margin, Math.min(top, height - card.height - margin))}px`;
  };
  const show = () => { clearClose(); preview.hidden = false; position(); };
  const scheduleClose = () => {
    clearClose();
    closeTimer = window.setTimeout(() => {
      if (!trigger.matches(':hover, :focus') && !preview.matches(':hover')) hide();
    }, 140);
  };
  trigger.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') show(); });
  trigger.addEventListener('pointerleave', scheduleClose);
  trigger.addEventListener('focus', show);
  trigger.addEventListener('blur', scheduleClose);
  preview.addEventListener('pointerenter', clearClose);
  preview.addEventListener('pointerleave', scheduleClose);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !preview.hidden) { hide(); event.preventDefault(); }
  });
  window.addEventListener('resize', position);
  window.addEventListener('scroll', position, { passive: true, capture: true });
})();
