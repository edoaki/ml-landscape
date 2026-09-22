/* Offline teaching examples: keyword retrieval and templates, no model inference. */
(() => {
  const $ = id => document.getElementById(id);
  if (!$('language-retrieval')) return;
  const questions = {
    reception: {words: ['見学会', '受付'], field: 'reception', label: '受付時刻'},
    place: {words: ['見学会', '会場'], field: 'place', label: '会場'},
    contact: {words: ['見学会', '電話番号'], field: 'contact', label: '電話番号'}
  };
  function retrieve() {
    const time = $('language-time').value;
    const eventText = `見学会の受付は${time}から。会場は工学部3号館。`;
    $('language-doc-event').textContent = '資料A｜' + eventText;
    $('language-doc-event').classList.toggle('language-excluded', !$('language-include').checked);
    const docs = [
      ...($('language-include').checked ? [{id: 'A', text: eventText, event: true, reception: time, place: '工学部3号館'}] : []),
      {id: 'B', text: '図書館の受付は9時から。貸出は学生証で手続き。'},
      {id: 'C', text: '食堂の営業時間は11時から14時まで。'}
    ];
    const q = questions[$('language-question').value];
    const hits = docs.map(d => ({...d, score: q.words.filter(w => d.text.includes(w)).length}))
      .filter(d => d.score > 0).sort((a, b) => b.score - a.score || a.id.localeCompare(b.id));
    $('language-hits').textContent = hits.length ? hits.map(d => `資料${d.id}（${d.score}語一致）`).join('、') : '一致する資料がありません。';
    const first = hits[0];
    let answer = 'この検索結果からは答えられません。';
    let reading = '必要な資料が検索対象にありません。見学会の案内を含めて、もう一度比べてください。';
    if (first && !first.event) reading = '「受付」は一致しますが、これは図書館の資料です。見学会の時刻として使うと誤りになります。';
    if (first?.event) {
      if (first[q.field]) {
        answer = q.field === 'reception' ? `見学会の受付は${first.reception}からです。[資料A]` : `見学会の会場は${first.place}です。[資料A]`;
        reading = `質問の「${q.words.join('」「')}」と一致する資料Aを採用しました。`;
      } else {
        answer = '見学会の案内に電話番号の記載がないため、答えられません。[資料A]';
        reading = '関連する資料は取れましたが、質問された項目がありません。検索成功だけでは回答を保証できません。';
      }
    }
    $('language-rag-answer').textContent = answer;
    $('language-rag-reading').textContent = reading;
  }
  ['language-question', 'language-include', 'language-time'].forEach(id => $(id).addEventListener('change', retrieve));
  document.querySelectorAll('.language-demo select, .language-demo input').forEach(el => { el.disabled = false; });
  retrieve();
})();
