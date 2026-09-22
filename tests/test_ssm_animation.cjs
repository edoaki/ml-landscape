// Run the production timeline with a controlled frame clock and minimal DOM.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const all = fs.readFileSync(path.join(__dirname, '../content/models/ssm/components/ssm.js'),'utf8');
const source = all.slice(all.indexOf('// SSM recurrence:'));
function setup(reduce=false) {
  const nodes = {};
  const make = () => ({style:{},dataset:{},textContent:'',disabled:false,hidden:true,listeners:{},
    addEventListener(event,fn){this.listeners[event]=fn;},setAttribute(name,value){this[name]=value;},
    querySelector(){return this.text||(this.text={textContent:''});}});
  for(const key of ['prev','input','a-term','b-term','state','output','new-input','wires','sum','play','next','reset','status','controls'])nodes[key]=make();
  const saved=[make(),make(),make()], panel=make();
  panel.querySelector=s=>nodes[s.replace('.ssm-','')];
  panel.querySelectorAll=()=>saved;
  let id=0;const frames=new Map(),events={};
  const document={hidden:false,querySelectorAll:()=>[panel],addEventListener:(n,fn)=>events[n]=fn};
  vm.runInNewContext(source,{document,window:{matchMedia:()=>({matches:reduce})},
    requestAnimationFrame:fn=>{frames.set(++id,fn);return id;},cancelAnimationFrame:id=>frames.delete(id)});
  return {nodes,panel,saved,document,events,click:key=>nodes[key].listeners.click(),
    frame:time=>{const f=[...frames.values()];frames.clear();f.forEach(fn=>fn(time));},frames};
}
const a=setup();
assert.equal(a.nodes.controls.hidden,false);
assert.equal(a.nodes.output.style.opacity,'0');
for(let i=0;i<4;i++)a.click('next');
a.click('play');a.frame(0);a.frame(700);
assert.equal(a.nodes.state.style.transform,'translate(-170px, 0px)');
assert.equal(a.nodes.output.style.transform,'translate(-123px, -72.5px)');
assert.equal(a.nodes['new-input'].style.opacity,'0.5');
a.click('play');const frozen=a.nodes.state.style.transform;a.frame(5000);
assert.equal(a.nodes.state.style.transform,frozen);
a.click('play');a.frame(6000);a.frame(6700);
assert.equal(a.panel.dataset.step,'2');
assert.equal(a.nodes.prev.text.textContent,'h₁');
assert.equal(a.nodes.input.text.textContent,'x₂');
assert.equal(a.saved[0].style.opacity,'1');
a.click('reset');a.frame(9000);
assert.equal(a.panel.dataset.step,'1');assert.equal(a.nodes.state.style.opacity,'0');
for(let i=0;i<15;i++)a.click('next');
assert.equal(a.panel.dataset.phase,'complete');assert.equal(a.nodes.next.disabled,true);
assert.equal(a.nodes.state.text.textContent,'h₃');
assert.equal(a.nodes.state.style.transform,'translate(-340px, 0px)');
a.click('play');assert.equal(a.panel.dataset.phase,'0');
a.document.hidden=true;a.events.visibilitychange();assert.equal(a.frames.size,0);
const b=setup(true);for(let i=0;i<4;i++)b.click('next');
assert.equal(b.nodes.state.style.transform,'translate(-340px, 0px)');
assert.equal(b.nodes.output.style.transform,'translate(-246px, -145px)');
console.log('SSM: handoff interpolation, pause/resume, reset, completion, restart, hidden-tab pause, reduced motion OK.');
