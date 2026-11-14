"""
voiceover.py: ElevenLabs narration for the tensor series (shared by all episodes).

Two halves:
  1. A CLI that turns  scripts/<episode>_narration.py  into one mp3 per beat
     under  audio/<episode>/<beat_id>.mp3 , cached by a hash of
     (spoken text, voice, model, settings, format, seed), so re-rendering
     never spends credits twice.

         python voiceover.py episode00 --dry-run      # chars / credits, no API calls
         python voiceover.py episode00                # generate what's missing/stale
         python voiceover.py episode00 --only E00_03_b5 --force
         python voiceover.py episode00 --placeholder  # offline silent clips
         python voiceover.py episode00 --check        # beat ids in narration vs episode00.py
         python voiceover.py --list-voices

  2. NarrationMixin for scenes:  with self.narrate("E00_03_b5"): ...
     adds the clip at beat start and, on exit, waits out the rest of the clip.
     TENSOR_VO=off renders silently with each episode's old timing.

Config (environment, or a git-ignored `.env` next to this file or in the cwd):
  ELEVENLABS_API_KEY     required for real audio (no key -> placeholders)
  ELEVENLABS_VOICE_ID    default 3TStB8f3X3To0Uj5R7RK
  ELEVENLABS_MODEL       default eleven_v3
  ELEVENLABS_STABILITY   v3: 0.0 Creative, 0.5 Natural (default), 1.0 Robust
  ELEVENLABS_SEED        default 1234 (best-effort determinism)
  ELEVENLABS_SPEED       non-v3 models only (0.7-1.2)
  TENSOR_VO              on (default) / off

Dependencies: the `elevenlabs` SDK for real generation only. Durations and
placeholder clips use PyAV (`av`), which Manim CE already installs. No ffmpeg
binary, mutagen, pydub or python-dotenv needed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent

DEFAULT_VOICE_ID = "3TStB8f3X3To0Uj5R7RK"
DEFAULT_MODEL = "eleven_v3"
OUTPUT_FORMAT = "mp3_44100_128"     # 128 kbps works on every plan (192 needs Creator+)
PLACEHOLDER_WPM = 150

# Per-request character limits (ElevenLabs "Models" docs, Nov 2026).
CHAR_LIMITS = {
    "eleven_v3": 5000,
    "eleven_v4": 10000,
    "eleven_multilingual_v2": 10000,
    "eleven_flash_v2_5": 40000,
    "eleven_flash_v2": 30000,
}
# Pay-as-you-go API price per 1,000 characters (elevenlabs.io/pricing/api, Nov 2026).
USD_PER_1K = {"eleven_v3": 0.08, "eleven_v4": 0.08, "eleven_multilingual_v2": 0.08,
              "eleven_flash_v2_5": 0.04, "eleven_flash_v2": 0.04}

TAG_RE = re.compile(r"\[[^\]]*\]")


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
def load_dotenv() -> list[Path]:
    """Minimal .env loader (KEY=VALUE lines). Real env vars always win.

    Looks in this file's folder (manim/TensorAlgebra/) and in the cwd.
    A `.env` that is a directory (e.g. a virtualenv) is ignored.
    """
    loaded = []
    for d in dict.fromkeys([HERE, Path.cwd().resolve()]):
        f = d / ".env"
        if not f.is_file():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip().removeprefix("export ").strip()
            v = v.strip().strip('"').strip("'")
            os.environ.setdefault(k, v)
        loaded.append(f)
    return loaded


def settings() -> dict:
    """Everything that changes the audio (and therefore the cache key)."""
    load_dotenv()
    model = os.environ.get("ELEVENLABS_MODEL", DEFAULT_MODEL)
    voice = os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE_ID)
    vs = {"stability": float(os.environ.get("ELEVENLABS_STABILITY", "0.5"))}
    if not model.startswith("eleven_v3"):
        # v3 only honours stability (Creative/Natural/Robust); the others are
        # accepted but ignored, so we don't send them (and don't hash them).
        vs["similarity_boost"] = float(os.environ.get("ELEVENLABS_SIMILARITY", "0.75"))
        vs["style"] = float(os.environ.get("ELEVENLABS_STYLE", "0.0"))
        vs["speed"] = float(os.environ.get("ELEVENLABS_SPEED", "1.0"))
    return {"voice_id": voice, "model_id": model, "voice_settings": vs,
            "output_format": OUTPUT_FORMAT, "seed": int(os.environ.get("ELEVENLABS_SEED", "1234"))}


def api_key() -> str | None:
    load_dotenv()
    return os.environ.get("ELEVENLABS_API_KEY") or None


def vo_enabled() -> bool:
    load_dotenv()
    return os.environ.get("TENSOR_VO", "on").strip().lower() not in ("off", "0", "false", "no")


# --------------------------------------------------------------------------
# Narration source
# --------------------------------------------------------------------------
def load_narration(episode: str):
    path = HERE / "scripts" / f"{episode}_narration.py"
    if not path.is_file():
        sys.exit(f"No narration file: {path}")
    spec = importlib.util.spec_from_file_location(f"{episode}_narration", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.NARRATION), dict(getattr(mod, "PRONUNCIATIONS", {}))


def spoken_text(text: str, pron: dict) -> str:
    """Apply whole-word pronunciation substitutions outside [audio tags]."""
    parts = re.split(r"(\[[^\]]*\])", text)
    for i, p in enumerate(parts):
        if p.startswith("["):
            continue
        for src, dst in pron.items():
            p = re.sub(rf"(?<![\w-]){re.escape(src)}(?![\w-])", dst, p)
        parts[i] = p
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def word_count(text: str) -> int:
    return len(TAG_RE.sub(" ", text).split())


def estimate_seconds(text: str) -> float:
    pauses = len(re.findall(r"\[(short |long )?pause\]", text)) + text.count("...")
    return word_count(text) / PLACEHOLDER_WPM * 60 + 0.4 * pauses


def clip_hash(text: str, cfg: dict) -> str:
    blob = json.dumps({"text": text, **cfg}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def audio_dir(episode: str) -> Path:
    return HERE / "audio" / episode


def read_manifest(episode: str) -> dict:
    f = audio_dir(episode) / "manifest.json"
    return json.loads(f.read_text()) if f.is_file() else {}


def write_manifest(episode: str, man: dict):
    d = audio_dir(episode)
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps(man, indent=2, sort_keys=True) + "\n")


# --------------------------------------------------------------------------
# Audio helpers (PyAV)
# --------------------------------------------------------------------------
def audio_duration(path: Path) -> float:
    """Exact duration in seconds by decoding (clips are short, this is fast)."""
    import av
    with av.open(str(path)) as c:
        stream = c.streams.audio[0]
        samples, rate = 0, stream.rate or stream.codec_context.sample_rate
        for frame in c.decode(stream):
            samples += frame.samples
    return samples / rate if rate else 0.0


def write_placeholder(path: Path, seconds: float, rate: int = 44100):
    """Silent mp3 of the given length with a soft 60 ms tick at the start,
    so beat boundaries are audible when checking sync."""
    import av
    import numpy as np
    n = int(round(seconds * rate))
    sig = np.zeros(n, dtype=np.float32)
    tick = int(0.06 * rate)
    t = np.arange(tick) / rate
    sig[:tick] = 0.05 * np.sin(2 * np.pi * 880 * t) * np.hanning(tick)
    path.parent.mkdir(parents=True, exist_ok=True)
    with av.open(str(path), "w", format="mp3") as out:
        st = out.add_stream("libmp3lame", rate=rate)
        st.layout = "mono"
        step = 1152 * 8
        for i in range(0, n, step):
            chunk = sig[i:i + step].reshape(1, -1)
            fr = av.AudioFrame.from_ndarray(chunk, format="flt", layout="mono")
            fr.sample_rate = rate
            for pkt in st.encode(fr):
                out.mux(pkt)
        for pkt in st.encode(None):
            out.mux(pkt)


def split_for_limit(text: str, limit: int) -> list[str]:
    """Split at sentence ends so every request is under the model's char limit."""
    if len(text) <= limit:
        return [text]
    chunks, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+", text):
        if len(s) > limit:
            raise ValueError(f"A single sentence is longer than {limit} characters.")
        if cur and len(cur) + 1 + len(s) > limit:
            chunks.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    return chunks + ([cur] if cur else [])


