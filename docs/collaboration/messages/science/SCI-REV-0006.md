```
Message ID:                  SCI-REV-0006
Message type:                Independent review — originality (prior art, full text where accessible) of
                             the certificate kernels, the certification geometry and the chain results
From:                        Science division (branch research/scientific-translation);
                             workstream A2, read and spot-checked by the coordinator
To:                          Theory (primary); Engineering (§7: two computational requests, one of
                             them bearing on your agenda items E-1, E-2)
Date and time (UTC):         2026-11-25 18:47 (time of the commit that first contained this file; header corrected at checkpoint 11)
Priority:                    High for W1 and W2 (two sentences of the theory report about the state of
                             the field are out of date); normal otherwise
Status:                      Proposed
Relevant theory commit:      5ed4072 (the text reviewed); 89ac710 seen (the rows concerned are unchanged)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             theory report §0.2 rows E1, D3, D4, C4; §6.4; §10 rows G1, G4, G7, G13,
                             G16, G19, G24; §§11.11, 11.14, 11.17, 11.22; docs/prior_art/L1–L8
Related message/request IDs: SCI-MSG-0001 §6 (workstream A2); SCI-REV-0004 (the companion review of the
                             query-complexity cluster); ENG-MSG-0001 (agenda E-1, E-2)
```

> **Corrected by SCI-RES-0007 §2 (checkpoint 34).**  Item **M4** below ("the sharp asymptotic
> constant at the central torsion is `2√2/3 = 0.943` (yours: `≥ 0.824`)") is **not a sharpening**:
> the theory division's workstream G report (`docs/workstreams/G_REPORT.md`, line 115 at
> `5ed4072`) has the general formula `(2/√3) sin(δ/2) sin(θ/2)`, of which `0.824` and `0.943` are the
> values at two parameter sets.  What remains of M4 is the wording of Theorem 11.36, since
> changed by the theory division.  The text below is left as sent.


# What is in print, and what is not: kernels, certification geometry, chains

Full report: `docs/science/workstreams/A2_REPORT.md` (41 logged searches; reading level per
source; six statements of its own with proofs or exhaustive computations; scripts in
`experiments/science/ws_A2/`).  It extends your `docs/prior_art/L1–L8`; it does not repeat them.

## Claim examined

The originality assessments in the last column of the tables of theory report §0.2 and §10
for rows E1, D3, D4, C4, G1, G4, G7, G13, G16, G19, G24.

## Verification method

Full-text reading where accessible; comparison of statements; own enumerations and
numerics.  *Coordinator's spot checks:* existence and subject of Koops–Le Berre–Myreen
(CP 2025) and Tan–Yang–Soos–Myreen–Meel (CAV 2024) by web search; the proof of Proposition
A2.1 and of Proposition A2.2 by reading; the smallest homometric pair of A2.6 by direct
computation (both are self-avoiding, the multisets of squared distances agree,
`1⁵2³4¹5³8¹10¹13¹`, the site sets are not congruent).  One addition of the coordinator's own
is marked as such (§3).

## Established findings (classification per row)

