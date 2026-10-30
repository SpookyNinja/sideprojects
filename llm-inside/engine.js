// Forward pass of the tiny transformer in plain JS. Keeps every intermediate
// activation so the page can draw them. Weights come from model-data.js.
(function (root) {
  function mat(p) { return Float64Array.from(p.data); }
  function load(data) {
    const P = {};
    for (const k in data.params) P[k] = mat(data.params[k]);
    return { cfg: data.config, vocab: data.vocab, P, idx: Object.fromEntries(data.vocab.map((w, i) => [w, i])) };
  }
  // out[T][n] = x[T][m] @ w[m][n] (+ b)
  function linear(x, w, m, n, b) {
    const out = x.map(row => {
      const o = new Float64Array(n);
      if (b) o.set(b);
      for (let i = 0; i < m; i++) { const xi = row[i]; if (xi === 0) continue; const off = i * n; for (let j = 0; j < n; j++) o[j] += xi * w[off + j]; }
      return o;
    });
    return out;
  }
  function layerNorm(x, g, b) {
    return x.map(row => {
      const n = row.length; let mu = 0; for (const v of row) mu += v; mu /= n;
      let va = 0; for (const v of row) va += (v - mu) * (v - mu); va /= n;
      const inv = 1 / Math.sqrt(va + 1e-5), o = new Float64Array(n);
      for (let i = 0; i < n; i++) o[i] = (row[i] - mu) * inv * g[i] + b[i];
      return o;
    });
  }
  function add(a, b) { return a.map((r, t) => r.map((v, i) => v + b[t][i])); }
  function softmax(z) {
    let mx = -Infinity; for (const v of z) if (v > mx) mx = v;
    const e = Array.from(z, v => Math.exp(v - mx)); let s = 0; for (const v of e) s += v;
    return e.map(v => v / s);
  }

  // ids: token ids including the leading <bos>. Returns a full activation trace.
  function run(M, ids) {
    const { d, heads, hidden, layers, vocab } = M.cfg, dh = d / heads, T = ids.length, P = M.P;
    const tok = ids.map(id => P.tok.slice(id * d, id * d + d));
    const pos = ids.map((_, t) => P.pos.slice(t * d, t * d + d));
    let x = add(tok, pos);
    const tr = { ids, T, tok, pos, emb: x, layers: [] };
    for (let l = 0; l < layers; l++) {
      const g = n => P[`l${l}_${n}`], L = {};
      L.in = x;
      L.ln1 = layerNorm(x, g('ln1_g'), g('ln1_b'));
      const q = linear(L.ln1, g('wq'), d, d), k = linear(L.ln1, g('wk'), d, d), v = linear(L.ln1, g('wv'), d, d);
      L.attn = []; const ctx = x.map(() => new Float64Array(d));
      for (let h = 0; h < heads; h++) {
        const A = [];
        for (let t = 0; t < T; t++) {
          const s = new Float64Array(t + 1);
          for (let u = 0; u <= t; u++) { let dot = 0; for (let i = 0; i < dh; i++) dot += q[t][h * dh + i] * k[u][h * dh + i]; s[u] = dot / Math.sqrt(dh); }
          const a = softmax(s), row = new Float64Array(T); // causal: later positions stay 0
          for (let u = 0; u <= t; u++) { row[u] = a[u]; for (let i = 0; i < dh; i++) ctx[t][h * dh + i] += a[u] * v[u][h * dh + i]; }
          A.push(row);
        }
        L.attn.push(A);
      }
      L.attnOut = linear(ctx, g('wo'), d, d);
      L.mid = add(x, L.attnOut);
      L.ln2 = layerNorm(L.mid, g('ln2_g'), g('ln2_b'));
      L.hidden = linear(L.ln2, g('w1'), d, hidden, g('b1')).map(r => r.map(v => Math.max(0, v)));
      L.mlpOut = linear(L.hidden, g('w2'), hidden, d, g('b2'));
      L.out = add(L.mid, L.mlpOut);
      x = L.out; tr.layers.push(L);
    }
    tr.lnf = layerNorm(x, P.lnf_g, P.lnf_b);
    tr.logits = linear(tr.lnf, P.out_w, d, vocab, P.out_b);
    tr.probs = softmax(tr.logits[T - 1]);
    return tr;
  }
  root.TinyLM = { load, run, softmax };
})(typeof window !== 'undefined' ? window : globalThis);
