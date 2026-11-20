#!/usr/bin/env python3
from pathlib import Path
screens = [
  'splash', 'home', 'live', 'guide', 'movies', 'series', 'kids',
  'favorites', 'search', 'sources', 'settings', 'player', 'editions'
]
for platform in ('android', 'windows', 'android-tv'):
    for screen in screens:
        path = Path('assets/screens') / platform / (screen + '.svg')
        if not path.exists() or '<svg ' not in path.read_text(encoding='utf-8'):
            raise SystemExit(f'Missing or invalid screen design: {path}')
print('Verified 39 design SVG files, across 3 platforms.')