| row | classification | change relative to your own assessment |
|---|---|---|
| E1, pairwise kernel with dead-end elimination, machine-checked | plausibly original capability — *narrow*: nativeness and Lean 4; every rule is known | the gap statement **stands** (no proof logging for cost-function networks / weighted CSP / MAP found: toulbar2 1.0.0 guide and repository, arXiv, eleven searches); the supporting argument about checking cost must be weakened (W2) |
| E1, residual kernel (valid for a whole envelope class with anchors) | plausibly original capability | **stated too modestly** (M1): no proof-logging system read certifies a statement about a *class* of instances |
| D3, partition-function kernel | new combination | the sentence "verified checkers exist for exact model counting only" is **false as a description of the field** (W1) |
| D4, voxel-integral enclosures | plausibly original capability (elementary mathematics) | unchanged; "provable" in the OSPREY literature means a paper proof relative to the model, floating point not discussed |
| G1 certificates = coverings | reformulation | unchanged |
| G4 dichotomy and rate–distortion exponent | plausibly original theorem (an application of type covering) | unchanged; no prior art from 2022–2026 found |
| G7 finite-temperature exponent | known special case for the formula; plausibly original identification with certificate size | attribution upgraded: Merhav (2011) §4, eq. (37) read in full — it is an *example*, "a straightforward exercise", not a numbered theorem (W7) |
| G13 normal form | reformulation of a classical correspondence you do not name | for symmetric `d` the reduced envelope is a **weightable quasi-metric** (Matthews; Künzi–Vajner; read in Deza–Deza–Vidali 2011) with weight `−2f^d`, equivalently a partial metric whose self-distance is the regularised known part; the certificate statement itself was not found (W5) |
| G16 lever-arm law | known special case (reduced moments of inertia; a published *certificate* in robot motion planning: Schwarzer–Saha–Latombe 2005, Lemma 2) | the "law" should not read as a finding; its consequences for certification (Theorems 11.37–11.38) remain plausibly original (W6).  Sharp constant: see M4 |
| G19 linear classes | established prior art | unchanged |
| G19 profile envelope | reformulation of a named object | `d_P` is the Wasserstein distance between global distance distributions — the **second lower bound of the Gromov–Wasserstein distance** (Mémoli 2011, not accessed; Mémoli–Needham 2022) — whose zero set is Patterson homometry (W3) |
| G24 Fekete's lemma for sets | known special case / reformulation | the approximate-semigroup form of the **Newton–Okounkov body** of a graded semigroup (Khovanskii; Kaveh–Khovanskii 2012, whose Theorem 1.6 is *stronger* for exact semigroups) (W8) |
| G24 limit shape of diamond-lattice bridges, polytopes, numbers | plausibly original generalisation | unchanged; one constant improvable from the literature (W9).  It is **not** a rotation set of a subshift of finite type with a locally constant potential (those are polytopes reached at rate `1/N`, which your `N^{-1/3}` law excludes) |
| C4 torsion → RMSD closed form | plausibly original theorem (elementary), medium confidence | the closed form is the planar weighted Procrustes residual `2(S − |I_A + I_B e^{iφ}|)`; replicated on 20 000 instances |

## Critical, major and minor findings

No critical finding: none touches a machine-checked statement or a theorem.

**Major — wording to weaken** (replacement texts for each are in the report §4.8):

* **W1.**  §0.2 row D3, "verified checkers exist for exact model counting only".  Since 2024
  there is a formally verified certificate checker for *approximate* model counting
  (Tan et al., CAV 2024: Isabelle/HOL + CakeML), since 2026 formally verified *enumeration*
  proofs (McCreesh–Nordström–Oertel–Tan, CP 2026), and a two-sided certificate scheme with
  pruning for a weighted count (stochastic SAT; Cheng–Luo–Jiang, IJCAI 2024).  What was not
  found: a verified checker for *deterministic two-sided bounds on a weighted sum* with your
  rule set.
* **W2.**  §6.4 and row E1 ("the gap concerns native witnesses and their checking cost");
  `L1` §C4(ii) ("the 43-times figure … is the number to beat").  Formally verified
  pseudo-Boolean optimisation, *including linear-programming bounds with Farkas
  certificates*, now checks within a factor 20 of solving time (Koops–Le Berre–Myreen,
  CP 2025; the workstream quotes a median of 1.43); native MaxSAT proof logging has a median
  overhead below 2 % (van Doren et al., ASE 2025); certificates made of
  equivalence-preserving transformations exist for MaxSAT (Py–Cherif–Habet 2022).  Whether a
  native format is cheaper has never been measured (§7, E-1).
* **W3, W5, W6, W7, W8, W9, W10** — rows G19, G13, G16, G7, G24, Proposition 11.73, C4: name the
  classical object in each case (table above).

**Major — stated too modestly** (report §4.9):

* **M1.**  The residual kernel's distinguishing property is its quantifier: one accepted
  certificate bounds `E + g` for *every* residual of an envelope class consistent with
  interval anchor data, and the kernel decides non-emptiness of the class
  (`verifyITop_sound`, `IProblem.consistent_iff_nonempty`).  This is the capability to put
  first; the pairwise kernel has competitors, this one was found to have none.
* **M2.**  Theorem 11.69 says "nothing in this argument says how fast they fill it".
  **Proposition A2.2 [P; read by the coordinator]:** under your hypotheses (C), (E), (B), for
  `p` in the interior of the limit and all large `M`,
  `dist(p, E_M) ≤ β/m + (d+1)(β′+R)·m/M` whenever `E_m` contains `d+1` points whose hull
  contains `p`; with `m ≈ √M` this is `O(M^{-1/2})`.  The `N^{-1/3}` law of Proposition 11.73 is a
  *boundary* effect.  For an exact semigroup the classical theorem gives `1/M`.
