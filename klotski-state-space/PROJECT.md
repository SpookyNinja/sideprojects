# Klotski State Space

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A single-file web app (`klotski.html`, no build step) with two linked views:

- **Left: a Klotski-style sliding-block board.** Grid size is configurable (default 4 cols × 5 rows). The player builds their own puzzle by dragging block types onto the grid, then slides blocks around like in the real puzzle.
- **Right: a 3D "neural network"-style graph of the puzzle's state space.** Every arrangement of the blocks is one node; two nodes are connected if one block slides one cell to get from one to the other. 1 block gives a grid/line, 2 blocks a lattice, 3 blocks a 3D-ish structure, and so on.

The user's original brief (paraphrased):
1. Board with Klotski-like grid, size settable, default normal Klotski size; player adds blocks however they like; starts with 3 random blocks; blocks move like in the puzzle.
2. 3D neural-network visualisation of all states, nodes connected to the states they can transition to.
3. The network should visibly build itself slowly.
4. Zooming in a lot replaces white dots with the actual picture of the state.
5. While moving blocks on the board, a marker moves around the network to the matching state.

Later requests:
- Real custom blocks, including L and T shapes, that can be placed on the board.
- A few templates that create interesting shapes of the state space (Möbius strip, pyramid, etc.).

## Tech
- Plain HTML/CSS/JS in one file. three.js r128 and `OrbitControls` loaded from jsDelivr CDN (needs internet).
- Hosted via GitHub Pages from the repo root (see root `index.html` / `projects.json`).

