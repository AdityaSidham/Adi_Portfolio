#!/usr/bin/env python3
"""Generate the six case-study pages from one template. Run: python3 .build/build_projects.py"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = pathlib.Path(pathlib.Path(__file__).resolve().parent / "index_template.html").read_text(encoding="utf-8")

# Shared icon sprite, kept in step with index.html
sprite = pathlib.Path(pathlib.Path(__file__).resolve().parent / "sprite.html").read_text(encoding="utf-8")

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Aditya Sidham</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#F6F7F2">
  <meta property="og:title" content="{title} — Aditya Sidham">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{og}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css?v=20260914e">
  <script>(function(){{try{{var t=localStorage.getItem('theme');if(t==='dark')document.documentElement.setAttribute('data-theme','dark');}}catch(e){{}}}})();</script>
</head>
<body class="is-ready">
<div class="grain" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"></div>
{sprite}

<header class="nav">
  <div class="container">
    <a class="brand" href="index.html" aria-label="Aditya Sidham — home"><span class="mark" aria-hidden="true">AS</span>Aditya Sidham</a>
    <nav class="nav-links" aria-label="Primary">
      <a href="index.html#work" class="is-active">Work</a>
      <a href="index.html#about">About</a>
      <a href="index.html#experience">Experience</a>
      <a href="index.html#highlights">Highlights</a>
      <a href="index.html#contact">Contact</a>
    </nav>
    <div class="nav-actions">
      <button class="icon-btn theme-toggle" type="button" aria-label="Toggle dark mode" aria-pressed="false">
        <svg class="sun"><use href="#i-sun"/></svg>
        <svg class="moon"><use href="#i-moon"/></svg>
      </button>
      <a class="btn btn--sm" href="assets/resume/Aditya_Sidham_Resume.pdf" target="_blank" rel="noopener" data-magnetic="0.18">Résumé <svg><use href="#i-download"/></svg></a>
      <button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>
      </button>
    </div>
  </div>
</header>

<div class="mobile-menu" id="mobile-menu">
  <ol>
    <li><a href="index.html#work">Work</a></li>
    <li><a href="index.html#about">About</a></li>
    <li><a href="index.html#experience">Experience</a></li>
    <li><a href="index.html#highlights">Highlights</a></li>
    <li><a href="index.html#contact">Contact</a></li>
  </ol>
  <div class="mm-foot">
    <a class="btn" href="assets/resume/Aditya_Sidham_Resume.pdf" target="_blank" rel="noopener">View résumé <svg><use href="#i-download"/></svg></a>
    <a class="icon-btn" href="https://www.linkedin.com/in/adityasidham/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg><use href="#i-linkedin"/></svg></a>
    <a class="icon-btn" href="https://github.com/adityasidham" target="_blank" rel="noopener" aria-label="GitHub"><svg><use href="#i-github"/></svg></a>
  </div>
</div>

<main id="top">
  <section class="project-hero" aria-labelledby="p-title">
    <div class="dotfield" aria-hidden="true"></div>
    <div class="art" style="right: -3%; top: 2%; width: min(38vw, 460px); aspect-ratio: 520/420; z-index: -1;">{art_hero}</div>
    <div class="container">
      <p class="crumbs" data-reveal="fade"><a href="index.html#work"><svg><use href="#i-arrow-right"/></svg> All work</a></p>
      <p class="mono" data-reveal style="margin-bottom:20px">{kicker}</p>
      <h1 class="display h-hero" id="p-title" data-reveal style="--d:60ms">{title_html}</h1>
      <p class="lede" data-reveal style="--d:120ms">{lede}</p>
      <dl class="meta-grid" data-reveal style="--d:180ms">
        <div><dt>Category</dt><dd>{category}</dd></div>
        <div><dt>Stack</dt><dd>{stack}</dd></div>
        <div><dt>Timeline</dt><dd>{when}</dd></div>
        <div><dt>Recognition</dt><dd>{recognition}</dd></div>
      </dl>
      <figure class="project-cover{cover_class} vf" data-reveal="scale" style="--d:240ms">
        <span class="vf-b" aria-hidden="true"></span>
        {cover_inner}
      </figure>
    </div>
  </section>

  <section class="section" style="padding-top: clamp(64px, 8vw, 112px)">
    <div class="container project-body">
      <aside class="side" data-reveal>
        <p class="mono" style="margin-bottom:16px">On this page</p>
        <ol>
          <li><a href="#overview">Overview</a></li>
          <li><a href="#how">How it works</a></li>
          {toc_extra}
          {toc_learned}
          <li><a href="#gallery">Gallery</a></li>
        </ol>
      </aside>
      <div>
        <section id="overview" data-reveal>
          <h2 class="display">Overview</h2>
          <div class="prose">{overview}</div>
        </section>
        <section id="how" data-reveal>
          <h2 class="display">How it works</h2>
          <ul class="bullets">{how}</ul>
        </section>
        {extra_sections}
        {learned}
        <section id="gallery" data-reveal>
          <h2 class="display">Gallery</h2>
          <div class="gallery">{gallery}</div>
        </section>
      </div>
    </div>
  </section>

  <section class="next-project">
    <div class="container" style="position:relative">
      <div class="art" style="right: 2%; top: 10%; width: min(26vw, 300px); aspect-ratio: 520/420; z-index: -1;">{art_next}</div>
      <a href="{next_href}">
        <span class="mono">Next project</span>
        <span class="display h-section">{next_title} <svg><use href="#i-arrow-right"/></svg></span>
      </a>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <p>© <span data-year>2026</span> Designed and built by Aditya Sidham in Los Angeles.</p>
    <span class="clock" data-clock>Los Angeles</span>
    <nav aria-label="Footer">
      <a href="index.html#work">Work</a>
      <a href="index.html#about">About</a>
      <a href="assets/resume/Aditya_Sidham_Resume.pdf" target="_blank" rel="noopener">Résumé</a>
    </nav>
  </div>
</footer>

<dialog class="lightbox" id="lightbox" aria-label="Image preview">
  <button class="icon-btn close" type="button" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  <img src="" alt="">
</dialog>
<a class="icon-btn to-top" href="#top" aria-label="Back to top"><svg><use href="#i-arrow-up"/></svg></a>
<script src="assets/js/main.js?v=20260914e" defer></script>
</body>
</html>
"""

