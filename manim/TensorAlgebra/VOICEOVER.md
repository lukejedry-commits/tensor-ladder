# Voice-over with ElevenLabs (Episode 0 trial)

Each beat of Episode 0 has its own narration clip. `voiceover.py` turns
`scripts/episode00_narration.py` into `audio/episode00/<beat>.mp3`, and each
scene plays those clips and holds every beat until its clip ends.

| File | Role |
|---|---|
| `scripts/episode00_narration.py` | **Source of truth for audio**: beat id → text with audio tags, plus `PRONUNCIATIONS` |
| `scripts/episode00_voiceover.md` | Human-readable script (on screen + said) |
| `voiceover.py` | CLI that generates and caches the clips, plus `NarrationMixin` (`with self.narrate("E00_03_b5"):`) |
| `audio/episode00/` | Generated clips + `manifest.json` (git-ignored by default) |

All commands below run in the Codespace terminal, from the TensorAlgebra folder:

```bash
cd /workspaces/tensor-ladder/manim/TensorAlgebra
```

## 1. One-time setup

```bash
pip install elevenlabs          # the only new dependency (Manim already ships PyAV)
```

Your key goes in `manim/TensorAlgebra/.env` (it is already git-ignored; `voiceover.py`
reads `.env` from its own folder and from the current directory):

```bash
# .env
ELEVENLABS_API_KEY=sk_...
# optional, these are the defaults:
# ELEVENLABS_VOICE_ID=3TStB8f3X3To0Uj5R7RK
# ELEVENLABS_MODEL=eleven_v3
# ELEVENLABS_STABILITY=0.5      # v3: 0.0 Creative, 0.5 Natural, 1.0 Robust
# ELEVENLABS_SEED=1234
```

A plain `export ELEVENLABS_API_KEY=...` works too, and so does a Codespaces secret
(GitHub → Settings → Codespaces → Secrets, named `ELEVENLABS_API_KEY`). Real
environment variables override `.env`.

Check that the `.env` stays untracked: `git check-ignore -v .env` should print a rule.

## 2. Pick a voice (optional)

The default is `3TStB8f3X3To0Uj5R7RK`. To list your voices:

```bash
python voiceover.py --list-voices
```

To try another voice, set `ELEVENLABS_VOICE_ID=<id>` in `.env`. The cache key includes the
voice, so the next run regenerates everything with the new voice.

## 3. Generate, then render

```bash
python voiceover.py episode00 --dry-run    # spoken text per beat, characters, cost. No API calls
python voiceover.py episode00              # generates only missing or changed clips
python voiceover.py episode00 --check      # every narrate() id matches a narration beat
manim -ql --disable_caching -a episode00.py          # preview, with sound
manim -qh --disable_caching -a episode00.py          # final quality
```

Join the scenes into one file:

```bash
ls media/videos/episode00/480p15/E00_0*.mp4 | sed "s|^|file '$PWD/|;s|$|'|" > concat00.txt
ffmpeg -f concat -safe 0 -i concat00.txt -c:v copy -c:a aac episode00_vo.mp4
```

(For `-qh` renders, use `1080p60` in place of `480p15`.)

Renders **never** call the API. If a clip is missing, the scene writes a silent placeholder and prints
`PLACEHOLDER`. If a clip is out of date (you changed its text or settings), it prints a
`stale` warning with the command to regenerate it.

To render silently with the old caption timing: `TENSOR_VO=off manim -ql -a episode00.py`.

## 4. Tweak a single beat

1. Edit the line in `scripts/episode00_narration.py` (and the matching line in the `.md`).
2. Regenerate only that beat, then re-render only its scene:

```bash
python voiceover.py episode00 --only E00_06_b2
manim -ql --disable_caching episode00.py E00_06_Beth
```

If a take sounds off but the text is right, keep the text and re-roll it: `--only E00_06_b2 --force`.
v3 is not fully deterministic, so a re-roll gives a slightly different read; the
`ELEVENLABS_SEED` makes it repeatable as far as ElevenLabs allows. `--only` can be repeated.

Beat ids are `E00_<scene>_b<n>`, in caption order within each scene. Run `--dry-run`
to see each one with its text.

## 5. Cost for Episode 0

49 beats, **6,442 characters** (audio tags and spaces count), about 8 minutes of speech.

- Subscription plans: about **6,400 credits** for one full pass (1 credit per character
  is the website rate; API requests are billed at a discount).
- Pay-as-you-go API: about **$0.52** (v3 costs $0.08 per 1,000 characters).

Clips that are already cached cost nothing. Re-rolling one beat costs about 100–250 characters.

## Tips for v3 audio tags

- Tags are directions, not words: `[warmly]`, `[curious]`, `[playfully]`, `[serious]`,
  `[short pause]`, `[laughs softly]`. Use them sparingly; Episode 0 has about one per scene.
- v3 ignores SSML `<break>`; use `[short pause]`, `...` or punctuation. Capitals add emphasis ("NOT").
- Stability: Natural (0.5) is the default. Creative (0.0) is livelier but can drift; Robust
  (1.0) mostly ignores tags.
- Write math the way you say it: "v super i", "beth, super i, sub j". `PRONUNCIATIONS`
  respells lone letters for the voice ("v" → "vee", "e" → "ee") and "tilde" → "tilda".
- Max 5,000 characters per request on v3; beats are far shorter, and longer text is split
  automatically at sentence ends.
- Eleven v4 (`ELEVENLABS_MODEL=eleven_v4`) is ElevenLabs' newer recommended model and
  takes the same tags. Switching models regenerates every clip.
