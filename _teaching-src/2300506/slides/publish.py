"""Copy rendered decks from _site/ to teaching/2300506/slides/.

    quarto render s01.qmd && python3 publish.py

Two changes on the way:
- slides.css is linked with a content hash, because GitHub Pages lets browsers keep it for 10 minutes;
- each deck gets its narration index inlined (script#nr-data), so narration and captions also work
  when students open the deck from a downloaded folder (no web server, fetch() of local files blocked).
"""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEST = REPO / 'teaching/2300506/slides'
SITE = HERE / '_site'

css = SITE / 'slides.css'
version = hashlib.md5(css.read_bytes()).hexdigest()[:8] if css.exists() else ''

for path in sorted(SITE.rglob('*')):
    if path.is_dir():
        continue
    target = DEST / path.relative_to(SITE)
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == '.html':
        html = path.read_text(encoding='utf-8')
        if version:
            html = html.replace('href="slides.css"', f'href="slides.css?v={version}"')
        index = SITE / 'narration' / f'{path.stem}.json'
        if index.exists():
            payload = json.dumps(json.loads(index.read_text()), ensure_ascii=False, separators=(',', ':'))
            payload = payload.replace('</', '<\\/')
            html = html.replace('</body>', f'<script type="application/json" id="nr-data">{payload}</script>\n</body>', 1)
        target.write_text(html, encoding='utf-8')
    else:
        shutil.copyfile(path, target)
    print(target.relative_to(REPO))
