# Workstream R7 — independent review and replication of the engineering division's results

Object reviewed: branch `research/ubuntu-engineering` at commit `a2f6dc781de05b642189a51d2ed88f94e8ed7026`
("`a2f6dc7`").  Every engineering file named below is cited by its path on that branch at that commit and
can be obtained with `git show a2f6dc7:<path>`.  My working copy of those files
(`experiments/science/ws_R7/eng_copy/`) is git-ignored and is not part of the science branch; it is
re-created by `experiments/science/ws_R7/make_eng_copy.sh`.  Everything of mine that is needed to
reproduce a number in this report is in `experiments/science/ws_R7/` (scripts `own_*.py`, `own_*.c`,
`x005_refit.py`, `x006_recount.py`, `check_*.py`, `rerun_engineering.sh`; outputs `out_*`, `rerun_logs/`;
the running log `NOTES.md`).

Three kinds of evidence are kept apart throughout:

* **REPLICATED** — recomputed with my own code, written from the model definition *before* I read the
  engineering implementation of that item (the order of events is in `NOTES.md`);
* **RE-RUN** — the engineering code at `a2f6dc7`, exported into a throw-away work tree outside the
  repository and executed here (`rerun_engineering.sh`);
* **READ** — read and checked for internal consistency (including recomputation from *their* stored
  files with my own code, which tests the document against the artifact, not the artifact).