def synthesize(text: str, cfg: dict, key: str) -> bytes:
    """One beat -> mp3 bytes via the official SDK (elevenlabs >= 2.x)."""
    from elevenlabs import VoiceSettings
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(api_key=key)
    limit = CHAR_LIMITS.get(cfg["model_id"], 5000)
    out = b""
    # Note: v3 rejects previous_text/next_text (400), so no stitching hints.
    for chunk in split_for_limit(text, limit):
        stream = client.text_to_speech.convert(
            cfg["voice_id"],
            text=chunk,
            model_id=cfg["model_id"],
            output_format=cfg["output_format"],
            voice_settings=VoiceSettings(**cfg["voice_settings"]),
            seed=cfg["seed"],
        )
        out += b"".join(stream)   # MP3 frames concatenate cleanly
    return out


# --------------------------------------------------------------------------
# Clip lookup used at render time
# --------------------------------------------------------------------------
def ensure_clip(episode: str, beat: str) -> tuple[Path, float, bool]:
    """Path, duration, is_placeholder for a beat. Never calls the API: a missing
    clip gets an offline placeholder so the render still works."""
    narr, pron = load_narration(episode)
    if beat not in narr:
        raise KeyError(f"Beat {beat!r} is not in scripts/{episode}_narration.py")
    path = audio_dir(episode) / f"{beat}.mp3"
    man = read_manifest(episode)
    entry = man.get(beat)
    text = spoken_text(narr[beat], pron)
    h = clip_hash(text, settings())
    if not path.is_file() or entry is None:
        dur = estimate_seconds(narr[beat])
        write_placeholder(path, dur)
        man[beat] = {"hash": None, "placeholder": True, "chars": len(text)}
        entry = man[beat]
        write_manifest(episode, man)
        print(f"[voiceover] PLACEHOLDER for {beat} (run: python voiceover.py {episode})")
    elif not entry.get("placeholder") and entry.get("hash") != h:
        print(f"[voiceover] WARNING: {beat}.mp3 is stale (text or settings changed). "
              f"Run: python voiceover.py {episode} --only {beat}")
    return path, audio_duration(path), bool(entry.get("placeholder"))


