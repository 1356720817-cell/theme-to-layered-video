"""Behavioral regression fixtures. All approvals are explicitly synthetic and never real consent."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from production_gate import read, init, record, check, record_shot
from audit_project import audit
from prepare_music import prepare
from verify_audio import verify

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def ff(args):
    subprocess.run(["ffmpeg","-v","error","-y"]+args, check=True, capture_output=True)

def run_tests(base):
    from PIL import Image
    project = base/"fixture"
    subprocess.run([sys.executable,"-I",str(Path(__file__).parent/"init_project.py"),"--topic","SYNTHETIC TEST ONLY","--seconds","4","--width","320","--height","180","--output",str(project)],check=True,capture_output=True)
    public=project/"public"; out=project/"outputs";out.mkdir()
    (project/"script.md").write_text("Fixture script; not a production approval.",encoding="utf8")
    (project/"look.md").write_text("Fixture appearance only.",encoding="utf8")
    for i,color in enumerate(((15,70,85),(80,45,10))):
        Image.new("RGB",(320,180),color).save(public/"assets"/f"image-{i}.png")
    ff(["-f","lavfi","-i","aevalsrc=0.18*sin(2*PI*(230*t+35*t*t))+0.08*sin(2*PI*117*t):d=7:s=48000","-c:a","pcm_s16le",str(public/"assets/full.wav")])
    recipe=prepare(project,"public/assets/full.wav","public/assets/master.m4a",1,4,-5,.1,.2,2.5)
    p=read(public/"project.json");p.update(status="ready")
    p["audio"]={"file":"assets/master.m4a","required":True,"source":"synthetic fixture","rights":"generated test tones","copy":True,"offsetSeconds":0}
    write(public/"project.json",p)
    assets={"assets":[{"id":f"a{i}","file":f"assets/image-{i}.png","ownerShot":f"s{i}","status":"ready","kind":"image","depiction":"generated","prompt":"Synthetic unit-test color field only","rights":"synthetic","alpha":False} for i in range(2)]}
    shots=[{"id":f"s{i}","start":i*60,"end":(i+1)*60,"section":"main","chapter":"","title":"TEST","subtitle":"","kicker":"","theme":"dark","camera":{"type":"still"},"transition":{"type":"cut","frames":0},"layers":[{"assetId":f"a{i}","role":"background","x":0,"y":0,"w":1,"h":1}]} for i in range(2)]
    write(public/"assets.json",assets);write(public/"shots.json",shots)
    ff(["-f","lavfi","-i","color=c=teal:s=320x180:r=30:d=4","-i",str(public/"assets/master.m4a"),"-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","ultrafast","-c:a","copy","-t","4",str(out/"audition.mp4")])
    plan={"song":"TEST FIXTURE","artist":"Synthetic","source_url":"local generated tones","excerpt_start_seconds":1,"excerpt_end_seconds":5,"gain_db":-5,"fade_in_seconds":.1,"fade_out_seconds":.2,"climax_source_seconds":2.5,"climax_video_seconds":1.5,"rights_status":"synthetic_test_only","preview_file":"outputs/audition.mp4"}
    write(project/"music-plan.json",plan)
    results=[]
    def expect(name, value):
        results.append({"test":name,"passed":bool(value)})
        if not value:
            raise AssertionError(name)
    expect("initialization selects cinematic production engine",(project/"src/Film.tsx").read_bytes()==(Path(__file__).resolve().parents[1]/"assets/starter/src/Film.tsx").read_bytes())
    expect("missing reviews block motion",not check(project,"motion")["passed"])
    record(project,"content","agent","TEST ONLY content review","",["script.md"])
    record(project,"look","user","SIMULATED TEST LOOK CONFIRMATION","TEST_FIXTURE_ONLY",["look.md","public/assets/image-0.png","outputs/audition.mp4"])
    record(project,"music","agent","TEST ONLY not actual user consent","",["music-plan.json"])
    expect("agent cannot substitute for required user music confirmation",not check(project,"motion")["passed"])
    def music():
        record(project,"music","user","SIMULATED TEST CONFIRMATION, NOT REAL CONSENT","TEST_FIXTURE_ONLY",["music-plan.json","outputs/audition.mp4"])
    music()
    expect("valid version-bound fixture passes motion gate",check(project,"motion")["passed"])
    p["audio"]["gain"]=.39;write(public/"project.json",p)
    expect("changed audio gain invalidates music confirmation",not check(project,"motion")["passed"])
    del p["audio"]["gain"];write(public/"project.json",p)
    raw=(public/"assets/master.m4a").read_bytes();(public/"assets/master.m4a").write_bytes(raw+b"changed")
    expect("changed music bytes invalidate confirmation",not check(project,"motion")["passed"])
    (public/"assets/master.m4a").write_bytes(raw)
    raw_preview=(out/"audition.mp4").read_bytes();(out/"audition.mp4").write_bytes(raw_preview+b"changed")
    expect("changed audition invalidates music confirmation",not check(project,"motion")["passed"])
    (out/"audition.mp4").write_bytes(raw_preview)
    plan["climax_source_seconds"]=3;write(project/"music-plan.json",plan);music()
    expect("inconsistent climax mapping rejected",any("mapping" in e for e in check(project,"motion")["errors"]))
    plan["climax_source_seconds"]=2.5;write(project/"music-plan.json",plan);music()
    ff(["-i",str(out/"audition.mp4"),"-t","1","-c","copy",str(out/"short.mp4")])
    plan["preview_file"]="outputs/short.mp4";write(project/"music-plan.json",plan);music()
    expect("audition ending before climax rejected",any("audition" in e for e in check(project,"motion")["errors"]))
    plan["preview_file"]="outputs/audition.mp4";write(project/"music-plan.json",plan);music()
    ledger=read(project/"work/review-ledger.json");ledger["policy"]["shot_approval"]="each";write(project/"work/review-ledger.json",ledger)
    expect("each-shot policy blocks missing confirmations",not check(project,"motion")["passed"])
    for i in range(2):
        record_shot(project,f"s{i}","SIMULATED TEST SHOT APPROVAL","TEST_FIXTURE_ONLY",["outputs/audition.mp4"])
    expect("each-shot policy accepts complete version-bound fixture",check(project,"motion")["passed"])
    original=(public/"assets/image-1.png").read_bytes()
    Image.new("RGB",(320,180),(45,15,72)).save(public/"assets/image-1.png")
    expect("asset replacement invalidates affected shot approval",not check(project,"motion")["passed"])
    (public/"assets/image-1.png").write_bytes(original)
    expect("unique contiguous ready fixture passes project audit",audit(project)["passed"])
    shots[0]["poem"]={"lines":["Fixture"],"author":"Test","work":"Synthetic","sourceUrl":"local-test","cueFrame":90,"lineStaggerFrames":6,"attributionCueFrame":24};write(public/"shots.json",shots)
    expect("out-of-shot poetry cue is rejected",not audit(project)["passed"])
    del shots[0]["poem"];shots[0]["accentFrames"]=[90];write(public/"shots.json",shots)
    expect("out-of-shot accent cue is rejected",not audit(project)["passed"])
    del shots[0]["accentFrames"];write(public/"shots.json",shots)
    assets["assets"][0]["alpha"]=True;write(public/"assets.json",assets)
    expect("opaque file falsely declared alpha is rejected",not audit(project)["passed"])
    assets["assets"][0]["alpha"]=False;write(public/"assets.json",assets)
    source_file=project/"src/Film.tsx";source_text=source_file.read_text(encoding="utf8");source_file.write_text(source_text+"\n// changed rendering code\n",encoding="utf8")
    expect("renderer change invalidates appearance confirmation",not check(project,"motion")["passed"])
    source_file.write_text(source_text,encoding="utf8")
    saved_ledger=read(project/"work/review-ledger.json");changed=json.loads(json.dumps(saved_ledger));changed["policy"]["required_user_gates"]=[]
    write(project/"work/review-ledger.json",changed)
    expect("music confirmation cannot be silently delegated",not check(project,"motion")["passed"])
    write(project/"work/review-ledger.json",saved_ledger)
    shutil.copy2(public/"assets/image-0.png",public/"assets/image-1.png")
    expect("renamed duplicate image is rejected",not audit(project)["passed"])
    (public/"assets/image-1.png").write_bytes(original)
    shots[1]["start"]+=1;write(public/"shots.json",shots)
    expect("timeline gap rejected",not audit(project)["passed"])
    shots[1]["start"]-=1;write(public/"shots.json",shots)
    # Source duration is checked independently of declared project metadata.
    ff(["-f","lavfi","-i","sine=f=440:r=48000:d=1","-c:a","aac",str(public/"assets/short.m4a")])
    p["audio"]["file"]="assets/short.m4a";write(public/"project.json",p)
    expect("short audio rejected without authorized padding",not audit(project)["passed"])
    p["audio"]["file"]="assets/master.m4a";write(public/"project.json",p)
    rejected=False
    try:
        prepare(project,"public/assets/full.wav","public/assets/invalid.m4a",6,4,0,.1,.1)
    except ValueError:
        rejected=True
    expect("excerpt beyond real source rejected",rejected)
    expect("continuous source-to-film climax map computed",recipe["climax_video_seconds"]==1.5)
    expect("copied approved track matches actual final packets",verify(project,out/"audition.mp4")["passed"])
    ff(["-i",str(out/"audition.mp4"),"-c:v","copy","-c:a","aac","-b:a","192k",str(out/"transcoded.mp4")])
    p["audio"]["copy"]=False;write(public/"project.json",p)
    expect("transcoded approved track passes decoded comparison",verify(project,out/"transcoded.mp4")["passed"])
    ff(["-i",str(out/"audition.mp4"),"-c:v","copy","-af","volume=0.5","-c:a","aac",str(out/"wrong-gain.mp4")])
    expect("wrong gain rejected despite matching melody",not verify(project,out/"wrong-gain.mp4")["passed"])
    ff(["-i",str(out/"audition.mp4"),"-f","lavfi","-i","sine=f=799:r=48000:d=4","-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac",str(out/"wrong-song.mp4")])
    expect("wrong song rejected",not verify(project,out/"wrong-song.mp4")["passed"])
    expect("missing final render and QC blocks delivery",not check(project,"deliver","outputs/audition.mp4")["passed"])
    return {"passed":all(r["passed"] for r in results),"test_count":len(results),"tests":results,"scope":"Synthetic behavioral fixtures only. No real user confirmations, new image quality, full production rerender, external accounts, or human listening are validated."}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--report",required=True);p.add_argument("--keep-fixtures")
    a=p.parse_args()
    if a.keep_fixtures:
        base=Path(a.keep_fixtures).resolve();base.mkdir(parents=True,exist_ok=False)
        report=run_tests(base)
    else:
        with tempfile.TemporaryDirectory(prefix="layered-skill-test-") as temp:
            report=run_tests(Path(temp))
    path=Path(a.report);path.parent.mkdir(parents=True,exist_ok=True);write(path,report)
    print(json.dumps(report,ensure_ascii=True,indent=2))
if __name__=="__main__":
    main()
