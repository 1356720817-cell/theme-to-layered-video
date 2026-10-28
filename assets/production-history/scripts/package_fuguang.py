import json,shutil,zipfile,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
deliver=root.parents[1]/'outputs';deliver.mkdir(exist_ok=True)
prefix='24-solar-terms-poetry-v5'
qc=root/'work/qc';report=json.loads((qc/'qc-summary.json').read_text(encoding='utf-8'))
assert report.get('visual_review_completed') is True
assert report['full_decode_passed'] and report['copied_audio_packet_hash_matches']
assert not report['unexpected_blank_frames'] and not report['unexpected_dark_flashes']
assert not report['chronological_image_duplicates']
final=deliver/(prefix+'.mp4');preview=deliver/(prefix+'-opening-35s.mp4');project=deliver/(prefix+'-project');archive=deliver/(prefix+'-project.zip')
assert not any(p.exists() for p in [final,preview,project,archive]),'V5 delivery already exists; preserve it and select the next version.'
state=json.loads((root/'production.json').read_text(encoding='utf-8'))
state.update(stage='delivered',updated_at=datetime.now(timezone.utc).isoformat(),next_action='Delivered V5 with poetry in all 24 terms; approved V4 audio and timing preserved.',checks={'schema_audit_passed':True,'lint_passed':True,'full_decode_passed':True,'visual_contact_sheets_reviewed':True,'audio_packet_hash_matches':True,'human_full_listening_review':False,'chronological_image_duplicates':[],'poetry_count':24,'poetry_text_and_attribution_checked':True,'audio_unchanged_from_v4':True,'climax_video_start_seconds':25})
(root/'production.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(root/'outputs/final.mp4',final)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(final),'-t','35','-vf','scale=1280:-2','-c:v','libx264','-crf','20','-preset','fast','-c:a','copy','-movflags','+faststart',str(preview)],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss','6','-i',str(final),'-frames:v','1','-update','1','-q:v','2',str(deliver/(prefix+'-poster.jpg'))],check=True)
for name in ['final-review-1.jpg','final-review-2.jpg','hook-final.jpg','qc-summary.json','media-report.json']:
 shutil.copy2(qc/name,deliver/(prefix+'-'+name))
shutil.copy2(root/'work/music-sync.json',deliver/(prefix+'-music-sync.json'))
shutil.copy2(root/'poetry-sources.md',deliver/(prefix+'-poems.md'))
excluded=['node_modules','node_modules-preview-link','work','outputs','review','.git','__pycache__','.env*','solar-terms-original.wav','solar-terms-original.m4a','fuguang-highlight-108s.m4a','fuguang-progressive-120s.m4a','music-composition.json','assemble_project.py','finalize_plan.py','compose_music.py','package_final.py','make_rhythm_track.py','reference_study.py','refine_layouts.py','update_revision_docs.py','write_v3_docs.py','write_v4_docs.py','retime_fuguang.py','render_prefix_fix.mjs']
shutil.copytree(root,project,ignore=shutil.ignore_patterns(*excluded))
(project/'work').mkdir()
for name in ['asset-jobs.json','scene-plan.json','opening-asset.json','asset-integrity.json','project-audit.json','render-report.json','audio-mux.json','music-sync.json','fuguang-analysis.json','fuguang-waveform.png','audio-offset-check.json','audio-level-check.json','poetry-check.json']:
 src=root/'work'/name
 if src.exists():shutil.copy2(src,project/'work'/name)
for name in ['generated-batches','generated-records','qc']:
 shutil.copytree(root/'work'/name,project/'work'/name)
(project/'README.md').write_text((project/'README-ʹ��˵��.md').read_text(encoding='utf-8'),encoding='utf-8')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for file in sorted(project.rglob('*')):
  if file.is_file():z.write(file,file.relative_to(deliver))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 names=z.namelist();assert not any('/node_modules/' in n or '.env' in Path(n).name for n in names)
 assert any(n.endswith('/public/assets/fuguang-25s-drop-128s.m4a') for n in names)
 assert any(n.endswith('/public/assets/fuguang-jannik-full.mp3') for n in names)
 count=len(names)
manifest={'version':'Poetry V5','final_mp4':{'file':final.name,'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest()},'preview_mp4':{'file':preview.name,'seconds':35},'editable_zip':{'file':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entries':count,'integrity_passed':True},'video':{'seconds':128,'width':1920,'height':1080,'fps':30,'frames':3840},'audio':{'song':'���� (The History)','artist':'Jannik','source':'https://music.163.com/song?id=1394601255','source_excerpt_seconds':[77,205],'climax_video_start_seconds':25,'unchanged_from_v4':True,'aac_packet_copy_verified':True,'public_or_commercial_rights_verified':False},'poetry':{'terms_with_verse':24,'single_line_fast_shots':6,'text_and_attribution_checked':True,'source_list':prefix+'-poems.md'},'main_layer_distribution':{'single':9,'double':11,'triple':4},'unique_images':44,'human_full_listening_review':False}
(deliver/(prefix+'-delivery.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(deliver/(prefix+'-notes.md')).write_text('''# ��ʮ�Ľ��� �� ʫ�ʰ� V5

128�룬1920��1080��30fps����ǰ�汾������

ÿ����������һ��ʫ�ʽ�ѡ��������ƪ�����ϳ���ͷ��һ����3��̾�ͷֻ��һ�䡣����ů�������ַ��е��룬������λ�÷������»����ϣ�â�ֵ��������Ա���ũ�±�ǩ��24���˶���Դ�湤�̺Ͷ����嵥������

���֡�������25��߳�����ʱ����V4һ�£����ı��û���ȷ�ϵ�����������

����44�Ŷ���ͼ��9����ͼ�㡢11��˫ͼ�㡢4����ͼ�����ģ�ǰ����ѡ��������΢�ص����������������˾�����ʱ�����˾���ת��������ȷ�ϵ�V4������ʫ��ʹ�ö������ֶ�Ч������Ϊ�����⡷��Jannik��

��飺ȫƬ���롢3840֡������ʱ����24����˳����ʫ�䡢ÿ���е��ȫ���л��߽��֡���ز�ȥ�ء�V4����һ���ԡ���Ƶ����ϣ��ZIP�����ԡ�δ�������˹������Զ�������֡�����������˹�����

���ְ�Ȩ��Ȩ���ˣ���Դ����Ȩ���鷶Χ�Ѽ�¼�ڹ����ڡ�
''',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=True,indent=2))
