"""Retiming uses measured .25s subdivisions and 1.5s accent groups of the approved recording."""
import json,subprocess,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np

root=Path(__file__).resolve().parents[1]
public=root/'public';work=root/'work'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
p=load(public/'project.json');shots=load(public/'shots.json');analysis=load(work/'fuguang-analysis.json')
fps=30;offset=77.0;duration=128.0;main_start=150
patterns=[[6,6,8,7.5,9,7.5],[3,4.5,4.5,3,4.5,4.5],[4.5,3,4.5,4.5,4.5,3],[4.5,3,4.5,4.5,3,4.5]]
cursor=main_start;boundaries=[]
for i,s in enumerate([s for s in shots if s['section']=='main']):
 seconds=patterns[i//6][i%6];s['start']=cursor;s['end']=cursor+round(seconds*fps)
 s['music']={'source_start_seconds':offset+s['start']/fps,'source_end_seconds':offset+s['end']/fps,'pulse_seconds':.5,'duration_pulses':seconds/.5,'entry_on_measured_grid':True}
 # A few selected accents move the subject; continuous environment motion stays independent.
 s['accentFrames']=[] if i<3 else ([0,90] if i==3 else ([45] if seconds>=4.5 else []))
 s['accentStrength']=.010 if len(s['layers'])==1 else .018
 s['labelCueFrames']={'kicker':0,'title':0,'subtitle':7}
 # Cut the energetic seasonal landings immediately; retain different transitions inside a season.
 if i==0:s['transition']={'type':'dissolve','frames':10}
 elif i%6==0 or i==3:s['transition']={'type':'cut','frames':0}
 else:s['transition']['frames']=0 if s['transition']['type']=='cut' else min(s['transition']['frames'],7)
 boundaries.append({'shot':s['id'],'title':s['title'],'film_frame':cursor,'source_seconds':offset+cursor/fps,'duration_seconds':seconds,'transition':s['transition']})
 cursor=s['end']
opening=shots[0];opening['start']=0;opening['end']=150
opening['words']=[{'text':'冰还没化','frame':0},{'text':'怎么就立春了','frame':30},{'text':'二十四节气','frame':75},{'text':'顺着太阳，读懂一年','frame':105}]
opening['music']={'source_start_seconds':77.0,'question_second_frame':30,'arrangement_break_video_seconds':[22.2,23.4],'title_frame':75,'pickup_tagline_frame':105,'main_drop_frame':750,'main_drop_shot':'春分','opening_fade_in_seconds':1.25}
ending=shots[-1];ending['start']=cursor;ending['end']=3840;ending['transition']={'type':'dissolve','frames':7};ending['accentFrames']=[]
ending['music']={'source_start_seconds':198.0,'arrangement_release_frame':45,'subtitle_frame':45,'tail_fade_seconds':2.0}
assert cursor==3630
p['durationFrames']=3840
p['audio']={'file':'assets/fuguang-25s-drop-128s.m4a','required':True,'source':'Jannik《浮光 (The History)》，网易云音乐 song 1394601255；原曲77.000–205.000秒连续截取，第25秒进入高潮','source_url':'https://music.163.com/song?id=1394601255','rights':'用户指定用于本次本地视频编辑；音乐版权归权利人，公开发布及商业授权未核验；非本项目原创音乐','offsetSeconds':0,'copy':True,'originalOffsetSeconds':77.0,'fullSourceFile':'assets/fuguang-jannik-full.mp3','gain':.39,'gainDbComparedToV3':-6.020599913,'fadeInSeconds':1.25,'fadeOutSeconds':2.0}
p['chapters']=[{'label':s,'start':f} for s,f in zip('春夏秋冬',[150,1470,2190,2910])]
p['beats']=[round((t-offset)*fps) for t in np.arange(77,205,.5)]
p['music_note']='V4：音乐降低约6dB。原曲77–205秒连续片段，第25秒对应原曲102秒高潮，切入春分。春季44秒，夏秋冬各24秒；实测0.500秒脉冲，全片128秒。'
p['openingCueFrames']={'first':0,'second':30,'questionOut':68,'title':75,'tagline':105}
p['musicCredit']='配乐：《浮光》— Jannik'
save(public/'project.json',p);save(public/'shots.json',shots)
subprocess.run(['ffmpeg','-v','error','-y','-ss','77','-i',str(public/'assets/fuguang-jannik-full.mp3'),'-t','128','-af','volume=0.39,afade=t=in:st=0:d=1.25,afade=t=out:st=126:d=2','-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart',str(public/p['audio']['file'])],check=True)
t=np.array(analysis['times']);flux=np.array(analysis['flux']['bass'])
onsets=[]
for b in boundaries:
 source=b['source_seconds'];mask=(t>=source-.045)&(t<=source+.045)
 i=np.flatnonzero(mask)[np.argmax(flux[mask])]
 onsets.append({**b,'nearby_bass_flux_peak_seconds':round(float(t[i]),5),'grid_error_frames':0.0,'nearby_peak_delta_ms':round(float(t[i]-source)*1000,3),'bass_strength':round(float(flux[i]),5)})
save(work/'music-sync.json',{'track':analysis['song'],'artist':'Jannik','source_sha256':analysis['source_sha256'],'source_duration_seconds':258,'excerpt_source_seconds':[77,205],'film_duration_seconds':128,'main_climax_source_seconds':[102,198],'climax_video_start_seconds':25,'gain_db_compared_to_v3':-6.020599913,'measured_subdivision_seconds':.25,'measured_pulse_seconds':.5,'method':'Measured spectral periodicity, bass-band flux and section-level waveform; all boundary times use the measured half-second grid. Main drop source 102s minus source offset 77s equals video 25s.','full_human_listening_review':False,'boundaries':onsets,'opening_events':opening['music'],'ending_events':ending['music']})
state=load(root/'production.json');state.update(stage='motion',updated_at=datetime.now(timezone.utc).isoformat(),audio=p['audio'],next_action='Render V4 with 25s climax and -6dB gain; verify and deliver.',checks={'source_audio_downloaded':True,'source_duration_verified':True,'audio_spectral_grid_measured':True,'visual_review_completed':False,'human_full_listening_review':False})
save(root/'production.json',state)
(root/'music-plan.md').write_text('''# 浮光 V3 · 先铺垫再进入高潮

用户修订：开头进入高潮太快，需要自然铺垫。

- 来源：https://music.163.com/song?id=1394601255；完整公开音频258秒，原始MP3随工程保存。
- 本片采用原曲85.000–205.000秒的连续120秒。不变速、不循环、不在两段音乐之间拼接。
- 前17秒保留原曲轻段、逐步推进与高潮前停顿。1.25秒音量淡入去掉截取起音的突兀感，但情绪递进来自原曲编排。
- 片头0–5秒保留已确认钩子；5–11秒立春、11–17秒雨水，舒缓环境与前景运动，不做重拍回弹。
- 第17秒对应原曲102秒主要落点，切入“惊蛰：蛰伏的生命醒来”。此后再加入局部前景重音。
- 春季36秒，夏秋冬各24秒。章节开始为5/41/65/89秒；正文结束113秒，结尾113–120秒。
- 春季各镜6秒；其余3/4.5秒交替，全部重测卡点。背景保持独立运动。
- 音频0.78倍增益，1.25秒淡入与2秒尾部淡出。最终AAC直接封装并核对包哈希。

测量依据：10ms频谱通量与分频能量，稳定0.250秒细分、0.500秒脉冲及1.500秒重音组。音乐结构依据波形变化判断；未做完整人工听审，不把自动候选称为人工逐拍听审。

音乐版权归权利人；用户指定用于本次本地编辑，公开发布/商业授权未核验。
''',encoding='utf-8')
print(json.dumps({'duration_frames':3840,'duration_seconds':128,'climax_enters_video_seconds':25,'chapter_starts':[5,49,73,97],'gain_db_compared_to_v3':-6.020599913},indent=2))
subprocess.run(['python','-I',str(root/'scripts/write_v4_docs.py')],check=True)
