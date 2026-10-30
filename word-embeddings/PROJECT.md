# Word Embedding Space

Handoff document: everything a new chat/session needs to continue this project.

## What it is
A 3D fly-through of about 6,000 English words placed by their GloVe word vectors. Words used in similar ways sit close together (weekdays, colours, sports, countries…). You can search a word and see its nearest neighbours, do vector arithmetic like *king − man + woman ≈ queen*, switch between a t-SNE "meaning map", PCA and your own semantic axes (e.g. man→woman, bad→good, small→big), and highlight word groups.

## Original brief
1. The user asked for more side projects similar to the existing ones, "with some nice visualizations"; the user picked this idea (with nine others), each on its own branch.
2. Accepted pitch: "Word Embedding Space: a 3D projection of a small word-vector set you can fly through, with vector arithmetic like king − man + woman."
3. Follow the repo conventions in `AGENTS.md`.

## Tech
- HTML/CSS/JS with three.js r128 + OrbitControls from jsDelivr (same versions as other projects).
- Files: `embeddings.html` (page), `vectors.js` (data, ~0.9 MB), `build/build_vectors.py` (regenerates `vectors.js`).
- Data: GloVe 6B 100d (Pennington, Socher & Manning 2014; Wikipedia 2014 + Gigaword 5; Public Domain Dedication and License), downloaded from the gensim-data GitHub release `glove-wiki-gigaword-100`.
- `vectors.js` sets `window.EMBED = {dim, scale, words, mapCount, mapIndex, vectors, coords}`: the 6,000 most frequent purely alphabetic words plus ~70 curated extras; vectors normalised to length 1 and quantised to int8 (base64); 3D coordinates as int16 (base64).
- 3D map: exact t-SNE (numpy, perplexity 25, 900 iterations) of the 2,500 most frequent content words; every other word is placed at the similarity-weighted average of its 5 nearest map words.

## Features implemented
- Point cloud (custom point shader, additive), map words brighter, group words coloured, highlighted words white.
- Search with autocomplete (datalist): nearest 13 words by cosine similarity, list with bars, lines to the neighbours, camera flies there.
- Word arithmetic: free expression with + and −; top 10 results excluding the input words; the computed point is shown as a white octahedron, arrows from subtracted to added words and from the first word to the result; 8 example chips.
- Layouts with animated transitions: t-SNE map, PCA (top 3 principal components by power iteration in the browser), custom axes from 3 word pairs (labelled axis lines).
- 12 highlight groups with labels (countries, capitals, animals, colours, numbers, family, jobs, feelings, food, sports, time, music).
- Automatic labels for words near the orbit target (fewer while a search/arithmetic result is shown); click a point to select it; slow rotation. Home button.

## Code map
- `build/build_vectors.py`: `main()` (load, choose vocabulary, quantise, t-SNE, place other words, write `vectors.js`), `tsne()`.
- `embeddings.html`, one IIFE: data decoding (`VEC`, `C16`, `onMap`), `nearest()`, `GROUPS`; layouts `layoutTsne/layoutPca/layoutAxes/project`; three.js scene (`cloud`, `lines`, `star`, `axisGroup`); labels `labelSprite()` (cached canvas textures), `wantedLabels()`, `updateLabels()`; actions `select()`, `calc()`, `placeStar()`, `flyTo()`, `setLayout()`; UI wiring; `loop()` (eases positions to the target layout).

## Decisions and user preferences
- An npm word2vec subset (word2vec-wordlist) was tried first but its vectors were too noisy (king − man + woman gave "weeping"); GloVe 100d gives the expected results (queen, rome, berlin, moscow…).
- Vocabulary kept to ~6k words and int8 to keep the data file under 1 MB.

## Known issues / not done yet
- Some classic analogies fail with GloVe (e.g. comparatives); the page shows whatever the vectors say.
- Words outside the vocabulary (rare words, plurals not in the top 6k) cannot be searched.
- Labels can overlap when zoomed out; needs internet for three.js. Only tested in headless Chromium.

## Ideas / planned
- Bias explorer (project jobs onto he→she), word-path interpolation, analogy quiz game.
- Larger vocabulary loaded lazily; sentence/emoji embeddings.

## Development notes
- Rebuild data: download `glove-wiki-gigaword-100.gz` (see Tech) and run `python3 build/build_vectors.py path/to/glove-wiki-gigaword-100.gz` (numpy only, ~3 minutes).
- Open via a local server (`python -m http.server`) or directly; `vectors.js` is loaded with a plain `<script>` tag so `file://` works too.