class NarrationMixin:
    """Mix into a Scene (before TensorScene).  Set EPISODE = "episode00".

        with self.narrate("E00_03_b5"):
            self.play(...)          # animations run while the voice plays
            self.caption("...")     # caption holds are skipped inside a beat

    On exit the scene waits until the clip has finished, plus VO_TAIL seconds
    of breathing room. If the animations ran longer than the clip, only the
    tail is added. With TENSOR_VO=off the block runs with the old timing.
    """

    EPISODE: str = ""
    VO_TAIL = 0.35
    _vo_active = False

    @contextmanager
    def narrate(self, beat: str, delay: float = 0.0, tail: float | None = None):
        if not vo_enabled():
            yield
            return
        path, dur, placeholder = ensure_clip(self.EPISODE, beat)
        if delay:
            self.wait(delay)
        t0 = self.time
        self.add_sound(str(path))
        self._vo_active = True
        try:
            yield
        finally:
            self._vo_active = False
        tail = self.VO_TAIL if tail is None else tail
        self.wait(max(tail, dur + tail - (self.time - t0)))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def cmd_list_voices():
    key = api_key()
    if not key:
        sys.exit("ELEVENLABS_API_KEY is not set (env or .env).")
    from elevenlabs.client import ElevenLabs
    client = ElevenLabs(api_key=key)
    resp = client.voices.search(page_size=100)
    for v in resp.voices:
        labels = ", ".join(f"{k}={val}" for k, val in (v.labels or {}).items())
        print(f"{v.voice_id}  {v.name:<28} {v.category or '':<12} {labels}")


