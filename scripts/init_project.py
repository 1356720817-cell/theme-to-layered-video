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
 shots=[{'id':'draft-01','start':0,'end':project['durationFrames'],'section':'main','chapter':'','title':a.topic,'subtitle':'制作预览：完成主题研究、正式分镜与专属素材后再导出成片','kicker':'','theme':'dark','camera':{'type':'still','amount':1},'transition':{'type':'cut','frames':0},'layers':[],'words':[]}]
 for name,data in [('project.json',project),('shots.json',shots),('assets.json',{'assets':[]})]:
  (public/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 subprocess.run([sys.executable,'-I',str(root/'scripts/production_gate.py'),'init',str(root)],check=True,capture_output=True)
 state={'topic':a.topic,'stage':'brief','delivery_status':'in_production','updated_at':datetime.now(timezone.utc).isoformat(),'completed_shot_ids':[],'pending_shot_ids':[],'audio':None,'checks':{},'next_action':'Research and storyboard the new theme; prepare actual music audition for confirmation and three visual anchors.'}
 (root/'production.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
 (root/'brief.md').write_text(f'# 本次主题：{a.topic}\n\n默认：中文、{a.width}×{a.height}、{a.fps}fps，策划目标约{a.seconds:g}秒，音乐驱动的图像叙事。\n\n重新研究本主题、设计论点和结构、逐镜专属素材、独立前后景、音乐卡点及多样运镜。参考旧片的制作方法，不沿用旧片具体内容。\n\n当前为draft工程，尚未制作成片。\n',encoding='utf-8')
 print(json.dumps({'project':str(root),'topic':a.topic,'status':'draft','next':'Author sources, storyboard, assets and audio before production rendering.'},ensure_ascii=True))
if __name__=='__main__':main()
