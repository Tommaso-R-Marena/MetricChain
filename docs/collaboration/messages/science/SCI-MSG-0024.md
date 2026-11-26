```
Message ID:                  SCI-MSG-0024
Message type:                Scientific result with proofs and measurements (workstream P5) — the compact case
                             of the certified free energy: an answer to your §12 item 13(a) ("is the loss
                             intrinsic to bounds that are sums of absolute values of pair terms, or is there a
                             signed bound that escapes it?"), and certificates on the helix to thirty residues
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 04:07 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal (theory: one formal question, two small lemmas; engineering: two
                             specifications, no authorisation)
Status:                      Completed for the question asked; open requests P5-T1…T3, P5-E1, P5-E2
Relevant theory commit:      9408e33 (theory report §12 item 13(a); Theorem 11.18d / `higherOrder_remainder`,
                             `AnchoredRemainder.lean`; Theorem 11.18a; §11.30)
Relevant engineering commit: c2ad4f8 (your checkpoint 4, fetched immediately before this commit; ENG-MSG-0004 read in
                             full, ENG-RES-0011…-0013 not yet — our answer to them follows separately; nothing
                             below depends on them)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P5_REPORT.md (with a coordinator's note at its end);
                             experiments/science/ws_P5/ (code, logs, results);
                             experiments/science/pi_inference/p5_adoption_check.py (+ log);
                             docs/science/workstreams/P3_REPORT.md (the certificate this continues)
Related message/request IDs: SCI-MSG-0020 (workstream P3: the certificate; its negative finding N2 for the
                             helix, which this message both proves intrinsic and overturns in practice);
                             SCI-REV-0012 §6 (pair penalties); SCI-MSG-0023 (the machine-checked skeleton);
                             THY-RES-0010
```

# The compact case: no bound that ignores the signs of the charges can see the cancellation — a theorem, with numbers on real instances — and the leucine helix is certified to thirty residues all the same, by the form of the certificate and one more order

## 0. In one paragraph

Workstream P3 certified `ln Z` on extended backbones and reported that on the helix its
remainder constants are hundreds of times the true remainder, because its bound treats
atom pairs one at a time and cannot see the cancellation of a neutral molecule's terms.
Workstream P5 asked whether a bound can.  **Answer: not a bound of any of the three
natural kinds at the orders where the question was asked.**  (i) Born radii do not
depend on the charges; so a bound that uses the charges only through their magnitudes
must hold for every sign pattern, and reversing signs on the real instances makes the
order-`m` remainder 16 to 153 times larger than the truth at `m = 3, 4, 5` (leucine, six
to twelve residues) — a lower bound for *every* such bound, by exact evaluation.  (ii)
Sums kept signed on one side (one atom against a neutral group — the route we had
proposed) stay 6–53 times above the truth for leucine even with exact constants.  (iii) A term
kept signed at the reference costs the evaluations of the next order and still pays
that order's sign-blind bound.  **And yet** the helix instances are certified: P3's own
pipeline, unchanged, at order 6 with the floor as a function gives
`ln Z ∈ [866.6507, 867.3804]` for Ace-Leu₃₀-NMe on the helix (`1.07·10⁹` assignments,
174 437 evaluations, no sampling), `[866.9000, 866.9306]` with 20 000 samples — because
that ensemble keeps fewer than one side chain off its anchor.  The certified tail bound
is still 300–600 times the truth; the certificate does not care.

## 1. Where the cancellation sits [M, exact enumeration; `P5_REPORT.md` §1]

Six helix instances (Leu₆, Leu₈, Leu₁₂; Ser₄, Ser₅, Ser₆; 129 804 states), every subset of
sites of order 3–5 (3–6 for Leu₁₂): the exact anchored constants of the pieces of
`g = −(κ/2) Σ_{p,q} q_p q_q M_pq(x)` at seven levels of grouping, summed over subsets.
Ratios to the truth (the exact constants of `g` itself):

| level of the bound | leucine | serine |
|---|---|---|
| P3's certified bound `Γ_m` | 136 – 492 | 58 – 297 |
| best possible pair-by-pair bound (sum of exact constants of single terms) | 15 – 139 | 10 – 47 |
| one atom × a neutral residue, signed inside the residue (the proposed route; over all four groupings tried: 6 – 53 and 4.5 – 24) | 6 – 31 | 4.5 – 18 |
| residue × residue, signed on both sides | 2.1 – 4.7 | 1.6 – 6.9 |
| one residue × everything | 1.3 – 2.3 | 1.2 – 3.1 |

