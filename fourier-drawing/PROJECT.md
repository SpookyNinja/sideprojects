# Fourier Drawing

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A single-page canvas toy. The user draws any closed shape freehand; the page computes its Discrete Fourier Transform and replays it as a chain of rotating circles (epicycles) whose tip retraces the drawing, leaving a fading trail.

## Original brief
1. "Another side project, Fourier drawing."
2. Landing-page description supplied by the user: "Draw any shape and watch it rebuilt by rotating epicycles (a Discrete Fourier Transform visualised)."

## Tech
Plain HTML/CSS/JS, no libraries, no build step. One file: `fourier.html`. Hosted via GitHub Pages; registered in `projects.json`.

## Features implemented
- Freehand drawing with mouse/touch/pen (Pointer Events); the path is implicitly closed on release.
- Path resampled to N=512 evenly-spaced points (by arc length), then a plain O(N²) DFT.
- Coefficients sorted by amplitude; epicycle chain drawn largest-first; yellow fading trail covers one period.
- Controls: Clear, presets (heart, star, infinity, trefoil), "Circles" slider (1–512, shows how few circles are needed), speed slider, toggles for showing circles and the original (resampled) path.
- Home button (bottom right), responsive toolbar.

## Code map
All in `fourier.html`: `resample()` (arc-length resampling), `dft()` (returns sorted `{k,re,im,amp,phase}`), `setShape()` (resample + DFT + reset), `preset()` (parametric shapes), `epicycles(t,n,draw)` (sums/draws the chain), `frame()` (render loop, trail), pointer handlers under "input".

## Decisions and user preferences
- Page named `fourier.html` (not index.html) per repo convention.
- Used a direct DFT instead of an FFT: N=512 is fast enough and keeps the code readable.

## Known issues / not done yet
- Only checked briefly in a browser; touch input untested on a real device.
- Resizing the window keeps the shape centred but does not rescale it.
- Changing the Circles slider clears the trail (it refills over one period).

## Ideas / planned
- Upload an SVG/image outline; multiple disconnected strokes.
- Export a GIF/PNG; show the frequency/amplitude spectrum.
- Replace the DFT with an FFT for larger N.

## Development notes
Open `fourier.html` directly in a browser or serve the repo root with any static server (e.g. `python -m http.server`).
