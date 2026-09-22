'use strict';
(() => {
 const root=document.querySelector('#ar-demo');if(!root)return;
 const select=root.querySelector('select'),next=root.querySelector('[data-next]'),play=root.querySelector('[data-play]');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');let step=0,timer=null;
 const sequence=()=>['私は',select.value,'が','好き','です','終了'];
 function stop(){clearInterval(timer);timer=null;play.textContent=reduced.matches?'再生（1段ずつ）':'順に再生';play.setAttribute('aria-pressed','false');}
 function render(){
  const words=sequence();root.querySelector('.ld-sequence').replaceChildren(...words.slice(0,step+1).map(t=>{const span=document.createElement('span');span.className='ld-token';span.textContent=t;return span;}));
  const candidates=['次の候補：猫 60% ／ 犬 40%',`次の候補：「が」${select.value==='猫'?'90':'80'}% ／ その他${select.value==='猫'?'10':'20'}%`,'次の候補：好き 50% ／ 苦手 30% ／ その他20%','次の候補：です 80% ／ その他20%','次の候補：終了 90% ／ その他10%','終了トークンを選んだので生成を止めます。'];
  root.querySelector('.ld-candidate').textContent=candidates[step];
  root.querySelector('[role="status"]').textContent=step===0?'まだ次のトークンを選んでいません。選んだ結果を入力へ戻します。':step===5?'5回の選択で終了。終了トークンは文の終わりを示す特別な記号です。':`「${words[step]}」を選択。次は「${words.slice(0,step+1).join(' ')}」全体を条件にします。`;
  next.disabled=step===5;play.disabled=step===5;select.disabled=step>0;
 }
 function advance(){if(step<5)step++;if(step===5)stop();render();}
 next.addEventListener('click',()=>{stop();advance();});
 play.addEventListener('click',()=>{if(timer){stop();return;}if(step===5)return;if(reduced.matches){advance();return;}play.textContent='停止';play.setAttribute('aria-pressed','true');timer=setInterval(advance,1400);});
 root.querySelector('[data-reset]').addEventListener('click',()=>{stop();step=0;render();});
 select.addEventListener('change',render);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 reduced.addEventListener('change',stop);root.querySelector('.ld-controls').hidden=false;stop();render();
})();
