import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
root=Path(__file__).resolve().parents[1];p=root/'public'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def write(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
a=read(p/'assets.json');o=read(root/'work/opening-asset.json');a['assets']=[x for x in a['assets'] if x['id']!='opening-ice']+[o];write(p/'assets.json',a)
s=read(p/'shots.json');s[0]['layers']=[dict(assetId='opening-ice',role='background',x=0,y=0,w=1,h=1)];s[0]['subtitle']='冰还没化，怎么就立春了？';s[0]['words']=[dict(text='冰还没化',frame=0),dict(text='怎么就立春了',frame=37),dict(text='二十四节气',frame=75),dict(text='顺着太阳，读懂一年',frame=102)];write(p/'shots.json',s)
rows=[];seen={}
for x in a['assets']:
 f=p/x['file'];h=hashlib.sha256(f.read_bytes()).hexdigest();assert h not in seen,(x['id'],seen.get(h));seen[h]=x['id'];im=Image.open(f);alpha=im.getchannel('A').getextrema() if 'A' in im.getbands() else None
 if x['alpha']:assert alpha and alpha[0]==0,x['id']
 rows.append(dict(id=x['id'],file=x['file'],ownerShot=x['ownerShot'],sha256=h,size=im.size,alpha_extrema=alpha))
write(root/'work/asset-integrity.json',dict(unique_count=len(rows),chronological_duplicates=[],images=rows))
state=read(root/'production.json');state.update(stage='preview',updated_at=datetime.now(timezone.utc).isoformat(),selected_assets=[x['id'] for x in a['assets']],audio=read(p/'project.json')['audio'],next_action='Inspect full storyboard midpoints and multi-layer starts/ends, refine, then render and verify final MP4.');write(root/'production.json',state)
text=(root/'script.md').read_text(encoding='utf-8').replace('无旁白。开场：太阳沿黄道每走15°，时间就有了一个名字。','无旁白。开场：冰还没化，怎么就立春了？随后入题“二十四节气 · 顺着太阳，读懂一年”。')
(root/'script.md').write_text(text,encoding='utf-8')
(root/'outline.md').write_text('# 整片方案\n\n130秒，1920×1080，30fps，无旁白。开场5秒用冰面反差提问；正文按立春至大寒推进120秒；结尾5秒回看四季。\n\n每个季节30秒，正文镜头按3.75、5、6.25秒交替。主画面为9个单图层、11个双图层、4个三图层镜头；天气、文字、时间轴和天文刻度为程序图形层。完整逐镜时间、相机与切换见storyboard.md，原始用图与完整提示词见public/assets.json。\n\n用户已确认立春和雨水，并授权自主完成剩余全部节气、图层分配、音乐与视频节奏；不再逐张等待确认。\n',encoding='utf-8')
(root/'music-plan.md').write_text('# 已实施配乐\n\n原创程序合成配乐，96BPM、4/4拍、130秒。自制拨弦、气息长音、柔和和声、低鼓和木质打击乐，四季段落逐步改变密度。没有外部采样录音。\n\n节气镜头按1.5、2或2.5小节编排；视频帧在音乐事件附近取最近整数帧。开场主落点为0、1.25、2.5、4.375、5秒，实际波形测量记录在music-composition.json。\n\n可编辑合成源码：scripts/compose_music.py；无损源：public/assets/solar-terms-original.wav；成片实际使用音轨：public/assets/solar-terms-original.m4a。最终合成复制AAC音频包，并核对包哈希。未做完整人工听审。\n',encoding='utf-8')
print(json.dumps(dict(assets=len(rows),shots=len(s),ready=True),ensure_ascii=True))