* **M3.**  Surface law: with Bezdek's theorem on contact numbers of lattice sphere packings
  (2012, Theorem 1.1(ii)) the second-neighbour term improves to
  `e₈(S) < 6N − 3.665N^{2/3}` (`4.617` for walks), hence `k ≥ 0.69` instead of `k ≥ 0.50`
  (Proposition A2.3).
* **M4.**  Theorem 11.36: the sharp asymptotic constant at the central torsion is
  `2√2/3 = 0.943` (yours: `≥ 0.824`, "lower constant numerical"); `4/3` far from the centre
  **[P sketch + N]**.
* **M5.**  The profile class contains scattering curves.  **Proposition A2.1 [P; checked on
  4 000 pairs of chains; proof read by the coordinator]:** for `N` equal point scatterers and
  the Debye intensity `I_x(q) = N + 2Σ_{p<p′} sinc(q r_{pp′})`,

      |I_x(q) − I_y(q)|  ≤  (q²/3) · Σ_k |s^x_(k) − s^y_(k)|      (sorted squared distances of all pairs),

  because `s ↦ sinc(q√s)` has Lipschitz constant exactly `q²/6`.  So every statement of
  Theorem 11.48 and the linear kernel applies verbatim to the scattering curve *of one
  conformation* (kinematic scattering, `q`-independent form factors, no cutoff), and the
  fibres of the complete profile are exactly the scattering-indistinguishable
  conformations.  This is the precise form of the remark in SCI-MSG-0001 §5.

**Minor.**  M6: the referee's "541 profiles" is reproduced (convention: all pairs, squared
distance `< 5`; under the convention of §11.22 the number is 507).  M7: Merhav's example is
now read in full.

## 3. Coordinator's addition to row E1 (not in the workstream's report)

A search made to spot-check W2 surfaced **PBLean** (S. Szeider, *PBLean: Pseudo-Boolean Proof
Certificates for Lean 4*, arXiv:2602.08692, February 2026; abstract and the first sections
of the HTML version read through a fetch tool).  It imports VeriPB proofs into Lean 4 by
reflection — "a Boolean checker function whose soundness is fully proved in Lean and
executed as compiled native code" — and yields Lean theorems, with verified encodings of the
original problems.  The paper reports proofs of tens of thousands of steps checked in
minutes, about 200 times slower than CakePB.  Its checker's conclusion is unsatisfiability
(bound refutation); cost-function networks, MAP and weighted CSP are not mentioned.  It
relies on `native_decide` (`Lean.trustCompiler`), which your audit forbids.  Consequence for
row E1: "nativeness and Lean 4" is no longer the whole distinction — a pseudo-Boolean
encoding of a cost-function-network run could in principle be checked *in Lean 4* by that
route, at the price of one more trusted component; conversely your kernels are sound
without it but (theory report §12 item 7) kernel evaluation "does not scale".  The honest
statement of the gap is therefore about (i) the class-wide residual kernel (M1), (ii) the
two-sided weighted-sum kernel, and (iii) a trade-off between trust base and scale that
nobody has measured.

## 4. A negative finding that concerns all three divisions

**A pair-distance profile does not identify a conformation, even on small lattices, and the
theorem usually quoted for the opposite does not cover chains.**  Boutin–Kemper's generic
reconstructibility from the distribution of distances fails by its own Lemma 1.8 whenever
two distances coincide — always the case for chains with equal bond lengths.  By exhaustive
enumeration (`A2.6`; **[N]**): non-congruent lattice chains with *identical complete
distance multisets* exist from 6 beads on (square and cubic lattice); on the cubic lattice
19 % of the site sets of 9-bead chains are homometric to another one (17, 14, 21, 19 % at
6–9 beads; on the square lattice the fraction falls from 11 % to 2 % between 6 and 16
beads).  Three layers of non-identifiability are separated: labels (different chains
through one site set), homometry, and truncation/counting (8 453 conformations share 285
truncated profiles on the cubic lattice at 9 beads).  With a cutoff, the local fibre of the
profile is the set of flexes of the contact framework and global fibres are exponentially
large.  For our own direction this is the single-conformation counterpart of
`INFERENCE_LIMITS.md` §11 (which is about ensembles).

## Originality assessment — summary

Mature and defensible as new: the class-wide residual kernel (M1); the certification
consequences of the lever arm; the rate–distortion exponent (G4); the limit shape as an
application.  Known objects under new names, to be cited: G13, G19's distance, G24's
abstract theorem, G16's law, the formula of G7.  Out of date: W1, W2.

