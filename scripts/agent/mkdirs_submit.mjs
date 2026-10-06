// Fill and submit the details step of a Mkdirs-template directory (Turbo0, aitoolfame,
// toolfame, NewTool.site, …): AI Autofill → Analyze → images → Submit → prints the
// plan page so you can pick Free and read the badge snippet.
//
// Usage (the page must already be on https://<site>/submit and logged in):
//   { echo 'const SPACE=114; const LABEL="p23"; const URL="https://product.example"; const LOGO="/abs/logo-512.png"; const COVER="/abs/cover.png";'; \
//     cat mkdirs_submit.mjs; } | ego-browser nodejs
const task = await taskSpace(SPACE);
const page = task.page(LABEL);
await page.fill('input[name=link]', URL);
await page.click('button:has-text("AI Autofill")', { label: 'AI Autofill' });
await page.waitForTimeout(1500);
await page.click('button:text-is("Analyze")', { label: 'Analyze' }).catch(() => {}); // confirm dialog on some sites
await page.waitForFunction(() => document.querySelector('input[name=name]')?.value?.length > 0
  && document.querySelector('textarea[name=description]')?.value?.length > 0, undefined, { timeout: 150000 })
  .catch(() => console.log('autofill timeout — fill manually'));
await page.waitForTimeout(4000);
console.log(JSON.stringify(await page.evaluate(() => ({
  name: document.querySelector('input[name=name]').value,
  desc: document.querySelector('textarea[name=description]').value,
  intro: (document.querySelector('.cm-content,.CodeMirror,[contenteditable]') || {}).innerText?.slice(0, 300),
}))));
// Upload images only if autofill didn't add one. Two inputs = logo + image; one = image.
const hasImg = await page.evaluate(() => !!document.querySelector('form img'));
if (!hasImg) {
  const n = await page.evaluate(() => [...document.querySelectorAll('input[type=file]')].map((e, i) => { e.setAttribute('data-f', i); return i; }).length);
  if (n > 1) { await page.setInputFiles('[data-f="0"]', [LOGO]); await page.waitForTimeout(3000); await page.setInputFiles('[data-f="1"]', [COVER]); }
  else await page.setInputFiles('[data-f="0"]', [COVER]);
  await page.waitForTimeout(5000);
}
await page.evaluate(() => [...document.querySelectorAll('button')].find((b) => b.innerText.trim() === 'Submit' && b.closest('form')).setAttribute('data-go', '1'));
await page.click('[data-go="1"]', { label: 'Submit' });
await page.waitForTimeout(7000);
console.log(await page.url());
const t = await page.evaluate(() => (document.querySelector('main') || document.body).innerText);
console.log(t.slice(t.indexOf('Plan:'), t.indexOf('Plan:') + 900));
// Next: click the Free card button ("Verify backlink first" / "Choose Free Plan" / "Verify Badge First"),
// read the snippet from the dialog's <code>/<pre>, add it to the site, deploy, then Verify → "Submit to review".
