# SHARK-Fin — Trailer

A ~90s cinematic trailer for the SHARK-Fin pitch, built with **HyperFrames** (HTML-as-video).
Voiceover, music, and SFX by **ElevenLabs**; cinematic backgrounds by **OpenAI gpt-image-2**.

## Output

`renders/SHARK-Fin-Trailer.mp4` — 1920×1080, 30 fps, ~90 s.
(Render outputs and QA frames are gitignored; `index.html` + `assets/` are the reproducible source.)

## Structure (10 beats)

| # | Beat | t (s) | Background |
|---|------|-------|------------|
| 1 | Cold open — "Setiap hari, data Anda bocor." | 0–9 | `ocean-leak.png` |
| 2 | Problem — breach cases (BRI Life / BPJS / Dukcapil) | 9–18 | `soc-indonesia.png` |
| 3 | The gap — **168 hari vs 24 jam** | 18–29 | gradient |
| 4 | Hero reveal — "Mempersembahkan… SHARK-Fin" | 29–37 | `shark-fin.png` |
| 5 | Collection — 4 sumber OSINT | 37–46 | `collection-funnel.png` |
| 6 | Intelligence — classifier ID (kartu/NIK/NPWP) + risk score | 46–56 | `scanner-grid.png` |
| 7 | Action — webhook / draft SEOJK / audit | 56–65 | `alert-network.png` |
| 8 | Proof — 102 tes, 4 sumber, 8 entitas, UU PDP | 65–75 | dashboard + gradient |
| 9 | Vision — "ratusan hari → mendekati real-time" | 75–83 | `shield-archipelago.png` |
| 10 | End card — tagline + demo URL | 83–90 | gradient |

Blur-crossfade primary transition + color-dip-to-black on the hero reveal; Ken Burns on every shot.

## Audio — single pre-mixed master (important)

HyperFrames mixes audio with ffmpeg `amix` using `normalize` (default), which **scales each track's gain by the number of active inputs** — so background music audibly ducks whenever VO/SFX play. To avoid this, all audio is **pre-mixed into one master track** (`assets/master.m4a`) by `build_master.py` using `amix=normalize=0` + a limiter, then referenced as a single `<audio>` clip in `index.html`. Result: **loud, constant-level VO over a stable music bed (no ducking)**.

- Music bed: constant `0.30`. VO: `1.0` (≈ +8–11 dB above the bed). SFX: `0.5–0.75`.

## Assets (`assets/`)

- **Images** (gpt-image-2, 1536×1024): `ocean-leak`, `soc-indonesia`, `shark-fin`, `collection-funnel`, `scanner-grid`, `alert-network`, `shield-archipelago`; `dashboard.png` (from `docs/screenshots/`).
- **Audio** (ElevenLabs): `vo_*.mp3` (7 lines, voice `1k39YpzqXZn52BgyLyGO`, `eleven_multilingual_v2`), `music90.mp3` (Music API, 90 s), `sfx_*.mp3`. → mixed into `master.m4a`.

## Regenerate

API keys are read from the environment (never committed). Set `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `EL_VOICE_ID`, then:

```bash
python3 gen_images_90.py     # extra backgrounds (collection / scanner / alert)
python3 gen_audio_90.py      # 90s music + 7 VO lines
python3 build_master.py      # pre-mix master.m4a (stable music + loud VO + SFX)
```

## Render

```bash
hyperframes lint
hyperframes render --quality high --fps 30 --output renders/SHARK-Fin-Trailer.mp4
# fast iteration: hyperframes render --quality draft --fps 24
```
