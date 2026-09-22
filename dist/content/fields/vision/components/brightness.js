'use strict';
(()=>{
  const $ = (q,root=document)=>root.querySelector(q);
  const $$ = (q,root=document)=>Array.from(root.querySelectorAll(q));
  const svg=(body,h=260)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 ${h}" role="img" aria-label="操作に対応する数値の図" style="width:100%;height:auto">${body}</svg>`;
  const text=(x,y,s,c='#35664d')=>`<text x="${x}" y="${y}" fill="${c}" font-family="system-ui,sans-serif" font-size="16">${s}</text>`;
  $$('[data-demo="brightness"]').forEach(d=>{
    const type=d.dataset.demo,range=$('input[type=range]',d),result=$('.result',d);
    if(type==='brightness'){range.addEventListener('input',()=>{$('img',d).style.filter=`brightness(${range.value})`;});}

  });
})();
