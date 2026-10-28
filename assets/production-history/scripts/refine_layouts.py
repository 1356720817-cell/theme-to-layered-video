import json
from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'public/shots.json';shots=json.loads(p.read_text(encoding='utf-8'))
for s in shots:
 i=s.get('index');layers=s['layers']
 if i==5:
  l=layers[1];l.update(x=.30,y=.56,w=.33,h=.255);l['motion'].update(x0=-.015,x1=.045,y0=.004,y1=-.002)
 if i==6:layers[1].update(x=.48,y=.52,w=.52,h=.72)
 if i==8:layers[1].update(y=.23,h=.88)
 if i==13:layers[1].update(x=.50,y=-.13,w=.50,h=.95)
 if i==18:layers[1].update(x=.50,y=-.20,w=.55,h=.90)
 if i==23:layers[1].update(x=.40,y=.22,w=.62,h=.92)
p.write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
print('Layout refinements applied')

