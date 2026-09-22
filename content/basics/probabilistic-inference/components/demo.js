'use strict';
(() => {
 const root=document.querySelector('#bayes-demo'); if(!root)return;
 const theta=[.25,.5,.75]; let history=[];
 const status=root.querySelector('[role="status"]');
 function render(){
  const heads=history.filter(x=>x==='H').length,tails=history.length-heads;
  const logs=theta.map(t=>heads*Math.log(t)+tails*Math.log(1-t));
  const max=Math.max(...logs),weights=logs.map(l=>Math.exp(l-max)),sum=weights.reduce((a,b)=>a+b,0);
  const probs=weights.map(w=>w/sum),prediction=probs.reduce((a,p,i)=>a+p*theta[i],0);
  probs.forEach((p,i)=>{root.querySelector(`[data-prob="${i}"]`).textContent=(100*p).toFixed(1)+'%';root.querySelector(`[data-bar="${i}"]`).style.width=(100*p)+'%';});
  status.textContent=(history.length?`${history.length}回観測（表${heads}回・裏${tails}回）`:'観測なし：事前分布は各1/3')+`。次に表が出る確率は${(100*prediction).toFixed(1)}%。`;
  root.querySelector('[data-undo]').disabled=!history.length;
  root.querySelectorAll('[data-coin]').forEach(b=>b.disabled=history.length>=100);
  if(history.length>=100)status.textContent+=' 上限100回です。戻すかリセットで再開できます。';
 }
 root.querySelectorAll('[data-coin]').forEach(b=>b.addEventListener('click',()=>{if(history.length<100)history.push(b.dataset.coin);render();}));
 root.querySelector('[data-example]').addEventListener('click',()=>{history=['H','H','T','H'];render();});
 root.querySelector('[data-undo]').addEventListener('click',()=>{history.pop();render();});
 root.querySelector('[data-reset]').addEventListener('click',()=>{history=[];render();});
 root.querySelector('.ld-controls').hidden=false;render();
})();
