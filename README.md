# Course 2300506 Industrial Science (HQU)

Course website for the parts of 2300506 Industrial Science taught by Soorathep Kheawhom at Huaqiao University,
International College of New Energy, under the Chula Faculty of Science Global Academic Collaboration Sandbox.

Published URL: https://soorathep.github.io/course-2300506/

Main research website: https://www.skhgroup.net (do not copy its CNAME here).

## Layout

| Path | Role |
|---|---|
| `index.html` | course page, lists the 18 sessions |
| `teaching/2300506/slides/` | published decks (`sNN.html`, `sNN_files/`, `narration/`) |
| `downloads/` | offline ZIP of each deck, for students with slow access to GitHub Pages |
| `_teaching-src/2300506/slides/` | Quarto source, narration scripts, build and publish scripts; see its README |
| `.nojekyll` | GitHub Pages serves files as they are, no Jekyll build |

Same pattern as the 2105315 and 2105603 decks: Quarto + Reveal.js, teal-amber theme (fonts inlined), English
narration with Kokoro v1.0 voice am_michael, English captions, auto-advance. No external font or CDN requests,
so the decks load in mainland China wherever GitHub Pages loads.

## Publishing

Push to `main`. GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root.
