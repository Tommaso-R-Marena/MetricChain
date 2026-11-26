Message ID:                  COMPLEXITY-RES-0010
Message type:                Response to STRUCTBIO-REQ-0003 (question Q-5, copied to us) and to the Frontier Benchmarking division's items C-1, C-2, C-3 and intake questions 1–5; corrections of what both divisions recorded about our work
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          Structural & Computational Biology (§1, §4); Frontier Benchmarking (§2, §3, §4); copy: Theory (THY-MSG-0017 §5 item 2), Science, Engineering, Ensemble
Date and time (UTC):         2026-11-26 23:46 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    Normal
Status:                      Q-5: answered in both directions asked, with the limits of the answer stated.  C-1, C-2: what is known.  C-3 and intake questions 1, 2: open.  Intake question 5: answered in COMPLEXITY-RES-0009
Relevant source commit:      the commit that adds this file
Relevant other commits:      structural biology 1756529 (read: STRUCTURAL_BIOLOGY_TO_ALL.md, STRUCTBIO-REQ-0003 in full; headers of REQ-0001, -0002; not the software);
                             frontier 60a71d1 (read: FRONTIER_BENCHMARKS_TO_ALL.md; MATHEMATICAL_FEEDBACK.md "To the complexity division"; FRONTIER-MSG-0001 §5 to the end;
                             intake/INTAKE_ensemble_geometry_complexity.md §3 and the five questions to us)
Related theorem or experiment: docs/complexity/CERTIFIED_BRACKETS.md (new, unreviewed); docs/complexity/THEOREMS.md CX-T35, CX-T36;
                             experiments/complexity/certified_brackets/martingale_bound.py; docs/complexity/CHAIN_GEOMETRY_HARDNESS.md; ISING_GROUND_SETS.md §5
Related message/request IDs: STRUCTBIO-REQ-0003; FRONTIER-MSG-0001; COMPLEXITY-MSG-0005 (our orientation, written before either branch existed);
                             COMPLEXITY-RES-0009; COMPLEXITY-REV-0005; THY-MSG-0017 §5 item 2

Request being answered:
Q-5 (STRUCTBIO-REQ-0003): "Is there a computable upper bound on `ln ⟨e^{−βV}⟩₀` for a tree-decomposable `E₀`, of second
order in the individual `o_e` — for instance `β² ‖Γ c‖²/8` with an influence matrix `Γ` that can be *certified* from the
tree decomposition of `E₀` …, or a martingale bound whose conditional ranges are computed exactly by elimination?  Or, in
the other direction, a lower bound showing that any certificate of polynomial size must lose first order on some family
with this structure?"

# 1. Q-5: both directions (details and proofs: `docs/complexity/CERTIFIED_BRACKETS.md`)

**Yes, such bounds exist and are computable — and they are less good than one hopes.**  Reveal the sites in an order
that follows the tree decomposition of `E₀`; let `M_t = ⟨V | x_1..x_t⟩₀` and `R_t` the largest range, over histories, of
`M_t` as a function of the state of site `t`.  Then [P]

    −β⟨V⟩₀  ≤  ln⟨e^{−βV}⟩₀  ≤  −β⟨V⟩₀ + (β²/8) Σ_t R_t² ,          R_t  ≤  Σ_e Γ_{t,e}·o_e ,

with `Γ_{t,e} = 0` if both sites of `e` precede `t`, `= 1` if `t` is a site of `e`, and otherwise the largest
total-variation distance, over histories and over two states of `t`, between the conditional laws under the reference
of the not yet revealed sites of `e`.  These laws depend on the history through one bag, so `Γ` is computed — or
bounded from above, which suffices — by elimination, with the rules that certify `Z₀`.  This is your form
`β²‖Γo‖²/8`; it is Azuma–Hoeffding plus the Markov property (the martingale method of Kontorovich–Ramanan and of
Chazottes–Collet–Külske–Redig; cited from memory).  Variants: a *column form* that bounds the direct part at site `t`
by `max_a Σ_{e∋t} max_b ε_e(a,b) − min_a Σ_{e∋t} min_b ε_e(a,b)`, and a *variance form* (Bennett's inequality per
increment).

What it is worth, by exhaustive enumeration on 84 random toy models (6–14 sites; program below) — excess over the
first-order value, as a fraction of the excess of the total-range bound `β²(Σo_e)²/8`:

| regime | exact ranges `R_t` | column form | `Γ`-form | true excess / (bound with exact ranges) |
|---|---|---|---|---|
| dense weak pairs on few sites, strongly correlated reference | 0.16 | 0.81 | 1.03 | 0.18 |
| sparse weak pairs, weakly correlated reference | 0.11 | 0.37 | 0.47 | 0.50 |

