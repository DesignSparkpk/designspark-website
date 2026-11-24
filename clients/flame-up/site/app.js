(() => {
  const WA = '923362222081';
  const fmt = n => 'Rs ' + n.toLocaleString('en-PK');
  const cart = new Map(); // id -> {name, price, qty}
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];

  // header turns solid after the hero
  const header = $('header.site');
  const onScroll = () => header.classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // background videos: side videos only on wide screens, none with reduced motion
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (matchMedia('(min-width: 901px)').matches && !reduce) {
    $$('video[data-src]').forEach(v => { v.src = v.dataset.src; v.play().catch(() => {}); });
  }
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

  // ---------- cart ----------
  const toast = $('#toast');
  let toastTimer;
  function say(msg) {
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 1500);
  }
  const count = () => [...cart.values()].reduce((s, l) => s + l.qty, 0);
  const total = () => [...cart.values()].reduce((s, l) => s + l.qty * l.price, 0);

  function change(id, name, price, d) {
    const line = cart.get(id) || { name, price, qty: 0 };
    line.qty = Math.max(0, line.qty + d);
    if (line.qty) cart.set(id, line); else cart.delete(id);
    render();
    if (d > 0) say(`${name} added · ${count()} in order`);
  }

  // what each stepper/tap points at
  function itemFor(el) {
    const host = el.closest('[data-item]');
    if (host) return { id: host.dataset.item, name: host.dataset.name, price: +host.dataset.price };
    const pz = el.closest('[data-pizza]');
    if (pz) {
      const [size, price] = pz.querySelector('input[type=radio]:checked').value.split('|');
      return { id: `${pz.dataset.pizza}-${size}`, name: `${pz.dataset.name} (${size})`, price: +price };
    }
    return null;
  }

  document.addEventListener('click', e => {
    const tap = e.target.closest('.tap');
    const act = e.target.closest('[data-act]');
    if (!tap && !(act && act.closest('.stepper'))) return;
    const it = itemFor(tap || act);
    if (!it) return;
    change(it.id, it.name, it.price, act && act.dataset.act === 'dec' ? -1 : 1);
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

  function render() {
    $$('[data-count]').forEach(c => c.textContent = count());
    const ul = $('#lines'); ul.innerHTML = '';
    for (const [id, l] of cart) {
      const li = document.createElement('li');
      li.innerHTML = `<span class="nm"></span><span class="pr"></span>
        <span class="qty"><button type="button">−</button><b></b><button type="button">+</button></span>`;
      li.querySelector('.nm').textContent = l.name;
      li.querySelector('.pr').textContent = fmt(l.qty * l.price);
      li.querySelector('.qty b').textContent = l.qty;
      const [minus, plus] = li.querySelectorAll('button');
      minus.setAttribute('aria-label', `Remove one ${l.name}`);
      plus.setAttribute('aria-label', `Add one ${l.name}`);
      minus.onclick = () => change(id, l.name, l.price, -1);
      plus.onclick = () => change(id, l.name, l.price, 1);
      ul.appendChild(li);
    }
    $('#empty').hidden = cart.size > 0;
    $('#total').textContent = fmt(total());
    renderSteppers();
  }

  // ---------- drawer ----------
  const drawer = $('#cart');
  let lastFocus;
  function openCart() {
    lastFocus = document.activeElement; drawer.hidden = false; document.body.style.overflow = 'hidden';
    drawer.querySelector('.x').focus();
  }
  function closeCart() {
    drawer.hidden = true; document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  $$('[data-open-cart]').forEach(b => b.addEventListener('click', openCart));
  $$('[data-close-cart]').forEach(b => b.addEventListener('click', closeCart));
  drawer.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeCart();
    if (e.key !== 'Tab') return;
    const f = [...drawer.querySelectorAll('button, input, textarea, a[href]')].filter(x => x.offsetParent !== null);
    if (!f.length) return;
    if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
  });

  // order type: address only for delivery
  const form = $('#orderForm');
  const addr = $('#addrWrap');
  function syncAddr() {
    const del = form.otype.value === 'Delivery';
    addr.hidden = !del; addr.querySelector('textarea').required = del;
  }
  form.querySelectorAll('input[name=otype]').forEach(r => r.addEventListener('change', syncAddr));
  syncAddr();

  form.addEventListener('submit', e => {
    e.preventDefault();
    const msg = $('#formmsg');
    if (!cart.size) { msg.textContent = 'Add at least one item first.'; return; }
    const req = [...form.querySelectorAll('[required]')].filter(i => !i.closest('[hidden]'));
    req.forEach(i => i.setAttribute('aria-invalid', !i.value.trim()));
    const missing = req.find(i => !i.value.trim());
    if (missing) { msg.textContent = 'Please fill in your details.'; missing.focus(); return; }
    msg.textContent = '';
    const d = Object.fromEntries(new FormData(form));
    const lines = [...cart.values()].map(l => `• ${l.qty} × ${l.name} = ${fmt(l.qty * l.price)}`).join('\n');
    const text = `Assalam o Alaikum Flame Up! New order:\n${lines}\nTotal: ${fmt(total())}\n\nType: ${d.otype}\nName: ${d.name}\nPhone: ${d.phone}` +
      (d.otype === 'Delivery' ? `\nAddress: ${d.address}` : '') + (d.note ? `\nNote: ${d.note}` : '');
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
  });

  render();
  const yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
