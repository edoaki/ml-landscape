(() => {
  // A single audible example at a time, including native controls.
  document.querySelectorAll('audio').forEach(audio => {
    audio.addEventListener('play', () => {
      document.querySelectorAll('audio').forEach(other => { if (other !== audio) other.pause(); });
    });
  });
  document.querySelectorAll('[data-audio-switch]').forEach(panel => {
    const audio = panel.querySelector('audio');
    const status = panel.querySelector('[role="status"]');
    const labels = {mix: '曲全体', melody: '旋律だけ', backing: '伴奏だけ'};
    const details = {mix: '旋律と伴奏が重なっています。', melody: '高い音が上下する旋律です。', backing: '低い音が繰り返される伴奏です。'};
    let revision = 0;
    panel.querySelectorAll('button[data-track]').forEach(button => {
      button.addEventListener('click', () => {
        if (button.getAttribute('aria-pressed') === 'true') return;
        const position = audio.currentTime;
        const playing = !audio.paused;
        const version = ++revision;
        const track = button.dataset.track;
        audio.pause();
        panel.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
        audio.setAttribute('aria-label', '切り替え試聴：' + labels[track]);
        status.textContent = labels[track] + '：' + details[track];
        audio.src = new URL('assets/audio-score-' + track + '.wav', new URL(document.body.dataset.siteRoot + "/", document.baseURI)).href;
        audio.addEventListener('loadedmetadata', () => {
          if (version !== revision) return;
          audio.currentTime = Math.min(position, Math.max(0, audio.duration - .01));
          if (playing) audio.play().catch(() => { status.textContent = '再生ボタンを押すと、選んだ音を聞けます。'; });
        }, {once: true});
        audio.load();
      });
    });
    audio.addEventListener('error', () => { status.textContent = '音声を読み込めませんでした。ページを再読み込みしてください。'; });
  });
})();
