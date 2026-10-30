"""Train the tiny transformer used by llm-inside (pure numpy, manual backprop).

Run:  python3 train.py            (writes ../model-data.js)
      python3 train.py --check    (finite-difference gradient check only)
"""
import json, sys, itertools
import numpy as np

# ---------------------------------------------------------------- corpus
CAPITALS = [("france","paris"),("germany","berlin"),("italy","rome"),("spain","madrid"),
            ("japan","tokyo"),("egypt","cairo"),("canada","ottawa"),("china","beijing"),
            ("greece","athens"),("portugal","lisbon")]
OPPOSITES = [("hot","cold"),("big","small"),("up","down"),("day","night"),
             ("fast","slow"),("happy","sad"),("old","young"),("light","dark")]
ANIMALS = [("dog","woof"),("cat","meow"),("cow","moo"),("duck","quack"),("sheep","baa"),("lion","roar")]
COLORS = [("sky","blue"),("grass","green"),("snow","white"),("coal","black"),("banana","yellow"),("tomato","red")]
NUMS = ["one","two","three","four","five","six","seven","eight","nine","ten"]

def corpus():
    s = []
    for c, y in CAPITALS:
        s.append(f"the capital of {c} is {y} .")
        s.append(f"what is the capital of {c} ? it is {y} .")
    for a, b in OPPOSITES:
        s.append(f"the opposite of {a} is {b} .")
        s.append(f"what is the opposite of {a} ? it is {b} .")
        s.append(f"the opposite of {b} is {a} .")
        s.append(f"what is the opposite of {b} ? it is {a} .")
    for a, n in ANIMALS:
        s.append(f"the {a} says {n} .")
        s.append(f"what does the {a} say ? it says {n} .")
    for a, c in COLORS:
        s.append(f"the {a} is {c} .")
        s.append(f"what color is the {a} ? it is {c} .")
    for i, j in itertools.product(range(1, 10), repeat=2):
        if i + j <= 10:
            s.append(f"{NUMS[i-1]} plus {NUMS[j-1]} is {NUMS[i+j-1]} .")
            s.append(f"what is {NUMS[i-1]} plus {NUMS[j-1]} ? it is {NUMS[i+j-1]} .")
    return s

# ---------------------------------------------------------------- model
D, NH, H, NL, TMAX = 32, 4, 128, 2, 14
DH = D // NH

def init_params(V, rng):
    def w(*shape, s=0.1): return rng.normal(0, s, shape)
    p = {"tok": w(V, D), "pos": w(TMAX, D), "lnf_g": np.ones(D), "lnf_b": np.zeros(D),
         "out_w": w(D, V), "out_b": np.zeros(V)}
    for l in range(NL):
        p.update({f"l{l}_ln1_g": np.ones(D), f"l{l}_ln1_b": np.zeros(D),
                  f"l{l}_wq": w(D, D), f"l{l}_wk": w(D, D), f"l{l}_wv": w(D, D), f"l{l}_wo": w(D, D),
                  f"l{l}_ln2_g": np.ones(D), f"l{l}_ln2_b": np.zeros(D),
                  f"l{l}_w1": w(D, H), f"l{l}_b1": np.zeros(H), f"l{l}_w2": w(H, D), f"l{l}_b2": np.zeros(D)})
    return p

def ln_fwd(x, g, b):
    mu = x.mean(-1, keepdims=True); var = x.var(-1, keepdims=True)
    inv = 1.0 / np.sqrt(var + 1e-5); xh = (x - mu) * inv
    return xh * g + b, (xh, inv, g)

def ln_bwd(dy, c):
    xh, inv, g = c
    dxh = dy * g
    dx = inv * (dxh - dxh.mean(-1, keepdims=True) - xh * (dxh * xh).mean(-1, keepdims=True))
    return dx, (dy * xh).reshape(-1, dy.shape[-1]).sum(0), dy.reshape(-1, dy.shape[-1]).sum(0)

def split(x):  # B,T,D -> B,NH,T,DH
    B, T, _ = x.shape
    return x.reshape(B, T, NH, DH).transpose(0, 2, 1, 3)
def merge(x):
    B, _, T, _ = x.shape
    return x.transpose(0, 2, 1, 3).reshape(B, T, D)