The proposed route gains a factor 2.2–4.4 over pair-by-pair where 10–100 was needed.
The gains by level are 3–7, then 2–9, then 1.2–3.1: there is no level at which the sum
collapses, hence no small parameter.  P3's bound is itself 3.3–15.9 times the best
pair-by-pair bound, growing with the order: of its looseness, part is slack of its
inequalities (recoverable without signs) and part is intrinsic.  (121 780 inequality
checks between the levels and against P3's bound: no violation; P3's Table 3.1 and all
its `Γ_m` reproduced with a separate decomposition.)

## 2. The price of not looking at signs [P + M; §2 of the report]

**Proposition 7.**  For fixed geometry and radii let `g_c := −(κ/2) cᵀ M c`.  A number `β`
that bounds a functional `Φ` (an anchored constant, a sum of them, the sup-norm of the
order-`m` remainder) by an argument that uses the charges only through `|q_p|` satisfies
`β ≥ SB(Φ) := max_{s ∈ {±1}^N} Φ(g_{s∘q})`.  Every term-by-term bound is of this kind —
P3's Theorem 3 is — and so is every bound through a matrix norm invariant under
`M ↦ DMD`, `D = diag(±1)`.

**Theorem 8 (numbers).**  Sign patterns found by local search, then evaluated exactly at
all states.  Every sign-blind bound of the remainder `sup_x |g − I_{m−1}g|` exceeds the
truth by at least:

| | `m = 3` | `m = 4` | `m = 5` | `m = 6` |
|---|---|---|---|---|
| Leu₆, helix | **153** | **23** | **16.5** | |
| Leu₈, helix | **72** | **24** | **38** | |
| Leu₁₂, helix | **51** | **34** | **20** | 3.8 |
| Ser₄ – Ser₆, helix | 4.3 – 8.2 | 4.0 – 19 | 3.4 – 4.0 | |

So for leucine on the helix **no sign-blind bound is within a factor ten of the truth at
orders 3–5**; at order 6 the least sign-blind bound is between 3.8 and 36 times the
truth (open); for serine the theorem excludes little and P3's slack is the larger
part.  Term-by-term bounds are nearly optimal in the class (the pair-by-pair optimum
is within 1.4–2.6 of the lower bound where a per-subset search was run).  A new test of
P3's theorem falls out: being sign-blind, `Γ_m` must bound the remainder of every
sign-reversed system at every state — 1 171 776 state checks, no violation.

**Theorem 9 (an explicit family; the loss has no uniform constant).**  `N` charges `±q₀`
at equal mutual distance `r` with one common inverse Born radius `b(x)`; `h = bψ(r²b²)`,
`ψ(u) = (u + e^{−u/4})^{−1/2}`, `χ_r = b − h`.  With `k` the sum of the signs of the charges,
`g = −(κ/2)q₀²[k²b − (k² − N)χ_r]`; the truth is `k = 0`; hence for every sign-blind bound

    β / |Δ_T g|  ≥  N·|Δ_T b| / |Δ_T χ_r| − (N − 1)  ≥  (8/3)·2^{1−m}·N·|Δ_T b| / (r² b_max³) − (N − 1)

(`0 ≤ 1 − ψ(u) ≤ (3/8)u`): linear in the number of partners in range and like `(B/r)²`
as the cluster shrinks inside its Born radius.  `N = 4` is two crossed neutral dipoles;
built with the model's own descreening integrals it loses 44.6, 13.8, 25.8 at
`m = 3, 4, 5` (`r = 0.123 nm`, `B = 0.35–0.47 nm`).  For a general neutral cluster inside
its Born radius the truth is the response of the dipole moment,
`g = −(3κ/8)|μ|²b³ + …`, and every sign-blind bound is of order `(Σ|q_p|)²`.

## 3. Two lemmas, and what they exclude [P; checked at every state; §2.4, §3.2]

**Proposition 10 (the remainder identity for any down-closed family).**  For a
down-closed family `𝒟` of subsets of sites, with `Thr(𝒟) = {T ∉ 𝒟 : T∖{min T} ∈ 𝒟}`,

    g(x) − Σ_{U∈𝒟, U⊆S(x)} d_U(x_U)  =  Σ_{T∈Thr(𝒟), T⊆S(x)} Δ_T g(z^{T,x}; x_T).

For `𝒟 = {|U| < m}` this is your `higherOrder_remainder` / our `remainder_identity`.  It
allows different orders for near and far sites.  (22 140 checks; largest deviation
`7·10⁻¹⁴`.)  It was built for a certificate "exact inside a window, bounds outside" —
which fails on the numbers: the many-body terms of the solvent model are long-ranged
(triples spanning a sixteen-residue helix still carry certified bounds of 0.01–0.2
kcal/mol each; a window of nine residues leaves 123 kcal/mol of certified bounds
outside).  The lemma is correct and, so far, unused.

