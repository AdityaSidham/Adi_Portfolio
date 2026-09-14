<div align="center">

# Aditya Sidham — Portfolio

**Applied AI, iOS & Backend Engineer**
M.S. Applied Data Science at USC · Los Angeles, California

[**View the live site →**](https://adityasidham.github.io/Adi_Portfolio/)

[![Live](https://img.shields.io/badge/live-adityasidham.github.io-3056D3?style=flat-square)](https://adityasidham.github.io/Adi_Portfolio/)
![Dependencies](https://img.shields.io/badge/dependencies-none-17212B?style=flat-square)
![Build step](https://img.shields.io/badge/build%20step-none-17212B?style=flat-square)
![Accessibility](https://img.shields.io/badge/contrast-WCAG%20AA-1E7A4A?style=flat-square)

</div>

---

## About

A hand-built portfolio for work across applied AI, native iOS, backend systems,
computer vision and IoT. It replaces a Bootstrap template with a site written
from scratch: **no framework, no build step, no runtime dependencies.**

Open `index.html` in a browser and it runs. That is the whole stack.

| | |
|---|---|
| **Runtime dependencies** | None. No Bootstrap, jQuery, Swiper, GLightbox, AOS or icon fonts. |
| **Build step** | None for viewing. A small Python generator renders the case studies. |
| **JavaScript** | ~330 lines of vanilla ES2020, no polyfills. |
| **Icons** | One inline SVG sprite, 32 symbols. |
| **External requests** | Google Fonts, and one Strava embed script. |

---

## What's in it

- **Choreographed hero** — headline lines slide up, the photo clip-reveals, and a
  person detection box locks onto the subject with a `person · SWE 100%` readout.
- **FitandFine showcase** — the flagship iOS project, shown as one large legible
  phone in a device frame with a four-button tablist to switch screens. Click,
  tap, or arrow keys.
- **Six case studies** — FitandFine, FitForm, Chat-DB, SafeSense, Face & Hand
  Recognition, and a gesture-controlled robotic arm. Each has a sticky in-page
  nav, stat row, and a keyboard-accessible lightbox.
- **Experience timeline** — a scroll-linked progress line with official vector
  logos, every mark normalised to the same optical weight.
- **Training section** — a live Strava activity embed instead of a bullet list.
- **Light and dark themes** — persisted to `localStorage`, both meeting WCAG AA.

---

## Design system

Everything is driven by CSS custom properties in
[`assets/css/style.css`](assets/css/style.css). Change a token, change the site.

### Palette

| Role | Light | Dark |
|---|---|---|
| Background | `#F6F7F2` | `#12171D` |
| Raised surface | `#FCFCFA` | `#171D24` |
| Primary text | `#17212B` | `#EDEFEA` |
| Secondary text | `#5A6570` | `#A3ACB4` |
| Accent / links | `#3056D3` | `#8FA8FF` |
| Borders | `#D9DDD8` | `#2A323A` |
| Strava (brand only) | `#FC4C02` | `#FC4C02` |

Strava orange is confined to Strava's own marks, large display type and
decorative rules. It measures **3.16:1** on this background, which passes for
large text but fails as body copy, so it never carries small text.

### Typography

| Role | Face | Scale |
|---|---|---|
| Display | Instrument Serif | `clamp(38px, 4.2vw, 62px)`, line-height 0.95 |
| Body | Manrope | 17–19px, line-height 1.6, ~64ch measure |
| Wordmark | Manrope 800 | Tight tracking, paired with an `AS` mark |
| Labels | JetBrains Mono | 10–13px, uppercase, tracked |

### The art system

Every decorative element comes from one idea: **a vision system looking at
things.** Nothing is ornament for its own sake.

- Landmark constellations that drift slowly in the background
- A person detection box on the hero photo, with corner brackets and a readout
- Viewfinder brackets that open outward on photo hover
- Dot fields behind the hero and case-study heroes
- Oversized outlined section numerals, `01` through `05`
- Node rulers between sections, concentric rings behind the contact block

The rule: **ink at low opacity, plus at most one accent node.** Never more colour
than that.

---

## Structure

```
Adi_Portfolio/
├── index.html                      Home: hero, work, about, experience,
│                                   training, highlights, contact
├── FitandFine.html                 Case study — AI iOS nutrition platform
├── FitForm.html                    Case study — patented CV form coach
├── ChatDB.html                     Case study — natural language to SQL
├── FireandSmokeDetectionPage.html  Case study — SafeSense IoT fire alarm
├── FaceandHanddetection.html       Case study — OpenCV to Arduino
├── RoboticArm.html                 Case study — gesture-controlled arm
│
├── assets/
│   ├── css/style.css               Every style: tokens, components, art, themes
│   ├── js/main.js                  Every interaction, vanilla
│   ├── img/web/                    Optimised images
│   │   └── logos/                  Institution and Strava marks
│   └── resume/                     Aditya_Sidham_Resume.pdf is current
│
└── .build/                         Page generators (see below)
```

---

## Running it

No server required. The site is static files:

```bash
open index.html
```

For a local server, which avoids `file://` quirks:

```bash
python3 -m http.server 8765
```

Then visit **http://localhost:8765**. Stop it with `Ctrl+C`.

---

## Regenerating the case studies

The six case studies share one template, so they are generated rather than
hand-edited. Editing them individually will be overwritten on the next build.

```bash
python3 .build/build_index.py      # renders index.html
python3 .build/build_projects.py   # renders the six case studies
```

| File | Purpose |
|---|---|
| `.build/index_template.html` | Homepage source, with `{{ART_*}}` slots |
| `.build/projects_data.py` | All case-study copy and metadata |
| `.build/build_projects.py` | Page template and renderer |
| `.build/art.py` | Generates the SVG constellations and detection overlay |
| `.build/sprite.html` | Shared inline icon sprite |

To change case-study copy, edit `projects_data.py` and re-run the build.

> **Cache busting.** After editing CSS or JS, bump the `?v=` query on the
> `style.css` and `main.js` links in `.build/index_template.html` and
> `.build/build_projects.py`, then rebuild. Browsers cache aggressively and will
> otherwise serve the old file.

---

## Things worth knowing before you edit

**The hero detection box is computed, not eyeballed.**
`assets/img/web/aditya-la.jpg` is pre-cropped to exactly 4:5 (1104×1380) so it
maps 1:1 onto the frame:

```
x% = sx / 1104        y% = sy / 1380
```

The figure sits at `sx 438–712`, `sy 272–1336`. Swap the photo and you must
recompute those four percentages or the box will not line up.

**Logos are normalised by optical area, not by box.**
Fitting marks of different aspect ratios into one box makes wide wordmarks look
tiny and compact ones look huge. Each logo's height is derived from its own
aspect ratio (`h = K / √aspect`) so all five carry equal visual weight. If you
swap a logo, set its `--logo-h` alongside the others in the stylesheet.

**Never put `overflow-x: hidden` on `body` here.**
It turns the body into its own scroll container, which silently breaks anchor
links and sticky positioning. Use `overflow-x: clip`.

**The Strava embed is pinned to one activity.**
It will not follow new runs. To feature a different one, copy a fresh embed
snippet from Strava and swap the `data-embed-id` and `data-token` in the
template. Without JavaScript the shell falls back to a plain link.

---

## Accessibility

Checked, not assumed:

- Body text meets **WCAG AA (4.5:1)** in both themes; every new colour pair was
  measured rather than eyeballed
- Screen switcher is a real `tablist` with `aria-selected`, roving `tabindex`,
  and arrow, `Home` and `End` key support
- Touch targets are 44px or larger
- Visible focus rings everywhere, never removed
- Every image carries descriptive alt text
- `prefers-reduced-motion` disables the cursor, parallax, marquee and all reveals
- No horizontal scroll at 375px

---

## Contact form

The form posts to [Formspree](https://formspree.io). Replace `YOUR_FORM_ID` in
the form's `action` in `.build/index_template.html`, then rebuild.

Until then, submitting falls back to opening the visitor's email client with the
message pre-filled, so nothing is lost.

---

## Deploying

Static files, served from `main` by GitHub Pages. Push and it ships.

```bash
git add -A && git commit -m "Your message" && git push
```

> Pages is **case-sensitive** even though macOS is not. A link that works
> locally can 404 in production purely from a capital letter. Verify filename
> casing matches your links exactly before pushing.

---

## Legacy

These are unreferenced leftovers from the original Bootstrap template and can be
deleted whenever you like:

`assets/vendor/` · `assets/scss/` · `assets/css/timelinecss.css` ·
`assets/js/Timeline.js` · `forms/` · `blog-single.html` · the older resume PDFs

---

<div align="center">

Designed and built by **Aditya Sidham** in Los Angeles.

[Website](https://adityasidham.github.io/Adi_Portfolio/) ·
[LinkedIn](https://www.linkedin.com/in/adityasidham/) ·
[GitHub](https://github.com/adityasidham) ·
[Strava](https://www.strava.com/athletes/186930143)

</div>
