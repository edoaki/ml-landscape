'use strict';
(()=>{
  const $ = (q,root=document)=>root.querySelector(q);
  const $$ = (q,root=document)=>Array.from(root.querySelectorAll(q));
  const svg=(body,h=260)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 ${h}" role="img" aria-label="操作に対応する数値の図" style="width:100%;height:auto">${body}</svg>`;
  const text=(x,y,s,c='#35664d')=>`<text x="${x}" y="${y}" fill="${c}" font-family="system-ui,sans-serif" font-size="16">${s}</text>`;
  $$('[data-demo="conv"]').forEach(d=>{
    const type=d.dataset.demo,range=$('input[type=range]',d),result=$('.result',d);
    if(type==='conv'){
      const input=[[1,2,0,1],[0,1,3,2],[2,0,1,0],[1,2,0,2]];
      const padding=$('.conv-padding',d),stride=$('.conv-stride',d),pool=$('.conv-pool',d);
      let poolIndex=0;
      const render=(element,values,classFor,click)=>{
        element.style.setProperty('--cols',values[0].length);element.replaceChildren();
        values.forEach((row,r)=>row.forEach((v,c)=>{
          const cell=document.createElement(click?'button':'span');
          if(click){cell.type='button';cell.addEventListener('click',()=>click(r,c));cell.setAttribute('aria-label',`行${r}、列${c}：${v}`);}
          cell.className='cell '+classFor(r,c);cell.textContent=Number.isInteger(v)?v:Number(v.toFixed(2));
          cell.dataset.value=v;cell.dataset.row=r;cell.dataset.col=c;
          if(click)cell.setAttribute('aria-pressed',String(cell.classList.contains('current')));
          element.append(cell);
        }));
      };
      const update=()=>{
        const p=Number(padding.value),s=Number(stride.value),size=4+2*p;
        const padded=Array.from({length:size},(_,r)=>Array.from({length:size},(_,c)=>input[r-p]?.[c-p]??0));
        const n=Math.floor((size-2)/s)+1;
        const output=Array.from({length:n},(_,r)=>Array.from({length:n},(_,c)=>padded[r*s][c*s]-padded[r*s+1][c*s+1]));
        range.max=n*n-1;range.value=Math.min(Number(range.value),n*n-1);
        const pos=Number(range.value),r=Math.floor(pos/n),c=pos%n,ir=r*s,ic=c*s;
        const pn=Math.floor(n/2),hasPool=pool.value!=='none';
        poolIndex=Math.min(poolIndex,Math.max(0,pn*pn-1));
        const pr=Math.floor(poolIndex/pn),pc=poolIndex%pn;
        $('.conv-settings',d).textContent=`stride=${s}、padding=${p}：${p?`周囲に0を補った${size}×${size}の入力`:'4×4の入力'} → ${n}×${n}の出力。`;
        $('.conv-position-value',d).textContent=`出力 (${r}, ${c})`;
        $('.conv-input-title',d).textContent=`入力 ${size} × ${size}${p?'（周囲は0）':''}`;
        $('.conv-output-title',d).textContent=`出力 ${n} × ${n}`;
        render($('.conv-input',d),padded,(a,b)=>(a>=ir&&a<ir+2&&b>=ic&&b<ic+2?'selected ':'')+(a<p||b<p||a>=4+p||b>=4+p?'padded':''));
        render($('.conv-output',d),output,(a,b)=>(a===r&&b===c?'current ':'')+(hasPool&&a>=pr*2&&a<pr*2+2&&b>=pc*2&&b<pc*2+2?'pool-source':''),(a,b)=>{range.value=a*n+b;update();});
        result.textContent=`出力 (${r}, ${c})：${padded[ir][ic]}×1 + ${padded[ir][ic+1]}×0 + ${padded[ir+1][ic]}×0 + ${padded[ir+1][ic+1]}×(−1) = ${output[r][c]}。入力の左上位置は (${ir}, ${ic})。行・列は0から数えます。`;
        $('.conv-pool-panel',d).hidden=!hasPool;
        const pooled=$('.conv-pooled',d),poolResult=$('.conv-pool-result',d);
        poolResult.textContent='';
        if(hasPool){
          if(!pn){pooled.replaceChildren();$('.conv-pool-title',d).textContent='pooling：計算できません';poolResult.textContent='畳み込みの出力が1×1なので、2×2のpoolingを適用できません。strideを小さくするかpaddingを増やしてください。';}
          else{
            const windows=Array.from({length:pn},(_,a)=>Array.from({length:pn},(_,b)=>[output[a*2][b*2],output[a*2][b*2+1],output[a*2+1][b*2],output[a*2+1][b*2+1]]));
            const values=windows.map(row=>row.map(v=>pool.value==='max'?Math.max(...v):v.reduce((a,b)=>a+b,0)/4));
            $('.conv-pool-title',d).textContent=`pooling後 ${pn} × ${pn}`;
            render(pooled,values,(a,b)=>a===pr&&b===pc?'current':'',(a,b)=>{poolIndex=a*pn+b;update();});
            const v=windows[pr][pc];
            poolResult.textContent=`青い範囲 [${v.join(', ')}] の${pool.value==='max'?'最大値':'平均値'} = ${values[pr][pc]}。pooling後のマスを押すと集約した範囲を確認できます。${n%2?'下端の1行と右端の1列は2×2に収まらないため使いません。':''}`;
          }
        }
      };
      range.addEventListener('input',update);
      [padding,stride,pool].forEach(control=>control.addEventListener('change',()=>{range.value=0;poolIndex=0;update();}));
      update();
    }

  });
})();
