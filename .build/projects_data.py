# -*- coding: utf-8 -*-
"""Case-study content. Imported by build_projects.py after its HEAD/template."""

P = {}

P["FitandFine.html"] = dict(
    title="FitandFine", og="assets/img/web/fitandfine-dashboard.jpg",
    desc="FitandFine is a solo-built iOS nutrition platform with barcode scanning, label OCR, Apple Health data and a four-agent Claude system behind a native SwiftUI app.",
    kicker="Flagship. Applied AI and native iOS.",
    title_html="FitandFine: nutrition tracking that adapts to the person using it.",
    lede="A native iOS platform that combines fast food logging, nutrition-label OCR, Apple Health data and four specialized Claude agents. Instead of handing everyone the same static calorie formula, it compares the plan with real behavior and proposes adjustments the user can review.",
    category="Applied AI, native iOS, backend", stack="Swift, SwiftUI, SwiftData, HealthKit, AVFoundation, FastAPI, PostgreSQL, Redis, Celery, Claude API, OpenCV, Tesseract, AWS S3, Lambda, API Gateway, CloudWatch",
    when="Apr 2026 – now", recognition='<span class="pill">Solo build</span><br>Design, iOS, backend and AI layer',
    cover="assets/img/web/fitandfine-dashboard.jpg", cover_alt="FitandFine dashboard: calorie ring, macro bars and the daily streak", cover_class=" is-phone",
    overview="""<p>Most nutrition apps are good at recording what happened. They are less useful when a routine changes, the initial calorie estimate is wrong, or logging becomes too slow to keep up. <strong>I built FitandFine to close the gap between tracking and adaptation.</strong></p>
<p>The app handles barcode lookup, manual entry, nutrition-label scanning, daily logs, macro trends, weight tracking, and activity and sleep from Apple Health, with an AI coach grounded in the user's own history. Behind the interface, a FastAPI backend coordinates food data, asynchronous OCR, analytics and four specialized Claude agents.</p>
<p>It is the clearest expression of the kind of engineer I want to be: close to the user, comfortable across the stack, and willing to stay with a problem past the demo.</p>""",
    how="""<li><strong>Make the frequent action fast.</strong> Barcode scanning returns a matching food card in under 500 ms against more than 50,000 USDA items. Redis caches repeat lookups; SwiftData keeps previously used foods available offline.</li>
<li><strong>Let AI interpret, not silently decide.</strong> The AI layer can parse a label, explain a weekly pattern, suggest a meal or propose a calorie change. It never moves a goal without confirmation.</li>
<li><strong>Use personal context carefully.</strong> HealthKit supplies steps, active calories and sleep, which the analysis combines with food logs and weight trend rather than treating every day as identical.</li>
<li><strong>Keep long work off the request path.</strong> Celery workers run OCR and the scheduled weekly analysis, so the interface never waits on an unpredictable model call.</li>
<li><strong>Automate the slow pipeline.</strong> The food catalog refresh runs on S3, Lambda and API Gateway and dropped from 25 minutes to 8, with retries, CloudWatch alarms, and unit and integration tests covering 85% of the backend.</li>
<li><strong>Close the loop.</strong> The calorie target re-fits against observed weight trend and activity instead of staying fixed to the formula it started with.</li>""",
    toc_extra='<li><a href="#agents">The four agents</a></li><li><a href="#impact">Results</a></li>',
    extra_sections=None,  # filled in build script
    gallery=None,
    next_href="FitForm.html", next_title="FitForm",
)

P["FitForm.html"] = dict(
    title="FitForm", og="assets/img/web/fitform-cover.jpg",
    desc="FitForm is a patent-pending computer-vision system that counts repetitions and checks exercise form in real time using MediaPipe and OpenCV.",
    kicker="Computer vision. Patent application published.",
    title_html="FitForm: a camera-based coach for exercise form.",
    lede="Pose estimation that counts repetitions and evaluates form while a person trains. It started with a personal question: could the same computer-vision tools used for detection become useful feedback during an ordinary workout?",
    category="Computer vision, health tech", stack="Python, MediaPipe, BlazePose, OpenCV, TensorFlow",
    when="2024", recognition='<span class="pill">Patent application</span><br>No. 202421099595, published 17 Jan 2025, co-applicant',
    cover="assets/img/web/fitform-1.jpg", cover_alt="FitForm interface showing the live webcam feed with per-exercise repetition counters", cover_class="",
    overview="""<p>A repetition counter can tell someone how much they moved, but not whether the movement was safe or effective. <strong>FitForm follows 33 body landmarks from a standard camera, turns them into joint relationships for each exercise, and checks those measurements against form rules while the user trains.</strong></p>
<p>It supports posture-aware counting for movements such as squats, curls and presses. A repetition only counts when the motion completes the required range, so a half-squat or a swinging curl does not inflate the number. The work led to Indian patent application 202421099595, published on 17 January 2025, with me as a co-applicant.</p>""",
    how="""<li><strong>Pose estimation.</strong> MediaPipe's BlazePose returns 33 body landmarks per frame from an ordinary webcam, fast enough to run on CPU.</li>
<li><strong>Joint angles.</strong> Relevant landmark triplets become angles every frame: hip-knee-ankle for squats, shoulder-elbow-wrist for curls.</li>
<li><strong>State machine per exercise.</strong> Angles drive an up/down stage detector, and a rep counts only on a full cycle that stays inside the posture thresholds.</li>
<li><strong>Live correction.</strong> OpenCV overlays the skeleton, stage, angle and counters directly on the video so form can be fixed mid-set.</li>
<li><strong>Steady under real conditions.</strong> Confidence filtering and temporal smoothing keep it at 25 FPS on a laptop CPU and cut false rep counts by 30% across 120 annotated clips, including fast and partly hidden movements.</li>
<li><strong>Session logging.</strong> Counts per exercise are collected with Pandas for review after the workout.</li>""",
    toc_extra='<li><a href="#impact">Results</a></li>',
    extra_sections=None, gallery=None,
    next_href="ChatDB.html", next_title="Chat-DB",
)

