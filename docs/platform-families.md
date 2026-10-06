# Platform families (same software = same agent flow)

Many directories run the same open-source or white-label software. Spot the family from the submit page and reuse the flow. Observed in October 2026; re-check details if a page looks different.

## Mkdirs template ("Submit 1/3 · Details → Payment → Publish")

Seen on: Turbo0, aitoolfame, toolfame, saasfame, toolrain, NewTool.site, aihuntlist (variant), many `*.com/item/<slug>` directories.

- Form: `input[name=link]` + **AI Autofill** → confirm dialog **Analyze** → fills name, categories, tags, `textarea[name=description]`, Markdown introduction. Image field (16:9, ≤1 MB); some also have a Logo field (two file inputs).
- Submit → lands on `/payment/<id>` with plan cards. Free card button: **"Verify backlink first"** / **"Verify Badge First"** / **"Choose Free Plan"** → dialog "Backlink Badge Verification" with the snippet `<a href="https://<site>/item/<slug>">…badge-light.svg</a>` and a Verify button.
- After deploy: Verify → button becomes **"Submit to review"** or **"Badge Verified - Submit Now"** → status "Pending" / "Under Review". Reviews: 1 week – 180 days.
- `scripts/mkdirs_submit.mjs` automates the details step.

## Open-Launch wizard (Project Info → Details → Launch Date → Review → Backlink)

Seen on: Aura++, Startup Fast (startupfa.st), OpenHunts-like clones.

- Some first ask "Startup profile vs Personal profile" (pick Personal).
- `websiteUrl` + **Auto-fill / AI Autofill** fills name, rich description, logo, product image.
- Details: categories (max 3), **Tech stack required** (type + Enter), platforms, pricing radio, maker name, Twitter URL.
- Launch date: a `<select>` or listbox of days with "N free slot(s)"; pick the first non-zero. Aura++ offered "Assign a random date" (books the first free slot) when the visible list was nearly all full.
- Free requires a badge; Submit stays disabled until "Verify Badge" passes. An upsell modal ("Your launch date doesn't have to be…") appears — choose "Continue with free launch".

## Fetch-form family (StartupTrusted, SaaSGrow, LaunchIgniter network)

- `Website URL` + **Fetch** fills name, tagline, description, logo URL. Category is a searchable button list. "Continue to Listing" / "Submit SaaS".
- Free → "Copy Embed Code" badges at `/api/badge?type=featured&style=light`, Verify Badge → "Submit for Review" / "Submit for Approval".
- LaunchIgniter: complete-profile step first; product submit then **math-CAPTCHA dialog** (human); then schedule page → Free Launch → Verify Badge → Book earliest week → confirm dialog "Submit for Review".

## Same-template "get-started" family

Good AI Tools, We Like Tools, Unite List, Trustiner, Acid Tools, ShinyLaunch, Startup Benchmarks (`/assets/images/badge.png`): 3 steps Website → **Badge first** (href must be the exact listing URL, e.g. `/ai/<slug>`) → Details (screenshot, icon, up to 4 categories, pricing, short ≤150, about ≤1500, terms) → Submit for Review → `/success`.

## Others worth knowing

