/* =====================================================================
   Aditya Sidham, portfolio interactions. Vanilla JS, no dependencies.
   The hero zoom lives in hero.js.
   ===================================================================== */
(() => {
  'use strict';

  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const reduceMQ = matchMedia('(prefers-reduced-motion: reduce)');
  let reduce = reduceMQ.matches;

  /* ---------- nav: solid after the first scroll, hides going down ---------- */
  const nav = $('.nav');
  let lastY = scrollY, ticking = false;
  function onScroll() {
    const y = scrollY;
    if (nav) {
      nav.classList.toggle('is-scrolled', y > 24);
      if (!document.body.classList.contains('menu-open')) nav.classList.toggle('is-hidden', y > lastY && y > 200);
    }
    lastY = y;
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  const menuToggle = $('.menu-toggle');
  const closeMenu = () => {
    document.body.classList.remove('menu-open');
    menuToggle && menuToggle.setAttribute('aria-expanded', 'false');
  };
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open && nav) nav.classList.remove('is-hidden');
    });
    $$('.mobile-menu a').forEach(a => a.addEventListener('click', closeMenu));
    addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  }

  /* ---------- active section in the nav ---------- */
  const navLinks = $$(".nav-links a[href^='#']");
  if (navLinks.length) {
    const spy = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        navLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    $$('main section[id]').forEach(s => spy.observe(s));
  }

  /* ---------- reveals ---------- */
  const revealEls = $$('[data-reveal]');
  const showAll = () => revealEls.forEach(el => el.classList.add('is-in'));
  if (reduce) showAll();
  else {
    // Headings start fully clipped, which never counts as intersecting, so watch their container.
    const watch = new Map();
    revealEls.forEach(el => {
      const t = el.matches('.h2') ? el.parentElement : el;
      watch.set(t, [...(watch.get(t) || []), el]);
    });
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        watch.get(en.target).forEach(el => el.classList.add('is-in'));
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0 });
    watch.forEach((_, t) => io.observe(t));
  }

  /* ---------- scroll-driven bits: the trail draws, training image drifts ---------- */
  const trail = $('[data-trail]');
  const stops = trail ? $$('.stop', trail) : [];
  const trainImg = $('.training-media img');
  let drawLast = -1;
  function scrollDrives() {
    const vh = innerHeight;
    if (trail) {
      const r = trail.getBoundingClientRect();
      const d = reduce ? 1 : Math.min(1, Math.max(0, (vh * .62 - r.top) / r.height));
      if (Math.abs(d - drawLast) > .002) {
        drawLast = d;
        trail.style.setProperty('--draw', d.toFixed(4));
        stops.forEach(s => s.classList.toggle('is-passed', reduce || s.offsetTop <= d * r.height + 8));
      }
    }
    if (trainImg && !reduce) {
      const r = trainImg.parentElement.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh) {
        const p = (r.top + r.height / 2 - vh / 2) / vh;
        trainImg.style.setProperty('--py', (p * -40).toFixed(1) + 'px');
      }
    }
  }
  let driveTick = false;
  addEventListener('scroll', () => { if (!driveTick) { driveTick = true; requestAnimationFrame(() => { scrollDrives(); driveTick = false; }); } }, { passive: true });
  addEventListener('resize', scrollDrives);
  scrollDrives();

  /* ---------- the one interactive moment: hold to scan ---------- */
  const scan = $('[data-scan]');
  const facts = $('[data-facts]');
  let pinScan = () => {};
  if (scan) {
    const btn = $('.scan-btn', scan);
    const label = $('.scan-label', scan);
    const status = $('.scan-status', scan);
    $$('li', facts).forEach((li, i) => li.style.setProperty('--i', i));
    let v = 0, holding = false, done = false, raf = null, last = 0;
    const HOLD_MS = 1500, RELEASE_MS = 900;
    const paint = () => scan.style.setProperty('--scan', v.toFixed(3));
    function finish() {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
      done = true; holding = false; v = 1; paint();
      scan.style.setProperty('--done', 1);
      facts && facts.classList.add('is-lit');
      btn.classList.remove('is-holding');
      label.textContent = 'Scanned';
      status.textContent = '33 landmarks found. One engineer, also a runner.';
    }
    function loop(now) {
      const dt = Math.min(64, now - (last || now));
      last = now;
      if (holding) v = Math.min(1, v + dt / HOLD_MS);
      else v = Math.max(0, v - dt / RELEASE_MS);
      paint();
      if (v >= 1) { raf = null; last = 0; finish(); return; }
      if (!holding && v <= 0) { raf = null; last = 0; return; }
      raf = requestAnimationFrame(loop);
    }
    const start = e => {
      if (done) return;
      if (e && e.type === 'pointerdown') { try { btn.setPointerCapture(e.pointerId); } catch {} }
      if (reduce) { finish(); return; }
      holding = true;
      btn.classList.add('is-holding');
      status.textContent = 'Scanning…';
      if (!raf) raf = requestAnimationFrame(loop);
    };
    const stop = () => {
      if (done || !holding) return;
      holding = false;
      btn.classList.remove('is-holding');
      status.textContent = v > .02 ? 'Keep holding to finish the scan.' : '';
      if (!raf) raf = requestAnimationFrame(loop);
    };
    btn.addEventListener('pointerdown', start);
    btn.addEventListener('pointerup', stop);
    btn.addEventListener('pointercancel', stop);
    btn.addEventListener('lostpointercapture', stop);
    btn.addEventListener('contextmenu', e => e.preventDefault());
    btn.addEventListener('keydown', e => {
      if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); start(); }
    });
    btn.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') stop(); });
    btn.addEventListener('blur', stop);
    pinScan = () => { if (!done) finish(); };
  }

  /* ---------- live reduced-motion flips: pin final states, or let drives run again ---------- */
  reduceMQ.addEventListener('change', e => {
    reduce = e.matches;
    if (reduce) { showAll(); pinScan(); }
    drawLast = -1;
    scrollDrives();
  });

  /* ---------- FitandFine screens (a real tablist) ---------- */
  const tabs = $$('.screen-tabs button');
  const screens = $$('.phone-screen img');
  const panel = $('.phone-screen');
  if (tabs.length && screens.length) {
    const show = key => {
      screens.forEach(img => img.classList.toggle('is-live', img.dataset.screen === key));
      tabs.forEach(b => {
        const on = b.dataset.target === key;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-selected', String(on));
        b.tabIndex = on ? 0 : -1;
        if (on && panel) panel.setAttribute('aria-labelledby', b.id);
      });
    };
    tabs.forEach((btn, i) => {
      btn.tabIndex = i === 0 ? 0 : -1;
      btn.addEventListener('click', () => show(btn.dataset.target));
      btn.addEventListener('keydown', e => {
        const map = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
        let next = null;
        if (e.key in map) next = tabs[(i + map[e.key] + tabs.length) % tabs.length];
        else if (e.key === 'Home') next = tabs[0];
        else if (e.key === 'End') next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); next.focus(); show(next.dataset.target); }
      });
    });
  }

  /* ---------- footer clock, year ---------- */
  const clock = $('[data-clock]');
  if (clock) {
    const fmt = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', hour: 'numeric', minute: '2-digit' });
    const tick = () => { clock.textContent = `los_angeles ${fmt.format(new Date()).toLowerCase()}`; };
    tick(); setInterval(tick, 30000);
  }
  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ---------- copy email ---------- */
  $$('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        const original = btn.textContent;
        btn.textContent = btn.dataset.copied || 'Copied';
        setTimeout(() => { btn.textContent = original; }, 1600);
      } catch {
        location.href = `mailto:${text}`;
      }
    });
  });

  /* ---------- contact form ---------- */
  const form = $('#contact-form');
  if (form) {
    const status = $('.form-status', form);
    const setError = (field, msg) => {
      const wrap = field.closest('.field');
      wrap.classList.toggle('is-invalid', Boolean(msg));
      $('.error', wrap).textContent = msg || '';
      field.setAttribute('aria-invalid', msg ? 'true' : 'false');
    };
    const validate = () => {
      let ok = true;
      $$('[required]', form).forEach(f => {
        const v = f.value.trim();
        let msg = '';
        if (!v) msg = f.id === 'f-email' ? 'Add your email so I can reply.' : f.id === 'f-name' ? 'Add your name.' : 'Write a short message.';
        else if (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = 'That email looks incomplete. Check it and try again.';
        setError(f, msg);
        if (msg) ok = false;
      });
      return ok;
    };
    $$('[required]', form).forEach(f => f.addEventListener('input', () => { if (f.closest('.field.is-invalid')) validate(); }));

    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!validate()) { $('.is-invalid input, .is-invalid textarea', form)?.focus(); return; }
      if ($('.hp input', form)?.value) return;
      const data = new FormData(form);
      const endpoint = form.getAttribute('action') || '';
      const btn = $('button[type=submit]', form);
      const viaMail = () => {
        const subject = encodeURIComponent(data.get('subject') || `Hello from ${data.get('name')}`);
        const body = encodeURIComponent(`${data.get('message')}\n\n${data.get('name')} (${data.get('email')})`);
        location.href = `mailto:${form.dataset.mail}?subject=${subject}&body=${body}`;
        status.textContent = 'Your email app is opening with the message ready to send.';
        status.className = 'form-status';
      };
      if (!endpoint || endpoint.includes('YOUR_FORM_ID')) { viaMail(); return; }
      btn.disabled = true;
      status.textContent = 'Sending…'; status.className = 'form-status';
      try {
        const res = await fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error('bad status');
        form.reset();
        status.textContent = "Message sent. I'll write back soon.";
        status.className = 'form-status ok';
      } catch {
        status.textContent = "The form couldn't send it, so your email app will open instead.";
        status.className = 'form-status err';
        setTimeout(viaMail, 900);
      } finally {
        btn.disabled = false;
      }
    });
  }

  /* ---------- case studies: gallery lightbox and side nav ---------- */
  const lightbox = $('#lightbox');
  if (lightbox) {
    const img = $('img', lightbox);
    $$('.gallery figure').forEach(fig => {
      fig.tabIndex = 0;
      fig.setAttribute('role', 'button');
      fig.setAttribute('aria-label', 'Open larger: ' + ($('img', fig)?.alt || 'image'));
      const open = () => {
        const src = $('img', fig);
        img.src = src.currentSrc || src.src;
        img.alt = src.alt;
        lightbox.showModal();
      };
      fig.addEventListener('click', open);
      fig.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
    $('.close', lightbox)?.addEventListener('click', () => lightbox.close());
    lightbox.addEventListener('click', e => { if (e.target === lightbox) lightbox.close(); });
  }
  const sideLinks = $$(".p-side a[href^='#']");
  if (sideLinks.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        sideLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    sideLinks.map(a => $(a.getAttribute('href'))).filter(Boolean).forEach(t => io.observe(t));
  }

  /* ---------- pause every loop while the tab is hidden ---------- */
  document.addEventListener('visibilitychange', () => document.body.classList.toggle('paused', document.hidden));
})();
