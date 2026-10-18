"""Monta a trilha de imagem (sem áudio) a partir de um edl.json.

Cada trecho é extraído com re-encode no fps de saída e depois concatenado
sem novo encode (-c copy). Limites de corte são arredondados para frames.
Uso: python3 build_picture.py <edl.json> <saida.mp4>
"""
import json, os, subprocess, sys, tempfile

edl_path, out = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(edl_path))
edl = json.load(open(edl_path))
fps, dur, off = edl["fps"], edl["duration"], edl["offset"]
src = os.path.join(base, edl["source"])
F = lambda t: int(round(t * fps))

# linha do tempo em frames: inserts + preenchimento em sincronia
segs, cur = [], 0
for ins in sorted(edl["inserts"], key=lambda i: i["start"]):
    a, b = F(ins["start"]), F(ins["end"])
    if a > cur:
        segs.append((cur, a, off + cur / fps))
    segs.append((a, b, ins["src"]))
    cur = b
if cur < F(dur):
    segs.append((cur, F(dur), off + cur / fps))

vf = f"crop={edl['crop']},scale={edl['size']}:flags=lanczos,fps={fps},setsar=1"
tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(out)))
parts = []
for k, (a, b, s) in enumerate(segs):
    p = os.path.join(tmp, f"seg{k:03d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", src, "-an",
                    "-vf", vf, "-frames:v", str(b - a), "-c:v", "libx264", "-preset", "medium",
                    "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps), p], check=True)
    parts.append(p)
    print(f"{a/fps:6.2f}-{b/fps:6.2f}  src {s:7.2f}")
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                "-c", "copy", "-movflags", "+faststart", out], check=True)
for p in parts + [lst]:
    os.remove(p)
os.rmdir(tmp)
