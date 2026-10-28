import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
root=Path(__file__).resolve().parents[1];p=root/'public'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def write(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
a=read(p/'assets.json');o=read(root/'work/opening-asset.json');a['assets']=[x for x in a['assets'] if x['id']!='opening-ice']+[o];write(p/'assets.json',a)
s=read(p/'shots.json');s[0]['layers']=[dict(assetId='opening-ice',role='background',x=0,y=0,w=1,h=1)];s[0]['subtitle']='����û������ô�������ˣ�';s[0]['words']=[dict(text='����û��',frame=0),dict(text='��ô��������',frame=37),dict(text='��ʮ�Ľ���',frame=75),dict(text='˳��̫��������һ��',frame=102)];write(p/'shots.json',s)
rows=[];seen={}
for x in a['assets']:
 f=p/x['file'];h=hashlib.sha256(f.read_bytes()).hexdigest();assert h not in seen,(x['id'],seen.get(h));seen[h]=x['id'];im=Image.open(f);alpha=im.getchannel('A').getextrema() if 'A' in im.getbands() else None
 if x['alpha']:assert alpha and alpha[0]==0,x['id']
 rows.append(dict(id=x['id'],file=x['file'],ownerShot=x['ownerShot'],sha256=h,size=im.size,alpha_extrema=alpha))
write(root/'work/asset-integrity.json',dict(unique_count=len(rows),chronological_duplicates=[],images=rows))
state=read(root/'production.json');state.update(stage='preview',updated_at=datetime.now(timezone.utc).isoformat(),selected_assets=[x['id'] for x in a['assets']],audio=read(p/'project.json')['audio'],next_action='Inspect full storyboard midpoints and multi-layer starts/ends, refine, then render and verify final MP4.');write(root/'production.json',state)
text=(root/'script.md').read_text(encoding='utf-8').replace('���԰ס�������̫���ػƵ�ÿ��15�㣬ʱ�������һ�����֡�','���԰ס�����������û������ô�������ˣ�������⡰��ʮ�Ľ��� �� ˳��̫��������һ�ꡱ��')
(root/'script.md').write_text(text,encoding='utf-8')
(root/'outline.md').write_text('# ��Ƭ����\n\n130�룬1920��1080��30fps�����԰ס�����5���ñ��淴�����ʣ����İ����������ƽ�120�룻��β5��ؿ��ļ���\n\nÿ������30�룬���ľ�ͷ��3.75��5��6.25�뽻�档������Ϊ9����ͼ�㡢11��˫ͼ�㡢4����ͼ�㾵ͷ�����������֡�ʱ��������Ŀ̶�Ϊ����ͼ�β㡣������ʱ�䡢������л���storyboard.md��ԭʼ��ͼ��������ʾ�ʼ�public/assets.json��\n\n�û���ȷ����������ˮ������Ȩ�������ʣ��ȫ��������ͼ����䡢��������Ƶ���ࣻ�������ŵȴ�ȷ�ϡ�\n',encoding='utf-8')
(root/'music-plan.md').write_text('# ��ʵʩ����\n\nԭ������ϳ����֣�96BPM��4/4�ġ�130�롣���Ʋ��ҡ���Ϣ��������ͺ������͹ĺ�ľ�ʴ���֣��ļ������𲽸ı��ܶȡ�û���ⲿ����¼����\n\n������ͷ��1.5��2��2.5С�ڱ��ţ���Ƶ֡�������¼�����ȡ�������֡�����������Ϊ0��1.25��2.5��4.375��5�룬ʵ�ʲ��β�����¼��music-composition.json��\n\n�ɱ༭�ϳ�Դ�룺scripts/compose_music.py������Դ��public/assets/solar-terms-original.wav����Ƭʵ��ʹ�����죺public/assets/solar-terms-original.m4a�����պϳɸ���AAC��Ƶ�������˶԰���ϣ��δ�������˹�����\n',encoding='utf-8')
print(json.dumps(dict(assets=len(rows),shots=len(s),ready=True),ensure_ascii=True))

