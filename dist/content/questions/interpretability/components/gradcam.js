'use strict';
(()=>{
  const $ = (q,root=document)=>root.querySelector(q);
  const $$ = (q,root=document)=>Array.from(root.querySelectorAll(q));
  const svg=(body,h=260)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 ${h}" role="img" aria-label="操作に対応する数値の図" style="width:100%;height:auto">${body}</svg>`;
  const text=(x,y,s,c='#35664d')=>`<text x="${x}" y="${y}" fill="${c}" font-family="system-ui,sans-serif" font-size="16">${s}</text>`;
  $$('[data-demo="gradcam"]').forEach(d=>{
    const type=d.dataset.demo,range=$('input[type=range]',d),result=$('.result',d);
    if(type==='gradcam'){
      $$('button',d).forEach(b=>b.addEventListener('click',()=>{const c=b.dataset.class;$('#gradcam-result').src=`assets/gradcam-${c}.png`;$('#gradcam-result').alt=`VGG-16の${c==='cat'?'猫':'犬'}クラスに対するGrad-CAM`;$('#gradcam-caption').textContent=`VGG-16 · ${c==='cat'?'Cat':'Dog'} を対象にしたGrad-CAM` ;$$('button',d).forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));
    }
  });
})();
