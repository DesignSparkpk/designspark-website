(() => {
  const WA = '923005148824';
  const root = document.documentElement;
  const btn = document.getElementById('langBtn');
  const nodes = [...document.querySelectorAll('[data-ur]')];
  nodes.forEach(n => { n.dataset.en = n.innerHTML; });
  const phNodes = [...document.querySelectorAll('[data-ur-placeholder]')];
  phNodes.forEach(n => { n.dataset.enPlaceholder = n.placeholder; });
  let fontLoaded = false;

  function setLang(lang) {
    const ur = lang === 'ur';
    if (ur && !fontLoaded) {
      const l = document.createElement('link');
      l.rel = 'stylesheet';
      l.href = 'https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap';
      document.head.appendChild(l);
      fontLoaded = true;
    }
    nodes.forEach(n => { n.innerHTML = ur ? n.dataset.ur : n.dataset.en; });
    phNodes.forEach(n => { n.placeholder = ur ? n.dataset.urPlaceholder : n.dataset.enPlaceholder; });
    root.lang = ur ? 'ur' : 'en';
    root.dir = ur ? 'rtl' : 'ltr';
    btn.textContent = ur ? 'English' : 'اردو';
    btn.lang = ur ? 'en' : 'ur';
    try { localStorage.setItem('beacon-lang', lang); } catch (e) {}
  }
  btn.addEventListener('click', () => setLang(root.lang === 'ur' ? 'en' : 'ur'));
  try { if (localStorage.getItem('beacon-lang') === 'ur') setLang('ur'); } catch (e) {}

  const menuBtn = document.getElementById('menuBtn');
  const nav = document.getElementById('mainNav');
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
  });

  function waForm(form, build) {
    if (!form) return;
    form.addEventListener('submit', e => {
      e.preventDefault();
      const note = form.querySelector('.note');
      const req = [...form.querySelectorAll('[required]')];
      req.forEach(i => i.setAttribute('aria-invalid', !i.value.trim()));
      const missing = req.filter(i => !i.value.trim());
      if (missing.length) {
        note.textContent = root.lang === 'ur' ? 'براہِ کرم تمام ضروری خانے پُر کریں۔' : 'Please fill in all required fields.';
        missing[0].focus();
        return;
      }
      const d = Object.fromEntries(new FormData(form));
      window.open(`https://wa.me/${WA}?text=${encodeURIComponent(build(d))}`, '_blank', 'noopener');
    });
  }

  waForm(document.getElementById('admForm'), d =>
    `Assalam o Alaikum, I want admission at Beacon Public School & College.
Student: ${d.student}
Parent: ${d.parent}
Phone: ${d.phone}
Class: ${d.cls}
Campus: ${d.campus}` + (d.msg ? `\nQuestion: ${d.msg}` : ''));

  waForm(document.getElementById('contactForm'), d =>
    `Assalam o Alaikum, Beacon Public School & College.
Topic: ${d.topic}
Name: ${d.name}
Phone: ${d.phone}
Message: ${d.message}`);

  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
