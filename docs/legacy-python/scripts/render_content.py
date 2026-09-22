"""Compile page-local Markdown, components, sources and stable ID links."""
from pathlib import Path
from functools import lru_cache
import html,re,subprocess
import markdown,yaml
ROOT=Path(__file__).resolve().parents[1]

def read_page(path):
    raw=path.read_text(); _,front,body=raw.split('---',2)
    return yaml.safe_load(front),body

@lru_cache(maxsize=None)
def math_html(tex):
    result=subprocess.run(['node',str(ROOT/'source/render-math.cjs')],input=tex,text=True,capture_output=True,check=True)
    return '<div class="equation" tabindex="0" aria-label="数式（横にスクロールできます）">'+result.stdout+'</div>'

def render(path,body,registry):
    sources_path=path.parent/'sources.yml'
    sources=yaml.safe_load(sources_path.read_text()) if sources_path.exists() else {}
    stash={}
    def hold(value):
        key='MLPLACEHOLDER'+str(len(stash))+'END';stash[key]=value
        return '\n\n'+key+'\n\n'
    def component(m):
        file=path.parent/'components'/(m[1]+'.html')
        if not re.fullmatch(r'[a-z0-9-]+',m[1]) or not file.is_file():raise ValueError(f'{path}: missing component {m[1]}')
        return hold(file.read_text())
    body=re.sub(r'\{\{component:([^}]+)\}\}',component,body)
    body=re.sub(r'(?ms)^\$\$\n(.*?)\n\$\$$',lambda m:hold(math_html(m[1])),body)
    out=markdown.markdown(body,extensions=['tables','attr_list','md_in_html','fenced_code'])
    for key,value in stash.items():out=out.replace('<p>'+key+'</p>',value).replace(key,value)
    def link(m):
        value=html.unescape(m[2])
        if value.startswith('page:'):
            target,sep,frag=value[5:].partition('#')
            if target not in registry:raise ValueError(f'{path}: unknown page {target}')
            value=registry[target]['url']+(sep+frag if sep else '')
        elif value.startswith('source:'):
            key=value[7:]
            if key not in sources:raise ValueError(f'{path}: unknown source {key}')
            value=sources[key]['url']
        elif value.startswith('media:'):
            value=(path.parent/'media'/value[6:]).relative_to(ROOT).as_posix()
        return m[1]+'="'+html.escape(value,quote=True)+'"'
    return re.sub(r'(href|src|poster)="([^"]+)"',link,out)
