import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

repo = Path('.')
global_json = repo / 'global.json'
if global_json.exists():
    data = json.loads(global_json.read_text(encoding='utf-8'))
    sdk = data.get('sdk', {}).get('version')
    if sdk:
        parts = sdk.split('.')
        if len(parts) >= 2:
            print(f"{parts[0]}.{parts[1]}.x")
        else:
            print(f"{sdk}.x")
        raise SystemExit(0)

for csproj in sorted(repo.glob('*.csproj')):
    root = ET.parse(csproj).getroot()
    tfm = None
    for node_name in ('TargetFramework', 'TargetFrameworks'):
        node = root.find(f'.//{node_name}')
        if node is not None and node.text:
            tfm = node.text.split(';')[0].strip()
            break
    if not tfm:
        continue
    m = re.match(r'^net(\d+)\.(\d+)', tfm)
    if m:
        print(f"{m.group(1)}.{m.group(2)}.x")
        raise SystemExit(0)

print('Unable to determine required .NET SDK version.', file=sys.stderr)
raise SystemExit(1)
