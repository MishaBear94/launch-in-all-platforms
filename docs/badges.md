# Badges, git and deploy

**Tooling.** Every badge snippet goes into the ledger (`listings.yaml` → `badge.html`, `badge.rules`, `badge.required`). Then:

```bash
python3 scripts/badges.py render launches/<p>/listings.yaml --format jsx > featured-on.tsx   # or --format html
# commit + deploy once per batch
python3 scripts/badges.py verify launches/<p>/listings.yaml                                   # every required link present, rel rules respected
```

One generated component, one commit, one deploy per batch of 4–6 platforms, then click every platform's Verify. `verify` reads the server-rendered HTML exactly like the platforms' crawlers do, so a pass there predicts a pass on the platform.


## Badge rules

- Most free tiers are a **link exchange**: the badge must be on the homepage or a footer visible on it, server-rendered (crawlers don't run JS), and stay there — many re-check weekly and unpublish if it disappears.
- Paste the snippet as given: same `href`, `src`, query params (`?ref=badge`, `utm_*`, tokens). Only adapt syntax (JSX `style={{}}`, `className`).
- Platform-specific constraints seen:
  - no `rel` attribute at all (CloutStack)
  - `rel="noopener"` only, no nofollow/sponsored/ugc, keep `?ref=badge` (ScrollLaunch)
  - href must be the exact listing URL (Good AI Tools family, Mkdirs `/item/<slug>`)
  - text link to the domain is enough (Aura++, Submit AI Tools)
- Optional badges still pay off: they turn nofollow listings into dofollow (Better Launch, neeed, Launch Llama, StartupBase priority queue).
- Keep one "Featured on" component; a horizontally scrolling single row scales to 30+ badges. Normalize heights (~54–56 px).
- Collect badges first, deploy **in batches** (4–6 per deploy), then run every Verify — not one deploy per platform.

## Verification loop

1. Commit badges → push → deploy (web only if possible).
2. `curl -s https://<site>/ | grep -oE '<badge host or path>' | sort | uniq -c` for each new badge; for rel-sensitive ones grep the full `<a …>` tag.
3. Click Verify on each platform; read the result text ("Badge found", "Verified", "Submit now" enabled).
4. Some verifiers say "not eligible" for reasons other than the badge (Domain Rating 0) — note it, use the non-dofollow free path if one exists.

## Git and deploy safety

- Find the branch that actually deploys the site (compare the live HTML with `git log`/files; it may be a different worktree or a remote branch ahead of local).
- Other sessions may edit the same component. Before the first edit: `ListAgents`, message them, and agree who appends what.
- Work in a **separate worktree** created from the remote branch (`git worktree add /tmp/<x> -b <tmp> origin/<branch>`), copy/link git-ignored deploy config (`.env.local`, CLI project link) from the main worktree.
- Every badge batch: `git fetch && git rebase origin/<branch>` → edit → commit → `git rebase` again → `git push origin HEAD:<branch>` → deploy.
- **Never deploy if the push failed**: a deploy from a HEAD that is behind the remote can roll back someone else's live change. If it happened, fetch and compare immediately (`git log HEAD..origin/<branch>`), re-push, redeploy.
- Record the commit that added each batch of badges in the progress file.
