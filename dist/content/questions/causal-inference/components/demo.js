'use strict';
(() => {
  const root = document.querySelector('#causal-demo');
  if (!root) return;
  const steps = {
    raw: {
      heading: '1. 実際の参加者と不参加者を、そのまま比べる',
      explanation: '補習ありには基礎に不安がある学生が80人、なしには20人います。人数の構成が違うまま、全体の合格率を計算しています。',
      status: '58% − 70% = −12ポイント。補習ありのほうが低く見えますが、参加前の学力構成も違います。次に「2. 学力別に比べる」で、同じ学力層どうしを比べます。',
      counts: [80, 20]
    },
    strata: {
      heading: '2. どちらの学力層でも、補習ありの合格率が高い',
      explanation: '全体を一度に比べず、参加前の学力が同じ層の学生どうしで比べます。下の四つの合格率は、元の表のままです。',
      status: '基礎に不安がある層では＋20ポイント、習得済みの層では＋10ポイント。全体の−12ポイントとは向きが逆です。次に「3. 同じ構成で比べる」で、人数の偏りをそろえて平均します。'
    },
    adjusted: {
      heading: '3. 両グループを「各学力層50人ずつ」として計算する',
      explanation: '手順2の合格率は変えず、計算に使う人数を両方とも50人ずつにします。実際の合格者数ではなく、同じ学力構成なら何人合格するかの見積もりです。',
      status: '70% − 55% = ＋15ポイント。学力別の合格率を変えなくても、構成をそろえると比較結果が変わりました。学力以外の交絡を見落としていないなどの仮定のもとで、この差を補習の効果と解釈します。',
      counts: [50, 50]
    }
  };
  function show(mode) {
    const step = steps[mode];
    root.querySelector('[data-heading]').textContent = step.heading;
    root.querySelector('[data-explanation]').textContent = step.explanation;
    root.querySelector('[role="status"]').textContent = step.status;
    root.querySelector('[data-summary]').hidden = mode === 'strata';
    root.querySelector('[data-strata]').hidden = mode !== 'strata';
    if (step.counts) {
      const withinRates = [[50, 90], [30, 80]];
      ['treated', 'untreated'].forEach((key, i) => {
        const low = step.counts[i], high = 100 - low;
        const [lowRate, highRate] = withinRates[i];
        const rate = Math.round((low * lowRate + high * highRate) / 100);
        root.querySelector(`[data-count="${key}"]`).textContent = `基礎に不安：${low}人 ／ 習得済み：${high}人`;
        root.querySelector(`[data-mix="${key}"]`).style.width = low + '%';
        root.querySelector(`[data-formula="${key}"]`).textContent = `${low}人 × ${lowRate}% ＋ ${high}人 × ${highRate}%\n= ${mode === 'adjusted' ? '合格の見積もり' : '合格'}${rate}人／100人`;
        root.querySelector(`[data-rate="${key}"]`).textContent = rate + '%';
        root.querySelector(`[data-bar="${key}"]`).style.width = rate + '%';
      });
      root.querySelector('[data-result-label]').textContent = mode === 'adjusted' ? '共通の構成で計算した合格率' : '実際に観測された合格率';
    }
    root.querySelectorAll('[data-mode]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
    });
  }
  root.querySelectorAll('[data-mode]').forEach(button => {
    button.addEventListener('click', () => show(button.dataset.mode));
  });
  root.querySelector('.ld-controls').hidden = false;
})();
