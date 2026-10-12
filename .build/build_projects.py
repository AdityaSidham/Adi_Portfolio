#!/usr/bin/env python3
"""Generate the six case-study pages from one template. Run: python3 .build/build_projects.py"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from build_index import V, SITE, mobile_links  # shared with the homepage

sprite = (HERE / "sprite.html").read_text(encoding="utf-8")

HEAD = """<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Aditya Sidham</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#0D1424">
  <link rel="canonical" href="{site}{name}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Aditya Sidham">
  <meta property="og:title" content="{title} | Aditya Sidham">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{site}{name}">
  <meta property="og:image" content="{site}{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{site}{og}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,700..800&family=Atkinson+Hyperlegible+Mono:wght@400;500&family=Atkinson+Hyperlegible+Next:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css?v={v}">
  <script>document.documentElement.className = 'js';</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="env" aria-hidden="true"><i></i><i></i></div>
{sprite}

<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="index.html" aria-label="Aditya Sidham, home"><span class="mark" aria-hidden="true">AS</span><span class="brand-name">Aditya Sidham</span></a>
    <nav class="nav-links" aria-label="Primary">
      <a href="index.html#work" class="is-active">Work</a>
      <a href="index.html#about">About</a>
      <a href="index.html#experience">Experience</a>
      <a href="index.html#contact">Contact</a>
    </nav>
    <div class="nav-actions">
      <a class="btn btn--ghost btn--sm" href="assets/resume/Aditya_Sidham_Resume.pdf" target="_blank" rel="noopener">Résumé <svg aria-hidden="true"><use href="#i-download"/></svg></a>
      <button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <span class="bars" aria-hidden="true"><i></i><i></i></span>
      </button>
    </div>
  </div>
</header>

<div class="mobile-menu" id="mobile-menu">
  <nav aria-label="Mobile">
    {mobile}
  </nav>
  <div class="mm-foot">
    <a class="btn" href="assets/resume/Aditya_Sidham_Resume.pdf" target="_blank" rel="noopener">Open my résumé <svg aria-hidden="true"><use href="#i-download"/></svg></a>
    <a class="icon-btn" href="https://www.linkedin.com/in/adityasidham/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg aria-hidden="true"><use href="#i-linkedin"/></svg></a>
    <a class="icon-btn" href="https://github.com/adityasidham" target="_blank" rel="noopener" aria-label="GitHub"><svg aria-hidden="true"><use href="#i-github"/></svg></a>
  </div>
</div>

<main id="main" tabindex="-1">
  <section class="p-hero" aria-labelledby="p-title">
    <div class="p-hero-media" aria-hidden="true"><img src="assets/img/web/{atmo}" alt="" width="1920" height="1072" fetchpriority="high"></div>
    <div class="wrap">
      <p class="crumbs"><a href="index.html#work"><svg aria-hidden="true"><use href="#i-arrow-right"/></svg> All work</a></p>
      <p class="p-kicker">{kicker}</p>
      <h1 class="p-title" id="p-title">{title_html}</h1>
      <p class="p-lede">{lede}</p>
      <dl class="meta-grid">
        <div><dt>Category</dt><dd>{category}</dd></div>
        <div><dt>Stack</dt><dd>{stack}</dd></div>
        <div><dt>Timeline</dt><dd>{when}</dd></div>
        <div><dt>Recognition</dt><dd>{recognition}</dd></div>
      </dl>
      <figure class="p-cover{cover_class}">{cover_inner}</figure>
    </div>
  </section>

  <div class="wrap p-body">
    <aside class="p-side">
      <p>On this page</p>
      <ol>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#how">How it works</a></li>
        {toc_extra}
        {toc_learned}
        <li><a href="#gallery">Gallery</a></li>
      </ol>
    </aside>
    <div class="p-main">
      <section id="overview" data-reveal>
        <h2>Overview</h2>
        <div class="prose">{overview}</div>
      </section>
      <section id="how" data-reveal>
        <h2>How it works</h2>
        <ul class="bullets">{how}</ul>
      </section>
      {extra_sections}
      {learned}
      <section id="gallery" data-reveal>
        <h2>Gallery</h2>
        <div class="gallery">{gallery}</div>
      </section>
    </div>
  </div>

  <section class="next-project">
    <div class="wrap">
      <a href="{next_href}">
        <span>Next project</span>
        <span class="next-title">{next_title} <svg aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
      </a>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="wrap footer-inner">
    <p>© <span data-year>2026</span> Designed and built by Aditya Sidham in Los Angeles. Photos and screenshots are real. Scene imagery made with Runway.</p>
    <span class="clock chip" data-clock>Los Angeles</span>
    <nav aria-label="Footer">
      <a href="index.html#work">Work</a>
      <a href="index.html#about">About</a>
      <a href="assets/resume/Aditya_Sidham_Resume.pdf" target="_blank" rel="noopener">Résumé</a>
    </nav>
  </div>
</footer>

<dialog class="lightbox" id="lightbox" aria-label="Image preview">
  <button class="icon-btn close" type="button" aria-label="Close"><svg viewBox="0 0 24 24" stroke-width="1.75" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  <img src="" alt="">
