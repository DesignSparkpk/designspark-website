#!/usr/bin/env python3
"""Generate the menu, kitchen, rooftop, vibe and visit sections of site/index.html.

Menu data lives here so prices are edited in one place. Run:  python3 build_sections.py
It replaces everything between <!-- SECTIONS START --> and <!-- SECTIONS END -->
and the icon sprite between <!-- ICONS START --> and <!-- ICONS END -->.
"""
import html
from pathlib import Path

ROOT = Path(__file__).parent
PAGE = ROOT / "site" / "index.html"
WA = "923362222081"

# ---------- icons (24x24, stroke) ----------
ICONS = {
    "burger": '<path d="M4 10a8 6 0 0 1 16 0z"/><path d="M3 13.5h18"/><path d="M4 17h16a2 2 0 0 1-2 3H6a2 2 0 0 1-2-3z"/><path d="M8 7.5h.01M12 6.5h.01M16 7.5h.01"/>',
    "fries": '<path d="M6 10h12l-1.6 10.2a1 1 0 0 1-1 .8H8.6a1 1 0 0 1-1-.8z"/><path d="M8 10 7 3M11 10V2.5M14 10l.5-6.5M17 10l1.5-5"/><path d="M9 14.5c1.8 1 4.2 1 6 0"/>',
    "drink": '<path d="M7 8h10l-1.3 12.2a1 1 0 0 1-1 .8H9.3a1 1 0 0 1-1-.8z"/><path d="M6 8h12"/><path d="m13 8 2-5.5 2.5.5"/><path d="M8 13h8"/>',
    "pizza": '<path d="M12 21 3.5 6.5a15 15 0 0 1 17 0z"/><path d="M5.3 9.6a12 12 0 0 1 13.4 0"/><circle cx="10" cy="11.5" r="1"/><circle cx="14" cy="13" r="1"/><circle cx="12" cy="16.5" r="1"/>',
    "wings": '<path d="M14 4c3.5 0 6 2.5 6 6 0 2.5-1.5 4.5-3.5 5.3L9 19.5a2.5 2.5 0 0 1-3.5-3.5l4.2-7.5C10.5 6 12 4 14 4z"/><path d="M6 20l-2.5 1.5M4.5 17.5 3 18"/>',
    "sandwich": '<path d="M3 15 12 5l9 10z"/><path d="M4.5 16.5h15"/><path d="M5 19h14"/><path d="M9 12.5c1.5 1 4.5 1 6 0"/>',
    "mint": '<path d="M7 3h10l-1.5 11a3.5 3.5 0 0 1-7 0z"/><path d="M12 17.5V21M8.5 21h7"/><path d="M15 3l2-1.5M9 7.5h6"/><circle cx="16.5" cy="6.5" r="1.6"/>',
    "platter": '<ellipse cx="12" cy="15" rx="9" ry="4"/><path d="M6.5 13.5c0-2 2.5-3.5 5.5-3.5s5.5 1.5 5.5 3.5"/><path d="M9 9.5 8 6M12 9V5.5M15 9.5l1-3.5"/>',
    "nuggets": '<path d="M5 11a4 3.2 0 0 1 7-1.5 4 3.2 0 0 1 7 1.5c0 2.8-3 4.5-7 4.5S5 13.8 5 11z"/><path d="M7.5 18.5c2.8 1.3 6.2 1.3 9 0"/>',
    "flame": '<path d="M12 22c4 0 7-2.8 7-6.8 0-3.6-2.4-5.6-3.8-8.7-.5 2.3-1.6 3.5-2.7 4C12.8 7.2 11 4.4 8.6 2c.2 3.6-3.6 6.8-3.6 11.2C5 18.8 8 22 12 22z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9.5"/><path d="M12 7v5l3.5 2"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
    "cake": '<path d="M4 21V12a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9"/><path d="M4 15.5c1.3 1 2.7 1 4 0s2.7-1 4 0 2.7 1 4 0 2.7-1 4 0"/><path d="M3 21h18M12 10V6M12 6c-1-1.2-1-2.4 0-3.5 1 1.1 1 2.3 0 3.5z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "tiktok": '<path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.5 2.8 2.4 4.6 5 5"/>',
    "insta": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
}