| Platform | Notes |
|---|---|
| OpenHunts | URL auto-fill fills everything incl. images; free queue ~60 weeks, "Add our badge to skip" dialog → Verify → Submit for review. |
| ShipBoost | No autofill; tags popover; Media tab file inputs; Socials tab; "Save your product" then reopen from dashboard draft link. Free needs badge **and 3 upvotes** (human). |
| SaaSCity | "Drop your link" wizard drafts in ~45 s; guessed socials wrong — fix. Plans radio → Free → pick launch Monday → badge → "Check my site for the badge" → Submit my launch. |
| Commune | Must create a project first (costs in-site gold); autofill; launch form has free weekly cohort; badge optional. |
| StackLedge | Type → URL → AI draft → plan (free queue) → **3 upvotes** (human). |
| StartupBase | Onboarding profile + optional upvote step (skip) → URL-based draft → General/Media/Makers/Extras tabs → Free launch needs **3 upvotes + 1 comment** (human); badge optional (priority queue). |
| ScrollLaunch | "Fill with AI"; description is a rich editor but a plain `textarea` exists; **Premium is pre-selected — untick it**; week auto-picks first free slot; badge verify dialog after scheduling. |
| DanielLaunches | Autofill → badge step → Verify → date `<select>` → Submit launch. |
| neeed.directory | Prefill; free goes live immediately; badge optional (dofollow) — modal "I'll add the badge – Submit". |
| Launch Llama | Prefill with AI generates fake-ish "key features" — replace; untick "Also list on Launch MCP"; free requires **5 upvotes + rating review** (human); badge optional. |
| Better Launch | Prefill; logo crop modal "Use this logo"; free = Mondays ≥30 days out; badge optional → dofollow. |
| Smol Launch | AI Import; "Free Verified" needs DR > 0 and badge; otherwise Basic Free; needs 3 upvotes. |
| KittyLaunch | Must upvote 3 products today before the form appears. |
| CloutStack | Autofill sometimes down; manual fill; free needs badge with **no rel attribute**; checked before going live. |
| Submit AI Tools | Verify badge link first, then long form; required "Suitable for jobs" checklist and newsletter opt-in on free. |
| Fazier | Free requires 3 thoughtful comments on other products (human) + badge. |
| ListMySaaS, AI Directories | Free requires Domain Rating ≥ 10 → skip for new domains. |
| ToolPilot | Shopify customer login (Shop / email code) — no Google. |
| Dang.ai, Yo.directory | Email magic link only. |
| No-account forms | EasyLaunch, EasyDoFollow, LemonLaunch, Twelve Tools, Wired Business, Toolfio, DodoDirectory, TheSaaSDir, NovaTools — submit directly, no login batch needed. |

## "Twelve Tools" family (no account; Website → Screenshot → Review → Badge → Live)

Seen on: twelve.tools, wired.business (same maker; also Ramen Tools, 500.Tools).

- `/submit` → "Continue — it's free" → `#fUrl` + `#btnAnalyze`. Auto screenshot; replace via hidden `input#shotFileOk` (setInputFiles works on it; the button opens a native chooser).
- Review: name, headline (≤92), `longdesc` (max 600 — use the short copy), category `<select>`, email; prefill invents "every morning" cadence → replace.
- "Submit for verification" → badge step → after deploy "Verify my website/badge" → **live instantly**, page shows a private edit link (`/edit?hash=…`) — save it, it's the only way to manage the listing.

## "Squeeze" family (no account; inline modal)

Seen on: EasyLaunch, EasyDoFollow, LemonLaunch (same software, homepage "Submit launch" or a URL box + "Launch").

- Modal fields `sl-url`, `sl-name`, `sl-tagline` (auto from site), `sl-email`, `sl-x`, founder checkbox, `sl-cat`; hidden honeypot `company` must stay empty.
- Continue → plan cards → "Continue with Badge" → badge for `/<category>/<slug>` → after deploy "Verify & publish" → live with dofollow.

## No-account forms with thresholds

- TheSaaSDir: `/submit/?tier=free` single page, Auto-fill, screenshot, up to 3 categories, email → "Submit Product"; badge URL becomes product-specific after submit; reviewed within 7 days.
- DodoDirectory: Free plan shows the badge first and a `verify-url` box; after verify the Mkdirs-style details form unlocks (intro is EasyMDE/CodeMirror → set via `document.querySelector('.CodeMirror').CodeMirror.setValue()`; consent checkboxes are custom buttons — click the snapshot ref) → `/payment/<id>` → "Submit & Wait".
- NovaTools: Option B "free waitlist" (batch reviews), badge required before joining; fields name, description 50–300, url, category, backlink page, email → "Join Free Waitlist".
- Toolfio: free needs DR ≥ 20 → skip for new domains.
