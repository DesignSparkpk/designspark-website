#!/usr/bin/env python3
"""Bundle site/ into one self-contained HTML file (flameup-demo.html) for phone previews."""
import base64, re
from pathlib import Path
ROOT = Path(__file__).parent; S = ROOT / "site"
MIME = {".webp": "image/webp", ".png": "image/png", ".mp4": "video/mp4", ".woff2": "font/woff2"}
def uri(rel):
    p = S / rel
    return f"data:{MIME[p.suffix]};base64," + base64.b64encode(p.read_bytes()).decode()
html = (S / "index.html").read_text(encoding="utf-8")
css = (S / "styles.css").read_text(encoding="utf-8")
css = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({uri(m.group(1))})", css)
js = (S / "app.js").read_text(encoding="utf-8")
html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}</style>")
html = html.replace('<script src="app.js" defer></script>', f"<script>\n{js}</script>")
html = re.sub(r'<link rel="preload"[^>]*>\n', "", html)
html = re.sub(r'<meta property="og:image"[^>]*>\n', "", html)
html = re.sub(r'(src|poster|href|data-src|data-poster|data-thumb)="((?:img|media)/[^"]+)"', lambda m: f'{m.group(1)}="{uri(m.group(2))}"', html)
assert not re.findall(r'"(?:img|media|fonts)/', html)
out = ROOT / "flameup-demo.html"; out.write_text(html, encoding="utf-8")
print(out, f"{len(html)//1024} KB")
