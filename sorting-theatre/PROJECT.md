# Sorting Algorithm Theatre

Handoff document: everything a new chat/session needs to continue this project.

## What it is
Up to 12 sorting algorithms race side by side on identical data. Every panel gets the same number of operations (compares/writes) per frame, so the faster algorithms visibly finish first and get a rank. Several views (bars, colour wheel, dots, spiral) and optional sound for one panel.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Sorting Algorithm Theatre: run 8–10 sorts side by side as bars, colour wheels or sound, with live counts of comparisons and swaps."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, no libraries. One file: `sorting.html`.
- Each algorithm is a generator; helpers `S.less`, `S.lessV`, `S.swap`, `S.write` count the operation, set highlights and `yield` once, so the runner can advance each algorithm by N operations per frame.
- Web Audio: one triangle oscillator whose pitch follows the last value touched in the focused panel.

## Features implemented
- Algorithms: bubble, cocktail shaker, insertion, selection, Shell (Ciura gaps), comb, merge (bottom-up), quicksort (median of three, explicit stack), heapsort, radix LSD base 4, odd–even, gnome. 8 are on by default; checkboxes add/remove panels.
- Data: 8–1024 elements; random, nearly sorted, reversed, few unique, sawtooth, already sorted.
- Views: bars (highlights: yellow = compare, red = write, green = known final position), colour wheel, dots, spiral.
- Start/pause (Space), single step, new data, operations per frame 1–3000 (log slider).
- Counters per panel (compares, writes) and finishing rank.
- Sound for the focused (clicked) panel. Home button.

## Code map
`sorting.html`, one IIFE:
- `ALGOS`: `{name, cx, *run(S, a)}` per algorithm. `DEFAULT_ON`.
- `makeData()`, `makePanel(key)` (creates DOM tile, context `S`, generator), `rebuild()`, `stepPanel()`.
- `drawPanel()` (all views), `beep()` (audio), `frame()` loop, UI wiring.

## Decisions and user preferences
- Fairness rule: equal operations per frame (not equal time). Radix sort's bucket reads count as operations but not as compares.
- All algorithms were checked offline against `Array.prototype.sort` for sizes 1–200 and several input kinds.

## Known issues / not done yet
- Only tested in headless Chromium; sound untested on mobile (needs a user gesture, handled by `audio.resume()` on Start).
- With 12 panels × 1024 bars the canvas drawing dominates frame time.

## Ideas / planned
- More algorithms (Tim sort, bitonic, intro sort, bogo for fun), stability indicator.
- Per-algorithm sound in a chord; "duel" mode with two big panels.
- Count reads separately; chart of operations vs. n.

## Development notes
- Open `sorting.html` directly. To test algorithms headlessly, extract the `ALGOS` block and run it in Node with a stub context (see git history / the session's test approach).
