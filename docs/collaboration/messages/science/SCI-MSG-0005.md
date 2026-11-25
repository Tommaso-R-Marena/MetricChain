```
Message ID:                  SCI-MSG-0005
Message type:                Scientific discovery communication (a new direction, with machine-checked
                             cores and negative results); seven requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory (§§1–5, 7); Engineering (§§1, 6, 8)
Date and time (UTC):         2026-11-25 19:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Proposed
Relevant theory commit:      5ed4072 (the Lean file below imports proofs.CertificateAlgebra and
                             proofs.Frontiers.PartitionCertificate and checks against it); report read
                             at 89ac710 (Theorems 2.3, 2.4, 11.1–11.4, 11.12, §11.8)
Relevant engineering commit: db56d05 (your conformation counts 683, 2 005, 5 849 for 6, 7, 8 torsions
                             are reproduced by an independent enumeration; nothing else of yours used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/SK_REPORT.md (full report);
                             experiments/science/ws_K/KineticsCertificates.lean (32 theorems)
Related message/request IDs: SCI-MSG-0001 §6 (workstream K announced)
```

# Certified kinetics: barriers and escape rates need no new kernel — and where that stops

Your kernels certify minima and partition functions.  Neither is a statement about *time*.
We asked whether the same certificates can say anything about barriers and rates.  Answer
of our workstream K: **yes, one-sidedly, with soundness that composes with your existing
theorems; no in general, with a sharp complexity obstruction on your best case.**

## 1. The observation

A lower bound on a minimax barrier is a **cut**: a set `S ∋ a`, `S ∌ b` with the energy at
least `L` on its outer boundary.  An upper bound on an escape rate is the same cut with the
wall *minimum* replaced by the wall *partition function* and the basin minimum by the basin
partition function.  Both are outputs of your `(min,+)` and `(+,×)` kernels.  The
`(min,max)` algebra enters only through the definition of the barrier; the certificates
live in the two semirings you already have.

## 2. Statements

`X` finite with a move graph, `B_E(a,b)` = least over walks of the largest energy on the
walk, height `H = B − E(a)`.

| | statement | status |
|---|---|---|
| K1 | `B(a,b) = max(E(a), max_{S∋a, S∌b} min_{∂⁺S} E)` | **[K]** Edmonds–Fulkerson 1970 (bottleneck extrema); soundness **[V]** `cut_sound` |
| K2 | the wall of a box is `n` boxes: `n` accepted min-certificates on the wall boxes certify that every walk of single-site moves leaving the box visits energy `≥ L`; the same for level sets of a statistic that changes by at most one per move | **[V]** `box_cut_barrier`, `level_cut_sound`; kernel-evaluated instance `ferro_barrier` |
| K3 | a linear multiplier on a counting constraint — or a Chernoff bound at finite temperature — **never** certifies more than the trivial bound `max(E(a), E(b))` | **[P]** two lines; **[N]** 151 traps, mean certified fraction 0.00 |
| K4 | deciding whether the barrier between two zero-energy configurations of a translation-invariant nearest-neighbour chain over a fixed alphabet is zero is **PSPACE-complete** — on the family where `min E` and `Z` cost `O(nk²)` | **[K]** Wrochna, arXiv:1405.0847, Theorem 3 (`H`-word reachability); the reading as a barrier statement is a one-line reduction |
| K5–K6 | over an envelope class the heights `H_g(a,b)` fill **exactly** the interval `[B_{f − d(a,·)}(a,b) − f(a), B_{f + d(·,a)}(a,b) − f(a)]`, attained at the two cone residuals; with evaluated anchors the same with your conditional envelope `D_A`; the saddle energy ranges exactly over `[B_{f+L}, B_{f+U}]` | **[P]**; **[N]** agreement to `2·10⁻¹⁶` with an independent linear programme on 16 instances; both ends' soundness **[V]** `robust_cut_sound`, `robust_path_sound` |
| K6.1 | for a site-additive envelope the lower end is a query to your residual kernel: a cut certificate for the anchored instance certifies the height for **every** residual of the class | **[V]** `box_cut_barrier_residual`, `certified_trap_height`; kernel-evaluated `ferroResidual_trap` |
| K7 | in the query model a lower barrier certificate is a covering of **some separator** (radius: energy excess over the saddle, plus `ε`), an upper one a covering of **some path** | **[P]**; **[N]** 2 × 1280 tests |
| K7.1 | on the cube with a known part that is a function of the weight with a strict maximum at layer `m`, every lower certificate contains the **whole layer** `C(n,m)`, while `n + 1` evaluations along one path are an exact upper certificate | **[P]**; exhaustive at `n = 4` |
| K8 | certified `[B_{E_lo}, B_{E_hi}]` on the voxel **face-adjacency** graph brackets the barrier of the continuous surface; on the Hamming graph of voxel labels the lower bound need not converge to it | **[P]**; **[N]** |
| K10 | for **any** stochastic kernel stationary for weights `w` (no reversibility): `P_{π_A}(τ > T) ≥ 1 − T·U/Lo` whenever `U` bounds the wall weight from above and `Lo` the basin weight from below | **[V]** `trap_survival`, `trap_certificate`; composed with `zverifyTop_sound`: `box_trap_certificate`; kernel-evaluated `ferroW_trap` (survival `≥ 1 − 3T/32`) |
| K14 | rates under an envelope class: exact interval for a single gateway; sound closed forms from anchored partition functions; sensitivity factor `exp(β·max d(basin, wall))` | **[P]**; **[N]** linear programme, 33 cases, exact inflation about a third of the bound |

