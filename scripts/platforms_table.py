#!/usr/bin/env python3
"""Render data/platforms.yaml as docs/platforms.md (run after editing the registry).

Usage: scripts/platforms_table.py > docs/platforms.md
"""
import os
import yaml

reg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'platforms.yaml')))

def req(p):
    f = p.get('free')
    if f is None:
        return '—'
    r = ', '.join(str(x) for x in f.get('requires') or []) or 'none'
    return r.replace('badge_optional', 'badge (optional)')

def row(p):
    login = ', '.join(p.get('login') or []) or '?'
    free = 'yes' if p.get('free') else ('no' if 'free' in p else '?')
    return (f"| [{p['name']}]({p['url']}) | {p.get('kind','?')} | {login} | {free} | {req(p)} | "
            f"{(p.get('free') or {}).get('wait','')} | {p.get('paid') or ''} | {p.get('votes','?')} | {p.get('family','')} | {p.get('verified') or 'unverified'} |")

verified = [p for p in reg if p.get('verified')]
unverified = [p for p in reg if not p.get('verified')]
free_n = sum(1 for p in reg if p.get('free'))
print('# Launch platforms\n')
print(f'_Generated from `data/platforms.yaml` — {len(reg)} platforms, {free_n} with a free tier. Edit the YAML, not this file._\n')
print('Legend — **requires**: what the free tier asks for. `badge` = their badge on your homepage, `upvotes:N` / `comments:N` = '
      'you must support other launches first (human task), `review` = manual approval, `dr_min:N` = minimum Domain Rating. '
      '**votes**: `now` = listing page takes upvotes today, `at_launch` = from the launch date, `none` = directory only.\n')
hdr = '| Platform | Kind | Login | Free | Free tier requires | Free wait | Cheapest paid | Votes | Family | Verified |\n|---|---|---|---|---|---|---|---|---|---|'
print('## Checked\n')
print(hdr)
for p in sorted(verified, key=lambda p: (p.get('free') is None, p['name'].lower())):
    print(row(p))
print('\n## Not yet verified\n')
print(hdr)
for p in sorted(unverified, key=lambda p: p['name'].lower()):
    print(row(p))
