import json,subprocess
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
def decode(path):
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','12000','-f','f32le','-'],check=True,capture_output=True).stdout
 return np.frombuffer(raw,dtype='<f4')
source=decode(root/'public/assets/fuguang-jannik-full.mp3')
final=decode(root/'outputs/final.mp4')
sr=12000;step=10
# Ignore the fade-in, intentional arrangement break, and fade-out for the alignment measurement.
start=28*sr;end=120*sr
y=final[start:end:step].astype(np.float64);y-=y.mean();yn=np.linalg.norm(y)
results=[]
for delta in range(-60,61,10):
 x=source[77*sr+start+delta:77*sr+end+delta:step].astype(np.float64);x-=x.mean()
 corr=float(np.dot(x,y)/(np.linalg.norm(x)*yn));gain=float(np.dot(x,y)/np.dot(x,x))
 results.append({'source_shift_samples':delta,'source_shift_ms':delta/sr*1000,'correlation':corr,'gain':gain})
best=max(results,key=lambda r:r['correlation'])
assert best['correlation']>.96,best
assert abs(best['source_shift_ms'])<=2,best
report={'source_song':'浮光 (The History) — Jannik','expected_source_offset_seconds':77,'sample_rate':sr,'comparison_video_seconds':[28,120],'method':'PCM cross-correlation against decoded original, sample decimation 10; compressed AAC differences are expected. This verifies source excerpt offset, not human listening or aesthetic beat selection.','best_alignment':best,'source_offset_verified':True,'human_full_listening_review':False}
(root/'work/audio-offset-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
