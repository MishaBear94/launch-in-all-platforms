# Pre-launch intake (fill before the first submission)

Distilled from every field seen while submitting one product to ~60 launch platforms and directories.
Goal: answer once, then every form is copy-paste. Two kinds of answers:

- **[Agent]**: derive from the product's own public site / repo (landing page, pricing, FAQ, `package.json`), then show the human for a quick confirm.
- **[Human]**: facts the agent must NOT guess. Ask in one message, batch all questions, offer a sensible default for each.

Priority:
- **P0**: blocks submission; most forms require it. Do not start Phase 3 without these.
- **P1**: asked by many forms or makes listings much better; prepare before batch 1.
- **P2**: a few platforms; prepare if time allows, otherwise fill when met.

Output: fill **`templates/product.yaml`** (structured, machine-checked) and **`templates/founder-notes.md`** (unstructured story), plus an `assets/` folder. Run `python3 scripts/check_intake.py launches/<product>/product.yaml` — it enforces the gate below.

---

## A. Identity & access (P0)

| # | Question | Who | Default / note |
|---|---|---|---|
| A1 | Login identity for all platforms (Google account email) | Human | One account for everything; record it |
| A2 | Maker display name, username | Human | |
| A3 | Maker headline (one line, e.g. "Founder of X") | Agent→confirm | Required by many onboarding screens |
| A4 | Maker short bio (≤500) | Agent→confirm | |
| A5 | Maker X/Twitter handle **and** full URL | Human | Some fields want `handle`, others `https://x.com/handle` |
| A6 | Product's own social accounts (X, LinkedIn, GitHub, Discord…) | Human | Only list accounts that exist |
| A7 | Contact / notification email | Human | Usually same as A1 |
| A8 | Other makers / co-founders to credit | Human | Optional |
| A9 | "How did you hear about us" answer | Agent | "Other – a list of launch directories" (honest default) |
| A10 | Country / location | Human | Optional; skip if unsure |
| A11 | Phone number | Human | Optional; default: don't provide |

## B. Product facts (P0 unless marked)

| # | Question | Who | Default / note |
|---|---|---|---|
| B1 | Product name (≤25 safest; some cap at 12–24) | Agent | |
| B2 | Slug (lowercase-hyphen), used for listing URLs | Agent | `product-name` |
| B3 | Canonical URL (no tracking params) | Agent | Many platforms lock it after submit |
| B4 | Product type | Agent | Software / SaaS / Digital product |
| B5 | Platforms actually shipped (Web, iOS, Android, API, CLI, Desktop, Extension) | **Human** | Only claim what is publicly available |
| B6 | Pricing model + every plan: name, price, period, 2–5 features | Agent from pricing page → confirm | Mismatched prices get listings rejected |
| B7 | Cheapest paid price; free-trial days (0 if none) | Agent | |
| B8 | Is billing live? Stage: Idea / Pre-revenue / Revenue / Profitable | **Human** (P1) | Don't inflate; mislabelled stages get corrected |
| B9 | Intent flags: open to acquisition / raising / neither | **Human** (P1) | Default "neither" |
| B10 | Founded year | **Human** (P2) | |
| B11 | Open source? Vibe coded? Selling the product? NSFW / crypto / gambling? | **Human** | Yes/No set |
| B12 | Tech stack (≤5–8 items, real ones) | Agent from repo (P1) | Some forms make it required |
| B13 | Data export available? | **Human** (P2) | |
| B14 | Self-reported traction / MRR | **Human** (P2) | Default: leave blank |
| B15 | Launch-only promo / deal code | **Human** (P2) | Optional |
| B16 | Domain Rating of the site (check verifieddr / ahrefs) | Agent (P1) | Free tiers often need DR ≥ 10 / 20; decides skips upfront |

## C. Copy (P0 unless marked) — write once, at several lengths

| # | Item | Lengths to prepare | Note |
|---|---|---|---|
| C1 | Tagline | **≤40, ≤60, ≤80** (also fits 90/92/100/130) | No hype words; say what it does |
| C2 | One-liner / SEO meta | **≤150 and 120–170** | Card + search description |
| C3 | Short description | **≈250–300** | |
| C4 | Long description | **≤600, ≈800–1000, ≈1100** (min often 300–500) | Plain paragraphs + numbered "how it works"; no claims the site doesn't make |
| C5 | Who it's for (one line, ≥10 chars) | | |
| C6 | Problem / Solution / What makes it unique (P1) | one short paragraph each | |
| C7 | Key features | 6 × one line | |
| C8 | Use cases (P1) | 5–8 short phrases | |
| C9 | FAQ (P1) | 4–6 Q&A, reuse the site's FAQ | |
| C10 | Real alternatives / competitors (P1) | 3–5 named products | **Human confirms**; never invent |
| C11 | Categories (ranked) & tags | top 4 categories, 5 tags | Pick closest per platform |
| C12 | SEO keywords (P2) | ≤10 | |
| C13 | Target audience / professions | 4–6 roles | Some forms require a checklist |
| C14 | Maker first comment | **≤200, ≤500, ≤1000** | Why I built it · what it does · free tier · ask for feedback |
| C15 | Thank-you note after upvote (P2) | ≤280 | |
| C16 | Facts that AI autofill tends to get wrong | list | e.g. cadence ("every morning"), plan limits; check autofill against this list |

## D. Media (P0 unless marked)

| # | Asset | Spec to prepare | Note |
|---|---|---|---|
| D1 | Square logo | **512×512 PNG, <200 KB** (also keep SVG) | Many reject <240/400 px or >500 KB–1 MB |
| D2 | Cover / social card | **1200×630 PNG/JPG <1 MB** | Fits 16:9 / 1.91:1 fields |
| D3 | Product screenshots (P1) | **3 different screens, 1600 px wide JPG <500 KB** | Real UI; blur personal data |
| D4 | Wide banner (P2) | 2400×400 (6:1) | A few platforms |
| D5 | Demo video (P1) | 30–90 s YouTube/Loom URL | Several platforms say it lifts conversion |
| D6 | Public URLs of D1–D2 | | Some forms take URLs only |
| D7 | Maker avatar (P2) | 512×512 | Otherwise Google photo is used |

## E. Launch rules & site access (P0)

| # | Question | Who | Default |
|---|---|---|---|
| E1 | Free tier only? Skip platforms without one? | Human | Yes |
| E2 | Date preference | Human | Earliest free date; avoid "random date" options |
| E3 | May the agent edit and deploy the site to add badges? Which repo / branch / worktree / deploy command? | Human | Required for most free tiers |
| E4 | Where badges go (homepage block / footer), light or dark | Human | Homepage "Featured on" row, light |
| E5 | Newsletter / marketing opt-ins | Human | Only when the free tier requires it |
| E6 | Browser to use (must hold the logged-in sessions) | Human | |
| E7 | Progress file path | Agent | `artifacts/<product>-launch-progress.md` |
| E8 | Human availability for batched chores (OAuth, CAPTCHA, 3–5 upvotes per platform, comments, emails) | Human | Agent batches them per round |

---

## Gate before Phase 3

- [ ] All P0 rows answered; [Human] rows confirmed by the human, not inferred
- [ ] `kit.json` has every C-item at every length listed
- [ ] D1, D2 exist on disk and at public URLs; at least one real screenshot
- [ ] Prices/plans in the kit match the live pricing page today
- [ ] Domain Rating checked, and DR-gated platforms pre-marked ⏭️
- [ ] Site edit/deploy path confirmed (E3) and tested once