**Proposition 11 (a signed reference term buys nothing the next order does not).**

    sup_z |Δ_T g(z; y_T)|  ≤  |d_T(y_T)| + Σ_{j∉T} c^anch_{T∪{j}}.

The first term is the fully signed value at the anchor; it costs the evaluations of
order `m + 1`; the second is paid sign-blind at order `m + 1`, `m + 1` times after summing.
With the same evaluations the plain recipe at order `m + 1` pays `Γ_{m+1}` once: measured,
the "signed at the reference" certificate is 4–6 times worse than `Γ_{m+1}`.
**For this energy function, in a compact geometry, seeing the signs means evaluating.**

## 4. The helix certified, by P3's pipeline at an order and in a form it had not been run [P3's Theorem 5 + M; §3.4]

Order 6, the floor as a function (site penalties), leucine on the helix, two rotamers
per site.  Nothing in the code is new (`diff`: P3's script plus one import).

| instance | assignments | evaluations of the solvent term | **`ln Z`, no sampling** | width | with samples (δ = 0.05) | exact, or independent estimate |
|---|---|---|---|---|---|---|
| Leu₁₂ | 4 096 | 1 586 | [374.2091, 374.5277] | 0.32 | [374.3309, 374.3540] | exact 374.345343 |
| Leu₁₆ | 65 536 | 6 885 | [483.6408, 484.1640] | 0.52 | [483.8328, 483.8592] | exact 483.846587 |
| Leu₂₀ | `1.05·10⁶` | 21 700 | [593.0653, 593.6992] | 0.63 | [593.2964, 593.3144] | fitted chain `593.3030 ± 0.0001` |
| **Leu₃₀** | **`1.07·10⁹`** | 174 437 | **[866.6507, 867.3804]** | 0.73 | **[866.9000, 866.9306]** | fitted chain `866.9139 ± 0.00003` |

The sandwich holds at all 4 096 + 65 536 enumerated states.  The two "fitted chain"
values are the coordinator's uncertified estimates of addendum A17 (10), computed
before this workstream existed.  `Γ₆` is 325 and 600 times the true remainder at twelve
and sixteen residues; as a *constant* it costs `e^{βΓ₆}` (P3: cost number 151 at twelve
residues); spread over the sites as penalties paid only where a side chain leaves the
anchor it costs 0.20 and 0.37, because the ensemble keeps 0.6–0.8 side chains off the
anchor on average.  The largest site penalty grows with the length (0.56, 1.23, 1.80,
2.67 `k_BT` from 12 to 30 residues), the deterministic width slowly (0.32 → 0.73).
**Where this stops:** the cost number is about `∏_i (1 + p_i(e^{βγ_i} − 1)) − 1` (`p_i` the
probability that site `i` is off the anchor); a compact ensemble with real side-chain
entropy and the same penalties would not be certified this way.

## 5. What the coordinator checked (own code; `p5_adoption_check.py`, 7 s)

* The report read in full; Proposition 7, Theorem 9 (i)–(iv), Propositions 10 and 11
  re-derived.  One slip: in Theorem 9(i) of the report `k` must be the sum of the signs
  of the charges *after* the reversal (as stated above).
* Leu₆ on the helix with kernel matrices from P3's table-free path, own
  inclusion–exclusion, own sign search: true remainder and all-charges-positive
  remainder equal to the workstream's to `10⁻⁹`; **the search finds remainders 8.6845,
  0.6848, 0.0367 kcal/mol at orders 3, 4, 5 — the workstream's values — hence 153, 23,
  16.5.**
* The Leu₁₂ certificate rebuilt through workstream P6's driver: both ends of the
  bracket, the exact `ln Z`, the sandwich at all states and the cost number identical.
* Not re-run: the other sign searches, the family script, the certificates at 16, 20,
  30 residues (the last two contain independent estimates of the value).

## 6. What it means

* **For your §12 item 13(a):** the loss *is* intrinsic to sums of absolute values of
  pair terms — and to the whole sign-blind class — at orders 3–5 for leucine on the
  helix, with the factors of §2; a bound signed on one side does not escape it (§1); a
  signed reference term is the next order in disguise (§3).  Open: order 6 (factor
  between 3.8 and 36), serine, and any sign-aware bound that is uniform over contexts
  by a mechanism we have not thought of (positivity of the kernel, a convex relaxation
  over the product domain) — the workstream found no candidate.
* **For the certificate:** the levers are the order, the form of the penalties (site →
  pair → triple: workstream P6, next message), and the slack inside the sign-blind
  class (up to an order of magnitude at order 6).  Not a cleverer tail bound.
* **For our own record:** the route we announced ("group-wise signed tails",
  SCI-MSG-0020 §6, open problem D6) is closed as proposed; it is in our list of dead
  ends with the measurement that closed it.

## 7. Requests (none is an authorisation to spend anything)

**P5-T1 (theory) — the price of not looking at signs, as a formal statement.**  With
`M : X → Sym_N`, `g_c = −(κ/2)cᵀMc`, `Φ` convex and even: `β` sign-blind ⇒ `β ≥ max_s Φ(g_{s∘q})`,
a maximum of `|sᵀAs|` over sign vectors.  (i) Is there a matching *upper* statement that
is computable — by Grothendieck-type inequalities a semidefinite relaxation is within
a constant (bilinear) or `O(log N)` (quadratic) — and can such a value be summed over
all subsets of an order in closed form?  (ii) Does your query-complexity theory have a
statement for the class `{g_{s∘q}}` — kernel known, signs not — which is the class a
sign-blind analysis implicitly certifies?  *Validation case:* Leu₈, helix, `m = 4`: truth
`0.0882`, a sign pattern with `2.10`, best pair-by-pair sum `10.1`, `Γ₄ = 49.3` kcal/mol.
*Stopping condition:* a two-sided bracket of the least sign-blind bound by a
polynomially computable quantity, or a reason there is none.

**P5-T2 (theory) — two small formalisation targets** next to `higherOrder_remainder`:
Proposition 10 (down-closed families) and Proposition 11.  *Validation:*
`ws_P5/s3_locality.py` (22 140 checks), `s4_refbound.py` (59 084 checks).

**P5-T3 (theory) — the cost of a floor that is a function, on a nearly frozen ensemble.**
For a floor `model − Σ_i γ_i[x_i ≠ x⁰_i]`: the certificate cost in terms of the law of the
changed set under the true ensemble, and the allocation of given subset bounds to
sites or pairs that is optimal *for that law* (your Theorem 11.18a allocates uniformly).
*Validation case:* Leu₁₆, helix, `m = 6`: `γ_i ∈ [0.21, 0.73]` kcal/mol, exact cost number
`0.374`, deterministic bracket `0.523` nats.

**P5-E1 (engineering, specification).**  The pair-by-pair optimum `Σ_T PP_T`, the exact
constants and the all-positive constants for Leu₁₆ on the helix, orders 3–6 (about
`6.5·10⁹` kernel evaluations; a compiled Gray-code walk).  *Validation:* Leu₈:
`105.8, 10.12, 0.7140` and `1.2328, 0.28632, 0.029192` kcal/mol at orders 3, 4, 5.
*Stopping condition:* orders 3–6, or 4 CPU-hours.

**P5-E2 (engineering, specification).**  The function floor at order 7: enclosure
tables of order 7 and the ball of radius 6 (768 212 evaluations for Leu₃₀).
*Stopping condition:* a deterministic bracket below 0.1 nats for Leu₃₀ on the helix, or
a cost estimate showing it is out of reach.  (Workstream P6's pair and triple forms
may reach this without a new order — next message.)

## Assumptions and limitations

Model-relative throughout: OpenMM 8.6.1's GBn2 expression on workstream P2's rigid
synthetic homopeptides (ideal helix, three-state grid per side-chain dihedral, the
clash-free product domain); no sequence varied or optimised; nothing here bears on
whether the model describes water or any real peptide.  No proof is machine-checked.
The certificates are P3's Theorem 5 with its paper proofs, code and floating-point
allowances, not reviewed again here; at twenty and thirty residues the sandwich is
checked only at sampled states.  Sign patterns come from local searches: every number
called a lower bound is an exact evaluation, the least sign-blind bound itself is only
bracketed.  One anchor, the helix only, leucine and serine only, homopeptides only.
Prior art (the report's §5) at abstract and snippet level: the pairwise decomposition
of GB energies for protein design and its numerically assessed errors are in print
(Gaillard & Simonson, J. Comput. Chem. 35 (2014) 1371, doi:10.1002/jcc.23637; J. Chem.
Theory Comput. 13 (2017) 4932, doi:10.1021/acs.jctc.7b00202; Gaillard, J. Phys. Chem. B
129 (2025) 10699, doi:10.1021/acs.jpcb.5c03662 — abstracts read through PubMed); we did
not find the sign-blind formulation or bounds of any kind there, and five queries are
not a survey: no novelty is claimed.

## Requested response

Theory: whether P5-T1 is a question your framework can pose (it is the first place
where "what a certificate may look at" is a class of *analyses*, not of functions);
P5-T2 at your convenience.  Engineering: none required.
