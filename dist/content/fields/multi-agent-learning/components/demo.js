'use strict';
(() => {
 const root=document.querySelector('#agents-demo');if(!root)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');let frame=0,pos=[100,100];
 const choices={alone:[235,100],together:[420,420],reset:[100,100]};
 function draw(p){pos=p;root.querySelector('[data-robot="A"]').setAttribute('transform',`translate(${p[0]} 90)`);root.querySelector('[data-robot="B"]').setAttribute('transform',`translate(${p[1]} 230)`);const load=root.querySelector('[data-load]');load.setAttribute('x1',p[0]);load.setAttribute('x2',p[1]);}
 function move(kind){
  cancelAnimationFrame(frame);const target=choices[kind];draw([100,100]);
  const message={alone:'Aだけが進むと、荷物は斜めになります。Aの前進だけでは安定して運べません。',together:'AとBが同時に進むと、荷物の向きを保ったまま台へ届きます。',reset:'出発位置：AもBも待っています。茶色の棒は荷物です。'}[kind];
  root.querySelector('[role="status"]').textContent=message;root.querySelector('desc').textContent=message;
  root.querySelectorAll('[data-move]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.move===kind)));
  if(reduced.matches||kind==='reset'){draw(target);return;}
  const start=performance.now();function tick(now){const t=Math.min((now-start)/800,1),s=t*t*(3-2*t);draw(target.map(x=>100+(x-100)*s));if(t<1)frame=requestAnimationFrame(tick);}frame=requestAnimationFrame(tick);
 }
 root.querySelectorAll('[data-move]').forEach(b=>{b.setAttribute('aria-pressed','false');b.addEventListener('click',()=>move(b.dataset.move));});
 root.querySelector('[data-reset]').addEventListener('click',()=>move('reset'));root.querySelector('.ld-controls').hidden=false;
})();
