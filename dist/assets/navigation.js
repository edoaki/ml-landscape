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
  function revealFragment(){
    let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
    const target=document.getElementById(id);if(!target)return;
    let opened=false;
    for(let node=target.parentElement;node;node=node.parentElement){
      if(node.tagName==='DETAILS'&&!node.open){node.open=true;opened=true;}
    }
    if(opened)target.scrollIntoView();
  }
  window.addEventListener('hashchange',revealFragment);
  revealFragment();
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){$$('.toc a').forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));}}},{rootMargin:'-15% 0px -65% 0px'});
    $$('.article section').forEach(s=>observer.observe(s));
  }
})();
