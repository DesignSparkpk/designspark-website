(() => {
  const WA = '923362222081';
  const fmt = n => 'Rs ' + n.toLocaleString('en-PK');
  const cart = new Map();
  const $ = s => document.querySelector(s);

  // header becomes solid after the hero
  const header = $('header.site');
  const onScroll = () => header.classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // desktop video wall: only load the side videos on wide screens
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (matchMedia('(min-width: 901px)').matches && !reduce) {
    document.querySelectorAll('video[data-src]').forEach(v => { v.src = v.dataset.src; v.play().catch(() => {}); });
  }

  // respect reduced motion for background videos
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('video[autoplay]').forEach(v => { v.removeAttribute('autoplay'); v.pause(); });
  }

  // deal tabs
  const tabs = [...document.querySelectorAll('[role=tab]')];
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

  // cart
  const toast = $('#toast');
  let toastTimer;
  function say(msg) {
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 1600);
  }
  function add(id, name, price) {
    const line = cart.get(id) || { name, price, qty: 0 };
    line.qty++; cart.set(id, line); render();
    say(`${name} added · ${count()} in order`);
  }
  const count = () => [...cart.values()].reduce((s, l) => s + l.qty, 0);
  const total = () => [...cart.values()].reduce((s, l) => s + l.qty * l.price, 0);

  function render() {
    document.querySelectorAll('[data-count]').forEach(c => c.textContent = count());
    const ul = $('#lines'); ul.innerHTML = '';
    for (const [id, l] of cart) {
      const li = document.createElement('li');
      li.innerHTML = `<span class="nm"></span><span class="pr"></span>
        <span class="qty"><button type="button" aria-label="Remove one">−</button><b></b><button type="button" aria-label="Add one">+</button></span>`;
      li.querySelector('.nm').textContent = l.name;
      li.querySelector('.pr').textContent = fmt(l.qty * l.price);
      li.querySelector('.qty b').textContent = l.qty;
      const [minus, plus] = li.querySelectorAll('button');
      minus.setAttribute('aria-label', `Remove one ${l.name}`);
      plus.setAttribute('aria-label', `Add one ${l.name}`);
      minus.onclick = () => { l.qty--; if (!l.qty) cart.delete(id); render(); };
      plus.onclick = () => { l.qty++; render(); };
      ul.appendChild(li);
    }
    $('#empty').hidden = cart.size > 0;
    $('#total').textContent = fmt(total());
  }

  document.querySelectorAll('[data-add]').forEach(b =>
    b.addEventListener('click', () => add(b.dataset.id, b.dataset.name, +b.dataset.price)));
  document.querySelectorAll('[data-add-size]').forEach(b =>
    b.addEventListener('click', () => {
      const [size, price] = document.querySelector(`input[name="${b.dataset.addSize}"]:checked`).value.split('|');
      add(`${b.dataset.id}-${size}`, `${b.dataset.name} (${size})`, +price);
    }));

  // drawer
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
  document.querySelectorAll('[data-open-cart]').forEach(b => b.addEventListener('click', openCart));
  document.querySelectorAll('[data-close-cart]').forEach(b => b.addEventListener('click', closeCart));
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
