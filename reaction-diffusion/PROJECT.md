# Reaction–Diffusion

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A GPU simulation of the Gray-Scott reaction–diffusion model. Two chemicals spread and react; two numbers (feed rate F and kill rate k) decide whether coral, spots, stripes, mazes or moving "solitons" grow. You paint chemical B with the mouse, pick patterns from presets or from a clickable F–k parameter map, or switch to "map mode" where F and k vary across the canvas.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Reaction–Diffusion (Gray-Scott): coral, spots and stripes grow in a GPU shader. You paint chemicals with the mouse and there's a parameter map for choosing patterns."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, WebGL 2, no libraries. One file: `reaction.html`.
- Two float textures (RGBA32F, or RGBA16F fallback) ping-pong; needs `EXT_color_buffer_float` (or the half-float variant). An error message is shown if missing.
- Simulation shader: 9-point Laplacian, Du = 1.0, Dv = 0.5, dt = 1, wrap-around edges; brush applied inside the shader. Display shader: palette ramp + optional relief lighting from the B gradient.

## Features implemented
- 12 presets (Coral, Mitosis, Spots, Worms, Maze, Fingerprint, Solitons, Waves, Bubbles, Chaos, U-skate, Holes); each reseeds random blobs.
- F and k sliders; parameter map canvas (click/drag to choose, preset dots, dashed saddle-node line k = √F/2 − F, cross for the current point).
- Map mode: F from 0.10 (top) to 0.01 (bottom), k from 0.045 (left) to 0.07 (right) across the canvas.
- Brush: add B / erase (right-click always erases), size 2–60 px. Works while paused (one step per frame while painting).
- Pause, reseed, clear; steps per frame 1–40; resolution full / ½ / ⅓ / ¼ of CSS pixels.
- 5 palettes (Teal coral, Inferno, Ink on paper, Neon, Ice), 3D lighting toggle, Save PNG. HUD; Home button.

## Code map
`reaction.html`, one IIFE:
- `PRESETS`, shader sources `VS`, `SIM`, `SHOW`; `program()` with a lazy uniform-location proxy.
- `makeTargets(data)`, `seedData(kind)`, `resize(keep)`.
- `step(n)`, `draw()`, `frame()`.
- Parameter map: `mapRange`, `drawMap()`, `pickMap()`; pointer input for the brush; UI wiring.

## Decisions and user preferences
- Simulation resolution defaults to ½ of CSS pixels: good balance of detail and speed.
- Resizing the window keeps the simulation if the grid size is unchanged, otherwise reseeds.

## Known issues / not done yet
- Requires WebGL 2 with float render targets (most desktop browsers; some older phones lack it).
- Map mode wraps around at the edges, so opposite edges with different F/k meet.
- Only tested in headless Chromium (SwiftShader).

## Ideas / planned
- Other models (Brusselator, FitzHugh–Nagumo, Turing patterns with anisotropy).
- Image/text as seed ("grow coral from your name"), video export.
- Shareable URL with F, k and palette.

## Development notes
- Open `reaction.html` directly or via `python -m http.server`.
