# launch-in-all-platforms

Launch your product on dozens of launch platforms and startup directories with an AI agent doing almost all the work — and keep track of every listing and upvote afterwards.

Built from a real run: one SaaS product submitted to ~70 platforms in two days, with the founder spending minutes per batch on the few steps an agent must never do for them (Google sign-in consent, CAPTCHAs, upvoting other launches). Everything that run learned is here as data, templates, scripts and an agent skill.

[中文说明](README.zh-CN.md)

## What's inside

| You want to… | Use |
|---|---|
| Know **where** to launch: free vs paid, what the free tier requires (badge, upvotes, DR), wait times, whether listings take votes | [`data/platforms.yaml`](data/platforms.yaml) → [`docs/platforms.md`](docs/platforms.md) (89 platforms, 57 with a free tier) |
| Understand how platforms **relate** (two tiers, the backlink mesh, hubs, clusters) | [`docs/ecosystem.md`](docs/ecosystem.md), [`data/link-graph.json`](data/link-graph.json) |
| Know **what to prepare** before launching (structured + unstructured) | [`templates/product.yaml`](templates/product.yaml), [`templates/founder-notes.md`](templates/founder-notes.md), [`docs/intake.md`](docs/intake.md), every form field seen with its limits: [`docs/form-fields.md`](docs/form-fields.md); gate: `scripts/check_intake.py` |
| Let an **agent** do the launch efficiently | [`docs/playbook.md`](docs/playbook.md), [`skills/launch-in-all-platforms/SKILL.md`](skills/launch-in-all-platforms/SKILL.md), [`docs/platform-families.md`](docs/platform-families.md), [`docs/agent-gotchas.md`](docs/agent-gotchas.md), `scripts/agent/` |
| Add **badges** to your site without a deploy per platform | [`docs/badges.md`](docs/badges.md), `scripts/badges.py render / verify` |
| **Reply** well (and meet "leave 3 helpful comments" requirements) | [`templates/replies.md`](templates/replies.md) — 24 templates |
| **Collect every listing link** and **keep upvotes coming** | [`docs/upvotes.md`](docs/upvotes.md), ledger [`templates/listings.yaml`](templates/listings.yaml), `scripts/check_listings.py`, `scripts/upvote_kit.py` (vote-now page + launch-day calendar) |

A complete worked example lives in [`examples/dailyhook/`](examples/dailyhook/): intake, assets, and a ledger of 57 platforms.

## How it works

```
 intake ──► pick platforms ──► login batches ──► submit ──► badges ──► ledger ──► upvotes
 (founder    (registry +        (agent stops at   (agent:     (render →   (every     (check pages,
  answers     discovery)         Google consent;   autofill,   1 deploy →  listing,   calendar,
  once)                          founder clicks)   fix, free)  verify)     date, URL) share kit)
```

The founder's part: answer the intake once, then per batch of 5–7 platforms pick their Google account, solve the occasional CAPTCHA, and upvote/comment on a few other launches where a free tier demands it. Everything else is the agent.

## Quick start

```bash
git clone https://github.com/MishaBear94/launch-in-all-platforms && cd launch-in-all-platforms
pip install -r requirements.txt && playwright install chromium

mkdir -p launches/acme/assets && cp templates/{product.yaml,founder-notes.md,listings.yaml} launches/acme/
# fill product.yaml + founder-notes.md, drop logo/cover/screenshots into assets/
python3 scripts/check_intake.py launches/acme/product.yaml          # must say GATE PASSED

# then let your agent run the skill (Claude Code):
#   copy skills/launch-in-all-platforms into ~/.claude/skills/  and say "launch acme on all free platforms"

# after submissions:
python3 scripts/badges.py render  launches/acme/listings.yaml --format jsx > featured-on.tsx
python3 scripts/badges.py verify  launches/acme/listings.yaml
python3 scripts/check_listings.py launches/acme/listings.yaml --discover --write
python3 scripts/upvote_kit.py     launches/acme/listings.yaml        # → launches/acme/out/
```

## Principles

- **Free tiers first, honestly.** No invented features, prices or cadence; AI autofill is corrected against your own copy.
- **The founder stays the founder.** Account consent, CAPTCHAs, votes and comments on other products, emails and payments are never automated.
- **No vote manipulation.** Ask real people, on launch day, with direct links.
- **Data over memory.** Platforms change weekly — `data/platforms.yaml` records what was seen and when. PRs that update entries are the most valuable contribution.

## Contributing

Found a platform that changed, or a new one? Edit `data/platforms.yaml` (set `verified` to today), run `python3 scripts/platforms_table.py > docs/platforms.md`, open a PR.

## License

MIT
