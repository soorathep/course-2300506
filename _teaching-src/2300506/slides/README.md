# 2300506 session decks

Eighteen sessions (Block 1: s01 to s10, 23 and 24 January 2027; Block 2: s11 to s18, 27 and 28 March 2027),
one Quarto + Reveal.js deck each, published at `teaching/2300506/slides/sNN.html`. Built one at a time.

Controls at the bottom left of every deck:

- **Narration**: off / on (English, Kokoro v1.0, voice am_michael, as in the 2105603 and 2105315 decks).
- **Pause / Resume** and **Replay slide** while narration is on.
- **Captions**: off / on (English). With narration off, the slide's full narration text is shown.
- **Auto-advance**: next slide when the narration ends; slides with `data-hold` wait.

Settings are remembered in the browser (keys `nr506-*`).

## Session pattern

Concepts, Activity 1 (pairs, paper), concepts, Activity 2, debrief, exit ticket on paper.
Activity slides use `.activity` (amber rule) and end with a note for students studying alone.
Interactive slides are raw HTML blocks with their own script; clicks inside them do not advance the slide.

## Files

| File | Role |
|---|---|
| `s01.qmd` | slides; slide ids (`{#route}`) must match the narration keys; the title slide is `title-slide` |
| `s01-narration.json` | per slide, the sentences (`en`), with optional `say` when the spoken form differs |
| `build_narration.py` | writes `narration/s01/<slide>.en.mp3` and `narration/s01.json` (texts and cue times); `SPOKEN` maps acronyms and CNY amounts to spoken forms |
| `narration-player.html` | controls and caption box; reads the index inlined in the page, or fetches it |
| `slides.css` | layouts; theme and click-to-advance are in `theme/` (copied from 2105603) |
| `publish.py` | copies `_site/` to `teaching/2300506/slides/` and inlines the narration index into each deck |

## Build

```bash
pip install quarto-cli kokoro-onnx soundfile
python3 build_narration.py s01 --models <folder with kokoro-v1.0.onnx and voices-v1.0.bin>
quarto render s01.qmd
python3 publish.py
```

Kokoro model files: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0

After publishing, refresh the offline copy:
`cd ../../../teaching/2300506/slides && zip -r ../../../downloads/2300506-s01-offline.zip s01.html s01_files narration/s01 narration/s01.json slides.css`
