import json,math,wave,subprocess
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1];out=root/'public/assets'
sr=44100;duration=130.;beat=.625;bar=2.5
audio=np.zeros((round(sr*duration),2),dtype=np.float32)
rng=np.random.default_rng(24026);events=[]
def add(time,sig,amp=1,pan=0):
 start=round(time*sr);sig=np.asarray(sig,dtype=np.float32)*amp
 if start<0:sig=sig[-start:];start=0
 end=min(len(audio),start+len(sig))
 if end<=start:return
 sig=sig[:end-start]
 audio[start:end,0]+=sig*math.sqrt((1-pan)/2)
 audio[start:end,1]+=sig*math.sqrt((1+pan)/2)
def freq(m):return 440*2**((m-69)/12)
def pluck(m,d=1.5):
 t=np.arange(round(d*sr),dtype=np.float32)/sr;f=freq(m);y=np.zeros_like(t)
 for k in range(1,10):
  if f*k>17000:break
  y+=np.sin(2*np.pi*f*k*t+.015*k*np.sin(t*3.1))*np.exp(-t*(1.8+k*.7))/(k**1.48)
 return y*(1-np.exp(-t*700))
def flute(m,d):
 t=np.arange(round(d*sr),dtype=np.float32)/sr;f=freq(m)
 env=np.minimum(1,t/.18)*np.minimum(1,np.maximum(0,(d-t)/.45))
 y=np.sin(2*np.pi*f*t+.035*np.sin(t*2*np.pi*5.1))+.12*np.sin(4*np.pi*f*t)
 return y*env*(.92+.08*np.sin(t*2*np.pi*4.7))
def pad(notes,d):
 t=np.arange(round(d*sr),dtype=np.float32)/sr;env=np.minimum(1,t/.65)*np.minimum(1,np.maximum(0,(d-t)/.85));y=np.zeros_like(t)
 for m in notes:
  f=freq(m);y+=(np.sin(2*np.pi*f*.999*t)+np.sin(2*np.pi*f*1.001*t))*.34+np.sin(2*np.pi*f*2*t)*.08
 return y*env/len(notes)
def drum(kind):
 d=.4 if kind=='low' else .12;t=np.arange(round(d*sr),dtype=np.float32)/sr
 if kind=='low':return np.sin(2*np.pi*(43*t+.95*(1-np.exp(-t*28))))*np.exp(-t*14)*(1-np.exp(-t*600))
 if kind=='wood':return (np.sin(t*2*np.pi*970)+.34*np.sin(t*2*np.pi*1873))*np.exp(-t*65)*(1-np.exp(-t*1200))
 return np.diff(rng.uniform(-1,1,len(t)+1)).astype(np.float32)*np.exp(-t*60)*(1-np.exp(-t*1600))
chords=[[50,57,62,66],[43,55,59,62],[47,54,59,66],[45,57,61,64]]
motifs=[[74,76,78,81,78,76,74,69],[78,81,83,86,83,81,78,76],[74,69,71,74,78,76,74,71],[69,71,74,76,74,71,69,66]]
for b in range(52):
 season=min(3,max(0,(b-2)//12));local=max(0,b-2)
 ch=chords[(local//2)%4] if b<50 else chords[0]
 add(b*bar,pad(ch,bar+1.2),.095,(-.12 if b%2 else .12))
 if b>=2 and b<50:
  energy=[.060,.105,.062,.035][season]
  for k in ([0,2] if season!=1 else [0,1,2,3]):add(b*bar+k*beat,drum('low'),energy)
  for k in [1,3]:add(b*bar+k*beat,drum('wood'),[.019,.035,.021,.011][season],.3)
  if season in [0,1,2]:
   for k in np.arange(.5,4,.5):add(b*bar+float(k)*beat,drum('shaker'),[.009,.016,.008,.0][season],-.35)
  for k in [0,2.5]:add(b*bar+k*beat,pluck(ch[0]-12,.9),.075,0)
for phrase in range(24):
 start=5+phrase*5;season=phrase//6;motif=motifs[season]
 offsets=[0,.5,1.5,2.5,4,4.75,5.5,6.75]
 if season==3:offsets=[0,1.5,4,6.5]
 elif season==2:offsets=[0,1,2.5,4,5.5,7]
 for k,off in enumerate(offsets):
  m=motif[(k+phrase%3)%len(motif)]-(12 if season==3 else 0)
  add(start+off*beat,pluck(m,1.6),[.145,.16,.13,.115][season],-.25+.5*(k%2))
  events.append({'time':round(start+off*beat,6),'instrument':'plucked-string','midi':m})
 if phrase%2==0:
  for k,m in enumerate([motif[0]-12,motif[3]-12,motif[4]-12]):add(start+.75+k*1.25,flute(m,1.7),.034,.30)
# Opening: exact visual cues, a low pulse and bright plucked accents.
for t,m,g in [(0,50,.15),(1.25,69,.20),(2.5,74,.23),(4.375,81,.15),(125,74,.18),(127.5,62,.17)]:
 add(t,pluck(m,2.2),g,-.05);events.append({'time':t,'instrument':'opening/closing accent','midi':m})
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
for s in shots[1:-1]:
 t=s['start']/30
 add(t,pluck([74,76,78,81,83][(s.get('index',1)-1)%5],1.25),.060,.10)
# Light room reflections, no external samples.
dry=audio.copy()
for delay,gain in [(.083,.06),(.147,.08),(.227,.07),(.383,.055),(.577,.033),(.811,.02)]:
 n=round(delay*sr);audio[n:]+=dry[:-n,::-1]*gain
fade=np.minimum(1,np.arange(len(audio))/(sr*.20))*np.minimum(1,(len(audio)-np.arange(len(audio)))/(sr*2.3))
audio*=fade[:,None]
peak=float(np.max(np.abs(audio)));audio*=.84/max(peak,.84)
rms=float(np.sqrt(np.mean(audio**2)));encoded=np.round(np.clip(audio,-1,1)*32767).astype('<i2')
wav=out/'solar-terms-original.wav'
with wave.open(str(wav),'wb')as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(encoded.tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-af','loudnorm=I=-18:TP=-1.5:LRA=10','-ar','48000','-c:a','aac','-b:a','192k','-t','130',str(out/'solar-terms-original.m4a')],check=True)
# Measure actual PCM onset envelopes around designed opening cues.
mono=np.mean(audio,axis=1);cues=[]
for t in [0,1.25,2.5,4.375,5]:
 lo=round(t*sr);hi=min(len(mono),lo+round(.12*sr));block=mono[lo:hi]
 cues.append({'intended_seconds':t,'frame':round(t*30),'local_peak_seconds':round(t+int(np.argmax(np.abs(block)))/sr,5),'peak':round(float(np.max(np.abs(block))),5)})
info={'source':'Original procedural composition for this project','rights':'Self-synthesized waveforms only; no sampled recordings or reference audio','bpm':96,'meter':'4/4','duration_seconds':130,'sample_rate':sr,'channels':2,'raw_peak_before_normalization':peak,'wav_peak':float(np.max(np.abs(audio))),'wav_rms':rms,'opening_measured_cues':cues,'notes':events,'human_full_listening_review':False}
(root/'music-composition.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in info.items() if k!='notes'},ensure_ascii=True))