def forward(p, ids):
    B, T = ids.shape
    x = p["tok"][ids] + p["pos"][:T]
    mask = np.triu(np.ones((T, T), bool), 1)
    caches = []
    for l in range(NL):
        g = lambda n: p[f"l{l}_{n}"]
        h1, c1 = ln_fwd(x, g("ln1_g"), g("ln1_b"))
        q, k, v = split(h1 @ g("wq")), split(h1 @ g("wk")), split(h1 @ g("wv"))
        s = q @ k.transpose(0, 1, 3, 2) / np.sqrt(DH)
        s = np.where(mask, -1e9, s)
        s = s - s.max(-1, keepdims=True); a = np.exp(s); a /= a.sum(-1, keepdims=True)
        ctx = merge(a @ v)
        xm = x + ctx @ g("wo")
        h2, c2 = ln_fwd(xm, g("ln2_g"), g("ln2_b"))
        pre = h2 @ g("w1") + g("b1"); m = np.maximum(pre, 0)
        xn = xm + m @ g("w2") + g("b2")
        caches.append((x, h1, c1, q, k, v, a, ctx, xm, h2, c2, pre, m))
        x = xn
    hf, cf = ln_fwd(x, p["lnf_g"], p["lnf_b"])
    logits = hf @ p["out_w"] + p["out_b"]
    return logits, (ids, caches, x, hf, cf)

def loss_and_grads(p, ids, targets):
    logits, (ids, caches, xlast, hf, cf) = forward(p, ids)
    B, T, V = logits.shape
    z = logits - logits.max(-1, keepdims=True); pr = np.exp(z); pr /= pr.sum(-1, keepdims=True)
    valid = targets >= 0
    n = valid.sum()
    tt = np.where(valid, targets, 0)
    loss = -(np.log(np.take_along_axis(pr, tt[..., None], -1)[..., 0] + 1e-12) * valid).sum() / n
    dl = pr.copy()
    np.put_along_axis(dl, tt[..., None], np.take_along_axis(dl, tt[..., None], -1) - 1, -1)
    dl *= valid[..., None] / n
    gr = {k: np.zeros_like(v) for k, v in p.items()}
    gr["out_w"] = hf.reshape(-1, D).T @ dl.reshape(-1, V); gr["out_b"] = dl.reshape(-1, V).sum(0)
    dx, gr["lnf_g"], gr["lnf_b"] = ln_bwd(dl @ p["out_w"].T, cf)
    for l in reversed(range(NL)):
        g = lambda n: p[f"l{l}_{n}"]
        x, h1, c1, q, k, v, a, ctx, xm, h2, c2, pre, m = caches[l]
        P = f"l{l}_"
        gr[P+"w2"] = m.reshape(-1, H).T @ dx.reshape(-1, D); gr[P+"b2"] = dx.reshape(-1, D).sum(0)
        dpre = (dx @ g("w2").T) * (pre > 0)
        gr[P+"w1"] = h2.reshape(-1, D).T @ dpre.reshape(-1, H); gr[P+"b1"] = dpre.reshape(-1, H).sum(0)
        dh2 = dpre @ g("w1").T
        dxm_ln, gr[P+"ln2_g"], gr[P+"ln2_b"] = ln_bwd(dh2, c2)
        dxm = dx + dxm_ln
        gr[P+"wo"] = ctx.reshape(-1, D).T @ dxm.reshape(-1, D)
        dctx = split(dxm @ g("wo").T)
        da = dctx @ v.transpose(0, 1, 3, 2); dv = a.transpose(0, 1, 3, 2) @ dctx
        ds = a * (da - (da * a).sum(-1, keepdims=True)) / np.sqrt(DH)
        dq = ds @ k; dk = ds.transpose(0, 1, 3, 2) @ q
        dq, dk, dv = merge(dq), merge(dk), merge(dv)
        h1f = h1.reshape(-1, D)
        gr[P+"wq"] = h1f.T @ dq.reshape(-1, D); gr[P+"wk"] = h1f.T @ dk.reshape(-1, D); gr[P+"wv"] = h1f.T @ dv.reshape(-1, D)
        dh1 = dq @ g("wq").T + dk @ g("wk").T + dv @ g("wv").T
        dx_ln, gr[P+"ln1_g"], gr[P+"ln1_b"] = ln_bwd(dh1, c1)
        dx = dxm + dx_ln
    np.add.at(gr["tok"], ids, dx)
    gr["pos"][:ids.shape[1]] += dx.sum(0)
    return loss, gr

