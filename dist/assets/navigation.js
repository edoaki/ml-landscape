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
  // Theme: the head script applied the saved or OS choice; the button overrides and remembers it.
  const themeButton=$('.theme-toggle'),docEl=document.documentElement;
  if(themeButton){
    const osDark=window.matchMedia('(prefers-color-scheme: dark)');
    const sync=()=>{const dark=docEl.dataset.theme==='dark';themeButton.setAttribute('aria-pressed',String(dark));themeButton.title=dark?'明るい配色に切り替える':'暗い配色に切り替える';};
    themeButton.hidden=false;sync();
    themeButton.addEventListener('click',()=>{
      const next=docEl.dataset.theme==='dark'?'light':'dark';
      docEl.dataset.theme=next;sync();
      try{localStorage.setItem('landscape-theme',next);}catch{}
    });
    osDark.addEventListener('change',()=>{
      let saved=null;try{saved=localStorage.getItem('landscape-theme');}catch{}
      if(!saved){docEl.dataset.theme=osDark.matches?'dark':'light';sync();}
    });
  }
  // Offline full-text search: the index is a script so it also loads over file://.
  const search=$('.site-search');
  if(search){
    const toggle=$('.search-toggle',search),panel=$('.search-panel',search),input=$('#search-input'),status=$('.search-status',search),list=$('.search-results',search);
    const root=(document.body.dataset.siteRoot||'.')+'/';
    const norm=s=>s.normalize('NFKC').toLowerCase();
    let entries=null,loading=false,timer;
    search.hidden=false;
    function load(){
      if(entries||loading)return;
      if(window.ML_SEARCH_INDEX){entries=window.ML_SEARCH_INDEX.map(e=>({...e,n:norm(e.t+' '+e.s+' '+e.x),nt:norm(e.t+' '+e.s)}));run();return;}
      loading=true;status.textContent='索引を読み込んでいます…';
      const script=document.createElement('script');
      script.src=root+'assets/search-index.js';
      script.onload=()=>{loading=false;load();};
      script.onerror=()=>{loading=false;status.textContent='検索用の索引を読み込めませんでした。';};
      document.head.appendChild(script);
    }
    function snippet(text,term){
      const at=Math.max(0,norm(text).indexOf(term)),start=Math.max(0,at-40);
      const frag=document.createDocumentFragment();
      frag.append((start?'…':'')+text.slice(start,at));
      const mark=document.createElement('mark');mark.textContent=text.slice(at,at+term.length);frag.append(mark);
      frag.append(text.slice(at+term.length,at+term.length+80)+(at+term.length+80<text.length?'…':''));
      return frag;
    }
    function run(){
      list.replaceChildren();
      const terms=norm(input.value).split(/\s+/).filter(Boolean);
      if(!terms.length){status.textContent='';return;}
      if(!entries){load();return;}
      const hits=[];
      for(const e of entries){
        if(!terms.every(t=>e.n.includes(t)))continue;
        let score=0;for(const t of terms){if(e.nt.includes(t))score+=10;score+=Math.min(5,e.n.split(t).length-1);}
        hits.push([score,e]);
      }
      hits.sort((a,b)=>b[0]-a[0]);
      status.textContent=hits.length?`${hits.length}件${hits.length>30?'（上位30件を表示）':''}`:'見つかりませんでした。';
      for(const [,e] of hits.slice(0,30)){
        const li=document.createElement('li'),a=document.createElement('a'),p=document.createElement('p');
        a.href=root+e.u+(e.h?'#'+encodeURIComponent(e.h):'');
        const page=document.createElement('small');page.textContent=e.t;
        a.append(page,document.createTextNode(e.s===e.t?e.t:e.s));
        p.append(snippet(e.x,terms[0]));
        li.append(a,p);list.append(li);
      }
    }
    function open(state){
      panel.hidden=!state;toggle.setAttribute('aria-expanded',String(state));
      if(state){load();input.focus();input.select();}
    }
    toggle.addEventListener('click',()=>open(panel.hidden));
    input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(run,120);});
    list.addEventListener('click',e=>{if(e.target.closest('a'))open(false);});
    document.addEventListener('keydown',e=>{
      if(e.key==='/'&&panel.hidden&&!e.target.closest('input,textarea,select,[contenteditable]')){e.preventDefault();open(true);}
      else if(e.key==='Escape'&&!panel.hidden){e.stopImmediatePropagation();open(false);toggle.focus();}
    },true);
    document.addEventListener('click',e=>{if(!panel.hidden&&!search.contains(e.target))open(false);});
  }
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){$$('.toc a').forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));}}},{rootMargin:'-15% 0px -65% 0px'});
    $$('.article section').forEach(s=>observer.observe(s));
  }
})();
