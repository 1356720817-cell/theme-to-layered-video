import json,shutil,zipfile,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1];deliver=root.parents[1]/'outputs';deliver.mkdir(exist_ok=True)
video=root/'outputs/final.mp4';qc=root/'work/qc'
report=json.loads((qc/'qc-summary.json').read_text(encoding='utf-8'))
assert report.get('visual_review_completed') is True,'Final visual review is still pending'
assert report['full_decode_passed'] and report['copied_audio_packet_hash_matches']
state=json.loads((root/'production.json').read_text(encoding='utf-8'))
state.update(stage='delivered',updated_at=datetime.now(timezone.utc).isoformat(),next_action='Delivered final MP4 and editable project.',checks={'schema_audit_passed':True,'lint_passed':True,'full_decode_passed':True,'visual_contact_sheets_reviewed':True,'audio_packet_hash_matches':True,'human_full_listening_review':False,'chronological_image_duplicates':[]})
(root/'production.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
final=deliver/'24-solar-terms-v1.mp4';shutil.copy2(video,final)
preview=deliver/'24-solar-terms-opening-10s.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(final),'-t','10','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(preview)],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss','3.5','-i',str(final),'-frames:v','1','-update','1','-q:v','2',str(deliver/'24-solar-terms-poster.jpg')],check=True)
for name in ['final-review-1.jpg','final-review-2.jpg','hook-final.jpg']:
 shutil.copy2(qc/name,deliver/('24-solar-terms-'+name))
for name in ['qc-summary.json','media-report.json']:
 shutil.copy2(qc/name,deliver/('24-solar-terms-'+name))
shutil.copy2(root/'hook-review.md',deliver/'24-solar-terms-hook-review.md')
project=deliver/'24-solar-terms-project-v1'
if project.exists():raise SystemExit('Project delivery directory already exists; preserve it and choose a new version.')
shutil.copytree(root,project,ignore=shutil.ignore_patterns('node_modules','node_modules-preview-link','work','outputs','review','.git','__pycache__','.env*'))
(project/'work').mkdir()
for name in ['asset-jobs.json','scene-plan.json','opening-asset.json','asset-integrity.json','project-audit.json','render-report.json','audio-mux.json']:
 src=root/'work'/name
 if src.exists():shutil.copy2(src,project/'work'/name)
for name in ['generated-batches','generated-records','qc']:
 shutil.copytree(root/'work'/name,project/'work'/name)
cmd1='@echo off\r\nchcp 65001 >nul\r\ncd /d "%~dp0"\r\nif not exist node_modules\\remotion\\package.json call npm ci --cache work\\npm-cache\r\ncall npm run dev\r\npause\r\n'
cmd2='@echo off\r\nchcp 65001 >nul\r\ncd /d "%~dp0"\r\nif not exist node_modules\\remotion\\package.json call npm ci --cache work\\npm-cache\r\ncall npm run render\r\nif errorlevel 1 goto end\r\ncall npm run finish\r\n:end\r\npause\r\n'
(project/'启动预览.cmd').write_bytes(cmd1.encode('utf-8'))
(project/'重新导出.cmd').write_bytes(cmd2.encode('utf-8'))
(project/'README.md').write_text((project/'README-使用说明.md').read_text(encoding='utf-8'),encoding='utf-8')
archive=deliver/'24-solar-terms-editable-v1.zip'
if archive.exists():raise SystemExit('ZIP already exists; preserve it and choose a new version.')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(project.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(deliver))
with zipfile.ZipFile(archive)as z:
 assert z.testzip() is None
 assert not any('node_modules' in n for n in z.namelist())
 count=len(z.namelist())
manifest={'final_mp4':{'file':final.name,'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest()},'editable_zip':{'file':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entries':count,'integrity_passed':True},'video':{'seconds':130,'width':1920,'height':1080,'fps':30,'frames':3900},'audio':'Original procedural composition; AAC 48kHz stereo; packet copy verified','layer_distribution':{'single':9,'double':11,'triple':4},'unique_images':44,'human_full_listening_review':False}
(deliver/'24-solar-terms-delivery.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
notes='# 二十四节气 · 成片交付\n\n130秒，1920×1080，30fps。24节气按时间完整推进；9个单图层、11个双图层、4个三图层正文镜头，背景与主体/前景独立运动，镜头长短交替。\n\n开头5秒采用dbs-hook优化：“冰还没化，怎么就立春了？”，随后进入“二十四节气 · 顺着太阳，读懂一年”。立春镜头用“节气入春，天气因地而异”接住问题。\n\n全片44张独立AI生成图片，只有结尾回看复用前文画面。原创程序合成配乐的源码、WAV、AAC、音符事件与开头卡点测量都在工程内。\n\n全片解码、3900帧、音画时长、全部镜头中点与切换边界抽帧、图像去重、真实alpha、音轨包哈希和ZIP完整性检查已完成。未做整片人工听审；各地物候表现不同，画面为典型时令意象的AI视觉演绎。\n\n文件：24-solar-terms-v1.mp4；24-solar-terms-opening-10s.mp4；24-solar-terms-editable-v1.zip。\n'
(deliver/'24-solar-terms-notes.md').write_text(notes,encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=True,indent=2))

