#!/usr/bin/env python3
"""Build the Beacon website.

Sources live in src/:
  styles.css            -> site/styles.css
  app.js                -> site/app.js
  pages/<name>.html     -> site/<name>.html   (first line is a JSON header)

In page sources, {{i:name}} becomes an inline line icon (see ICONS).

Run:  python3 build.py            build the site
      python3 build.py --demo     also make beacon-demo.html (one-file preview)
"""
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"
EXTRA_CSS = []  # theme files appended after styles.css (see --theme)

NAV = [
    ("index", "index.html", "Home", "ہوم"),
    ("about", "about.html", "About", "تعارف"),
    ("academics", "academics.html", "Academics", "تعلیم"),
    ("admissions", "admissions.html", "Admissions", "داخلے"),
    ("contact", "contact.html", "Contact", "رابطہ"),
]

ICONS = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.6A8.4 8.4 0 1 1 21 11.5z"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "apply": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "fees": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>',
    "steps": '<path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/><path d="M13 6h8M13 12h8M13 18h8"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16"/><path d="M10 14.7V17c0 .6-.5 1-1 1.2C7.9 18.8 7 20.2 7 22M14 14.7V17c0 .6.5 1 1 1.2 1.2.6 2 2 2 3.8"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/>',
    "blocks": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><circle cx="17.5" cy="17.5" r="3.5"/>',
    "pencil": '<path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"/>',
    "flask": '<path d="M9 2v6L4 18a2 2 0 0 0 1.8 3h12.4A2 2 0 0 0 20 18l-5-10V2M8 2h8M7 15h10"/>',
    "cap": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "bus": '<rect x="4" y="3" width="16" height="15" rx="2"/><path d="M4 11h16M8 18v3M16 18v3M8 14.5h.01M16 14.5h.01"/>',
    "school": '<path d="M3 21h18M5 21V10l7-5 7 5v11"/><path d="M10 21v-5h4v5"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "library": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
}

WA_PATH = '<path fill="currentColor" stroke="none" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.8 1.2 3.2 1.4 3.5 2.4 3.6 5.8 5c2.2.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5s.3-1.3.2-1.5-.3-.2-.6-.4z"/>'

DUO = {'apply': '<circle cx="16.5" cy="16.5" r="5" fill="#fbbd13" stroke="none"/>', 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="#fbbd13" stroke="none" opacity=".45"/>', 'book': '<path d="M6.5 2H20v15H6.5A2.5 2.5 0 0 0 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" fill="#fbbd13" stroke="none" opacity=".45"/>', 'pin': '<circle cx="12" cy="10" r="3.2" fill="#fbbd13" stroke="none"/>', 'steps': '<circle cx="6" cy="8" r="4" fill="#fbbd13" stroke="none" opacity=".6"/><circle cx="6" cy="18" r="4" fill="#fbbd13" stroke="none" opacity=".6"/>', 'fees': '<circle cx="12" cy="12" r="3.5" fill="#fbbd13" stroke="none"/>', 'megaphone': '<path d="m3 11 18-5v12L3 14v-3z" fill="#fbbd13" stroke="none" opacity=".5"/>', 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z" fill="#fbbd13" stroke="none" opacity=".4"/>', 'school': '<path d="M5 21V10l7-5 7 5v11z" fill="#fbbd13" stroke="none" opacity=".4"/>', 'blocks': '<circle cx="17.5" cy="17.5" r="3.5" fill="#fbbd13" stroke="none"/>', 'cap': '<path d="M22 10 12 5 2 10l10 5 10-5z" fill="#fbbd13" stroke="none" opacity=".5"/>', 'star': '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="#fbbd13" stroke="none" opacity=".55"/>', 'trophy': '<path d="M18 2H6v7a6 6 0 0 0 12 0V2z" fill="#fbbd13" stroke="none" opacity=".55"/>', 'help': '<circle cx="12" cy="12" r="10" fill="#fbbd13" stroke="none" opacity=".35"/>', 'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" fill="#fbbd13" stroke="none" opacity=".35"/>', 'flask': '<path d="M6.5 15h11l2.5 3a2 2 0 0 1-1.8 3H5.8A2 2 0 0 1 4 18z" fill="#fbbd13" stroke="none" opacity=".6"/>', 'pencil': '<path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z" fill="#fbbd13" stroke="none" opacity=".45"/>', 'monitor': '<rect x="2" y="3" width="20" height="14" rx="2" fill="#fbbd13" stroke="none" opacity=".35"/>', 'users': '<circle cx="9" cy="7" r="4" fill="#fbbd13" stroke="none" opacity=".55"/>', 'library': '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z" fill="#fbbd13" stroke="none" opacity=".45"/>', 'bus': '<rect x="4" y="3" width="16" height="8" rx="2" fill="#fbbd13" stroke="none" opacity=".45"/>'}

