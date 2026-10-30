# Lorenz Attractor Garden

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A three.js scene where hundreds of particles follow a chaotic system of ODEs (Lorenz, Rössler, Thomas, Aizawa, Halvorsen, Chen–Lee, Dadras) and leave fading glowing trails, tracing the strange attractor. "Butterfly effect" mode starts all particles a millionth apart: they move as one, then suddenly fan out; a log-scale chart shows how fast the spread grows.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Lorenz Attractor Garden (three.js): release hundreds of particles in the Lorenz, Rössler or Thomas systems. Two nearly identical starting points drift apart, which shows the butterfly effect."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- HTML/CSS/JS, three.js r128 + OrbitControls from jsDelivr (same versions as Klotski / Three-Body):
  `https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js`, `.../examples/js/controls/OrbitControls.js`.
- One file: `lorenz.html`. Trails are one `LineSegments` with vertex colours (additive blending); heads are `Points` with a radial-gradient sprite.

## Features implemented
- 7 systems, each with its equations shown and sliders for every parameter (+ reset).
- Release: "Random cloud" (particles across a box, coloured by starting position) or "Butterfly effect" (all particles 10^-gap apart along x, rainbow-coloured, after first running onto the attractor).
- Particles 1–2000, starting gap 1e-9 … 1e-1, speed 0–3×, trail length 2–200, pause, clear trails.
- Colour by starting position / speed / single colour; glowing heads toggle; slow auto-rotation.
- Spread chart (RMS distance from the mean, log scale) in butterfly mode.
- Particles that blow up (e.g. after extreme parameter changes) are respawned in the box.
- HUD with time, particle count and fps; Home button.

## Code map
`lorenz.html`, one IIFE:
- `SYSTEMS`: per system `f(x,y,z,p)`, `dt`, `scale`, `centre`, `params` ([default, min, max]), `eq` text, spawn `box`.
- Scene setup (renderer, camera, OrbitControls, `trails`, `heads`).
- `world()` maps system coords to world (system z is up), `allocate()`, `release(butterfly)`, `rk4()`, `simulate()` (fixed dt, steps per frame from speed), `trackSpread()`, `updateBuffers()` (ring buffer → segments with fading colour), `drawChart()`.
- UI: `buildParams()`, `setSystem()`, sliders; `loop()`.

## Decisions and user preferences
- RK4 with a fixed step per system for stability; the trail stores one point per frame (not per integration step).

## Known issues / not done yet
- Needs internet for the CDN.
- 2000 particles × 200 trail points is heavy on weak machines (all buffers rebuilt each frame on the CPU).
- Only tested in headless Chromium (software GL, ~17 fps there).

## Ideas / planned
- Move integration to the GPU (transform feedback / texture ping-pong) for 100k particles.
- Poincaré section / slice view, Lyapunov exponent estimate.
- User-entered equations.

## Development notes
- Open `lorenz.html` via a local server or directly; requires network for three.js.