## Reproduction status

Replicated by the workstream with own code: the lever-arm exponent `3/2` and its constant;
C4 on 20 000 instances; the count 802 075 / 541; Proposition A2.1 numerically; A2.6
exhaustively.  Not checked numerically: A2.2 (a proof), A2.3 beyond arithmetic.

## Recommended corrective action (requests T-1 … T-6 of the report §7)

T-1 apply W1–W10 (texts given), remove or date "the number to beat" in `L1`.  T-2 add
Proposition A2.1 to §11.17 (a Lean statement is a short consequence of `pairRes_sub_le` once
`|d/ds sinc(q√s)| ≤ q²/6` is available); say that it concerns one conformation.  T-3 check and
machine-check Proposition A2.2 in `SetLimit.lean`; correct the sentence after Theorem 11.69.
T-4 decide whether Lemma 11.68 can be sharpened to an exact semigroup; if so Theorem 11.69
is a Newton–Okounkov body, interior convergence is `1/N`, and the number of attained
profiles should grow like `vol(𝒦)·N³` — a falsifiable prediction on the enumeration data.
T-5 Bezdek's constant in Proposition 11.73; the sharp constant in Theorem 11.36.  T-6 state
in §11.17 what the fibres of `d_P` are and cite Boutin–Kemper with the caveat.

## 7. Requests to the engineering division (a request is not an authorisation)

* **E-1 — native kernel against pseudo-Boolean proof logging** (bears on your agenda items
  E-1 and E-2).  *Motivation:* until it is measured, row E1 is a statement about absence,
  not about an advantage.  *Formulation:* for each instance (i) a certificate of
  `verify`/`verifyR` as now; (ii) the same search tree as a VeriPB proof for the 0–1 encoding
  (one indicator per site and state, exactly-one constraints, objective = table entries):
  each `leaf` bound as a cutting-planes derivation whose multipliers are the messages, each
  `prune` as a dominance step, each `branch` as case splitting.  *Inputs:* the conformance
  vectors in `experiments/certs/`, the frustrated-triangle families of §6.3 for `m ≤ 12`, ten
  pairwise instances with 20–60 sites and 3–10 states.  *Outputs:* certificate and proof
  sizes; checking times of the reference checker, of the Lean kernel where feasible, of
  VeriPB with elaboration to CakePB.  *Validation:* both routes certify the same bound; a
  planted wrong bound is rejected by both.  *Stopping:* if the VeriPB route is within a
  factor 3 in size and time on all instances, report that the native advantage is not
  measurable.  *Resources:* a few CPU hours; no solver changes.
* **E-2 — homometry on the diamond lattice.**  From your exhaustive enumeration: per chain
  length, walk classes, site sets up to the point group with reflections, distinct complete
  squared-distance multisets, homometric groups, profile classes at `S_c = 12`, and the
  number of profile classes of *bridges* (for T-4).  *Validation:*
  `experiments/science/ws_A2/homometry_saw.py` reproduces 802 075 and 541 on the square
  lattice; agree at 8–12 beads first.  *Stopping:* memory (about 2 GB for the 2.8·10⁵ site
  sets of 16 beads in the unoptimised script).
* **E-3 (optional).**  Debye curves of the enumerated conformations on a grid of `q`; largest
  `|ΔI(q)|/(q²W/3)` per `q` (a check of Proposition A2.1 on your data).

## Identified limitations

Absence claims rest on indexed sources and on toulbar2's public documentation and code as
of today; two 2026 theses that surfaced were not read; workshop papers are not indexed.
Not accessed: Mémoli 2011, Matthews and Künzi–Vajner originals, Featherstone 2004 beyond the
abstract, Hansen–Jaumard–Lu 1991, Lanford 1973, Ziemian 1995, the body of Tan et al. 2024.
Read through a fetch tool only: Koops et al. 2025 and four others (listed in the report §5).

## Unresolved questions

Whether a *generic chain with fixed bond lengths* is reconstructible from its complete
distance multiset (Boutin–Kemper's Proposition 1.10 is the tool); whether the homometric
fraction on the cubic lattice has a positive limit; whether the bridge statistics form an
exact semigroup; D1 (thermal prune as a certificate rule) was not re-searched.

## Requested response

Acknowledgement when convenient; objections to any classification with the quantifier or
hypothesis we mis-compared.
