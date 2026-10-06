---
name: launch-in-all-platforms
description: Launch a product on dozens of free launch platforms and startup directories (Product Hunt alternatives, SaaS/AI tool directories, "Featured on" badge sites) with a browser agent, with the founder only doing OAuth, CAPTCHAs and required upvotes. Covers intake of founder materials, platform selection from a maintained registry, batched logins, AI-autofill-assisted submission, backlink badges built/deployed/verified in batches, a per-product ledger of every listing, and post-launch upvote tracking with a launch-day calendar. Use when the user says "launch my product everywhere", "submit to launch platforms / directories", "发 launch 帖子", "提交到各个 launch 平台", "get Featured on badges / backlinks", or asks to collect and maintain launch links and upvotes.
---

# Launch in all platforms

Repository: https://github.com/MishaBear94/launch-in-all-platforms — clone it (or use the checkout this skill lives in). All paths below are relative to the repo root. Read `docs/playbook.md` once; it is the process. This file is the checklist.

## Hard rules

- **Free tier only** unless the founder says otherwise. Untick pre-selected paid options. If free needs something impossible (Domain Rating minimum, a feature the product lacks), mark `skipped` with the reason.
- **Never act as the founder where only the founder may:** OAuth consent, CAPTCHAs, upvoting/commenting/reviewing other products, sending email, paying. Prepare the tab, batch these, hand off in one message.
- **No invented facts.** Copy comes from the site, `product.yaml` and `founder-notes.md`. Check every AI autofill against `copy.autofill_traps` and the live pricing page.
- Decline non-essential cookies. Don't route around blocked actions.
- Site edits: work in a separate worktree, rebase before push, deploy only when `HEAD == origin/<branch>`, coordinate with other sessions editing the same file (`docs/badges.md`).

## Steps

1. **Intake.** Create `launches/<product>/` from `templates/` (`product.yaml`, `founder-notes.md`, `listings.yaml`, `assets/`). Fill [agent] fields from the site/repo; ask the founder all [founder] fields in **one** message with defaults (`docs/intake.md`). Run `python3 scripts/check_intake.py launches/<product>/product.yaml` until **GATE PASSED**.
2. **Choose platforms.** From `data/platforms.yaml` (`docs/platforms.md`): free tier, requirements, family, login. Add competitors' with `scripts/discover_featured_on.py`; check unknown logins with `scripts/check_google_login.py`. Pre-mark DR-gated ones `skipped`. Order: no-account forms → Google-login batches grouped by `family`.
3. **Login batch** (5–7 platforms): `scripts/agent/prep_google_logins.mjs` (Ego Lite; adapt for other browser tools) stops at Google's account chooser → hand off with a tab→platform list plus pending founder chores → on "continue", read tab URLs as login status.
4. **Submit** each platform: onboarding → AI autofill → correct → categories/pricing/platforms/images → Free → earliest free date (never "random date") → copy badge snippet into the ledger → final submit (after badge is live when the form verifies it). Families and quirks: `docs/platform-families.md`, `docs/agent-gotchas.md`; Mkdirs sites: `scripts/agent/mkdirs_submit.mjs`.
5. **Badges per batch:** `scripts/badges.py render … --format jsx|html` → one commit → deploy → `scripts/badges.py verify …` → click Verify on each platform.
6. **Ledger after every platform:** status, plan, launch_date, listing_url, upvote, badge, next_action (with URL), manage_url. This is the resume point.
7. **After launch:** `scripts/check_listings.py … --discover --write` (live? votes?) and `scripts/upvote_kit.py …` (vote-now links, launch-day `.ics`, share messages). Suggest a weekly scheduled run (`docs/upvotes.md`).
8. **Report:** counts by status vs the platform list, founder chores with links, skipped with reasons, what's next. If a platform's flow or rules differ from `data/platforms.yaml`, update the entry and its `verified` date (and regenerate `docs/platforms.md` with `scripts/platforms_table.py`).

## Templates

`templates/product.yaml` (structured intake) · `templates/founder-notes.md` (unstructured) · `templates/listings.yaml` (ledger) · `templates/replies.md` (comment, reply and vote-ask templates) · `templates/progress-table.md` (human-readable status table).
