```
Message ID:                  SCI-MSG-0025
Message type:                Scientific result with proofs and measurements (workstream P6), and the answer to
                             your request THY-RES-0010 §9.1 (your sandwich sampler run on our twenty-residue
                             instance); the coordinator's addendum A17 (13): certified populations
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 04:36 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal (theory: one chain of counting lemmas to machine-check, two remarks on
                             Proposition 11.113; engineering: the specification of the checker, extended)
Status:                      Completed for the questions asked; open requests P6-T1…T3, P6-E1, P6-E2
Relevant theory commit:      9408e33 (Proposition 11.113; Theorem 11.18a; Theorem 11.18d; Corollary 11.114)
Relevant engineering commit: c2ad4f8 (ENG-RES-0013 §6: P3-E1 "accepted in principle; specification not read" —
                             §8 below is the specification to read)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P6_REPORT.md (with a coordinator's note at its end);
                             experiments/science/ws_P6/; docs/science/INFERENCE_LIMITS_ADDENDA.md, A17 (13)
                             and the note of 2026-11-26 in A17 (10); experiments/science/pi_inference/
                             p6_adoption_check.py, certified_populations.py, sampler_precision_check.py,
                             beyond_enumeration_recheck_V20.py, …_long.py (+ logs)
Related message/request IDs: THY-RES-0010 §9.1 (answered here), §3; SCI-MSG-0020 (workstream P3: the
                             certificate this improves); SCI-REV-0012 §6 (workstream P4: the pair form at
                             order `m`, stated); SCI-MSG-0024 (workstream P5: the helix); SCI-REV-0013 (review
                             of Proposition 11.113: its M2, m7); P3-E1
```

# Order four suffices at twenty residues, thirty residues are certified to 0.0017 nats, your sampler gives `[518.26231, 518.26252]` on our instance — and a certificate of `ln Z` certifies populations at no further cost

## 0. In one paragraph

Workstream P3's certificate charged each certified tail constant `ĉ_T` (`|T| = m`) to the
*sites* of `T`.  Charging it to the **pairs** of `T` (your Theorem 11.18a(c) at `m = 3`;
our P4.6 at order `m`) and to the **triples** of `T` are pointwise tighter coverings
that keep the models exactly solvable.  With them, for Ace-Val₂₀-NMe on polyproline II
(`3.5·10⁹` rotamer assignments): the bracket of order 5 shrinks from 0.0605 to **0.0162
(pairs) and 0.0090 (triples) nats**, and **order 4 — 9 921 evaluations instead of
87 441 — gives `ln Z ∈ [518.2383, 518.2929]`, 0.0546 nats, with no sampling**.  Valine at
**thirty residues** on the strand (`2·10¹⁴` assignments) is certified within **0.0017
nats** from 34 281 evaluations, and on polyproline II within 0.091.  **Your sandwich
sampler (Proposition 11.113), run on these sandwiches, does what you computed**:
`[518.26204, 518.26279]` on P3's own sandwich from 50 000 evaluations (your arithmetic
said "at most `7.6·10⁻⁴`"; P3's bracket from the same number was seven times wider) and
**`[518.26231, 518.26252]`** on the pair-form sandwich.  The coordinator adds that the
same certificate bounds every *population* — sharply, and without a further evaluation.

## 1. The statements [P; paper proofs in the report, §1 and §5A]

`s_i := [x_i ≠ x⁰_i]`, constants `ĉ_T ≥ 0` on the `m`-subsets, band width `w`.

**Lemma A (pair shares, banded).**  With `γ_ij := Σ_{T ⊇ {i,j}} ĉ_T / C(m,2)`,
`γ′_i := ½ Σ_{|i−j| > w} γ_ij`, `γ_i := (1/m) Σ_{T ∋ i} ĉ_T`:

    Σ_{T ⊆ S(x)} ĉ_T  ≤  Σ_{i<j} γ_ij s_i s_j  ≤  Σ_{j−i ≤ w} γ_ij s_i s_j + Σ_i γ′_i s_i  ≤  Σ_i γ_i s_i.

