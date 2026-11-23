"""Build per-slide English narration (MP3) with caption cues for a 2300506 deck.

    python3 build_narration.py s01 --models /path/to/kokoro-models

Reads <session>-narration.json and writes
  narration/<session>/<slide-id>.en.mp3
  narration/<session>.json   (per slide: sentence texts and cue times)

Voice: Kokoro v1.0, am_michael, speed 0.94 (the same voice as the 2105603 and 2105315 decks).
A sentence may carry "say" when the spoken form should differ from the caption
(for example "C N Y 39 million" read as "39 million yuan").
"""
from pathlib import Path
import argparse
import json
import subprocess
import tempfile

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
GAP = 0.35            # silence between sentences, s
LEAD, TAIL = 0.25, 0.6


def write_mp3(audio, sr, path):
    with tempfile.NamedTemporaryFile(suffix='.wav') as wav:
        sf.write(wav.name, audio, sr, subtype='PCM_16')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav.name, '-ac', '1', '-b:a', '64k', str(path)], check=True)


def assemble(clips, sr):
    """Join sentence clips with gaps; return audio and (start, end) per sentence."""
    parts, cues, t = [np.zeros(int(LEAD * sr), dtype=np.float32)], [], LEAD
    for clip in clips:
        clip = clip.astype(np.float32)
        clip *= min(1.0, 0.89 / (float(np.max(np.abs(clip))) or 1.0))
        cues.append([round(t, 2), round(t + len(clip) / sr, 2)])
        parts += [clip, np.zeros(int(GAP * sr), dtype=np.float32)]
        t += len(clip) / sr + GAP
    parts.append(np.zeros(int(TAIL * sr), dtype=np.float32))
    return np.concatenate(parts), cues


import re

# Spoken forms. Captions keep the written text; the voice reads these instead.
SPOKEN = [
    (r'\bCNY ([\d.,]+) million\b', r'\1 million yuan'),
    (r'\bCNY\b', 'yuan'),
    (r'\bCellCo\b', 'Cell Co'),
    (r'\bGWh\b', 'gigawatt hours'),
    (r'\bMILP\b', 'M I L P'),
    (r'\bDMAIC\b', 'dee may ick'),
    (r'\bCUSUM\b', 'cue sum'),
    (r'\bPuLP\b', 'pulp'),
    (r'\b(EMV|EOL|EVPI|EVSI|AHP|NPV|LFP|LCOS|CE|CR|MDP|HQU|LP|SQC|OEE|RTY|FPY|DPMO|PERT|CPM|EWMA|GRR)\b', lambda m: ' '.join(m.group(1))),
    (r'−(?=\d)', 'minus '),
    (r'≈', 'about'),
    (r'α', 'alpha'),
    (r'\bHurwicz\b', 'Hurvitch'),
]


def speakable(text):
    for pat, rep in SPOKEN:
        text = re.sub(pat, rep, text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('session')
    ap.add_argument('--models', default=str(HERE / 'kokoro-models'))
    ap.add_argument('--slides', nargs='*', help='rebuild only these slide ids (others keep their audio)')
    args = ap.parse_args()
    from kokoro_onnx import Kokoro
    spec = json.loads((HERE / f'{args.session}-narration.json').read_text())
    voice = spec.get('voice_en', 'am_michael')
    k = Kokoro(str(Path(args.models) / 'kokoro-v1.0.onnx'), str(Path(args.models) / 'voices-v1.0.bin'))
    out_dir = HERE / 'narration' / args.session
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = HERE / 'narration' / f'{args.session}.json'
    old = json.loads(index_path.read_text()) if index_path.exists() else {}
    index = {}
    for slide_id, sentences in spec['slides'].items():
        text = [s['en'] for s in sentences]
        if args.slides and slide_id not in args.slides and slide_id in old and old[slide_id].get('text') == text:
            index[slide_id] = old[slide_id]
            continue
        clips = []
        for s in sentences:
            audio, sr = k.create(speakable(s.get('say', s['en'])), voice=voice, speed=0.94, lang='en-us')
            assert sr == 24000
            clips.append(audio)
        audio, cues = assemble(clips, 24000)
        write_mp3(audio, 24000, out_dir / f'{slide_id}.en.mp3')
        index[slide_id] = {'text': text, 'en': {'audio': f'narration/{args.session}/{slide_id}.en.mp3', 'cues': cues}}
        print(slide_id, f'{cues[-1][1]:.1f}s', flush=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
