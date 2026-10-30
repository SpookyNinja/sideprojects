# Maze Generator & Pathfinder Race

Handoff document: everything a new chat/session needs to continue this project.

## What it is
Generate a maze with one of several algorithms (animated), then race path-finding algorithms (BFS, Dijkstra, A*, greedy best-first, DFS) through the same maze, each in its own panel. Explored cells are coloured as a heat map by visit order, the frontier is cyan and the found path white. You can draw walls, mud (cost 5) and move start/goal on any panel.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Maze Generator + Pathfinder: generate a maze with DFS, Prim or Wilson's algorithm, then race BFS, Dijkstra and A* through it. Explored cells show as a heat map. You can also draw your own walls."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, no libraries. One file: `maze.html`.
- Grid of cells (`Uint8Array`: 0 wall, 1 open, 2 mud). "Rooms" are at odd coordinates, walls between them, so perfect mazes fit the grid.
- Generators and solvers are JS generator functions stepped from the animation loop. Binary heap for Dijkstra / A* / greedy.

## Features implemented
- Generators: recursive backtracker (DFS), randomized Prim, Wilson's (loop-erased random walks, uniform spanning tree), randomized Kruskal, recursive division, random obstacles (re-rolled until start and goal connect), empty room. Animated or instant.
- Size 11–121 columns (rows ≈ 0.62 × columns, odd). "Extra openings" knocks out walls between rooms to create loops; "mud patches" adds round mud blobs.
- Solvers: BFS, Dijkstra, A* (Manhattan / octile heuristic, tiny tie-break factor), greedy best-first, DFS; choose any subset (one panel each). Optional diagonal moves (no corner cutting).
- Race: same number of expanded cells per frame for every solver; rank shown when done (ties in the same frame share a rank); stats: explored, path length, path cost.
- Editing tools: wall, erase, mud, start, goal (works on every panel, resets the race).
- Redraws only when something changes. Home button.

## Code map
`maze.html`, one IIFE:
- `Heap` (min-heap), `cost()`, `neighbours()`, `h()` heuristic, `bestFirst(S, prio)` shared by Dijkstra/A*/greedy, `SOLVERS`.
- `GEN` generators, `isRoom`, `isInner`, `connected()`, `fullGeneration()` (size, generator, loops, mud).
- Panels: `newSearch(P)` (search state with `visit/frontier/found`), `newPanels()`, `resetRace()`.
- Drawing: `heat()`, `drawPanel()`; editing: `cellAt`, `apply`, `attachPointer`; `frame()` loop and UI.

## Decisions and user preferences
- BFS and DFS ignore mud cost on purpose, to show the difference to Dijkstra/A*.
- Race fairness = expanded cells per frame.

## Known issues / not done yet
- Only tested in headless Chromium; touch editing implemented but untested on phones.
- Drawing uses one `fillRect` per cell per panel; very large mazes with 5 panels are CPU-heavy while racing.
- Editing during generation is ignored.

## Ideas / planned
- Bidirectional search, Jump Point Search, IDA*.
- More generators (Eller's, growing tree, hunt-and-kill), hex mazes.
- Save/load mazes, step-by-step mode with the open list shown.

## Development notes
- Open `maze.html` directly or via `python -m http.server`.
