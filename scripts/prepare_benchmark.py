"""Fetch the optional full visual benchmark from the public release and verify its SHA-256."""
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda:source.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    root=Path(__file__).resolve().parents[1]
    index=json.loads((root/"assets/benchmarks/reference-index.json").read_text(encoding="utf8"))
    item=index["finished_full_visual"]
    target=root/"assets/benchmarks"/item["file"]
    if target.exists():
        if digest(target)!=item["sha256"]:
            raise SystemExit("The existing benchmark hash differs. Preserve it and inspect the file before retrying.")
        print(json.dumps({"status":"already_available","file":str(target),"sha256":item["sha256"]}))
        return
    partial=target.with_suffix(target.suffix+".part")
    if partial.exists():
        raise SystemExit("A partial file already exists; inspect it before retrying: "+str(partial))
    try:
        request=urllib.request.Request(item["download_url"],headers={"User-Agent":"theme-to-layered-video/2.0"})
        with urllib.request.urlopen(request,timeout=60) as response,partial.open("xb") as output:
            while True:
                chunk=response.read(1024*1024)
                if not chunk:
                    break
                output.write(chunk)
        actual=digest(partial)
        if actual!=item["sha256"]:
            raise ValueError("Downloaded benchmark SHA-256 did not match.")
        os.replace(partial,target)
        print(json.dumps({"status":"downloaded","file":str(target),"sha256":actual}))
    except Exception as exc:
        if partial.exists():
            partial.unlink()
        raise SystemExit("Benchmark download failed: "+str(exc))
if __name__=="__main__":
    main()