def sprite():
    syms = "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items())
    return f'<svg class="sprite" aria-hidden="true" focusable="false">{syms}</svg>'


def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def rs(n):
    return f"Rs {n:,}"


def esc(s):
    return html.escape(s, quote=True)


def stepper(item_id, name):
    return (f'<div class="stepper" data-stepper="{item_id}">'
            f'<button type="button" class="st-add" data-act="inc" aria-label="Add {esc(name)} to order">Add {ic("plus", "ic-s")}</button>'
            f'<div class="st-qty" hidden><button type="button" data-act="dec" aria-label="Remove one {esc(name)}">{ic("minus", "ic-s")}</button>'
            f'<output aria-live="polite">0</output>'
            f'<button type="button" data-act="inc" aria-label="Add one more {esc(name)}">{ic("plus", "ic-s")}</button></div></div>')


def tap(item_id, name, price):
    return f'<button type="button" class="tap" data-tap="{item_id}" aria-label="Add {esc(name)}, {rs(price)}, to order"></button>'


def item_attrs(item_id, name, price):
    return f'data-item="{item_id}" data-name="{esc(name)}" data-price="{price}"'


# ---------- menu ----------
NEW = [
    dict(id="mega", name="Mega Deal", price=2450, img="mega-spread", w=720, h=720, tag="Limited time", tagc="red",
         alt="Flame Up pizza with cold drinks, fries and dip on a table",
         desc="3 Zingers · 1 Flameup Medium Special pizza · 1.5 litre cold drink", big=True),
    dict(id="beast", name="Blazed Beast Burger", price=499, img="burger", w=720, h=720, tag="New flavour", tagc="",
         alt="Blazed Beast Burger with lettuce, tomato and cheese on a sesame bun", desc="Our loaded signature burger"),
    dict(id="club", name="Club Sandwich Deal", price=580, img="club-sandwich", w=720, h=720, tag="", tagc="",
         alt="Club sandwich pieces in red baskets with fries and white dip", desc="4 pcs · regular fries · white dip"),
]

DEALS = {
    "special": ("Special offers", [
        ("d1", "Deal 1", 790, "c-purple", "", [("burger", "1 Bazinga Burger"), ("fries", "1 Regular Fries"), ("drink", "1 Regular Drink")]),
        ("d2", "Deal 2", 680, "c-orange", "", [("burger", "1 Reggy Burger"), ("fries", "1 Regular Fries"), ("drink", "1 Regular Drink")]),
        ("blazing", "Blazing Combo", 1499, "c-red", "New", [("pizza", "1 Medium Pizza"), ("sandwich", "1 Cordoba Sandwich"), ("drink", "1 Litre Drink")]),
        ("d4", "Deal 4", 1949, "c-blue", "", [("pizza", "1 Medium Pizza"), ("wings", "10 pcs Hot Wings"), ("drink", "1.5 Litre Drink")]),
    ]),
    "premium": ("To share", [
        ("cheesy", "Cheesy Bite Deal", 3220, "c-orange", "", [("pizza", "2 Large Pizzas"), ("drink", "1.5 Litre Drink")]),
        ("friends", "Friends Deal", 2340, "c-green", "", [("burger", "5 Bazinga Burgers"), ("drink", "1.5 Litre Drink")]),
        ("family", "Family Deal", 2430, "c-teal", "", [("pizza", "1 Large Pizza"), ("nuggets", "20 Hotshots"), ("drink", "1.5 Litre Drink")]),
        ("flameupdeal", "Flameup Deal", 2690, "c-purple", "", [("pizza", "1 Large Pizza"), ("platter", "1 Platter"), ("drink", "1.5 Litre Drink")]),
    ]),
    "minty": ("New deals", [
        ("mintyclub", "The Minty Club Deal", 1650, "c-dark", "New", [("pizza", "2 Small Pizzas"), ("sandwich", "1 Club Sandwich"), ("mint", "2 Mint Margarita")]),
        ("mintymelte", "The Minty Melte Deal", 2250, "c-navy", "New", [("pizza", "2 Medium Pizzas"), ("mint", "3 Mint Margarita")]),
        ("bazinga", "The Bazinga Deal", 1400, "c-dark", "New", [("burger", "2 Bazinga Burgers"), ("fries", "1 Large Fries"), ("mint", "2 Mint Margarita")]),
    ]),
}

