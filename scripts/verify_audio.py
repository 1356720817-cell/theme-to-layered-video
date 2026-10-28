"""Verify the actual approved master against final media. Not a listening/beat judgment."""
import argparse
import array
import json
import math
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from production_gate import digest, read

def ffmpeg(args, binary=False):
    r = subprocess.run([os.environ.get("FFMPEG_BIN", "ffmpeg"), "-v", "error"]+args, check=True, capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", errors="replace").strip()

def verify(root, video):
    root = Path(root).resolve()
    video = Path(video).resolve()
    p = read(root/"public/project.json")
    audio = p.get("audio", {})
    seconds = p["durationFrames"]/p["fps"]
    if not audio.get("file"):
        raise ValueError("Approved audio master is missing.")
    source = (root/"public"/audio["file"]).resolve()
    if not source.is_relative_to(root/"public") or not source.is_file():
        raise ValueError("Audio must exist inside public.")
    offset = float(audio.get("offsetSeconds", 0))
    report = {"source_sha256": digest(source), "video_sha256": digest(video),
              "source_offset_seconds": offset, "compared_seconds": seconds,
              "human_full_listening_review": False, "passed": False}
    args = ["-map", "0:a:0", "-c:a", "copy", "-f", "hash", "-hash", "sha256", "-"]
    if audio.get("copy") and offset == 0:
        sh = ffmpeg(["-i", str(source), "-t", str(seconds)]+args)
        vh = ffmpeg(["-i", str(video)]+args)
        report.update(method="compressed_audio_packet_sha256", source_packet_hash=sh, final_packet_hash=vh, passed=(sh == vh))
    else:
        def decode(path, start):
            raw = ffmpeg(["-ss", str(start), "-i", str(path), "-t", str(seconds), "-map", "0:a:0", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], True)
            a = array.array("f"); a.frombytes(raw)
            if sys.byteorder != "little":
                a.byteswap()
            return a
        x, y = decode(source, offset), decode(video, 0)
        n = min(len(x), len(y))
        if n < 800:
            raise ValueError("Audio is too short for waveform verification.")
        trim = min(4000, n//10)
        # Decimate to 1kHz; allow up to 20ms of codec alignment, not arbitrary music edits.
        xa = list(x[trim:n-trim:8]); ya = list(y[trim:n-trim:8])
        best = None
        for lag in range(-20, 21):
            lo = max(0, -lag); hi = min(len(xa), len(ya)-lag)
            xx = xa[lo:hi]; yy = ya[lo+lag:hi+lag]
            count = len(xx)
            if not count:
                continue
            sx = sum(xx); sy = sum(yy)
            vx = sum(t*t for t in xx)-sx*sx/count
            vy = sum(t*t for t in yy)-sy*sy/count
            covariance = sum(a*b for a,b in zip(xx, yy))-sx*sy/count
            corr = covariance / math.sqrt(vx*vy) if vx > 1e-12 and vy > 1e-12 else 0
            gain = math.sqrt(vy/vx) if vx > 1e-12 else 0
            if best is None or corr > best["correlation"]:
                best = {"lag_ms": lag, "correlation": corr, "rms_gain_ratio": gain}
        coverage_ok = abs(len(x)-len(y)) <= 800
        passed = coverage_ok and best["correlation"] >= 0.98 and 0.97 <= best["rms_gain_ratio"] <= 1.03
        report.update(method="decoded_waveform_correlation", sample_rate=8000, best_alignment=best,
                      duration_coverage_passed=coverage_ok, thresholds={"correlation_min":0.98,"gain_ratio":[0.97,1.03]}, passed=passed)
    report["scope"] = "Approved master matches final track under stated method; not a rights, peak/loudness, beat-naturalness, or full-listening review."
    folder = root/"work/qc"; folder.mkdir(parents=True, exist_ok=True)
    (folder/"audio-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project"); p.add_argument("--video", required=True)
    a = p.parse_args()
    try:
        result = verify(a.project, a.video)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if result["passed"] else 1
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"passed":False,"error":str(exc)}, ensure_ascii=True))
        return 1
if __name__ == "__main__":
    sys.exit(main())