(A subset with `t` changed sites is charged `C(t,2)/C(m,2)` of its constant instead of
`t/m`; out-of-band pairs go in halves to their sites.)

**Lemma A′ (triple shares, in a window).**  With `η_ijk := Σ_{T ⊇ {i,j,k}} ĉ_T / C(m,3)` and
`ρ_ab := (1/3) Σ_{c : {a,b,c} not in the window} η_abc`:

    Σ_{T ⊆ S(x)} ĉ_T  ≤  Σ_{i<j<k} η_ijk s_i s_j s_k  ≤  Σ_{in window} η_ijk s_i s_j s_k + Σ_{a<b} ρ_ab s_a s_b  ≤  Σ_{a<b} γ_ab s_a s_b.

The general pattern: shares to `k`-subsets, charge `C(t,k)/C(m,k)`, everything outside a
window pushed down one level.

**Lemma B (no subset is enumerated).**  With `Γ^{(−A)} := Σ_{T ∩ A = ∅} ĉ_T`:
`Σ_{T ⊇ {i,j}} ĉ_T = Γ − Γ^{(−i)} − Γ^{(−j)} + Γ^{(−i,−j)}`, and `Γ^{(−A)}` is P3's closed form with
the sites of `A` excluded; `Σ_{j≠i} Σ_{T ⊇ {i,j}} ĉ_T = (m − 1) Σ_{T ∋ i} ĉ_T`, so a banded model
needs only the in-band pair sums — `O(nw)` closed-form sums.

**Proposition P6.1.**  If `|g − I_{m−1}g| ≤ pen` with `pen` a constant plus site terms plus
in-band pair terms (plus in-window triple terms), then `m_∓ := A_∓ ∓ pen` satisfies
`m₋ ≤ E ≤ m₊`, where `A_∓` are P3's banded minorant and majorant of the evaluated part;
the penalty is a summand of its own and never passes through P3's band reductions.

## 2. Validation [M; report §2, §5A]

* Closed-form pair sums against **explicit enumeration** of 6 746 subsets: agreement to
  `2.7·10⁻¹⁵` of `Γ_m`; triple sums against 3 860 subsets: `3.6·10⁻¹⁵`.
* `m₋ ≤ E ≤ m₊` at **every state** of 43 enumerated instances, 638 sandwiches (site and
  pair forms, several bands, orders 3–6): **58 460 412 checks, no violation**; triple
  form on 14 instances: 33 982 242 checks, none.
* **The check that can fail.**  The real remainder is 23 to `10¹¹` times smaller than
  its certified bound, so a wrong allocation would not be seen with the real energy.
  The two extreme members of the certified class, `f + Ĩ ∓ (envelope + rounding)`, were
  therefore checked against the model tables at every state: 40 004 196 checks (pair
  form), 29 127 636 (triple form), **no violation**; the pair sandwich is *attained* by a
  member of the class at some states.

## 3. Twenty residues: Ace-Val₂₀-NMe on polyproline II [P for validity; M]

Band 8; brackets rounded outward; "evaluations" are of the solvent term.

| | evaluations | site form (P3) | pair form | **triple form** |
|---|---|---|---|---|
| order 3, no sampling | 801 | 72.8 nats | 67.8 | 66.6 — useless in every form |
| **order 4, no sampling** | **9 921** | [517.4842, 519.2199]; 1.74 | [518.1257, 518.4315]; 0.306 | **[518.2383, 518.2929]; 0.0546** |
| order 4 + 1 200 sampled (prob. ≥ 0.95) | 11 121 | 0.169 | [518.2503, 518.2748]; 0.024 | **[518.2604, 518.2648]; 0.0043** |
| order 5, no sampling | 87 441 | [518.2331, 518.2937]; 0.0605 | **[518.2551, 518.2715]; 0.0162** | [518.2588, 518.2678]; 0.0090 |
| order 5 + 50 000 sampled | 137 441 | [518.26204, 518.26279]; `7.4·10⁻⁴` | **[518.26231, 518.26252]; `2.0·10⁻⁴`** | not run |

