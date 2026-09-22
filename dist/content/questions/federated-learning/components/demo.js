'use strict';
(() => {
 const root=document.querySelector('#fed-demo');if(!root)return;let step=0;
 const messages=['1/4：同じ重み2.0を三つの工場へ配ります。','2/4：各工場が手元の記録で学習。重みはA=1.0、B=2.0、C=3.0に変わりました。','3/4：サーバーへ返すのは更新後の重みと集約に必要な件数。生の設備記録は返しません。','4/4：(20×1 + 30×2 + 50×3) / 100 = 2.3。これが次のラウンドで配る共通の重みです。'];
 function render(){root.querySelectorAll('.ld-stages li').forEach((li,i)=>{if(i===step)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');});root.querySelectorAll('[data-weight]').forEach((n,i)=>n.textContent=step===0?'受信した重み 2.0':`更新後の重み ${(i+1).toFixed(1)}`);root.querySelector('[data-server]').textContent=step===3?'新しい共通モデル：重み w = 2.3':step===2?'サーバー：Aの1.0、Bの2.0、Cの3.0を受信':'サーバーの共通モデル：重み w = 2.0';root.querySelector('[role="status"]').textContent=messages[step];root.querySelector('[data-next]').disabled=step===3;}
 root.querySelector('[data-next]').addEventListener('click',()=>{step=Math.min(3,step+1);render();});root.querySelector('[data-reset]').addEventListener('click',()=>{step=0;render();});root.querySelector('.ld-controls').hidden=false;render();
})();