PIZZAS = [
    dict(id="stuffed", name="Chicken Cheese Stuffed Pizza", img="stuffed-cheesepull",
         alt="Long cheese pull from a Flame Up stuffed crust pizza", desc="Cheese-stuffed crust loaded with chicken."),
    dict(id="doner", name="Doner Pizza", img="pizza-top",
         alt="Flame Up pizza with olives and chicken, fresh from the oven", desc="Doner-style chicken, peppers and olives."),
]
SIZES = [("M", 1420), ("L", 1890), ("XL", 2599)]

KITCHEN = [
    ("Beef Burger", "beef-burger", "Flame Up Beef Burger with cheese and tomato on a plate", "Our new king of burgers: a juicy beef patty, cheese and fresh veg.", True),
    ("Pizza Stacker", "pizza-stacker", "Flame Up Pizza Stacker in a box with fries on top", "Layers of cheesy, saucy goodness, stacked and loaded with fries.", False),
    ("Grilled Bite Pizza", "grilled-bite", "Flame Up Special Grilled Bite Pizza on the rooftop table", "The Flame Up special: grilled chicken bites with a creamy drizzle.", False),
]

VIBE = [
    ("vibe-rooftop", "Flame Up rooftop at sunset with lamps, plants and seating under a pink sky", "Rooftop at sunset", "big"),
    ("vibe-hall", "Flame Up dining hall with hanging plants, warm lights and green booths", "The dining hall", ""),
    ("vibe-booth", "Green velvet booth with balloons and neon at Flame Up", "Cosy booths", ""),
    ("vibe-lights", "Hanging bulbs wrapped in leaves at Flame Up", "Warm lights", ""),
    ("birthday", "Birthday setup with purple balloons and a neon Happy Birthday sign at Flame Up", "Birthday setups", ""),
]


def head(eyebrow, title, hid, sub="", light=False):
    cls = " light" if light else ""
    s = f'<div class="sec-head{cls}"><p class="eyebrow">{ic("flame", "ic-f")}{eyebrow}</p><h2 id="{hid}" class="title">{title}</h2>'
    if sub:
        s += f'<p class="sub">{sub}</p>'
    return s + "</div>"


def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"


