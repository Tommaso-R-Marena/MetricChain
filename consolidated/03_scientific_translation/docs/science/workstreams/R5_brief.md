# Workstream R5 — independent review SCI-REV-0005: theory report §11.26 (heteropolymer product landscapes; the dictionary with channel coding)

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_R5/`; your report: `docs/science/workstreams/R5_REPORT.md`.

**Where the object under review is.**  The theory division published it at its commit
`89ac710`, *after* our branch was created; it is therefore **not** in `/home/user/MetricChain`
but in the read-only checkout

    /tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro

(call it `thy_ro`).  There: `docs/THEORY_REPORT.md` §11.26 (from line 6138;
`grep -n '^### 11.26'`), `docs/workstreams/W_REPORT.md` (the workstream report behind it, 1185
lines; §5 lists every changed step of the "proof by transfer"), `docs/workstreams/W_brief.md`,
`proofs/Frontiers/RenyiCentre.lean`, `experiments/coordinator_checks/sites_W/` (the coordinator's
re-computations, `wv_lib.py`), `experiments/workstreams/W/`, `docs/DEAD_ENDS.md` D52,
`docs/collaboration/messages/theory/THY-MSG-0011.md`,
`docs/collaboration/requests/theory/THY-REQ-0011.md` (the request this review answers: item A1).

## The request (theirs, verbatim in substance)

"**Theory report §11.26, Theorem 11.99** (the site function is a Rényi capacity; the
dictionary with channel coding) and **Theorem 11.101** (the adaptive exponent for several
site types and any alphabets — a proof *by transfer*: `docs/workstreams/W_REPORT.md` §5 lists
every changed step).  The identity can be checked numerically in minutes
(`experiments/coordinator_checks/sites_W/wv_lib.py`); the transfer cannot, and nobody but its
author has read it line by line."  Status claimed: a workstream's paper proofs, re-computed
by the coordinator; **not refereed**; two elementary steps machine-checked
(`RenyiCentre.lean`).

Claims in outline (read the exact statements): a fixed sequence of site types; type `j` has
`q_j` letters, a site law `π_j`, a site envelope `d_j` (possibly asymmetric); residual `ψ` with
`ψ(x) − ψ(y) ≤ Σ_i d(x_i, y_i)`; target `ln E_π e^{−ψ}` to accuracy `ε₁n`.  (a) hinted exponent at
the hardest instance = adaptive exponent without a hint: `R(e) = max_{0≤t≤1}[F*(t) − te]`,
`F* = Σ_j λ_j F*_j`; non-adaptive `θ_na = R∘S⁻¹`, `S(e) = e + R(e)`; one common slope `t` across site
types.  (b) `F*_j(t) = (1 − t)·C_t`, `C_t` the Rényi capacity of order `t` of the "vertex channel"
(vertices `φ` of the site's Lipschitz polytope ↦ Gibbs laws `π_φ ∝ π_j e^{−φ}`); `a_j` the Shannon
capacity; with Gallager's `E_0(ρ) = ρ Σ_j λ_j C_{1/(1+ρ)}`: `θ_na` is the inverse of the
sphere-packing exponent, and adaptivity (or a hint) certifies `E_sp(θ) − θ`.  (c) reference
numbers.  (d) three two-letter statements that fail beyond two letters (non-concave site
function; a field does not always help; the uniform site law is not always hardest;
crossings at `e^u = k(k−1)`).

## What a review here means

1. **Theorem 11.99 (the identity).**  Re-derive `F*_j(t) = (1 − t)C_t` yourself from the
   definition of the site function (find that definition and its role in the lower and
   upper bounds first — Theorems 11.95, 11.97, 11.98).  Which definition of Rényi capacity
   and of Rényi divergence (order `t ∈ (0,1)`; Sibson's / Csiszár's / Augustin's — they
   differ) makes the identity true?  Is the stated convex programme
   `max_M −t ln Σ_a (Σ_φ M(φ)π_φ(a)^t)^{1/t}` the right one for that definition?  Check the limits
   `t → 1` (Shannon capacity) and `t → 0`.  Check the claimed dictionary with Gallager's `E_0`
   and the sphere-packing exponent with exact conventions (`ρ = (1−t)/t`?), and the "parallel
   channels" rule for several site types.  **Replicate numerically with your own
   implementation** (not `wv_lib.py`): the reference numbers of THY-MSG-0011 §1(c) for the
   three-state site (path envelope with steps 0.8, 1.6; site law (0.5, 0.3, 0.2):
   `E = 0.400622`, `a = 0.294791`, `R(0) = 0.089589`, `R(0.3E) = 0.043375`, `θ_na(0.3E) = 0.066899`), the
   uniform cube as a sanity check (binary symmetric channel with crossover `1/(1+e^u)`), and
   at least one of the "fails beyond two letters" statements of (d), including the exact
   crossing `e^u = k(k−1)`.
2. **Theorem 11.101 (the transfer).**  This is the part nobody has read.  Go through
   `W_REPORT.md` §5 step by step against the two-letter proofs it transfers (theory report
   §11.18–11.20: Theorems 11.52, 11.54, 11.56, 11.58, 11.63, 11.64).  For each changed step:
   is the new statement true, is the argument given complete, what does it silently
   require (e.g. finitely many site types with positive fractions; envelope asymmetry;
   non-concave site functions — which (d) says occur; a tail lemma relative to a
   reference instance for alphabets with more than two letters; an isoperimetric input —
   which one, and is it proved or cited?).  Classify: proved / proved with gaps (list) /
   not proved / false.  If the upper bound needs an isoperimetric or type-covering
   statement that is only asserted "by transfer", say exactly which.
3. **Lean match.**  `RenyiCentre.lean`: what do its theorems state, and which two "elementary
   steps" of Theorem 11.99 do they cover?  Vacuity, hypotheses.
4. **Headline vs theorem.**  THY-MSG-0011 and the README of `thy_ro` advertise "certification
   cost is a channel-coding exponent".  For which algorithm classes, accuracies and
   instance sets is each half (lower bound for every `n`; upper bound) actually proved?
5. **Originality** in one paragraph (workstream A1 is doing the deep search on the
   dictionary; note anything you recognise: Rényi capacity and the sphere-packing
   exponent (Gallager; Csiszár; Arimoto), compound channels, list decoding).

## Deliverable

`R5_REPORT.md` in the review format: claim examined; verification method; evidence inspected;
established findings; limitations; **critical / major / minor findings** (numbered, with
location, what is wrong, why it matters, suggested correction); originality assessment;
reproduction status (your values next to theirs); recommended corrective action;
unresolved questions.  If you find a real error, give the strongest true statement you can
prove in its place.  Final message to the coordinator: at most 600 words.
