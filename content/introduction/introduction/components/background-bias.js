(() => {
  const demo = document.querySelector('#background-demo');
  if (!demo) return;
  const labels = {cat: '猫', dog: '犬', indoor: '室内', outdoor: '屋外'};
  let animal = 'cat', scene = 'indoor';
  function update() {
    demo.querySelectorAll('[data-animal]').forEach(n => n.style.display = n.dataset.animal === animal ? '' : 'none');
    demo.querySelectorAll('[data-scene]').forEach(n => n.style.display = n.dataset.scene === scene ? '' : 'none');
    demo.querySelectorAll('[data-select-animal]').forEach(n => n.setAttribute('aria-pressed', String(n.dataset.selectAnimal === animal)));
    demo.querySelectorAll('[data-select-scene]').forEach(n => n.setAttribute('aria-pressed', String(n.dataset.selectScene === scene)));
    const input = `${labels[scene]}の${labels[animal]}`;
    demo.querySelector('[data-bias-scene]').setAttribute('aria-label', input);
    demo.querySelector('[data-bias-label]').textContent = `入力：${input}`;
    demo.querySelector('[data-shape-result]').textContent = `${labels[animal]} · 正解`;
    const prediction = scene === 'indoor' ? 'cat' : 'dog';
    const correct = prediction === animal;
    const result = demo.querySelector('[data-background-result]');
    result.textContent = `${labels[prediction]} · ${correct ? '正解' : '不正解'}`;
    result.dataset.incorrect = String(!correct);
    demo.querySelector('[data-bias-explanation]').textContent = correct
      ? `${input}では、どちらの判断も正解します。これだけでは、何を手がかりにしたか分かりません。`
      : `${input}でも、動物は${labels[animal]}のままです。背景だけに頼る判断は「${labels[prediction]}」と間違えます。`;
  }
  demo.querySelectorAll('[data-select-animal]').forEach(button => button.addEventListener('click', () => { animal = button.dataset.selectAnimal; update(); }));
  demo.querySelectorAll('[data-select-scene]').forEach(button => button.addEventListener('click', () => { scene = button.dataset.selectScene; update(); }));
  update();
  demo.querySelector('.intro-bias-controls').hidden = false;
  demo.querySelector('.intro-bias-static').hidden = true;
})();
