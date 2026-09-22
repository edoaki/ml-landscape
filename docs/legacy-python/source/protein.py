"""Render actual AlphaFold CA coordinates; no model inference is performed."""
from common import *
import json

def build():
 points=[]
 for row in (ROOT/'assets/alphafold-P69905-v6.pdb').read_text().splitlines():
  if row.startswith('ATOM') and row[12:16].strip()=='CA':points.append([float(row[30:38]),float(row[38:46]),float(row[46:54]),float(row[60:66])])
 mean=[sum(p[j] for p in points)/len(points) for j in range(3)]
 points=[[round(p[j]-mean[j],3) for j in range(3)]+[p[3]] for p in points]
 def color(score):return '#1355ca' if score>=90 else '#65cbf3' if score>=70 else '#ffce31' if score>=50 else '#ed7327'
 scale=8;parts=[]
 for a,b in zip(points,points[1:]):
  parts.append(((a[2]+b[2])/2,line(390+a[0]*scale,240-a[1]*scale,390+b[0]*scale,240-b[1]*scale,color(a[3]),arrow=False,width=5)))
 drawing=''.join(s for _,s in sorted(parts))+txt(400,30,'Hemoglobin subunit alpha · P69905',18)+txt(400,475,'Cα座標を残基順につないだ表示。側鎖・原子の大きさは省略。',14)
 (ROOT/'assets/protein.svg').write_text(svg(drawing,500,label='AlphaFold DBのP69905の予測構造。色はpLDDT'),encoding='utf-8')
 (ROOT/'assets/protein-data.js').write_text('window.PROTEIN_POINTS = '+json.dumps(points)+';\n',encoding='utf-8')
 print('Protein:',len(points),'CA atoms, pLDDT',min(p[3] for p in points),max(p[3] for p in points))
