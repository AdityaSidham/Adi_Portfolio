# Design package: "Landmarks" (portfolio revision, Oct 2026)

Built with the 10k-websites skill. Graphics: Runway stills only (Free plan).
Every viewer-facing line below ships verbatim. Numbers are starting points,
validated by the flick test.

## 1. Brand premise

**Landmarks.** A vision model ignores almost everything in a noisy frame and
keeps the few points that matter: 33 of them for a human body. Everything useful
is built on those points. That is how Aditya works on messy problems, and it is
the one idea the page teaches. The hero is a camera that locks onto one landmark
after another, from a city at night to the 33 points of a runner. The career
sections are landmarks too, and the interactive moment lets the visitor run the
detection on Aditya himself.

## 2. Palette (direction now, final values sampled from the approved stills)

```css
:root{
  --canvas:#0D1424;        /* night blue, toward the LA-at-night grade, never black */
  --panel:#141D31;
  --panel-2:#1B2640;
  --accent:#7C93FF;        /* Aditya's #3056D3 brightened for a dark canvas, 6.6:1 */
  --accent-hover:#A0B1FF;
  --accent-muted:rgba(124,147,255,.22);
  --text-secondary:#A3ADC2;
  --text-primary:#ECE9E1;  /* warm off-white, like paper under sodium light */
}
```
City-light orange lives only inside the imagery. The accent appears on the CTA,
focus rings and the detection HUD, nowhere else.

## 3. Type trio

- Display: **Archivo**, width 112 to 125 (expanded), weights 700 and 800. Wide and
  engineered, like a race bib or a spec sheet.
- Body: **Atkinson Hyperlegible Next**, 400 and 600. Built for legibility.
- Mono: **Atkinson Hyperlegible Mono**, 400 and 500, only for detector readouts
  and small machine labels.

## 4. The storyboard (five nested stills, zoom factor 3 per layer)

Each layer is painted so it sits exactly in the center third of the layer before
it. Scroll down pushes the camera in (law 1: down reads as arriving). Generation
runs inside-out (L4 first, each outer layer outpainted around the inner one); the
browser composites the original inner image over the center with a feathered edge.

| Layer | What the visitor sees | Center third (next target) | Detector chip |
|---|---|---|---|
| L0 | Night over Los Angeles from a dark hillside trail, dry brush at the edges, the city grid to the horizon, mountains under deep blue sky | downtown towers | `downtown_la 0.98` |
| L1 | Glass towers at night, mostly dark windows | one warm lit window | `window_21f 0.94` |
| L2 | Through the glass: a dim room, a desk, a phone upright on a stand, screen glowing (no interface, no text) | the glowing screen | `phone 0.97` |
| L3 | Inside the glow: a field of soft blue-white points of light | a cluster of points | `landmarks 33` |
| L4 (rest) | The points connect with thin lines into a runner mid-stride, calm, centered, generous space around it | none, this is the settle | `pose 33/33` |

Boundary moments: L1 to L2 crosses the window glass (a sheen sweeps across and a
short blur beat). L2 to L3 passes into the screen (a soft bloom of light).

## 5. Band map (hero 840vh, scroll range 740vh; validated by the flick test)

Zoom is eased per segment: a slow drift while a band reads, then a push between
bands. The detector chip locks onto the next target just before each push and
grows with it, so the box literally becomes the next frame. That is the signature.

| Band | Range | Layer | Copy (verbatim) | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.14 | L0 | **I'm Aditya Sidham. I build AI that sees.** / Applied AI, iOS and backend engineer in Los Angeles. M.S. Applied Data Science at USC. | word-by-word rise on load |
| 2 | 0.25 to 0.41 | L1 | **Demos are easy. I build the version people use.** / A patent-pending form coach. A four-agent nutrition app. A database you can ask in plain English. | grid snap-align, echoing the window grid |
| 3 | 0.46 to 0.62 | L2 | **One person. The whole stack.** / SwiftUI on the phone, FastAPI and Postgres behind it, Claude agents doing the reasoning. I built every layer of FitandFine myself. | blur-to-sharp, focusing through the glass |
| 4 | 0.67 to 0.82 | L3 | **Find the points that matter.** / A pose model keeps 33 points from a noisy frame. I treat messy problems the same way: find what matters, then build on it. | scatter, characters gather like points |
| 5 | 0.88 to 1.00 | L4 | **Let's build something that holds up.** / Open to full-time roles in AI, iOS and backend, and to early-stage teams building something real. / [Start a conversation] [See the work] | word rise into staged settle |

