"""Measure actual input loudness/true peak and an optional same-music interval; does not normalize saved audio."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from production_gate import digest

def measure(file, start=0., seconds=None):
    file=Path(file).resolve()
    if not file.is_file() or start<0 or (seconds is not None and seconds<=0):
        raise ValueError("Existing file and a valid measurement interval required.")
    args=["ffmpeg","-hide_banner","-ss",str(start),"-i",str(file)]
    if seconds is not None:
        args+=["-t",str(seconds)]
    args+=["-map","0:a:0","-vn","-af","astats=metadata=0:reset=0,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"]
    r=subprocess.run(args,check=True,capture_output=True,text=True,encoding="utf8",errors="replace")
    match=re.search(r'\{\s*"input_i".*?\}',r.stderr,re.S)
    if not match:
        raise ValueError("FFmpeg did not emit loudness input measurements.")
    values=json.loads(match.group())
    rms=re.findall(r"RMS level dB: ([-0-9.inf]+)",r.stderr)
    return {"file":str(file),"sha256":digest(file),"interval_start_seconds":start,"interval_length_seconds":seconds,
            "integrated_loudness_LUFS":values["input_i"],"input_true_peak_dBTP":values["input_tp"],
            "loudness_range_LU":values["input_lra"],"rms_level_dBFS":rms[-1] if rms else None,
            "true_peak_above_zero":float(values["input_tp"])>0,
            "scope":"Actual input measurement only. No normalized audio saved. The analysis filter targets are not universal delivery requirements. Same-song gain comparisons must use corresponding intervals; final loudness still needs actual audition."}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--file",required=True);p.add_argument("--start",type=float,default=0);p.add_argument("--seconds",type=float);p.add_argument("--output",required=True)
    a=p.parse_args()
    try:
        report=measure(a.file,a.start,a.seconds);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
        print(json.dumps(report,ensure_ascii=True,indent=2))
    except (OSError,ValueError,subprocess.CalledProcessError) as e:
        p.exit(1,str(e)+"\n")
if __name__=="__main__":main()
