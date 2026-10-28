"""Package a current validated project without caches, dependencies or environment secrets."""
import argparse
import json
import sys
import zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from production_gate import check,digest,read,local

def package(root,video,output):
    root=Path(root).resolve();video=(root/video).resolve();output=Path(output).resolve()
    result=check(root,"deliver",str(video))
    if not result["passed"]:
        raise ValueError("Delivery gate failed: "+json.dumps(result["errors"],ensure_ascii=True))
    if output.exists():
        raise ValueError("Preserve existing package versions; select a new filename.")
    root_files={"package.json","package-lock.json","tsconfig.json","production.json","music-plan.json","visual-plan.json",
                "sources.json","camera-plan.json","continuity-obligations.json","reference-map.json"}
    evidence_files={"review-ledger.json","shot-approvals.json","project-audit.json","render-report.json","lint-report.json","audio-mux.json","music-sync.json","music-levels.json"}
    excluded={"node_modules",".git","__pycache__","render-bundle","preview-bundle"}
    files=[]
    def collect(folder):
        if not folder.exists():
            return
        for f in folder.rglob("*"):
            if not f.is_file():
                continue
            rel=f.relative_to(root)
            if any(n in excluded or n.startswith(".env") for n in rel.parts) or f.suffix in (".pyc",".pem",".key"):
                continue
            if not f.resolve().is_relative_to(root):
                raise ValueError("External file link cannot be packaged: "+str(rel))
            files.append(f)
    for folder in ("public","src","scripts"):
        collect(root/folder)
    for f in root.iterdir():
        if f.is_file() and (f.name in root_files or f.suffix in (".md",".mjs",".cmd")) and not f.name.startswith(".env"):
            files.append(f)
    for name in evidence_files:
        if (root/"work"/name).is_file():
            files.append(root/"work"/name)
    for name in ("qc","generated-records","generated-batches"):
        collect(root/"work"/name)
    # An editable archive must include approved auditions, even when stored under outputs.
    # The final film itself remains a separate deliverable; rerendering requires fresh final QC.
    ledger=read(root/"work/review-ledger.json")
    for row in ledger.get("records",[]):
        if row.get("gate") == "visual":
            continue
        for name in row.get("files",{}):
            f=local(root,name)
            if any(part.startswith(".env") for part in f.relative_to(root).parts) or f.suffix in (".pem",".key"):
                raise ValueError("A required evidence file is secret-like and cannot be packaged: "+name)
            files.append(f)
    shots=root/"work/shot-approvals.json"
    if shots.is_file():
        for row in read(shots).get("records",[]):
            files.extend(local(root,name) for name in row.get("files",{}))
    files=sorted(set(files))
    state=root/"production.json"
    if state.is_file():
        d=read(state);d["stage"]="delivered_pending_acceptance";d["delivery_status"]="delivered_pending_acceptance"
        state.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf8")
    manifest={"video_file":str(video.relative_to(root)),"video_sha256":digest(video),
              "delivery_state":"delivered_pending_acceptance","user_final_acceptance_inferred":False,
              "files":[{"file":f.relative_to(root).as_posix(),"sha256":digest(f)} for f in files],
              "scope":"Current project/source/evidence ZIP. Final MP4 delivered separately. No independent clean dependency installation or human full listening implied."}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in files:
            z.write(f,root.name+"/"+f.relative_to(root).as_posix())
        z.writestr(root.name+"/delivery-manifest.json",json.dumps(manifest,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC failed")
        count=len(z.namelist())
    return {"archive":str(output),"entries":count,"sha256":digest(output),"bytes":output.stat().st_size,"integrity_passed":True,"final_acceptance":"pending"}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("project");p.add_argument("--video",required=True);p.add_argument("--output",required=True)
    a=p.parse_args()
    try:
        print(json.dumps(package(a.project,a.video,a.output),ensure_ascii=True,indent=2))
    except (OSError,ValueError,KeyError,zipfile.BadZipFile) as e:
        p.exit(1,str(e)+"\n")
if __name__=="__main__":main()