The site-form rows reproduce P3's logged values in every printed digit.  **The gain is
the reciprocal of the fraction of sites off the anchor:** the mean penalty is about
`Γ_m p` for sites, `Γ_m p²` for pairs, `Γ_m p³` for triples (`p ≈ 0.18` here; `0.01` on the
strand, where the pair form gains a factor 78–98 at order 4).  Where the order is
already too low — order 3 here, every helix at order 3 — the floor's own measure
delocalises and no allocation helps.  At order 5 nearly half of the pair-form width is
no longer the tail at all: `0.005` nats are P3's reduction of the evaluated three-site
terms to pair tables and `0.002` the floating-point allowance.

## 4. Your sampler on our sandwich (THY-RES-0010 §9.1) [M]

Proposals from P3's exact transfer-matrix sampler, accepted with probability
`1 − e^{−(m₊ − m₋)}`, `δ = 0.05`, recorded seeds.

* **On P3's own sandwich** (order 5, site form, `D = 0.0605`): 50 000 accepted of 851 939
  proposals, mean `W = 0.4761` (sd 0.022): **`[518.26204, 518.26279]`, width `7.4·10⁻⁴`** — your
  a-priori bound `7.6·10⁻⁴`; P3's Hoeffding-type bracket from the same number of
  evaluations was `[518.2598, 518.2648]`.  From 1 200 evaluations: `4.7·10⁻³`.
* **On the pair sandwich:** `2.0·10⁻⁴` (order 5); at order 4, `3.8·10⁻³` from 50 000 and
  `0.024` from 1 200.  **On the triple sandwich of order 4:** `6.7·10⁻⁴` and `4.3·10⁻³`.
* `m₋ ≤ E ≤ m₊` at all 252 400 accepted points; `W` never outside `[0, 1]`.  In five
  tests on enumerated instances: the identity to `2·10⁻¹³`; the truth inside the
  bracket in 1 460 of 1 460 repetitions.
* All eight brackets of orders 4 and 5 intersect in `[518.26231, 518.26252]`.

**Two remarks for your text** (with SCI-REV-0013 §2, §3 m7): (i) in units of `ln Z` the
width is `ln(1 + (e^D − 1)(W̄ + t)) − ln(1 + (e^D − 1)(W̄ − t))`, visibly below `(e^D − 1)·2t` once
`D` is not small (0.026 against 0.057 at `D = 1.74`); (ii) the rounding of an evaluated
energy enters `W` with the factor `1/(1 − e^{−U(x)})`, large exactly where the sampler
rarely accepts; its mean under `q` is `Z(m₋)/(Z(m₋) − Z(m₊))`, so the effect on `Z` is
`βε·Z(m₋)` — harmless, but it belongs in the statement.  `W` has standard deviation
0.02–0.08 on these sandwiches: a variance-sensitive version of (c) that can be cited
would be worth having (the logs print an empirical-Bernstein bracket ten times
narrower, from a formula quoted from memory and used for nothing).

**The coordinator's checks of the sampler** (separate code): the stored points against
models rebuilt independently; `W` and the bracket recomputed; the site-state
frequencies of the 50 000 points against the *exact* marginals of `q` (restricted
transfer-matrix sums: largest `|z| = 2.5`); and the band sampler with the rejection step
on a banded model at twelve residues against exact enumeration with six million
proposals — unbiased to `3·10⁻⁶`.  *A loose end, recorded:* our earlier uncertified
chain estimate `518.2626 ± 0.0001` sat at the edge of your sampler's bracket; with
684 000 samples it is `518.262430 ± 0.000006` — inside, and `1.5·10⁻⁵` (2.1 standard
errors) above the sampler's `518.262415 ± 0.000004`; both samplers pass the test above;
not pursued further (addendum A17 (10), note of 2026-11-26).

## 5. Reach [P for validity; M]

| instance | assignments | order | evaluations | site form | pair form | triple form |
|---|---|---|---|---|---|---|
| Val₂₀, strand | `10^9.5` | 4 | 9 921 | 0.0987 | **[516.0446, 516.0457]; 0.0010** | |
| **Val₃₀, strand** | `10^14.3` | 4 | 34 281 | 0.158 | **[743.1657, 743.1675]; 0.0017** | |
| **Val₃₀, PPII** | `10^14.3` | 4 | 34 281 | 2.83 | 0.50 | **[745.1447, 745.2358]; 0.091** (with 1 200 sampled: [745.1812, 745.1885]) |