def cmd_check(episode: str, narr: dict):
    src = (HERE / f"{episode}.py").read_text()
    used = re.findall(r"narrate\(\s*[\"']([^\"']+)[\"']", src)
    missing = [b for b in used if b not in narr]
    unused = [b for b in narr if b not in used]
    dupes = sorted({b for b in used if used.count(b) > 1})
    print(f"{len(used)} narrate() calls, {len(narr)} narration beats")
    for label, items in (("missing from narration", missing), ("never narrated", unused),
                         ("used twice", dupes)):
        if items:
            print(f"  {label}: {', '.join(items)}")
    if not (missing or unused or dupes):
        print("  OK: every beat is used exactly once.")
    return not (missing or unused or dupes)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("episode", nargs="?", help="e.g. episode00")
    ap.add_argument("--only", action="append", metavar="BEAT", help="beat id (repeatable)")
    ap.add_argument("--force", action="store_true", help="regenerate even if cached")
    ap.add_argument("--dry-run", action="store_true", help="show text/chars/credits, call nothing")
    ap.add_argument("--placeholder", action="store_true", help="write offline placeholder clips")
    ap.add_argument("--check", action="store_true", help="compare beat ids with <episode>.py")
    ap.add_argument("--list-voices", action="store_true")
    a = ap.parse_args(argv)

    if a.list_voices:
        return cmd_list_voices()
    if not a.episode:
        ap.error("episode is required")
    narr, pron = load_narration(a.episode)
    if a.check:
        sys.exit(0 if cmd_check(a.episode, narr) else 1)
    if a.only:
        bad = [b for b in a.only if b not in narr]
        if bad:
            sys.exit(f"Unknown beat(s): {', '.join(bad)}")
    beats = a.only or list(narr)

    cfg = settings()
    key = api_key()
    placeholder = a.placeholder or not key
    man = read_manifest(a.episode)
    d = audio_dir(a.episode)
    limit = CHAR_LIMITS.get(cfg["model_id"], 5000)

    print(f"episode {a.episode} | model {cfg['model_id']} | voice {cfg['voice_id']} | "
          f"settings {cfg['voice_settings']} | key {'set' if key else 'NOT SET'}")
    if placeholder and not a.dry_run:
        why = "--placeholder" if a.placeholder else "no ELEVENLABS_API_KEY"
        print(f"*** OFFLINE PLACEHOLDERS ({why}): silent clips timed at "
              f"{PLACEHOLDER_WPM} wpm. Not real narration. ***")

    tot_chars = todo_chars = 0
    for b in beats:
        text = spoken_text(narr[b], pron)
        h = clip_hash(text, cfg)
        e = man.get(b, {})
        path = d / f"{b}.mp3"
        cached = path.is_file() and e.get("hash") == h and not e.get("placeholder")
        n = len(text)
        tot_chars += n
        need = a.force or not cached
        if need:
            todo_chars += n
        if n > limit:
            print(f"  note: {b} has {n} chars > {limit}; it will be split into several requests")
        status = "cached" if cached and not a.force else "TODO"
        if a.dry_run:
            print(f"\n[{b}] {status} | {word_count(text)} words | {n} chars | "
                  f"~{estimate_seconds(narr[b]):.1f}s\n  {text}")
            continue
        if not need:
            print(f"  {b}: cached ({e.get('duration', 0):.2f}s)")
            continue
        if placeholder:
            if e and not e.get("placeholder") and path.is_file() and not a.placeholder:
                print(f"  {b}: keeping existing real clip (no key to refresh it)")
                continue
            write_placeholder(path, estimate_seconds(narr[b]))
            man[b] = {"hash": None, "placeholder": True, "chars": n}
        else:
            print(f"  {b}: generating {n} chars ...", flush=True)
            try:
                data = synthesize(text, cfg, key)
            except Exception as err:   # ApiError (401 bad key, 402/429 quota, 400 ...)
                write_manifest(a.episode, man)
                body = getattr(err, "body", None)
                sys.exit(f"\nElevenLabs request failed for {b}: {getattr(err, 'status_code', '')} "
                         f"{body or err}\nClips finished so far are saved; re-run to resume.")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            man[b] = {"hash": h, "placeholder": False, "chars": n, "text": text,
                      "model_id": cfg["model_id"], "voice_id": cfg["voice_id"]}
        man[b]["duration"] = round(audio_duration(path), 3)
        print(f"  {b}: {'placeholder' if placeholder else 'ok'} {man[b]['duration']:.2f}s")
        write_manifest(a.episode, man)

    usd = USD_PER_1K.get(cfg["model_id"], 0.08)
    print(f"\nTotal: {len(beats)} beats, {tot_chars} characters "
          f"(tags and spaces count). To generate now: {todo_chars} characters.")
    print(f"Estimated cost of what's TODO: ~{todo_chars} credits on a subscription "
          f"(1 credit/char, website rate; API is usually billed at a discount) "
          f"or ~${todo_chars / 1000 * usd:.2f} pay-as-you-go at ${usd}/1K chars.")


if __name__ == "__main__":
    main()