SPRITE = '<svg class="sprite" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{DUO.get(k, "")}{v}</symbol>' for k, v in ICONS.items()
) + f'<symbol id="i-wa" viewBox="0 0 32 32">{WA_PATH}</symbol>' + "</svg>"


def icon(name):
    return f'<svg class="ic" aria-hidden="true"><use href="#i-{name}"/></svg>'


PHONE = "0300&#8209;5148824"
WA = "https://wa.me/923005148824"

HEAD = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0a2a4f">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="img/logo-160.png">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="preload" href="fonts/plus-jakarta-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
{extra_head}</head>
<body>
{sprite}
<a class="skip" href="#main" data-ur="مواد پر جائیں">Skip to content</a>

<aside class="notice-strip" aria-label="Admissions notice">
  <div class="container">
    <p><b data-ur="داخلے جاری ہیں">Admissions open</b><span class="hide-sm" data-ur="پلے گروپ تا ایف ایس سی · پری کیڈٹ گریڈ ۵ تا ۹"> · Playgroup to FSc · Pre-cadet Grades 5–9</span> <a href="admissions.html#apply" data-ur="اپلائی کریں ←">Apply →</a></p>
    <button class="lang" id="langBtn" type="button" lang="ur">اردو</button>
  </div>
</aside>

<header class="site">
  <div class="container">
    <a class="brand" href="index.html">
      <img src="img/logo-96.webp" width="48" height="48" alt="">
      <span class="long"><b data-ur="بیکن پبلک اسکول اینڈ کالج">Beacon Public School &amp; College</b><small data-ur="ہری پور، خیبر پختونخوا">Haripur, Khyber Pakhtunkhwa</small></span>
      <span class="short"><span data-ur="بیکن پبلک اسکول">Beacon Public School</span><span data-ur="اینڈ کالج، ہری پور">&amp; College, Haripur</span></span>
    </a>
    <nav class="main" id="mainNav" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
    <div class="actions">
      <a class="icon-btn call" href="tel:+923005148824" aria-label="Call 0300-5148824">{i_phone}</a>
      <a class="icon-btn wa" href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp 0300-5148824">{i_wa}<span class="wa-label">WhatsApp</span></a>
      <a class="btn btn-gold apply-top" href="admissions.html#apply" data-ur="ابھی داخلہ لیں">Apply now</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="Menu">{i_menu}</button>
    </div>
  </div>
</header>

<main id="main">
"""

CTA = """
<section class="cta" aria-label="Admissions open">
  <div class="container">
    <div>
      <h2 data-ur="داخلے جاری ہیں: پلے گروپ تا ایف ایس سی">Admissions open: Playgroup to FSc</h2>
      <p data-ur="محدود نشستیں۔ کسی بھی کیمپس پر تشریف لائیں، کال کریں یا واٹس ایپ کریں۔">Limited seats. Visit any campus, call or message us on WhatsApp.</p>
    </div>
    <div class="cta-row">
      <a class="btn btn-navy" href="admissions.html#apply" data-ur="آن لائن اپلائی کریں">Apply online</a>
      <a class="btn btn-outline" href="{wa}" target="_blank" rel="noopener">{iwa}WhatsApp <span class="ltr">0300&#8209;5148824</span></a>
    </div>
  </div>
</section>
"""

FOOT = """</main>

