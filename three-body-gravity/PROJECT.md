# Three-Body Gravity

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A single-file web app (`threebody.html`, no build step) that simulates the classic three-body gravity problem in 3D. The user places three glowing bodies (yellow, red, green) in space, gives each its own gravity (mass), position and velocity, then runs the simulation and watches the orbits unfold, each body leaving a fading trail. Dark space background with a starfield.

## Original brief
1. 3D visualisation of the three-body gravity problem.
2. The user can create 3 objects in 3D space and give them custom gravities.
3. A simulation then runs, visualising the paths the objects take.
4. Dark, space-like background.
5. One object glows yellow, one red, one green.
6. All objects leave a short trail while moving.

## Tech
- Plain HTML/CSS/JS in one file. three.js r128 and `OrbitControls` from jsDelivr CDN (same versions as `klotski-state-space`; needs internet).
- Hosted via GitHub Pages from the repo root.

## Features implemented
- Three bodies: yellow, red, green, drawn as a bright core plus two additive glow sprites. Size scales with mass^(1/3).
- Per-body controls: gravity (= mass, 0.1–10), position x/y/z, velocity x/y/z.
- Drag bodies in the 3D view during setup (drag plane is perpendicular to the camera, so rotate the view to move along other axes). Velocity arrows are shown during setup.
- Start / Pause / Resume, Reset (back to the entered initial conditions), Randomize.
- Presets: figure-eight, Lagrange triangle, chaotic dance, heavy sun with two planets, slingshot.
- Global sliders: gravitational constant G (0.2–5), simulation speed (0.1–5×), trail length (10–600 points).
- Options: cancel total momentum at reset (default on, stops the system drifting away), camera follows centre of mass (default off).
- Trails: one point every 0.02 simulated time units (frame-rate independent), additive line with brightness fading to the tail.
- Editing any input while running or paused resets the simulation to the new initial conditions.
- **Home button** fixed at the bottom right (`#home`, links to `../index.html`), as the repo convention requires.
- Orbit camera (rotate, zoom, pan) with damping; dim reference grid at y = −6 for depth.

## Code map
All in `threebody.html`, inside one IIFE:
- Config constants at the top (`SOFTENING`, `TRAIL_DT`, step limits).
- Scene setup: renderer, camera, `OrbitControls`, starfield, grid, `glowTex` (canvas radial gradient).
- `bodies[]`: per-body three.js objects (core, glow sprites, hit sphere, trail line, velocity arrow) plus state (`pos`, `vel`, `acc`, `mass`) and `init` (the initial conditions from the UI).
- UI: cards built in JS into `fields[]`; `readFields` / `writeFields` sync inputs with `init`.
- Physics: `computeAcc` (softened Newtonian gravity), `adaptiveStep` (step size from the closest pair's free-fall time), `stepSim` (kick-drift-kick leapfrog, pushes trail points).
- Trails: ring buffer per body (`pushTrail`), copied oldest to newest into the geometry in `updateTrail`.
- `resetSim`, `syncVisuals`, `presets`, pointer-drag handlers, `frame()` main loop.

## Decisions and user preferences
- "Gravity" of an object is implemented as its mass (the strength of the pull it exerts), plus a global G.
- Glow is done with additive sprites rather than a bloom post-process, to keep to the single CDN script set.
- Trails are sampled in simulated time rather than per frame so their length does not depend on frame rate or speed setting.

## Known issues / not done yet
- Checked only briefly in the in-app browser (default chaos start and the figure-eight preset, no console errors). Not tested on mobile or with very close encounters; very tight passes may still look energy-inexact (softening 0.05, adaptive leapfrog is not strictly symplectic).
- Bodies do not collide or merge; they pass through each other with softening.
- Bodies can fly far away and leave the view; there is no auto-framing.
- The velocity fields show the entered values, not the momentum-corrected ones when "Cancel total momentum" is on.

## Ideas / planned
- Auto-fit camera, or a "reset camera" button.
- Energy / angular momentum readout to show integrator quality.
- Real bloom post-processing, per-body trail colour/length options.
- Shareable URL encoding the initial conditions; save/load custom setups.
- Time reversal, slow-motion on close encounters.

## Development notes
- Run locally with any static server from the repo root, e.g. `python -m http.server`, then open `/three-body-gravity/threebody.html`.
- The figure-eight preset is a good sanity check: it should stay a closed figure-eight for many periods (period about 6.33 time units at G = 1).
