#!/usr/bin/env python3
"""Turn a launch ledger into things supporters can act on.

Usage: scripts/upvote_kit.py launches/<p>/listings.yaml [--out launches/<p>/out]

Writes:
  upvote-links.md   grouped: vote now / opens on launch day (with dates) / listed (no votes) / pending
  launches.ics      one all-day calendar event per launch date, with the listing link —
                    import it so nobody misses a launch day (votes usually count only that week)
  share.txt         a short message per "vote now" link to paste into X / Slack / email
"""
import datetime, os, sys
import yaml

def main(path, out):
    d = yaml.safe_load(open(path))
    os.makedirs(out, exist_ok=True)
    name = d.get('product_name') or d.get('product')
    today = datetime.date.today()
    L = [l for l in d['listings'] if l.get('status') not in ('skipped', 'removed')]
    def date(l):
        v = l.get('launch_date')
        return v if isinstance(v, datetime.date) else (datetime.date.fromisoformat(v) if v else None)
    def is_live(l):  # checked result wins; otherwise trust the recorded status
        return l['live'] if l.get('live') is not None else l.get('status') in ('live', 'submitted', 'scheduled')
    has_page = lambda l: bool(l.get('listing_url')) and is_live(l)
    now = [l for l in L if l.get('upvote') is True and has_page(l) and (not date(l) or date(l) <= today)]
    later = sorted([l for l in L if l.get('upvote') and date(l) and date(l) > today], key=date)
    waiting = [l for l in L if l.get('upvote') == 'at_launch' and not (date(l) and date(l) > today) and has_page(l)]
    listed = [l for l in L if not l.get('upvote') and has_page(l)]
    pending = [l for l in L if l not in now + later + listed + waiting]

    md = [f'# {name}: where to support it\n', f'_Updated {today}_\n']
    md.append('## Vote now\n')
    md += [f"- **{l['platform']}** — {l['listing_url']}" + (f" ({l['votes']} votes)" if l.get('votes') is not None else '') for l in now]
    md.append('\n## Opens on launch day\n')
    md += [f"- {date(l)} · **{l['platform']}** — {l.get('listing_url') or '(link when live)'}" for l in later]
    md.append('\n## Page live, voting not open yet (date unknown)\n')
    md += [f"- **{l['platform']}** — {l['listing_url']}" for l in waiting]
    md.append('\n## Listed (no voting)\n')
    md += [f"- {l['platform']} — {l['listing_url']}" for l in listed]
    md.append('\n## Pending review\n')
    md += [f"- {l['platform']}" + (f" — next: {l['next_action']}" if l.get('next_action') else '') for l in pending]
    open(os.path.join(out, 'upvote-links.md'), 'w').write('\n'.join(md) + '\n')

    ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//launch-in-all-platforms//EN']
    for l in later:
        dt = date(l).strftime('%Y%m%d')
        nxt = (date(l) + datetime.timedelta(days=1)).strftime('%Y%m%d')
        ics += ['BEGIN:VEVENT', f"UID:{d.get('product')}-{l['platform']}-{dt}@launch-in-all-platforms",
                f'DTSTAMP:{today.strftime("%Y%m%d")}T000000Z', f'DTSTART;VALUE=DATE:{dt}', f'DTEND;VALUE=DATE:{nxt}',
                f"SUMMARY:{name} launches on {l['platform']} — ask for upvotes",
                f"DESCRIPTION:{l.get('listing_url') or ''}", 'END:VEVENT']
    ics.append('END:VCALENDAR')
    open(os.path.join(out, 'launches.ics'), 'w').write('\r\n'.join(ics) + '\r\n')

    share = [f"{name} is live on {l['platform']} today. If it looks useful, an upvote helps a lot: {l['listing_url']}" for l in now]
    open(os.path.join(out, 'share.txt'), 'w').write('\n\n'.join(share) + '\n')
    print(f'vote now: {len(now)} · launch-day: {len(later)} · listed: {len(listed)} · pending: {len(pending)} → {out}/')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    main(a[0], a[a.index('--out') + 1] if '--out' in a else os.path.join(os.path.dirname(a[0]), 'out'))
