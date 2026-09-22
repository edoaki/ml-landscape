/* Progressive enhancement: all educational states remain readable without JS. */
(() => {
  'use strict';
  document.querySelectorAll('.exp-stepper').forEach(root => {
    const stages = [...root.querySelectorAll('.exp-stage')];
    const controls = root.querySelector('.exp-controls');
    let current = 0;
    function render() {
      stages.forEach((stage, i) => { stage.hidden = i !== current; });
      controls.querySelector('[data-exp="prev"]').disabled = current === 0;
      controls.querySelector('[data-exp="next"]').disabled = current === stages.length - 1;
      controls.querySelector('.exp-counter').textContent = `${current + 1} / ${stages.length}：${stages[current].querySelector('.exp-stage-title').textContent.replace(/^\d+\. /, '')}`;
    }
    controls.addEventListener('click', event => {
      const action = event.target.closest('button')?.dataset.exp;
      if (action === 'next') current = Math.min(current + 1, stages.length - 1);
      if (action === 'prev') current = Math.max(current - 1, 0);
      if (action === 'reset') current = 0;
      if (action) render();
    });
    render();
    controls.hidden = false;
  });

  document.querySelectorAll('.exp-optimization').forEach(root => {
    const controls = root.querySelector('.exp-controls');
    const select = root.querySelector('.exp-rate');
    let points = [2];
    const number = value => Number(value.toFixed(5)).toString();
    function render() {
      const bound = Math.max(3, Math.ceil(Math.max(...points.map(Math.abs)) * 1.1));
      const xy = w => [35 + (w + bound) / (2 * bound) * 490, 215 - w * w / (bound * bound) * 175];
      const curve = Array.from({length: 101}, (_, i) => xy(-bound + i / 100 * 2 * bound).join(','));
      root.querySelector('.exp-curve').setAttribute('d', 'M ' + curve.join(' L '));
      root.querySelector('.exp-trail').setAttribute('points', points.map(w => xy(w).join(',')).join(' '));
      const w = points[points.length - 1];
      const [x, y] = xy(w);
      const dot = root.querySelector('.exp-dot');
      dot.setAttribute('cx', x); dot.setAttribute('cy', y);
      root.querySelector('.exp-xmin').textContent = `−${bound}`;
      root.querySelector('.exp-xmax').textContent = bound;
      root.querySelector('.exp-ymax').textContent = bound * bound;
      const n = points.length - 1;
      root.querySelector('.exp-result').textContent = `${n}回更新：w＝${number(w)}、損失＝${number(w * w)}。` + (n ? ` 直前の計算：${number(points[n - 1])} − ${select.value} × 2 × (${number(points[n - 1])})。` : ' 学習率を選び、1回ずつ進めてください。');
      root.querySelector('svg').setAttribute('aria-label', `横軸wは−${bound}から${bound}、縦軸損失は0から${bound * bound}。${n}回更新後のwは${number(w)}、損失は${number(w * w)}。`);
      controls.querySelector('[data-exp="next"]').disabled = n >= 8;
    }
    controls.addEventListener('click', event => {
      const action = event.target.closest('button')?.dataset.exp;
      if (action === 'next' && points.length <= 8) {
        const w = points[points.length - 1];
        points.push(w - Number(select.value) * 2 * w);
      }
      if (action === 'reset') points = [2];
      if (action) render();
    });
    select.addEventListener('change', () => { points = [2]; render(); });
    render(); controls.hidden = false;
  });

  document.querySelectorAll('.exp-abstention').forEach(root => {
    const input = root.querySelector('.exp-threshold');
    const cases = [...root.querySelectorAll('.exp-case')];
    function render() {
      const threshold = Number(input.value) / 100;
      let accepted = 0, errors = 0;
      cases.forEach(item => {
        const keep = Number(item.dataset.confidence) >= threshold;
        item.classList.toggle('exp-held', !keep);
        item.querySelector('.exp-case-state').textContent = keep ? '自動回答' : '保留';
        if (keep) { accepted++; errors += 1 - Number(item.dataset.correct); }
      });
      root.querySelector('.exp-threshold-value').textContent = `${input.value}%`;
      const rate = accepted ? `${Number((errors / accepted * 100).toFixed(1))}%（${errors}/${accepted}件）` : '計算できません（自動回答0件）';
      root.querySelector('.exp-result').textContent = `自動回答${accepted}/${cases.length}件（${accepted / cases.length * 100}%）・その中の誤り率は${rate}。保留${cases.length - accepted}件。`;
    }
    input.addEventListener('input', render);
    render(); root.querySelector('.exp-controls').hidden = false;
  });
})();