# ---------------------------------------------------------------- data
def build():
    sents = corpus()
    words = sorted({w for s in sents for w in s.split()})
    vocab = ["<bos>", "<unk>"] + words
    idx = {w: i for i, w in enumerate(vocab)}
    seqs = [[0] + [idx[w] for w in s.split()] for s in sents]
    assert max(map(len, seqs)) <= TMAX, max(map(len, seqs))
    X = np.zeros((len(seqs), TMAX), int); Y = -np.ones((len(seqs), TMAX), int)
    for i, s in enumerate(seqs):
        X[i, :len(s)] = s; Y[i, :len(s)-1] = s[1:]
    return sents, vocab, idx, X, Y

def greedy(p, vocab, idx, prompt, n=12):
    ids = [0] + [idx.get(w, 1) for w in prompt.split()]
    out = []
    while len(ids) < TMAX and len(out) < n:
        lg, _ = forward(p, np.array([ids]))
        t = int(lg[0, -1].argmax()); out.append(vocab[t]); ids.append(t)
        if vocab[t] == ".": break
    return " ".join(out)

def gradcheck():
    rng = np.random.default_rng(1)
    sents, vocab, idx, X, Y = build()
    p = init_params(len(vocab), rng)
    for k in p:  # randomise so zeros/ones don't hide bugs
        p[k] = p[k] + rng.normal(0, 0.05, p[k].shape)
    xb, yb = X[:6], Y[:6]
    _, gr = loss_and_grads(p, xb, yb)
    worst = 0
    for k in p:
        for _ in range(3):
            i = tuple(rng.integers(0, s) for s in p[k].shape)
            old = p[k][i]; e = 1e-6
            p[k][i] = old + e; lp, _ = loss_and_grads(p, xb, yb)
            p[k][i] = old - e; lm, _ = loss_and_grads(p, xb, yb)
            p[k][i] = old
            num = (lp - lm) / (2 * e); ana = gr[k][i]
            rel = abs(num - ana) / max(1e-8, abs(num) + abs(ana))
            worst = max(worst, rel if abs(num) + abs(ana) > 1e-7 else 0)
            if rel > 1e-4 and abs(num) + abs(ana) > 1e-7: print("MISMATCH", k, i, num, ana)
    print("gradcheck worst relative error:", worst)

def train(steps=4000, lr=3e-3, seed=0):
    rng = np.random.default_rng(seed)
    sents, vocab, idx, X, Y = build()
    p = init_params(len(vocab), rng)
    m = {k: np.zeros_like(v) for k, v in p.items()}; v2 = {k: np.zeros_like(v) for k, v in p.items()}
    for t in range(1, steps + 1):
        sel = rng.choice(len(X), 64, replace=False)
        loss, gr = loss_and_grads(p, X[sel], Y[sel])
        cur = lr * min(1, t / 100) * (0.5 * (1 + np.cos(np.pi * t / steps)) * 0.95 + 0.05)
        for k in p:
            m[k] = 0.9 * m[k] + 0.1 * gr[k]; v2[k] = 0.999 * v2[k] + 0.001 * gr[k] ** 2
            p[k] -= cur * (m[k] / (1 - 0.9 ** t)) / (np.sqrt(v2[k] / (1 - 0.999 ** t)) + 1e-8)
        if t % 250 == 0: print(t, round(float(loss), 4), flush=True)
    return p, sents, vocab, idx

def main():
    if "--check" in sys.argv: return gradcheck()
    p, sents, vocab, idx = train()
    # accuracy: greedy completion of every prompt (text before the answer) must reproduce the sentence
    ok = 0; bad = []
    for s in sents:
        w = s.split()
        cut = len(w) - 2  # prompt = all but "<answer> ."
        got = greedy(p, vocab, idx, " ".join(w[:cut]))
        if got == " ".join(w[cut:]): ok += 1
        else: bad.append((s, got))
    print(f"greedy accuracy {ok}/{len(sents)}"); [print("  bad:", b) for b in bad[:10]]
    r = lambda a: [round(float(x), 4) for x in a.reshape(-1)]
    data = {"config": {"d": D, "heads": NH, "hidden": H, "layers": NL, "maxLen": TMAX, "vocab": len(vocab)},
            "vocab": vocab, "params": {k: {"shape": list(v.shape), "data": r(v)} for k, v in p.items()}}
    with open("../model-data.js", "w") as f:
        f.write("// Generated by train/train.py - do not edit by hand.\nwindow.MODEL_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")
    # reference outputs for JS parity test
    ids = [0] + [idx[w] for w in "what is two plus three ? it is".split()]
    lg, _ = forward(p, np.array([ids]))
    json.dump({"ids": ids, "logits_last": r(lg[0, -1])}, open("reference.json", "w"))

if __name__ == "__main__": main()
