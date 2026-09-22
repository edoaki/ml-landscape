"""Validate the static chapter as a portable set of linked documents."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest
import os
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = Path(os.environ.get('ML_LANDSCAPE_SITE', ROOT/'dist')).resolve()


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.links = []
        self.assets = []
        self.headings = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('img', 'script', 'source', 'audio') and 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'video' and 'poster' in attrs:
            self.assets.append(attrs['poster'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.assets.append(attrs['href'])
        if tag == 'h1':
            self.headings += 1


class LandscapeDocuments(unittest.TestCase):
    def test_all_navigation_and_local_assets_resolve_without_design_docs(self):
        pages = {path.resolve(): Document(path) for path in [CHAPTER/'index.html', *(p for group in ('basics','models','fields','questions') for p in (CHAPTER/group).glob('*.html'))]}
        self.assertGreaterEqual(len(pages), 26)
        self.assertEqual({p.name for p in CHAPTER.glob('*.html')}, {'index.html'})
        self.assertFalse((CHAPTER/'legacy').exists())
        for path, doc in pages.items():
            with self.subTest(page=path.name):
                self.assertEqual(doc.headings, 1)
                self.assertEqual(len(doc.ids), len(set(doc.ids)))
                for href in doc.links + doc.assets:
                    url = urlsplit(href)
                    if url.scheme or url.netloc:
                        continue
                    target = (path.parent / unquote(url.path)).resolve() if url.path else path
                    self.assertTrue(target.is_file(), (path.name, href))
                    self.assertTrue(target.is_relative_to(CHAPTER), (path.name, href))
                    self.assertNotIn(ROOT / 'docs', target.parents)
                    if url.fragment and target in pages:
                        self.assertIn(unquote(url.fragment), pages[target].ids, (path.name, href))
                for src in doc.assets:
                    self.assertFalse(urlsplit(src).scheme, f'External runtime dependency: {src}')

    def test_svg_assets_parse_and_protein_has_real_coordinates(self):
        for path in (CHAPTER / 'assets').glob('*.svg'):
            root = ET.parse(path).getroot()
            self.assertTrue(root.tag.endswith('svg'))
            self.assertIn('viewBox', root.attrib)
        pdb = (CHAPTER / 'assets/alphafold-P69905-v6.pdb').read_text()
        atoms = [line for line in pdb.splitlines() if line.startswith('ATOM') and line[12:16].strip() == 'CA']
        self.assertEqual(len(atoms), 142)
        for atom in atoms:
            self.assertTrue(0 <= float(atom[60:66]) <= 100)


if __name__ == '__main__':
    unittest.main()