P["ChatDB.html"] = dict(
    title="Chat-DB", og="assets/img/web/chatdb-cover.svg?v=20261012",
    desc="Chat-DB translates plain-language questions into reviewable MySQL and MongoDB queries using the Gemini API and Streamlit.",
    kicker="LLM application. Team lead.",
    title_html="Chat-DB: ask the question before you remember the syntax.",
    lede="A Gemini-powered application that turns plain-language questions into reviewable MySQL or MongoDB queries. It cut query-construction time by roughly 60% for people who were not comfortable writing database syntax by hand.",
    category="LLM application, data tooling", stack="Python, Streamlit, Google Gemini API, MySQL, MongoDB, pytest",
    when="Mar – May 2025, USC", recognition='<span class="pill">Team lead</span><br>Four-person graduate project',
    cover="assets/img/web/chatdb-cover.svg?v=20261012", cover_alt="Chat-DB converting an English question into a SQL query with a run button", cover_class="",
    overview="""<p>A person can understand the business question and still get blocked by joins, field names or MongoDB aggregation syntax. <strong>Chat-DB removes that first barrier.</strong> The user connects a database, asks in ordinary language, and gets a query they can review, edit and run.</p>
<p>I led the four-person team, shaped the architecture, managed the delivery plan, and worked with teammates on prompting and API integration. The project also showed us where language models need structure: real schema context, dialect-specific instructions and a human-controlled execution step.</p>""",
    how="""<li><strong>Schema grounding.</strong> On connect, the app reads available tables, collections and fields, then compresses that schema into the model context so Gemini generates against the real database instead of guessing names.</li>
<li><strong>Dialect-aware prompting.</strong> Separate prompt paths handle SQL and MongoDB's aggregation pipeline, because the two engines need different syntax and reasoning.</li>
<li><strong>Review before run.</strong> The generated query appears in an editable block. Nothing executes until the user confirms.</li>
<li><strong>Results and explanation.</strong> After execution the app renders the result table and explains in plain language what the query did.</li>
<li><strong>Guard rails.</strong> Potentially destructive statements are flagged and need an extra confirmation.</li>
<li><strong>Measured, not assumed.</strong> A pytest evaluation suite of 150 labeled questions reached 92% result correctness and caught 12 regressions before release.</li>""",
    toc_extra='<li><a href="#impact">Results</a></li>',
    extra_sections=None, gallery=None,
    next_href="FireandSmokeDetectionPage.html", next_title="SafeSense",
)

P["FireandSmokeDetectionPage.html"] = dict(
    title="SafeSense", og="assets/img/web/fire-smoke-cover.jpg",
    desc="SafeSense is an ESP8266 fire and smoke detection system with local alarms plus GSM and Wi-Fi notifications. CIIA exhibition finalist.",
    kicker="IoT safety system. CIIA finalist.",
    title_html="SafeSense: a fire alarm designed to reach the person who can act.",
    lede="An ESP8266-based fire and smoke detection system that combines a local alarm with GSM and Wi-Fi notifications. I led the four-person team that designed, built and presented the working prototype.",
    category="IoT, embedded systems, safety", stack="ESP8266, NodeMCU, Arduino IDE, GSM, Wi-Fi, Flame sensor, Smoke sensor",
    when="2023", recognition='<span class="pill">CIIA finalist</span><br>Creative Ideas & Innovations in Action',
    cover="assets/img/web/fire-smoke-cover.jpg", cover_alt="Aditya presenting the SafeSense scale-model home at the CIIA exhibition", cover_class="",
    overview="""<p>A conventional alarm is only useful if somebody can hear it. That is no help if you are at work, asleep two rooms away, or the building is empty. <strong>SafeSense detects a potential fire locally and reaches registered contacts remotely, including over GSM when there is no internet.</strong></p>
<p>We installed flame and smoke sensors across a scale model of a home. When readings crossed calibrated thresholds, the NodeMCU raised a local alarm and triggered both remote paths at once. The zoned demonstration model let judges trigger detection live, and the project was selected as a finalist at the Creative Ideas & Innovations in Action exhibition.</p>""",
    how="""<li><strong>Sensing.</strong> An MQ-series smoke sensor and IR flame sensors feed analog and digital signals into the ESP8266.</li>
<li><strong>Thresholding.</strong> Readings are filtered and compared against calibrated thresholds, so cooking smoke does not raise a false alarm.</li>
<li><strong>Dual alert channels.</strong> A GSM module sends SMS to registered numbers while Wi-Fi pushes a parallel notification. Neither path depends on the other.</li>
<li><strong>Local response.</strong> A buzzer and indicator LEDs give an immediate on-site warning.</li>
<li><strong>Zoned demo rig.</strong> A scale model home with separate sensor zones made the behavior testable in front of judges.</li>""",
    toc_extra='<li><a href="#impact">Results</a></li>',
    extra_sections=None, gallery=None,
    next_href="FaceandHanddetection.html", next_title="Face & Hand Recognition",
)

