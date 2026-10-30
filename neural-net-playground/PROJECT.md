# Neural Net Playground

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A small multi-layer perceptron, written from scratch in JavaScript, learns to separate orange from blue points in 2D. The big picture shows the network's output and decision boundary; a network diagram shows every neuron as a small heat map of what it responds to, with weights drawn as coloured lines. Training happens live in the browser.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Neural Net Playground from Scratch: train a small multilayer neural network in the browser on 2D point sets. The decision boundary changes as it trains, and you can see each neuron's activation."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- Plain HTML/CSS/JS, no ML libraries. One file: `nn.html`.
- Network: dense layers with Float64Arrays, hidden activation tanh/ReLU/sigmoid/sine/linear, sigmoid output with binary cross-entropy, mini-batch backprop, Adam (effective step = learning rate × 0.1) or plain SGD, optional L2 on weights.
- Heat maps: forward pass on a 48 × 48 grid for every neuron each time something changes.

## Features implemented
- Datasets: circle, XOR, spiral, two blobs, moons, checker; noise and point count sliders; 80/20 train/test split (test points hollow). Click to add an orange point, right-click / shift-click for blue.
- Input features: x, y, x², y², x·y, sin x, sin y, r (any combination; at least one stays on).
- Architecture: free text "6, 4" (up to 6 hidden layers, 16 neurons each) plus shortcut buttons.
- Train/pause (Space), single epoch step, reset weights; learning rate (log), batch size, L2.
- Live train and test loss + chart; epoch counter.
- Network diagram: heat map per neuron, curves coloured by weight sign (orange positive, blue negative) and thickness by size; click a neuron to show it big in the main view.
- Home button; layout stacks vertically on narrow screens.

## Code map
`nn.html`, one IIFE:
- `DATA` generators, `makeData()`; `FEATS`, `featurise()`.
- `ACT` (function + derivative), `buildNet()`, `forward()`, `trainBatch()` (backprop + Adam/SGD), `lossOf()`.
- `computeMaps()`, `colourOf()`, `mapImage()`, `drawImg()`.
- `drawBoundary()`, `drawNet()` (stores `nodePos` for clicks), `drawLoss()`.
- `stepEpoch()`, `frame()`, `layout()`, UI wiring.

## Decisions and user preferences
- The design is our own (left: output + loss, right: network diagram) rather than a copy of an existing playground.
- One epoch per animation frame while training.

## Known issues / not done yet
- Very wide networks (6 × 16) recompute many heat maps every frame and get slow.
- Only tested in headless Chromium.

## Ideas / planned
- Multi-class (3+ colours) with softmax; regression datasets.
- Show gradients/weight updates as animation; dropout; learning-rate schedule.
- Drag weights by hand to see the effect.

## Development notes
- Open `nn.html` directly or via `python -m http.server`.