A quiet "Skip to the work" link sits in the hero for visitors in a hurry.

## 6. Static hero (reduced motion, and short landscape phones)

L0 behind, all copy settled:
**I'm Aditya Sidham. I build AI that sees.**
Applied AI, iOS and backend engineer in Los Angeles. I take products past the demo:
a patent-pending form coach, a four-agent nutrition app, a database you can ask in plain English.
[Start a conversation] [See the work]

Deviation, said out loud: because the hero is stills, not video, phones and
tablets get the zoom journey too (lighter 1280px layers). Only reduced motion and
short landscape phones get the static hero.

## 7. Below the hero (each funnels to #contact, "Start a conversation")

1. **Work.** "Things I've shipped." / Each one started as a practical question.
   Can a camera coach your form? Can someone query a database without knowing SQL?
   Can a nutrition app adjust to what you actually eat? I build the whole loop,
   then fix what breaks when real people use it.
   FitandFine flagship showcase (real screenshots, tabbed phone), then FitForm and
   Chat-DB as large cards, then "Where it started": SafeSense, Face & Hand, Robotic
   Arm as compact rows. Every card leads with what shipped, the role, the number.
2. **About.** "I learn by getting close to the problem." Existing prose and four
   principles. **The interactive moment** lives here: "Hold to scan" on Aditya's
   real photo. Holding builds progress, landmarks appear and link into a pose,
   the box locks with `aditya 0.99 · engineer, runner`, and the facts list lights
   up line by line. Releasing early eases back. Reduced motion shows the final state.
3. **Training.** "Goals you have to earn, one session at a time." Existing copy,
   Strava embed. Runway still: Baldwin Hills stairs at blue hour, one distant runner.
4. **Experience.** "Where I've done the work." Timeline drawn as a trail that
   draws itself on scroll, each role a waypoint.
5. **Highlights.** "Landmarks so far." / A published patent, a solo-built AI
   product, a national finals and a maker award.
6. **Contact.** "Have a hard problem? I'd like to hear it." Backdrop: the L5
   runner constellation, reused. Form keeps the Formspree endpoint with the
   mailto fallback (the Formspree ID is still a placeholder, so today messages
   open the visitor's email app addressed to sidham@usc.edu). Button "Send message",
   success "Message sent. I'll write back soon."

Case-study pages: same system, each gets one Runway atmosphere still in the same
night world as its header backdrop, with the real cover image untouched below.
FitandFine: a kitchen counter at night, a phone glowing beside a meal. FitForm: a
home workout corner lit by a laptop camera, faint pose points in the air. Chat-DB:
server racks dissolving into light. SafeSense: a dark scale-model house, faint
smoke, one red sensor glow. Face & Hand: five LEDs glowing on a breadboard.
Robotic Arm: a servo arm silhouette under one desk lamp.

## 8. Vector layer

Detection HUD brackets and chips (hero, About scan, section marks). Self-drawing
trail in Experience. Constellation overlay for the About scan. One fixed
background layer: grain plus faint drifting points, 60s+ cycle. All honors
reduced motion.

## 9. Engineering list

Canvas zoom renderer reading the source pixels directly, dt-normalized lerp,
a rAF loop that rests when converged and off-screen, delta-gated DOM writes,
band pacing with the flick test, the four-layer legibility system with a
worst-frame audit, the static-hero gate wired live to change listeners,
complete-without-images, and the quality floor from scrub-pipeline.md.

## 10. Copy gate

Every line above ships verbatim. The built pages must pass the Phase 9 gate:
zero em dashes, zero stock words (leverage, seamless, empower, unlock, robust,
actionable, data-driven, solutions), plus the body-copy sweep for AI tells.
The designed triplet in band 2 is a deliberate brand device and stays.