def build():
    out = []
    # NEW & HOT
    out.append('<section class="sec cream" id="new" aria-labelledby="new-h">\n  <div class="wrap">')
    out.append(head("Fresh off the flame", "New &amp; hot", "new-h", "Tap any card to add it to your order."))
    out.append('    <div class="hot">')
    for it in NEW:
        cls = "hot-card big" if it.get("big") else "hot-card"
        tag = f'<span class="sticker {it["tagc"]}">{it["tag"]}</span>' if it["tag"] else ""
        out.append(f'''      <article class="{cls}" {item_attrs(it["id"], it["name"], it["price"])}>
        {tap(it["id"], it["name"], it["price"])}
        <img src="img/{it["img"]}.webp" width="{it["w"]}" height="{it["h"]}" alt="{esc(it["alt"])}" loading="lazy">
        <div class="hot-shade" aria-hidden="true"></div>
        {tag}
        <div class="hot-body">
          <h3>{esc(it["name"])}</h3>
          <p>{esc(it["desc"])}</p>
          <div class="buy"><span class="price">{rs(it["price"])}</span>{stepper(it["id"], it["name"])}</div>
        </div>
      </article>''')
    out.append("    </div>\n  </div>\n</section>\n")

    # DEALS
    out.append('<section class="sec green" id="deals" aria-labelledby="deals-h">\n  <div class="wrap">')
    out.append(head("Tasty treats, unbeatable prices", "Deals", "deals-h", "Tap a deal to add it. Use − and + to change the quantity.", light=True))
    out.append('    <div class="tabs" role="tablist" aria-label="Deal groups">')
    for k, (key, (label, _)) in enumerate(DEALS.items()):
        sel = "true" if k == 0 else "false"
        ti = "" if k == 0 else ' tabindex="-1"'
        out.append(f'      <button role="tab" id="t-{key}" aria-controls="p-{key}" aria-selected="{sel}"{ti} type="button">{label}</button>')
    out.append("    </div>")
    for k, (key, (label, deals)) in enumerate(DEALS.items()):
        hidden = "" if k == 0 else " hidden"
        out.append(f'    <div class="deals" role="tabpanel" id="p-{key}" aria-labelledby="t-{key}"{hidden}>')
        for did, name, price, color, tag, items in deals:
            lis = "".join(f'<li>{ic(i, "ic-i")}<span>{esc(t)}</span></li>' for i, t in items)
            tg = f'<span class="sticker red">{tag}</span>' if tag else ""
            out.append(f'''      <article class="deal {color}" {item_attrs(did, name, price)}>
        {tap(did, name, price)}
        {ic(items[0][0], "deal-mark")}{tg}
        <h3>{esc(name)}</h3>
        <ul class="items">{lis}</ul>
        <div class="buy"><span class="price">{rs(price)}</span>{stepper(did, name)}</div>
      </article>''')
        out.append("    </div>")
    out.append('    <p class="note">All prices include taxes. Prices from Flame Up\'s menu; please confirm when ordering.</p>\n  </div>\n</section>\n')

    # PIZZAS
    out.append('<section class="sec cream" id="pizza" aria-labelledby="pizza-h">\n  <div class="wrap">')
    out.append(head("Every bite is a new adventure", "Signature pizzas", "pizza-h", "Pick a size, then add."))
    out.append('    <div class="pizzas">')
    for p in PIZZAS:
        radios = "".join(
            f'<label><input type="radio" name="sz-{p["id"]}" value="{s}|{pr}"{" checked" if s == "M" else ""}><span>{s}<b>{pr:,}</b></span></label>'
            for s, pr in SIZES)
        out.append(f'''      <article class="pz" data-pizza="{p["id"]}" data-name="{esc(p["name"])}">
        <div class="pz-img"><img src="img/{p["img"]}.webp" width="720" height="720" alt="{esc(p["alt"])}" loading="lazy"><span class="sticker red">New</span></div>
        <div class="pz-body">
          <h3>{esc(p["name"])}</h3>
          <p>{esc(p["desc"])}</p>
          <fieldset class="sizes"><legend class="sr-only">Size for {esc(p["name"])}</legend>{radios}</fieldset>
          <div class="buy"><span class="price" data-pz-price>{rs(SIZES[0][1])}</span>{stepper(p["id"] + "-M", p["name"] + " (M)")}</div>
        </div>
      </article>''')
    out.append("    </div>\n  </div>\n</section>\n")

    # KITCHEN
    out.append('<section class="sec kitchen" id="kitchen" aria-labelledby="kitchen-h">\n  <div class="wrap">')
    out.append(head("Straight from our kitchen", "Kitchen favourites", "kitchen-h", "New on the menu. Ask us for today's price.", light=True))
    out.append('    <div class="kgrid">')
    for name, img, alt, desc, new in KITCHEN:
        tag = '<span class="sticker red">New</span>' if new else ""
        out.append(f'''      <article class="kcard">
        <div class="k-img"><img src="img/{img}.webp" width="720" height="600" alt="{esc(alt)}" loading="lazy">{tag}</div>
        <div class="kbody"><h3>{esc(name)}</h3><p>{esc(desc)}</p>
        <a class="ask" href="{wa_link(f"Assalam o Alaikum Flame Up, what is the price of the {name}?")}" target="_blank" rel="noopener">{ic("phone", "ic-s")}Ask price on WhatsApp</a></div>
      </article>''')
    out.append("    </div>\n  </div>\n</section>\n")

    # ROOFTOP
    out.append(f'''<section class="sec dark" id="rooftop" aria-labelledby="roof-h">
  <div class="wrap roof">
    <div class="roof-media">
      <video autoplay muted loop playsinline preload="none" poster="img/rooftop-poster.webp" aria-hidden="true">
        <source src="media/rooftop.mp4" type="video/mp4">
      </video>
    </div>
    <div>
      {head("Flame Up rooftop", "Your day,<br>under the open sky", "roof-h", light=True)}
      <p class="lead">Lamps, flowers and city views on the rooftop. We set up birthdays, anniversaries, girls' day outs and family nights. Just tell us the date.</p>
      <ul class="chips">
        <li>{ic("cake", "ic-s")}Birthday setups</li><li>{ic("heart", "ic-s")}Anniversaries</li><li>{ic("users", "ic-s")}Girls' day out</li><li>{ic("star", "ic-s")}Student deals</li><li>{ic("flame", "ic-s")}Family nights</li>
      </ul>
      <a class="btn btn-yellow" href="{wa_link("Assalam o Alaikum Flame Up, I want to book the rooftop for an event. Date: , Guests: ")}" target="_blank" rel="noopener">Book an event on WhatsApp</a>
    </div>
  </div>
</section>
''')

    # VIBE
    out.append('<section class="sec vibe" id="vibe" aria-labelledby="vibe-h">\n  <div class="wrap">')
    out.append(head("Inside Flame Up", "Come for the food.<br>Stay for the vibe.", "vibe-h", "Green booths, warm lights, hanging plants and a rooftop that glows at sunset. Haripur's favourite hangout on GT Road."))
    out.append('    <div class="mosaic">')
    for img, alt, cap, cls in VIBE:
        c = f' class="{cls}"' if cls else ""
        out.append(f'      <figure{c}><img src="img/{img}.webp" width="720" height="900" alt="{esc(alt)}" loading="lazy"><figcaption>{cap}</figcaption></figure>')
    out.append("    </div>\n  </div>\n</section>\n")

    # VISIT
    maps = "https://www.google.com/maps/search/?api=1&amp;query=Flame+Up+Jahangir+Khan+Plaza+GT+Road+Haripur"
    out.append(f'''<section class="sec cream" id="visit" aria-labelledby="visit-h">
  <div class="wrap visit">
    <div>
      {head("Find us", "Visit Flame Up", "visit-h")}
      <ul class="info">
        <li>{ic("pin", "ic-c")}<div><b>Address</b><span>1st Floor, Jahangir Khan Plaza, near Shaheen Chemist, Sabzi Mandi Mor, G.T. Road, Haripur</span></div></li>
        <li>{ic("clock", "ic-c")}<div><b>Hours</b><span>Every day, 12 PM – 12 AM</span></div></li>
        <li>{ic("phone", "ic-c")}<div><b>Delivery &amp; orders</b><span><a href="tel:+923362222081">0336&#8209;2222081</a> · <a href="tel:+923141401155">0314&#8209;1401155</a></span></div></li>
      </ul>
      <div class="cta">
        <a class="btn btn-green" href="{maps}" target="_blank" rel="noopener">{ic("pin", "ic-s")}Get directions</a>
        <a class="btn btn-outline" href="tel:+923362222081">{ic("phone", "ic-s")}Call&nbsp;now</a>
      </div>
    </div>
    <div class="social-card">
      <img src="img/logo-badge-160.png" width="96" height="96" alt="">
      <p class="big">2M+</p>
      <p>views on Flame Up's TikTok videos</p>
      <div class="socials">
        <a href="https://www.tiktok.com/@flameup_haripur" target="_blank" rel="noopener" aria-label="Flame Up on TikTok">{ic("tiktok")}</a>
        <a href="https://www.instagram.com/flameup_haripur/" target="_blank" rel="noopener" aria-label="Flame Up on Instagram">{ic("insta")}</a>
        <a href="https://www.facebook.com/p/Flame-Up-61565751334650/" target="_blank" rel="noopener" aria-label="Flame Up on Facebook">{ic("fb")}</a>
      </div>
      <a class="btn btn-yellow" href="https://www.tiktok.com/@flameup_haripur" target="_blank" rel="noopener">@flameup_haripur</a>
    </div>
  </div>
</section>''')
    return "\n".join(out)


def splice(doc, start, end, content):
    a = doc.index(start) + len(start)
    b = doc.index(end)
    return doc[:a] + "\n" + content + "\n" + doc[b:]


if __name__ == "__main__":
    doc = PAGE.read_text(encoding="utf-8")
    doc = splice(doc, "<!-- ICONS START -->", "<!-- ICONS END -->", sprite())
    body = "\n".join(l for l in (x.rstrip() for x in build().split("\n")) if l)
    doc = splice(doc, "<!-- SECTIONS START -->", "<!-- SECTIONS END -->", body)
    PAGE.write_text(doc, encoding="utf-8")
    print("sections written")
