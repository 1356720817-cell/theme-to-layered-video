from pathlib import Path
import subprocess
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
out=root/'work/reference-study';out.mkdir(exist_ok=True)
source=root.parent/'douyin-reference/video.mp4'
times=[23.1,23.5,23.9,36.1,36.5,36.9,49.2,49.7,50.2,73.2,73.7,74.2]
sheet=Image.new('RGB',(1440,1200),'#181818')
font=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',22)
for i,t in enumerate(times):
 p=out/f'{i:02d}.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1','-update','1','-q:v','2',str(p)],check=True)
 im=Image.open(p);im.thumbnail((480,270));x=(i%3)*480;y=(i//3)*300
 sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x+12,y+273),f'{t:.1f}s',font=font,fill='white')
sheet.save(out/'source-motion-samples.jpg',quality=94)
print(out/'source-motion-samples.jpg')

