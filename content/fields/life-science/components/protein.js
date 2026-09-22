'use strict';
(()=>{
  const $ = (q,root=document)=>root.querySelector(q);
  const $$ = (q,root=document)=>Array.from(root.querySelectorAll(q));
  const svg=(body,h=260)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 ${h}" role="img" aria-label="操作に対応する数値の図" style="width:100%;height:auto">${body}</svg>`;
  const text=(x,y,s,c='#35664d')=>`<text x="${x}" y="${y}" fill="${c}" font-family="system-ui,sans-serif" font-size="16">${s}</text>`;
  $$('[data-demo="protein"]').forEach(d=>{
    const type=d.dataset.demo,range=$('input[type=range]',d),result=$('.result',d);
    if(type==='protein'){
      const points=window.PROTEIN_POINTS||[];
      const color=s=>s>=90?'#1355ca':s>=70?'#65cbf3':s>=50?'#ffce31':'#ed7327';
      const update=()=>{const angle=Number(range.value)*Math.PI/180,c=Math.cos(angle),s=Math.sin(angle);const rotated=points.map(p=>[p[0]*c+p[2]*s,p[1],-p[0]*s+p[2]*c,p[3]]);const lines=rotated.slice(1).map((p,i)=>({a:rotated[i],b:p})).sort((u,v)=>(u.a[2]+u.b[2])-(v.a[2]+v.b[2]));const body=lines.map(({a,b})=>`<path d="M${350+a[0]*6} ${205-a[1]*6}L${350+b[0]*6} ${205-b[1]*6}" fill="none" stroke="${color(a[3])}" stroke-width="4" stroke-linecap="round"/>`).join('');$('.protein-plot',d).innerHTML=svg(body,420);};range.addEventListener('input',update);update();
    }

  });
})();
