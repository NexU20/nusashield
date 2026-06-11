#!/usr/bin/env python3
"""Generate 3 extra cinematic backgrounds for the 90s trailer's how-it-works beats."""
import base64, json, os, urllib.request
KEY = os.environ["OPENAI_API_KEY"]
OUT = os.path.join(os.path.dirname(__file__), "assets")

PROMPTS = {
  "collection-funnel": "Cinematic widescreen film still, multiple glowing blue rivers of data — chat messages, code, documents, search results — converging and pouring into a single bright funnel against a dark background, OSINT collection metaphor, volumetric light, ultra detailed, no text, no watermark",
  "scanner-grid": "Cinematic widescreen film still, a holographic blue scanning grid analyzing and highlighting fragments of ID cards and rows of financial numbers, precise targeting reticles locking onto matches, dark high-tech laboratory ambiance, depth of field, ultra detailed, no text, no watermark",
  "alert-network": "Cinematic widescreen film still, a single bright alert pulse radiating outward across a dark constellation network of glowing nodes toward a luminous shield, blue with amber warning accents, sense of real-time dispatch, atmospheric, ultra detailed, no text, no watermark",
}
def gen(name, prompt):
    body = json.dumps({"model":"gpt-image-2","prompt":prompt,"size":"1536x1024","quality":"high","n":1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: data = json.load(r)
        open(os.path.join(OUT, f"{name}.png"), "wb").write(base64.b64decode(data["data"][0]["b64_json"]))
        print(f"OK  {name}.png", flush=True)
    except urllib.error.HTTPError as e:
        print(f"ERR {name}: HTTP {e.code} {e.read()[:300]}", flush=True)
    except Exception as e:
        print(f"ERR {name}: {e}", flush=True)
for n,p in PROMPTS.items(): gen(n,p)
print("images90 done", flush=True)
