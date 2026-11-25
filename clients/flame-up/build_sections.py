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
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "trash": '<path d="M3 6h18M8 6V4.5A1.5 1.5 0 0 1 9.5 3h5A1.5 1.5 0 0 1 16 4.5V6M18.5 6l-.9 13.1a2 2 0 0 1-2 1.9H8.4a2 2 0 0 1-2-1.9L5.5 6"/><path d="M10 10.5v6M14 10.5v6"/>',
    "bike": '<circle cx="5.5" cy="17.5" r="3"/><circle cx="18.5" cy="17.5" r="3"/><path d="M5.5 17.5h5l3.5-7h3.2l1.3 7"/><path d="M14 6h2.6l.6 4.5M8 10.5h6"/>',
    "bag": '<path d="M5 8h14l-1.1 11.2a2 2 0 0 1-2 1.8H8.1a2 2 0 0 1-2-1.8z"/><path d="M9 10.5V7a3 3 0 0 1 6 0v3.5"/>',
    "table": '<path d="M3 10h18M6 10v10M18 10v10M8 6.5h8L18 10H6z"/><path d="M6 15h12"/>',
    "menu": '<path d="M5 3.5h11a3 3 0 0 1 3 3v14H8a3 3 0 0 1-3-3z"/><path d="M9 8.5h6M9 12.5h6M9 16.5h3.5"/>',
    "cart": '<path d="M3 4h2.2l2.3 11h10.8l2.2-8H6.4"/><circle cx="9" cy="19.5" r="1.5"/><circle cx="17" cy="19.5" r="1.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
    "note": '<path d="M4 4h16v11l-5 5H4z"/><path d="M15 20v-5h5M8 9h8M8 12.5h5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}

WA_PATH = ('M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6z'
           'm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4'
           'c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.8 1.2 3.2 1.4 3.5 2.4 3.6 5.8 5c2.2.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5s.3-1.3.2-1.5-.3-.2-.6-.4z')


def wa_icon(cls="ic-wa"):
    return f'<svg class="{cls}" viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" stroke="none" d="{WA_PATH}"/></svg>'


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


def item_attrs(item_id, name, price, thumb="", icon="", color=""):
    extra = f' data-thumb="{thumb}"' if thumb else f' data-icon="{icon}" data-color="{color}"'
    return f'data-item="{item_id}" data-name="{esc(name)}" data-price="{price}"{extra}'


# ---------- menu ----------
NEW = [
    dict(id="mega", name="Mega Deal", price=2450, img="mega-spread", w=720, h=900, tag="Limited time", tagc="red",
         alt="Flame Up Special pizza in a pan, cut into slices",
         desc="3 Zingers\u00a0· 1 Flameup Medium Special pizza\u00a0· 1.5 litre cold drink", big=True,
         chips=[("burger", "3 Zingers"), ("pizza", "1 Pizza"), ("drink", "1.5 L drink")]),
    dict(id="beast", name="Blazed Beast Burger", price=499, img="burger", w=720, h=720, tag="New flavour", tagc="",
         alt="Blazed Beast Burger with lettuce, tomato and cheese on a sesame bun", desc="Lettuce, tomato and cheese in a sesame bun"),
    dict(id="club", name="Club Sandwich Deal", price=580, img="club-sandwich", w=720, h=720, tag="", tagc="",
         alt="Club sandwich pieces in red baskets with fries and white dip", desc="4 pcs\u00a0· regular fries\u00a0· white dip"),
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
         alt="Cheese pulling from a slice of Flame Up stuffed crust pizza lifted from the pan", desc="Cheese-stuffed crust loaded with chicken."),
    dict(id="doner", name="Doner Pizza", img="pizza-top",
         alt="Slice lifted from a Flame Up pizza topped with creamy sauce and olives", desc="Doner chicken, creamy sauce and olives."),
]
SIZES = [("M", 1420), ("L", 1890), ("XL", 2599)]

