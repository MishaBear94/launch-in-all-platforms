# After launch: collect every link, keep the upvotes coming

Submitting is half the work. Most launch platforms rank by votes **during a launch window** (a day or a week), and many free listings go live weeks or months later, on different dates. Without one place that knows every link and every date, launch days pass unnoticed.

## 1. One ledger per product

`launches/<product>/listings.yaml` (template: [templates/listings.yaml](../templates/listings.yaml)). The agent writes an entry right after each platform: status, plan, launch date, listing URL, whether the page takes votes, badge, next founder action, and any private "manage" links some platforms show only once.

## 2. Fill in and check links in bulk

```bash
python3 scripts/check_listings.py launches/<p>/listings.yaml --discover --write
```

- `--discover` fills missing `listing_url` from each platform's URL pattern (`data/platforms.yaml` → `listing`) and from its `sitemap.xml`.
- Each page is opened logged out, like a visitor: is it live (product name shown, no 404), does it take votes, what's the count.
- Re-run weekly (or schedule it). It catches listings that go live, get approved, or silently disappear — e.g. a page that 404s while your site still shows its badge.

## 3. Turn the ledger into something supporters can use

```bash
python3 scripts/upvote_kit.py launches/<p>/listings.yaml
```

Writes to `launches/<p>/out/`:
- `upvote-links.md`: **vote now** · **opens on launch day** (with dates) · listed (no voting) · pending.
- `launches.ics`: one calendar event per launch date with the link — import it, share it with your team.
- `share.txt`: one ready message per vote-now link for X, Slack or email.

## 4. Keeping votes honest and effective

- Ask **real users and friends** to vote on launch day, with the direct link; most platforms need an account, so tell them which login works.
- Spread asks over the calendar instead of all at once — votes usually only count during that platform's launch window.
- Reply to every comment on your listing the same day (templates: [templates/replies.md](../templates/replies.md)).
- Don't buy votes, use vote-swap rings or alt accounts — platforms detect it and delist.
- After a launch window closes, update the ledger (`status: live`, final rank, any winner badge to add to the site).

## 5. Automate the routine

A weekly scheduled job (cron, GitHub Action, or an agent routine) that runs `check_listings.py --write` and `upvote_kit.py`, commits the ledger, and posts "this week's launch days + vote-now links" to your team channel is enough to keep it running without anyone remembering.
