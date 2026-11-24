(() => {
  const WA = '923362222081';
  const fmt = n => 'Rs ' + n.toLocaleString('en-PK');
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const svg = (name, cls = 'ic') => `<svg class="${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // header turns solid after the hero
  const header = $('header.site');
  const onScroll = () => header.classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // background videos: side videos only on wide screens, none with reduced motion
  if (matchMedia('(min-width: 901px)').matches && !reduce) {
    $$('video[data-src]').forEach(v => { v.poster = v.dataset.poster || ''; v.src = v.dataset.src; v.play().catch(() => {}); });
  }
  else if (matchMedia('(min-width: 901px)').matches) $$('video[data-poster]').forEach(v => { v.poster = v.dataset.poster; });
  if (reduce) $$('video[autoplay]').forEach(v => { v.removeAttribute('autoplay'); v.pause(); });

  // deal tabs
  const tabs = $$('[role=tab]');
  function selectTab(t) {
    tabs.forEach(x => {
      const on = x === t;
      x.setAttribute('aria-selected', on);
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => selectTab(t));
    t.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      const n = tabs[(i + d + tabs.length) % tabs.length];
      selectTab(n); n.focus();
    });
  });

  // ---------- cart state ----------
  // id -> {name, price, qty, thumb, icon, color}
  const cart = new Map();
  try {
    JSON.parse(sessionStorage.getItem('flameup-cart') || '[]').forEach(([id, l]) => {
      if (l && l.qty > 0 && l.price > 0) cart.set(id, l);
    });
  } catch (e) { /* storage blocked: start empty */ }
  const save = () => { try { sessionStorage.setItem('flameup-cart', JSON.stringify([...cart])); } catch (e) {} };

  const count = () => [...cart.values()].reduce((s, l) => s + l.qty, 0);
  const total = () => [...cart.values()].reduce((s, l) => s + l.qty * l.price, 0);

  const toast = $('#toast');
  let toastTimer;
  function say(msg) {
    toast.innerHTML = svg('check', 'ic-s') + '<span></span>';
    toast.lastChild.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 1600);
  }

  function change(id, info, d, quiet) {
    const line = cart.get(id) || { ...info, qty: 0 };
    line.qty = Math.max(0, line.qty + d);
    if (line.qty) cart.set(id, line); else cart.delete(id);
    render();
    if (d > 0) {
      $$('[data-count]').forEach(c => { c.classList.remove('bump'); void c.offsetWidth; c.classList.add('bump'); });
      if (!quiet) say(`${line.name} added`);
    }
  }

  // what a card, tap area or stepper points at
  function itemFor(el) {
    const host = el.closest('[data-item]');
    if (host) {
      const d = host.dataset;
      return { id: d.item, name: d.name, price: +d.price, thumb: d.thumb || '', icon: d.icon || '', color: d.color || '' };
    }
    const pz = el.closest('[data-pizza]');
    if (pz) {
      const [size, price] = pz.querySelector('input[type=radio]:checked').value.split('|');
      return { id: `${pz.dataset.pizza}-${size}`, name: `${pz.dataset.name} (${size})`, price: +price, thumb: pz.dataset.thumb || '', icon: '', color: '' };
    }
    return null;
  }

  document.addEventListener('click', e => {
    const tap = e.target.closest('.tap');
    const act = e.target.closest('[data-act]');
    if (!tap && !(act && act.closest('.stepper'))) return;
    const it = itemFor(tap || act);
    if (!it) return;
    change(it.id, it, act && act.dataset.act === 'dec' ? -1 : 1);
  });

  // pizzas: size change updates price and stepper target
  $$('[data-pizza]').forEach(pz => pz.addEventListener('change', () => {
    const it = itemFor(pz.querySelector('.stepper'));
    pz.querySelector('[data-pz-price]').textContent = fmt(it.price);
    const st = pz.querySelector('.stepper');
    st.dataset.stepper = it.id;
    st.querySelector('.st-add').setAttribute('aria-label', `Add ${it.name} to order`);
    const [dec, inc] = st.querySelectorAll('.st-qty button');
    dec.setAttribute('aria-label', `Remove one ${it.name}`);
    inc.setAttribute('aria-label', `Add one more ${it.name}`);
    render();
  }));

  function renderSteppers() {
    $$('.stepper').forEach(st => {
      const line = cart.get(st.dataset.stepper);
      const q = line ? line.qty : 0;
      st.querySelector('.st-add').hidden = q > 0;
      const box = st.querySelector('.st-qty');
      box.hidden = q === 0;
      box.querySelector('output').textContent = q;
      const card = st.closest('[data-item], [data-pizza]');
      if (card) card.classList.toggle('in-cart', q > 0);
    });
  }

  // ---------- order sheet lines (updated in place so focus is kept) ----------
  const ul = $('#lines');
  const lineEls = new Map();

  function makeLine(id, l) {
    const li = document.createElement('li');
    li.className = 'line'; li.dataset.id = id;
    li.innerHTML = `<span class="th"></span>
      <div class="ln-main"><p class="ln-name"></p><p class="ln-unit"></p></div>
      <div class="ln-right"><b class="ln-total"></b>
        <div class="qp"><button type="button" data-q="-1"></button><output></output><button type="button" data-q="1">${svg('plus', 'ic-s')}</button></div>
      </div>`;
    const th = li.querySelector('.th');
    if (l.thumb) {
      const img = new Image(); img.src = l.thumb; img.alt = ''; img.width = 58; img.height = 58; img.decoding = 'async';
      th.append(img);
    } else {
      if (l.color) th.classList.add(l.color);
      th.innerHTML = svg(l.icon || 'flame');
    }
    li.querySelector('.ln-name').textContent = l.name;
    li.querySelector('.ln-unit').textContent = `${fmt(l.price)} each`;
    li.querySelector('[data-q="1"]').setAttribute('aria-label', `Add one more ${l.name}`);
    return li;
  }

  function updateLine(li, l) {
    li.querySelector('.ln-total').textContent = fmt(l.qty * l.price);
    li.querySelector('output').textContent = l.qty;
    const dec = li.querySelector('[data-q="-1"]');
    const last = l.qty === 1;
    if (dec.dataset.mode !== String(last)) {
      dec.dataset.mode = String(last);
      dec.innerHTML = svg(last ? 'trash' : 'minus', 'ic-s');
      dec.classList.toggle('rm', last);
      dec.setAttribute('aria-label', last ? `Remove ${l.name} from order` : `Remove one ${l.name}`);
    }
  }

  ul.addEventListener('click', e => {
    const b = e.target.closest('button[data-q]');
    if (!b) return;
    const li = b.closest('li');
    const id = li.dataset.id;
    const d = +b.dataset.q;
    const sib = li.nextElementSibling || li.previousElementSibling;
    change(id, null, d, true);
    if (!cart.has(id)) {
      const next = sib && sib.querySelector('button[data-q="-1"]');
      (next || $('#empty a')).focus({ preventScroll: true });
    }
  });

  const plural = n => `${n} item${n === 1 ? '' : 's'}`;

  function render() {
    const n = count();
    $$('[data-count]').forEach(c => c.textContent = n);

    // lines: remove, add, update, keep order of the cart
    for (const [id, li] of lineEls) if (!cart.has(id)) { li.remove(); lineEls.delete(id); }
    for (const [id, l] of cart) {
      let li = lineEls.get(id);
      if (!li) { li = makeLine(id, l); lineEls.set(id, li); ul.append(li); }
      updateLine(li, l);
    }

    const empty = cart.size === 0;
    $('#empty').hidden = !empty;
    ['#lines', '#addMore', '#orderForm', '#sheetFoot', '#clearCart'].forEach(s => { $(s).hidden = empty; });
    $('#cartSub').textContent = empty ? 'No items yet' : `${plural(n)} · ${fmt(total())}`;
    $('#subtotal').textContent = fmt(total());
    $('#total').textContent = fmt(total());
    renderSteppers();
    save();
  }

  $('#clearCart').addEventListener('click', () => {
    cart.clear(); render();
    $('#empty a').focus({ preventScroll: true });
  });

  // ---------- open / close ----------
  const drawer = $('#cart');
  const sheet = drawer.querySelector('.sheet');
  let lastFocus, closeTimer;

  function openCart() {
    clearTimeout(closeTimer);
    drawer.classList.remove('closing');
    sheet.style.transform = '';
    lastFocus = document.activeElement;
    drawer.hidden = false;
    document.body.style.overflow = 'hidden';
    drawer.querySelector('.sh-x').focus({ preventScroll: true });
  }
  function closeCart() {
    if (drawer.hidden || drawer.classList.contains('closing')) return;
    drawer.classList.add('closing');
    document.body.style.overflow = '';
    closeTimer = setTimeout(() => {
      drawer.hidden = true;
      drawer.classList.remove('closing');
      sheet.style.transform = ''; sheet.style.transition = '';
    }, reduce ? 0 : 220);
    if (lastFocus && lastFocus.isConnected) lastFocus.focus({ preventScroll: true });
  }
  $$('[data-open-cart]').forEach(b => b.addEventListener('click', openCart));
  $$('[data-close-cart]').forEach(b => b.addEventListener('click', closeCart));
  drawer.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeCart(); return; }
    if (e.key !== 'Tab') return;
    const f = [...drawer.querySelectorAll('button, input, textarea, a[href]')].filter(x => x.offsetParent !== null && !x.disabled);
    if (!f.length) return;
    const i = f.indexOf(document.activeElement);
    if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
  });

  // phones: drag the sheet header down to close
  const head = $('#sheetHead');
  let dragY = null, dy = 0;
  head.addEventListener('pointerdown', e => {
    if (!matchMedia('(max-width: 640px)').matches || e.target.closest('button')) return;
    dragY = e.clientY; dy = 0; sheet.style.transition = 'none';
    head.setPointerCapture(e.pointerId);
  });
  head.addEventListener('pointermove', e => {
    if (dragY === null) return;
    dy = Math.max(0, e.clientY - dragY);
    sheet.style.transform = `translateY(${dy}px)`;
  });
  const endDrag = () => {
    if (dragY === null) return;
    dragY = null;
    if (dy > 90) { closeCart(); return; }
    sheet.style.transition = 'transform .2s ease'; sheet.style.transform = '';
  };
  head.addEventListener('pointerup', endDrag);
  head.addEventListener('pointercancel', endDrag);

  // ---------- form ----------
  const form = $('#orderForm');
  const addr = $('#addrWrap');
  const KEEP = ['name', 'phone', 'address'];
  try {
    const saved = JSON.parse(localStorage.getItem('flameup-details') || '{}');
    KEEP.forEach(k => { if (saved[k]) form.elements[k].value = saved[k]; });
  } catch (e) {}

  function syncType() {
    const del = form.otype.value === 'Delivery';
    addr.hidden = !del; addr.querySelector('textarea').required = del;
    $('#sumNote').hidden = !del;
  }
  form.querySelectorAll('input[name=otype]').forEach(r => r.addEventListener('change', syncType));
  syncType();

  form.addEventListener('input', e => {
    if (e.target.getAttribute('aria-invalid') === 'true' && e.target.value.trim()) e.target.removeAttribute('aria-invalid');
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    const msg = $('#formmsg');
    if (!cart.size) { msg.textContent = 'Add at least one item first.'; return; }
    const req = [...form.querySelectorAll('[required]')].filter(i => !i.closest('[hidden]'));
    req.forEach(i => { if (i.value.trim()) i.removeAttribute('aria-invalid'); else i.setAttribute('aria-invalid', 'true'); });
    const missing = req.find(i => !i.value.trim());
    if (missing) {
      const n = req.filter(i => !i.value.trim()).length;
      msg.textContent = n > 1 ? 'Please fill in the fields marked in red.'
        : `Please add your ${missing.name === 'phone' ? 'phone number' : missing.name === 'address' ? 'delivery address' : 'name'}.`;
      missing.focus(); return;
    }
    const phone = form.elements.phone;
    const digits = phone.value.replace(/\D/g, '');
    if (digits.length < 10 || digits.length > 13) {
      phone.setAttribute('aria-invalid', 'true');
      msg.textContent = 'Please check your phone number, e.g. 0300 1234567.';
      phone.focus(); return;
    }
    msg.textContent = '';
    const d = Object.fromEntries(new FormData(form));
    try { localStorage.setItem('flameup-details', JSON.stringify({ name: d.name, phone: d.phone, address: d.address || '' })); } catch (err) {}
    const lines = [...cart.values()].map((l, i) => `${i + 1}. ${l.qty} × ${l.name} = ${fmt(l.qty * l.price)}`).join('\n');
    const text = `Assalam o Alaikum Flame Up! I would like to order:\n\n${lines}\n\nTotal: ${fmt(total())}\n\n` +
      `Order type: ${d.otype}\nName: ${d.name.trim()}\nPhone: ${d.phone.trim()}` +
      (d.otype === 'Delivery' ? `\nAddress: ${d.address.trim()}` : '') + (d.note.trim() ? `\nNote: ${d.note.trim()}` : '');
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
  });

  render();
  const yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
