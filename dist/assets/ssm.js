// SSM recurrence: one clock drives every moving element, so pause/reset are exact.
(() => {
  document.querySelectorAll('.ssm-animation').forEach(panel => {
    const q = selector => panel.querySelector(selector);
    const groups = Object.fromEntries(['prev','input','a-term','b-term','state','output','new-input','wires','sum'].map(key=>[key,q('.ssm-'+key)]));
    const saved = [...panel.querySelectorAll('.ssm-saved-output')];
    const play=q('.ssm-play'), next=q('.ssm-next'), reset=q('.ssm-reset'), status=q('.ssm-status');
    const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    const phaseMs=1400, phases=5, steps=3, total=phaseMs*phases*steps;
    let elapsed=0, running=false, frame=0, lastTime=null, lastStatus='';
    const sub=n=>String(n).replace(/\d/g,d=>'₀₁₂₃₄₅₆₇₈₉'[d]);
    const opacity=(key,value)=>{groups[key].style.opacity=String(value);};
    const label=(key,value)=>{groups[key].querySelector('text').textContent=value;};
    const move=(key,x=0,y=0)=>{groups[key].style.transform=`translate(${x}px, ${y}px)`;};
    const render=()=>{
      const done=elapsed>=total;
      const step=done?steps-1:Math.floor(elapsed/(phaseMs*phases));
      const local=done?phases:(elapsed%(phaseMs*phases))/phaseMs;
      const phase=Math.min(4,Math.floor(local));
      const t=step+1;
      const shift=phase===4?(reduced.matches?1:Math.max(0,Math.min(1,local-4))):0;
      const smooth=shift*shift*(3-2*shift);
      label('prev','h'+sub(t-1));label('input','x'+sub(t));label('state','h'+sub(t));label('output','y'+sub(t));label('new-input','x'+sub(t+1));
      label('a-term','Āh'+sub(t-1));label('b-term','B̄x'+sub(t));
      for(const key of ['prev','input','a-term','b-term','state','output','new-input','wires','sum'])move(key);
      opacity('prev',1-smooth);opacity('input',1-smooth);opacity('wires',1-smooth);
      opacity('a-term',phase===1?1:0);opacity('b-term',phase===1?1:0);
      opacity('sum',phase<2?1:0);opacity('state',phase>=2?1:0);opacity('output',phase>=3?1:0);opacity('new-input',phase===4&&t<steps?smooth:0);
      // Move the actual h_t and y_t nodes; they become the next state and saved output.
      move('state',-340*smooth,0);
      move('output',(-246+step*120)*smooth,-145*smooth);
      move('new-input',0,65*(1-smooth));
      saved.forEach((node,i)=>{node.style.opacity=String(i<step?1:0);});
      const messages=[
        `入力 x${sub(t)} と前の状態 h${sub(t-1)} を受け取る。`,
        `Āh${sub(t-1)} と B̄x${sub(t)} を計算する。`,
        `二つを足して、新しい状態 h${sub(t)} を作る。`,
        `Cを掛け、y${sub(t)} = Ch${sub(t)} を読み出す。`,
        t<steps?`y${sub(t)}を上へ送り、h${sub(t)}を左へ引き継ぐ。下からx${sub(t+1)}が到着する。`:`y${sub(t)}を上へ送り、h${sub(t)}を左に保持する。`
      ];
      const text=done?'3ステップ完了。出力y₁・y₂・y₃がそろい、最後の状態h₃が残る。':`時刻 ${t} / ${steps} · ${phase+1} / ${phases}　${messages[phase]}`;
      if(text!==lastStatus){status.textContent=text;lastStatus=text;}
      panel.dataset.step=String(t);panel.dataset.phase=done?'complete':String(phase);
      play.textContent=running?'一時停止':done?'もう一度再生':'再生';
      play.setAttribute('aria-pressed',String(running));next.disabled=done;
    };
    const stop=()=>{running=false;cancelAnimationFrame(frame);frame=0;lastTime=null;};
    const tick=now=>{
      if(!running)return;
      if(lastTime!==null)elapsed=Math.min(total,elapsed+Math.max(0,now-lastTime));
      lastTime=now;
      if(elapsed>=total)stop();
      render();
      if(running)frame=requestAnimationFrame(tick);
    };
    play.addEventListener('click',()=>{
      if(running)stop();
      else{if(elapsed>=total)elapsed=0;running=true;lastTime=null;frame=requestAnimationFrame(tick);}
      render();
    });
    next.addEventListener('click',()=>{stop();elapsed=Math.min(total,(Math.floor(elapsed/phaseMs)+1)*phaseMs);render();});
    reset.addEventListener('click',()=>{stop();elapsed=0;render();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden&&running){stop();render();}});
    q('.ssm-controls').hidden=false;render();
  });
})();
