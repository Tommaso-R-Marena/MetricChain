#!/usr/bin/env python3
"""P9 step 8 -- at twelve residues, my chains with STATE-INDEPENDENT constants against the coordinator's forms.

On Lys5 the brackets built from P8's constants through my chains (p9lib.form_tables, resolved=False, plus P6's
allowances as p9_05_brackets.fp_parts allocates them) equal the coordinator's recipe to every printed digit.  At twelve
residues only the coordinator's recipe was run as a model.  Here the two PENALTY FUNCTIONS are compared directly, without
a model: at uniformly random states,
    pen_mine(x) = [my chain with P8's constants](x) + [P6's allowances, allocated as in p9_05_brackets.py](x)
    pen_ref(x)  = sum_i gs_i s_i + sum_{i<j} g2_ij s_i s_j + sum eta_ijk s_i s_j s_k   with (gs, g2, eta) from
                  p6lib.site_form / banded_pair_form / window_model.triple_form_two_windows  (the coordinator's recipe).
They must agree up to the allowances the coordinator's recipe adds for the rounding of its sums (1e-12 Gamma per sum).
usage: python3 -B p9_08_chaincheck.py SEQ M      writes logs/chaincheck_<tag>_m<M>.log"""
import sys
from p9lib import *

seq, m = sys.argv[1], int(sys.argv[2]); bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau); w = 7; M = m - 1
log = Log(os.path.join(LOGS, f"chaincheck_{tag}_m{m}.log"))
log(f"=== p9_08_chaincheck {seq} on {bb}, order {m}, band {w}; started {now()}")
LD = Loaded(os.path.join(OUT, f"tables_{tag}_m{m}_w{w}.npz")); n, k, x0 = LD.n, LD.k, LD.x0; subs = LD.TB[1].subs; chat = LD.TB[1].sab
phi1, psi1, psi2 = L.fp_tables(n, k, x0, M); tris = T9.window_triples(n, w); zn, znn = np.zeros(n), np.zeros((n, n))
Gam = float(chat.sum()); S = np.zeros(n); Gp = np.zeros((n, n)); H = {tr: 0.0 for tr in tris}
for T, v in zip(subs, chat):
    for i in T: S[i] += v
    for i, j in itertools.combinations(T, 2): Gp[i, j] += v; Gp[j, i] += v
    for tr in itertools.combinations(T, 3):
        if tr in H: H[tr] += v
absA = 1e-12 * Gam
rng = np.random.default_rng(2024); X = np.stack([rng.integers(0, k[i], size=5000) for i in range(n)], axis=1)
s = (X != np.array(x0)[None]).astype(float)
for form in "SBT":
    if form == "S":
        gs, g2, eta = L.site_form(n, m, S, phi1), znn, None; fp = (phi1.copy(), znn)
    elif form == "B":
        gs, g2 = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absA); eta = None; fp = L.banded_pair_form(n, m, w, zn, znn, psi1, psi2, 0.0)
    else:
        gs, g2, eta = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w, Gp, H, psi1, psi2, absA, absA); fp = L.banded_pair_form(n, m, w, zn, znn, psi1, psi2, 0.0)
    ref = s @ gs + 0.5 * np.einsum("ni,ij,nj->n", s, g2, s)
    if eta:
        for (i, j, l), v in eta.items():
            ref += v * s[:, i] * s[:, j] * s[:, l]
    mine = pen_value(X, *form_tables(LD.TB[1], form, w, resolved=False, const=chat)) + s @ fp[0] + 0.5 * np.einsum("ni,ij,nj->n", s, fp[1], s)
    dev = np.abs(mine - ref); rel = dev / np.maximum(ref, 1e-300)
    log(f"    form {form}: 5000 uniformly random states ({s.sum(1).mean():.1f} sites off the anchor on average); penalty of the coordinator's recipe: mean {ref.mean():.6g} kcal/mol; "
        f"largest deviation of my chain {dev.max():.2e} kcal/mol (relative {rel.max():.1e}); my chain below the recipe by more than 1e-9 relative at {int((mine < ref * (1 - 1e-9)).sum())} states")
log.done()
