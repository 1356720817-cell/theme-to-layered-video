"""Prepare a continuous music excerpt; does not imply user approval or rights clearance."""
import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from production_gate import digest

def prepare(root, source, output, start, duration, gain_db, fade_in, fade_out, climax_source=None):
    root = Path(root).resolve()
    source = (root/source).resolve()
    output = (root/output).resolve()
    values = [start, duration, gain_db, fade_in, fade_out] + ([] if climax_source is None else [climax_source])
    if not all(math.isfinite(x) for x in values):
        raise ValueError("All time/gain values must be finite.")
    if not source.is_file() or not output.is_relative_to(root/"public"):
        raise ValueError("Source must exist and output must stay inside project/public.")
    if output.exists() or output.with_suffix(".recipe.json").exists():
        raise ValueError("Refusing to overwrite an existing music version.")
    if start < 0 or duration <= 0 or min(fade_in, fade_out) < 0 or fade_in + fade_out > duration:
        raise ValueError("Invalid excerpt or fade durations.")
    probe = subprocess.run([os.environ.get("FFPROBE_BIN", "ffprobe"), "-v", "error", "-show_format", "-of", "json", str(source)], check=True, capture_output=True, text=True)
    full_duration = float(json.loads(probe.stdout)["format"]["duration"])
    if start + duration > full_duration + 0.01:
        raise ValueError("Requested excerpt exceeds actual source duration.")
    if climax_source is not None and not start <= climax_source < start+duration:
        raise ValueError("Climax must occur within the excerpt.")
    output.parent.mkdir(parents=True, exist_ok=True)
    filters = ["volume=" + str(gain_db) + "dB"]
    if fade_in:
        filters.append("afade=t=in:st=0:d=" + str(fade_in))
    if fade_out:
        filters.append("afade=t=out:st=" + str(duration-fade_out) + ":d=" + str(fade_out))
    subprocess.run([os.environ.get("FFMPEG_BIN", "ffmpeg"), "-v", "error", "-n", "-ss", str(start), "-i", str(source), "-t", str(duration),
                    "-vn", "-af", ",".join(filters), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)], check=True)
    report = {"source_file": str(source), "source_sha256": digest(source),
              "prepared_file": str(output.relative_to(root)), "prepared_sha256": digest(output),
              "excerpt_start_seconds": start, "excerpt_end_seconds": start+duration, "duration_seconds": duration,
              "gain_db": gain_db, "fade_in_seconds": fade_in, "fade_out_seconds": fade_out,
              "climax_source_seconds": climax_source, "climax_video_seconds": None if climax_source is None else climax_source-start,
              "user_approved": False, "rights_verified": False,
              "scope": "Continuous unretimed excerpt with baked gain/fades; inspect/listen before confirmation."}
    output.with_suffix(".recipe.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project")
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--start", type=float, required=True)
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--gain-db", type=float, default=0)
    p.add_argument("--fade-in", type=float, default=1)
    p.add_argument("--fade-out", type=float, default=2)
    p.add_argument("--climax-source", type=float)
    a = p.parse_args()
    try:
        print(json.dumps(prepare(a.project, a.source, a.output, a.start, a.duration, a.gain_db, a.fade_in, a.fade_out, a.climax_source), ensure_ascii=True, indent=2))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        p.exit(1, str(exc) + "\n")
if __name__ == "__main__":
    main()