KITCHEN = [
    ("Beef Burger", "beef-burger", "Flame Up Beef Burger with cheese and tomato on a plate", "Finally launched at Flame Up: a juicy beef patty with cheese and fresh veg.", True),
    ("Pizza Stacker", "pizza-stacker", "Flame Up Pizza Stacker in an open box, topped with fries", "Layers of cheesy, saucy goodness, stacked and loaded with fries.", False),
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


TICKER = ["New: Chicken Cheese Stuffed Pizza", "New: Beef Burger", "Doner Pizza from Rs 1,420", "Blazed Beast Burger Rs 499",
          "Club Sandwich Deal Rs 580", "Birthday setups on the rooftop", "Order on WhatsApp 0336-2222081"]


def ticker():
    one = "".join(f'<li>{ic("flame", "tk-ic")}{esc(t)}</li>' for t in TICKER)
    two = "".join(f'<li aria-hidden="true">{ic("flame", "tk-ic")}{esc(t)}</li>' for t in TICKER)
    return (f'<section class="ticker" aria-label="Today at Flame Up">\n  <ul class="ticker-track">{one}{two}</ul>\n</section>\n')


def build():
    out = [ticker()]
    # NEW & HOT
    out.append('<section class="sec cream" id="new" aria-labelledby="new-h">\n  <div class="wrap">')
    out.append(head("Fresh off the flame", "New &amp; hot", "new-h", "Tap any card to add it to your order."))
    out.append('    <div class="hot">')
    for it in NEW:
        cls = "hot-card big" if it.get("big") else "hot-card"
        tag = f'<span class="sticker {it["tagc"]}">{it["tag"]}</span>' if it["tag"] else ""
        if it.get("chips"):
            tag += ('<ul class="inside" aria-label="In this deal">'
                    + "".join(f'<li>{ic(i, "ic-s")}{esc(t)}</li>' for i, t in it["chips"]) + "</ul>")
        out.append(f'''      <article class="{cls}" {item_attrs(it["id"], it["name"], it["price"], thumb="img/thumb/" + it["img"] + ".webp")}>
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
            out.append(f'''      <article class="deal {color}" {item_attrs(did, name, price, icon=items[0][0], color=color)}>
        {tap(did, name, price)}
        {ic(items[0][0], "deal-mark")}{tg}
        <h3>{esc(name)}</h3>
        <ul class="items">{lis}</ul>
        <div class="buy"><span class="price">{rs(price)}</span>{stepper(did, name)}</div>
      </article>''')
        out.append("    </div>")
    out.append('    <p class="note">Prices from Flame Up\'s menu card. Please confirm when you order.</p>\n  </div>\n</section>\n')

    # PIZZAS
    out.append('<section class="sec cream" id="pizza" aria-labelledby="pizza-h">\n  <div class="wrap">')
    out.append(head("Every bite is a new adventure", "Signature pizzas", "pizza-h", "Pick a size, then add."))
    out.append('    <div class="pizzas">')
    for p in PIZZAS:
        radios = "".join(
            f'<label><input type="radio" name="sz-{p["id"]}" value="{s}|{pr}"{" checked" if s == "M" else ""}><span>{s}<b>{pr:,}</b></span></label>'
            for s, pr in SIZES)
        out.append(f'''      <article class="pz" data-pizza="{p["id"]}" data-name="{esc(p["name"])}" data-thumb="img/thumb/{p["img"]}.webp">
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
        <a class="ask" href="{wa_link(f"Assalam o Alaikum Flame Up, what is the price of the {name}?")}" target="_blank" rel="noopener">{wa_icon("ic-s")}Ask price on WhatsApp</a></div>
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
      <a class="btn btn-yellow" href="{wa_link("Assalam o Alaikum Flame Up, I want to book the rooftop for an event. Date: , Guests: ")}" target="_blank" rel="noopener">{wa_icon("ic-s")}Book an event on WhatsApp</a>
    </div>
  </div>
</section>
''')

    # VIBE
    out.append('<section class="sec vibe" id="vibe" aria-labelledby="vibe-h">\n  <div class="wrap">')
    out.append(head("Inside Flame Up", "Come for the food.<br>Stay for the vibe.", "vibe-h", "Green booths, warm lights, hanging plants and a rooftop that glows at sunset. Your hangout on GT Road."))
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
      <img src="img/logo-badge-160.webp" width="96" height="96" alt="" loading="lazy">
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


MAPS = "https://www.google.com/maps/search/?api=1&amp;query=Flame+Up+Jahangir+Khan+Plaza+GT+Road+Haripur"


def chrome():
    order_wa = wa_link("Assalam o Alaikum Flame Up, I want to place an order.")
    return f'''<footer class="foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="img/logo-badge-160.webp" width="72" height="72" alt="" loading="lazy">
      <p class="foot-name">Flame Up Haripur</p>
      <p class="foot-tag">Grill is old. We like it flamed.</p>
      <div class="socials">
        <a href="https://www.tiktok.com/@flameup_haripur" target="_blank" rel="noopener" aria-label="Flame Up on TikTok">{ic("tiktok")}</a>
        <a href="https://www.instagram.com/flameup_haripur/" target="_blank" rel="noopener" aria-label="Flame Up on Instagram">{ic("insta")}</a>
        <a href="https://www.facebook.com/p/Flame-Up-61565751334650/" target="_blank" rel="noopener" aria-label="Flame Up on Facebook">{ic("fb")}</a>
      </div>
    </div>
    <nav class="foot-col" aria-labelledby="fm-h">
      <h2 class="foot-h" id="fm-h">Menu</h2>
      <ul class="foot-links">
        <li><a href="#new">New &amp; hot</a></li><li><a href="#deals">Deals</a></li><li><a href="#pizza">Signature pizzas</a></li>
        <li><a href="#kitchen">Kitchen favourites</a></li><li><a href="#rooftop">Rooftop events</a></li>
      </ul>
    </nav>
    <div class="foot-col">
      <h2 class="foot-h">Visit</h2>
      <ul class="foot-info">
        <li>{ic("pin", "ic-s")}<a href="{MAPS}" target="_blank" rel="noopener">1st Floor, Jahangir Khan Plaza, Sabzi Mandi Mor, G.T. Road, Haripur</a></li>
        <li>{ic("clock", "ic-s")}<span>Every day, 12 PM – 12 AM</span></li>
      </ul>
    </div>
    <div class="foot-col">
      <h2 class="foot-h">Order</h2>
      <ul class="foot-info">
        <li>{ic("phone", "ic-s")}<a href="tel:+923362222081">0336&#8209;2222081</a></li>
        <li>{ic("phone", "ic-s")}<a href="tel:+923141401155">0314&#8209;1401155</a></li>
        <li>{wa_icon("ic-s")}<a href="{order_wa}" target="_blank" rel="noopener">Order on WhatsApp</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <p>© <span id="yr">2026</span> Flame Up Haripur</p>
    <p>Website by DesignSpark</p>
  </div>
</footer>

<nav class="quickbar" aria-label="Quick actions">
  <a href="#deals">{ic("menu")}Menu</a>
  <a href="{MAPS}" target="_blank" rel="noopener">{ic("pin")}Map</a>
  <a href="tel:+923362222081">{ic("phone")}Call</a>
  <button type="button" class="qb-order" data-open-cart>{ic("cart")}Order <b class="count" data-count>0</b><span class="sr-only"> items, open your order</span></button>
</nav>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<div class="drawer" id="cart" role="dialog" aria-modal="true" aria-labelledby="cart-h" hidden>
  <div class="drawer-bg" data-close-cart></div>
  <div class="sheet">
    <div class="sheet-head" id="sheetHead">
      <span class="grab" aria-hidden="true"></span>
      <div class="sh-title">
        <h2 id="cart-h">Your order</h2>
        <p class="sh-sub" id="cartSub">No items yet</p>
      </div>
      <button type="button" class="sh-clear" id="clearCart">{ic("trash", "ic-s")}Clear</button>
      <button type="button" class="sh-x" data-close-cart aria-label="Close your order">{ic("x")}</button>
    </div>

    <div class="sheet-body">
      <div class="empty" id="empty">
        <span class="empty-art" aria-hidden="true">{ic("cart")}</span>
        <h3>Your order is empty</h3>
        <p>Tap any deal, burger or pizza to add it here.</p>
        <a class="btn btn-yellow" href="#deals" data-close-cart>Browse deals {ic("arrow", "ic-s")}</a>
      </div>

      <ul class="lines" id="lines" aria-label="Items in your order"></ul>
      <a class="addmore" id="addMore" href="#deals" data-close-cart>{ic("plus", "ic-s")}Add more items</a>

      <form id="orderForm" class="oform" novalidate>
        <fieldset class="otype">
          <legend>How do you want it?</legend>
          <div class="seg">
            <label><input type="radio" name="otype" value="Delivery" checked><span>{ic("bike")}Delivery</span></label>
            <label><input type="radio" name="otype" value="Pick-up"><span>{ic("bag")}Pick-up</span></label>
            <label><input type="radio" name="otype" value="Dine-in"><span>{ic("table")}Dine-in</span></label>
          </div>
        </fieldset>
        <div class="fields">
          <label class="fld"><span class="fl">Your name</span><span class="inp">{ic("user", "ic-s")}<input type="text" name="name" autocomplete="name" placeholder="e.g. Ali Khan" required></span></label>
          <label class="fld"><span class="fl">Phone number</span><span class="inp">{ic("phone", "ic-s")}<input type="tel" name="phone" autocomplete="tel" inputmode="tel" placeholder="03XX XXXXXXX" required></span></label>
          <label class="fld" id="addrWrap"><span class="fl">Delivery address</span><span class="inp">{ic("pin", "ic-s")}<textarea name="address" rows="2" autocomplete="street-address" placeholder="House, street, area" required></textarea></span></label>
          <label class="fld"><span class="fl">Note <i>(optional)</i></span><span class="inp">{ic("note", "ic-s")}<input type="text" name="note" placeholder="Extra sauce, no onions…"></span></label>
        </div>
      </form>
    </div>

    <div class="sheet-foot" id="sheetFoot">
      <div class="sum">
        <div><span>Subtotal</span><b id="subtotal">Rs 0</b></div>
        <div class="sum-note" id="sumNote"><span>Delivery charges</span><span>Confirmed on WhatsApp</span></div>
      </div>
      <p class="formmsg" id="formmsg" role="status"></p>
      <button class="send" type="submit" form="orderForm">{wa_icon()}<span>Send order on WhatsApp</span><b id="total">Rs 0</b></button>
      <p class="sh-fine">WhatsApp opens with your order typed out. Just press send.</p>
    </div>
  </div>
</div>'''


def splice(doc, start, end, content):
    a = doc.index(start) + len(start)
    b = doc.index(end)
    return doc[:a] + "\n" + content + "\n" + doc[b:]


if __name__ == "__main__":
    doc = PAGE.read_text(encoding="utf-8")
    doc = splice(doc, "<!-- ICONS START -->", "<!-- ICONS END -->", sprite())
    body = "\n".join(l for l in (x.rstrip() for x in build().split("\n")) if l)
    doc = splice(doc, "<!-- SECTIONS START -->", "<!-- SECTIONS END -->", body)
    doc = splice(doc, "<!-- CHROME START -->", "<!-- CHROME END -->", chrome())
    PAGE.write_text(doc, encoding="utf-8")
    print("sections written")
