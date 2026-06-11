#!/usr/bin/env python3
"""Regenerate audio for the 90s trailer: 90s music + fuller VO script."""
import json, os, urllib.request
KEY = os.environ["ELEVENLABS_API_KEY"]; VOICE = os.environ["EL_VOICE_ID"]
OUT = os.path.join(os.path.dirname(__file__), "assets")

def post(url, body, name):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: audio = r.read()
        open(os.path.join(OUT, name), "wb").write(audio)
        print(f"OK  {name} ({len(audio)//1024} KB)", flush=True)
    except urllib.error.HTTPError as e:
        print(f"ERR {name}: HTTP {e.code} {e.read()[:300]}", flush=True)
    except Exception as e:
        print(f"ERR {name}: {e}", flush=True)

VO = {
  "vo_open.mp3":    "Setiap hari, data nasabah Indonesia bocor ke kanal-kanal gelap.",
  "vo_late.mp3":    "Dan lembaga keuangan, sering menjadi yang terakhir tahu.",
  "vo_gap.mp3":     "Terdeteksi rata-rata seratus enam puluh delapan hari kemudian. Padahal, regulasi menuntut laporan dalam dua puluh empat jam.",
  "vo_present.mp3": "Mempersembahkan... SHARK-Fin.",
  "vo_intel.mp3":   "Memantau sumber publik tanpa henti. Mengenali data finansial Indonesia — kartu, NIK, NPWP — secara presisi.",
  "vo_close.mp3":   "Mendeteksi kebocoran, lalu menjembatani temuan ke kewajiban pelaporan OJK. Sebelum data dieksploitasi.",
  "vo_end.mp3":     "SHARK-Fin. Melindungi ekosistem keuangan digital Indonesia.",
}
for name, text in VO.items():
    post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
         {"text": text, "model_id": "eleven_multilingual_v2",
          "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.35}}, name)

post("https://api.elevenlabs.io/v1/music",
     {"prompt": "Ninety second dark cinematic movie-trailer score with a clear arc: starts with a low pulsing sub-bass drone and ticking suspense, builds tension with rising strings and pulses, a powerful mid braam hit, a driving hybrid orchestral-electronic section, escalating to an epic triumphant climax, then a resolved hopeful outro. Modern cyber tech-thriller, no vocals.",
      "music_length_ms": 90000}, "music90.mp3")
print("audio90 done", flush=True)
