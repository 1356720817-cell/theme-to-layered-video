import json,subprocess,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
root=Path(__file__).resolve().parents[1];work=root/'work/qc';work.mkdir(exist_ok=True)
video=root/'outputs/final.mp4'
subprocess.run(['python','-I',str(root/'scripts/verify_media.py'),str(root),'--video',str(video)],check=True)
report=json.loads((work/'media-report.json').read_text(encoding='utf-8'));shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
project=json.loads((root/'public/project.json').read_text(encoding='utf-8'));fps=project['fps'];total_frames=project['durationFrames'];seconds=total_frames/fps
index={x['frame']:root/x['file'] for x in report['review_frame_index']}
hook=[0,18,38,60,80,105,140]
folder=work/'hook';folder.mkdir(exist_ok=True)
selector='+'.join('eq(n'+chr(92)+','+str(n)+')' for n in hook)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf','select='+selector+',scale=960:-1','-q:v','2','-fps_mode','vfr','-start_number','1',str(folder/'frame-%03d.jpg')],check=True)
for n,f in zip(hook,sorted(folder.glob('frame-*.jpg'))):index[n]=f
font=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',20)
def sheet(rows,path,cols=3,w=480,h=270):
 im=Image.new('RGB',(cols*w,(h+32)*math.ceil(len(rows)/cols)),'#15191f');d=ImageDraw.Draw(im)
 for i,(frame,label) in enumerate(rows):
  thumb=Image.open(index[frame]);thumb.thumbnail((w,h));x=i%cols*w;y=i//cols*(h+32);im.paste(thumb,(x,y));d.text((x+7,y+h+4),label,font=font,fill='#eee6d8')
 im.save(path,quality=94)
for part in range(2):
 sub=shots[part*13:(part+1)*13]
 sheet([(105 if s['id']=='opening' else (s['start']+s['end'])//2,s['title']+' | '+str(len(s['layers']))+'层') for s in sub],work/f'final-review-{part+1}.jpg')
sheet([(n,f'开场 {n/30:.2f}s') for n in hook],work/'hook-final.jpg')
boundaries=shots[1:]
for part in range(math.ceil(len(boundaries)/7)):
 rows=[(max(0,min(total_frames-1,s['start']+off)),s['title']+' '+str(off)) for s in boundaries[part*7:(part+1)*7] for off in [-1,0,3,8]]
 sheet(rows,work/f'boundaries-{part+1}.jpg',cols=4,w=320,h=180)
blank=[]
for n,file in index.items():
 im=np.asarray(Image.open(file).convert('RGB'));crop=im[:,im.shape[1]//2:];sd=float(crop.std());mean=float(crop.mean())
 if sd<1 and (mean<3 or mean>252):blank.append(n)
assert not blank,blank
dark_flashes=[]
for s in shots[1:]:
 if not s['transition']['frames']:continue
 means=[]
 for n in [s['start']-1,s['start'],s['start']+8]:
  a=np.asarray(Image.open(index[n]).convert('RGB'));means.append(float(a[:,a.shape[1]//2:].mean()))
 if min(means[0],means[2])>15 and means[1]<min(means[0],means[2])*.30:dark_flashes.append({'shot':s['id'],'means':means})
assert not dark_flashes,dark_flashes
names=[s['title'] for s in shots if s['section']=='main']
expected='立春 雨水 惊蛰 春分 清明 谷雨 立夏 小满 芒种 夏至 小暑 大暑 立秋 处暑 白露 秋分 寒露 霜降 立冬 小雪 大雪 冬至 小寒 大寒'.split()
assert names==expected
raw=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vn','-f','f32le','-acodec','pcm_f32le','-'],check=True,capture_output=True).stdout
pcm=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
aprobe=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=sample_rate','-of','json',str(video)],check=True,capture_output=True,text=True).stdout);sr=int(aprobe['streams'][0]['sample_rate'])
rms=[float(np.sqrt(np.mean(pcm[i*sr:min((i+1)*sr,len(pcm))]**2))) for i in range(math.ceil(seconds))]
audio={'decoded_sample_rate':sr,'decoded_sample_peak':float(np.max(np.abs(pcm))),'samples_at_or_above_full_scale':int(np.sum(np.abs(pcm)>=.999)),'rms_by_second':rms,'unexpected_near_silent_seconds':[i for i,v in enumerate(rms[:-1]) if v<.0001]}
assert audio['samples_at_or_above_full_scale']==0
assert not audio['unexpected_near_silent_seconds']
report.update({'unexpected_blank_frames':blank,'solar_terms_in_order':names,'chronological_image_duplicates':json.loads((root/'work/asset-integrity.json').read_text(encoding='utf-8'))['chronological_duplicates'],'main_layer_distribution':{str(k):sum(len(s['layers'])==k for s in shots if s['section']=='main') for k in [1,2,3]},'audio_analysis':audio,'opening_review_frames':hook,'visual_review_completed':False,'human_full_listening_review':False,'scope_note':'Full decode, dimensions/timing/audio packet checks, all scene midpoints and all boundary samples; final visual contact sheets require explicit review.'})
report['unexpected_dark_flashes']=dark_flashes
sync=json.loads((root/'work/music-sync.json').read_text(encoding='utf-8'))
report['music_sync']={'source_song':sync['track'],'artist':sync['artist'],'source_excerpt_seconds':sync['excerpt_source_seconds'],'main_climax_source_seconds':sync['main_climax_source_seconds'],'measured_grid_seconds':sync['measured_pulse_seconds'],'main_boundary_count':len(sync['boundaries']),'maximum_grid_alignment_error_frames':max(abs(b['grid_error_frames']) for b in sync['boundaries']),'method':sync['method'],'full_human_listening_review':False}
report['intentional_arrangement_break_seconds']=[22.2,23.4]
report['climax_video_start_seconds']=25
(work/'qc-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['review_frame_index','audio_analysis']},ensure_ascii=True,indent=2))

