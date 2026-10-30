# Game of Life Explorer

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A cellular-automaton playground in one static page. You draw cells on a grid, stamp patterns from a library, and run the simulation under Conway's Life or any other Life-like rule (HighLife, Seeds, Day & Night, ...), including custom Birth/Survival rules. It is for exploring how small rule changes change the behaviour.

## Original brief
1. (Suggested by the assistant earlier as a side-project idea, then chosen by the user.) "Game of Life explorer: Cellular automata playground: draw patterns, try rule variants (Life, HighLife, etc.), adjustable speed, pattern library."
2. Follow the repo conventions in `AGENTS.md` (own folder, PROJECT.md, entry in `projects.json`, Home button).

## Tech
- Plain HTML/CSS/JS, no libraries, no build step. Works on GitHub Pages.
- Files: `life.html` (everything inline), `PROJECT.md`.
- Rendering: 2D canvas, redrawn on every change; simulation on typed arrays.

## Features implemented
- Grid fills the stage; size follows cell size (3-24 px slider) and window size. Content stays centred when the grid resizes.
- Play/Pause, single Step, Reset (back to the state after the last edit), speed 1-120 gen/s (max 8 steps per frame).
- Tools: Draw (click toggles, drag paints, Bresenham line between pointer events), Erase, Stamp (ghost preview). Right-click always erases. Pointer events, so touch works.
- Rules: 14 presets (Life, HighLife, Seeds, Day & Night, Replicator, Maze, Mazectric, 34 Life, Diamoeba, 2x2, Life without death, Anneal, Gnarl, Coral) with a short description each; B0-B8 / S0-S8 checkboxes; editable rule text (`B3/S23`). Selecting/typing keeps all three in sync and shows "Custom rule" when no preset matches.
- Pattern library (16): single cell, glider, LWSS, block, beehive, blinker, toad, beacon, pulsar, pentadecathlon, thunderbird, R-pentomino, diehard, acorn, Gosper glider gun, HighLife replicator. Rotate (R) and flip (F) before stamping.
- Board options: wrap-around torus on/off, colour by cell age (yellow to violet), grid lines.
- Randomize with density slider, Clear.
- Population sparkline (last 288 generations), generation and population counters in the HUD.
- RLE import (pasted text becomes a stamp; a `rule =` header is applied) and RLE export of the whole board's bounding box.
- Keyboard: Space, S, C, X, R, F, D/E/T.
- Starts paused with an R-pentomino in the centre.
- Home button bottom right.

## Code map
All in `life.html`, one IIFE, sections marked with `// ----------` comments:
- rules: `RULES`, `birth`/`surv` lookup arrays, `setRule`, `readBoxes`, `parseRule`, `refreshRuleUI`.
- patterns: `PATTERNS` (rows of `O`/`.` text compiled to cell lists by `compilePattern`), `oriented()` applies rotate/flip.
- board: `resize()` (rebuilds/resamples the grid), `step()` (one generation, neighbour counting with precomputed wrap column tables, ages), `grid`/`next`/`age`, `snap` (for Reset).
- editing: `setTool`, `setCell`, `stamp`, `clearAll`, `randomize`, `edited()` (takes the Reset snapshot and restarts the population graph).
- pointer: `cellAt`, `line`, pointer handlers.
- rendering: `draw()`, `drawSpark()`, palette `PAL`.
- run loop: `frame()`, `setRunning`.
- RLE: `#rleLoad` and `#rleExport` handlers.

## Decisions and user preferences
- Panel is a fixed left column (not an overlay) so it never hides part of the grid. On narrow screens it moves below the canvas.
- Finite grid sized to the window rather than an infinite universe: simple and fast. Wrap-around is on by default so gliders never die at the edge.
- Pattern text uses `O` for live cells and `.` for dead; RLE is only used for import/export.

## Known issues / not done yet
- Only checked in the built-in browser pane; not tested on a real touch device.
- Changing cell size recomputes the grid size, so cells near the edges are lost when it shrinks (they do not return when it grows back).
- No zoom/pan and no undo.
- Rules are the "Life-like" (outer totalistic, Moore neighbourhood) family only. B0 rules (cells born from nothing) will flash the whole board and are not specially handled.
- RLE import ignores multi-state letters beyond a simple fallback.

## Ideas / planned
- Zoom and pan on a larger board.
- Undo/redo for edits.
- Save/load boards in the browser (localStorage) and shareable URLs with rule and pattern.
- More patterns (guns, puffers, rakes, Wireworld-style extras).
- Other automata: Generations rules, Wolfram 1D rules, Langton's ant.
- Pattern hover search/filter and a category grouping in the library.

## Development notes
- Open `life.html` directly in a browser, or serve the repo root with `python -m http.server`. No build step.
- The Home link is `../index.html`, so keep the page one folder deep.
