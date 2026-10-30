# Clustering Step by Step

Handoff document: everything a new chat/session needs to continue this project.

## What it is
An interactive explainer for two clustering algorithms. Click or spray points (or load a dataset), then step through k-means (assign / update rounds, with centre trails and the region each centre owns) or DBSCAN (visit points one at a time, ε circles, core / border / noise). A text box explains every step and a small chart shows the error per round, an elbow chart, or cluster sizes.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "K-Means / DBSCAN Step-Through: click to place points, then step through clustering one iteration at a time."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, no libraries. One file: `clustering.html`.
- Both algorithms are generators that yield after each visible step and call `explain()` with a sentence about what just happened.

## Features implemented
- Datasets: blobs, moons, rings, uneven sizes, noisy blobs, uniform. Click = add point, drag = spray, right-click = remove nearest point, clear.
- k-means: k 1–10; start with k-means++, random points, or all in a corner (to show bad starts); nearest-centre shading; centre trails; squared-error chart per round; elbow chart (best of 4 runs for k = 1–10, current k highlighted).
- DBSCAN: ε 8–120 px, min. neighbours 2–15; random visiting order; ε circles around core points; current point with dashed ε circle; queue shown as white dots; noise as grey ×; cluster-size bar chart.
- Play/pause, step, restart; steps per second 1–300. Explanations for every step. HUD; Home button.

## Code map
`clustering.html`, one IIFE:
- `DATA` generators; `kmeans()` and `dbscan()` generators writing to `state`.
- `draw()` (shading, ε circles, points, centres, trails, current DBSCAN point), `drawChart()`, `explain()`.
- `restart()`, `stepOnce()`, `frame()`; pointer input (`edited()` restarts); elbow computation in the `#elbow` handler.

## Decisions and user preferences
- Points are stored in CSS pixels; ε is in pixels so it is easy to relate to the picture.
- DBSCAN visits points in random order (like many textbook illustrations) so clusters appear in a non-obvious order.

## Known issues / not done yet
- DBSCAN neighbour search is O(n) per query (fine for a few hundred points, slow for thousands).
- Resizing the window does not rescale existing points.
- Only tested in headless Chromium.

## Ideas / planned
- More algorithms: hierarchical (dendrogram), Gaussian mixture (EM with ellipses), mean shift, spectral.
- Silhouette score; side-by-side comparison of two algorithms on the same points.

## Development notes
- Open `clustering.html` directly or via `python -m http.server`.
