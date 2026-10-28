import argparse,json,math,subprocess
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--previous',required=True);args=p.parse_args()
def decode(path):
 r=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','12000','-f','f32le','-'],check=True,capture_output=True)
 return np.frombuffer(r.stdout,dtype='<f4')
old=decode(Path(args.previous));new=decode(root/'outputs/final.mp4');sr=12000
# Both windows represent original source seconds 102�C198, so the music content is identical.
a=old[17*sr:113*sr];b=new[25*sr:121*sr]
assert len(a)==len(b)==96*sr
rms=lambda x:float(np.sqrt(np.mean(x.astype(np.float64)**2)))
ratio=rms(b)/rms(a);db=20*math.log10(ratio)
assert -6.3<db<-5.7,db
report={'previous_source':Path(args.previous).name,'comparison_original_seconds':[102,198],'previous_video_seconds':[17,113],'current_video_seconds':[25,121],'previous_rms':rms(a),'current_rms':rms(b),'rms_ratio':ratio,'measured_gain_db_compared_to_v3':db,'expected_gain_db_compared_to_v3':-6.020599913,'reduction_verified':True,'current_pcm_peak':float(np.abs(new).max()),'human_full_listening_review':False}
(root/'work/audio-level-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