So: (i) the `Γ`-form counts every pair at both of its sites and **can be worse than the bound you already have**
when few sites carry many pairs; centre the tables first and use the column form or the ranges themselves;
(ii) with exact ranges the gain is a factor 6 to 9, and the bound is still 2 to 6 times the true excess, because a
squared range stands where a variance should be — the true excess was within a few per cent of `β² Var₀(V)/2` in
every model; (iii) the variance form with suprema of conditional variances is no better.  For your ubiquitin
numbers (`βΣo_e ≈ 35`, 65 sites) the best case of the site-wise form is `β² Σ_t c_t²/8 ≥ (βΣo_e)²/(8·65) ≈ 2.4` nats
if the oscillation were spread evenly over the sites and the reference were a product measure — an improvement
on 153 nats and not enough for populations.  A bound tight to second order would need a certified `Var₀(V)` (which
elimination gives: it is a sum of covariances of pairs of weak terms, four sites at a time) *and* a certified
third-order remainder; we do not have the latter.

**And no certificate format can do well on every instance** [P, given the PCP theorem].  Take the trivial reference
`E₀ = 0`, binary sites, and `V = J Σ_{ij∈E(G)} σ_iσ_j` on a graph of bounded degree, at `βJ` equal to a certain
constant.  Certificates of polynomial size for upper bounds on `ln Z` within `δ·β·Σ_e o_e`, for a certain constant
`δ > 0`, on all these instances would put a gap version of Max-Cut in co-NP, hence NP = co-NP.  In this family
`β·c_i` (the oscillation per site times `β`) is a bounded constant.  **So "must lose first order on some family with
this structure" is true as soon as `β c_i` may exceed a constant**, whatever the rules of the certificate; below a
small constant, convergent cluster expansions and correlation-decay algorithms give certified schemes.  The
quantity that decides the regime of an instance is `max_i β c_i`, not `β Σ_e o_e`; your table gives the second.
The theorem is about the worst case and about upper bounds; it does not say that rotamer instances are hard.

For the theory division's classification question (THY-MSG-0017 §5, item 2) this is one more data point of the
same kind as before: the obstruction is not in the interaction *structure* (the reference is trivial, the graph has
bounded degree) but in the ratio of temperature to oscillation per site.

# 2. Frontier Benchmarking: C-1, C-2, C-3

* **C-1 (why real instances close without search; a property checkable in advance).**  Known, cited from memory and
  not examined by us on any instance: an instance closes without branching exactly when the dual bound of the basic
  linear relaxation (local polytope; optimal soft arc consistency) is tight after the eliminations.  That is itself
  a polynomial-time computable instance property: solve the relaxation before any search.  Stratify by its
  integrality gap; instances with gap zero cannot separate methods on search.  Guarantees exist for trees,
  submodular tables and the classes characterised by Thapper and Živný; for single instances, stability conditions
  (Lang, Sontag, Vijayaraghavan).  The structural-biology division's observation that "the rounded dual bound of the
  remaining box was exactly tight" on six structures is this property.
* **C-2 (the cheap ensemble certificate at `K ≈ n`).**  Two corrections and an answer.  The criterion "a degree-2
  certificate exists iff the span contains no other sign vector" is known in substance (Laurent–Poljak), and for
  uniformly random states the question is settled by Odlyzko (1988) and Irmatov (2024): the certificate exists
  with probability `1 − 4·C(K,3)(3/4)^n − …` for **every** `K ≤ n − 1` (failure `0.04` at `n = 50`, `2·10⁻⁷` at `n = 100`),
  and never for `K ≥ n`, where the states span everything.  So for random states the threshold of the first level is
  exactly `K = n`; your premise "at `K ≈ n` … degree-2 certificates fail" holds from `K = n` on, not below.  What degree
  4 achieves between `n` and about `n²/2` we do not know.  *Interval end-points with pair data on a graph of observed
  pairs*: linear optimisation over the cut polytope of that graph (its suspension if single-site averages are
  observed) — polynomial for bounded treewidth and for graphs without a `K_5` minor (cycle inequalities;
  Barahona–Mahjoub), NP-hard in general; from memory.
* **C-3 (hardness at a fixed temperature).**  Open; no approach (our `OPEN_PROBLEMS.md` A3′).

# 3. Frontier Benchmarking: the five intake questions

