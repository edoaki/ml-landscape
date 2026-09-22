// Browse the original notebook results in temporal order.
document.querySelectorAll('.spatial-frame-viewer').forEach(viewer => {
  const frames = [0, 30, 60, 90, 120, 150, 180];

  const previous = viewer.querySelector('[data-frame-step="-1"]');
  const next = viewer.querySelector('[data-frame-step="1"]');
  let index = 0;
  function move(step) {
    index = Math.max(0, Math.min(frames.length - 1, index + step));
    const frame = frames[index];
    viewer.querySelectorAll('[data-frame-kind]').forEach(panel => {
      const input = panel.dataset.frameKind === 'input';
      const src = `assets/sam2-${input ? 'input' : 'track'}-${frame}.${input ? 'jpg' : 'png'}`;
      const image = panel.querySelector('img');
      image.src = src;
      image.alt = `SAM 2の${input ? '元画像' : '推論結果'}、frame ${frame}。`;
      panel.querySelectorAll('a').forEach(link => { link.href = src; });
      panel.querySelector('.frame-caption').textContent = `frame ${frame}`;
    });
    viewer.querySelector('.frame-status').textContent = `${index + 1} / ${frames.length} · frame ${frame}`;
    previous.disabled = index === 0;
    next.disabled = index === frames.length - 1;
  }
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  viewer.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    move(event.key === 'ArrowLeft' ? -1 : 1);
  });
});