<footer>
  <div class="container">
    <div class="cols">
      <div>
        <img src="img/logo-160.webp" width="80" height="80" alt="" loading="lazy">
        <p class="motto">ASPIRE · ACQUIRE · INSPIRE</p>
        <p data-ur="بیکن پبلک اسکول اینڈ کالج، ہری پور۔ پلے گروپ سے ایف ایس سی تک، تین کیمپسز میں۔ جہاں ہر بچہ چمکتا ہے۔">Beacon Public School &amp; College, Haripur. Playgroup to FSc on three campuses. Where every child shines.</p>
      </div>
      <div>
        <h3 data-ur="صفحات">Pages</h3>
        <ul>
{footnav}
          <li><a href="privacy.html" data-ur="پرائیویسی پالیسی">Privacy policy</a></li>
        </ul>
      </div>
      <div>
        <h3 data-ur="کیمپس">Campuses</h3>
        <ul>
          <li data-ur="مین کیمپس، شکر شاہ روڈ">Main Campus, Shakar Shah Road</li>
          <li data-ur="ٹی آئی پی کیمپس، ہاؤسنگ کالونی روڈ ۱۸">TIP Campus, Housing Colony Road 18</li>
          <li data-ur="مانکرائی کیمپس، بی ایچ یو کے قریب">Mankrai Campus, near BHU</li>
        </ul>
      </div>
      <div>
        <h3 data-ur="رابطہ">Contact</h3>
        <ul>
          <li><a href="tel:+923005148824">{phone}</a></li>
          <li><a href="{wa}" target="_blank" rel="noopener" data-ur="واٹس ایپ پر پیغام بھیجیں">Message us on WhatsApp</a></li>
          <li><a href="https://www.facebook.com/bpsharipur/" target="_blank" rel="noopener">facebook.com/bpsharipur</a></li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>© <span id="yr">2026</span> Beacon Public School &amp; College, Haripur</span>
      <span data-ur="ویب سائٹ کا ڈیزائن: DesignSpark">Website by DesignSpark</span>
    </div>
  </div>
</footer>


