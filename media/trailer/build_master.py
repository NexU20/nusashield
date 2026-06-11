#!/usr/bin/env python3
"""Pre-mix one master track: a flat, quiet music bed under loud, even VO.

dynaudnorm flattens the score's ~16 dB arc to a steady bed; VO is loudness-
normalised so every line matches; amix uses normalize=0 to avoid level ducking.
"""
import subprocess
A = "assets/"

# (file, delay_ms, volume, kind) — music: flattened bed; vo: normalised, on top; sfx: transient
clips = [
    ("music90.mp3",     0,     0.16, "music"),
    ("vo_open.mp3",     1500,  1.0,  "vo"),
    ("vo_late.mp3",     9800,  1.0,  "vo"),
    ("vo_gap.mp3",      18600, 1.0,  "vo"),
    ("vo_present.mp3",  29400, 1.0,  "vo"),
    ("vo_intel.mp3",    38000, 1.0,  "vo"),
    ("vo_close.mp3",    65600, 1.0,  "vo"),
    ("vo_end.mp3",      83600, 1.0,  "vo"),
    ("sfx_whoosh.mp3",  8900,  0.38, "sfx"),
    ("sfx_glitch.mp3",  17500, 0.42, "sfx"),
    ("sfx_impact.mp3",  28600, 0.5,  "sfx"),
    ("sfx_sonar.mp3",   29400, 0.42, "sfx"),
    ("sfx_whoosh.mp3",  37000, 0.35, "sfx"),
    ("sfx_whoosh.mp3",  46000, 0.35, "sfx"),
    ("sfx_whoosh.mp3",  56000, 0.35, "sfx"),
    ("sfx_whoosh.mp3",  65000, 0.35, "sfx"),
    ("sfx_whoosh.mp3",  75000, 0.35, "sfx"),
    ("sfx_impact.mp3",  83000, 0.5,  "sfx"),
]

inputs = []
for f, _, _, _ in clips:
    inputs += ["-i", A + f]

AFMT = "aformat=sample_rates=48000:channel_layouts=stereo"
parts, labels = [], []
for i, (f, d, v, kind) in enumerate(clips):
    lab = f"a{i}"
    if kind == "music":
        # f=500ms frames, g=31-frame gaussian (~15s) -> flattens the long arc,
        # keeps short-term dynamics; m caps boost so the quiet outro isn't over-driven.
        chain = f"[{i}:a]dynaudnorm=f=500:g=31:m=8:p=0.9,{AFMT}"
    elif kind == "vo":
        # single-pass loudnorm to a consistent broadcast level across all lines.
        chain = f"[{i}:a]loudnorm=I=-16:TP=-2:LRA=11,{AFMT}"
    else:
        chain = f"[{i}:a]{AFMT}"
    if d > 0:
        chain += f",adelay={d}:all=1"
    chain += f",volume={v}[{lab}]"
    parts.append(chain)
    labels.append(f"[{lab}]")

fg = (";".join(parts) + ";" + "".join(labels) +
      f"amix=inputs={len(clips)}:normalize=0:dropout_transition=0[mix];"
      "[mix]alimiter=limit=0.95:level=false[out]")

cmd = (["ffmpeg", "-y"] + inputs +
       ["-filter_complex", fg, "-map", "[out]", "-t", "90",
        "-c:a", "aac", "-b:a", "192k", A + "master.m4a"])
subprocess.run(cmd, check=True)
print("master.m4a built")
