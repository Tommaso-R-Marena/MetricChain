# Workstream A4 (launched 2026-11-26) — prior art for the Geometry division's Theorem L: a global stability bound of order `n²` for reconstructing a chain of points from its sequence-local distances

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date; there are now six
divisions, and the object of this workstream belongs to the Geometric Inference division, branch
`research/geometric-inference`).  This is an **originality review**, not a review of correctness: you are asked what is
in print, not whether their proof is right.  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_A4/` and its draft in `docs/science/workstreams/A4_REPORT.md`.*

## Why

The Geometry division asked for it (their GEOMETRY-MSG-0007 §1 and GEOMETRY-RES-0004 §5): our review of another
theorem of theirs (SCI-REV-0021, workstream R22) found it in print in dimension one after their own search had
classified the paper as "a relative" without reading the relevant statement.  For Theorem L their search was two
web searches and one paper read once through an automated fetch; they say themselves that "the statement is
elementary enough to be folklore in rod theory or in the literature on discretizable distance geometry".  The
research owner's directives ask for rigorous novelty evaluation and forbid presenting anything as new on a thin
search.

## The statement (read-only copies; do not use anything of their branch but these files)

`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/geo_ro_288b2de/`:
`LOCAL_DATA_STABILITY.md` (their note at commit `288b2de`: §2 Theorem K, §3 Theorem L with its proof, §5 their
prior-art paragraph with four addresses), `GEOMETRY-MSG-0007.md` §1, `PRIOR_ART.md`.

**Theorem L.**  `X`: `n ≥ 5` points in space; `P_i = [x_{i+1} − x_i, x_{i+2} − x_i, x_{i+3} − x_i]` the edge matrices of the
windows of four consecutive points; `τ = min_i σ_min(P_i) > 0` (no four consecutive points coplanar),
`D = max_i σ_max(P_i)`, `b` the longest bond.  If `Y` is **any** configuration of `n` points whose squared distances at
sequence separation at most 4 differ from those of `X` by at most `τ⁴/(73D²)` each, then for some isometry `g`

    ‖Y − gX‖_F ≤ 6.9 · (b/τ²) · n(n + 1) · ‖η‖₂,     η = the differences of squared distances at separation ≤ 3.

Nothing is assumed about `Y` (no closeness, no chain structure); the threshold does not depend on `n`.
Corollary L.1: any estimator that fits noisy data as well as the truth (a stress minimiser) is within
`13.8 (b/τ²) n(n + 1)‖ε‖₂`.  With Theorem K (c) (a lower bound of order `n²` on rod-like chains — a bending mode):
the stability constant of sequence-local distance data on helices is `Θ(n²)`.
*Their proof idea:* compare orthogonal frames of overlapping windows (a polar decomposition per window; the
separation-4 distance excludes a reflection between consecutive windows); frame errors **add** along the chain
because orthogonal maps preserve norms; positions are never reconstructed step by step.
*What they found:* Arias-Castro and Vishwanath, arXiv 2310.10900 — for lateration graphs a constant that is
exponential in the number of points in exactly this case.

## What to establish — three questions, in this order

**Q1.  Is the polynomial bound in print?**  A global (not infinitesimal) perturbation bound, polynomial in `n`, for
recovering a configuration from distances on a band graph / a `(d+1)`-lateration ordering in which each point is
attached to its immediate predecessors — or a statement of which it is a direct corollary.  Places to look, each
with **generic queries only** (see the rules):

1. *Arias-Castro–Vishwanath itself*, in full (arXiv abstract page, then the HTML or PDF): confirm or correct the
   Geometry division's reading — theorem numbers, the form of the constant, the sentence about tightness, whether
   any special case with a polynomial constant is stated (e.g. bounded "depth" of the lateration order, or a
   remark on chains).  Then **papers that cite it** (2024–2026).
2. *Sensor-network localisation and graph realisation with noise:* error propagation in trilateration and
   sequential localisation (Moore–Leonard–Rus–Teller 2004; Anderson, Shames, Mao, Fidan and co-authors on noisy
   localisation of globally rigid / trilateration graphs; Aspnes et al., "A theory of network localization");
   Javanmard–Montanari (localisation from incomplete noisy distances; bounds for geometric graphs, where a chain or
   strip is the thin case); semidefinite-programming localisation with stability bounds.
3. *Patch-based methods:* "as-synchronised-as-possible" localisation and global registration of patches
   (Cucuringu–Lipman–Singer; Chaudhury–Khoo–Singer, "global registration of multiple point clouds", with its
   stability theorem for lateration-type patch graphs); synchronisation over the orthogonal or Euclidean group on
   a **path** graph — where errors add along the path, which is their mechanism.
4. *Distance geometry of chains:* the discretizable molecular distance geometry problem (distances at sequence
   separation up to 3 plus pruning distances — exactly this data), geometric build-up algorithms and their error
   analyses (Dong–Wu; Sit–Wu–Yuan; Lavor–Liberti–Maculan–Mucherino and later interval versions): is there a
   stability or error-accumulation theorem, and is it exponential, polynomial or absent?
5. *Rigidity theory with constants:* quantitative global or universal rigidity; stiffness-matrix / rigidity
   eigenvalue bounds for band or "ladder" frameworks (the infinitesimal `n⁻⁴` eigenvalue of a truss beam is
   classical — say where it is stated); any *nonlinear* (finite-perturbation) statement.
6. *The continuous analogue:* the geometric rigidity estimate (Friesecke–James–Müller 2002) for thin domains and
   rods (Mora–Müller; later proofs with explicit constants; **discrete** versions — "discrete geometric rigidity",
   rigidity estimates for lattices or simplicial chains, Γ-limits of atomistic chains or discrete rods).  Is the
   `(L/h)²` scaling of the constant stated, and is there a discrete statement that implies Theorem L up to
   constants?

**Q2.  Is the lower bound (Theorem K (c)) in print in this form?**  Lower bounds for localisation error on thin or
chain-like networks (Cramér–Rao bounds for strips; "error accumulates quadratically along a chain"); the bending
mode argument for local distance data.  Their own note claims no novelty for K (a) and says K (b), (c) are
elementary; say what the nearest printed statements are.

**Q3.  The verdict**, for each of: Theorem L; Corollary L.1; the `Θ(n²)` statement — one of *in print as stated* /
*a direct corollary of a printed statement (name it, give the reduction in a few lines)* / *known in a different
setting, the transfer not in print* / *not found* — with the list of what you could **not** access and how thin the
basis of "not found" is.  A replacement text for their "Prior art" paragraph on Theorem L that claims no more than
you can support.

## Rules

Write only in `experiments/science/ws_A4/` (notes, `NOTES.md` from the first minute, a `search_log.md` with every
query and every address opened) and `docs/science/workstreams/A4_REPORT.md`.  No state-changing git; no subagents;
no computation is needed beyond perhaps checking a reduction by hand.
**Queries must be generic:** nothing of this project — no project, division, branch or person names, no theorem
labels of ours or theirs, no text copied from the files — may be put into a search query or a fetched address.
**Never fabricate** a citation, a statement number, a formula or a quotation.  For every source give its
**reading level**: *opened in full* (say which sections) / *abstract only* / *search summary only* / *from memory*.
A theorem you attribute to a paper must come from text you opened; otherwise say "according to the abstract" or
"according to a search summary".  Quote the decisive sentences (short quotations, with where they stand).  If a
paper is behind a paywall, say so and look for an arXiv or author version; do not guess its content.
**If a tool declines an action, do not work around it: keep everything in `NOTES.md` and return the findings as
text in your hand-back, with a line "Tool actions declined".  Do not delete files with wildcards or `rm -r`.**
A time written into a file is read from the clock at that moment.  This is an internal review by an AI agent,
not external peer review; say so in the report.

## The report

(0) Verdict in ten lines (Q3).  (1) The statement as you understand it and the keywords under which it would be
found.  (2) Source by source: what it proves, in its own setting, with the reading level and the decisive
quotation; how far it is from Theorem L.  (3) The table of Q3.  (4) A replacement text for their prior-art
paragraph.  (5) The search log (queries, addresses, what was not accessible); your own errors.  Hand back a
summary of at most fifty lines that includes **every address you opened**.
