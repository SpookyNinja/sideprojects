# Inside a Tiny LLM

Handoff document: everything a new chat/session needs to continue this project.

## What it is
An interactive visualization of a language model reading a sentence and generating an answer one token at a time. It runs a real, very small GPT-style transformer (trained in this repo with numpy) entirely in the browser and draws every intermediate activation: tokens, embeddings, attention connections per head, MLP neurons, the residual stream after each sublayer, and next-token probabilities. The user steps through the 8 stages of one generated token (Tokenize, Embed, Attention 1, MLP 1, Attention 2, MLP 2, Unembed, Pick), then the picked token is appended and the loop repeats.

## Original brief
1. "Let's make another side project."
2. After being offered several ideas, the user chose: "a visualization of an LLM reading a sentence and the steps it takes to generate an answer, with a view of the neural network."

## Tech
- Plain HTML/CSS/JS, no libraries, no build step (works from `file://` and GitHub Pages).
- Files: `llm-inside.html` (UI + canvas drawing), `engine.js` (JS forward pass, `window.TinyLM`), `model-data.js` (generated trained weights, ~230 KB, `window.MODEL_DATA`), `train/train.py` (numpy trainer), `train/reference.json` (logits from numpy for a parity check).
- Model: pre-LayerNorm decoder-only transformer, 2 layers, 4 heads (head dim 8), d_model 32, MLP hidden 128 (ReLU), learned position embeddings, max length 14, vocabulary 102 words (whole words + `?` `.`, plus `<bos>`, `<unk>`), untied output layer, no attention biases.
- Training data: ~166 generated sentences (capitals, opposites, animal sounds, colours, addition up to ten), each in a statement form ("the capital of france is paris .") and a question form ("what is the capital of france ? it is paris ."). Trained 4000 Adam steps; final loss ~0.6 is the unavoidable entropy of the question tokens; greedy completion of every prompt is 166/166 correct.

## Features implemented
- Prompt box + example chips + clickable vocabulary list; unknown words are read as `<unk>` with a warning; prompt shortened to fit the max length.
- Stage stepper (clickable pipeline), Back / Next / Play / "Next token"; keyboard: left/right arrows, space.
- Main canvas: one row per token, columns = residual-stream vectors (32 coloured cells: orange positive, blue negative) after embedding / each attention / each MLP, attention arcs between columns (thickness = weight), MLP neuron strips (128 cells, ReLU), per-row next-token guesses, "+ token" ghost row when a token is picked. Columns fade in as the stages advance.
- Hover a row to make it the attention focus (default = last token); hover cells for exact values / top attended tokens.
- Side panel: narration with live facts, text so far, per-layer attention-head thumbnails (average or single head, click to select), top-8 probability bars, temperature slider (0 = greedy, >0 samples).
- Generation stops at `.` or max length.

## Code map
- `train/train.py`: `corpus()` builds sentences, `forward`/`loss_and_grads` are the model with manual backprop, `gradcheck()` (`--check`) verifies gradients, `main()` trains, tests greedy accuracy, writes `../model-data.js` and `reference.json`. Run from inside `train/`. Hyperparameters D, NH, H, NL, TMAX at the top.
- `engine.js`: `TinyLM.load(data)`, `TinyLM.run(model, ids)` returns a trace (`emb`, `layers[l].{in, ln1, attn[head][t][u], attnOut, mid, ln2, hidden, mlpOut, out}`, `lnf`, `logits`, `probs`), `TinyLM.softmax`.
- `llm-inside.html`: state object `st` (prompt ids, generated ids, stage, picked token, head selection, hover row); `setStage/next/back/skip/commit` state machine; `draw()` canvas renderer (layout constants `LAY`, `X`, `W`, `RH`); `story()` narration; `headsPanel()`, `probs()`, mousemove tooltip handler. `window.__llm` is exposed for testing.

## Decisions and user preferences
- Chose a self-trained toy transformer over a downloaded real model (e.g. transformers.js GPT-2): exported ONNX models do not expose attention weights, the download is large, and a toy model lets every drawn number be real. Trade-off: it only knows a ~100-word vocabulary.
- Whole-word tokens (not BPE) so the token-to-word mapping is obvious.

## Known issues / not done yet
- Weights are rounded to 4 decimals in `model-data.js`; JS logits differ from numpy by ~0.01 (checked, harmless).
- Only tested in headless Chromium (Playwright screenshots); not tested on touch devices or small phones (the canvas just scales down).
- The model answers poorly outside its training templates (it is not a general LLM); out-of-template prompts give confident nonsense.
- Back is only available within one token (cannot step back across an appended token).

## Ideas / planned
- Neuron-level zoom: click a row at an MLP stage to see the 32 -> 128 -> 32 weights as a node-link diagram.
- Show per-head contribution vectors and a "logit lens" (decode each residual column into word guesses).
- Side-by-side comparison of two prompts; export of the trace.
- Larger corpus (more facts, two-step sentences) and a bigger model, retrained with `train/train.py`.

## Development notes
- Retrain: `cd llm-inside/train && python3 train.py` (about 70 s on 4 cores, numpy only). Gradient check: `python3 train.py --check`.
- Parity check: load `model-data.js` and `engine.js` in node, run `TinyLM.run` on `reference.json` ids and compare the last-row logits (expected max diff ~0.01).
- If you change the model config, `maxLen`/vocab are read from `MODEL_DATA.config`; the canvas layout assumes d=32 (3 px cells) and hidden=128 (1 px neurons), so adjust `LAY`, `CS` and `HID` handling in `llm-inside.html` accordingly.
- Screenshot testing: Playwright (preinstalled in the cloud environment) with `window.__llm.setStage(n)`.
