(() => {
  document.querySelectorAll('[data-science-motion]').forEach(figure => {
    const button = figure.querySelector('.science-play');
    const range = figure.querySelector('.science-progress');
    let frame = null, started = 0;
    const title = button.textContent;
    function draw(value) {
      range.value = value;
      const t = Math.min(1, value / 55);
      const x = t < .5 ? 65 + 170 * t : 150 + 186 * (t - .5);
      const y = t < .5 ? 48 + 194 * t : 145 - 194 * (t - .5);
      const dot = figure.querySelector('.science-wave-dot');
      dot.setAttribute('cx', x); dot.setAttribute('cy', y);
      figure.querySelector('.science-layers').style.opacity = Math.max(0, (value - 65) / 35);
      const status = value < 55 ? '① 地下を伝わった波が、地表のセンサーに届きます。' : value < 75 ? '② 届いた揺れの記録を、AIへの入力にします。' : '③ 揺れの記録から、地下の層を推定します。';
      const text = figure.querySelector('.science-motion-status');
      if (text.textContent !== status) text.textContent = status;
    }
    function stop() {
      if (frame !== null) cancelAnimationFrame(frame);
      frame = null;
      button.textContent = title;
      button.setAttribute('aria-pressed', 'false');
    }
    function tick(now) {
      const progress = Math.min(100, (now - started) / 80);
      draw(progress);
      if (progress < 100) frame = requestAnimationFrame(tick);
      else stop();
    }
    button.addEventListener('click', () => {
      if (frame !== null) { stop(); return; }
      if (matchMedia('(prefers-reduced-motion: reduce)').matches) { draw(Number(range.value) === 100 ? 0 : 100); return; }
      started = performance.now();
      draw(0);
      button.textContent = '一時停止';
      button.setAttribute('aria-pressed', 'true');
      frame = requestAnimationFrame(tick);
    });
    range.addEventListener('input', () => { stop(); draw(Number(range.value)); });
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    figure.querySelector('.science-controls').hidden = false;
  });
})();