## Features implemented
### Board
- Configurable grid (cols/rows, 2–10). "Apply" resets to 3 random blocks.
- 3 random blocks on load ("3 random blocks" button repeats this), "Clear board".
- Grid size can be 1–10 in each direction (1 is needed for corridor templates).
- **Drag & drop placement:** press and drag a palette button (1×1, 1×2, 2×1, 2×2, custom W×H via "Drag custom", or the custom-shape editor's "Drag shape") onto the grid. A ghost follows the cursor, snaps to cells, shows a white outline if valid and red if occupied/out of bounds. While dragging, **R** rotates and **M** mirrors the shape. Plain click on the palette does nothing.
- **Arbitrary shapes (polyominoes):** every block is a set of cells. The "Custom shape" fieldset has a 5×5 editor (click or paint cells; it must be connected by sides, otherwise it is drawn red and can't be dragged), Rotate / Mirror / Clear buttons and presets: corner, L, T, S, plus, U, big L, P, big T.
- **Rotate a placed block:** select it and press R or "Rotate selected ⟳". It is nudged by up to 2 cells if needed to fit. This changes the puzzle, so the graph is rebuilt.
- **Walls:** with "place as wall (immovable)" checked, dragged blocks become fixed obstacles (grey, hatched). Walls cannot be dragged and are not part of a state; they can be removed like other blocks.
- "3 random blocks" can also produce corner, L and T pieces (randomly rotated).
- Slide blocks by dragging (moves stepwise, each step is a state transition; blocks can slip diagonally around obstacles) or with arrow keys on the selected block.
- Remove a block: right-click, double-click, or select + Delete/Backspace.
- Each block has its own colour and identity, so two identical-shaped blocks in swapped positions are different states.
- **Option "rectangles move along long side only"** (ON by default): 1×2 moves only vertically, 2×1 only horizontally; squares (1×1, 2×2) and non-rectangular shapes move freely. Toggling rebuilds the graph.
- **Option "identical shapes are interchangeable"** (OFF by default): movable blocks with the same shape *and orientation* count as the same piece, so swapping them is not a new state. They are drawn in the same colour. Implemented by sorting each group's positions in the state vector (`canonGroup`).

### Templates
Dropdown + "Load". Each template sets grid size, the two options, max nodes, build speed and the blocks. State counts were verified in a headless browser:
| Template | Setup | States |
|---|---|---|
| Möbius strip | 5×5, 3×3 wall in the middle, two identical 1×1 on the ring | 120 |
| Cylinder (annulus) | same, blocks distinguishable (double cover of the Möbius strip) | 240 |
| Pyramid (tetrahedron) | 10×1 corridor, 3 blocks (can't pass → a<b<c) | 120 |
| Hyper-pyramid (4D simplex) | 10×1 corridor, 4 blocks | 210 |
| Triangle | 10×1 corridor, 2 blocks | 45 |
| Cube 6×6×6 | 6×5, three lanes separated by walls | 216 |
| Torus (donut) | 9×4, two separate 4×4 rings with one block each | 144 |
| Plane | 7×7, single block | 49 |
| Classic Klotski (Huarong Dao) | 4×5 classic layout, interchangeable on, axis rule off, max 30000 | 25,955 |
| L & T pieces | 5×5 with L, T and corner | 384 |

The force layout shows the topology only roughly (e.g. the tetrahedron tends to look like a curved sheet; the Möbius strip like a twisted band).

### Graph
- State = tuple of block positions. Graph is built by BFS outward from the current state, a configurable number of nodes per second (build speed slider, exponential 20–2000 nodes/s).
- Incremental force-directed 3D layout (springs + grid-hashed repulsion + weak gravity), run on the main thread within a ~12 ms per-frame budget; auto-stops when settled.
- New nodes spawn at their parent's position so the graph visibly grows organically.
- Nodes drawn as round points via a custom shader (screen size scales with distance, clamped); edges as `LineSegments`.
- **Level of detail:** within a few world units of the camera, up to 36 nearest nodes become sprites showing a rendered picture of their board state (same drawing code as the board). The current state's picture has a red border. Fades in between distances 6 and 3.5.
- **Marker:** red glowing sprite that follows the current state smoothly. Moving to a state not yet in the graph creates and expands it immediately.
- Clicking a node loads that state onto the board.
- **Node limit:** "max nodes" field (default 15000) plus a "no limit" checkbox with a slowdown warning (hard cap in code is 100,000,000, unreachable in practice: JS `Map` tops out around 16.7M entries). Changing either rebuilds the graph. Status line shows "growing…", "complete" or "node limit reached".
- Arrays are growable (start at 4096 nodes / 8192 edges, double when needed; GL buffers are rebuilt on growth).

### Camera / mouse controls (3D view)
- Left-drag rotate, right-drag or shift+left-drag pan, wheel zoom (very close zoom allowed), click a node to load it.
- Buttons: **Fit view** (auto-frames graph; also the default until the user first touches the camera), **Zoom to marker**, **follow marker** checkbox, **Rebuild**.
- **Home button** fixed at the bottom right (`#home`, links to `../index.html`).
- Responsive: stacks vertically below 760 px width.

## Code map (all in `klotski.html`)
- Block object: `{cells:[[dx,dy]…], w, h, rect, x, y, fixed, base, color}` (`cells` normalised to start at 0,0; `w,h` = bounding box; `rect` = full rectangle; `base` = own colour, `color` = displayed colour).
- Shapes: `normShape`, `rectCells`/`rectShape`, `rotShape`, `mirShape`, `shapeSig`, `connected`, presets `SHAPES`.
- Puzzle state `S` (cols, rows, blocks, selection), `mkBlock`, `occupancy`, `fits`, `addBlock` (random spot), `placeShape`, `removeBlock`, `randomBlocks`, `recolor`, `rotateSelected`.
- Drawing: `rrPath`/`rr`, `blockPath` (rounded cells joined by bridges for non-rectangles), `blockOutline` (exposed edges only), `drawBlock` (hatches walls), `drawGrid` (shared by board, ghost, editor and 3D thumbnails; supports `preview`).
- Board input: pointer handlers on `#board`, `tryStep`, `moveToward`, `dirAllowed`, `startPaletteDrag` (canvas ghost; `paletteDrag.transform` used by R/M keys).
- Shape editor: `ED`, `edSet`, `edCells`, `edDraw`, `edShape`.
- Templates: `TEMPLATES` (helpers `R(w,h,x,y,fixed)`, `P(name,x,y)`), `loadTemplate`.
- Graph `G`: only movable blocks are in the state (`G.mi` maps to `S.blocks`); walls are in `G.wallOcc` (-2). `resetGraph`, `boardState`, `canonGroup`/`canonAll`, `createNode`, `addEdge`, `expand` (BFS neighbours; honours axis rule via `G.axis`), `ensureNodeCap`/`ensureEdgeCap`, `onMoved`, `loadNode`.
- Layout: `layoutStep` (constants `REST, KS, ETA, REP, RCUT, MAXSTEP, GRAV`).
- Three.js: scene setup, `rebuildGLBuffers`, `buildSprites`/`updateLOD`/`placeSprites`, marker, `frame()` main loop, status `setInterval`.

## Decisions and user preferences
- Node limit: user first wanted it removed, then asked for it back with default 15000 plus a "no limit" option that warns about slowdowns.
- "Rectangles move along long side only" is ON by default (user request).
- Custom blocks may be any side-connected shape (L, T, …); walls and the interchangeable option were added so that templates can produce real topological shapes (Möbius strip needs identical blocks).
- Blocks are placed by drag and drop from the palette, not randomly on button press (user request). Random placement is only used for the initial 3 blocks and the "3 random blocks" button.
- 3D view must support mouse rotate, pan and zoom.

## Known issues / not done yet
- Headless-tested (Chromium): all templates, shape drag with R-rotation, wall placement, rotate selected. Not tested on touch devices (rotating while dragging needs a keyboard there; rotate in the editor first instead) or very large graphs (hundreds of thousands of nodes).
- "Interchangeable" only groups blocks with the same orientation; an L and a rotated L are different pieces (they can't rotate during play anyway).
- With "interchangeable" on, loading a node may swap which of two identical blocks is where (same colour, so not visible).
- No undo for rotate/remove.
- Layout runs on the main thread; big graphs reduce framerate. Layout quality for high-dimensional graphs is a "hairball" blob rather than a clean lattice like in the reference images.
- Requires CDN access (three.js); no offline fallback.
- Hidden/background browser tabs pause `requestAnimationFrame`, so growth pauses there (expected).
- Switching grid size or axis-only rebuilds the graph from scratch; no undo.
- No goal/win condition, no move counter, no solver.

## Ideas / planned
- Move layout to a Web Worker.
- Better layout for lattice-like graphs (e.g. initialise from per-block coordinates, or multilevel layout).
- Highlight path history / visited nodes, show shortest path to a chosen state, optional Klotski solver (BFS/A*) and goal marking (e.g. 2×2 block at the bottom-centre exit).
- Colour nodes by BFS depth or connected component; highlight neighbours of the current node.
- Save/load layouts of blocks (URL hash or localStorage); more templates (e.g. other classic Klotski layouts, Klein-bottle-like or higher tori with more rings).
- Layout seeded from block coordinates so simplex/torus templates show their shape more cleanly.
- Keyboard/touch polish; instanced edges for performance.

## Development notes
- To run locally, serve the folder over HTTP (e.g. `python -m http.server`) and open `klotski.html`; opening via `file://` also works for this page since it has no fetches, but the repo's root `index.html` needs HTTP (`fetch('projects.json')`).
- Windows quirk met during development: long scratch paths break `git`; clone the repo to a short path.
