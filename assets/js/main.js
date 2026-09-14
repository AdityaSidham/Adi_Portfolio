/* =====================================================================
   Aditya Sidham — Portfolio interactions
   Vanilla JS. No dependencies.
   ===================================================================== */
(() => {
  "use strict";

  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(pointer: fine)").matches;

  /* ---------- Theme ---------- */
  const root = document.documentElement;
  const applyTheme = (t) => {
    if (t === "dark") root.setAttribute("data-theme", "dark");
    else root.removeAttribute("data-theme");
    $$(".theme-toggle").forEach((b) => b.setAttribute("aria-pressed", String(t === "dark")));
  };
  const storedTheme = (() => { try { return localStorage.getItem("theme"); } catch { return null; } })();
  applyTheme(storedTheme === "dark" ? "dark" : "light");
  $$(".theme-toggle").forEach((btn) =>
    btn.addEventListener("click", () => {
      const next = root.hasAttribute("data-theme") ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem("theme", next); } catch {}
    })
  );

  /* ---------- Page ready (hero choreography) ---------- */
  const ready = () => document.body.classList.add("is-ready");
  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 900))]).then(() =>
      requestAnimationFrame(() => setTimeout(ready, 60))
    );
  } else {
    setTimeout(ready, 120);
  }

  /* ---------- Navigation: hide on scroll down, show on up ---------- */
  const nav = $(".nav");
  const toTop = $(".to-top");
  let lastY = window.scrollY;
  let ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    if (nav) {
      nav.classList.toggle("is-scrolled", y > 24);
      if (!document.body.classList.contains("menu-open")) {
        nav.classList.toggle("is-hidden", y > lastY && y > 160);
      }
    }
    if (toTop) toTop.classList.toggle("is-visible", y > 600);
    lastY = y;
    ticking = false;
  };
  window.addEventListener("scroll", () => {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  const menuToggle = $(".menu-toggle");
  const closeMenu = () => {
    document.body.classList.remove("menu-open");
    menuToggle && menuToggle.setAttribute("aria-expanded", "false");
  };
  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      menuToggle.setAttribute("aria-expanded", String(open));
      if (open && nav) nav.classList.remove("is-hidden");
    });
    $$(".mobile-menu a").forEach((a) => a.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });
  }

  /* ---------- Active section links ---------- */
  const sections = $$("main section[id]");
  const navLinks = $$(".nav-links a[href^='#']");
  if (sections.length && navLinks.length && "IntersectionObserver" in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const id = "#" + en.target.id;
        navLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === id));
      });
    }, { rootMargin: "-40% 0px -55% 0px", threshold: 0 });
    sections.forEach((s) => spy.observe(s));
  }

  /* ---------- Scroll reveal ---------- */
  const revealEls = $$("[data-reveal]");
  if (revealEls.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealEls.forEach((el) => el.classList.add("is-in"));
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      revealEls.forEach((el) => io.observe(el));
    }
  }
  // Staggered groups: children of [data-stagger] get incremental delays
  $$("[data-stagger]").forEach((group) => {
    const step = parseInt(group.dataset.stagger, 10) || 70;
    $$(":scope > [data-reveal]", group).forEach((el, i) => el.style.setProperty("--d", `${i * step}ms`));
  });

  /* ---------- Timeline progress line ---------- */
  const timeline = $(".timeline");
  if (timeline && !reduceMotion) {
    const bar = $(".progress", timeline);
    const update = () => {
      const r = timeline.getBoundingClientRect();
      const vh = window.innerHeight;
      const pct = Math.min(1, Math.max(0, (vh * 0.7 - r.top) / r.height));
      if (bar) bar.style.height = `calc(${(pct * 100).toFixed(2)}% - 16px)`;
    };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---------- Subtle parallax on work media ---------- */
  const parallaxEls = $$("[data-parallax]");
  if (parallaxEls.length && !reduceMotion && finePointer) {
    let raf = false;
    const move = () => {
      const vh = window.innerHeight;
      parallaxEls.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        const p = (r.top + r.height / 2 - vh / 2) / vh; // -0.5 .. 0.5
        const amt = parseFloat(el.dataset.parallax) || 14;
        el.style.setProperty("--py", `${(-p * amt).toFixed(2)}px`);
      });
      raf = false;
    };
    window.addEventListener("scroll", () => { if (!raf) { requestAnimationFrame(move); raf = true; } }, { passive: true });
    move();
  }

  /* ---------- Magnetic buttons ---------- */
  if (finePointer && !reduceMotion) {
    $$("[data-magnetic]").forEach((el) => {
      const strength = parseFloat(el.dataset.magnetic) || 0.25;
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const x = e.clientX - (r.left + r.width / 2);
        const y = e.clientY - (r.top + r.height / 2);
        el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
      });
      el.addEventListener("mouseleave", () => { el.style.transform = ""; });
    });
  }

  /* ---------- Custom cursor ---------- */
  const cursor = $(".cursor");
  if (cursor && finePointer && !reduceMotion) {
    document.body.classList.add("has-cursor");
    let cx = -100, cy = -100, tx = -100, ty = -100;
    window.addEventListener("mousemove", (e) => { tx = e.clientX; ty = e.clientY; cursor.classList.remove("is-hidden"); }, { passive: true });
    document.addEventListener("mouseleave", () => cursor.classList.add("is-hidden"));
    const loop = () => {
      cx += (tx - cx) * 0.22; cy += (ty - cy) * 0.22;
      cursor.style.transform = `translate(${cx}px, ${cy}px) translate(-50%, -50%)`;
      requestAnimationFrame(loop);
    };
    loop();
    const hoverables = "a, button, [role='button'], input, textarea, label, .gallery figure";
    document.addEventListener("mouseover", (e) => { if (e.target.closest(hoverables)) cursor.classList.add("is-link"); });
    document.addEventListener("mouseout", (e) => { if (e.target.closest(hoverables)) cursor.classList.remove("is-link"); });
  }


  /* ---------- Flagship showcase: screen switcher ---------- */
  const tabs = $$(".screen-tabs button");
  const screens = $$(".phone-screen img");
  if (tabs.length && screens.length) {
    const show = (key) => {
      screens.forEach((img) => img.classList.toggle("is-live", img.dataset.screen === key));
      tabs.forEach((b) => {
        const on = b.dataset.target === key;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-selected", String(on));
        b.tabIndex = on ? 0 : -1;
      });
    };
    tabs.forEach((btn) => btn.addEventListener("click", () => show(btn.dataset.target)));
    // roving tabindex: arrow keys move between screens, as a tablist should
    tabs.forEach((btn, i) => {
      btn.tabIndex = i === 0 ? 0 : -1;
      btn.addEventListener("keydown", (e) => {
        const map = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
        if (e.key in map) {
          e.preventDefault();
          const next = tabs[(i + map[e.key] + tabs.length) % tabs.length];
          next.focus();
          show(next.dataset.target);
        } else if (e.key === "Home" || e.key === "End") {
          e.preventDefault();
          const next = e.key === "Home" ? tabs[0] : tabs[tabs.length - 1];
          next.focus();
          show(next.dataset.target);
        }
      });
    });
  }

  /* ---------- Footer clock (Los Angeles) ---------- */
  const clock = $("[data-clock]");
  if (clock) {
    const fmt = new Intl.DateTimeFormat("en-US", { timeZone: "America/Los_Angeles", hour: "2-digit", minute: "2-digit", hour12: true });
    const tick = () => { clock.textContent = `Los Angeles · ${fmt.format(new Date())}`; };
    tick(); setInterval(tick, 30000);
  }
  $$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

  /* ---------- Copy email ---------- */
  $$("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        const original = btn.innerHTML;
        btn.innerHTML = btn.dataset.copied || "Copied";
        setTimeout(() => { btn.innerHTML = original; }, 1600);
      } catch {
        window.location.href = `mailto:${text}`;
      }
    });
  });

  /* ---------- Contact form ---------- */
  const form = $("#contact-form");
  if (form) {
    const status = $(".form-status", form);
    const setError = (field, msg) => {
      const wrap = field.closest(".field");
      if (!wrap) return;
      wrap.classList.toggle("is-invalid", Boolean(msg));
      const err = $(".error", wrap);
      if (err) err.textContent = msg || "";
      field.setAttribute("aria-invalid", msg ? "true" : "false");
    };
    const validate = () => {
      let ok = true;
      $$("[required]", form).forEach((f) => {
        const v = f.value.trim();
        let msg = "";
        if (!v) msg = "This field is required.";
        else if (f.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Enter a valid email address.";
        setError(f, msg);
        if (msg) ok = false;
      });
      return ok;
    };
    $$("[required]", form).forEach((f) => f.addEventListener("input", () => { if (f.closest(".field.is-invalid")) validate(); }));

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!validate()) { $(".is-invalid input, .is-invalid textarea", form)?.focus(); return; }
      if ($(".hp input", form)?.value) return; // honeypot

      const data = new FormData(form);
      const endpoint = form.getAttribute("action") || "";
      const btn = $("button[type=submit]", form);
      const fallbackMail = () => {
        const subject = encodeURIComponent(data.get("subject") || `Message from ${data.get("name")}`);
        const body = encodeURIComponent(`${data.get("message")}\n\n— ${data.get("name")} (${data.get("email")})`);
        window.location.href = `mailto:${form.dataset.mail}?subject=${subject}&body=${body}`;
        status.textContent = "Opening your email app…";
        status.className = "form-status";
      };

      if (!endpoint || endpoint.includes("YOUR_FORM_ID")) { fallbackMail(); return; }

      btn.disabled = true;
      status.textContent = "Sending…"; status.className = "form-status";
      try {
        const res = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error("bad status");
        form.reset();
        status.textContent = "Thanks! Your message is on its way. I'll get back to you soon.";
        status.className = "form-status ok";
      } catch {
        status.textContent = "Couldn't send through the form. Falling back to your email app…";
        status.className = "form-status err";
        setTimeout(fallbackMail, 900);
      } finally {
        btn.disabled = false;
      }
    });
  }

  /* ---------- Project page: gallery lightbox + side nav ---------- */
  const lightbox = $("#lightbox");
  if (lightbox) {
    const img = $("img", lightbox);
    $$(".gallery figure").forEach((fig) => {
      fig.setAttribute("tabindex", "0");
      fig.setAttribute("role", "button");
      const open = () => {
        const src = $("img", fig);
        img.src = src.dataset.full || src.src;
        img.alt = src.alt;
        lightbox.showModal();
      };
      fig.addEventListener("click", open);
      fig.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
    });
    $(".close", lightbox)?.addEventListener("click", () => lightbox.close());
    lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });
  }
  const sideLinks = $$(".project-body .side a[href^='#']");
  if (sideLinks.length && "IntersectionObserver" in window) {
    const targets = sideLinks.map((a) => $(a.getAttribute("href"))).filter(Boolean);
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        sideLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id));
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    targets.forEach((t) => io.observe(t));
  }
})();
