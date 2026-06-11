#!/usr/bin/env python3
"""Generate trailer audio via ElevenLabs: VO, music, SFX."""
import json, os, urllib.request

KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE = os.environ["EL_VOICE_ID"]
OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

def post(url, body, name):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            audio = r.read()
        path = os.path.join(OUT, name)
        open(path, "wb").write(audio)
        print(f"OK  {name} ({len(audio)//1024} KB)", flush=True)
    except urllib.error.HTTPError as e:
        print(f"ERR {name}: HTTP {e.code} {e.read()[:300]}", flush=True)
    except Exception as e:
        print(f"ERR {name}: {e}", flush=True)

# ── Voiceover (Indonesian, minimal) ──
VO = {
  "vo1.mp3": "Setiap hari, data nasabah Indonesia bocor ke kanal-kanal gelap.",
  "vo2.mp3": "Dan lembaga keuangan, sering menjadi yang terakhir tahu.",
  "vo3.mp3": "Mempersembahkan... SHARK-Fin.",
  "vo4.mp3": "Sebuah platform intelijen ancaman, yang mendeteksi kebocoran data keuangan sebelum dieksploitasi.",
}
for name, text in VO.items():
    post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
         {"text": text, "model_id": "eleven_multilingual_v2",
          "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3}}, name)

# ── Music (~32s cinematic trailer) ──
post("https://api.elevenlabs.io/v1/music",
     {"prompt": "Dark tense cinematic movie-trailer score, low pulsing sub-bass drone and ticking suspense building into an epic powerful hybrid orchestral-and-electronic climax with deep braam hits, modern cyber tech-thriller, no vocals, no melody vocals",
      "music_length_ms": 32000}, "music.mp3")

# ── SFX ──
SFX = {
  "sfx_whoosh.mp3": ("deep cinematic whoosh transition, fast air swoosh riser", 2),
  "sfx_impact.mp3": ("massive deep cinematic boom impact, trailer braam sub-bass hit", 3),
  "sfx_glitch.mp3": ("digital glitch alarm, data corruption stutter, error alert", 2),
  "sfx_sonar.mp3": ("single clean sonar detection ping, underwater echo", 2),
}
for name, (text, dur) in SFX.items():
    post("https://api.elevenlabs.io/v1/sound-generation",
         {"text": text, "duration_seconds": dur}, name)

print("audio done", flush=True)