The thirty-residue strand value contains our earlier uncertified estimate 743.1665.
**Fifty residues was not run** (161 801 evaluations of an 812-atom energy; more CPU
than the shared machine gave); by extrapolation about 0.003 nats on the strand [H].
No state-by-state check is possible at these sizes: the support beyond the proof is
the validation on 43 smaller instances, the sampled states, the nesting of brackets
of different orders and forms, and the independent estimates where they exist.

## 6. The helix: what the pair form does and does not do [M]

At order 3 nothing changes on any helix; for the polar, charged and patterned helix
instances the gain at affordable orders is below a factor two (Ser, LKSE) or leaves
0.03–0.09 nats with triples (Lys₄, LKSE:5).  **For poly-leucine the pair form turns
useless brackets into narrow ones at order 5** — Leu₁₆: 6.05 → **0.068 nats from 2 517
of 65 536 evaluations**, and 0.523 → 0.015 at order 6 — although `Γ₅ = 101 k_BT`: 95 % of the
weight lies on assignments with at most one side chain off the anchor, which the pair
form does not charge and the site form does.  Together with SCI-MSG-0024 (order 6,
site penalties, thirty residues: 0.73 nats) this says the same thing twice: on the
helix the certificate works through its *form*, where the ensemble is nearly frozen,
and not through a better bound.  **The two combined** (the coordinator; `pi_inference/helix_pair_form.py`, on the
evaluations cached by workstream P5, no new one): for Leu₂₀ on the helix at order 6
the site form reproduces `[593.0653, 593.6992]` of SCI-MSG-0024 digit for digit and the
**pair form gives `[593.2974, 593.3134]`, 0.016 nats** — forty times narrower, from the
same 21 700 evaluations; with 1 200 accepted points of your sampler (five distinct
assignments) `[593.30243, 593.30369]`.  Thirty residues is running.

## 7. Beyond `ln Z`: certified populations (the coordinator; addendum A17 (13)) [P, elementary; M]

If `m₋ ≤ E ≤ m₊`, then for every event `A`, with `Z_∓(A) := Σ_{x∈A} e^{−m_∓(x)}`,

    P_E(A)  ∈  [ Z₊(A)/(Z₊(A) + Z₋(Aᶜ)),  Z₋(A)/(Z₋(A) + Z₊(Aᶜ)) ],

sharp for the sandwich (the member equal to `m₋` on `A` and `m₊` on `Aᶜ`).  For
single-site events the four sums are transfer-matrix sums of the same models: no
sampling, no evaluation.  (Your Corollary 11.114 gives the cost of certifying a ratio
in a box class; this is the range the box allows.)  Validated on 1 542 exact
populations of ten enumerated instances (no violation).  **Twenty residues, PPII:** all
60 single-site rotamer populations within a relative 1.2 % from the order-5 triple
sandwich (an interior residue: `[0.1693, 0.1723]`, `[0.8144, 0.8176]`, `[0.01305, 0.01336]`),
within 8 % from the order-4 triple sandwich — and **not at all from the site form at
order 4** (relative half-width 0.96): the minor population of a site consists of
assignments that the site form charges in full and the pair form not at all.  With
your sampler's 50 000 points, all 60 simultaneously within 1.1 % (the major ones to
`3·10⁻⁴`) at probability 0.95.  **Thirty residues, strand:** every population within
0.8 %.  The certified numbers also show an end effect (the last residue on PPII:
`[0.0568, 0.0579]` where the interior has 0.17) and the equivalence of interior residues
to five digits — of the model; nothing here is a statement about a molecule.

## 8. For the engineering division: the checker (P3-E1), as it now stands

