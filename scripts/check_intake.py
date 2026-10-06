#!/usr/bin/env python3
"""Gate check for a founder intake (product.yaml) before any launch submission.

Usage: scripts/check_intake.py launches/<product>/product.yaml

Fails (exit 1) on missing P0 fields, copy over its length limit, missing image files,
or images outside the specs most forms accept. Prints P1 gaps as warnings and the
platforms the product cannot use yet because of a Domain Rating minimum.
"""
import os, re, sys
import yaml

LIMITS = {  # copy key -> (min, max) characters
    'tagline_40': (10, 40), 'tagline_60': (10, 60), 'tagline_80': (10, 80),
    'one_liner_150': (40, 150), 'meta_120_170': (120, 170), 'short_300': (120, 300),
    'long_600': (300, 600), 'long_1000': (500, 1000), 'long_1100': (500, 1200),
    'who_for': (10, 120), 'maker_comment_200': (40, 200), 'maker_comment_500': (100, 500),
    'maker_comment_1000': (200, 1000), 'thank_you_280': (10, 280),
}
P0_COPY = ['tagline_40', 'tagline_60', 'tagline_80', 'one_liner_150', 'short_300', 'long_600',
           'long_1000', 'who_for', 'maker_comment_200', 'maker_comment_500']
P1_COPY = ['meta_120_170', 'long_1100', 'problem', 'solution', 'unique', 'maker_comment_1000']
P1_LISTS = {'use_cases': 5, 'faq': 4, 'alternatives': 3, 'tags': 5}


def main(path):
    d = yaml.safe_load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    errors, warns = [], []
    get = lambda sect, key: (d.get(sect) or {}).get(key)

    for sect, keys in {'identity': ['login_email', 'maker_name', 'headline', 'x_handle'],
                       'product': ['name', 'slug', 'url', 'platforms'],
                       'pricing': ['model', 'plans'],
                       'launch_rules': ['free_only', 'site']}.items():
        for k in keys:
            if get(sect, k) in (None, '', []):
                errors.append(f'{sect}.{k} is missing (P0)')

    url = get('product', 'url') or ''
    if re.search(r'[?&](utm_|ref=)', url):
        errors.append('product.url has tracking params; use the canonical URL')
    if len(get('product', 'name') or '') > 25:
        warns.append('product.name > 25 chars: some forms cap at 12–24')

    copy = d.get('copy') or {}
    for k, (lo, hi) in LIMITS.items():
        v = (copy.get(k) or '').strip()
        if not v:
            (errors if k in P0_COPY else warns).append(f'copy.{k} is empty ({"P0" if k in P0_COPY else "P1"})')
        elif not lo <= len(v) <= hi:
            errors.append(f'copy.{k} is {len(v)} chars, needs {lo}–{hi}')
    for k in P1_COPY:
        if k not in LIMITS and not (copy.get(k) or '').strip():
            warns.append(f'copy.{k} is empty (P1)')
    feats = [f for f in copy.get('features') or [] if f]
    if len(feats) < 6:
        errors.append(f'copy.features has {len(feats)}, needs 6 (P0)')
    for k, n in P1_LISTS.items():
        if len(copy.get(k) or []) < n:
            warns.append(f'copy.{k} has {len(copy.get(k) or [])}, aim for ≥{n} (P1)')

    media = d.get('media') or {}
    def img(rel, label, spec=None, max_kb=None, required=True):
        if not rel:
            (errors if required else warns).append(f'media.{label} is missing')
            return
        p = os.path.join(base, rel)
        if not os.path.exists(p):
            errors.append(f'media.{label}: {rel} not found')
            return
        kb = os.path.getsize(p) / 1024
        if max_kb and kb > max_kb:
            warns.append(f'media.{label} is {kb:.0f} KB (> {max_kb} KB; some forms reject it)')
        if spec:
            try:
                from PIL import Image
                w, h = Image.open(p).size
                if (w, h) != spec:
                    warns.append(f'media.{label} is {w}×{h}, expected {spec[0]}×{spec[1]}')
            except ImportError:
                pass
    img(media.get('logo_512'), 'logo_512', (512, 512), 200)
    img(media.get('cover_1200x630'), 'cover_1200x630', (1200, 630), 1000)
    shots = media.get('screenshots') or []
    if not shots:
        errors.append('media.screenshots: at least one real screenshot (P0)')
    for i, s in enumerate(shots):
        img(s, f'screenshots[{i}]', None, 500)
    if len(shots) < 3:
        warns.append('media.screenshots: 3 different screens recommended (P1)')
    if not media.get('demo_video'):
        warns.append('media.demo_video is empty (P1: several platforms say it lifts conversion)')

    dr = get('product', 'domain_rating')
    if dr is None:
        warns.append('product.domain_rating unknown: check it before starting')
    else:
        reg = os.path.join(os.path.dirname(__file__), '..', 'data', 'platforms.yaml')
        if os.path.exists(reg):
            blocked = []
            for p in yaml.safe_load(open(reg)):
                for r in (p.get('free') or {}).get('requires') or []:
                    m = re.match(r'dr_min:(\d+)', str(r))
                    if m and dr < int(m.group(1)):
                        blocked.append(f"{p['name']} (DR ≥ {m.group(1)})")
            if blocked:
                print('Skip for now (Domain Rating too low):', ', '.join(blocked))

    for w in warns:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    print(f'\n{len(errors)} errors, {len(warns)} warnings —', 'GATE PASSED' if not errors else 'fix errors before submitting')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
