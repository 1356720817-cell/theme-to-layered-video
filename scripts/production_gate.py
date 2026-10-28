"""Version-bound review records. Records are evidence indexes, not authenticated consent."""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

GATES = ("content", "look", "music", "preview", "visual")
STAGES = {"assets": ("content", "look"), "motion": ("content", "look", "music"),
          "render": ("content", "look", "music", "preview"),
          "deliver": ("content", "look", "music", "preview", "visual")}

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def stable(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()

def local(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("Evidence must be an existing project-local file: " + str(value))
    return path

def file_map(root, values):
    return {str(local(root, v).relative_to(root)).replace(chr(92), "/"): digest(local(root, v)) for v in values}

def production_fingerprint(root):
    root = Path(root).resolve()
    files = []
    for folder in ("public", "src"):
        base = root / folder
        if not base.is_dir():
            raise ValueError("Missing production directory: " + folder)
        files.extend(str(p.relative_to(root)) for p in base.rglob("*") if p.is_file())
    files.extend(str(p.relative_to(root)) for p in root.glob("*.mjs"))
    files.extend(n for n in ("package.json", "package-lock.json", "tsconfig.json") if (root/n).is_file())
    return stable(file_map(root, sorted(set(files))))

def scope(root, gate):
    project = read(root / "public/project.json")
    if gate == "music":
        audio = project.get("audio", {})
        values = [str(Path("public") / audio["file"])] if audio.get("file") else []
        if audio.get("fullSourceFile"):
            values.append(str(Path("public") / audio["fullSourceFile"]))
        if (root/"music-plan.json").is_file():
            values.append("music-plan.json")
            plan = read(root/"music-plan.json")
            if plan.get("preview_file"):
                values.append(plan["preview_file"])
        return stable({"audio": audio, "fps": project["fps"], "durationFrames": project["durationFrames"],
                       "files": file_map(root, values)})
    if gate in ("preview", "visual"):
        return production_fingerprint(root)
    if gate == "look":
        values = [str(p.relative_to(root)) for p in (root/"src").rglob("*") if p.is_file()]
        values += ["visual-plan.json"] if (root/"visual-plan.json").is_file() else []
        return stable({"files": file_map(root,values), "layout":{k:project.get(k) for k in ("width","height","fonts","palette")}})
    names = ("brief.md", "script.md", "outline.md", "sources.md", "sources.json") if gate == "content" else ()
    return stable(file_map(root, [n for n in names if (root/n).is_file()]))

def init(root, user_gates=("music", "look")):
    path = root/"work/review-ledger.json"
    if path.exists():
        raise ValueError("Review ledger already exists; preserve prior records.")
    if not set(user_gates).issubset(GATES):
        raise ValueError("Unknown user gate")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"schema_version": 2, "policy": {"required_user_gates": list(user_gates),
             "music_delegation": None, "shot_approval": "anchors"},
            "records": [], "delivery_status": "in_production"}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data

def record(root, gate, actor, statement, source_ref, files):
    path = root/"work/review-ledger.json"
    data = read(path)
    if not statement.strip() or not files:
        raise ValueError("Record a substantive real review and at least one concrete evidence file.")
    if actor == "user" and not source_ref.strip():
        raise ValueError("User confirmation needs its actual message/turn reference.")
    entry = {"gate": gate, "actor": actor, "statement": statement, "source_ref": source_ref,
             "recorded_at": datetime.now(timezone.utc).isoformat(), "scope_sha256": scope(root, gate),
             "files": file_map(root, files)}
    data["records"].append(entry)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry

def shot_scope(root, shot_id):
    shots = read(root/"public/shots.json")
    shot = next((s for s in shots if s["id"] == shot_id), None)
    if shot is None:
        raise ValueError("Unknown shot: " + shot_id)
    records = {a["id"]: a for a in read(root/"public/assets.json")["assets"]}
    files = [str(Path("public")/records[l["assetId"]]["file"]) for l in shot["layers"]]
    files += [str(p.relative_to(root)) for p in (root/"src").rglob("*") if p.is_file()]
    return stable({"shot": shot, "files": file_map(root, files)})

def record_shot(root, shot_id, statement, source_ref, files):
    if not statement.strip() or not source_ref.strip() or not files:
        raise ValueError("Per-shot confirmation needs real user statement, message reference and preview.")
    path = root/"work/shot-approvals.json"
    data = read(path) if path.exists() else {"records":[]}
    entry = {"shot_id":shot_id,"actor":"user","statement":statement,"source_ref":source_ref,
             "scope_sha256":shot_scope(root, shot_id),"files":file_map(root, files)}
    data["records"].append(entry)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    return entry

def check(root, stage, video=None):
    errors = []
    try:
        data = read(root/"work/review-ledger.json")
        policy = data["policy"]
        required_user = policy.get("required_user_gates", ["music", "look"])
        if not set(required_user).issubset(GATES):
            errors.append("Unknown user confirmation gate.")
        if "music" not in required_user:
            delegation = policy.get("music_delegation") or {}
            if not delegation.get("statement") or not delegation.get("source_ref"):
                errors.append("Delegated music approval requires explicit user delegation evidence.")
        for gate in STAGES[stage]:
            entries = [r for r in data["records"] if r.get("gate") == gate]
            if not entries:
                errors.append("Missing review: " + gate)
                continue
            entry = entries[-1]
            if gate in required_user and (entry.get("actor") != "user" or not entry.get("source_ref")):
                errors.append("Actual user confirmation required: " + gate)
            if entry.get("actor") not in ("user", "agent") or not entry.get("statement"):
                errors.append("Invalid review actor/statement: " + gate)
            if entry.get("scope_sha256") != scope(root, gate):
                errors.append("Stale review after input changes: " + gate)
            if not entry.get("files") or entry["files"] != file_map(root, entry["files"].keys()):
                errors.append("Evidence changed or missing: " + gate)
        if "music" in STAGES[stage]:
            plan = read(root/"music-plan.json")
            required = ("song", "artist", "source_url", "excerpt_start_seconds", "excerpt_end_seconds",
                        "gain_db", "fade_in_seconds", "fade_out_seconds", "climax_video_seconds",
                        "rights_status", "preview_file")
            missing = [k for k in required if k not in plan]
            if missing:
                errors.append("Music plan missing: " + ", ".join(missing))
            else:
                project = read(root/"public/project.json")
                seconds = project["durationFrames"]/project["fps"]
                nums = [plan[k] for k in ("excerpt_start_seconds", "excerpt_end_seconds", "gain_db", "fade_in_seconds", "fade_out_seconds")]
                if not all(isinstance(n, (int, float)) and math.isfinite(n) for n in nums):
                    errors.append("Invalid numeric music plan values.")
                elif not plan.get("segments") and abs(plan["excerpt_end_seconds"]-plan["excerpt_start_seconds"]-seconds) > 1/project["fps"]:
                    errors.append("Music excerpt length differs from current film duration.")
                preview = local(root, plan["preview_file"])
                probe = subprocess.run([os.environ.get("FFPROBE_BIN", "ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(preview)], check=True, capture_output=True, text=True)
                media = json.loads(probe.stdout)
                if not any(s["codec_type"] == "audio" for s in media["streams"]):
                    errors.append("Music audition has no actual audio.")
                drop = plan.get("climax_video_seconds")
                if drop is not None:
                    if not isinstance(drop, (int, float)) or not math.isfinite(drop) or not 0 <= drop < seconds:
                        errors.append("Invalid climax position.")
                    elif float(media["format"]["duration"])+0.02 < min(seconds, drop+2):
                        errors.append("Music audition does not cover the climax and its context.")
                    elif not plan.get("segments") and plan.get("climax_source_seconds") is not None and abs(plan["climax_source_seconds"]-plan["excerpt_start_seconds"]-drop) > 1/project["fps"]:
                        errors.append("Source-to-video climax mapping is inconsistent.")
        if stage in ("motion", "render", "deliver") and policy.get("shot_approval") == "each":
            shots = read(root/"public/shots.json")
            ids = policy.get("shot_ids") or [s["id"] for s in shots if s.get("section") == "main"]
            approvals = read(root/"work/shot-approvals.json")["records"]
            for sid in ids:
                rows = [r for r in approvals if r.get("shot_id") == sid]
                if not rows:
                    errors.append("Missing user shot approval: " + sid)
                    continue
                row = rows[-1]
                if row.get("actor") != "user" or not row.get("source_ref") or not row.get("statement"):
                    errors.append("Invalid user shot approval: " + sid)
                if row.get("scope_sha256") != shot_scope(root, sid) or not row.get("files") or row["files"] != file_map(root, row["files"].keys()):
                    errors.append("Stale user shot approval: " + sid)
        if stage == "deliver":
            if video is None:
                errors.append("Delivery requires --video.")
            else:
                vpath = local(root, video)
                vhash = digest(vpath)
                fingerprint = production_fingerprint(root)
                media = read(root/"work/qc/media-report.json")
                project = read(root/"public/project.json")
                audio = read(root/"work/qc/audio-verification.json") if project.get("audio",{}).get("file") else {}
                render = read(root/"work/render-report.json")
                mux = read(root/"work/audio-mux.json")
                if render.get("draft") or render.get("production_fingerprint") != fingerprint:
                    errors.append("Production render is draft or stale.")
                if mux.get("final_sha256") != vhash or mux.get("production_fingerprint") != fingerprint:
                    errors.append("Mux evidence does not bind current final video/inputs.")
                if not media.get("full_decode_passed") or media.get("file_sha256") != vhash:
                    errors.append("Media QC does not bind a fully decoded final file.")
                if media.get("production_fingerprint") != fingerprint:
                    errors.append("Media QC input binding is stale.")
                lint = read(root/"work/lint-report.json")
                if not lint.get("passed") or lint.get("production_fingerprint") != fingerprint:
                    errors.append("Lint/TypeScript evidence is missing or stale.")
                if project.get("status") != "ready":
                    errors.append("Project is not ready.")
                if (media.get("width"), media.get("height"), media.get("frames")) != (project["width"], project["height"], project["durationFrames"]):
                    errors.append("Media dimensions/frames differ from project.")
                if project.get("audio", {}).get("required", True):
                    source = local(root, str(Path("public") / project["audio"]["file"]))
                    if not audio.get("passed") or audio.get("video_sha256") != vhash or audio.get("source_sha256") != digest(source):
                        errors.append("Audio verification is missing, stale, or failed.")
                visual = [r for r in data["records"] if r.get("gate") == "visual"]
                rel = str(vpath.relative_to(root)).replace(chr(92), "/")
                if not visual or visual[-1].get("files", {}).get(rel) != vhash:
                    errors.append("Visual review must explicitly bind this final MP4.")
                sys.path.insert(0, str(Path(__file__).resolve().parent))
                from audit_project import audit
                fresh_audit = audit(root)
                errors.extend("Project audit: " + e for e in fresh_audit["errors"])
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        errors.append(str(exc))
    return {"passed": not errors, "stage": stage, "errors": errors,
            "scope": "Evidence freshness and recorded gates only; not identity authentication, aesthetics, factual verification, or full listening."}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("init", "record", "record-shot", "check", "fingerprint"):
        q = sub.add_parser(name)
        q.add_argument("project")
        if name == "init":
            q.add_argument("--user-gates", default="music,look")
        if name == "record":
            q.add_argument("--gate", choices=GATES, required=True)
            q.add_argument("--actor", choices=("user", "agent"), required=True)
            q.add_argument("--statement", required=True)
            q.add_argument("--source-ref", default="")
            q.add_argument("--file", action="append", required=True)
        if name == "record-shot":
            q.add_argument("--shot-id", required=True)
            q.add_argument("--statement", required=True)
            q.add_argument("--source-ref", required=True)
            q.add_argument("--file", action="append", required=True)
        if name == "check":
            q.add_argument("--stage", choices=STAGES, required=True)
            q.add_argument("--video")
    a = p.parse_args()
    root = Path(a.project).resolve()
    try:
        if a.command == "init":
            result = init(root, tuple(filter(None, a.user_gates.split(","))))
        elif a.command == "record":
            result = record(root, a.gate, a.actor, a.statement, a.source_ref, a.file)
        elif a.command == "record-shot":
            result = record_shot(root, a.shot_id, a.statement, a.source_ref, a.file)
        elif a.command == "fingerprint":
            result = {"production_fingerprint": production_fingerprint(root)}
        else:
            result = check(root, a.stage, a.video)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if result.get("passed", True) else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
