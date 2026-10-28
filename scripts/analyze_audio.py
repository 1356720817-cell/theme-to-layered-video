import argparse,array,json,math,os,statistics,subprocess,wave
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description='Measure audio duration and simple transient candidates; results are not confirmed musical beats.')
 p.add_argument('audio');p.add_argument('--output',required=True);p.add_argument('--seconds',type=float,default=30);a=p.parse_args();out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 probe=subprocess.run([os.environ.get('FFPROBE_BIN','ffprobe'),'-v','error','-show_format','-of','json',a.audio],check=True,capture_output=True,text=True)
 duration=float(json.loads(probe.stdout)['format']['duration']);pcm=out.with_suffix('.analysis.wav')
 subprocess.run([os.environ.get('FFMPEG_BIN','ffmpeg'),'-v','error','-y','-i',a.audio,'-t',str(min(duration,a.seconds)),'-ac','1','-ar','22050',str(pcm)],check=True)
 with wave.open(str(pcm),'rb') as w:rate=w.getframerate();x=array.array('h',w.readframes(w.getnframes()))
 hop=220;window=440;energy=[]
 for i in range(0,len(x)-window,hop):energy.append(math.sqrt(sum(v*v for v in x[i:i+window])/window)/32768)
 flux=[0]+[max(0,energy[i]-energy[i-1]) for i in range(1,len(energy))];peaks=[]
 for i in range(3,len(flux)-3):
  local=flux[max(0,i-30):i+1];threshold=max(.002,statistics.median(local)*2.5)
  if flux[i]>=max(flux[i-3:i+4]) and flux[i]>threshold:
   t=i*hop/rate
   if not peaks or t-peaks[-1]['seconds']>.12:peaks.append({'seconds':round(t,4),'strength':round(flux[i],5)})
 report={'duration_seconds':duration,'analyzed_seconds':min(duration,a.seconds),'method':'20ms RMS positive difference, 10ms hop','candidates':peaks,'confirmed_beats':False,'review_required':'Check waveform, reference imagery or listening; do not treat every peak as a beat.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'report':str(out),'duration_seconds':duration,'candidate_count':len(peaks)}))
if __name__=='__main__':main()
