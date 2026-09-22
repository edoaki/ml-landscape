'use strict';
(() => {
  const $ = (q,root=document)=>root.querySelector(q);
  const $$ = (q,root=document)=>Array.from(root.querySelectorAll(q));
  const menu=$('.mobile-menu'),nav=$('.sidenav'),layout=$('.layout');
  const narrow=window.matchMedia('(max-width: 820px)');
  let desktopOpen=true;
  try{desktopOpen=localStorage.getItem('landscape-nav-open')!=='false';}catch{}
  function setNav(open){
    nav.classList.toggle('open',open);
    nav.hidden=!open;
    layout.classList.toggle('nav-collapsed',!open);
    menu.setAttribute('aria-expanded',String(open));
    const label=open?'章の目次を折りたたむ':'章の目次を開く';
    menu.setAttribute('aria-label',label);
    menu.title=label;
  }
  function toggleNav(open){
    setNav(open);
    if(!narrow.matches){
      desktopOpen=open;
      try{localStorage.setItem('landscape-nav-open',String(open));}catch{}
    }
  }
  menu.addEventListener('click',()=>toggleNav(nav.hidden));
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'&&!nav.hidden){toggleNav(false);menu.focus();}
  });
  document.addEventListener('click',e=>{
    if(narrow.matches&&!nav.contains(e.target)&&!menu.contains(e.target))setNav(false);
  });
  narrow.addEventListener('change',()=>setNav(narrow.matches?false:desktopOpen));
  setNav(narrow.matches?false:desktopOpen);
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){$$('.toc a').forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));}}},{rootMargin:'-15% 0px -65% 0px'});
    $$('.article section').forEach(s=>observer.observe(s));
  }
  // Course link works as a file and returns to the outer portal when embedded.
  $$('.course-link').forEach(a=>{if(location.protocol!=='file:'){a.href='../';a.target='_top';}});
  const svg=(body,h=260)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 ${h}" role="img" aria-label="操作に対応する数値の図" style="width:100%;height:auto">${body}</svg>`;
  const text=(x,y,s,c='#35664d')=>`<text x="${x}" y="${y}" fill="${c}" font-family="system-ui,sans-serif" font-size="16">${s}</text>`;
  $$('[data-transformer-layers]').forEach(d=>{
    const {states,stages}=JSON.parse(d.dataset.transformerLayers);
    const tokens=$$('.tf-token',d),steps=$$('[data-layer]',d);
    const reduced=matchMedia('(prefers-reduced-motion: reduce)');
    let timers=[],current=0;
    const later=(fn,delay)=>timers.push(setTimeout(fn,delay));
    const place=points=>tokens.forEach((token,i)=>{const [x,y]=points[i];token.style.transform=`translate(${x}px,${y}px)`;});
    const show=stage=>{
      const previous=current;current=stage;timers.forEach(clearTimeout);timers=[];
      d.classList.remove('tf-numeric','tf-output-morph','tf-output-ready','tf-output-moving');
      d.classList.toggle('tf-sentence',stage===0);
      d.classList.toggle('tf-final-layer',stage===5);
      steps.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===stage)));
      $('.tf-counter',d).textContent=stage===0?'SENTENCE':stage===1?'EMBEDDING':stage===5?'LAYER N':stage===6?'NEXT TOKEN':`LAYER ${stage-1}`;
      $('.tf-stage-title',d).textContent=stages[stage][0];
      $('.tf-stage-description',d).textContent=stages[stage][1];
      $('.tf-space svg',d).setAttribute('aria-label',`${stages[stage][0]}：${stages[stage][1]}`);
      if(stage===1&&!reduced.matches){
        // First replace words with numerical vectors; only then form spatial dots.
        place(states[0]);d.classList.add('tf-numeric');
        later(()=>{d.classList.remove('tf-numeric');place(states[1]);},1400);
      }else if(stage===6){
        // Preserve the final token element: its dot expands into the output vector.
        if(previous!==5)place(states[5]);
        d.classList.add('tf-output-moving');
        const morph=()=>{d.classList.add('tf-output-morph');tokens[tokens.length-1].style.transform='translate(260px,60px)';};
        if(reduced.matches){morph();d.classList.add('tf-output-ready');}
        else {later(morph,previous===5?60:1000);later(()=>d.classList.add('tf-output-ready'),previous===5?1200:2200);}
      }else place(states[stage]);
    };
    steps.forEach(button=>button.addEventListener('click',()=>show(Number(button.dataset.layer))));
    reduced.addEventListener('change',()=>show(current));
    $('.tf-live',d).hidden=false;d.classList.add('tf-enhanced');show(0);
  });
  $$('[data-demo]').forEach(d=>{
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
    if(type==='flow'){
      const update=()=>{const t=Number(range.value),x=100+480*t,y=215-160*t;$('.flow-plot',d).innerHTML=svg(`<path d="M100 215L580 55" stroke="#b4c4aa" stroke-width="3" stroke-dasharray="5 5"/><circle cx="100" cy="215" r="8" fill="#4d7897"/><circle cx="580" cy="55" r="8" fill="#ba7147"/><circle cx="${x}" cy="${y}" r="12" fill="#35664d"/>`+text(40,250,'ノイズ (−1,0)')+text(495,35,'データ (1,2)')+text(260,280,`時刻 t = ${t.toFixed(2)}`),300);result.textContent=`位置 (${(-1+2*t).toFixed(2)}, ${(2*t).toFixed(2)})。速度は (2, 2)。Δt=0.1なら位置の変化は (0.2, 0.2)。`;};range.addEventListener('input',update);update();
    }
    if(type==='brightness'){range.addEventListener('input',()=>{$('img',d).style.filter=`brightness(${range.value})`;});}
    if(type==='protein'){
      const points=window.PROTEIN_POINTS||[];
      const color=s=>s>=90?'#1355ca':s>=70?'#65cbf3':s>=50?'#ffce31':'#ed7327';
      const update=()=>{const angle=Number(range.value)*Math.PI/180,c=Math.cos(angle),s=Math.sin(angle);const rotated=points.map(p=>[p[0]*c+p[2]*s,p[1],-p[0]*s+p[2]*c,p[3]]);const lines=rotated.slice(1).map((p,i)=>({a:rotated[i],b:p})).sort((u,v)=>(u.a[2]+u.b[2])-(v.a[2]+v.b[2]));const body=lines.map(({a,b})=>`<path d="M${350+a[0]*6} ${205-a[1]*6}L${350+b[0]*6} ${205-b[1]*6}" fill="none" stroke="${color(a[3])}" stroke-width="4" stroke-linecap="round"/>`).join('');$('.protein-plot',d).innerHTML=svg(body,420);};range.addEventListener('input',update);update();
    }
    if(type==='gradcam'){
      $$('button',d).forEach(b=>b.addEventListener('click',()=>{const c=b.dataset.class;$('#gradcam-result').src=new URL(`assets/gradcam-${c}.png`, new URL(document.body.dataset.siteRoot + "/", document.baseURI)).href;$('#gradcam-result').alt=`VGG-16の${c==='cat'?'猫':'犬'}クラスに対するGrad-CAM`;$('#gradcam-caption').textContent=`VGG-16 · ${c==='cat'?'Cat':'Dog'} を対象にしたGrad-CAM` ;$$('button',d).forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));
    }
  });
})();

// Numeric changes happen in place; every calculation remains visible.
(() => {
  document.querySelectorAll('.gnn-calc').forEach(panel => {
    const button = panel.querySelector('.gnn-replay');
    if (!button) return;
    const nodes = [...panel.querySelectorAll('[data-start][data-end]')];
    let running = false;
    button.hidden = false;
    button.addEventListener('click', () => {
      if (running) return;
      running = true; button.disabled = true;
      panel.classList.add('gnn-running');
      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const duration = reduced ? 0 : 1800;
      const started = performance.now();
      const tick = now => {
        const t = duration ? Math.min(1, (now-started)/duration) : 1;
        nodes.forEach(node => {
          const from = node.dataset.start.split(',').map(Number);
          const to = node.dataset.end.split(',').map(Number);
          node.textContent = t === 1 ? node.dataset.to : '(' + from.map((v,i) => (v+(to[i]-v)*t).toFixed(3)).join(', ') + ')';
        });
        if (t < 1) requestAnimationFrame(tick);
        else { running = false; button.disabled = false; panel.classList.remove('gnn-running'); }
      };
      requestAnimationFrame(tick);
    });
  });
})();