<script src="app.js" defer></script>
</body>
</html>
"""


def nav_html(active, indent="        "):
    out = []
    for key, href, en, ur in NAV:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'{indent}<li><a href="{href}"{cur} data-ur="{ur}">{en}</a></li>')
    if active is not None:
        out.append(f'{indent}<li class="nav-apply"><a class="btn btn-gold" href="admissions.html#apply" data-ur="ابھی داخلہ لیں">Apply now</a></li>')
    return "\n".join(out)


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    return css.strip() + "\n"


def render(text):
    text = re.sub(r"\{\{i:([a-z]+)\}\}", lambda m: icon(m.group(1)), text)
    # keep the phone number on one line in English text (leave Urdu data-ur values alone)
    parts = re.split(r'(data-ur="[^"]*")', text)
    parts = [p.replace("0300-5148824", "\u20660300-5148824\u2069") if p.startswith("data-ur=")
             else p.replace("0300-5148824", '<span class="ltr">0300&#8209;5148824</span>') for p in parts]
    return "".join(parts)


def build():
    css = (SRC / "styles.css").read_text(encoding="utf-8")
    for extra in EXTRA_CSS:
        css += "\n" + extra.read_text(encoding="utf-8")
    (OUT / "styles.css").write_text(minify_css(css), encoding="utf-8")
    (OUT / "app.js").write_text((SRC / "app.js").read_text(encoding="utf-8"), encoding="utf-8")
    keep = set()
    for page in sorted((SRC / "pages").glob("*.html")):
        header, body = page.read_text(encoding="utf-8").split("\n", 1)
        meta = json.loads(header)
        html = HEAD.format(
            title=meta["title"], desc=meta["desc"], phone=PHONE, wa=WA,
            nav=nav_html(meta.get("nav") or ""), extra_head=meta.get("head", ""), sprite=SPRITE,
            i_phone=icon("phone"), i_wa=icon("wa"), i_menu=icon("menu"),
        )
        html += render(body).rstrip() + "\n"
        if meta.get("cta", True):
            html += CTA.format(wa=WA, iwa=icon("wa"))
        html += FOOT.format(phone=PHONE, wa=WA, footnav=nav_html(None, "          "))
        (OUT / page.name).write_text(html, encoding="utf-8")
        keep.add(page.name)
    for old in OUT.glob("*.html"):
        if old.name not in keep:
            old.unlink()
            print("removed old page:", old.name)
    print("built:", ", ".join(sorted(keep)))


ROUTER = """<script>
(() => {
  const pages = [...document.querySelectorAll('.page')];
  function show() {
    const h = decodeURIComponent(location.hash.slice(1));
    if (h === 'main') return;
    let pg = h.split('--')[0];
    if (!pages.some(p => p.dataset.page === pg)) pg = 'index';
    pages.forEach(p => { p.hidden = p.dataset.page !== pg; });
    document.title = pages.find(p => p.dataset.page === pg).dataset.title;
    document.querySelectorAll('nav.main a').forEach(a => {
      if (a.getAttribute('href') === '#' + pg) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    document.getElementById('mainNav').classList.remove('open');
    const target = h.includes('--') ? document.getElementById(h) : null;
    if (target) target.scrollIntoView(); else window.scrollTo(0, 0);
  }
  addEventListener('hashchange', show);
  show();
})();
</script>
"""

KEEP_IDS = {"admForm", "contactForm"}


def demo_links(html):
    """Rewrite page.html / page.html#x links to in-file routes."""
    html = re.sub(r'href="([a-z]+)\.html#([\w-]+)"', r'href="#\1--\2"', html)
    return re.sub(r'href="([a-z]+)\.html"', r'href="#\1"', html)


def build_demo(out_file):
    """Bundle every built page into one self-contained HTML file for previews."""
    def uri(name, mime="image/webp"):
        return f"data:{mime};base64," + base64.b64encode((OUT / "img" / name).read_bytes()).decode()

    images = {
        "img/logo.webp": uri("logo-360.webp"),
        "img/logo-96.webp": uri("logo-96.webp"),
        "img/logo-160.webp": uri("logo-160.webp"),
        "img/poster-cadet.webp": uri("poster-cadet.webp"),
        "img/poster-admissions.webp": uri("poster-admissions.webp"),
        "img/favicon.png": uri("favicon.png", "image/png"),
    }
    sections, shell = [], None
    for page in sorted((SRC / "pages").glob("*.html")):
        key = page.stem
        html = (OUT / page.name).read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", html).group(1)
        start = html.index('<main id="main">') + len('<main id="main">')
        end = html.index("</main>")
        body = html[start:end]
        if key == "index":
            shell = (html[:start], html[end:])
        body = re.sub(r'id="([\w-]+)"', lambda m: m.group(0) if m.group(1) in KEEP_IDS else f'id="{key}--{m.group(1)}"', body)
        body = re.sub(r'aria-labelledby="([\w-]+)"', rf'aria-labelledby="{key}--\1"', body)
        body = re.sub(r'href="#(?!i-)([\w-]+)"', rf'href="#{key}--\1"', body)
        body = demo_links(body)
        sections.append(f'<div class="page" data-page="{key}" data-title="{title}">\n{body}</div>\n')
    head, tail = shell
    head = demo_links(head).replace(' aria-current="page"', "")
    tail = demo_links(tail)
    css = (OUT / "styles.css").read_text(encoding="utf-8")
    head = head.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}</style>")
    head = head.replace('<meta property="og:image" content="img/logo-160.png">\n', "")
    head = re.sub(r'<link rel="preload"[^>]*>\n', "", head)
    font = "data:font/woff2;base64," + base64.b64encode((OUT / "fonts" / "plus-jakarta-sans-latin.woff2").read_bytes()).decode()
    head = head.replace("url(fonts/plus-jakarta-sans-latin.woff2)", f"url({font})")
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    js = (OUT / "app.js").read_text(encoding="utf-8")
    tail = tail.replace('<script src="app.js" defer></script>', f"<script>\n{js}</script>\n{ROUTER}")
    doc = head + "\n" + "".join(sections) + tail
    doc = re.sub(r'\s(srcset|sizes)="[^"]*"', "", doc)
    for path, data in images.items():
        doc = doc.replace(f'"{path}"', f'"{data}"')
    leftover = re.findall(r'(?:src|href)="(img/[^"]+)"', doc)
    assert not leftover, leftover
    Path(out_file).write_text(doc, encoding="utf-8")
    print("demo:", out_file, f"{len(doc) // 1024} KB")


if __name__ == "__main__":
    theme = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else None
    if theme:
        import shutil
        OUT = ROOT / "variants" / theme / "site"
        OUT.mkdir(parents=True, exist_ok=True)
        for folder in ("img", "fonts"):
            shutil.copytree(ROOT / "site" / folder, OUT / folder, dirs_exist_ok=True)
        EXTRA_CSS = [SRC / "themes" / f"{theme}.css"]
    build()
    if "--demo" in sys.argv:
        build_demo(ROOT / (f"beacon-demo-{theme}.html" if theme else "beacon-demo.html"))
