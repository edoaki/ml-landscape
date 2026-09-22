(() => {
  'use strict';
  document.querySelectorAll('.exp-abstention').forEach(root => {
    const input = root.querySelector('.exp-threshold');
    const cases = [...root.querySelectorAll('.exp-case')];
    const acceptedTray = root.querySelector('.unc-accepted');
    const heldTray = root.querySelector('.unc-held-cases');
    const set = (selector, value) => { root.querySelector(selector).textContent = value; };
    function render() {
      const threshold = Number(input.value);
      let accepted = 0, errors = 0;
      cases.forEach(item => {
        const keep = Number(item.dataset.confidence) * 100 >= threshold;
        item.classList.toggle('exp-held', !keep);
        item.querySelector('.exp-case-state').textContent = keep ? '自動回答' : '保留';
        (keep ? acceptedTray : heldTray).append(item);
        if (keep) { accepted++; errors += 1 - Number(item.dataset.correct); }
      });
      const held = cases.length - accepted;
      const coverage = accepted / cases.length * 100;
      const rate = accepted ? `${Number((errors / accepted * 100).toFixed(1))}%` : '計算できません';
      set('.exp-threshold-value', `${threshold}%`);
      input.setAttribute('aria-valuetext', `${threshold}%以上なら自動回答`);
      set('.unc-rule', `確信度${threshold}%以上 → 自動回答 ／ ${threshold}%未満 → 保留`);
      set('.unc-accepted-count', `${accepted}件`);
      set('.unc-held-count', `${held}件`);
      root.querySelector('.unc-accepted-empty').hidden = accepted !== 0;
      root.querySelector('.unc-held-empty').hidden = held !== 0;
      set('.unc-coverage', `${accepted} / 全${cases.length}件 = ${coverage}%`);
      set('.unc-risk', accepted ? `誤り${errors} / 自動回答${accepted}件 = ${rate}` : '計算できません（自動回答0件）');
      set('.exp-result', `閾値${threshold}%。自動回答${accepted}/${cases.length}件（${coverage}%）・その中の誤り率は${rate}。保留${held}件。`);
      let observation;
      if (!accepted) observation = 'すべて人の確認へ回しました。自動回答が0件なので、誤り率は0%ではなく計算できません。';
      else if (threshold <= 55) observation = '10件すべてに答えると、4件の誤りもそのまま返します。';
      else if (threshold <= 95) observation = `${held}件を保留しましたが、確信度95%の写真3の誤りは残ります。確信度が高くても正しいとは限りません。`;
      else observation = 'この例では残った回答に誤りはありませんが、別のデータでも誤りがなくなる保証はありません。';
      set('.unc-observation', observation);
      root.querySelectorAll('[data-threshold]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.threshold) === threshold)));
    }
    input.addEventListener('input', render);
    root.querySelectorAll('[data-threshold]').forEach(button => button.addEventListener('click', () => {
      input.value = button.dataset.threshold;
      render();
    }));
    render();
    root.querySelector('.exp-controls').hidden = false;
  });
})();
