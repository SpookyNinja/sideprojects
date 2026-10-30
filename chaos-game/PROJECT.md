# Chaos Game & IFS Ferns

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A canvas toy about how random jumping builds fractals. In the "Polygon game" a point repeatedly jumps a fraction of the way towards a randomly chosen corner; the visited spots form a Sierpiński triangle or other fractals depending on the corners, the jump fraction and a rule about which corner may come next. In "IFS fractals" the point is moved by random affine maps (Barnsley fern, dragon curve, maple leaf, …). Millions of points are accumulated into a density image.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Chaos Game & IFS Ferns: pick polygon corners and jump rules, then watch the Sierpiński triangle or Barnsley fern build up from millions of random points."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, no libraries. One file: `chaos.html`.
- Two stacked canvases: `#cv` (density image via `ImageData`) and `#overlay` (corners, step-by-step trace; receives pointer input).
- Accumulators per device pixel: `dens` (hit count) and `hueSumX/Y` (average hue as a vector, so colours mix correctly).

## Features implemented
- Polygon mode: 3–10 corners (regular polygon, draggable corners), optional extra targets (centre, edge midpoints), jump fraction 0.2–0.8 with a "just touching" button (formula in `touching(n)`), corner rules: any / not same twice / not a neighbour / not +1 / not +2 / not the one two jumps ago.
- IFS mode: 9 presets (Barnsley fern, Sierpiński, Maple leaf, Heighway dragon, Lévy C, Spiral, Tree, Crystal, Koch arm); maps listed as `a b c d e f p`; "slowly morph the maps" animates the coefficients (old picture fades).
- Run/pause, clear, points per frame (1 – 200k, log slider), "show the first jumps step by step" (first 40 jumps animated slowly with dashed lines to the chosen corner).
- Colouring: by corner/map chosen, by density (heat), white glow; exposure slider (log tone mapping).
- Save PNG, HUD with point count, Home button.

## Code map
`chaos.html`, one IIFE:
- `IFS` presets, `HUES` per corner/map.
- `resize()`, `clear()`, `makePolygon()`, `touching(n)`, `targets()`, `pickCorner()` (rules), `plot()`.
- `stepPoly(count)`, `fitIfs()` (samples the attractor to find its bounding box), `chooseMap()`, `stepIfs(count)`, `setIfs()`, `showMaps()`.
- `render()` (tone mapping to ImageData), `hsl()`, `drawOverlay()`, `frame()` loop.
- UI wiring at the bottom; corner dragging on the overlay canvas.

## Decisions and user preferences
- Everything accumulates in a per-pixel float buffer and is re-tone-mapped each frame, so exposure changes apply instantly.
- Changing any polygon setting clears the picture (otherwise the old fractal stays mixed in).

## Known issues / not done yet
- Only tested in headless Chromium; touch dragging of corners is implemented but untested on a phone.
- Rendering the whole ImageData every frame is the main cost on very large / high-DPI screens.
- Resizing the window clears the image.

## Ideas / planned
- Edit IFS maps by dragging transformed parallelograms on the canvas.
- More rules (weighted corners, "not the opposite corner"), random rule explorer.
- Fractal flame–style colouring and non-linear variations.

## Development notes
- Open `chaos.html` directly or via `python -m http.server` from the repo root.
