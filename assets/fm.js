// Discrete comic frames: pause on each prediction and each position update.
(() => {
  document.querySelectorAll('[data-comic]').forEach(d=>{
    const frames=Array.from(d.querySelectorAll('.fm-frame'));
    const q=s=>d.querySelector(s),play=q('[data-action="play"]'),prev=q('[data-action="prev"]'),next=q('[data-action="next"]');
    const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    let index=0,timer=null;
    q('.fm-controls').hidden=false;
    const render=()=>{
      frames.forEach((f,i)=>{f.hidden=i!==index;});
      prev.disabled=index===0;next.disabled=index===frames.length-1;
      q('.fm-status').textContent=`${index+1} / ${frames.length} コマ：${frames[index].querySelector('h4').textContent}`;
      play.textContent=timer===null?'自動でめくる':'一時停止';
      play.setAttribute('aria-pressed',String(timer!==null));
    };
    const stop=()=>{clearInterval(timer);timer=null;render();};
    play.addEventListener('click',()=>{
      if(timer!==null){stop();return;}
      if(index===frames.length-1)index=0;
      if(reduced.matches){index=Math.min(frames.length-1,index+1);render();return;}
      timer=setInterval(()=>{index++;if(index===frames.length-1)stop();else render();},650);render();
    });
    prev.addEventListener('click',()=>{stop();index=Math.max(0,index-1);render();});
    next.addEventListener('click',()=>{stop();index=Math.min(frames.length-1,index+1);render();});
    q('[data-action="reset"]').addEventListener('click',()=>{stop();index=0;render();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    reduced.addEventListener('change',stop);render();
  });
})();
