import json,subprocess,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
targets={int((s['start']+s['end'])//2) for s in shots}
targets.update([0,18,38,60,80,105,140])
anchors=[s for s in shots if s.get('index') in [5,9,15,21]]
for s in anchors:targets.update([s['start']+12,(s['start']+s['end'])//2,s['end']-1])
subprocess.run(['node','preview.mjs']+[str(x) for x in sorted(targets)],cwd=root,check=True)
font=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',20)
def sheet(rows,dest,cols=3):
 out=Image.new('RGB',(480*cols,300*math.ceil(len(rows)/cols)),'#14171b');d=ImageDraw.Draw(out)
 for i,(frame,label) in enumerate(rows):
  im=Image.open(root/f'work/preview-stills/frame-{frame:05d}.jpg');im.thumbnail((480,270));x=i%cols*480;y=i//cols*300;out.paste(im,(x,y));d.text((x+8,y+273),label,font=font,fill='white')
 out.save(dest,quality=94)
for part in range(2):
 subset=shots[part*13:(part+1)*13];sheet([((s['start']+s['end'])//2,s['title']+' | '+str(len(s['layers']))+'层 | '+s['camera']['type']) for s in subset],root/f'work/storyboard-review-{part+1}.jpg')
sheet([(f,f'{s["title"]} | {f/30:.2f}s') for s in anchors for f in [s['start']+12,(s['start']+s['end'])//2,s['end']-1]],root/'work/anchor-motion-review.jpg')
sheet([(f,f'opening {f/30:.2f}s') for f in [0,18,38,60,80,105,140]],root/'work/opening-review.jpg')
print('Review images ready')

