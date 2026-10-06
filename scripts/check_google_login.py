#!/usr/bin/env python3
"""Check which sites offer "Sign in with Google" (headless Playwright, 8 at a time).

Usage: check_google_login.py domains.txt [--out results.json]
  domains.txt: one domain per line (example.com)

For each domain: open the homepage, follow visible login / sign-up / submit
links, then try common auth paths; look for a Google button text or links to
accounts.google.com / gsi/client / auth/google. Also notes email-link,
password and other SSO options. Treat negatives and "accounts.google.com only"
hits as unconfirmed: many login forms are modals that only render after a click
(re-check them in a real browser by clicking "Log in").
Requires: pip install playwright && playwright install chromium
"""
import asyncio, json, re, sys
from urllib.parse import urlparse, urljoin
from playwright.async_api import async_playwright

PATHS = ['/login', '/sign-in', '/signin', '/auth/login', '/auth/signin', '/auth/sign-in',
         '/signup', '/sign-up', '/register', '/submit', '/dashboard']
AUTH_TXT = re.compile(r'^\s*(log ?in|sign ?in|sign ?up|register|get started|submit.*|add your (tool|product)|list your.*)\s*$', re.I)
G_TXT = re.compile(r'(continue|sign ?in|log ?in|sign ?up|login)\s+(with|via|using)\s+google', re.I)
G_HTML = re.compile(r'accounts\.google\.com|/auth/google|provider[=:/"\' ]+google|gsi/client|g_id_onload', re.I)
EMAIL = re.compile(r'magic link|email me|send (me )?(a )?(link|code)|sign[- ]in link', re.I)
OTHER = re.compile(r'(with|via)\s+(github|apple|microsoft|discord|linkedin|x|twitter)\b', re.I)

async def probe(page, url):
    try:
        r = await page.goto(url, timeout=25000, wait_until='domcontentloaded')
        try: await page.wait_for_load_state('networkidle', timeout=6000)
        except Exception: pass
        await page.wait_for_timeout(1000)
        if r and r.status >= 400: return None
        return page.url, await page.content(), await page.evaluate("document.body ? document.body.innerText : ''")
    except Exception:
        return None

async def check(ctx, sem, dom):
    async with sem:
        page = await ctx.new_page()
        res = {'domain': dom, 'google': False, 'evidence': '', 'login_url': '', 'email_link': False, 'others': set()}
        base = f'https://{dom}'
        first = await probe(page, base)
        cands = []
        if first:
            base = f'{urlparse(first[0]).scheme}://{urlparse(first[0]).netloc}'
            for a in await page.query_selector_all('a'):
                try:
                    t = (await a.inner_text()).strip(); href = await a.get_attribute('href')
                except Exception: continue
                if href and AUTH_TXT.match(t):
                    u = urljoin(base + '/', href)
                    if urlparse(u).netloc.removeprefix('www.') == urlparse(base).netloc.removeprefix('www.'):
                        cands.append(u)
        def analyse(pg):
            url, html, txt = pg
            g = G_TXT.search(txt) or G_TXT.search(html) or G_HTML.search(html)
            if g and not res['google']:
                res.update(google=True, evidence=g.group(0)[:60], login_url=url)
            if EMAIL.search(txt): res['email_link'] = True
            for m in OTHER.finditer(txt): res['others'].add(m.group(2).lower())
        if first: analyse(first)
        for u in list(dict.fromkeys(cands))[:6] + [base + p for p in PATHS]:
            if res['google']: break
            pg = await probe(page, u)
            if pg: analyse(pg)
        res['reachable'] = bool(first); res['others'] = sorted(res['others'])
        await page.close()
        print(f"{dom}: google={res['google']} {res['evidence']!r} {res['login_url']}", file=sys.stderr, flush=True)
        return res

async def main(domains, out):
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
        sem = asyncio.Semaphore(8)
        results = await asyncio.gather(*[check(ctx, sem, d) for d in domains])
        await b.close()
    if out: json.dump(results, open(out, 'w'), indent=1)
    print(f"\n{sum(r['google'] for r in results)}/{len(results)} show Google sign-in")

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    doms = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    asyncio.run(main(doms, sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None))
