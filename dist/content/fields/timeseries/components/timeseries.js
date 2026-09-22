(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('ts-data').textContent);
  const forecast = document.getElementById('ts-forecast');
  const sensor = document.getElementById('ts-sensor');
  const method = document.getElementById('ts-method');
  const reveal = document.getElementById('ts-reveal');
  const event = document.getElementById('ts-event');
  const threshold = document.getElementById('ts-threshold');
  let visible = false;
  function points(values, start = 0, count = 48, low = 0, high = 100) {
    return values.map((v, i) => `${54 + (i + start) * 650 / (count - 1)},${222 - (v - low) * 174 / (high - low)}`).join(' ');
  }
  function drawForecast() {
    const prediction = method.value === 'seasonal' ? data.history : Array(24).fill(data.history[23]);
    forecast.querySelector('[data-line="prediction"]').setAttribute('points', points(prediction, 24));
    forecast.querySelector('[data-line="truth"]').setAttribute('points', visible ? points(data.future, 24) : '');
    const mae = data.future.reduce((total, v, i) => total + Math.abs(v - prediction[i]), 0) / 24;
    forecast.querySelector('.ts-status').textContent = visible
      ? `今日の24時間のMAE：${mae.toFixed(1)} kW。${method.value === 'seasonal' ? '一日の山と谷は追えていますが、今日は全体に少し高めです。' : '36 kWを予測し続けるため、昼や夕方の大きな需要を捉えられません。'}`
      : '今日の実測はまだ隠れています。夕方の山を予測できそうでしょうか。';
    reveal.textContent = visible ? '今日の実測を隠す' : '今日の実測を表示';
    reveal.setAttribute('aria-pressed', String(visible));
  }
  function drawSensor() {
    const values = data.sensor.map((v, i) => v + ((event.value === 'spike' && i === 12) || (event.value === 'shift' && i >= 12) ? 20 : 0));
    const limit = Number(threshold.value);
    const alarms = values.map((v, i) => Math.abs(v - 50) > limit ? i : -1).filter(i => i >= 0);
    sensor.querySelector('[data-line="sensor"]').setAttribute('points', points(values, 0, 24, 40, 80));
    const marks = sensor.querySelector('[data-marks]');
    marks.replaceChildren();
    alarms.forEach(i => {
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', 54 + i * 650 / 23);
      circle.setAttribute('cy', 222 - (values[i] - 40) * 174 / 40);
      circle.setAttribute('r', 6);
      circle.setAttribute('fill', 'white');
      circle.setAttribute('stroke', '#b44437');
      circle.setAttribute('stroke-width', 3);
      marks.append(circle);
    });
    document.getElementById('ts-threshold-value').textContent = `${limit} ℃`;
    sensor.querySelector('.ts-status').textContent = `警報：${alarms.length} / 24点。` + (alarms.length ? `${alarms.map(i => i + 1).join('・')}時間目で、50℃との差が${limit}℃を超えています。` : `50℃との差が${limit}℃を超える観測はありません。`);
  }
  method.addEventListener('change', drawForecast);
  reveal.addEventListener('click', () => { visible = !visible; drawForecast(); });
  event.addEventListener('change', drawSensor);
  threshold.addEventListener('input', drawSensor);
  document.querySelectorAll('.ts-controls').forEach(control => { control.hidden = false; });
  drawForecast();
  drawSensor();
})();