P["FaceandHanddetection.html"] = dict(
    title="Face & Hand Recognition", og="assets/img/web/face-hand-cover.jpg",
    desc="A webcam vision system that detects a face, counts raised fingers and controls LEDs through an Arduino in real time.",
    kicker="Computer vision meets physical computing.",
    title_html="Turning a hand gesture into a physical output.",
    lede="A webcam-based vision system that detects a face, counts raised fingers, and drives LEDs through an Arduino in real time. My first complete sensing-to-actuation loop.",
    category="Computer vision, physical computing", stack="Python, OpenCV, MediaPipe, PyFirmata, Arduino UNO",
    when="November 2021", recognition="College mini-project",
    cover="assets/img/web/face-hand-cover.jpg", cover_alt="Webcam frame with hand landmarks and a face bounding box, wired LEDs in the foreground", cover_class="",
    overview="""<p>This project connected two kinds of computing I had been exploring separately. MediaPipe identifies 21 landmarks on the hand; the Python application compares fingertip and joint positions to work out how many fingers are raised, then passes that count through PyFirmata to an Arduino, which lights the same number of LEDs on a breadboard.</p>
<p>It was a small project, but the loop was complete: <strong>observe the real world, interpret the signal, make a decision, drive a physical response.</strong> That pattern shows up again in everything I have built since, FitForm and FitandFine included.</p>""",
    how="""<li><strong>Hand landmarks.</strong> MediaPipe Hands returns 21 keypoints per hand; comparing fingertip and knuckle positions gives a reliable finger count.</li>
<li><strong>Face detection.</strong> A face model draws a bounding box and confirms a person is present before the system acts.</li>
<li><strong>Serial bridge.</strong> PyFirmata talks to the Arduino UNO over USB, so Python sets digital pins directly with no custom firmware.</li>
<li><strong>Actuation.</strong> Each finger count maps to a pin pattern that lights one to five LEDs in real time.</li>""",
    toc_extra="", extra_sections=None, gallery=None,
    next_href="RoboticArm.html", next_title="Gesture-Controlled Robotic Arm",
)

P["RoboticArm.html"] = dict(
    title="Gesture-Controlled Robotic Arm", og="assets/img/web/robotic-arm-cover.jpg",
    desc="A servo-driven robotic arm built with an Arduino, later extended with gyroscope-based hand-gesture control. SP Robotics Maker of the Month, 2018.",
    kicker="Robotics. Maker of the Month.",
    title_html="The robotic arm that started my habit of building things.",
    lede="A servo-driven arm built with an Arduino, later extended so it mirrors the operator's hand through a gyroscope. It earned SP Robotics' Maker of the Month in September 2018.",
    category="Robotics, electronics", stack="Arduino, C/C++, Servo motors, Servo controller, Gyroscope",
    when="September 2018", recognition='<span class="pill">Maker of the Month</span><br>SP Robotic Works',
    cover="assets/img/web/robotic-arm-cover.jpg", cover_alt="Servo-driven robotic arm built on an Arduino", cover_class=" is-contain",
    overview="""<p>This was the first project that made engineering feel tangible to me. I assembled the arm, wired the servo system and programmed base, shoulder, elbow and gripper movement in the Arduino IDE. <strong>There was nowhere for a mistake to hide.</strong> Weak power delivery, a bad angle or loose wiring showed up immediately as motion that was slow, unstable or completely wrong.</p>
<p>A later version added a gyroscope that read the operator's hand orientation, scaling pitch and roll into servo targets so the arm could mirror gestures. It earned SP Robotics' Maker of the Month, but what stayed with me was the curiosity: I want to know what happens after the software leaves the screen.</p>""",
    how="""<li><strong>Three axes plus grip.</strong> Base, shoulder, elbow and gripper servos each map to an input, giving three dimensions of motion and a controlled grasp.</li>
<li><strong>Clean power.</strong> A dedicated servo controller supplies power and PWM, so the Arduino only has to send target angles.</li>
<li><strong>Smoothing.</strong> Target angles are interpolated across frames, which removes the jerk and reduces mechanical stress.</li>
<li><strong>Gesture mode.</strong> A gyroscope reports hand orientation; pitch and roll scale into servo angles for direct mirroring.</li>""",
    toc_extra="", extra_sections=None, gallery=None,
    next_href="FitandFine.html", next_title="FitandFine",
)
