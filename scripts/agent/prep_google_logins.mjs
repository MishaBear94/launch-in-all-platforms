// Prepare a batch of Google sign-ins in Ego Lite, stopping at Google's account chooser.
// The human then picks the account and consents; the agent never does that step.
//
// Usage (prepend the constants, then pipe to ego-browser):
//   { echo 'const SPACE=114; const CLOSE=["p3","p5"]; const URLS=["https://a.com/login","https://b.com/"];'; \
//     cat prep_google_logins.mjs; } | ego-browser nodejs
//
// CLOSE: labels of finished tabs to free the page budget (Ego Lite allows ~8).
// URLS: login pages, or homepages (the script clicks "Log in"/"Sign in" first if no Google button).
// Afterwards: `await task.handOff()` and tell the human which tab is which.
const task = await taskSpace(SPACE);
for (const l of CLOSE) { try { await task.page(l).close(); } catch (e) { console.log('close', l, String(e).slice(0, 80)); } }

const mark = (page, re, attr, maxLen) => page.evaluate(({ src, attr, maxLen }) => {
  const re = new RegExp(src, 'i');
  const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const el = [...document.querySelectorAll('button,a,[role=button]')]
    .find((e) => vis(e) && re.test((e.innerText || e.getAttribute('aria-label') || '').trim()) && (e.innerText || '').length < maxLen);
  if (!el) return null;
  el.setAttribute(attr, '1');
  return (el.innerText || el.getAttribute('aria-label')).trim();
}, { src: re, attr, maxLen });

for (const u of URLS) {
  const page = await task.newPage();
  try {
    await page.goto(u); await page.waitForLoadState(); await page.waitForTimeout(2500);
    let g = await mark(page, 'google', 'data-dh-g', 60);
    if (!g) {
      const l = await mark(page, '^(log ?in|sign ?in|login|sign up|get started|join)$', 'data-dh-l', 30);
      if (l) { await page.click('[data-dh-l="1"]', { label: l }); await page.waitForTimeout(2500); g = await mark(page, 'google', 'data-dh-g', 60); }
    }
    if (!g) { console.log(page.label, u, 'NO GOOGLE BUTTON ->', (await page.url()).slice(0, 80)); continue; }
    const r = await page.click('[data-dh-g="1"]', { label: 'Continue with Google' });
    await page.waitForTimeout(4000);
    console.log(page.label, u, 'clicked', JSON.stringify(g), 'popups', JSON.stringify((r.popups || []).map((p) => p.label)), '->', (await page.url()).slice(0, 70));
  } catch (e) { console.log(page.label, u, 'ERR', String(e).slice(0, 150)); }
}
for (const t of await task.tabs()) console.log(t.label, t.url.slice(0, 80));
