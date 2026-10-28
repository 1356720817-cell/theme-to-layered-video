"""Extract full-reference metadata, evenly spaced stills and candidate cuts; not a viewing/listening claim."""
import argparse
import json
import re
import subprocess
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video",required=True);p.add_argument("--output",required=True)
    p.add_argument("--interval",type=float,default=5)
    p.add_argument("--scene-threshold",type=float,default=.25)
    p.add_argument("--motion-at",type=float,action="append",default=[])
    a=p.parse_args();video=Path(a.video).resolve();out=Path(a.output).resolve()
    if not video.is_file() or a.interval<=0 or not 0<a.scene_threshold<1:
        p.error("Existing video, positive interval and threshold between zero and one required.")
    out.mkdir(parents=True,exist_ok=False)
    probe=json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(video)],check=True,capture_output=True,text=True).stdout)
    duration=float(probe["format"]["duration"])
    times={0.0}
    t=0.
    while t<duration:
        times.add(round(t,3));t+=a.interval
    for anchor in a.motion_at:
        for delta in (-.25,0,.1,.25,.5):
            times.add(round(max(0,min(duration-.05,anchor+delta)),3))
    rows=[]
    for i,t in enumerate(sorted(times)):
        target=out/f"sample-{i:03d}-{t:08.3f}s.jpg"
        subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",str(video),"-frames:v","1","-vf","scale=640:-2","-q:v","2",str(target)],check=True,capture_output=True)
        rows.append({"requested_time_seconds":t,"file":target.name})
    cuts=subprocess.run(["ffmpeg","-hide_banner","-i",str(video),"-an","-vf","select=gt(scene"+chr(92)+","+str(a.scene_threshold)+"),showinfo","-f","null","-"],check=True,capture_output=True,text=True,encoding="utf8",errors="replace")
    candidates=[float(x) for x in re.findall(r"pts_time:([0-9.]+)",cuts.stderr)]
    (out/"cut-candidates.log").write_text(cuts.stderr,encoding="utf8")
    report={"video":str(video),"duration_seconds":duration,"audio_present":any(s["codec_type"]=="audio" for s in probe["streams"]),"samples":rows,"scene_cut_candidates_seconds":candidates,"scene_threshold":a.scene_threshold,"full_continuous_viewing_completed":False,"full_listening_completed":False,"scope":"Sampling and scene-difference candidates only. Does not infer original layers, confirm cuts, transcribe words, identify beats or judge style."}
    (out/"reference-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
    try:
        from PIL import Image,ImageDraw
        cell_w,cell_h=328,210;columns=4
        sheet=Image.new("RGB",(columns*cell_w,((len(rows)+columns-1)//columns)*cell_h),"#101821")
        d=ImageDraw.Draw(sheet)
        for i,row in enumerate(rows):
            x=i%columns*cell_w;y=i//columns*cell_h
            with Image.open(out/row["file"]) as im:
                im.thumbnail((320,180));sheet.paste(im,(x+4,y+4))
            d.text((x+6,y+187),str(row["requested_time_seconds"])+"s",fill="white")
        sheet.save(out/"contact-sheet.jpg",quality=92)
    except ImportError:
        pass
    print(json.dumps({"output":str(out),"sample_count":len(rows),"candidate_cuts":len(candidates),"audio_present":report["audio_present"]},ensure_ascii=True))
if __name__=="__main__":main()
