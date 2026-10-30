# Mandelbrot & Julia Explorer

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A GPU (WebGL 1) fractal explorer. The main view shows the Mandelbrot set; a small inset shows the Julia set for the point *c* under the mouse, so you can see that every point of the Mandelbrot set has its own Julia set. You can swap the two views, pin *c*, zoom in, change colours and jump to well-known places.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations". The assistant proposed a list; the user picked this one (and nine others), each to be built on its own branch.
2. Pitch that was accepted: "Mandelbrot / Julia Explorer: deep-zoom a fractal in a WebGL shader. Hover any point of the Mandelbrot set to see its matching Julia set live beside it."
3. Follow the repo conventions in `AGENTS.md` (own folder, PROJECT.md, entry in `projects.json`, Home button).

## Tech
- Plain HTML/CSS/JS, no libraries, no build step. One file: `fractal.html`.
- Two `<canvas>` elements, each with its own WebGL 1 context running the same fragment shader (uniform `mode` = 0 Mandelbrot, 1 Julia). A third 2D canvas overlays the orbit of *c*.

## Features implemented
- Main view: drag to pan, wheel / pinch to zoom at the cursor, double-click zooms in. `Home` key resets.
- Julia inset (top right) follows the mouse; click (or Space / checkbox) pins *c*. A white ring marks *c* in the Mandelbrot view when pinned.
- "Show Julia as main view" (key J) swaps the views; each view keeps its own camera.
- Smooth (continuous) iteration colouring; 5 palettes (Fire, Ocean, Rainbow, Electric, Greyscale), colour-cycle density, colour shift, animated colour cycling.
- Max iterations slider (50–3000) plus "raise iterations as you zoom" (auto), capped at 4000 in the shader loop.
- Exponent 2–6 (Multibrot sets z^n + c).
- Orbit of *c* (z₀ = 0, z₁ = c, …, up to 80 steps) drawn as a line over the Mandelbrot view: shows why a point escapes or stays bounded.
- 8 bookmarks (Seahorse valley, Elephant valley, Spiral arm, Mini-brot, Triple spiral, Lightning, Douady rabbit, San Marco).
- Position read-out (centre, zoom, iterations, c) and a precision warning.
- Save PNG of the main view. Home button bottom right.

## Code map
All in `fractal.html`, one IIFE:
- `VS`, `FS`: shaders. `pal()` palettes, `cpow()` integer complex power, main loop with smooth count `n + 1 - log(log|z|)/log(power)`.
- `renderer(canvas)`: compiles the program and returns `{draw(opts)}`.
- State: `views.m` / `views.j` cameras `{cx, cy, r}` (r = half height in the complex plane), `swapped`, `pinned`, `c`.
- `opts()` builds uniforms (incl. auto iterations), `render()` draws both views + info text, `drawOrbit()`.
- Interaction: `planeAt()`, pointer handlers (pan, pinch), `zoomAt()`, wheel, bookmarks, keyboard.

## Decisions and user preferences
- Single-precision floats on the GPU: simple and fast, but zoom is limited (~10⁵×). A warning appears when `r < 2e-5`. This was a deliberate scope choice for a first version.

## Known issues / not done yet
- Deep zoom beyond float precision is not implemented (needs double-single emulation or perturbation theory).
- Checked only in headless Chromium (software WebGL); not tested on phones/touch (pinch is implemented but untested).
- Very high iteration counts can be slow on weak GPUs (no progressive rendering).

## Ideas / planned
- Deeper zoom with perturbation (reference orbit computed in JS with doubles / BigInt).
- Shareable URL with position, c and palette.
- Burning Ship and other formulas; 3D "height" rendering of the iteration count.
- Zoom-video recording.

## Development notes
- Open `fractal.html` directly in a browser or serve the repo root with `python -m http.server`.
- Keep the page one folder deep (Home link is `../index.html`).
