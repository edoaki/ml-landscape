(() => {
  const root = document.querySelector('.fa-demo');
  if (!root) return;
  const normal = root.querySelector('[data-method="normal"]');
  const flash = root.querySelector('[data-method="flash"]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let step = 0;
  let timer = null;
  const stop = () => { clearTimeout(timer); timer = null; };
  let visible = false;
  const status = (panel, value) => { panel.querySelector('.fa-status').textContent = value; };
  const output = (panel, value, done) => {
    const node = panel.querySelector('.fa-output');
    node.textContent = value;
    node.classList.toggle('done', done);
  };
  function render() {
    const block = Math.ceil(step / 2);
    const calculating = step > 0 && step < 7 && step % 2 === 1;
    const saved = Math.min(3, Math.floor(step / 2));
    normal.querySelectorAll('.fa-block').forEach((node, i) => {
      node.classList.toggle('filled', i < saved);
      node.classList.toggle('active', calculating && i === block - 1);
    });
    normal.querySelector('.fa-transfer').classList.toggle('active', step === 7);
    flash.querySelector('.fa-transfer').classList.toggle('active', step > 0 && step <= 6 && !calculating);
    flash.querySelector('.fa-tile').classList.toggle('active', calculating);
    flash.querySelector('.fa-tile').textContent = calculating ? `▦ ${block}` : '空き';
    flash.querySelector('.fa-tile-label').textContent = calculating ? `範囲${block}を計算中` : '次の範囲に使い回せる';
    output(normal, step === 8 ? '出力が完成' : '出力はまだ未計算', step === 8);
    output(flash, saved === 3 ? '出力が完成' : saved ? `${saved}/3 の範囲を反映した途中結果` : '出力の準備', saved === 3);
    if (step === 0) {
      status(normal, 'これから全組合せの関連度・重みを計算。');
      status(flash, '同じ組合せを、小分けに計算。');
    } else if (step <= 6) {
      status(normal, calculating ? `範囲${block}の関連度・重みを計算。` : `範囲${block}の表を保存。前の表も残す。`);
      status(flash, calculating ? `範囲${block}の関連度・重みを高速メモリで計算。` : `範囲${block}を出力に反映。途中結果の倍率を補正し、表は破棄。`);
    } else {
      status(normal, step === 7 ? '保存した表全体を読み戻して、情報を重み付けして集める。' : '表の保存・読み戻しを経て、出力が完成。');
      status(flash, 'すべての範囲を反映済み。大きな表の読み戻しは不要。');
    }
    root.dataset.step = String(step);
  }
  function running() {
    return visible && !document.hidden && !reduced.matches &&
      !(root.closest('details') && !root.closest('details').open);
  }
  function schedule() {
    stop();
    if (!running()) return;
    timer = setTimeout(() => {
      step = (step + 1) % 9;
      render();
      schedule();
    }, step === 8 ? 1800 : 850);
  }
  function sync() {
    if (reduced.matches) { step = 8; render(); }
    schedule();
  }
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    sync();
  }, { threshold: 0 }).observe(root);
  for (let parent = root.parentElement; parent; parent = parent.parentElement) {
    if (parent.tagName === 'DETAILS') parent.addEventListener('toggle', sync);
  }
  document.addEventListener('visibilitychange', sync);
  reduced.addEventListener('change', sync);
  render();
})();
