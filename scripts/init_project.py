import argparse,json,shutil,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description='Create a clean, theme-independent layered-video project.')
 p.add_argument('--topic',required=True);p.add_argument('--output',required=True)
 p.add_argument('--seconds',type=float,default=130);p.add_argument('--width',type=int,default=1920);p.add_argument('--height',type=int,default=1080);p.add_argument('--fps',type=int,default=30)
 a=p.parse_args();root=Path(a.output).expanduser().resolve()
 if root.exists():raise SystemExit('Refusing to overwrite an existing project: '+str(root))
 if min(a.seconds,a.width,a.height,a.fps)<=0:raise SystemExit('Duration, dimensions and fps must be positive.')
 starter=Path(__file__).resolve().parents[1]/'assets/starter'
 shutil.copytree(starter,root,ignore=shutil.ignore_patterns('node_modules','work','outputs','.git','.env*','__pycache__'));public=root/'public';public.mkdir(exist_ok=True);(public/'assets').mkdir(exist_ok=True)
 (root/'scripts').mkdir(exist_ok=True)
 for helper in ['audit_project.py','verify_media.py','make_rhythm_track.py','analyze_audio.py','production_gate.py','prepare_music.py','verify_audio.py','measure_audio.py','inspect_reference.py','package_project.py']:
  shutil.copy2(Path(__file__).resolve().parent/helper,root/'scripts'/helper)
 project={'topic':a.topic,'status':'draft','width':a.width,'height':a.height,'fps':a.fps,'durationFrames':round(a.seconds*a.fps),'language':'zh-CN','palette':{'dark':'#080a0d','paper':'#e4d8b9','accent':'#e4b264','text':'#f0e5cd','ink':'#25251f'},'fonts':{'serif':'KaiTi, SimSun, serif','sans':'Microsoft YaHei, sans-serif'},'audio':{'file':'','required':True,'source':'','rights':'','offsetSeconds':0,'copy':False},'chapters':[],'beats':[]}
 shots=[{'id':'draft-01','start':0,'end':project['durationFrames'],'section':'main','chapter':'','title':a.topic,'subtitle':'����Ԥ������������о�����ʽ�־���ר���زĺ��ٵ�����Ƭ','kicker':'','theme':'dark','camera':{'type':'still','amount':1},'transition':{'type':'cut','frames':0},'layers':[],'words':[]}]
 for name,data in [('project.json',project),('shots.json',shots),('assets.json',{'assets':[]})]:
  (public/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 subprocess.run([sys.executable,'-I',str(root/'scripts/production_gate.py'),'init',str(root)],check=True,capture_output=True)
 state={'topic':a.topic,'stage':'brief','delivery_status':'in_production','updated_at':datetime.now(timezone.utc).isoformat(),'completed_shot_ids':[],'pending_shot_ids':[],'audio':None,'checks':{},'next_action':'Research and storyboard the new theme; prepare actual music audition for confirmation and three visual anchors.'}
 (root/'production.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
 (root/'brief.md').write_text(f'# �������⣺{a.topic}\n\nĬ�ϣ����ġ�{a.width}��{a.height}��{a.fps}fps���߻�Ŀ��Լ{a.seconds:g}�룬����������ͼ�����¡�\n\n�����о������⡢����۵�ͽṹ����ר���زġ�����ǰ�󾰡����ֿ��㼰�����˾����ο���Ƭ�����������������þ�Ƭ�������ݡ�\n\n��ǰΪdraft���̣���δ������Ƭ��\n',encoding='utf-8')
 print(json.dumps({'project':str(root),'topic':a.topic,'status':'draft','next':'Author sources, storyboard, assets and audio before production rendering.'},ensure_ascii=True))
if __name__=='__main__':main()
