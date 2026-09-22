// Numeric changes happen in place; every calculation remains visible.
(() => {
  document.querySelectorAll('.gnn-calc').forEach(panel => {
    const button = panel.querySelector('.gnn-replay');
    if (!button) return;
    const nodes = [...panel.querySelectorAll('[data-start][data-end]')];
    let running = false;
    button.hidden = false;
    button.addEventListener('click', () => {
      if (running) return;
      running = true; button.disabled = true;
      panel.classList.add('gnn-running');
      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const duration = reduced ? 0 : 1800;
      const started = performance.now();
      const tick = now => {
        const t = duration ? Math.min(1, (now-started)/duration) : 1;
        nodes.forEach(node => {
          const from = node.dataset.start.split(',').map(Number);
          const to = node.dataset.end.split(',').map(Number);
          node.textContent = t === 1 ? node.dataset.to : '(' + from.map((v,i) => (v+(to[i]-v)*t).toFixed(3)).join(', ') + ')';
        });
        if (t < 1) requestAnimationFrame(tick);
        else { running = false; button.disabled = false; panel.classList.remove('gnn-running'); }
      };
      requestAnimationFrame(tick);
    });
  });
})();

