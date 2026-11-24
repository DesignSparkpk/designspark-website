#!/usr/bin/env python3
"""Build the Beacon multi-page site.

Sources live in src/:
  base.css, pages.css   -> site/styles.css
  app.js                -> site/app.js
  pages/<name>.html     -> site/<name>.html   (first line is a JSON header)

Run:  python3 build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"

NAV = [
    ("index", "index.html", "Home", "ہوم"),
    ("about", "about.html", "About", "تعارف"),
    ("academics", "academics.html", "Academics", "تعلیم"),
    ("admissions", "admissions.html", "Admissions", "داخلے"),
    ("results", "results.html", "Results", "نتائج"),
    ("contact", "contact.html", "Contact", "رابطہ"),
]

PHONE = "0300&#8209;5148824"

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
<link rel="stylesheet" href="styles.css">
{extra_head}</head>
<body>
<a class="skip" href="#main" data-ur="مواد پر جائیں">Skip to content</a>

<aside aria-label="Notice and contact bar">
<div class="demo" role="note" data-ur="ڈیزائن کا نمونہ از DesignSpark۔ جن معلومات پر &quot;نمونہ&quot; لکھا ہے وہ اسکول سے تصدیق ہونا باقی ہیں۔">Concept design by DesignSpark. Items marked "Sample" are waiting for confirmation from the school.</div>
<div class="topbar">
  <div class="container">
    <div class="left">
      <a href="tel:+923005148824">📞&nbsp;{phone}</a>
      <a href="https://wa.me/923005148824" target="_blank" rel="noopener" data-ur="💬 واٹس ایپ">💬 WhatsApp</a>
      <a class="hide-sm" href="https://www.facebook.com/bpsharipur/" target="_blank" rel="noopener">Facebook</a>
    </div>
    <button class="lang" id="langBtn" type="button" lang="ur">اردو</button>
  </div>
</div>
</aside>

<header class="site">
  <div class="container">
    <a class="brand" href="index.html">
      <img class="brand-logo" src="img/logo-96.webp" width="46" height="46" alt="">
      <span><b data-ur="بیکن پبلک اسکول اینڈ کالج">Beacon Public School &amp; College</b><small data-ur="ہری پور، خیبر پختونخوا">Haripur, Khyber Pakhtunkhwa</small></span>
    </a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mainNav" data-ur="مینو">Menu</button>
    <nav class="main" id="mainNav" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
    <a class="btn btn-gold apply-top" href="admissions.html#apply" data-ur="داخلہ لیں">Apply now</a>
  </div>
</header>

<main id="main">
"""

CTA = """
<section class="block" aria-label="Admissions open">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2 data-ur="داخلے جاری ہیں: پلے گروپ تا ایف ایس سی">Admissions open: Playgroup to FSc</h2>
        <p data-ur="محدود نشستیں، جلد اپلائی کریں۔ کسی بھی کیمپس پر تشریف لائیں یا واٹس ایپ کریں۔">Limited seats, apply early. Visit any campus or message us on WhatsApp.</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-gold" href="admissions.html#apply" data-ur="آن لائن داخلہ فارم">Apply online</a>
        <a class="btn btn-wa" href="https://wa.me/923005148824" target="_blank" rel="noopener" data-ur="واٹس ایپ کریں">WhatsApp us</a>
      </div>
    </div>
  </div>
</section>
"""

FOOT = """</main>

<footer>
  <div class="container">
    <div class="cols">
      <div>
        <img class="foot-logo" src="img/logo-160.webp" width="80" height="80" alt="" loading="lazy">
        <p class="foot-motto">ASPIRE · ACQUIRE · INSPIRE</p>
        <p data-ur="جہاں ہر بچہ چمکتا ہے۔ پلے گروپ سے ایف ایس سی تک، ہری پور میں۔">Where every child shines. Playgroup to FSc in Haripur.</p>
      </div>
      <div>
        <h3 data-ur="صفحات">Pages</h3>
        <ul>
{footnav}
          <li><a href="privacy.html" data-ur="پرائیویسی پالیسی">Privacy policy</a></li>
        </ul>
      </div>
      <div>
        <h3 data-ur="رابطہ">Contact</h3>
        <ul>
          <li><a href="tel:+923005148824">📞&nbsp;{phone}</a></li>
          <li><a href="https://wa.me/923005148824" target="_blank" rel="noopener">💬 WhatsApp</a></li>
          <li><a href="https://www.facebook.com/bpsharipur/" target="_blank" rel="noopener">Facebook</a></li>
          <li data-ur="مین کیمپس، شکر شاہ روڈ">Main Campus, Shakar Shah Road</li>
          <li data-ur="ٹی آئی پی کیمپس، ہاؤسنگ کالونی روڈ ۱۸">TIP Campus, Housing Colony Road 18</li>
          <li data-ur="مانکرائی کیمپس، بی ایچ یو کے قریب">Mankrai Campus, near BHU</li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>© <span id="yr">2026</span> Beacon Public School &amp; College, Haripur</span>
      <span data-ur="ڈیزائن: DesignSpark">Website concept by DesignSpark</span>
    </div>
  </div>
</footer>

<aside aria-label="Quick WhatsApp chat">
<a class="fab" href="https://wa.me/923005148824" target="_blank" rel="noopener" aria-label="Chat with Beacon on WhatsApp">
  <svg viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.8 1.2 3.2 1.4 3.5 2.4 3.6 5.8 5c2.2.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5s.3-1.3.2-1.5-.3-.2-.6-.4z"/></svg>
</a>
</aside>

<script src="app.js" defer></script>
</body>
</html>
"""


def nav_html(active, indent="        "):
    out = []
    for key, href, en, ur in NAV:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'{indent}<li><a href="{href}"{cur} data-ur="{ur}">{en}</a></li>')
    return "\n".join(out)


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    return css.strip() + "\n"


def build():
    css = (SRC / "base.css").read_text(encoding="utf-8") + "\n" + (SRC / "pages.css").read_text(encoding="utf-8")
    (OUT / "styles.css").write_text(minify_css(css), encoding="utf-8")
    (OUT / "app.js").write_text((SRC / "app.js").read_text(encoding="utf-8"), encoding="utf-8")
    built = []
    for page in sorted((SRC / "pages").glob("*.html")):
        raw = page.read_text(encoding="utf-8")
        header, body = raw.split("\n", 1)
        meta = json.loads(header)
        html = HEAD.format(
            title=meta["title"],
            desc=meta["desc"],
            phone=PHONE,
            nav=nav_html(meta.get("nav")),
            extra_head=meta.get("head", ""),
        )
        html += body.rstrip() + "\n"
        if meta.get("cta", True):
            html += CTA
        html += FOOT.format(phone=PHONE, footnav=nav_html(None, "          "))
        (OUT / page.name).write_text(html, encoding="utf-8")
        built.append(page.name)
    print("built:", ", ".join(built))


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
    import base64

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
    sections = []
    shell = None
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
        body = re.sub(r'href="#([\w-]+)"', rf'href="#{key}--\1"', body)
        body = demo_links(body)
        sections.append(f'<div class="page" data-page="{key}" data-title="{title}">\n{body}</div>\n')
    head, tail = shell
    head = demo_links(head).replace(' aria-current="page"', "")
    tail = demo_links(tail)
    css = (OUT / "styles.css").read_text(encoding="utf-8")
    head = head.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}</style>")
    head = head.replace('<meta property="og:image" content="img/logo-160.png">\n', "")
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
    import sys
    build()
    if "--demo" in sys.argv:
        build_demo(ROOT / "beacon-demo.html")