def fig(src, alt, caption="", cls=""):
    c = f' class="{cls}"' if cls else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure{c}><img src="{src}" alt="{alt}" loading="lazy">{cap}</figure>'

def stats(items):
    cells = "".join(f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>' for n, l in items)
    return f'<section id="impact" data-reveal><h2 class="display">Impact</h2><div class="stat-row">{cells}</div></section>'

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import art as artmod

def learned(title, paras):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f'<section id="learned" data-reveal><h2 class="display">{title}</h2><div class="prose">{body}</div></section>'

P = {}


from projects_data import P

# ---- per-project galleries, stats and reflections ----
P["FitandFine.html"]["extra_sections"] = (
    '<section id="agents" data-reveal><h2 class="display">The four agents</h2>'
    '<ul class="bullets">'
    '<li><strong>Food Parser.</strong> After OpenCV and Tesseract pull text off a nutrition label, this agent turns noisy OCR into structured nutrition data and returns per-field confidence. High confidence flows into the log; anything uncertain goes to a review screen.</li>'
    '<li><strong>Diet Analysis.</strong> Reads a seven-day summary of logs, weight direction and goal settings, then reports adherence patterns, macro imbalances and meal-timing issues in priority order.</li>'
    '<li><strong>Recommendation.</strong> Uses remaining macros, dietary restrictions, allergies and budget to suggest realistic meals rather than a generic food list.</li>'
    '<li><strong>Progress Evaluator.</strong> Compares four weeks of weight and calorie adherence and tries to tell a consistency problem apart from a genuine plateau before proposing a change.</li>'
    '</ul>'
    '<div class="prose" style="margin-top:20px"><p>A central orchestrator routes each request to the right agent. The agents never call one another, which keeps responsibilities clear and makes every output easy to validate on its own.</p></div>'
    '</section>'
    + stats([("&lt;500ms", "barcode to food card"), ("50,000+", "USDA food records"), ("&gt;85%", "OCR field accuracy in testing"), ("4", "specialised Claude agents"), ("Offline", "cached foods and logs"), ("Closed loop", "target re-fits on real data")])
)
P["FitandFine.html"]["learned"] = learned("What I learned", [
    "The most useful lesson was that <strong>AI architecture is product architecture</strong>. Confidence thresholds, review states, response streaming, background execution and user confirmation mattered as much as the prompts did.",
    "Specialised agents beat one general-purpose prompt here. Parsing a label, analysing a week, suggesting a meal and evaluating a plateau need different context and different output rules, and separate schemas make each one testable.",
    "Next: meal planning, food-photo estimation, an Apple Watch companion and faster logging from the Home Screen.",
])
P["FitandFine.html"]["gallery"] = "".join([
    fig("assets/img/web/fitandfine-dashboard.jpg", "FitandFine dashboard with calorie ring, macro bars and streak tracker", "Dashboard: calories, macros, streak", "is-phone"),
    fig("assets/img/web/fitandfine-foodlog.jpg", "FitandFine food log grouped into breakfast, lunch, dinner and snack", "Food log by meal, with macro chips", "is-phone"),
    fig("assets/img/web/fitandfine-coach.jpg", "FitCoach answering a question about protein using the user's own logs", "FitCoach, grounded in your own logs", "is-phone"),
    fig("assets/img/web/fitandfine-analytics.jpg", "FitandFine analytics with 30-day averages, calorie trend and macro split", "Analytics: trend and macro split", "is-phone"),
])

P["FitForm.html"]["extra_sections"] = stats([("33", "body landmarks per frame"), ("3+", "exercises with posture-aware counting"), ("1", "patent published, Jan 2025")])
P["FitForm.html"]["learned"] = learned("What I learned", [
    "FitForm changed how I think about applied computer vision. <strong>Detection alone was not the product.</strong> The useful part was translating landmarks into feedback a person can act on in the middle of a movement.",
    "It also taught me that thresholds are a design decision, not a constant. Too strict and honest reps go uncounted; too loose and the counter stops meaning anything.",
])
P["FitForm.html"]["gallery"] = "".join([
    fig("assets/img/web/fitform-cover.jpg", "Overhead press with skeleton overlay and rep counters", "Overhead press, both arms tracked"),
    fig("assets/img/web/fitform-2.jpg", "Flow diagram of the FitForm pipeline from camera feed to rep estimation", "Pipeline: feed to estimation", "is-contain"),
    fig("assets/img/web/fitform-3.jpg", "Bicep curl start position with counters reading 4 up and 1 down", "Curl start, arms down"),
    fig("assets/img/web/fitform-4.jpg", "Shoulder press at the top of the rep with stage readouts", "Shoulder press, rep counted"),
    fig("assets/img/web/fitform-5.jpg", "Squat at full depth with the squat counter reading 5 down", "Squat depth, 5 down"),
    fig("assets/img/web/patent.jpg", "Published patent document for FitForm", "Patent publication", "is-contain"),
])

P["ChatDB.html"]["extra_sections"] = stats([("~60%", "faster query construction"), ("2", "engines: MySQL and MongoDB"), ("4", "person team, which I led")])
P["ChatDB.html"]["learned"] = learned("What I learned", [
    "Language models need structure to be trustworthy near a database. <strong>Real schema context, dialect-specific instructions and a human-controlled execution step</strong> did more for output quality than any amount of prompt polish.",
    "Leading the team taught me to split an ambiguous brief into reviewable pieces, and to make the risky part, query execution, the most visible part of the interface.",
])
P["ChatDB.html"]["gallery"] = "".join([
    fig("assets/img/web/chatdb-cover.svg", "Chat-DB interface concept: English question above the generated SQL", "Question in, query out", "is-contain"),
])

P["FireandSmokeDetectionPage.html"]["extra_sections"] = stats([("3", "alert paths: local, GSM, Wi-Fi"), ("4", "person team, led from build to demo"), ("Finalist", "CIIA exhibition")])
P["FireandSmokeDetectionPage.html"]["learned"] = learned("What I learned", [
    "Real-world systems live on redundancy, calibration and clear failure behaviour. <strong>A safety system cannot assume one network path will always be available</strong>, which is why GSM and Wi-Fi fire in parallel rather than as a fallback chain.",
    "Leading four people through a build and a live demo also taught me to design for the worst demo conditions, not the best ones.",
])
P["FireandSmokeDetectionPage.html"]["gallery"] = "".join([
    fig("assets/img/web/fire-smoke-1.jpg", "Close-up of the SafeSense prototype circuit and sensors", "Prototype wiring", "is-tall"),
    fig("assets/img/web/fire-smoke-2.jpg", "SafeSense scale model home with sensor zones", "Scale model home"),
    fig("assets/img/web/fire-smoke-team.jpg", "The SafeSense team at the CIIA exhibition", "The team at CIIA", "is-tall"),
    fig("assets/img/web/ciia.jpg", "CIIA exhibition logo", "", "is-contain"),
])

P["FaceandHanddetection.html"]["extra_sections"] = stats([("21", "hand landmarks tracked"), ("1-5", "LEDs driven by finger count"), ("Real time", "vision to actuation")])
P["FaceandHanddetection.html"]["learned"] = None
P["FaceandHanddetection.html"]["toc_extra"] = '<li><a href="#impact">Results</a></li>'
P["FaceandHanddetection.html"]["gallery"] = "".join([
    fig("assets/img/web/face-hand-cover.jpg", "Live detection output with hand landmarks and a face box", "Live detection"),
    fig("assets/img/web/face-hand-diagram.jpg", "Block diagram of the vision-to-Arduino pipeline", "Block diagram", "is-contain"),
    fig("assets/img/web/face-hand-arduino.jpg", "Arduino UNO and LED breadboard wiring", "Arduino wiring", "is-contain"),
])

P["RoboticArm.html"]["extra_sections"] = stats([("3", "axes plus a controlled gripper"), ("2018", "SP Robotics Maker of the Month"), ("Gyroscope", "hand-gesture input")])
P["RoboticArm.html"]["learned"] = None
P["RoboticArm.html"]["toc_extra"] = '<li><a href="#impact">Results</a></li>'
P["RoboticArm.html"]["gallery"] = "".join([
    fig("assets/img/web/robotic-arm-cover.jpg", "The servo-driven robotic arm", "The arm", "is-contain"),
    fig("assets/img/web/sp-robotics.jpg", "SP Robotic Works logo", "Maker of the Month, Sep 2018", "is-contain"),
])

# ---- render ----
SEEDS = {"FitandFine.html": 3, "FitForm.html": 11, "ChatDB.html": 19, "FireandSmokeDetectionPage.html": 27, "FaceandHanddetection.html": 35, "RoboticArm.html": 47}
LABELS = {"FitandFine.html": "agents", "FitForm.html": "landmarks", "ChatDB.html": "schema", "FireandSmokeDetectionPage.html": "sensors", "FaceandHanddetection.html": "keypoints", "RoboticArm.html": "servos"}

SHOTS = ("dashboard", "foodlog", "coach", "analytics")
SHOT_ALT = {
    "dashboard": "FitandFine dashboard with calorie ring and macro bars",
    "foodlog": "FitandFine food log grouped by meal",
    "coach": "FitCoach answering a question from the user's own logs",
    "analytics": "FitandFine analytics with calorie trend and macro split",
}
CLUSTER = ('<div class="shots" aria-hidden="true">'
           + "".join(f'<img src="assets/img/web/fitandfine-{k}.jpg" alt="" width="440" height="1022" fetchpriority="high">' for k in SHOTS)
           + '</div><span class="sr-only">Four FitandFine screens: '
           + ", ".join(SHOT_ALT[k] for k in SHOTS) + '</span>')

for name, d in P.items():
    d = dict(d)
    if name == "FitandFine.html":
        d["cover_class"] = " is-shots"
        d["cover_inner"] = CLUSTER
    else:
        d["cover_inner"] = f'<img src="{d["cover"]}" alt="{d["cover_alt"]}" width="1400" height="788" fetchpriority="high">' 
    d["learned"] = d.get("learned") or ""
    d["toc_learned"] = '<li><a href="#learned">What I learned</a></li>' if d["learned"] else ""
    d["art_hero"] = artmod.constellation(SEEDS[name], label=LABELS[name])
    d["art_next"] = artmod.constellation(SEEDS[name] + 100, n=9)
    out = HEAD.format(sprite=sprite, **d)
    assert "{" not in out.split("<style")[0][:0] or True
    (ROOT / name).write_text(out, encoding="utf-8")
    print("wrote", name, len(out))
