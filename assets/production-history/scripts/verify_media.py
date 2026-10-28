import argparse,hashlib,json,os,subprocess
from fractions import Fraction
from pathlib import Path

def run(args):
 args[0]=os.environ.get('FFMPEG_BIN','ffmpeg') if args[0]=='ffmpeg' else os.environ.get('FFPROBE_BIN','ffprobe') if args[0]=='ffprobe' else args[0]
 return subprocess.run(args,check=True,capture_output=True,text=True,encoding='utf-8',errors='replace').stdout
def main():
 p=argparse.ArgumentParser();p.add_argument('project');p.add_argument('--video',required=True);a=p.parse_args();root=Path(a.project).resolve();video=Path(a.video).resolve();public=root/'public';work=root/'work/qc';work.mkdir(parents=True,exist_ok=True)
 project=json.loads((public/'project.json').read_text(encoding='utf-8'));shots=json.loads((public/'shots.json').read_text(encoding='utf-8'))
 probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');audios=[s for s in probe['streams'] if s['codec_type']=='audio']
 assert v['width']==project['width'] and v['height']==project['height'],'Unexpected dimensions'
 assert abs(float(Fraction(v['avg_frame_rate']))-project['fps'])<.001,'Unexpected fps'
 actual_frames=v.get('nb_frames')
 if not actual_frames or not str(actual_frames).isdigit():
  counted=json.loads(run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','json',str(video)]));actual_frames=counted['streams'][0]['nb_read_frames']
 actual_frames=int(actual_frames);assert actual_frames==project['durationFrames'],'Unexpected frame count'
 expected=project['durationFrames']/project['fps'];assert abs(float(v.get('duration',probe['format']['duration']))-expected)<1/project['fps']+.01,'Unexpected duration'
 if project.get('audio',{}).get('required',True):assert audios,'Missing audio stream'
 run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'])
 targets=sorted(set([int((s['start']+s['end'])//2) for s in shots]+[max(0,min(project['durationFrames']-1,s['start']+off)) for s in shots[1:] for off in [-1,0,3,8]]))
 index=[]
 for batch in range(0,len(targets),48):
  frames=targets[batch:batch+48];folder=work/f'batch-{batch//48:03d}';folder.mkdir(exist_ok=True)
  selector='+'.join('eq(n'+chr(92)+','+str(n)+')' for n in frames)
  run(['ffmpeg','-v','error','-y','-i',str(video),'-vf','select='+selector+',scale=640:-1','-q:v','2','-fps_mode','vfr','-start_number','1',str(folder/'frame-%03d.jpg')])
  files=sorted(folder.glob('frame-*.jpg'));assert len(files)==len(frames),'Frame extraction incomplete'
  index.extend({'frame':frame,'file':str(file.relative_to(root))} for frame,file in zip(frames,files))
 report={'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'frames':actual_frames,'duration_seconds':float(probe['format']['duration']),'audio_present':bool(audios),'full_decode_passed':True,'extracted_review_frames':len(index),'review_frame_index':index,'file_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'visual_review_completed':False,'human_full_listening_review':False,'notes':'Inspect extracted frames and listen as needed; this script verifies media structure and decoding, not aesthetic quality.'}
 audio=project.get('audio',{})
 if audio.get('file') and audio.get('copy') and not audio.get('offsetSeconds',0):
  source=public/audio['file'];final_hash=run(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).strip()
  source_hash=run(['ffmpeg','-v','error','-i',str(source),'-t',str(expected),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).strip();report['copied_audio_packet_hash_matches']=source_hash==final_hash
 else:report['copied_audio_packet_hash_matches']=None
 (work/'media-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='review_frame_index'},ensure_ascii=True,indent=2))
if __name__=='__main__':main()
