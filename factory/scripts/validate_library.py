#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
errors = []
required = {'id','type','name','version','source','source_path','tags','dependencies','compatibility','quality_status','last_synced_at'}
for meta in ROOT.glob('library/*/**/*.meta.json'):
    data = json.loads(meta.read_text())
    missing = required - set(data.keys())
    if missing:
        errors.append(f"{meta}: missing {sorted(missing)}")
if errors:
    print('Library validation FAILED')
    print('\n'.join(errors))
    sys.exit(1)
print('Library validation passed')
