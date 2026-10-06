# Playbook: launching with an agent

What one founder + one browser agent did across ~70 platforms in two days, turned into a repeatable process. The rule of thumb: **the agent does everything except the few steps that act as the founder in a way only the founder may**, and it batches those so the founder spends minutes, not hours.

## Who does what

| Agent | Founder (never automated) |
|---|---|
| Find and qualify platforms, check login methods | Google / OAuth account choice and consent (it creates an account) |
| Draft every copy length from the site and founder notes | CAPTCHAs and "math problem" checks |
| Fill forms, use each platform's AI autofill, then correct it | Upvotes / comments / reviews some free tiers require on *other* products |
| Choose the free tier and the earliest free date | Emails to platforms that list by email |
| Collect badge snippets, update the site, deploy, verify | Any payment |
| Keep the ledger, check listings, build the upvote kit | Rallying supporters on launch days |

## Phases

### 0. Intake (once, before anything)
Fill `templates/product.yaml` + `templates/founder-notes.md` + `assets/`. The agent derives what it can from the site and repo and asks the founder the rest in **one** message (see [intake.md](intake.md)). `scripts/check_intake.py` must pass. Every missing answer found mid-batch costs a round trip per platform.

### 1. Pick platforms
- Start from [platforms.md](platforms.md) (free tier, requirements, votes, family).
- Add competitors' platforms: `python3 scripts/discover_featured_on.py <competitor page>` pulls every badge link from a "Featured on" strip.
- For new domains, `python3 scripts/check_google_login.py domains.txt` checks for Google sign-in (then hand-check negatives — many login forms are modals).
- Pre-skip what can't work yet: Domain Rating minimums (`check_intake.py` lists them), platforms that need a feature you don't have.
- Order: **no-account forms first** (zero founder time), then Google-login batches grouped by **family** (same software = same flow).

### 2. Login batches (founder: ~3–5 minutes per batch)
- Browser tab budget is small; batch 5–7 platforms.
- `scripts/agent/prep_google_logins.mjs` opens each login page, clicks "Continue with Google", and stops at Google's account chooser. Then hand the browser over with one message: tab → platform, plus any upvote/CAPTCHA chores waiting.
- On "continue": read each tab's URL as the status (`/dashboard`, `/onboarding` = in; `state_mismatch`, back on `/sign-in` = retry next batch or use email login).

### 3. Submit (agent alone)
Per platform: finish onboarding (headline, bio, X handle) → submit form → **AI autofill with the URL** → fix what autofill invented (cadence, plan limits, fake features — the `autofill_traps` list in product.yaml) → categories / pricing / platforms / images → **untick pre-selected paid options** → Free → earliest free date → copy the badge snippet into the ledger → final submit after the badge is live.

Recognise families to go faster — [platform-families.md](platform-families.md) (Mkdirs, Open-Launch, get-started, fetch-form, Twelve, Squeeze…). `scripts/agent/mkdirs_submit.mjs` does the Mkdirs details step in one call.

### 4. Badges (one deploy per batch)
Collect 4–6 badge snippets → `scripts/badges.py render` → one commit → deploy → `scripts/badges.py verify` → click Verify on each platform. Details and git safety: [badges.md](badges.md).

### 5. Ledger and follow-up
Update `launches/<product>/listings.yaml` after **every** platform (status, plan, date, listing URL, badge, next founder action, private manage links). Then see [upvotes.md](upvotes.md): `check_listings.py` refreshes live/vote state, `upvote_kit.py` produces the support page and a launch-day calendar.

## Efficiency rules that mattered

1. **One message per founder round.** Every login, CAPTCHA, upvote chore and question for the batch goes into a single handoff list with tab names.
2. **Never ask what the site already answers.** Prices, FAQ, features come from the live site; the founder only confirms.
3. **Same family back-to-back.** The second Mkdirs or get-started site takes a third of the time of the first.
4. **Badges in batches.** Deploying per platform is the slowest possible order.
5. **Prefer the platform's AI autofill, then edit.** It fills images, tags, categories in seconds; it also invents facts, so always diff it against the kit.
6. **Record as you go.** The ledger is the resume point after context loss, a new session, or a teammate taking over.
7. **Daily-quota platforms early in the UTC day** (some accept only 5 free submissions per day site-wide).
8. **Free tiers move.** Queues of weeks to a year are normal; a "random date" can land 12 months out. Pick dates explicitly.

## Things that went wrong (so you don't)

- Autofill claimed "runs every morning" / "10 per day" for a product whose free plan refreshes twice a week. Keep `autofill_traps` current.
- A "random date" option assigned a launch a year away, with no free way to change it.
- Two older listings silently went 404 while their badges still linked to them — `check_listings.py` catches this.
- A deploy ran after a rejected push; it happened to be harmless, but never deploy unless `HEAD == origin/<branch>`.
- Pre-checked paid add-ons, newsletter opt-ins and "also list on our sister site" boxes on several forms.
- Login frameworks fail sometimes (`state_mismatch`, `unable_to_create_user`): retry once, then switch to email login.

More traps and fixes for browser automation: [agent-gotchas.md](agent-gotchas.md).
