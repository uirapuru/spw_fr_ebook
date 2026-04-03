#!/usr/bin/env python3
import os
import urllib.parse
from pathlib import Path

import generate_attribution as ga

path = Path('zrodla_grafik.md')
raw_lines = path.read_text(encoding='utf-8').splitlines()
entries = []
idx = 0
while idx < len(raw_lines):
    line = raw_lines[idx].strip()
    if not (line.startswith('- Zdj.') or line.startswith('Zdj.')):
        idx += 1
        continue

    line = line[2:].strip() if line.startswith('- ') else line
    match = __import__('re').match(r'^Zdj\.\s*(\d+)\.\s*(.*)$', line)
    if not match:
        idx += 1
        continue
    number = int(match.group(1))
    rest = match.group(2)

    local_key = None
    if '**plik**:' in rest:
        after = rest.split('**plik**:', 1)[1].strip()
        local_key = after.split('`', 2)[1]
        after = after.split('`, ', 1)[1]
    else:
        idx += 1
        continue

    artist = after.split('**autor**:', 1)[1].split(', lic.', 1)[0].strip()
    license_str = after.split(', lic.', 1)[1].strip()
    if ', **url**:' in license_str:
        license_str, inline_url = license_str.split(', **url**:', 1)
        url = inline_url.strip()
    else:
        license_str = license_str.rstrip(',')
        url = '—'
        if idx + 1 < len(raw_lines):
            next_line = raw_lines[idx + 1].strip()
            if next_line.startswith('**url**:'):
                url = next_line.split(':', 1)[1].strip()
                if url.startswith('[Wikimedia Commons](') and url.endswith(')'):
                    url = url[len('[Wikimedia Commons]('):-1]
                    if url.startswith('<') and url.endswith('>'):
                        url = url[1:-1]
                idx += 1

    if url == '—' or not url:
        fixed_url = '—'
    elif url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        fixed_url = url
    else:
        commons_name = ga.resolve_commons_filename(local_key)
        if commons_name:
            fixed_url = 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(commons_name.replace(' ', '_'))
        else:
            fixed_url = url

    entries.append((number, os.path.basename(local_key), artist, license_str.strip(), fixed_url))
    idx += 1

if not entries:
    raise SystemExit('No entries parsed')

out = [
    '# Źródła grafik',
    '',
    'Wszystkie grafiki użyte w podręczniku pochodzą z **Wikimedia Commons** i są dostępne na wolnych licencjach. Poniżej zestawienie każdego obrazu z podaniem autora, licencji i odnośnika do strony źródłowej.',
    '',
    'Każdy punkt zawiera nazwę pliku, autora, licencję i klikalny odnośnik URL do strony pliku w Wikimedia Commons.',
    ''
]
for number, file_name, artist, license_str, url in entries:
    out.append(f'Zdj. {number}. `{file_name}`, **autor**: {artist}, lic. {license_str},')
    out.append(f'**url**: [Wikimedia Commons](<{url}>)')
    out.append('')
path.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'Rebuilt {len(entries)} entries')
