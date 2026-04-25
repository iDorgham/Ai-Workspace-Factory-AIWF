# TOMBSTONED: 2026-04-25 | Reason: DEPRECATED | Successor: N/A | Do not import.
#!/usr/bin/env python3
from pathlib import Path
import json, argparse
ROOT = Path(__file__).resolve().parents[1]

fields = [
    ('client_name','Client name'),('workspace_slug','Workspace slug'),('workspace_purpose','Profile/purpose'),
    ('team_level','Team level (non-dev/mixed/dev)'),('delivery_mode','Delivery mode (founder/pro/hybrid)'),
    ('required_modules','Required modules (comma-separated)'),('compliance_level','Compliance level'),
    ('language_support','Language support (comma-separated)'),('deployment_target','Deployment target'),
    ('notes','Notes'),('client_contacts','Client contacts (comma-separated)'),('website','Website'),('social_media','Social media URLs (comma-separated)')
]

def splitcsv(v):
    return [x.strip() for x in v.split(',') if x.strip()]

def prompt(k, label):
    return input(f'{label}: ').strip()

data = {}
for k,label in fields:
    val = prompt(k,label)
    if k in {'required_modules','language_support','client_contacts','social_media'}:
        data[k] = splitcsv(val)
    else:
        data[k] = val

client = data['workspace_slug'] or data['client_name'].lower().replace(' ','-')
out = ROOT / 'intake' / f'{client}.json'
out.write_text(json.dumps(data, indent=2) + "\n")
print(f'Wrote {out}')