Labels of COMMON rule 6: **[V]** machine-checked, **[P]** paper proof given here, **[K]** known and cited,
**[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.  Nothing here was machine-checked.

Contents: 1 verdicts (one paragraph, verdict table, classified findings) · 2 precise statements with
proofs · 3 numerics (3.1 generic chain, 3.2 lattice covers as certificates, 3.3 Harper closed form,
3.4 tail-function reduction, 3.5 statistics of X-005/X-006, 3.6 the record, 3.7 a control on non-ball
level sets) · 4 prior art and search log · 5 not settled · 6 next steps · 7 requests.

---

## 1. Verdicts

**In one paragraph.**  I found **no wrong number** in the engineering division's results.  Every
quantity I recomputed with my own code — the generic chain (conformations and profile classes for
5–14 torsions, the covering numbers of 5–11 torsions, the tie analysis, 60 entropy numbers), the
lattice class tables for 1–22 torsions, the single-flip constants up to 14 torsions, the closed form
for the uniform-cube hitting numbers (all 52 stored rows) — is identical to theirs, and their stored
outputs regenerate bit for bit wherever I re-ran their code at reduced size.  All 288 published
lattice covers are valid certificates; of the 263 cells published as optima, **254 are certified
here without trusting any solver's search** (241 by an exact LP-duality certificate, 13 more by my
own branch and bound with an exact certificate at every pruned node) and 9 remain optima by
HiGHS's branch and bound only; the other 25 cells are brackets.  The findings are about what the record
supports, not about values: (i) the sentence "two solvers agree on every cover / proved by HiGHS and
CP-SAT independently" rests on stored rows that no committed code produces — the committed driver
never runs the second solver on a cell the first one closes — and I could not reproduce a CP-SAT proof
with the one core I may use; (ii) ten lattice bracket ends and most generic ones are called
"certified" but are solver bounds, one to three above what is certified; (iii) "the excess decays
about like `1/√n`" is not what the X-005 data show (it decays faster; the exponent ½ is neither
established nor excluded), the search budget was cut at the two largest sizes without saying so, and
the `7·10⁶` "mean runs" are objective evaluations of an optimiser at the expectation level; (iv) the
off-lattice chain is *not* generic in the sense a floating-point treatment needs — its squared
distances are rational polynomials in `cos θ`, the "exact ties" are identities, and at 13 torsions
(the division's next size) one cell has 253 of them.  On the positive side the same structure shows
that the published off-lattice numbers are exact (covering numbers for `n ≤ 12`, class tables and
entropy numbers for `n ≤ 14`); the Harper reduction of ENG-RES-0008 §5
is correct as stated (re-derived, checked exhaustively on small cubes, and tested on a family with
non-ball level sets that the division had not tried: no claim violated, no worse instance); and the
total conformation counts of all 24 lattice tables, including the four produced on Modal, equal the
published series of diamond-lattice self-avoiding walks.

### 1.1 Verdict table

"Replicated" = own code written before reading theirs; "re-run" = their code executed here;
"read" = read, and where stated recomputed from their stored files with my own code.

| # | claim (source) | verdict | how | difference |
|---|---|---|---|---|
| 1 | generic chain: conformations and profile classes, `n = 5…14` (ENG-RES-0007 §3, -0009 §2) | **replicated** | `own_gen.py` | none |
| 2 | generic chain: 12-cell cover table, `n = 5…10` (72 cells incl. two open brackets) | **replicated** | `own_cover_table.py` | none (same two brackets, same ends) |
| 3 | generic chain: cover table, `n = 11` | 6 exact cells **replicated**; 6 brackets **consistent** | MILP (`L = 1/5`); own LP certificate + greedy (`L = 1`) | none in the values; 5 of the 6 lower ends are solver bounds, not certified ones |
| 4 | generic chain: cover table, `n = 12` | **consistency only**: my bounds agree with all 12 cells and my LP certificate equals 5 of the 6 published exact values; no cover of the published sizes constructed | own LP certificate + greedy | none |
| 5 | generic chain: "nearest tie"; five exact ties at `n = 11`, none elsewhere; classes `≥ 0.035` apart; hard-core margins | **replicated**, and explained | `own_ties*.py`; 60-digit re-evaluation | none |
| 6 | generic chain: distance entropy `σ(ρ)`, `n = 5…14`; pairs per bead | **replicated** | `own_entropy.py` | none (3 printed decimals) |
| 7 | generic-chain results carry the label "[X\*]" (floating point) | **strengthened**: exact (covers `n ≤ 12`; classes and entropy `n ≤ 14`) | Propositions G1–G3 | — |
| 8 | lattice class tables, `n = 1…22` (the tables of `n = 21, 22` were produced on Modal, job M-002) | **replicated** | `own_dia.c` | none (per class: count, fewest / most gauche) |
| 9 | lattice class tables, `n = 23, 24` (Modal job M-002) | totals **checked against the literature** (OEIS A001394 / 12, as for every `n ≤ 24`); classes **not examined** | `check_saw_counts_oeis.py` | none in the totals |
| 10 | the 288 lattice covers are covers of the stated sizes | **replicated** (certificates checked exactly) | `own_lattice_cert.py primal` | none |
| 11 | the 263 single lattice covering numbers are optima | **254 certified solver-independently**; 9 **not** (HiGHS only; one of them re-solved by HiGHS in my own formulation) | exact LP certificate (241); `own_certified_bb.py` (13) | none |
| 12 | "all 24 published covering numbers reproduced" | **replicated**, and certified | they are among the 241 | none |
| 13 | "two solvers agree on every cover"; "by HiGHS and CP-SAT independently for `n ≤ 18`" | **not reproducible from the repository; not confirmed** | re-run of the committed driver at `n = 14`: CP-SAT never called; CP-SAT with one worker on three cells: no proof | sentence vs record (finding M1) |
| 14 | lattice brackets, `n ≥ 19`: "`[certified lower bound, verified cover]`" | upper ends **replicated** (25 / 25); 15 certified lower ends **replicated**; 10 lower ends are solver bounds | `own_lattice_cert.py dual` | wording (finding m1) |
| 15 | lattice entropy table (ENG-RES-0002 §4), 50 cells | lower sides **replicated** where LP-certified (33 single values; all 10 bracket ends); upper sides **not checkable** (covers not stored); 7 values rest on branch and bound | `own_lattice_nets.py` | none |
| 16 | single-flip constants `c^{sf}` | `n = 3, 5, 8…14` **replicated**; `n = 15, 16` and the envelope-validity test **not examined** | `own_flip.c` | none |
| 17 | every trans/gauche pattern is realised (two-line proof) | **read**: proof correct | — | — |
| 18 | finite-size table and prose numbers of ENG-RES-0002, -0007 §2, -0009 §1 | **read**, recomputed from their stored tables | `check_eng_res_0002_prose.py` | three last-digit roundings |
| 19 | uniform-cube hitting numbers: closed form and table (ENG-RES-0006 §1) | **re-derived and replicated** (52 / 52 rows); their script **re-run**, byte-identical | `own_harper.py` | none |
| 20 | ENG-RES-0006 §2 (pricing as closure plus one budget row) | **not examined** (stated there as unimplemented analysis) | — | — |
| 21 | X-005: the generated tables of ENG-RES-0008 follow from the stored results | **re-run** (`make_tables --verify`); trend table rebuilt with own code | `x005_refit.py` | none |
| 22 | X-005: the stored search results are regenerated by the stated command | **re-run**: two cells bit-identical; all stored maximisers with `n ≤ 2000` re-evaluated | `rerun_engineering.sh … search`, `… recheck` | none |
| 23 | X-005: "no claim violated in 7 095 840 mean runs" | **read**: count and extremes agree with the stored files; what it means: Statement S1 | `check_record_numbers.py` | headline wording (m3) |
| 24 | X-005: "the excess decays about like `1/√n`" (digest) | **discrepancy with the data** (decays faster; Statement S2) | refit | finding m2 |
| 25 | X-005: "the flat instance is not the worst one" | **read + re-run**: the instances are in the class and the stored maximisers reproduce; correctness of the evaluator **not examined** (workstream R6) | — | none |
| 26 | X-005 §5: reduction of outer landscapes to tail functions (Harper) | **re-derived** [P] and checked numerically; scope note T(e); extra control on non-ball level sets **re-run** | `own_tail.py`, `rerun_eng_partial_shell.py` | none (correct as stated) |
| 27 | X-006: 585 000 literal runs without failure; "below `5.1·10⁻⁶` at 95 %, pooled" | **read**, recounted from the stored file; not re-run | `x006_recount.py` | none |
| 28 | X-001 (replication of the theory audit) | **not examined** | — | — |
| 29 | the tables of ENG-RES-0002, -0007, -0008, -0009 are generated from the artifacts | **re-run** (`make_tables --verify`, four documents) | | none |
| 30 | `python -m pytest tests/eng -q` | **re-run**: 128 passed | | — |

### 1.2 Findings, classified

**Critical** (a published result is wrong): **none found.**

**Major**

* **M1 — the two-solver validation cannot be regenerated, and what is stored does not show two
  proofs.**  *Where:* `docs/engineering/EXPERIMENT_REGISTER.md`, X-002, validation (vi);
  `docs/collaboration/responses/engineering/ENG-RES-0002.md` §1 ("Exactness"), §2 (note under the cover
  table), "Assumptions and limitations"; `docs/engineering/DEPENDENCY_MAP.md` ("minimum covers are
  optimal"); `src/metricchain_eng/chains/profile_cover.py`, `covering_number_P` (the loop over solvers);
  `experiments/eng/chain_cover/results/lattice_Sc12.json`, rows `n = 1…18`.  *What:* §3.2 (d).  *Effect
  on the numbers:* none that I could find — 254 of the 263 values are certified here without any
  solver's search, and the sampled others agree with HiGHS in my own formulation.  *Effect on the
  claim:* "proved by two independent solvers" is, on the evidence in the repository, "proved by HiGHS;
  a second solver once found covers of the same size".
* **M2 — the floating-point treatment of the off-lattice chain is at its limit at the next size.**
  *Where:* `src/metricchain_eng/chains/generic_chain.py` (`ROUND_DECIMALS = 8`, `TOL = 1e-9`);
  ENG-RES-0007 §3–§4; the plan in `docs/engineering/RESEARCH_LOG.md` ("covers of the generic chain at 13
  and 14 torsions").  *What:* §2.1, §3.1 — exact ties are identities and become frequent (253 in one
  cell at 13 torsions), the nearest non-tie is `2·10⁻⁸` at 14 torsions, and the entropy table of
  ENG-RES-0009 already contains 305 exact ties (`n = 9, 10, 12, 13, 14`) that are reported nowhere —
  decided correctly only because the comparison carries a tolerance.  This is **not** a defect
  of any published number (those are exact, Corollary G3); it is a defect waiting in the announced
  continuation, with a clean remedy (request R7-ENG-3).

**Minor**

* **m1 — "certified lower bound" is said of bounds that are not.**  ENG-RES-0002 §2, ENG-RES-0007 §3,
  `docs/engineering/DEAD_ENDS.md` ED-3, the docstring of `generic_analysis`: ten lattice bracket ends
  (§3.2 (c)) and five of the six generic ones at each of 11 and 12 torsions are `max(certified, solver)`;
  `results/generic_Sc16.json` does not keep the two apart.  (For the entropy brackets the wording is
  accurate: all ten lower ends equal the certified bound.)
* **m2 — digest item 1** (`docs/collaboration/ENGINEERING_TO_THEORY.md`): "the excess decays about like
  `1/√n`"; see Statement S2.  The response itself (ENG-RES-0008 §3) is worded correctly.
* **m3 — ENG-RES-0008 does not state** the tolerance of "violation" (`10⁻⁷`), the search budgets per
  size (reduced at `n = 64 000` and `128 000`), or that the convergence control covers `u = 1`,
  `n ≤ 16 000` only; its headline number counts the objective evaluations of 2 624 searches.
* **m4 — provenance.**  `results/generic_Sc16_ties.json` has no generating script; the generic cover
  table has no stored covers and only a Modal entry point; stored result files carry no job id or
  commit (except the class tables for `n ≥ 21`); the ledger names a commit only for M-008 … M-011;
  ENG-RES-0007 cites ED-3 for job M-006.
* **m5 — three numbers computed from rounded table entries** (6.1 for 6.15; 0.014 for 0.0134; "rises
  by 0.2–0.3" of which one is 0.15).
* **m6 (for the theory division)** — the remark after Theorem 11.56 that adopts ENG-RES-0008 §5 drops
  the restriction to instances with a common fibre offset (T(e)); request R7-THY-1.

### 1.3 What is missing, and what a hostile referee would attack first (brief, item 6)

Claims with **no control or negative test** on the engineering branch: (a) the class *decomposition*
at 23–24 torsions — produced once, remotely, by one code; the 64-way merge is tested by equality with
a local run at `n = 14` only (now also: independent replications at `n = 21` and `22`, and the
literature totals for all sizes); (b) the upper ends of the entropy brackets and of all generic brackets — the
covers are not stored; (c) in X-005: instances that are not of product form (one scalar offset serves
all fibres), level sets that are not balls (now: the cylinders of §3.7), other design parameters than
the one set used, and the search at the two largest sizes (smallest budget, no convergence control);
(d) in X-006: real inner brackets (stated by the division itself).
**I would attack, in this order:** (1) X-005 beyond product instances — an instance whose fibres sit
at different places of their trivial brackets is in the class, is outside the Harper reduction, and
nobody has evaluated one; (2) the two largest sizes of X-005, which carry "no persistent margin";
(3) the 9 lattice optima that only HiGHS vouches for (`n = 16…19`, `ε ∈ {0, 1, N/20, N/10}`, and `(22, N/4)`);
(4) the class tables at 23–24 torsions.

---

## 2. Precise statements, with proofs or counterexamples

### 2.1 The "generic" chain is exactly decidable up to 14 torsions; the "exact ties" are identities

Model "gen" (theory `docs/workstreams/P_REPORT.md` §0): unit bonds `b_k = x_{k+1} − x_k`, bond angle
`θ = 111°`, torsions `180°, ±60°`.  Put `c := −cos θ = b_k·b_{k+1}` (`= cos 69° = 0.358368…`).

**Proposition G1 [P; checked numerically by integer-relation search at 50 digits].**  For every torsion
word and all beads `p < q`, the squared distance `s_pq = |x_q − x_p|²` is a polynomial in `c` with
**rational** coefficients, of degree at most `q − p − 1`.

*Proof.*  `s_pq = (q − p) + 2 Σ_{p ≤ k < l ≤ q−1} b_k·b_l`.  In the frame attached to bond `k`, `b_l` has
coordinates `T_{k+1}⋯T_l e₁` with `T_j = R_x(φ_j)R_z(π − θ)` (`R_z`: rotation by the angle between
consecutive bonds, entries `c, ±s, 0, 1` with `s = sin θ`; `R_x`: rotation by a torsion, entries
`1, 0, ±cos φ, ±sin φ` with `cos φ ∈ {−1, ½}`, `sin φ ∈ {0, ±√3/2}`, whatever the convention for the
origin of the torsion angle).  So `b_k·b_l` is the `(1,1)` entry of a product of `l − k`
such matrices: a polynomial of total degree `≤ l − k` in `(c, s)` with coefficients in `ℚ(√3)`.
(i) *It is even in `s`.*  With `P = diag(1, −1, −1)`: `P R_z(α) P = R_z(−α)`, `P R_x(φ) P = R_x(φ)`,
`Pe₁ = e₁`; so replacing `s` by `−s` conjugates the product by `P` and leaves the `(1,1)` entry
unchanged.  Writing the entry as `A(c) + s·B(c)` (use `s² = 1 − c²`), evenness gives `B = 0`.
(ii) *Its coefficients are rational.*  With `M = diag(1, 1, −1)`: `M R_x(φ) M = R_x(−φ)`,
`M R_z(α) M = R_z(α)`, `Me₁ = e₁`; so the mirror image (all `φ_j → −φ_j`, i.e. `√3 → −√3` in the
expression) has the same entry.  Writing it as `A(c) + √3·B(c)` with `A, B ∈ ℚ[c]`, invariance gives
`B = 0`.  ∎

Examples found by PSLQ and consistent with the proof (`out_own_ties_detail.txt`): 1–4 pair, trans
`5 + 4c`, gauche `2 + 4c + 3c²`; 1–5 pair `tt`: `8 + 8c`; `g⁺g⁺`: `(7 + 7c + 9c² + 9c³)/2`; `tg`:
`5 + 8c + 3c²`.

**Proposition G2 [P, given K].**  `cos 69° = cos(2π·23/120)` is an algebraic number of degree
`φ(120)/2 = 16` (**[K]**, the degree of `cos(2πk/n)`; confirmed here by `sympy.minimal_polynomial`, which
returns `65536x¹⁶ − 262144x¹⁴ + … − 384x² + 1`).  Therefore, for a chain with `n ≤ 14` torsions
(`N − 2 = n + 1 ≤ 15`), at `θ = 111°` exactly:
(a) two squared distances are equal iff they are equal as polynomials in `c`; a non-constant squared
distance never equals a rational number — in particular never the hard-core bound `3` or the cutoff
`16`;
(b) for two conformations `x, y` the profile distance `D(x,y) = Σ_k |s̃^x_(k) − s̃^y_(k)|` (sorted truncated
squared distances; P_REPORT Proposition 2) is the value at `cos 69°` of one polynomial `Q_xy ∈ ℚ[c]` of
degree `≤ n + 1`, and the same polynomial gives `D(x,y; θ)` for all bond angles in a neighbourhood of
`111°`; `D(x,y)` is rational iff `Q_xy` is constant.

*Proof.*  (a) The difference of two distinct rational polynomials of degree `≤ 15` cannot vanish at an
algebraic number of degree 16.  (b) By (a) the only ties in the weak order of the finitely many values
`{s_pq(x)}, {s_pq(y)}, 16` at `111°` are between identical polynomials, so that order persists on a
neighbourhood; there the two sorted lists are fixed lists of polynomials and every `|·|` has a fixed sign
(or is identically zero).  Rationality of the value forces constancy, again by the degree.  ∎

**Corollary G3 (what this settles) [P + N].**  For `n ≤ 14`, every *equality* that a computation on
this model can meet — equal profiles (class identity), a pair exactly at the hard core or at the
cutoff, a profile distance exactly equal to a rational threshold `(gmin + ε)/L` — is a polynomial
identity in `c`, valid for an open interval of bond angles; it is not an accident of `111°`, and it is
reproduced by floating point to rounding error (`~10⁻¹³`).  Every *strict inequality* has the margin
measured in §3.1 (cover relation: `≥ 2.9·10⁻⁸` for `n ≤ 12`; distinct distance values: `≥ 5.4·10⁻⁶` for
`n ≤ 12`, `≥ 8.6·10⁻⁷` for `n ≤ 14`; hard core: `≥ 0.020` for `n ≤ 13`, `≥ 0.006` at `n = 14`; cutoff:
`≥ 0.011`), five orders of magnitude above rounding error.  **So the floating-point results of the
engineering division for the generic chain (label [X\*] there) are the exact ones: the cover relation
and the covering numbers for `n ≤ 12`, the class tables and the entropy numbers for `n ≤ 14`** — the
margins are **[N]**, the dichotomy "identity or margin" is **[P]**.

**Proposition G4 (the five "exact ties" of ENG-RES-0007 §3) [P for one pair, by explicit polynomials;
N for all five: 60 digits at 111° and 30 digits at seven bond angles].**  At `n = 11` the five pairs
(centre, point) listed in §3.1 have `D ≡ 13` identically in `c`.  For the pair
`tt g⁺g⁺ t g⁻ tt g⁺ t g⁻` / `g⁺ t g⁺ ttt g⁺g⁺ t g⁻g⁻`, eleven of the 66 sorted positions differ; the
positive differences sum to `13/2 + P(c)` and the negative ones to `13/2 − P(c)` with
`P(c) = (21c − 3c² − 9c³)/2`, so `D = 13` for every bond angle at which the order of the 132 values is
the same as at `111°` (numerically: `D = 13.000…` to 30 digits at `110°, 110.5°, 111°, 111.5°, 112°,
113°, 115°`, and `D = 12.81…12.94` at `109°`, where the order has changed).

This answers the remark of ENG-RES-0007 ("that sums of differences of squared distances of this
'generic' chain can be exact integers is itself a small observation; we did not pursue it"): the chain
is generic in its *angle* but its distances live in a 16-dimensional ℚ-vector space, and integer-valued
profile distances are frequent (§3.1: 17, 65, 208, 581, 1 566 pairs of classes at `n = 10 … 14`).

### 2.2 Fractional hitting numbers on the uniform cube (X-003): re-derivation

Setting (theory `docs/workstreams/A_REPORT.md` §2.0, uniform cube): `X = {0,1}ⁿ`, `π` uniform, slack
`u·d_H`; for a proper nonempty `D ⊂ X`, `h_D(y) = u·d_H(y, Dᶜ)`; `D` is *sensitive at level `ε`* iff
`ln E_π e^{h_D} > ε`; `FC_n(ε) = 1/max_q min_{D sensitive} q(D)`.

**Proposition H [P + K (Harper's vertex-isoperimetric theorem); derived by me before reading
ENG-RES-0006; the derivation there is the same].**
(H1) `FC_n(ε) = 2ⁿ / m*`, `m*` the least size of a sensitive set.  *Proof:* `q ↦ min_D q(D)` is concave
and invariant under the automorphism group of the cube (the family of sensitive sets is defined
metrically), which is vertex-transitive; averaging `q` over the group does not decrease the value and
gives the uniform distribution.
(H2) For every `m`, `max_{|D| = m} E e^{h_D}` is attained at the complement of the initial segment
`I_{2ⁿ−m}` of the simplicial order.  *Proof:* with `C = Dᶜ` and `N^j` the `j`-fold closed neighbourhood,
`Σ_y e^{u·d(y,C)} = e^{uJ}2ⁿ − Σ_{j=0}^{J−1}(e^{u(j+1)} − e^{uj})|N^j(C)|` (Abel summation, `J ≥` the largest
distance), decreasing in every `|N^j(C)|`; by Harper `|N(S)| ≥ |N(I_{|S|})|` and `N(I_k)` is an initial
segment, so all `|N^j(C)|` are minimised simultaneously by `C = I_{|C|}`.
(H3) These optimal sets are nested, so `F(m) := max_{|D|=m} E e^{h_D}` is nondecreasing and
`m* = min{m : ln F(m) > ε}` is found by bisection.  Consequently `1 ≤ FC/FC_dip < |B(k)|/|B(k−1)|`, `k` the
radius of the smallest sensitive ball (the Harper set of size `|B(k−1)|` *is* the ball, which is not
sensitive).  ∎

Checked: §3.3 (brute force over all subsets for `n ≤ 4`, including an LP that does *not* assume (H1)).

### 2.3 The reduction of outer landscapes to tail functions (ENG-RES-0008 §5): re-derivation, scope, and one addition

Let `g` be `u`-Lipschitz on the cube `Q_d` (Hamming metric), `W = e^{−g}`, `m(t) = |{W > t}|`, and `∂(k)` the
size of the closed neighbourhood of the initial segment `I_k` of the simplicial order.

**Proposition T [P + K (Harper); re-derived; checked numerically in exact integer arithmetic, §3.4].**
(a) `m` is nonincreasing and right-continuous and `m(te^{−u}) ≥ ∂(m(t))` for all `t > 0`.
(b) Conversely, every nonincreasing right-continuous `m` with values in `{0,…,2^d}`, equal to `2^d` below
a positive threshold and to `0` above another, with `m(te^{−u}) ≥ ∂(m(t))` for all `t`, is the tail
function of a `u`-Lipschitz `g` whose super-level sets `{W > t}` are initial segments.
(c) The tail functions whose level sets are balls are those of monotone radial profiles with
increments in `[0, u]`.
*Proof.*  (a) If `x ∈ N({W > t})` then `W(x) ≥ W(y)e^{−u} > te^{−u}` for a neighbour (or `x` itself)
`y ∈ {W > t}`; so `N({W > t}) ⊆ {W > te^{−u}}`, and `|N(S)| ≥ ∂(|S|)` is Harper's theorem.  (b) Put
`S_t := I_{m(t)}` (nested, since `m` is nonincreasing) and `W(x) := sup{t : x ∈ S_t}`; `W > 0` by the lower
threshold, `{W > t} = S_t` by right-continuity.  For neighbours `x, y` and `t < W(y)`: `y ∈ S_t`, so
`x ∈ N(S_t) = I_{∂(m(t))} ⊆ I_{m(te^{−u})} = S_{te^{−u}}`, i.e. `W(x) > te^{−u}`; let `t ↑ W(y)`.  (c)
`∂(|B(r)|) = |B(r+1)|`.  ∎  **The engineering argument is correct as stated.**

**Addition T(d) (how far "up to partial shells" is) [P].**  For every admissible `m` let
`r(t) := max{r : |B(r)| ≤ m(t)}` (for `m(t) ≥ 1`) and `m_rad(t) := |B(r(t))|` (`0` if `m(t) = 0`).  Then
`m_rad` is the tail function of a monotone radial profile with increments in `[0, u]`, and

    m_rad(t)  ≤  m(t)  <  |B(r(t)+1)|  ≤  (d + 1)·m_rad(t).

*Proof.*  `∂` is nondecreasing (initial segments are nested), so
`m(te^{−u}) ≥ ∂(m(t)) ≥ ∂(|B(r(t))|) = |B(r(t)+1)|`, i.e. `r(te^{−u}) ≥ r(t) + 1` whenever `r(t) < d`: the
radius grows by at least one per factor `e^{−u}`, which is the condition "increments `≤ u`" for the
radial profile `F(ρ) = −ln sup{t : r(t) ≥ ρ}` (and `{W_rad > t} = B(r(t))` by right-continuity).
`|B(r+1)|/|B(r)| ≤ 1 + C(d, r+1)/C(d, r) ≤ d + 1`.  ∎
So every tail probability of every `u`-Lipschitz landscape is within a factor `d + 1` of that of a
monotone radial one: negligible at the exponential scale, but **not** small compared with the
differences the engineering tables resolve — a factor `n_o + 1` is `ln(n_o+1)/(na) ≈ 0.06` in the units
of those tables at `n = 1000`, `u = 1`, against the "`0.002·na`" quoted for general versus monotone
profiles.  The engineering search evaluated no instance with a partial shell; I ran one family
(§3.7): it changes the cost by up to `0.075·na`, in the favourable direction.

**Scope T(e) (what the outer loop reads) [P, from the text of the algorithm].**  Step 1 of Algorithm 2L⁺
(theory `docs/workstreams/K_REPORT.md` §2.2) gives a new outer point `a` the trivial bracket
`[e^{−ψ(a,0)−un_i}, e^{−ψ(a,0)+un_i}]` after one query of `ψ(a, 0)`.  So the outer loop reads an instance
through the joint law of the pair `(W(a), ψ(a,0))` (and through what the inner procedures return), not
through the law of `W(a)` alone.  For product instances `ψ(a,b) = g(a) + F_i(b)` the second coordinate is
a function of the first and the reduction applies — and then it applies to the *distribution* of
literal runs with oracle inner behaviour, not only to mean runs, because the outer sample is i.i.d.
uniform.  For a general `u`-Lipschitz `ψ` the offset `t₀(a) = ψ(a,0) + un_i + ln W(a)` varies with `a`
within `[n_i(u − Λ₁), n_i(2u − Λ₁)]`, and the reduction says nothing.  ENG-RES-0008 §5 states this limit
("fibres that differ from point to point other than by their value at the reference"); the remark by
which the theory division adopted the argument (theory report at `40c5bd7`, after Theorem 11.56: "The
outer loop sees an instance only through the law of the fibre averages … the mean run on any instance
is the mean run on an instance whose outer level sets are initial segments") **drops it**.

### 2.4 What "no violation in 7 095 840 mean runs" is (X-005)

**Statement S1 [read from `src/metricchain_eng/twolevel/meanrun.py` and the stored results].**  A *mean
run* is one deterministic evaluation of Algorithm 2L⁺ on one instance (a discrete law of `W`, a reference
value `ψ₀`, one fibre offset `t₀`) and one inner behaviour ("bottom" or "top"), in which every random
count `#{i ≤ M : W(a_i) > s}` is replaced by its mean `M·P(W > s)`.  The number `7 095 840` is the sum of
the numbers of objective-function evaluations of 2 624 differential-evolution searches
(`5 144 256 + 1 568 160 + 383 424`, files `x005_cost.jsonl`, `x005_claims.jsonl`, `x005_converge.jsonl`;
recounted).  Hence "no violation in `7·10⁶` mean runs" is
* a statement about **expectations**: the inequalities of Theorem 11.56 hold along the trajectory that
  the algorithm follows when all counts sit at their means — which is how the deterministic part of
  the proof (accounting on the good event) is tested, not its probabilistic part;
* a **count of evaluated instances**, strongly dependent (populations of an optimiser converging, in
  468 cells `(u, n, φ)`), from one 19-parameter family of radial product instances — not a number of
  independent trials, and no confidence statement attaches to it;
* **not a statement about a tail.**  The only tail statement of the experiment is that of X-006
  (585 000 literal runs with oracle inner brackets at `n_o ≤ 300`, `n_i = 6`: zero failures, hence a
  failure frequency below `5.1·10⁻⁶` at 95 % *pooled over the 117 cases*, below `6.0·10⁻⁴` for each
  single case, `1.6·10⁻³` with a Bonferroni correction over the cases) — recounted in §3.5.
"Violation" means a slack above `10⁻⁷` in the logarithm (`Run.violations`, `tol = 1e-7`); the message
does not state this tolerance, and its table shows the validity slack `ln L − ln A` at
`+1.6·10⁻¹⁰` (rounding at an instance where `L = A`).

**Statement S2 (the trend) [N; refit of the stored data, §3.5].**  Over `n = 250 … 128 000` the excess of
the worst case found over the claimed exponent decays *faster* than `1/√n` at every size: effective
exponents `0.76, 0.68, 0.63` (`u = ½, 1, 2`; `0.71, 0.61, 0.56` for `n ≥ 4000`), and the column
"difference × √n" of the engineering table falls by factors `4.9, 2.9, 2.2` across the range.  A pure
law `A/√n` misfits by 24–45 % (rms, relative); `A/√n + B/n` fits to 3–4 %, `A/√n + B·ln n/n` equally
well, and a pure power `n^{−2/3}` fits `u = 1` to 8 %.  The data are *compatible with* an asymptote
`∝ 1/√n` reached from above with a `1/n` correction that is still as large as the leading term at
`n ≈ 6000, 1300, 440`; they neither establish nor exclude the exponent ½.  The sentence of ENG-RES-0008
§3 ("consistent with the `O(√n)` correction of the theorem") is accurate; the digest's "the excess
decays about like `1/√n`" (`docs/collaboration/ENGINEERING_TO_THEORY.md`, item 1) is not what the data
show.

---

## 3. Numerics: what was done, at which sizes, with what result, and how to re-run it

All runs: one core (`OMP_NUM_THREADS=1`), one computation at a time (two short overlaps of two of my
own jobs occurred, of about 4 s and about 1 min; see `NOTES.md`), this machine (shared; load average
between 2 and 8 on 4 cores during the work), no single computation above 15 minutes or 2 GB (longest:
the `n = 22` lattice enumeration, 867 s), Python 3.13, NumPy 2.5.3, SciPy 1.18.1 (HiGHS), mpmath 1.3.0, gcc 13.3; OR-Tools 9.15.6755
installed into a private directory outside the shared environment (for CP-SAT only).  No remote
resource was used and no Modal job was re-run (the web was used for two literature searches and one
page fetch, §4 and §3.2 (a)).  From `experiments/science/ws_R7/`:

### 3.1 X-004 — the generic (off-lattice) chain (ENG-RES-0007 §3, ENG-RES-0009 §2): REPLICATED, no difference

Own code, written from P_REPORT §0, §2.1 and theory report Theorem 11.4 before any engineering file
on X-004 was opened: `own_gen.py` (enumeration breadth-first with prefix pruning, **no** symmetry
reduction; profile classes by *global* clustering of the occurring distance values with the gap
spectrum recorded), `own_cover.py` (cover relation `L·D ≤ gmin + ε`; greedy; LP; a tolerance-free
lower bound; MILP by HiGHS with exact re-check of the returned cover), `own_entropy.py` + `l1kern.c`,
`own_stats.py`, `own_hardcore.py`, `own_ties*.py`, `own_integer_distances*.py`, `own_angle_robust.py`.
The engineering implementation (`src/metricchain_eng/chains/generic_chain.py`, `generic_analysis.py`,
`profile_cover.py`, `experiments/eng/chain_cover/generic_entropy.py`) was read afterwards; it differs
in method (depth-first with mirror reduction; class key = distances rounded to 8 decimals; dominance
reductions before the integer programme) and agrees in every number:

| quantity (engineering source) | range | engineering | mine | verdict |
|---|---|---|---|---|
| conformations (ENG-RES-0007, -0009) | `n = 5…14` | 99, 239, 577, 1 393, 3 363, 8 115, 19 559, 47 141, 113 587, 273 623 | identical | REPLICATED |
| profile classes | `n = 5…14` | 30, 60, 136, 291, 639, 1 360, 2 908, 6 137, 13 012, 27 421 | identical | REPLICATED |
| cover table, 12 cells per `n` | `n = 5…9` (60 cells) | all proved optima | identical in all 60 (in 40 my LP certificate alone proves the optimum) | REPLICATED |
| cover table | `n = 10` (12 cells) | 319, 223, 255, `[209,211]`, `[119,123]`, 60 ; 13, 8, 10, 8, 5, 3 | identical, including the two open brackets with the same ends (240 s per cell on one core) | REPLICATED |
| cover table | `n = 11` | 6 exact cells, 6 brackets | 6 exact cells identical; brackets consistent with my bounds | exact cells REPLICATED |
| cover table | `n = 12` | 6 exact cells, 6 brackets | bounds only: consistent; no cover constructed | consistency only |
| "nearest tie" column | `n = 5…12` | 5.2e-4, 2.7e-4, 1.2e-4, 1.8e-5, 4.5e-6, 3.2e-7, (ties), 2.9e-8 | 5.211e-4, 2.711e-4, 1.155e-4, 1.824e-5, 4.473e-6, 3.248e-7, (5 ties; nearest non-tie 1.273e-7), 2.929e-8 | REPLICATED |
| exact ties | `n = 5…12` | 5 at `n = 11` (`L = 1`, `ε = N/2`), none elsewhere | the same 5, none elsewhere | REPLICATED, and explained (§2.1) |
| hard-core margins at `n = 10` | | 0.078 above, 0.020 below | 0.078462, 0.020008 | REPLICATED |
| "classes never closer than 0.035" | `n ≤ 12` | 0.035 | 0.0353 (and 0.0075, 0.0072 at `n = 13, 14`) | REPLICATED |
| pairs within the cutoff per bead (three statistics) | `n = 5…14` | e.g. 2.58 / 2.46 / 4.23 at `n = 10` | identical | REPLICATED |
| distance entropy `σ(ρ)`, six radii | `n = 5…14` (60 numbers) | table of ENG-RES-0009 §2 | identical to the three printed decimals | REPLICATED |

Two things I expected to be weak points and that are not: (i) the column "max" of pairs per bead
equals (number of pairs)/N at every size — it is real (conformations of the type `(t g⁺g⁺)^k` keep all
pairs within the cutoff up to 17 beads); (ii) the class key "round to 8 decimals" could split a class if a
value sat on a rounding boundary — my boundary-free clustering gives the same counts at every size.

*Ties and exactness.*  `own_ties.py 5 12`: the five ties at `n = 11`, re-evaluated at 60 digits from the
torsion words, have `D − 13 = O(10⁻⁶⁰)`.  In my float64 run all five come out slightly **above** 13
(`13.000000000000014 … 37`), in the engineering run one example is `12.999999999999998`: without the
tolerance `10⁻⁹` the two programmes would have decided these comparisons differently; with it both
count them as covered, which is the exact answer (§2.1, G4).  `own_angle_robust.py 5 12`: the set of
accepted torsion words and the partition into profile classes are unchanged when the bond angle is
moved by `−0.02°, −0.007°, +0.003°, +0.011°, +0.03°` — the equalities that define the classes are
identities (G2), not accidents.  Integer-valued profile distances (`own_integer_distances*.py`):

| `n` | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|
| unordered pairs of classes with `D ∈ ℤ` (to `10⁻⁹`) | 1 | 11 | 17 | 65 | 208 | 581 | 1 566 |
| exact ties of the `L = 1` cover relation, `ε = N/4` / `ε = N/2` | — | 0 / 0 | — | — / 5 | — | **4 / 253** | — |
| nearest non-tie over the six `L = 1` cells | 1.6e-3 | 4.5e-6 | 1.5e-5 | 2.4e-6 | 2.5e-6 | 5.0e-7 | **2.1e-8** |

("—": the accuracy is not an integer at that size, so no tie is possible; at `ε = 0` and `ε = 1`, which
are integers at every size, there is no tie for any `n ≤ 14`.)  **At 13 torsions — the next size on
the engineering division's list — 253 comparisons of one cell sit exactly on the threshold, and at 14
torsions the nearest non-tie is within a factor 20 of the tolerance.**  The floating-point treatment
is at its limit there; §7 asks for exact arithmetic in `ℚ[c]`.

The same identities sit in the **entropy table** of ENG-RES-0009 §2, whose comparisons are `D ≤ ρN`
(`own_entropy_ties.py`): unordered pairs of classes with `D = ρN` exactly — `n = 9`: 3 (`ρ = 1.25`,
`D = 15`); `n = 10`: 8 (`ρ = 1`, `D = 13`); `n = 12`: 48 (`ρ = 1`, `D = 15`); `n = 13`: 13 (`ρ = ¼`, `D = 4`)
and 13 (`ρ = 1`, `D = 16`); `n = 14`: 220 (`ρ = 1`, `D = 17`); none at `n ≤ 8` and `n = 11`.  The nearest
non-tie is `≥ 3.4·10⁻⁸` at every size.  Both programmes count the ties as "within" (tolerance `10⁻⁹`),
which is the exact answer, so the published `σ` are exact; but ENG-RES-0009 says only that "the tie
analysis of ENG-RES-0007 §3 applies", and that analysis ("five exact ties at `n = 11`, none
elsewhere") is about the cover relation — the 305 ties of the entropy table are not reported
anywhere.

*Covers at `n = 11, 12`.*  `n = 11` (2 908 classes): the six `L = 1/5` cells, by HiGHS in my formulation
(five of them already by my LP certificate alone): `16, 10, 11, 10, 6, 4` — identical.  For the six
`L = 1` cells I computed bounds only (tolerance-free LP certificate; greedy cover):
`[471, 523] [338, 388] [378, 432] [307, 361] [167, 208] [85, 105]` against the published
`[474, 484] [339, 350] [379, 392] [308, 319] [168, 179] [85, 90]` — consistent in all six, and in five of
them the published lower end exceeds the LP certificate (by 3, 1, 1, 1, 1): it is the HiGHS bound at
the 90 s limit, not "the certified lower bound" (the stored file has a single field `lower`).
`n = 12` (6 137 classes), bounds only: `L = 1`: `[755, 861] [551, 642] [603, 697] [483, 569] [250, 318]
[109, 143]` against `[757, 788] [552, 595] [605, 645] [484, 526] [251, 284] [109, 136]` — consistent; lower
ends above the certificate by 2, 1, 2, 1, 1, 0.  `L = 1/5`: my certificates `20, 13, 15, 11, 6, 4` against
the published exact values `21, 13, 15, 11, 6, 4`: the lower side is certified in five cells; I did not
construct covers of the published sizes (my greedy covers have `26, 18, 20, 15, 7, 5`; the
engineering covers are not stored), so **the `n = 12` row is checked for consistency, not replicated.**
The per-cell "nearest tie" values of both sizes agree with the stored ones to all printed digits.

*A remark on the growth test of ENG-RES-0009 §2* (`check_entropy_growth.py`, from the stored numbers).
The prediction "growth of classes divided by `e^σ`" assumes `σ` independent of `n`; with the form that
does not, `g_n·exp(nσ_n − (n+1)σ_{n+1})`, the predicted ratios at `ε = N/2` are
`1.79, 1.70, 1.15, 1.20, 1.26, 1.31, 1.27` (`n = 5→6 … 11→12`) against the measured
`1.67, 1.40, 1.62, 1.26, 1.40, [1.42, 1.50], [1.21, 1.60]` — scattered on both sides, no systematic
over-prediction; at `ε = N/4` it still over-predicts (by 10–30 %).  This is the finite-size correction
the message itself asks for; it removes most of the "over-prediction by 10–50 %" at `ε = N/2`. **[N]**

Re-run: `python3 own_gen.py 11`; `python3 own_cover_table.py 5 9 300`; `python3 own_cover_table.py 10 10 240`;
`python3 own_cover_table.py 11 11 200 "1.0:0,1.0:1,1.0:N/20,1.0:N/10,1.0:N/4,1.0:N/2,0.2:0,0.2:1,0.2:N/20,0.2:N/10,0.2:N/4,0.2:N/2" 0`
(fifth argument 0 = bounds only for the `L = 1` cells); `python3 own_cover_table.py 12 12 0`;
`python3 own_entropy.py 5 12`; `python3 own_entropy.py 13 14` (77 s for `n = 14`); `python3 own_stats.py 5 14`;
`python3 own_hardcore.py 2 12`; `python3 own_ties.py 5 12`; `python3 own_ties_structure.py`;
`python3 own_ties_detail.py`; `python3 own_integer_distances.py 5 12`; `python3 own_integer_distances_big.py 13 14`;
`python3 own_angle_robust.py 5 12`; `python3 own_entropy_ties.py 5 14` (build the kernel first: `gcc -O3 -march=native -fPIC -shared -o l1kern.so l1kern.c -lm`).
Outputs: `out_own_cover_n5_9.txt`, `out_own_cover_table_*.{txt,json}`, `out_own_entropy_*.json`,
`out_own_ties_*.{txt,json}`, `out_own_integer_distances*.{txt,json}`, `out_own_angle_robust.txt`.

RE-RUN of their code (reduced size): see §3.6.

### 3.2 X-002 — lattice chains: the published covers as certificates (ENG-RES-0002 §§1–2, 4, 6; ENG-RES-0007 §2)

Own code: `own_lattice_cert.py` (exact primal check; tolerance-free dual bound), `own_dia.c` +
`own_dia_compare.py` (own enumerator, written from the model definition before `dia_enum.c` was read),
`own_lattice_opt.py` (HiGHS and CP-SAT in my own formulation on the unreduced instance), `own_flip.c`
(brute-force single-flip constants), `own_lattice_nets.py`, `check_eng_res_0002_prose.py`.

**(a) Class tables** (`experiments/eng/chain_cover/data/dia_Sc12_n*.txt`; per class: pair counts, number of
conformations, fewest and most gauche torsions).  My enumerator gives **identical tables for
`n = 1 … 22`** (with the mirror reduction; without it for `n ≤ 9`): e.g. `n = 20`: 2 139 332 335
conformations, 2 328 classes; **`n = 21`: 6 204 141 457 conformations, 2 753 classes (278 s on one
core); `n = 22`: 17 973 153 955 conformations, 3 319 classes (867 s)** — the first two of the four
tables that were produced on Modal (job M-002) and that nobody outside the engineering division had
replicated (workstream R2 reached 23 beads, `n = 20`).  `n = 23, 24` would take about 40 minutes and
two hours of one core with my enumerator (in prefix chunks); I did not run them.
**An external control the engineering register does not use:** the total number of conformations of
*every* table, `n = 1…24`, equals `c_{n+2}/12`, where `c_k` is the published number of `k`-step
self-avoiding walks on the diamond lattice (OEIS A001394; the enumerators fix the first two bonds,
`4·3 = 12` choices) — e.g. `n = 24`: `1 810 062 340 812 / 12 = 150 838 528 401`
(`check_saw_counts_oeis.py`; b-file read `[full text, through a page-fetching tool]`).  This validates
the totals of the Modal tables for `n = 23, 24` as well; their split into classes remains
unreplicated.

**(b) Primal certificates.**  `results/lattice_Sc12.json` stores for each of the 288 cells
(`n = 1…24` × 12 settings) the cover itself (`centres_hist`).  With my own profile distance
(`5|ΔC₁| + 3|ΔC₂| + |ΔC₃|`, derived from the definition) and an exact integer cover relation:
**all 288 stored covers are covers of the stored class table and have the published size**
(`python3 own_lattice_cert.py primal`: 0 failures); class counts and conformation counts of the result
file equal those of the class tables in all 24 rows.

**(c) Dual bounds — which optima are certified, and by what.**  My lower bound solves the dual of the
covering LP in floating point, truncates the weights to integers and evaluates the largest centre
load in exact integer arithmetic on the *unreduced* matrix; it is valid whatever the LP solver did.

| | cells | what proves the published lower end |
|---|---|---|
| published single number, my certified bound equals it | **241** | stored cover (checked) + exact LP certificate: **an optimum with no reliance on any branch and bound** |
| published single number, LP certificate 1 or 2 below | 22 | a solver's branch and bound: 18 cells at `n = 14…18` (`L = 1`, `ε ∈ {0, 1, N/20, N/10}`) and 4 cells at `n ≥ 19`: `(19, N/10)` 35, `(19, N/4)` 22, `(20, N/4)` 24, `(22, N/4)` 26.  (13 of the 22 are closed by my certified branch and bound: (h) below) |
| published bracket `[a, b]` | 25 | `b`: stored cover (checked, 25/25).  `a`: equals my certified bound in 15 cells; in **10 cells it is one above it** and is the HiGHS branch-and-bound bound after 300 s |

For `n ≥ 19` my certified bound equals the stored `lower_certified` in all 72 cells, and my LP value
equals the stored `lp_bound` in all 288 (to its 6 printed decimals).  The ten brackets whose published
lower end is *not* the certified bound: `(19, ε=0)` `[52, 56]` (certified 51); `(19, ε=1)` and
`(19, N/20)` `[42, 44]` (41); `(20, ε=0)` `[57, 61]` (56); `(20, N/10)` `[37, 40]` (36); `(21, ε=1)` and
`(21, N/20)` `[50, 54]` (49); `(23, ε=0)` `[74, 83]` (73); `(23, ε=1)` and `(23, N/20)` `[60, 67]` (59).
ENG-RES-0002 §2 describes every bracket as "`a` a certified lower bound"; the table generator
(`make_tables.cover_cell`) prints `max(lower_certified, lower_solver)`.  **So "is each bracket what it
says?": the upper ends yes; fifteen lower ends yes; ten lower ends are solver-trusted bounds, one
above what is certified.**  (They are very probably true; they are not what the text says they are.)
As a consequence all 24 published covering numbers of the theory division (P_REPORT §3.3, `n = 5…12`)
are among the 241: reproduced *and* certified independently of any solver's search.

**(d) "Two solvers agree on every cover" / "proved by HiGHS and CP-SAT independently for `n ≤ 18`".**
Three of the 18 cells that rest on branch and bound, 1 core:

| cell (published; LP-certified) | HiGHS, my formulation, unreduced | CP-SAT, my formulation, unreduced, 1 worker, 120 s | their `min_cover_highs` on their reduced instance | their `min_cover_cpsat(workers=1)` on it, 240 s |
|---|---|---|---|---|
| `n = 14`, `L = 1`, `ε = 1` (25; 24) | optimal 25 (13 s) | cover 27, bound 6 | proves 25 (5 s) | cover 27, bound 7, not proved |
| `n = 15`, `L = 1`, `ε = 0` (33; 32) | optimal 33 (6 s) | cover 38, bound 6 | proves 33 (4 s) | cover 39, bound 8, not proved |
| `n = 16`, `L = 1`, `ε = 0` (38; 36) | optimal 38 (45 s) | cover 50, bound 7 | proves 38 (21 s) | cover 43, bound 7, not proved |

The published optima are confirmed by HiGHS in three settings (their stored run; my formulation on
the unreduced matrix; their function re-run here).  That CP-SAT proves them *independently* I could
not confirm: with one worker it neither finds the optimum nor gets a bound above 8 in the time I can
give it; the engineering runs used 8 workers on 4 cores without a time limit (job M-004).  More
important for the record: **the evidence for the sentence cannot be regenerated from the repository.**
The stored rows `n = 1…18` have `solvers = {highs: k, cpsat: k}` and lack the keys `lower_certified`,
`lower_solver`, `exact_certified`, which `lattice_analysis.analyse_table` writes at *every* commit of
the branch (`206fd9e`, `db56d05`, `a2f6dc7`): they were produced by a version of the code that was
never committed.  In the committed `covering_number_P` the loop over solvers ends as soon as one of
them has proved optimality, so CP-SAT is only a fallback; re-running `analyse_table` at `a2f6dc7` for
`n = 14` reproduces all twelve covering numbers and reports `solvers = {greedy, highs}` or `{greedy}` —
**CP-SAT is not called in any cell** (`out_rerun_lattice_solvers.txt`).  And the stored rows record,
per solver, only the size it found, not whether it proved it.

**(e) Single-flip constants** (ENG-RES-0002 §6, `results/lattice_Sc12_flip.json`).  Own brute force
(every self-avoiding conformation, every torsion, both other states; gauche states defined by the
sign of a triple product): `c^{sf}` **identical for `n = 3, 5, 8, 9, 10, 11, 12, 13, 14`**
(`n = 14`: `57 92 109 118 137 154 147 | sym`, 52 s).  Not replicated: `n = 15, 16` and the exhaustive
test that `c^{sf}` is a valid Hamming envelope (their mode B).  The derived table of ENG-RES-0009 §1
(36 pairs `(n, j)`, bounds of Proposition 11.74, no violation; least excess 21 … 73; largest ratio
0.136 … 0.286) follows from the stored constants (recomputed).

**(f) Prose and derived numbers of ENG-RES-0002 / -0007 §2**, recomputed from the class tables and the
result file (`check_eng_res_0002_prose.py`): the finite-size table (2.45 … 4.56; 6.64 … 13.56; 7/8 …
14/24), "four gauche torsions reach `‖N‖₁ = 166`", the sequence of conformations and classes for
`n = 13…24`, `N_cov/N² = 0.100, 0.093, 0.109, 0.110–0.126`, the effective exponent 4.3, "at most 8" at
`L = 1/5`, the `ε = N/2` sequence, the hand-typed table of ENG-RES-0007 §2: all consistent.  (One
rounding: `166/27 = 6.15`, printed as 6.1.)  The two-line proof that every trans/gauche pattern is
realised (restrict even bonds to `{a₀, a₂}` and odd bonds to `{a₁, a₃}`: every bond then has
`y`-component `+1`) is correct **[P, checked by reading]**.

**(g) Entropy brackets** (ENG-RES-0002 §4; internal covering numbers at closed radius `δN`; 50 cells,
`n ∈ {8, 10, 12, 13, 14, 16, 18, 20, 22, 24}` × five radii; `own_lattice_nets.py`).  No inconsistency
in any cell (my certified bound never exceeds a published upper end; my greedy cover is never below a
published lower end).  Of the 40 published single values, my tolerance-free LP bound equals 33 — the
lower side is certified; **the upper side (a cover of that size exists) cannot be checked, because the
net covers are not stored** — and 7 rest on branch and bound (`n = 10`, `δ = ¼`: 43 against 40;
`n = 12`, `δ = ¼`: 65 / 60; `n = 13`: 20 / 19 and 55 / 52; `n = 14`: 25 / 24 and 72 / 66).  In all ten
brackets the published lower end **equals** my certified bound (25, 98, 29, 104, 33, 146, 38, 141,
41, 186): for the entropy table "certified lower bound" is accurate.

**(h) A solver-independent proof for cells that rest on branch and bound.**  `own_certified_bb.py`: a
branch and bound in which every pruned node carries an exact-integer LP-dual certificate (the
floating-point dual vector is only a hint; node bound `|F₁| + ⌈Σw / max load⌉` in integer arithmetic;
branching on an uncovered class, children partition the covers; exact dominance reductions done with
my own code; self-test against brute force on 300 random instances, with "target = optimum" exhausted
and "target = optimum + 1" refuted in every one).  Applied to the 22 cells of (c) with a limit of 240 s
per distinct instance (`own_certified_bb_all.py optima 240`):

| cell(s) | published | LP certificate | certified branch and bound |
|---|---|---|---|
| `n = 14`: `ε = 1`, `N/10` (one instance) | 25 | 24 | **proved `≥ 25`**: 598 nodes, 3.7 s |
| `n = 15`: `ε = 0`, `N/20` | 33 | 32 | **proved `≥ 33`**: 99 nodes, 1.6 s |
| `n = 15`: `ε = 1`, `N/10` | 27 | 26 | **proved `≥ 27`**: 12 nodes, 0.2 s |
| `n = 16`: `ε = 1`, `N/10` | 30 | 29 | **proved `≥ 30`**: 8 nodes, 0.3 s |
| `n = 17`: `ε = 1`, `N/20` | 34 | 33 | **proved `≥ 34`**: 493 nodes, 34 s |
| `n = 17`: `N/10` | 28 | 27 | **proved `≥ 28`**: 225 nodes, 15 s |
| `n = 19`: `N/4` | 22 | 21 | **proved `≥ 22`**: 8 nodes, 1.2 s |
| `n = 20`: `N/4` | 24 | 23 | **proved `≥ 24`**: 207 nodes, 38 s |
| `n = 16`: `ε = 0`, `N/20` | 38 | 36 | not finished in 240 s (11 226 nodes) |
| `n = 17`: `ε = 0` | 43 | 41 | not finished (4 800 nodes) |
| `n = 18`: `ε = 0` | 48 | 46 | not finished (2 874 nodes) |
| `n = 18`: `ε = 1`, `N/20` | 39 | 37 | not finished (3 001 nodes) |
| `n = 18`: `N/10` | 31 | 29 | not finished (2 702 nodes) |
| `n = 19`: `N/10` | 35 | 34 | not finished (2 278 nodes) |
| `n = 22`: `N/4` | 26 | 25 | not finished (520 nodes) |

Together with the stored covers this makes **254 of the 263 published single covering numbers optima
that are certified without any solver's search** (241 by the LP certificate alone, 13 by this branch
and bound).  The 9 cells that did not finish (LP gap 2, or the largest instances) are vouched for by
HiGHS only; a better branching rule or more time would very probably close them — I did not try.

Re-run: `gcc -O3 -march=native -o own_dia own_dia.c && python3 own_dia_compare.py 1 22` (about 25 min in all);
`python3 own_lattice_cert.py primal`; `python3 own_lattice_cert.py dual 1 18` and `… dual 19 24` (13 min);
`PYTHONPATH=<ortools> python3 own_lattice_opt.py 120 "14:L=1,eps=1" "15:L=1,eps=0" "16:L=1,eps=0"`;
`PYTHONPATH=<ortools> python3 rerun_eng_two_solvers.py <work tree> 240 "14:L=1,eps=1" …`;
`gcc -O3 -march=native -o own_flip own_flip.c && ./own_flip -n 14`; `python3 check_eng_res_0002_prose.py`;
`python3 own_lattice_nets.py 0 8 10 12 13 14 16 18 20 22 24`; `python3 test_own_certified_bb.py`;
`python3 own_certified_bb_all.py optima 240 14 16` and `… 17 24` (35 min); `python3 check_saw_counts_oeis.py`.
Outputs: `out_own_dia_compare_*.txt`, `out_own_lattice_primal.json`, `out_own_lattice_dual_*.{txt,json}`,
`out_own_lattice_opt_batch1.txt`, `out_rerun_eng_two_solvers.{txt,json}`, `out_rerun_lattice_solvers.txt`,
`out_own_flip_*.txt`, `out_own_lattice_nets.{txt,json}`, `out_own_certified_bb_*.{txt,json}`.

### 3.3 X-003 — exact fractional hitting numbers on the uniform cube (ENG-RES-0006 §1): RE-DERIVED and REPLICATED, no difference

`own_harper.py` (written from A_REPORT §2.0 before ENG-RES-0006 and
`experiments/eng/fc_uniform_cube/harper_fc.py` were read).

* `python3 own_harper.py brute` — all `2^{2ⁿ} − 2` proper nonempty subsets for `n = 2, 3, 4` and 30
  parameter pairs (`u ∈ {¼, ½, 1, 2, 3}` × `ε ∈ {0.05, 0.1, 0.3, 0.5, 1, 2}`; 90 cases; the engineering
  check has 72 cases with other parameters).  In all 90: (i) the least size of a sensitive set equals
  the prediction from simplicial-order sets; (ii) the linear programme `max_q min_D q(D)` over **all**
  inclusion-minimal sensitive sets, solved without assuming the uniform sampler, equals `m*/2ⁿ`
  (largest deviation `5.6·10⁻¹⁶`) — a check of (H1) that the engineering script does not make;
  (iii) for **every** size `m` the true maximum of `Σ_y e^{u·d(y,Dᶜ)}` over `|D| = m` equals the value at
  the complement of the initial segment (relative deviation `≤ 6.7·10⁻¹⁶`) — (H2) in full, not only at
  the threshold size.  Smallest margin of a sensitivity comparison: `6.0·10⁻⁴` (no tolerance issue).
* `python3 own_harper.py table 14` — explicit simplicial-order sets, distances by breadth-first search,
  bisection over `m`; no closed-form shortcut.  **All 52 rows of
  `experiments/eng/fc_uniform_cube/harper_fc_table.json`** (four parameter sets × `n = 2…14`: smallest
  sensitive `|D|`, smallest sensitive ball, its radius) **are identical to mine**; e.g. `u = 1`,
  `ε = 0.3`: `1, 2, 4, 6, 11, 19, 36, 64, 120, 222, 408, 763, 1432`.
* RE-RUN of their script: `harper_fc.py --check` prints "72 cases, all agree"; `--nmax 14` regenerates
  the stored JSON **byte for byte** (`rerun_logs/harper_check.log`).

Outputs: `out_own_harper_brute.{txt,json}`, `out_own_harper_table.{txt,json}`.

### 3.4 The tail-function reduction (ENG-RES-0008 §5): numerical checks of Proposition T

`python3 own_tail.py` → `out_own_tail.txt` (exact integer arithmetic throughout).

| check | sizes | result |
|---|---|---|
| T0: Harper's theorem itself — `min_{|S|=k}|N(S)| = |N(I_k)|` for every `k`, by brute force over all subsets | `Q_2, Q_3, Q_4` | true |
| T0′: the closed neighbourhood of an initial segment is an initial segment | `Q_m`, `m ≤ 12`, every `k` | true |
| T1: claim (a) on random `u`-Lipschitz landscapes of three kinds (largest Lipschitz minorant of random data; sparse deep dips; multiples of `u`), on grids of 1, 7 and 1000 units per unit slope | `m = 3, 4, 6, 8, 10`; 150–3000 landscapes per block | `min_t [m(te^{−u}) − ∂(m(t))] = 0` in every block: never violated, and tight |
| T2: claim (b) — random admissible tail functions, the constructed landscape must be `u`-Lipschitz and have the prescribed tail function | `m = 3…10`; 27 900 constructions | 0 failures |
| T3: exhaustive converse — the set of level-size sequences `(|{h ≤ 0}|, |{h ≤ 1}|, …)` of **all** integer-valued 1-Lipschitz `h` with `min h = 0` against the set of **all** sequences with `k_{j+1} ≥ ∂(k_j)` | `Q_2`: 19 functions; `Q_3`: 495; `Q_4`: 197 547 | 5 = 5, 17 = 17, 86 = 86 sequences, the two sets equal |

### 3.5 X-005 / X-006 — the statistics and the claims (not the algorithm)

Read: ENG-RES-0008 in full, `src/metricchain_eng/twolevel/meanrun.py` (definition of the mean run and
of "violation"), `adversary.py`, `experiments/eng/twolevel/run_search.py`, `recheck.py`.  Recomputed
from the stored result files with my own code (`x005_refit.py`, `x006_recount.py`):

* **Table "trend" of ENG-RES-0008 §3** (39 rows): worst case found, best `φ` against it, claimed
  exponent, difference, difference × `√n` — rebuilt from `x005_cost.jsonl`; identical in every printed
  digit.  **Refit** (relative least squares; `out_x005_refit.json`):

  | law fitted to the excess | `u = ½` | `u = 1` | `u = 2` |
  |---|---|---|---|
  | `C·n^{−p}`, all 13 sizes: `p` (± s.e. of the log–log regression) | 0.758 ± 0.011 | 0.676 ± 0.012 | 0.626 ± 0.010 |
  | the same, `n ≥ 4000` (best `φ` fixed at 0.50) | 0.707 ± 0.017 | 0.612 ± 0.022 | 0.560 ± 0.008 |
  | local exponent between the last two sizes | 0.63 | 0.56 | 0.54 |
  | `A/√n`: rms relative misfit, all sizes / `n ≥ 4000` | 45 % / 23 % | 33 % / 13 % | 24 % / 7 % |
  | `A/√n + B/n` | 3.0 % / 0.6 % | 4.0 % / 3.0 % | 3.7 % / 1.3 % |
  | `A/√n + B·ln n/n` | 4.6 % / 1.9 % | 4.0 % / 3.7 % | 3.8 % / 1.3 % |
  | `A·n^{−2/3}` | 18 % / 6 % | 7.7 % / 8 % | 10 % / 12 % |
  | `A·n^{−3/4}` | 7.4 % / 6 % | 14 % / 16 % | 22 % / 22 % |

  (These are deterministic numbers, not noisy samples: the "errors" are search sub-optimality and the
  grids of `φ` and of the ladder, so the misfits are descriptive, and a formal goodness-of-fit test
  would be meaningless.)  Reading: Statement S2 of §2.4.
* **The search budget is not uniform in `n`, and the message does not say so** (the code and the
  stored records do).  4000 (monotone) / 2000 (general) evaluations per search for `n ≤ 32 000`,
  2500 / 1250 at `n = 64 000`, 1500 / 750 at `n = 128 000` (`run_search.tasks`: "reduced at the two largest
  sizes so that a task stays near a quarter of an hour").  The gain of the search over the best of its 63 structured
  starting points falls from `0.11·na` (`n = 250`) to `0.003·na` (`n = 128 000`), and its median over the
  searches of a size is exactly `0` for every `n ≥ 1400`.  The convergence control (five times the
  budget at `n = 1000`, three times at `n = 16 000`, two more seeds) covers four cells, all at `u = 1`.  So at the two largest
  sizes — the ones that carry "no persistent margin" and "still falling at `n = 128 000`" — the number
  called "worst instance found" is in effect "the worst of 63 hand-made instances", obtained with the
  smallest budget and without a convergence control.  That the hand-made instances are near-optimal
  there is plausible (the theory predicts that the instance matters less as `n` grows) but it is not
  shown by this experiment.
* **X-006** (`x006_sampled.jsonl`, 585 records): the table of ENG-RES-0008 §6 recounted — 117 cases ×
  5000 runs = 585 000 literal runs at the theorem's `K`, no failure of any kind; with `K` divided by
  4, 16, 64, 256 the good event fails in 82 / 14 668 / 29 408 / 31 698 of 39 000 runs (`u = ½`), etc.;
  every number of the table agrees.  "Below `5.1·10⁻⁶` at 95 %, pooled": `1 − 0.05^{1/585000} = 5.12·10⁻⁶`,
  correct, and correctly qualified as pooled; for a single case the bound is `6.0·10⁻⁴`.  At the
  theorem's `K` the literal runs' mean `ln(evaluations)` differs from the mean-run value by
  `−0.0006 … +0.0019`, and the extreme runs of a case by `−0.0035 … +0.018`: at these sizes the cost is
  essentially deterministic, which is what licenses the mean run as a proxy *there* (`n_o ≤ 300`,
  `n_i = 6`, oracle inner brackets) and nowhere else.
* **"The flat instance is not the worst one"** is a constructive claim: one instance with a larger
  mean-run cost at the same `φ` suffices, and the stored file contains one for every one of the 468
  cells (by more than `0.001·na` in 419 of them; largest excess `1.10·na`; recounted).
  I checked that the instances are members of the class (radial outer profile with slopes in `[0, u]`
  resp. `[−u, u]`; inner offset within `[−n_iΛ₁, n_i(u − Λ₁)]`, the exact range of
  `ln E e^{−F_i} + F_i(ref)` over `u`-Lipschitz `F_i`; product form) and that the stored maximisers
  reproduce the stored costs when re-evaluated by the engineering code (§3.6).  Whether the mean-run
  cost is the cost of the algorithm of the theorem is the question of workstream R6, not examined
  here.

Re-run: `python3 x005_refit.py`; `python3 x006_recount.py`.

### 3.6 The record: can the quoted numbers be traced to stored outputs and regenerated at reduced size?

Three experiments were taken through the whole chain (document → stored output → stated command at
reduced size): X-003, X-004 (with X-007) and X-005.  All re-runs use the engineering code at `a2f6dc7`
in a work tree outside the repository (`bash rerun_engineering.sh <dir> export`, then one step per call;
logs in `rerun_logs/`).

| step | what was re-run | result |
|---|---|---|
| tables | `experiments/eng/chain_cover/make_tables.py --verify` on ENG-RES-0002, -0007, -0009; `experiments/eng/twolevel/make_tables.py --verify` on ENG-RES-0008 | all four: "tables … match the artifacts" |
| X-003 | `harper_fc.py --check`; `harper_fc.py --nmax 14` | 72 cases agree; stored JSON regenerated byte for byte |
| X-004 | `generic_analysis.analyse_generic(n)`, `n = 5…9` (the function behind the Modal entry point) | counts, margins, all 60 cells (lower, upper, exact), reduced sizes: identical to the stored rows; "nearest tie" to `4.5·10⁻¹⁴` |
| X-007 | `generic_entropy.py --nmin 5 --nmax 11` | rows 5…11 identical to the stored rows (all fields but timings) |
| X-005 | `run_search.py --u 1 --n 1000 --phi 0.5 0.8` (the local command stated in ENG-RES-0008) | flat 1.0405 / worst 1.0466 and flat 0.7013 / worst 1.3382; **all eight search optima equal the stored ones to the last bit**, with the same numbers of evaluations (54 s) |
| X-005 | `recheck.py --nmax 2000` | 1 008 search optima and 504 flat values of the cost job reproduce the stored values exactly (plain comparisons), within `1.5·10⁻⁵` with the tie rule; claims and convergence jobs: exactly; no violation under either convention |
| tests | `python -m pytest tests/eng -q` (C sources compiled here) | 128 passed |
| X-002 | `lattice_analysis.analyse_table` at `n = 14`, solvers `("highs","cpsat")` | the 12 covering numbers regenerate; the `solvers` field does not (§3.2 (d)) |

Numbers quoted in prose (outside the generated table blocks), recomputed from the stored files
(`check_record_numbers.py`, `check_eng_res_0002_prose.py`): the job statistics of the ledger (M-008:
468 tasks, 5 144 256 instances, 34.8 core-hours, longest task 2 241 s; M-009: 180, 1 568 160, 20.7 h,
2 147 s; M-010: 8, 383 424, 1.1 h, 971 s), the extremes of the claims table, `e^{71}` and `e^{513}`,
"11–49 %", the absolute margins below 0.01, the generic-chain timings (389, 565, 701 s; 25, 73, 334 s),
"at most 0.05 … 0.03", "0.013 per torsion", "3.1 … 0.12 per bead", and everything listed in §3.2 (f):
**all traced; no number quoted in ENG-RES-0002, -0006, -0007, -0008 or -0009 was found to disagree
with a stored output.**  (Three statements are computed from rounded table entries and differ in the
last digit from the stored values: `166/27 = 6.15` printed as 6.1; an increment 0.0134 printed as
0.014; rises of "0.2–0.3" of which one is 0.15.)

What could **not** be traced or regenerated:

1. `experiments/eng/chain_cover/results/generic_Sc16_ties.json` — the evidence for "five exact ties at
   `n = 11`, none elsewhere; nearest non-tie `≥ 2.9·10⁻⁸`" (ENG-RES-0007 §3; register X-004) — **has no
   generating script on the branch**: its keys (`exact_ties`, `nearest_non_tie`, `min_class_distance`)
   occur in no source file.  (Its content is right: replicated in §3.1.)  The example
   "12.999999999999998" is in no stored file.
2. The stored rows `n = 1…18` of `results/lattice_Sc12.json` (216 of 288 cells, and the only evidence for
   the two-solver sentence) come from code that is in no commit (§3.2 (d)).
3. The generic cover table has **no stored covers** (only sizes), so its upper ends cannot be checked as
   certificates, only regenerated; its only driver is a Modal entry point
   (`modal_jobs/chain_cover_app.py::generic`) — there is no local script, although the function runs
   locally in seconds for `n ≤ 9`.
4. In the stored generic rows the certified and the solver lower bounds are merged into one field
   `lower`; at `n = 11` the published lower end exceeds my tolerance-free LP bound in five of the six
   brackets (474/471, 339/338, 379/378, 308/307, 168/167; equal in the sixth, 85), so there too
   "`[certified lower bound, verified cover]`" (ENG-RES-0007 §3) is, in most cells,
   `[solver bound, verified cover]`.
5. ENG-RES-0007 refers the stopped job M-006 to "`DEAD_ENDS.md` ED-3"; ED-3 describes the lattice job
   M-004.

**Compute ledger** (`docs/engineering/COMPUTE_LEDGER.md`): remote jobs (M-001 … M-011: command,
resources, bound before launch, measured cost, status) and local runs are in separate tables, and the
register names the environment of every experiment, so *at the level of jobs* remote and local work
are distinguishable.  *At the level of artifacts* they mostly are not: only the class tables for
`n ≥ 21` carry their provenance (header line and `.meta.json`); `lattice_Sc12.json`, `generic_Sc16.json`
and the `x005_*.jsonl`/`x006_*.jsonl` records carry no job id, host or commit, and the ledger gives a
commit only for M-008 … M-011.  For X-005 the gap is closed by `recheck.py` (every stored maximiser
re-evaluated with the final code); for the lattice rows `n ≤ 18` it is not.

### 3.7 A control the engineering search did not run: level sets that are not balls (X-005)

`rerun_eng_partial_shell.py` re-uses the engineering evaluator and search (decoder, seeds, differential
evolution, both oracles, budget 2000) on **cylinders** `g(a) = F(|a_{k+1…n_o}|)`, `k = 1, 2, 4, 8, 16, 32`:
`u`-Lipschitz landscapes of the outer cube whose level sets are not balls (for `k = 1` they are initial
segments with a partial shell), whose law of `W` is the radial law of the `(n_o − k)`-cube.

| cell | radial worst (stored / re-run, `k = 0`) | cylinders, worst over `k` | least over `k` |
|---|---|---|---|
| `u = 1`, `n = 250`, `φ = 0.60` | 2.0811 / 2.0811 | 2.0553 | 2.0553 |
| `u = 1`, `n = 1000`, `φ = 0.55` | 1.0402 / 1.0401 | 0.9959 | 0.9904 |
| `u = 1`, `n = 1000`, `φ = 0.80` | 1.3382 / 1.3382 | 1.2882 | 1.2632 |
| `u = ½`, `n = 1000`, `φ = 0.55` | 1.8285 / 1.8285 | 1.8285 | 1.8285 |
| `u = 2`, `n = 1000`, `φ = 0.50` | 0.7726 / 0.7723 | **0.7728** | 0.7723 |
| `u = 1`, `n = 4000`, `φ = 0.50` | 0.6941 / 0.6941 | 0.6939 | 0.6926 |

(entries: `ln(cost)/(na)`; my `k = 0` re-run uses the monotone family and budget 2000 only, whence the
last-digit differences from the stored values, which come from both families at budget 4000 / 2000.)
In 158 508 mean runs (135 864 of them on cylinders) **no claim of the theorem is violated** (largest
`ln cost − ln C_max = −10.75`), and non-ball level sets of this type exceed the radial worst case in one
cell only, by `0.0002·na`.  So the reading of ENG-RES-0008 §5 survives a control it did not have.  Two
qualifications: the cost is *not* insensitive to the shell structure at the `0.002·na` level quoted
there (cylinders cost up to `0.075·na` less than the radial worst case); and cylinders are one
admissible family among many — partial shells placed just above the closing radius were not tried.
**[N; RE-RUN of their evaluator on new inputs — it inherits whatever error that evaluator may have.]**

---

## 4. Prior art, with a search log

This workstream is a review, not a novelty claim; the only literature it leans on is cited here with
the level at which I read it (COMMON rule 5).

* **Harper's vertex-isoperimetric theorem** (initial segments of the simplicial order minimise the
  closed neighbourhood on the cube; neighbourhoods of initial segments are initial segments): L. H.
  Harper, "Optimal numberings and isoperimetric problems on graphs", *J. Combinatorial Theory* 1 (1966)
  385–393.  `[search snippet]` for the bibliographic data (web search, 2026-11-25, query "Harper 1966
  Optimal numberings and isoperimetric problems on graphs vertex isoperimetric theorem hypercube
  simplicial order initial segments": the result list confirms title, journal, volume, pages; no
  snippet states the theorem in the form used).  The statement itself is used here as `[from memory —
  unverified against the paper]`; it is **verified by my own brute force for the cubes `Q_2, Q_3, Q_4`**
  (all subsets) and the nestedness for `m ≤ 12` (§3.4), i.e. exactly in the range where the engineering
  division's exhaustive checks live, and it is a cited theorem beyond.
* **Degree of `cos(2πk/n)`**: D. H. Lehmer, "A note on trigonometric algebraic numbers", *Amer. Math.
  Monthly* 40 (1933) 165–166: for `gcd(k, n) = 1`, `n > 2`, `2cos(2πk/n)` has degree `φ(n)/2`.
  `[search snippet]` (same date, query "degree of minimal polynomial of cos(2π/n) is φ(n)/2 Lehmer 1933 A
  note on trigonometric algebraic numbers": the Wikipedia article "Niven's theorem" and a lecture note
  state the result and the reference; the search also reports that Lehmer's *sine* statement needed a
  correction, which does not concern the cosine).  For the one instance used (`n = 120`, `k = 23`) the
  degree 16 is **computed here** (`sympy.minimal_polynomial`).
* Proposition G1 (squared distances of a chain with fixed bond angle and rotameric torsions are
  rational polynomials in the cosine of the bond angle) is elementary transfer-matrix algebra of the
  rotational-isomeric-state kind; I did **not** search for a prior statement and make no claim that
  it is new.  The same holds for T(d).
* Weak LP duality for set cover, the "rule of three" for zero failures, and Abel summation are
  standard and are not cited.

No other search was made; in particular I did not search for prior art on any engineering claim
(those are computational results on the programme's own models).

---

## 5. What I did not settle

1. **Nine lattice optima are still vouched for by HiGHS alone** (`n = 16`: `ε = 0, N/20`; `n = 17`: `ε = 0`;
   `n = 18`: `ε = 0, 1, N/20, N/10`; `n = 19`: `N/10`; `n = 22`: `N/4`): my certified branch and bound did not
   finish on them in 240 s.  One of them (`n = 16`, `ε = 0`) I re-solved with HiGHS in my own
   formulation and with their function (38 in both).
2. **Whether CP-SAT proves any lattice optimum on its own.**  With one worker it does not get near
   (§3.2 (d)); the configuration behind the stored record (8 workers, 4 cores, no time limit,
   uncommitted code) is out of my reach under the one-core rule.
3. **The ten bracket lower ends that are solver bounds** (lattice, `n = 19…23`) and the corresponding
   generic ones (`n = 11, 12`): neither certified nor refuted.  None of the open brackets was closed.
4. **Class tables beyond my enumeration** (`n = 23, 24`): the totals agree with the published
   self-avoiding-walk counts, the split into classes is unreplicated; everything stated about covers
   at those sizes is relative to the stored tables.
5. **Single-flip constants `n = 15, 16`** and the exhaustive validity of `c^{sf}` as a Hamming envelope
   (ENG-RES-0002 §6; mode B of `dia_flip.c`): not replicated; `dia_flip.c` was not read.
6. **Generic covers at `n = 12`**: consistency of bounds only (§3.1); the upper ends of all generic
   brackets and the covers behind the exact values cannot be checked, because they are not stored.
7. **The 253 exact ties at `n = 13`** (and the 4 at `ε = N/4`) were identified by the gap between `10⁻⁹`
   and the nearest non-tie (`5·10⁻⁷`), not re-evaluated one by one at high precision; by G2 they are
   identities if they are ties at all.
8. **X-005: the correctness of the evaluator** (is the mean run the algorithm of Theorem 11.56; is its
   cost formula the number of evaluations) — workstream R6; my re-runs and my control of §3.7 inherit
   it.  **X-006** was recounted from its stored file, not re-run.  Fibre offsets that vary with the
   outer point (non-product instances), partial shells other than cylinders, other design parameters,
   and a convergence control at `n ≥ 64 000`: examined by nobody.
9. **X-001** (replication of the theory audit), ENG-RES-0006 §2 (the pricing reformulation, stated
   there as unimplemented analysis), ENG-MSG-0003 §5 (the tie pitfall of literal runs), the
   farthest-point traversal numbers `m(δ)`, and the upper sides of the entropy table: not examined.

---

## 6. The three most promising next steps

1. **Make the off-lattice chain exact.**  Represent every squared distance as an element of `ℚ[c]`
   (degree `≤ n + 1`; Proposition G1 gives the recursion: products of `3×3` matrices over `ℚ[c, s, √3]`
   reduced by `s² = 1 − c²`), decide all comparisons by the sign of a polynomial at `cos 69°` (interval
   arithmetic on a rational enclosure, or Sturm sequences; ties are the zero polynomial), and store the
   class table with exact keys.  This removes both tolerances, turns `[X*]` into `[X]`, lists every pair
   with constant profile distance, and is *needed* at 13 torsions (253 exact ties in one cell) and at
   14 (nearest non-tie `2·10⁻⁸`).  Cost: small — the float code already decides everything correctly
   up to 12 torsions.
2. **Certify the optima that rest on branch and bound.**  A branch and bound whose every pruned node
   carries an exact-integer LP-dual certificate (prototype: `own_certified_bb.py`, §3.2 (h): it closes
   13 of the 22 cells in seconds) makes an optimum independent of any solver's tolerances and leaves a
   tree that a third party can check in linear time.  Finish the nine remaining cells (a stronger
   branching rule or cover cuts will be needed at LP gap 2), then the ten solver-trusted bracket ends
   and the seven entropy values of §3.2 (g).
3. **Attack X-005 where its family ends**: (a) product structure — instances whose fibre offset
   `t₀(a)` is anti-correlated with `W(a)` (low fibres at the bottom of their trivial bracket, high ones
   at the top), which the reduction of ENG-RES-0008 §5 does not cover and which need the pair law
   `(W, ψ(·,0))` as input to the evaluator; (b) a convergence control at `n = 64 000, 128 000` and at
   `u ≠ 1`; (c) partial shells tuned to the closing radius.  Any of these could move the "worst
   instance" columns; none can be read off the present data.

---

## 7. Requests

### To the engineering division (each can be sent as it stands)

**R7-ENG-1 (record; small).**  *Motivation:* the sentences "two solvers agree on every cover"
(register X-002, validation (vi)) and "optimum proved … by HiGHS and CP-SAT independently for `n ≤ 18`"
(ENG-RES-0002 §2) rest on rows `n = 1…18` of `experiments/eng/chain_cover/results/lattice_Sc12.json`
that no committed code produces: `covering_number_P` stops at the first solver that proves
optimality, and re-running `analyse_table` at `a2f6dc7` for `n = 14` never calls CP-SAT.  *Request:*
either (a) add an option `independent=True` that runs every solver to its own conclusion and stores,
per solver, `size`, `proved`, `bound`, wall time and the number of workers, regenerate the rows
`n = 1…18` with the committed code and state the commit in the ledger; or (b) withdraw the two
sentences and say "HiGHS; cross-checked by a solver-independent certificate in 198 of the 216 cells"
(209 with the certified branch and bound of §3.2 (h)).
*Validation:* `git show <commit>:…/lattice_Sc12.json` has the same keys in every row; a third party
running the stated command obtains the stored `solvers` field.  *Resources:* minutes on 4 cores.

**R7-ENG-2 (wording; trivial).**  In ENG-RES-0002 §2, ENG-RES-0007 §3 and `DEAD_ENDS.md` ED-3 a
bracket is described as `[certified lower bound, verified cover]`.  In 10 of the 25 lattice brackets
and in 5 of the 6 generic brackets at each of 11 and 12 torsions the lower end is the MILP solver's
bound at the time limit, one to three above the certified one.  (For the entropy brackets of
ENG-RES-0002 §4 the description is accurate.)  *Request:* print both
(`[certified | solver, cover]`), store both in `generic_Sc16.json` (it has a single `lower`), and store
the covers of the generic chain as the lattice file does (`centres` as torsion words or class keys),
so that the upper ends are checkable certificates.

**R7-ENG-3 (exactness of the off-lattice chain; the substantive one).**  *Motivation:* §2.1/§3.1 of
this report: distances are in `ℚ[c]`, `c = cos 69°` of degree 16; the five "exact ties" are polynomial
identities; at 13 torsions the cell `(L = 1, ε = N/2)` has 253 of them and the cell `(L = 1, ε = N/4)`
four; at 14 torsions the nearest non-tie is `2.1·10⁻⁸`.  *Formulation:* implement the chain in exact
arithmetic over `ℚ[c]` as in §6 item 1.  *Inputs:* none.  *Expected outputs:* class tables for
`n = 5…14` with exact keys (must equal the stored counts: … 13 012, 27 421); for every `n` the list of
class pairs with constant profile distance (must contain 1, 11, 17, 65, 208, 581, 1 566 integer-valued
ones for `n = 8…14`) and the exact cover matrices; the label `[X]`.  *Validation:* agreement with the
float code wherever the float margin exceeds `10⁻⁶`; the five pairs of §3.1 give exactly 13.
*Stopping condition:* `n = 14` (beyond it the degree reaches 16 and reduction modulo the minimal
polynomial is needed).  *Resource estimate:* single core, minutes to an hour; no remote compute.
Also: add the script that produced `results/generic_Sc16_ties.json` (none is on the branch) and a
local driver for the generic cover table (the only one is a Modal entry point).

**R7-ENG-4 (X-005, disclosure and two controls).**  State in ENG-RES-0008 (i) the tolerance of
"violation" (`10⁻⁷` in the logarithm), (ii) the search budgets per size (4000/2000 up to `n = 32 000`,
2500/1250 at 64 000, 1500/750 at 128 000), (iii) that 7 095 840 counts objective evaluations of 2 624
searches in 468 cells.  Replace "the excess decays about like `1/√n`" in the digest by what the fit
shows (effective exponent 0.63–0.76; compatible with `A/√n + B/n`; exponent ½ not established).  Run
the convergence control (5× budget, two more seeds) at `n ∈ {64 000, 128 000}`, `φ ∈ {0.50, 0.55}`,
`u ∈ {½, 1, 2}` — 12 cells; *expected output:* change of the worst case `≤ 0.001·na` or a new
maximiser; *resource estimate:* with budgets 12 000 / 6 000 and two seeds, from the stored task times
(about 900 s and 1 160 s per cell at the present budgets): roughly 45 core-hours; *stopping condition:*
one pass.  And evaluate at least one family with non-ball level sets
(the cylinders of §3.7 cost nothing to add) so that "up to partial shells" is a tested statement.

**R7-ENG-5 (certify what the solver only asserts).**  For the lattice cells whose optimum rests on a
MILP solver's search (§3.2 (c), (h)) and for the ten bracket ends that are solver bounds, run a branch
and bound whose pruned nodes carry exact-integer dual certificates (prototype `own_certified_bb.py`:
13 cells closed in 0.2–38 s each on one core) and store the tree — fixed-in / fixed-out sets and the
integer weight vector of every leaf — so that a third party can check optimality in linear time.
*Stopping condition:* the cells of this report that did not finish in 240 s (LP gap 2 at
`n = 16…18`; `(19, N/10)`); a strong-branching rule or cover cuts will be needed there.

### To the theory division

**R7-THY-1.**  The remark after Theorem 11.56 at `40c5bd7` ("for the outer loop, radial landscapes are
almost the whole class") says that the outer loop sees an instance only through the law of the fibre
averages.  By step 1 of Algorithm 2L⁺ it also sees `ψ(a, 0)` for every outer point, so the statement
holds for instances in which `ψ(a,0) + ln W(a)` does not depend on `a` (product instances) — the
qualification ENG-RES-0008 §5 makes and the remark drops.  Suggested wording: "With a fixed inner
behaviour *and a fibre offset `t₀` common to all outer points (e.g. product instances)* the law of
everything the outer loop sees — hence of the bracket and of the cost, not only the mean run — is a
function of the tail function …".  Proposition T(d) of §2.3 here quantifies "almost": every tail
probability is within a factor `n_o + 1` of a monotone radial one.

**R7-THY-2.**  Where the theory report quotes "in `7 095 840` mean runs no claim of Theorem 11.56 was
violated" (at `40c5bd7`: §11.19, Remarks (1) after the table "The picture for the cube class"), add that these are objective evaluations of an
optimiser at the expectation level (§2.4, S1) and that "the excess … decreases with `n`, consistently
with the `O(√n)` correction" is an upper-bound statement: the measured decay is faster (S2).
