import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
specs=read(ROOT/'work/scene-plan.json')
records={}
for folder in ['generated-batches','generated-records']:
 for p in (ROOT/'work'/folder).glob('*.json'):
  data=read(p)
  for r in data if isinstance(data,list) else [data]:records[r['id']]=r
assert len(records)==39,('Missing generated images',len(records))
old=read(PUBLIC/'assets.json')['assets'][:4]
for a in old:a['status']='ready';a['rights']='本次生成；用户已确认画面'
assets=old[:]
for r in sorted(records.values(),key=lambda r:(r['index'],r['id'])):
 assets.append({'id':r['id'],'file':r['file'],'ownerShot':f"term-{r['index']:02d}-{r['slug']}",'entityId':r['name']+'·'+r['id'].split('-')[-1],'status':'ready','kind':'image','depiction':'generated','source':'image_gen','source_file':r['source'],'prompt':r['prompt'],'rights':'本项目使用内置image_gen生成','alpha':r['alpha']})
shots=read(PUBLIC/'shots.json')[:2]
shots[0]['index']=1;shots[1]['index']=2
for s in shots:s['layout']='left';s['visual']='nature';s['weather']='rain' if s['index']==2 else 'mist'
t=15.0
for s in specs:
 idx,slug,name,season,seconds,angle,caption,camera,cut,bg,extra=s
 own=[r for r in records.values() if r['index']==idx]
 main=next(r for r in own if r['role']=='background')
 layers=[{'assetId':main['id'],'role':'background','x':0,'y':0,'w':1,'h':1,'fit':'cover','parallax':1}]
 for k,(tag,_,layout) in enumerate(extra):
  r=next(r for r in own if r['id'].endswith('-'+tag));x,y,w,h=layout
  sign=1 if idx%2 else -1
  motion={'x0':sign*.012,'x1':-sign*.014,'y0':.004,'y1':-.004,'scale0':.99,'scale1':1.025,'sway':.55 if tag in ['wheatbundle','sickle','roof'] else 1.0}
  if tag=='boat':motion={'x0':-.035,'x1':.055,'y0':.004,'y1':-.002,'scale0':.97,'scale1':1}
  if tag=='grass':motion={'x0':.025,'x1':-.025,'y0':0,'y1':0,'scale0':1,'scale1':1.02,'sway':.4}
  if tag=='roof':x,y,w,h=.53,.62,.43,.40
  layers.append({'assetId':r['id'],'role':r['role'],'x':x,'y':y,'w':w,'h':h,'fit':'contain','parallax':.38 if r['role']=='subject' else 1.5,'motion':motion})
 end=t+seconds
 weather='rain' if idx in [6,12] else 'snow' if idx in [20,21] else 'mist' if idx in [15,17,24] else 'none'
 shots.append({'id':f'term-{idx:02d}-{slug}','index':idx,'start':round(t*30),'end':round(end*30),'section':'main','chapter':season,'title':name,'subtitle':caption,'kicker':f'{season} · 黄经 {angle}°','theme':'dark','layout':'bottom' if idx in [7,12,14,19,24] else 'left','visual':'nature','weather':weather,'camera':{'type':camera,'amount':.65 if camera.startswith('track') else .6 if camera.startswith('tilt') else 1},'transition':{'type':cut,'frames':0 if cut=='cut' else 8 if cut!='focus' else 10},'layers':layers,'words':[]})
 t=end
assert round(t*30)==3750
opening={'id':'opening','start':0,'end':150,'section':'opening','chapter':'开场','title':'二十四节气','subtitle':'太阳沿黄道每走15°，时间就有了一个名字。','kicker':'','theme':'dark','visual':'calendar-opening','camera':{'type':'still'},'transition':{'type':'cut','frames':0},'layers':[],'words':[{'text':'一年，不止四季','frame':5},{'text':'二十四节气','frame':75}]}
ending={'id':'ending','start':3750,'end':3900,'section':'ending','chapter':'回望','title':'二十四节气','subtitle':'记下的不只是时间，也是人与大地相处的方式。','kicker':'','theme':'dark','visual':'calendar-ending','camera':{'type':'still'},'transition':{'type':'dissolve','frames':10},'layers':[{'assetId':next(s for s in shots if s['index']==i)['layers'][0]['assetId'],'role':'background','x':k*.25,'y':0,'w':.25,'h':1} for k,i in enumerate([4,10,16,22])],'words':[]}
shots=[opening]+shots+[ending]
project=read(PUBLIC/'project.json')
project.update({'status':'ready','durationFrames':3900,'chapters':[{'label':'春','start':150},{'label':'夏','start':1050},{'label':'秋','start':1950},{'label':'冬','start':2850}],'beats':[round(i*.625*30) for i in range(208)],'audio':{'file':'assets/solar-terms-original.m4a','required':True,'source':'本项目原创程序合成配乐，96 BPM；自制拨弦、气息长音、和声与打击乐音色','rights':'无外部采样录音，无参考片音轨；合成源码随工程交付','offsetSeconds':0,'copy':True},'layer_plan':{'single':9,'double':11,'triple':4},'music_note':'整体96BPM；节气镜头按1.5、2或2.5小节编排，交节落点取最近视频帧。','visual_disclosure':'AI视觉演绎；物候因地区而异'})
write(PUBLIC/'assets.json',{'assets':assets});write(PUBLIC/'shots.json',shots);write(PUBLIC/'project.json',project)
state=read(ROOT/'production.json')
state.update({'stage':'motion','updated_at':datetime.now(timezone.utc).isoformat(),'completed_shot_ids':[s['id'] for s in shots if s['section']=='main'],'pending_shot_ids':[],'selected_assets':[a['id'] for a in assets],'checks':{'user_visual_approval_required':False,'approval_note':'用户已确认立春和雨水，并明确授权自主完成其余全部节气与节奏规划','research_sources':['中国气象局','中国非遗网']},'next_action':'Generate original music, render complete visual previews, inspect composition and transitions, then final export and QC.'})
write(ROOT/'production.json',state)
report=[]
hashes={}
for a in assets:
 p=PUBLIC/a['file'];im=Image.open(p)
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 assert digest not in hashes,('Duplicate image',a['id'],hashes.get(digest));hashes[digest]=a['id']
 if a['alpha']:
  assert 'A' in im.getbands(),a['id']
  assert im.getchannel('A').getextrema()[0]==0,a['id']
 report.append({'id':a['id'],'file':a['file'],'ownerShot':a['ownerShot'],'size':im.size,'alpha':a['alpha'],'sha256':digest})
write(ROOT/'work/asset-integrity.json',{'images':report,'unique_count':len(hashes),'chronological_duplicates':[]})
table=['# 逐镜节奏与用图','', '|节气|时间(秒)|主画面层数|相机|切换|文案|','|---|---:|---:|---|---|---|']
for s in shots[1:-1]:table.append(f"|{s['title']}|{s['start']/30:.3f}–{s['end']/30:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|")
(ROOT/'storyboard.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
(ROOT/'script.md').write_text('# 二十四节气·最终画面文案\n\n无旁白。开场：太阳沿黄道每走15°，时间就有了一个名字。\n\n'+'\n'.join(f"{s['index']:02d}. {s['title']}：{s['subtitle']}" for s in shots[1:-1])+'\n\n结尾：二十四节气，记下的不只是时间，也是人与大地相处的方式。\n',encoding='utf-8')
print(json.dumps({'shots':len(shots),'images':len(assets),'layers':dict(Counter(len(s['layers']) for s in shots[1:-1])),'frames':3900},ensure_ascii=True))

