# Browser-automation traps (and the fix that worked)

## Selecting and clicking

- `[name=description]` often matches `<meta name="description">` first → use `textarea[name=description]` / `input[name=…]`.
- `button:text-is("X")` frequently fails (nested spans, icons, duplicate hidden mobile copies). Fallback: `page.evaluate(() => [...document.querySelectorAll('button')].find(b => b.innerText.trim()==='X' && b.offsetParent).click())`, or tag it with a `data-*` attribute then `page.click('[data-go="1"]')`.
- "matched N elements" → filter by `offsetParent` (visible) and pick the right one; or use snapshot refs (`@12`).
- "element has zero-sized bounding box" on a pricing option → it is a `<select>` option; use `selectOption`.
- "`<html>`/`<div>`/`<section>` intercepts pointer events" → a modal, cookie banner, or ad overlay is open. Screenshot, close/refuse it, or `el.click()` via evaluate.
- Google ad vignettes (`#google_vignette`, `iframe[id^=aswift]`, `ins.adsbygoogle`): remove them in-page before clicking.
- Never click at coordinates you computed from an element that returned (0,0) — it lands on the backdrop and closes the dialog.
- Rich editors (contenteditable): click it, `ControlOrMeta+a`, `keyboard.paste(text)`. Check for a hidden plain `textarea` first — filling that is easier.
- Async autofill: wait with `waitForFunction(() => input.value.length > 0, …, {timeout: 120000})`; some show a confirm dialog ("Analyze") before starting.

## Pages and tabs

- Ego Lite page budget (8). Close finished tabs at the start of each batch; Google popups also count as pages.
- Clicking some links opens new tabs (e.g. a "Launch MCP" link label) — close strays.
- When the human takes control, every command fails with a hard stop. Stop, report, wait for "continue", then `takeOverTaskSpace(id)`.
- Each `ego-browser nodejs` call is a new process; keep state in files (`kit.json`, `badges.md`) and in page labels.
- Heredoc + env vars don't mix with `ego-browser nodejs < file`; inject constants by prepending a `const X = …;` line.

## Forms

- Submit buttons that do nothing: look for a hidden requirement (badge verification banner, "Choose at least one job", tech stack, terms checkbox). Screenshot the bottom of the form.
- Default selections to undo: Premium pre-selected (ScrollLaunch), "also list on X" ticked (Launch Llama), wrong socials from autofill (`@productname`, `github.com/unknown`).
- Autofill quality: generally good for name/tagline/categories; sometimes thin or invents features, prices, plans, frequencies. Compare with the live site.
- Logo too small from favicon → upload the 512 px PNG; crop modals need "Use this logo".
- "Draft saved" pages: the dashboard holds a `?draft=` link to resume; reopening `/submit` may start a blank form.

## Logins

- Google `state_mismatch` / landing back on `/sign-in`: retry in the next batch; if it repeats, suggest email login or a normal browser.
- Some login pages show reCAPTCHA before the Google button (human).
- Onboarding gates (profile headline, bio, preferences, "upvote a few launches" with a Skip) appear right after first login — complete or skip before `/submit`.

## Tooling permissions

- Upvotes, comments and reviews on other people's products may be blocked by the agent's permission policy — don't retry through another path; list them for the human with the tab and count.
- A transient "classifier error" on an edit can be retried once.
