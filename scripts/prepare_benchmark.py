"""Assemble the complete visual benchmark from verified repository segments."""
import hashlib
import json
import os
import urllib.request
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    index = json.loads((root / "assets/benchmarks/reference-index.json").read_text(encoding="utf-8"))
    item = index["finished_full_visual"]
    target = root / "assets/benchmarks" / item["file"]
    if target.exists():
        if digest(target) != item["sha256"]:
            raise SystemExit("The existing benchmark hash differs. Preserve it and inspect the file before retrying.")
        print(json.dumps({"status": "already_available", "file": str(target), "sha256": item["sha256"]}))
        return

    partial = target.with_suffix(target.suffix + ".part")
    if partial.exists():
        raise SystemExit("A partial file already exists; inspect it before retrying: " + str(partial))
    try:
        with partial.open("xb") as output:
            for segment in item["parts"]:
                request = urllib.request.Request(
                    segment["download_url"], headers={"User-Agent": "theme-to-layered-video/2.0"}
                )
                part_hash = hashlib.sha256()
                part_size = 0
                with urllib.request.urlopen(request, timeout=60) as response:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        output.write(chunk)
                        part_hash.update(chunk)
                        part_size += len(chunk)
                if part_size != segment["size"] or part_hash.hexdigest() != segment["sha256"]:
                    raise ValueError("A downloaded benchmark segment failed its size or SHA-256 check.")

        actual = digest(partial)
        if actual != item["sha256"]:
            raise ValueError("The assembled benchmark SHA-256 did not match.")
        os.replace(partial, target)
        print(json.dumps({"status": "assembled", "file": str(target), "sha256": actual}))
    except Exception as exc:
        if partial.exists():
            partial.unlink()
        raise SystemExit("Benchmark assembly failed: " + str(exc))


if __name__ == "__main__":
    main()
