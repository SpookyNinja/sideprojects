# Graph & Map Colouring

Handoff document: everything a new chat/session needs to continue this project.

## What it is
Colour a map (or any graph) so that no two neighbours share a colour, and watch a backtracking solver do it step by step: it tries a colour, detects clashes (red dashed edge), backs up, and optionally looks ahead (forward checking). Random maps are drawn as Voronoi "countries" on an island; you can also draw your own graph.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Graph Coloring / Map Coloring: draw a planar graph and watch a backtracking solver colour it, showing every backtrack."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, no libraries. One file: `coloring.html`.
- Map: random sites inside a wobbly island shape, rasterised Voronoi regions (`regionOwner`, one cell per 2–4 device px) on an offscreen canvas; graph edges = regions whose pixels touch (≥ 3 border pixels), so the graph matches what you see.
- Solver: recursive generator that yields after every try / assignment / backtrack.

## Features implemented
- Random map (6–120 regions), random planar graph (shortest non-crossing edges first), empty canvas.
- Drawing: click empty space = new vertex, drag vertex→vertex = edge (rejected if it crosses another edge while "planar only" is on), right-click = delete vertex or edge.
- Solver options: number of colours (1–8), vertex order (creation order = top to bottom on maps, DSATUR, most connections first, random), forward checking.
- Solve (animated, 1–2000 steps/s), Step, Reset; Greedy (one pass, no backtracking); Find minimum (tries k = 1, 2, … without animation).
- Display: map view toggle, current vertex enlarged, tried colour ring on clashes, clashing edges red; stats (tries, assignments, backtracks, colours used) and an indented solver log.
- Home button.

## Code map
`coloring.html`, one IIFE:
- Graph: `V`, `E`, `adj`, `col`; `rebuildAdj`, `crosses`, `crossesAny`.
- Map: `inIsland`, `randomMap`, `computeRegions`, `bordersFromRegions`, `paintRegions`; `randomGraph`.
- Solver: `solve(k)` generator (`pick()` for ordering, `rec()` with forward checking via bitmask domains), `resetSolver`, `stepSolver`, `greedy`, `chromatic`.
- `draw()`, pointer input, `frame()`, `resize()`, UI.

## Decisions and user preferences
- Default order is "creation order" without forward checking so backtracking is visible; with 4 colours most maps still solve with few backtracks (the note suggests 3 colours / random order to watch it struggle).
- Map adjacency comes from the raster, not from a Delaunay triangulation (an earlier version used Delaunay, which produced edges between regions that do not visibly touch on the island edge).

## Known issues / not done yet
- "Find minimum" runs synchronously and gives up after 3 million tries; on large graphs with impossible k it can freeze the page for a few seconds.
- Exhaustive backtracking with 3 colours on a big map can run for a very long time (that is the point, but there is no time estimate).
- Editing a generated map turns it into a plain graph (map view is lost).
- Only tested in headless Chromium.

## Ideas / planned
- Real-world maps (e.g. countries of Europe, US states) as presets.
- Kempe-chain / heuristic solvers (tabu search) for comparison; show search tree size.
- Drag vertices to move them.

## Development notes
- Open `coloring.html` directly or via `python -m http.server`.
