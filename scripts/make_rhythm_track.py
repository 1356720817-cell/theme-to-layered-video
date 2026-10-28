import argparse,array,json,math,random,wave
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description='Create a basic original instrumental rhythm bed; not a commercial music-library track.')
 p.add_argument('--output',required=True);p.add_argument('--seconds',type=float,default=130);p.add_argument('--bpm',type=float,default=120);p.add_argument('--seed',type=int,default=17);a=p.parse_args()
 if a.seconds<=0 or not 40<=a.bpm<=220:raise SystemExit('Invalid duration or bpm.')
 rate=22050;n=round(a.seconds*rate);beat=60/a.bpm;rng=random.Random(a.seed);samples=array.array('h')
 chords=[(110,130.8128,164.8138),(87.3071,110,130.8128),(130.8128,164.8138,195.9977),(97.9989,123.4708,146.8324)]
 for i in range(n):
  t=i/rate;phase=(t/beat)%1;bar=int(t/(beat*8))%4;previous=chords[(bar-1)%4];current=chords[bar];blend=min(1,(t%(beat*8))/.8)
  pad=0
  for f0,f1 in zip(previous,current):
   pad+=(1-blend)*math.sin(2*math.pi*f0*t)+blend*math.sin(2*math.pi*f1*t)
  age=phase*beat;kick=math.sin(2*math.pi*(45*age+1.5*(1-math.exp(-age*45))))*math.exp(-age*18)*.19*min(1,age/.002)
  hat=rng.uniform(-1,1)*math.exp(-((t/(beat/2))%1)*70)*.018
  bass=((1-blend)*math.sin(2*math.pi*previous[0]/2*t)+blend*math.sin(2*math.pi*current[0]/2*t))*.055*(.8+.2*math.sin(2*math.pi*t/(beat*4)))
  fade=min(1,t/1.2,max(0,(a.seconds-t)/1.6));value=(pad*.027+kick+hat+bass)*fade
  samples.append(round(max(-.9,min(.9,value))*32767))
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 with wave.open(str(out),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(samples.tobytes())
 info={'source':'Locally synthesized original basic instrumental bed','rights':'New procedural synthesis; no copied reference audio or sampled recordings','duration_seconds':n/rate,'bpm':a.bpm,'beat_seconds':beat,'beat_frames_note':'Convert seconds to the current project fps; audition cues before use.','beats_seconds':[round(j*beat,6) for j in range(math.ceil(a.seconds/beat))]}
 out.with_suffix('.json').write_text(json.dumps(info,indent=2),encoding='utf-8');print(json.dumps({'file':str(out),'seconds':n/rate,'bpm':a.bpm}))
if __name__=='__main__':main()
