"""Build portable HTML from page-local Markdown, without regenerating media."""
from pathlib import Path
from string import Template
import argparse,html,re,sys,shutil,posixpath
from urllib.parse import urlsplit, urlunsplit, unquote
import yaml
from bs4 import BeautifulSoup
sys.path.insert(0,str(Path(__file__).resolve().parent/'scripts'))
from render_content import read_page,render,ROOT
esc=lambda value:html.escape(str(value),quote=True)
LABELS={'planned':'準備中','partial':'既存内容を移行・拡充予定','migrated':'既存内容を移行','ready':'公開本文'}

def page_toc(parsed):
    """Follow the reading order, leaving optional detail out of the overview."""
    links=[];seen=set()
    for heading in parsed.find_all(['h2','h3']):
        if heading.find_parent('details'):continue
        target=heading if heading.get('id') else heading.find_parent(['section','div'],id=True)
        if target is None or target['id'] in seen:continue
        seen.add(target['id'])
        links.append('<a data-level="'+heading.name[1]+'" href="#'+esc(target['id'])+'">'+esc(heading.get_text())+'</a>')
    return ''.join(links)

def build(output=None):
    registry={}; bodies={}; paths={}
    for path in sorted((ROOT/'content').glob('*/*/index.md')):
        meta,body=read_page(path);id=meta['id']
        if id in registry:raise ValueError(f'Duplicate page ID: {id}')
        if not re.fullmatch('[a-z][a-z0-9-]*',id):raise ValueError(id)
        if meta['status'] not in LABELS:raise ValueError(f'Unknown status: {id}')
        if not re.fullmatch(r'(?:[a-z][a-z0-9-]*/)*[a-z][a-z0-9-]*\.html',meta['url']):raise ValueError(meta['url'])
        registry[id]=meta;paths[id]=path;bodies[id]=body
    navigation=yaml.safe_load((ROOT/'navigation.yml').read_text())
    order=[item['page'] for group in navigation for item in group['items']]
    if len(order)!=len(set(order)) or set(order)!=set(registry):raise ValueError('Navigation and page IDs differ')
    if len({v['url'] for v in registry.values()})!=len(registry):raise ValueError('Duplicate URL')
    for group in navigation:
        for item in group['items']:
            if item.get('parent') and item['parent'] not in registry:raise ValueError(item)
            registry[item['page']]['group']=group['title']
    template=Template((ROOT/'templates/page.html').read_text())
    root_entry=output is None
    output=Path(output or ROOT/'dist').resolve();output.mkdir(parents=True,exist_ok=True)
    if output!=ROOT:
        shutil.copytree(ROOT/'assets',output/'assets',dirs_exist_ok=True)
        for media in [*(ROOT/'content').glob('*/*/media'),*(ROOT/'content').glob('*/*/components')]:
            shutil.copytree(media,output/media.relative_to(ROOT),dirs_exist_ok=True)
        shutil.copy2(ROOT/'templates/README-distribution.md',output/'README.md')
    rendered={}
    def nav_html(current):
        out='<p class="nav-label">目次</p>'
        for group in navigation:
            out+='<details'+(' open' if registry[current]['group']==group['title'] or group['title']=='はじめに' else '')+'><summary>'+esc(group['title'])+'</summary>'
            category=None
            for item in group['items']:
                id=item['page'];meta=registry[id]
                if item.get('category')!=category:
                    category=item.get('category')
                    if category:out+='<p class="nav-category">'+esc(category)+'</p>'
                status='<small>'+('準備中' if meta['status']=='planned' else '拡充予定')+'</small>' if meta['status'] in ('planned','partial') else ''
                out+='<a href="'+meta['url']+'"'+(' aria-current="page"' if id==current else '')+(' data-parent="'+esc(item['parent'])+'"' if item.get('parent') else '')+'>'+esc(meta['title'])+status+'</a>'
            out+='</details>'
        return out
    for id in order:
        meta=registry[id];body=render(paths[id],bodies[id],registry)
        parsed=BeautifulSoup(body,'html5lib');ids=[x['id'] for x in parsed.find_all(id=True)]
        if len(ids)!=len(set(ids)):raise ValueError(f'{id}: duplicate content IDs')
        toc=page_toc(parsed)
        status=''
        if meta['status'] in ('planned','partial'):
            message='本文はまだ公開していません。今後扱う予定の範囲を示しています。' if meta['status']=='planned' else '既存の説明・素材を移行したページです。予定範囲のうち、まだ説明していない項目は今後拡充します。'
            status='<aside class="publication-status"><strong>'+LABELS[meta['status']]+'</strong><p>'+message+'</p><details><summary>予定する範囲</summary><p>'+esc(meta['scope'])+'</p></details></aside>'
        scripts=''.join('<script src="'+esc(src)+'" defer></script>' for src in meta.get('scripts',[]))
        scripts+=''.join('<link rel="stylesheet" href="'+esc(src)+'">' for src in meta.get('styles',[]))
        out=template.substitute(id=id,title=esc(meta['title']),description=esc(meta['summary']),summary=esc(meta['summary']),group=esc(meta['group'])+' · <span lang="en">'+esc(meta.get('english_title',''))+'</span>',status=status,navigation=nav_html(id),body=body,toc=toc,scripts=scripts)
        rendered[meta['url']]=out
    # Templates and content references are site-root-relative until this final pass.
    # Emit explicit relative URLs so both file:// and subdirectory hosting work.
    def relative_reference(match, current):
        value=html.unescape(match[2]);ref=urlsplit(value)
        if ref.scheme or ref.netloc or not ref.path:return match[0]
        target=ref.path
        relative=posixpath.relpath(target,posixpath.dirname(current) or '.')
        return match[1]+'="'+esc(urlunsplit(('', '', relative, ref.query, ref.fragment)))+'"'
    for url,text in rendered.items():
        text=text.replace('data-site-root="."','data-site-root="'+posixpath.relpath('.',posixpath.dirname(url) or '.')+'"')
        rendered[url]=re.sub(r'(href|src|poster)="([^\"]+)"',lambda m:relative_reference(m,url),text)
    # Fail before writing on broken internal links, duplicate IDs, unresolved references or assets.
    parsed={url:BeautifulSoup(text,'html5lib') for url,text in rendered.items()}
    errors=[]
    copied_resources={'README.md'}
    for url,doc in parsed.items():
        if re.search(r'\{\{component:|\{\.[a-z][a-z-]*\}|\{#[a-z][a-z-]*\}',doc.select_one('main').get_text()):raise ValueError(f'{url}: unresolved Markdown marker')
        ids=[n['id'] for n in doc.find_all(id=True)]
        if len(ids)!=len(set(ids)):raise ValueError(f'{url}: duplicate IDs')
        for node in doc.find_all(True):
            for attr in ['href','src','poster']:
                if not node.get(attr):continue
                ref=urlsplit(node[attr])
                if ref.scheme or ref.netloc:continue
                dest=posixpath.normpath(posixpath.join(posixpath.dirname(url),unquote(ref.path))) if ref.path else url
                if dest not in rendered:
                    resource=(ROOT/dest).resolve()
                    if not resource.is_relative_to(ROOT) or not resource.is_file():raise ValueError(f'{url}: missing {node[attr]}')
                    if output!=ROOT and dest not in copied_resources:
                        (output/dest).parent.mkdir(parents=True,exist_ok=True)
                        shutil.copy2(resource,output/dest)
                        copied_resources.add(dest)
                if ref.fragment and dest in parsed and not parsed[dest].find(id=unquote(ref.fragment)):errors.append(f'{url}: missing anchor {node[attr]}')
    if errors:raise ValueError('\n'.join(errors))
    for url,text in rendered.items():
        (output/url).parent.mkdir(parents=True,exist_ok=True)
        (output/url).write_text(text)
    if root_entry:
        def entry_reference(match):
            value=html.unescape(match[2]);ref=urlsplit(value)
            if ref.scheme or ref.netloc or not ref.path:return match[0]
            target=ref.path if ref.path in ('index.html','README.md') else 'dist/'+ref.path
            return match[1]+'="'+esc(urlunsplit(('', '', target, ref.query, ref.fragment)))+'"'
        entry=re.sub(r'(href|src|poster)="([^\"]+)"',entry_reference,rendered['index.html'])
        entry=entry.replace('data-site-root="."','data-site-root="dist"')
        (ROOT/'index.html').write_text(entry)
    print(f'Built {len(registry)} pages; links, IDs and assets validated.')
    return registry

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();build(args.output)