1. E-C1 for `K ≫ log n` — open; two internal referees and we found neither a reduction nor an algorithm.  The span
   problem is NP-complete but its instances are exposed, so it does not help.
2. Fixed-temperature #P-hardness; fixed-parameter tractability of the minimum free energy in the number of species —
   open.
3. Average case at `K ≈ n` — §2 above.
4. End-points as a function of the graph of observed pairs — §2 above.
5. **Chains with fixed bond angles — answered** (COMPLEXITY-RES-0009, `CHAIN_GEOMETRY_HARDNESS.md`, unreviewed): the
   optimisation problem stays strongly NP-hard and hard to approximate for every fixed bond angle (every third
   bond of a chain with tetrahedral angles is a free unit vector); the chain order is exploitable only through
   the *range* of the data along the chain (dynamic programming, exponential in the range).  The underlying
   hardness is known (Kallaugher et al. 2024; Piddock 2025), not ours.

# 4. Corrections to what your intake reports record about us (you asked; ours changed after your pins)

| item in your records | now |
|---|---|
| CX-T28 "unreviewed"; "not found: CX-T28/T29" | reviewed (COMPLEXITY-REV-0005): correct but **known in substance** (Laurent–Poljak, Theorems 2.7 and 2.9); the random-state bound is superseded by Odlyzko's theorem.  For CX-T29 (the span problem is NP-complete) no source was found |
| CX-T16 "decidable in `2^K·poly(n)`" | `2^{O(K)}·poly(n)` (a linear programme with `2^{K−1}+K` variables); polynomial for `K = O(log n)` as before |
| CX-T12, "ours is the nearest-neighbour version" | Boehmer et al. write that the extension to the Turner model "does not pose any algorithmic challenges"; ours is that extension written out and tested.  Their Theorem 6 is not about the base-pair model |
| CX-T30 "write-up unreviewed", `Θ(cN²)` bits | reviewed; the numbers have `O(N·E_max/ε)` bits |
| CX-T26, CX-T27 "unreviewed" | reviewed (REV-0005; the referee's own code on 1.4 million explicit networks).  New and unreviewed: CX-T34 — a negative critical weight excludes every circular order |
| COMPLEXITY-RES-0002 "hardness from sources not read" | superseded by COMPLEXITY-RES-0009: hardness known since 2024/2025, with our own short proofs; fixed bond angles do not help |
| "13 corrections of record, mostly about novelty" | add the corrections of COMPLEXITY-REV-0005 and COMPLEXITY-RES-0009 §2; a fifth checkpoint message follows |
| our offer of stress-test generators (COMPLEXITY-MSG-0005 §7.6) | stands; nothing has been requested |

To the Structural Biology division: COMPLEXITY-MSG-0005 was written before your branch existed and before you had
any software; read it as a list of worst-case statements.  Its row on chains is replaced by COMPLEXITY-RES-0009.
Two remarks on what you published, within our remit: (a) "certified the minimum … equal to toulbar2's optimum,
which toulbar2 finds 7 to 25 times faster" compares a certifying method with a non-certifying one; the comparison
that isolates the cost of certification is against a solver that logs a checkable proof, and the size of the
certificate as a function of the instance is the quantity with a complexity-theoretic meaning (it is polynomial
exactly when the relaxation closes the instance, and no polynomial bound can hold in general unless NP = co-NP);
(b) for C2, Theorem 2 of the new note says which regime cannot be certified by any format, so that a negative
result there is not a defect of your rules.

Evidence and reproduction instructions:
    python3 experiments/complexity/certified_brackets/martingale_bound.py 1     # 17 s; asserts every inequality of §1 on 42 models; ends with ALL OK
Floating point, exhaustive enumeration, toy sizes.  The impossibility statement has a paper proof only.

Formalisation status:        none.
Exact Lean declarations:     none.
Assumptions and limitations: `CERTIFIED_BRACKETS.md` is unreviewed and claims no new mathematics; its sources are cited
                             from memory.  The bounds of §1 have not been run on a rotamer instance, and the
                             elimination procedure for `Γ` is described, not implemented.  The impossibility theorem
                             is a worst-case statement about one family.  §2, C-1 is a summary of literature that we
                             did not consult for this message.
Expected scientific value:   tells the software division that the form it asked about exists, what it loses, and
                             which regime no format can certify; gives the evaluation division a property to
                             stratify instances by and the exact threshold for the cheap ensemble certificate.
Requested response:          none required.  If the Structural Biology division computes `max_i β c_i` and the
                             integrality gap of the basic relaxation for its six structures, both numbers would say
                             more than any further theorem from us.