</dialog>
<script src="assets/js/main.js?v={v}" defer></script>
</body>
</html>
"""


def fig(src, alt, caption="", cls=""):
    c = f' class="{cls}"' if cls else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure{c}><img src="{src}" alt="{alt}" loading="lazy">{cap}</figure>'


def stats(items):
    cells = "".join(f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>' for n, l in items)
    return f'<section id="impact" data-reveal><h2>Results</h2><div class="stat-row">{cells}</div></section>'


def learned(title, paras):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f'<section id="learned" data-reveal><h2>{title}</h2><div class="prose">{body}</div></section>'


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
    + stats([("&lt;500ms", "barcode to food card"), ("50,000+", "USDA food records"), ("&gt;85%", "label-field accuracy in testing"), ("4", "specialized Claude agents"), ("25 → 8 min", "catalog refresh on AWS Lambda"), ("85%", "backend test coverage")])
)
P["FitandFine.html"]["learned"] = learned("What I learned", [
    "The most useful lesson was that <strong>AI architecture is product architecture</strong>. Confidence thresholds, review states, response streaming, background execution and user confirmation mattered as much as the prompts did.",
    "Specialized agents beat one general-purpose prompt here. Parsing a label, analyzing a week, suggesting a meal and evaluating a plateau need different context and different output rules, and separate schemas make each one testable.",
    "Next: meal planning, food-photo estimation, an Apple Watch companion and faster logging from the Home Screen.",
])
P["FitandFine.html"]["gallery"] = "".join([
    fig("assets/img/web/fitandfine-dashboard.jpg", "FitandFine dashboard with calorie ring, macro bars and streak tracker", "Dashboard: calories, macros, streak", "is-phone"),
    fig("assets/img/web/fitandfine-foodlog.jpg", "FitandFine food log grouped into breakfast, lunch, dinner and snack", "Food log by meal, with macro chips", "is-phone"),
    fig("assets/img/web/fitandfine-coach.jpg", "FitCoach answering a question about protein using the user's own logs", "FitCoach, grounded in your own logs", "is-phone"),
    fig("assets/img/web/fitandfine-analytics.jpg", "FitandFine analytics with 30-day averages, calorie trend and macro split", "Analytics: trend and macro split", "is-phone"),
])

P["FitForm.html"]["extra_sections"] = stats([("33", "body landmarks per frame"), ("25 FPS", "on a laptop CPU"), ("−30%", "false rep counts across 120 annotated clips")])
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
    fig("assets/img/web/patent.jpg", "Published patent application document for FitForm", "Published patent application", "is-contain"),
])

P["ChatDB.html"]["extra_sections"] = stats([("~60%", "faster query construction"), ("92%", "correct on 150 labeled test questions"), ("12", "regressions caught before release")])
P["ChatDB.html"]["learned"] = learned("What I learned", [
    "Language models need structure to be trustworthy near a database. <strong>Real schema context, dialect-specific instructions and a human-controlled execution step</strong> did more for output quality than any amount of prompt polish.",
    "Leading the team taught me to split an ambiguous brief into reviewable pieces, and to make the risky part, query execution, the most visible part of the interface.",
])
P["ChatDB.html"]["gallery"] = "".join([
    fig("assets/img/web/chatdb-cover.svg?v=20261012", "Chat-DB interface concept: English question above the generated SQL", "Question in, query out", "is-wide"),
])

P["FireandSmokeDetectionPage.html"]["extra_sections"] = stats([("3", "alert paths: local, GSM, Wi-Fi"), ("4", "person team, led from build to demo"), ("Finalist", "CIIA exhibition")])
P["FireandSmokeDetectionPage.html"]["learned"] = learned("What I learned", [
    "Real-world systems live on redundancy, calibration and clear failure behavior. <strong>A safety system cannot assume one network path will always be available</strong>, which is why GSM and Wi-Fi fire in parallel rather than as a fallback chain.",
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
# One Runway still per project, in the hero's night world (header backdrop only;
# the real screenshots and photos below stay untouched).
ATMO = {
    "FitandFine.html": "atmo-fitandfine.jpg", "FitForm.html": "atmo-fitform.jpg",
    "ChatDB.html": "atmo-chatdb.jpg", "FireandSmokeDetectionPage.html": "atmo-safesense.jpg",
    "FaceandHanddetection.html": "atmo-facehand.jpg", "RoboticArm.html": "atmo-roboticarm.jpg",
}

SHOTS = ("dashboard", "foodlog", "coach", "analytics")
SHOT_ALT = {
    "dashboard": "FitandFine dashboard with calorie ring and macro bars",
    "foodlog": "FitandFine food log grouped by meal",
    "coach": "FitCoach answering a question from the user's own logs",
    "analytics": "FitandFine analytics with calorie trend and macro split",
}
CLUSTER = ("".join(f'<img src="assets/img/web/fitandfine-{k}.jpg" alt="" width="440" height="1022" fetchpriority="high">' for k in SHOTS)
           + '<span class="sr-only">Four FitandFine screens: ' + ", ".join(SHOT_ALT[k] for k in SHOTS) + '</span>')

for name, d in P.items():
    d = dict(d)
    if name == "FitandFine.html":
        d["cover_class"] = " is-shots"
        d["cover_inner"] = CLUSTER
    else:
        d["cover_inner"] = f'<img src="{d["cover"]}" alt="{d["cover_alt"]}" width="1400" height="788" fetchpriority="high">'
    d["learned"] = d.get("learned") or ""
    d["toc_learned"] = '<li><a href="#learned">What I learned</a></li>' if d["learned"] else ""
    d["og"] = "assets/img/og/og-" + ATMO[name][len("atmo-"):]  # social card, see .build/og_cards.py
    out = HEAD.format(sprite=sprite, site=SITE, name=name, v=V, atmo=ATMO[name], mobile=mobile_links("index.html"), **d)
    assert "—" not in out, name
    (ROOT / name).write_text(out, encoding="utf-8")
    print("wrote", name, len(out))
