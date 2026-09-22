"""Contracts that keep page editing independent and portable."""
from pathlib import Path
import sys,re,tempfile,unittest
import yaml
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_content import render,read_page
sys.path.insert(0,str(ROOT))
from build import page_toc

class ContentContracts(unittest.TestCase):
 def test_navigation_matches_current_plan_and_page_metadata(self):
  nav=yaml.safe_load((ROOT/'navigation.yml').read_text())
  ids=[p['page'] for group in nav for p in group['items']]
  plan=(ROOT/'docs/content-plan.md').read_text().split('## 2.')[1].split('## 3.')[0]
  planned={'introduction'}
  for row in plan.splitlines():
   if row.startswith('|'):
    planned.update(re.findall(r'\| `([a-z][a-z-]+)` \|',row))
  self.assertEqual(set(ids),planned);self.assertEqual(len(ids),len(set(ids)))
  pages={read_page(p)[0]['id']:(p,*read_page(p)) for p in (ROOT/'content').glob('*/*/index.md')}
  self.assertEqual(set(pages),planned)
  self.assertEqual([g['title'] for g in nav],['はじめに','基礎と代表的な機械学習手法','分野・タスクから知る','横断的な研究を知る','モデルの仕組みを知る'])
  for id,(path,meta,body) in pages.items():
   self.assertTrue(meta['scope'],id)
   if meta['status']=='planned':self.assertFalse(body.strip(),id)
   self.assertNotIn('source/',str(meta.get('scripts',[])),id)
  vit=next(item for group in nav for item in group['items'] if item['page']=='vit')
  self.assertEqual(vit['parent'],'transformer')

 def test_toc_follows_visible_heading_order_and_preserves_hierarchy(self):
  doc=BeautifulSoup('''<h2 id="intro">導入</h2>
<section id="task"><h2>タスク</h2><section id="example"><h3>例</h3></section></section>
<details><summary>補足</summary><section id="detail"><h2>詳説</h2></section></details>
<h2 id="evaluation">評価</h2>''','html5lib')
  links=BeautifulSoup(page_toc(doc),'html5lib').find_all('a')
  self.assertEqual([a['href'] for a in links],['#intro','#task','#example','#evaluation'])
  self.assertEqual([a['data-level'] for a in links],['2','2','3','2'])

 def test_markdown_components_sources_math_and_changed_url(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as d:
   p=Path(d)/'index.md';(p.parent/'components').mkdir();(p.parent/'media').mkdir()
   (p.parent/'sources.yml').write_text('paper:\n  url: https://example.org/paper\n  label: Example\n')
   (p.parent/'components/demo.html').write_text('<figure id="static"><svg viewBox="0 0 10 10" aria-label="図"><circle r="2"/></svg><noscript>静止図を参照</noscript></figure>')
   body='''## 説明 {#idea}

[別ページ](page:other#part)・[出典](source:paper)

![画像](media:figure.svg)

$$
p(y \\mid x)
$$

{{component:demo}}
'''
   out=render(p,body,{'other':{'url':'renamed.html'}})
   doc=BeautifulSoup(out,'html5lib')
   self.assertEqual(doc.h2['id'],'idea');self.assertEqual(doc.a['href'],'renamed.html#part')
   self.assertIn('https://example.org/paper',out)
   self.assertIn(str(p.parent.relative_to(ROOT))+'/media/figure.svg',out)
   self.assertIsNotNone(doc.find('math'));self.assertEqual(doc.svg['viewBox'],'0 0 10 10')
   self.assertEqual(doc.noscript.get_text(),'静止図を参照');self.assertNotIn('{{',out)

 def test_unknown_page_source_and_component_fail(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as d:
   p=Path(d)/'index.md'
   for body in ['[x](page:missing)','[x](source:missing)','{{component:missing}}','{{component:../../escape}}']:
    with self.subTest(body=body),self.assertRaises(ValueError):render(p,body,{})

 def test_sources_and_fonts_are_resolvable(self):
  for path in (ROOT/'content').glob('*/*/sources.yml'):
   for id,ref in yaml.safe_load(path.read_text()).items():
    self.assertTrue(ref['url'],(path,id));self.assertTrue(ref['label'],(path,id))
    if not ref['url'].startswith(('https://','http://')):self.assertTrue((ROOT/ref['url']).is_file(),(path,id))
    if ref.get('provenance'):self.assertTrue((ROOT/ref['provenance']).is_file(),(path,id))
  for value in re.findall(r'url\(([^)]+)\)',(ROOT/'assets/katex.css').read_text()):
   if value.startswith('data:'):continue
   self.assertTrue((ROOT/'assets'/value.strip('"\'')).is_file(),value)

if __name__=='__main__':unittest.main()
