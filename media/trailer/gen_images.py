#!/usr/bin/env python3
"""Generate cinematic trailer backgrounds via OpenAI gpt-image-2."""
import base64, json, os, sys, urllib.request

KEY = os.environ["OPENAI_API_KEY"]
OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

PROMPTS = {
  "ocean-leak": "Cinematic widescreen film still, deep dark underwater digital ocean, abstract vertical streams of faint glowing data, digits and ID numbers drifting like debris through murky depths, ominous teal and black palette, distant red warning glints far below, volumetric god rays, moody atmospheric, anamorphic lens, ultra detailed, no text, no watermark",
  "shark-fin": "Cinematic widescreen film still, a sleek shark fin sculpted from glowing cyan circuitry and flowing data streams, slicing through the dark mirror surface of a digital ocean at night, dramatic rim light, ripples of luminous blue, sense of a powerful silent guardian predator, deep navy and black, filmic color grade, ultra detailed, no text, no watermark",
  "soc-indonesia": "Cinematic widescreen film still, a futuristic security operations command center at night, massive dark curved control screens displaying a glowing blue map of the Indonesian archipelago with pulsing red threat-alert pings, silhouettes of analysts watching, holographic blue UI panels, atmospheric haze, volumetric light, ultra detailed, no text, no watermark",
  "shield-archipelago": "Cinematic widescreen film still, the Indonesian archipelago seen from high orbit at night, a vast luminous protective dome of blue light shielding the islands, glowing connection lines linking cities, hopeful powerful mood, deep navy sky with subtle aurora, filmic, ultra detailed, no text, no watermark",
}

def gen(name, prompt):
    body = json.dumps({"model": "gpt-image-2", "prompt": prompt,
                       "size": "1536x1024", "quality": "high", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
        b64 = data["data"][0]["b64_json"]
        path = os.path.join(OUT, f"{name}.png")
        open(path, "wb").write(base64.b64decode(b64))
        print(f"OK  {name}.png ({os.path.getsize(path)//1024} KB)", flush=True)
    except urllib.error.HTTPError as e:
        print(f"ERR {name}: HTTP {e.code} {e.read()[:300]}", flush=True)
    except Exception as e:
        print(f"ERR {name}: {e}", flush=True)

for n, p in PROMPTS.items():
    gen(n, p)
print("images done", flush=True)