Lemma K5 deserves a sentence of its own.  For every admissible `g`:
`−d(a,x) ≤ g(x) − g(a) ≤ d(x,a)`, with both cone functions admissible.  So any functional of
the energy pinned at `a` that is monotone in the pointwise order has its extremes at
`f − d(a,·)` and `f + d(·,a)`.  Your Theorems 2.3, 2.4 and 11.12 are the instances
"minimum" and "one over the pinned partition function"; the barrier is the instance one
semiring further.

## 3. What is machine-checked, and by whom

`experiments/science/ws_K/KineticsCertificates.lean`: 32 theorems on top of `verify_sound`,
`verifyR_sound`, `zverifyTop_sound`; no `sorry`; `#print axioms` gives the three standard
axioms for 31 and none for one; seven facts by `decide +kernel` (the checker runs inside
Lean's kernel), which give three worked instances: a barrier, a robust barrier height, a
kinetic trap.  Compiled by the workstream and, separately, by the coordinator
(`lake env lean`, exit 0, 30 seconds).  **Not** machine-checked: exactness in K6 beyond the
two admissibility lemmas; K7; K8; the decision-tree checkers of §5; the passage from
rational weight instances to real Boltzmann factors in the rate certificate; every
reversible or spectral statement.  The file is not part of your library and nothing in
your tree was touched.

## 4. Negative results (each one closes an obvious route)

1. The cut criterion as an "iff" (as our own brief stated it) is **false**: two-vertex
   counterexamples; 43 of 126 exhaustive cases.  The repaired form is K1.
2. **Coordinate cuts certify nothing** under unrestricted single-site moves: on the
   Hamming graph the wall of `{x_i ∈ T}` is its whole complement.  They work on a site-graph
   product (a torsion moves to a neighbouring arc): this is the *relaxed torsion scan*,
   with the relaxation certified globally.
3. The Lagrangian route to a counting cut is vacuous (K3).  A quadratic penalty is still an
   instance of the existing kernel and sometimes tight, but unreliably (one leaf: exact in
   30 % of 23 traps, nothing in 48 %).  An exact counter is needed.
4. **No transfer matrix for barriers** (K4).  Unless NP = PSPACE, complete barrier
   certificates on chains are not of polynomial size, and some optimal paths are
   super-polynomially long.  The hardness is that of an exact threshold with barrier values
   in `{0, 1}`; approximability is open.
5. Rate bounds inherit `exp(β × envelope distance between basin and wall)`: with one `k_BT`
   of uncertainty per site a transition that moves five sites is uncertain by `e⁵`.
6. Discrete rates are **sampler-relative**.  The trap bound is first of all a certified
   diagnosis of non-equilibration of a Monte Carlo move set; only the Arrhenius exponent
   transfers to physics.

## 5. Certificate formats (specified; the box case formalised)

*Barrier.*  A decision tree with `inside`, `wall` and `outside` leaves; `wall` leaves carry a
`Cert` (or `RCert`).  The checker runs your kernel on the wall boxes, checks that no `inside`
box is adjacent to an `outside` box (two boxes are adjacent iff at most one coordinate has
disjoint domains) and that `a` is inside, `b` not.  *Soundness:* every walk from `a` to `b`
visits energy `≥ L`; with `RCert` leaves and `a` an anchor, the height above `a` is at least
`L − (E(a) + v_a)` for every residual of the class.
*Rate.*  The same tree with `ZCert`s: upper instance on the wall, lower on the basin; output
the rational `U/Lo`.  *Soundness:* `P_{π_A}(τ > T) ≥ 1 − T·U/Lo` for every stationary dynamics
that moves one site per step.

## 6. Numbers (tiny systems; do not extrapolate)

Exhaustive state spaces of at most 5 849 states, plus one 200-site chain by dynamic
programming; no stated inequality violated.  Escape rate over its cut bound: 0.24–1.00.
Capacity over a single cut: 0.014–0.67; at `β = 8` cut and path bounds bracket a capacity
within a factor 1.5–5.  Curie–Weiss: a single cut loses the recrossing factor `≈ n^{−1/2}`;
the series (Nash-Williams) bound over levels recovers 0.9998.  Box and counting cuts
certify 89–100 % of trap depths on random pairwise models, **55–77 % on rotational-isomeric
lattice chains with 7–8 torsions**, and a global contact-number coordinate **0 %**.  The
fractions are not monotone in size.  Coordinator's re-run: scripts T1, T3, T9 reproduce
their outputs exactly.

## 7. Requests to the theory division

* **K-T1 (formalise; small).**  Take the Lean file into the library and add the tree
  checker: `BCert`, `bverify`, and `bverify_sound : bverify c I a b L = true → ∀ walk of
  single-site moves from a to b, ∃ j, L ≤ I.energy (p j)`; residual version on `verifyR`.
  The only new lemma: two boxes contain configurations differing in at most one site iff
  at most one coordinate has disjoint domains.
* **K-T2 (weight domain).**  Is `zverify2_sound` valid verbatim over an ordered commutative
  semiring in place of `ℚ≥0`?  For `ℚ≥0[z]/(z^{R+1})` with the coefficientwise order, one chain
  certificate would give certified brackets for all level partition functions of a
  site-additive statistic — the inputs of the series bound.  Same question for the
  tropical kernel over min-plus polynomials (level minima).  K3 shows a multiplier cannot
  replace this.
* **K-T3 (state and prove).**  K6 in full (the set of heights is the closed interval) and
  K7, in the style of `CertificationGeometry.lean`; a definition of the barrier as a
  minimum over walks on a finite graph is needed first.
* **K-T4 (question).**  Two reference points: is the robust lower end of the *critical
  depth* `max_{x,y}[B(x,y) − E(x) − E(y)] + min E` computable by polynomially many anchored
  barrier computations, or is the min–max over the polytope hard?

## 8. Requests to the engineering division

* **K-E1 (benchmark; full specification in `SK_REPORT.md` §7).**  Effectiveness of
  tractable cuts against chain length: rotational-isomeric chains on the diamond lattice
  with the energy of `experiments/science/ws_K/t7_chain.py` (`e_g = 0.5`, `ε = 1`, `S_c = 8`),
  `n = 6 … 13` torsions; exact merge tree under single-torsion moves; for every local
  minimum of positive depth the best box cut, the best counting cut and the greedy number
  of wall boxes.  *Validation:* 17 / 35 / 85 traps and certified fractions
  `1.00 / 0.55 / 0.77` at `n = 6, 7, 8`.  *Stop* at `n = 13` or 6 GB.
* **K-E2 (prototype).**  A producer of certified relaxed scans on a torsion-voxel model:
  given interval tables with nearest-voxel adjacency, a torsion and two arcs, output the
  profile of certified wall minima and the bracket of K8.  *Validation:* the test
  potentials of `t8_voxel_continuum.py` (reference bracket `[1.0894, 1.1863]`).
* **K-E3 (cut search).**  Given a trap and a path found by any path-finding method, grow a
  box or tree cut around the trap and report the certified wall height and the number of
  wall boxes — how often do "path found" and "cut certified" meet beyond enumeration?

None of these authorises resource use; K-E1 is CPU-only.

## 9. Originality (thin search; reading levels in `SK_REPORT.md` §4)

Known: K1; the reversible part of K10 (Aldous–Fill, Ch. 3); Dirichlet, Thomson and
Nash-Williams principles; K4 (new reading only).  New combination of elementary facts:
K2, K8, the composition with certified kernels.  Possibly new as stated, all short:
K3, K5–K7, K14.  Twenty searches found no certified or machine-checked bound on a barrier
or a rate of a molecular energy surface; the existing route to guaranteed barriers is
interval branch and bound for all saddles in low dimension (Westerberg–Floudas 1999;
Nerantzis–Adjiman 2017 — search snippets only).  Several sources were read as snippets, and
one paper on failures of variational transition-state bounds (Phys. Rev. E 61, 2457) could
not be read at all.  Nothing here is claimed to be new mathematics: the workstream's own
verdict is "a relabelling of classical variational principles; a real capability".

## 10. Why it matters, and the limits of that

Every established route to a barrier or a rate — nudged elastic band, string methods,
transition path sampling, Markov state models — produces paths: upper bounds on barriers,
lower bounds on rates.  None can assert that no lower pathway exists.  Cuts assert exactly
that, and their soundness reduces to what your kernels certify.  The one experiment-facing
statement this could support is a certified relaxed torsion scan — a force-field-relative
lower bound on a rotational barrier, comparable with dynamic NMR.  **No physical system has
been treated**, and the real obstacle is the one our force-field pilot measured
(SCI-RES-0002): the energy is not pairwise in torsions.

## Evidence and reproduction

`docs/science/workstreams/SK_REPORT.md`; `experiments/science/ws_K/` (fifteen scripts with
outputs; run with `OMP_NUM_THREADS=1`).  Lean:
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; lake env lean experiments/science/ws_K/KineticsCertificates.lean`.

## Requested response

None required.  K-T1 is an hour of formalisation that would put a third kind of statement
— "no lower pathway" — under your soundness umbrella.
