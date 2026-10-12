/* Hero: a nested zoom through six Runway stills, scrubbed by scroll.
   Each layer is painted to sit inside the one before it. The page draws the
   current layer, its parent and its child on one canvas, so pushing in reads as
   one continuous camera move. No video, no libraries. */
(() => {
  'use strict';
  const hero = document.getElementById('hero');
  if (!hero) return;

  const stage = hero.querySelector('.hero-stage');
  const canvas = hero.querySelector('.hero-canvas');
  const ctx = canvas.getContext('2d');
  const ring = hero.querySelector('.hero-ring circle');
  const readout = hero.querySelector('.hero-readout b');
  const bands = [...hero.querySelectorAll('.band')].map((el, n) => ({
    el, n,
    a: +el.dataset.a, b: +el.dataset.b,
    ramp: el.dataset.ramp ? +el.dataset.ramp : 0,
    op: -1, k: -1,
  }));
  const lastBand = bands.length - 1;

  /* ---------- split each band headline once, with seeded offsets ---------- */
  function rng(seed) {
    let s = seed >>> 0;
    return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
  }
  function split(el, n) {
    const mode = el.dataset.split;
    const band = el.closest('.band');
    const text = el.textContent.trim();
    const r = rng(101 + n * 17);
    const sr = document.createElement('span');
    sr.className = 'sr-only';
    sr.textContent = text;
    el.textContent = '';
    el.appendChild(sr);
    if (mode === 'soft') {
      for (const cls of ['soft', 'sharp']) {
        const s = document.createElement('span');
        s.className = cls; s.setAttribute('aria-hidden', 'true'); s.textContent = text;
        el.appendChild(s);
      }
      return;
    }
    const vis = document.createElement('span');
    vis.setAttribute('aria-hidden', 'true');
    const words = text.split(/\s+/);
    const total = text.replace(/\s/g, '').length;
    const spread = band.dataset.spread ? +band.dataset.spread : .45;
    const grid = band.classList.contains('band--grid');
    let ci = 0;
    words.forEach((word, wi) => {
      const w = document.createElement('span');
      w.className = 'w';
      w.style.setProperty('--th', (wi / words.length * .5).toFixed(3));
      if (mode === 'chars') {
        for (const ch of word) {
          const c = document.createElement('span');
          c.className = 'c'; c.textContent = ch;
          if (grid) {
            c.style.setProperty('--th', (ci / total * spread + r() * .06).toFixed(3));
            c.style.setProperty('--jx', ((r() < .5 ? -1 : 1) * (14 + r() * 26)).toFixed(1) + 'px');
          } else {
            c.style.setProperty('--th', (r() * .55).toFixed(3));
            c.style.setProperty('--jx', ((r() - .5) * 120).toFixed(1) + 'px');
            c.style.setProperty('--jy', ((r() - .5) * 90).toFixed(1) + 'px');
            c.style.setProperty('--jr', ((r() - .5) * 50).toFixed(1) + 'deg');
          }
          w.appendChild(c);
          ci++;
        }
      } else {
        w.textContent = word;
      }
      vis.appendChild(w);
      if (wi < words.length - 1) vis.appendChild(document.createTextNode(' '));
    });
    el.appendChild(vis);
  }
  hero.querySelectorAll('.band [data-split]').forEach(split);

  /* Layer geometry, measured from the generated images (see .build/design-package.md).
     box:  where the child frame sits in this frame (width fraction, center).
     fade: the child fades in over this part of the push (0 = leaving, 1 = arrived).
     lock: the detector box shown while this layer holds, in child-frame units.  */
  const L = window.HERO_LAYERS || [];
  const N = L.length;

  // Scroll progress (0..1) to zoom position (0..N-1). Slow drift while a band
  // reads, a push between bands.
  const KF = window.HERO_KEYFRAMES || [[0, 0], [1, N - 1]];

  const GATES = [
    '(prefers-reduced-motion: reduce)',
    '(orientation: landscape) and (pointer: coarse) and (max-height: 560px)',
  ];

  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const smooth = (e0, e1, x) => {
    const t = clamp((x - e0) / (e1 - e0), 0, 1);
    return t * t * (3 - 2 * t);
  };
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  function zoomAt(p) {
    for (let k = 0; k < KF.length - 1; k++) {
      const [p0, z0] = KF[k], [p1, z1] = KF[k + 1];
      if (p <= p1) {
        const t = clamp((p - p0) / (p1 - p0 || 1), 0, 1);
        return z0 + (z1 - z0) * (z1 - z0 > .4 ? ease(t) : t);
      }
    }
    return KF[KF.length - 1][1];
  }

  /* ---------- geometry ---------- */
  let vw = 0, vh = 0;
  function cover() {
    const s = Math.max(vw / 16, vh / 9);
    const w = 16 * s, h = 9 * s;
    return { x: (vw - w) / 2, y: (vh - h) / 2, w, h };
  }
  function baseRect(i, f, C) {
    const b = L[i].box;
    const wv = Math.pow(b.w, f);
    const t = (1 - wv) / (1 - b.w);
    const cx = .5 + (b.cx - .5) * t, cy = .5 + (b.cy - .5) * t;
    const w = C.w / wv, h = C.h / wv;
    return { x: C.x + C.w / 2 - cx * w, y: C.y + C.h / 2 - cy * h, w, h };
  }
  const childRect = (R, b) => ({
    x: R.x + (b.cx - b.w / 2) * R.w, y: R.y + (b.cy - b.w / 2) * R.h, w: b.w * R.w, h: b.w * R.h,
  });
  // How the child layer enters while the camera pushes from its parent (f = 0..1):
  // it fades in, its soft mask hides the seam, and the mask relaxes to nothing
  // by arrival so the frame we land on is the clean, full image.
  function entry(j, f) {
    const e = L[j].enter || {};
    const fd = e.fade || [0, .5];
    return { a: smooth(fd[0], fd[1], f), solid: smooth(e.solid ?? .75, 1, f), mask: e.mask };
  }

  // Draw only the part of a layer that lands on screen, sampled from the source.
  // Portrait layers hold just the middle of the frame (crop < 1).
  let crop = 1;
  function drawClipped(img, fr, alpha) {
    const r = crop < 1 ? { x: fr.x + (1 - crop) / 2 * fr.w, y: fr.y, w: fr.w * crop, h: fr.h } : fr;
    const x0 = Math.max(0, r.x), y0 = Math.max(0, r.y);
    const x1 = Math.min(vw, r.x + r.w), y1 = Math.min(vh, r.y + r.h);
    if (x1 <= x0 || y1 <= y0) return;
    const iw = img.naturalWidth, ih = img.naturalHeight;
    const sx = (x0 - r.x) / r.w * iw, sy = (y0 - r.y) / r.h * ih;
    const sw = (x1 - x0) / r.w * iw, sh = (y1 - y0) / r.h * ih;
    const c = target2d || ctx;
    c.globalAlpha = alpha;
    c.drawImage(img, sx, sy, sw, sh, x0, y0, x1 - x0, y1 - y0);
    return [x0, y0, x1 - x0, y1 - y0];
  }

  // The child is drawn into an offscreen canvas, masked there, then composited.
  const off = document.createElement('canvas');
  const octx = off.getContext('2d');
  let target2d = null, dprNow = 1;
  function drawMasked(img, fr, alpha, mask, solid) {
    if (!mask || solid >= .999) { drawClipped(img, fr, alpha); return; }
    target2d = octx;
    octx.setTransform(dprNow, 0, 0, dprNow, 0, 0);
    octx.globalCompositeOperation = 'source-over';
    octx.clearRect(0, 0, vw, vh);
    const box = drawClipped(img, fr, 1);
    target2d = null;
    if (!box) return;
    const [x, y, w, h] = box;
    octx.globalCompositeOperation = 'destination-in';
    octx.globalAlpha = 1;
    const edge = `rgba(0,0,0,${solid.toFixed(3)})`;
    if (mask.type === 'ellipse') {
      const cx = fr.x + fr.w / 2, cy = fr.y + fr.h / 2;
      octx.setTransform(dprNow, 0, 0, dprNow * fr.h / fr.w, dprNow * cx, dprNow * cy);
      const g = octx.createRadialGradient(0, 0, 0, 0, 0, fr.w / 2);
      g.addColorStop(0, '#000');
      g.addColorStop(Math.max(0, 1 - mask.f), '#000');
      g.addColorStop(1, edge);
      octx.fillStyle = g;
      const k = fr.w / fr.h;
      octx.fillRect(x - cx, (y - cy) * k, w, h * k);
    } else {
      const fw = mask.f * fr.h;
      const sides = [
        [fr.x, 0, fr.x + fw, 0], [fr.x + fr.w, 0, fr.x + fr.w - fw, 0],
        [0, fr.y, 0, fr.y + fw], [0, fr.y + fr.h, 0, fr.y + fr.h - fw],
      ];
      for (const s of sides) {
        const g = octx.createLinearGradient(...s);
        g.addColorStop(0, edge);
        g.addColorStop(1, '#000');
        octx.fillStyle = g;
        octx.fillRect(x, y, w, h);
      }
    }
    octx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = alpha;
    ctx.drawImage(off, Math.floor(x * dprNow), Math.floor(y * dprNow), Math.ceil(w * dprNow), Math.ceil(h * dprNow),
      Math.floor(x * dprNow) / dprNow, Math.floor(y * dprNow) / dprNow, Math.ceil(w * dprNow) / dprNow, Math.ceil(h * dprNow) / dprNow);
  }

  /* ---------- the detector chip (the signature) ---------- */
  const ACCENT = '124,147,255';
  function drawChip(box, label, a, tighten) {
    if (a < .01 || box.w < 24) return;
    const g = (tighten - 1) * .5;
    const x = box.x - box.w * g, y = box.y - box.h * g;
    const w = box.w * tighten, h = box.h * tighten;
    const len = Math.min(28, Math.min(w, h) * .14);
    ctx.globalAlpha = a;
    ctx.strokeStyle = `rgba(${ACCENT},.95)`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(x, y + len); ctx.lineTo(x, y); ctx.lineTo(x + len, y);
    ctx.moveTo(x + w - len, y); ctx.lineTo(x + w, y); ctx.lineTo(x + w, y + len);
    ctx.moveTo(x + w, y + h - len); ctx.lineTo(x + w, y + h); ctx.lineTo(x + w - len, y + h);
    ctx.moveTo(x + len, y + h); ctx.lineTo(x, y + h); ctx.lineTo(x, y + h - len);
    ctx.stroke();
    ctx.globalAlpha = a * .22;
    ctx.lineWidth = 1;
    ctx.strokeRect(x + .5, y + .5, w - 1, h - 1);
    if (label) {
      ctx.globalAlpha = a;
      ctx.font = '500 12px "Atkinson Hyperlegible Mono", ui-monospace, monospace';
      const tw = ctx.measureText(label).width;
      const px = clamp(x, 10, vw - tw - 28), py = clamp(y - 26, 76, vh - 30);
      ctx.fillStyle = 'rgba(9,14,26,.72)';
      roundRect(px, py, tw + 18, 20, 6); ctx.fill();
      ctx.fillStyle = `rgba(${ACCENT},1)`;
      ctx.fillRect(px + 7, py + 8, 4, 4);
      ctx.fillStyle = 'rgba(236,233,225,.94)';
      ctx.fillText(label, px + 15, py + 14);
    }
  }
  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  const lockRect = (R, lb) => lb
    ? { x: R.x + lb.x * R.w, y: R.y + lb.y * R.h, w: lb.w * R.w, h: lb.h * R.h }
    : R;

  /* ---------- lens moments ---------- */
  function lens(z) {
    for (const m of (window.HERO_LENS || [])) {
      if (z < m.z0 || z > m.z1) continue;
      const t = (z - m.z0) / (m.z1 - m.z0);
      const bell = Math.sin(Math.PI * t);
      if (m.type === 'sheen') {
        const gx = -vw * .6 + t * vw * 2.2;
        const gr = ctx.createLinearGradient(gx, 0, gx + vw * .45, vh);
        gr.addColorStop(0, 'rgba(200,215,255,0)');
        gr.addColorStop(.5, `rgba(200,215,255,${.20 * bell})`);
        gr.addColorStop(1, 'rgba(200,215,255,0)');
        ctx.globalAlpha = 1;
        ctx.fillStyle = gr;
        ctx.fillRect(0, 0, vw, vh);
      } else if (m.type === 'haze') {
        // flying through the warm glow that hangs over the city
        const r = Math.hypot(vw, vh) * .7;
        const gr = ctx.createRadialGradient(vw / 2, vh / 2, 0, vw / 2, vh / 2, r);
        gr.addColorStop(0, `rgba(255,196,140,${.42 * bell})`);
        gr.addColorStop(.5, `rgba(242,166,90,${.24 * bell})`);
        gr.addColorStop(1, `rgba(120,110,140,${.16 * bell})`);
        ctx.globalAlpha = 1;
        ctx.fillStyle = gr;
        ctx.fillRect(0, 0, vw, vh);
      } else if (m.type === 'bloom') {
        const r = Math.hypot(vw, vh) * .6;
        const gr = ctx.createRadialGradient(vw / 2, vh / 2, 0, vw / 2, vh / 2, r);
        gr.addColorStop(0, `rgba(214,226,255,${.62 * bell})`);
        gr.addColorStop(.45, `rgba(150,175,255,${.22 * bell})`);
        gr.addColorStop(1, 'rgba(150,175,255,0)');
        ctx.globalAlpha = 1;
        ctx.fillStyle = gr;
        ctx.fillRect(0, 0, vw, vh);
      }
    }
  }

  /* ---------- frame ---------- */
  const imgs = [];
  let ready = false;
  function draw(z) {
    z = clamp(z, 0, N - 1);
    const i = Math.min(N - 2, Math.floor(z));
    const f = z - i;
    const C = cover();
    const R = [];
    R[i] = baseRect(i, f, C);
    for (let j = i + 1; j < N; j++) R[j] = childRect(R[j - 1], L[j - 1].box);

    // base layer, clean and opaque; then the child entering it
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#0D1424';
    ctx.fillRect(0, 0, vw, vh);
    drawClipped(imgs[i], R[i], 1);
    const e = entry(i + 1, f);
    if (e.a > .002 && R[i + 1].w > vw * .02) drawMasked(imgs[i + 1], R[i + 1], e.a, e.mask, e.solid);
    lens(z);

    // the detector locks onto the next target, then rides the push
    const cur = Math.round(z * 1000) / 1000 >= N - 1 ? N - 1 : i;
    if (cur === N - 1) {
      const a = smooth(N - 1.12, N - 1.01, z);
      drawChip(lockRect(R[N - 1], L[N - 1].lock), L[N - 1].chip, a, 1 + .2 * (1 - a));
    } else {
      const a = smooth(.02, .10, f) * (1 - smooth(.34, .62, f));
      const tight = 1 + .22 * (1 - smooth(.02, .12, f));
      drawChip(lockRect(R[i + 1], L[i].lock), L[i].chip, a, tight);
    }
    ctx.globalAlpha = 1;
  }

  /* ---------- captions ---------- */
  let lastEnd = -1;
  function updateCaptions(p, loadK) {
    // as the journey settles, the bottom of the frame melts into the page below
    const end = smooth(.9, 1, p);
    if (Math.abs(end - lastEnd) > .01 || (end === 1) !== (lastEnd === 1) || (end === 0) !== (lastEnd === 0)) {
      lastEnd = end;
      stage.style.setProperty('--end', end.toFixed(2));
    }
    for (const b of bands) {
      const len = b.b - b.a;
      const f = Math.min(.02, len / 3);
      let op = smooth(b.a, b.a + f, p) * (1 - smooth(b.b - f, b.b, p));
      if (b.n === 0) op = 1 - smooth(b.b - f, b.b, p);
      if (b.n === lastBand) op = smooth(b.a, b.a + f, p);
      let k = clamp((p - b.a) / (b.ramp || Math.min(.025, len * .35)), 0, 1);
      if (b.n === 0) k = Math.max(k, loadK);
      if (Math.abs(op - b.op) > .004 || (op === 0) !== (b.op === 0) || (op === 1) !== (b.op === 1)) {
        b.op = op;
        b.el.style.opacity = op.toFixed(3);
        b.el.style.visibility = op < .004 ? 'hidden' : 'visible';
      }
      if (Math.abs(k - b.k) > .008 || (k === 1 && b.k !== 1) || (k === 0 && b.k !== 0)) {
        b.k = k;
        b.el.style.setProperty('--k', k.toFixed(3));
      }
    }
  }

  // machine readout, about 10 times a second and only when it changes
  let lastLabel = '', lastLabelAt = 0;
  function updateReadout(z, now) {
    if (!readout || now - lastLabelAt < 100) return;
    let m = 1;
    const i = Math.min(N - 2, Math.floor(z)), f = z - i;
    for (let j = 0; j < i; j++) m /= L[j].box.w;
    m /= Math.pow(L[i].box.w, f);
    const s = (m < 10 ? m.toFixed(1) : Math.round(m)) + '×';
    if (s === lastLabel) return;
    lastLabel = s; lastLabelAt = now;
    readout.textContent = s;
  }

  /* ---------- the drive loop (rests when converged) ---------- */
  let target = 0, shown = 0, rafId = null, lastTick = 0, onScreen = true;
  let loadK = 0, loadStart = 0;
  function progress() {
    const r = hero.getBoundingClientRect();
    const range = hero.offsetHeight - window.innerHeight;
    return range > 0 ? clamp(-r.top / range, 0, 1) : 0;
  }
  function tick(now) {
    const dt = Math.min(100, now - (lastTick || now));
    lastTick = now;
    shown += (target - shown) * (1 - Math.pow(1 - .14, dt / 16.667));
    if (loadStart) loadK = smooth(0, 1, (now - loadStart) / 1100);
    const converged = Math.abs(target - shown) < .0004;
    if (converged) shown = target;
    const z = zoomAt(shown);
    if (ready) draw(z);
    updateCaptions(shown, loadK);
    updateReadout(z, now);
    if (converged && (loadK >= 1 || !loadStart)) { rafId = null; lastTick = 0; return; }
    rafId = requestAnimationFrame(tick);
  }
  function kick() {
    if (rafId === null && onScreen) rafId = requestAnimationFrame(tick);
  }
  function onScroll() { target = progress(); kick(); }

  function resize() {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    vw = stage.clientWidth; vh = stage.clientHeight;
    // rotating between portrait and landscape needs the other image set
    if (started && loadedSize && (vh > vw) !== (loadedSize === 'p')) {
      started = false; ready = false; crop = 1;
      stage.classList.remove('is-live');
      loadLayers();
    }
    canvas.width = off.width = Math.round(vw * dpr);
    canvas.height = off.height = Math.round(vh * dpr);
    dprNow = dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingQuality = 'high';
    if (ready) draw(zoomAt(shown));
  }

  /* ---------- loading ---------- */
  let started = false, loadedSize = '';
  function loadLayers() {
    if (started) return;
    started = true;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = stage.clientWidth, h = stage.clientHeight;
    let size;
    if (h > w) { size = 'p'; crop = window.HERO_P_CROP || .5; }
    else size = Math.max(w, h * 16 / 9) * dpr > 1700 ? 'd' : 'm';
    loadedSize = size;
    const set = [];
    let done = 0;
    const setRing = () => ring && ring.style.setProperty('--ld', (126 * (1 - done / N)).toFixed(1));
    setRing();
    const jobs = L.map((layer, j) => new Promise((res, rej) => {
      const im = new Image();
      im.decoding = 'async';
      im.onload = () => (im.decode ? im.decode().catch(() => {}) : Promise.resolve()).then(() => {
        set[j] = im; done++; setRing(); res();
      });
      im.onerror = rej;
      im.src = `assets/img/hero/${layer.name}-${size}.webp?v=${window.HERO_V || 1}`;
    }));
    Promise.all(jobs).then(() => {
      if (loadedSize !== size) return;  // a rotation started a newer load
      set.forEach((im, j) => { imgs[j] = im; });
      ready = true;
      resize();
      stage.classList.add('is-live');
      kick();
    }).catch(() => stage.classList.add('is-failed'));
  }

  /* ---------- static gate, decided live ---------- */
  let on = false;
  function enable() {
    if (on) return; on = true;
    hero.classList.remove('is-static');
    hero.classList.add('is-armed');
    loadLayers();
    addEventListener('scroll', onScroll, { passive: true });
    bands.forEach(b => { b.op = -1; b.k = -1; });
    if (!loadStart) loadStart = performance.now();
    target = shown = progress();
    resize();
    kick();
  }
  function disable() {
    if (!on && hero.classList.contains('is-static')) return;
    on = false;
    hero.classList.add('is-static');
    hero.classList.remove('is-armed');
    stage.style.removeProperty('--end'); lastEnd = -1;
    removeEventListener('scroll', onScroll);
    if (rafId !== null) { cancelAnimationFrame(rafId); rafId = null; }
    bands.forEach(b => { b.el.style.opacity = ''; b.el.style.visibility = ''; b.el.style.setProperty('--k', 1); });
  }
  const MQ = GATES.map(q => matchMedia(q));
  function apply() { MQ.some(m => m.matches) ? disable() : enable(); }
  MQ.forEach(m => m.addEventListener('change', apply));

  new IntersectionObserver(([e]) => {
    onScreen = e.isIntersecting;
    if (onScreen) kick();
  }).observe(hero);
  new ResizeObserver(() => { if (on) resize(); }).observe(stage);

  apply();
})();