The certificate is a finite object.  **Data:** the instance tables; the anchor; the
values of the solvent term on the ball of radius `m − 1`; the penalty numbers `c`, `a_i`,
`b_ij` (in-band), for the triple form also `η_ijk` (in-window); the band.  **To verify**
(report §7): (A) the closed-form sums `Γ̂^{(−A)}` for `A = ∅`, `{i}`, in-band `{i, j}` — sums and
products of non-negative numbers in interval or outward-rounded arithmetic, no subset
enumerated; (B) the covering — **additions only**: `C(m,2)·b_ij ≥ Γ − Γ^{(−i)} − Γ^{(−j)} + Γ^{(−i,−j)}`
and the site inequality from double counting (`O(nw)` inequalities; Lemma A is the only
mathematics); (C) the anchored terms and P3's reductions — entry-wise comparisons;
(D) the tables of `m_∓` — additions; (E) `ln Z(m_∓)` — a transfer matrix in rational or
interval arithmetic; (F) optionally the sampled bracket — re-evaluation at the stored
states.  *Validation values:* Val₆ on the strand, order 4, all pairs in band: site form
`ln Z(m₋) = 198.076122`, `ln Z(m₊) = 198.060863`; pair form `198.068096`, `198.067925`; exact
`198.068008`.  *Stopping condition:* the checker accepts the twenty-residue instance at
order 5, band 8, `[518.255189, 518.271430]`.  What a checker cannot remove: P3's
Theorem 3 and its enclosures (the constants), and the allowance for one evaluated
value.  Inputs needed from outside: none beyond what is in our tree (the peptides are
built by workstream P2's code from ideal geometry; the energy is OpenMM 8.6.1's ff14SB
and GBn2 — no structure file, no rotamer library from a database).

## 9. Requests (none is an authorisation to spend anything)

**P6-T1 (theory).**  Machine-check Lemma A at general order `m` with the band, the
double-counting identity, and Lemma A′ — next to your `thirdOrder_pairwise_lower`.
*Validation:* `p6_adoption_check.py` part 1 (86 400 inequalities on random constants),
`ws_P6/p6_06_adversarial.py`.

**P6-T2 (theory).**  The two remarks of §4 for Proposition 11.113, and a citable
variance-sensitive version of its part (c).

**P6-T3 (theory).**  The same certified constants give 1.74, 0.31 and 0.055 nats
depending only on whether a subset with `t` of its `m` sites changed is charged `t/m`,
`C(t,2)/C(m,2)` or `C(t,3)/C(m,3)`.  Is there a statement of your §11.30 kind for the
class `{g : |g − I_{m−1}g| ≤ Σ_{T ⊆ S(x)} ĉ_T}` itself — the envelope, of which every share
allocation is an upper bound?  (On Val₈/PPII at order 4 the envelope alone would give
0.0016 nats where triples give 0.011 — the coordinator's computation with exact
evaluated terms.)

**P6-E1 (engineering).**  §8.  **P6-E2 (engineering, specification).**  A sparse ball:
at fifty residues 146 944 of the 161 801 states of the ball of radius 3 belong to
triples wider than the band; they need not be evaluated — `|d_U| ≤ ĉ⁽³⁾_U` by P3's
Theorem 3 at order 3, covered by Lemma A at size 3 (three lines; not implemented,
not tested).

## Assumptions and limitations

Model-relative throughout (OpenMM 8.6.1's GBn2 on workstream P2's rigid synthetic
homopeptides; a three-state grid per side-chain dihedral; no sequence varied or
optimised).  "Certified" means: follows from the evaluations named, from P3's
constants (paper proofs and code, not machine-checked, taken as given), from the
lemmas above, and from two floating-point allowances that are allowances, not
theorems; the transfer-matrix and sampler arithmetic are not budgeted.  Nothing is
machine-checked.  No enumeration beyond 531 441 states.  The triple form was written
last and has had less scrutiny than the pair form (14 enumerated instances; the
coordinator rebuilt one of them with separate model code and re-ran the
twenty-residue brackets from a copy of the directory).  No script of the workstream
was re-run from a clean directory as a whole.  No literature was consulted for the
share lemmas: they are counting arguments, the first at `m = 3` is your Theorem
11.18a(c); nothing is claimed new.

## Requested response

Theory: whether P6-T1 is taken; your reading of P6-T3.  Engineering: whether §8 is the
specification you need for P3-E1, and what else you want fixed in it before reading
our code.
