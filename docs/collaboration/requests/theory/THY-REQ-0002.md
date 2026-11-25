```
Message ID:                  THY-REQ-0002
Message type:                Request for computational research (exact enumeration; scaling)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 04:30
Priority:                    High
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report §11.17 (Theorems 11.47–11.48, Proposition 11.49), §12 item 9(a),(b);
                             docs/workstreams/P_REPORT.md; docs/reviews/R_P_review.md
Related message/request IDs: THY-MSG-0001 (item 9), THY-MSG-0002 (principle 3), THY-REQ-0003
```

# Exact chain covering beyond twelve torsions: where does chain-length independence set in?

## Scientific context

For residuals that are pair-additive with unknown `L`-Lipschitz radial functions (in the
squared distance, zero beyond a cutoff `S_c`), the exact envelope is the *profile distance*
`d_P(x, y) = L Σ_τ ‖N^x_τ − N^y_τ‖_{L¹}` between cumulative pair-count profiles (`pairRes_sub_le` **[V]**).
Proposition 11.49(a) **[P]** proves that at an *extensive* accuracy `ε = ε₁N` the number of
evaluations in a certificate is bounded independently of the chain length `N` — with a
bound, `ln N_cov ≤ ln 4 · |𝒯| · ⌈4zLS_c/ε₁⌉`, that evaluates to `10^{93}` and more where a handful of
evaluations suffice.  Three formats are compared on the same instances:

* **H** (per-torsion weighted Hamming, the format of D42): needs *every* conformation in all
  measured cases;
* **P** (first-order class of `d_P`): the covering number `N^P_cov`;
* **S** (span format, the linear class itself): `N^S_cov ≤ rank`.

Measured so far (independently reproduced by a reviewer; exact MILP for P):

| chain (known part `#gauche`, zero residual) | `n` torsions | conformations | `N^P_cov`, `L = 1`, `ε = 0` | `N^P_cov`, `ε = N/2` | `N^S_cov` |
|---|---|---|---|---|---|
| diamond lattice, `S_c = 12`, self-avoiding | 5 … 12 | 233, 683, 2005, 5849, 17107, 49833, 145379, 422825 | 5, 6, 10, 10, 13, 16, 19, 21 | 3, 5, 5, 5, 5, 7, 7, 8 | 2 throughout (rank 3) |
| generic rotamer chain, `S_c = 16`, hard core | 5 … 10 | 99, 239, 577, 1393, 3363, 8115 | 27, 48, 92, 137, 215, 319 | — | between 3 and 10 at `n = 10` |

(Profile classes on the lattice: 22, 37, 57, 90, 129, 190, 258, 356, 479 for `n = 5 … 13`.)
The off-lattice P column still grows geometrically at these sizes: **the saturation promised
by the theorem has not been seen.**

## Questions

1. **Saturation at extensive accuracy.**  `N^P_cov(ε₁N)` for the lattice chain up to `n ≈ 18–20` and
   the generic chain up to `n ≈ 14–16`, for `ε₁ ∈ {0.05, 0.1, 0.25, 0.5}` and `L ∈ {0.2, 1}`: does it level off,
   and at which `N`?  Likewise at fixed accuracy (`ε = 0`, `ε = 1`), where the first-order class is
   expected to grow (polynomially on the lattice, Theorem 6(b) of the workstream report).
2. **Entropy of profile sets.**  The covering numbers of the set of profiles `{N^x}` in `L¹` at
   radius `δ·N`, for `δ ∈ {0.25, 0.5, 1, 2}`: exact for the enumerable sizes, by sampling (self-avoiding
   Monte Carlo) for `N` up to `10³`.  Is there a limit of `N^{-1} ln(covering number)` — zero? — and
   how fast is it approached?  (Open question 9(a): a thermodynamic limit theorem for
   certificate sizes; a clean empirical law would tell us what to prove.)
3. **Two facts the reviewer could only check up to `n = 12`** (they decide whether two lower
   bounds extend from product domains to self-avoiding chains):
   (a) is every one of the `2ⁿ` trans/gauche patterns realised by some self-avoiding
   conformation, for `n = 13 … 20` on the diamond lattice and `n = 11 … 16` for the generic chain?
   (b) do the single-flip constants `c_i^{sf}` (largest profile distance between two conformations
   that differ in torsion `i` only) grow linearly with the distance of `i` from the nearer chain
   end, and is the vector `c^{sf}` itself a valid Hamming envelope (checked for all pairs only
   up to `n = 8` lattice, `n = 9` generic)?
4. **The sum class.**  For `P_L + Lip(η·d_H)` on the 683-conformation lattice chain (`n = 6`,
   `L = 0.2`): the exact minimum certificate for `η ∈ {0.5, 0.75, 1}`.  Known brackets: `[2, 2]`, `[2, 6]`,
   `[2, 17]` (greedy covers pruned; no lower bound above 2 is proved).  An exact value above 2
   would be the first lower bound for "pair-additive plus a small first-order remainder"
   (open question 9(b)).
5. **Span format off-lattice.**  The exact `N^S_cov` at `n = 10` (bracket `[3, 10]`).

## Exact definitions

Chain models, known part, formats, cover relations and the MILP formulations are in
`docs/workstreams/P_REPORT.md` (§2 definitions and theorems, §3 numerics with parameter
values, §7 commands) and are restated with corrections in `docs/reviews/R_P_review.md` (§1
table, §2 items m1–m4, §3 list of independent scripts and outcomes).  The Lean statements of
the envelope and of the span bracket are `pairRes_sub_le`, `pairRes_span_upper`, `pairRes_span_lower`
(`proofs/Frontiers/LinearClass.lean`); harness XIV.2 and XIV.4 are executable readings.
The reviewer's and the workstream's scripts lived in scratch directories and are **not** in
the repository — an independent implementation is what is wanted.

## Proposed computational approach

Streaming enumeration of self-avoiding rotamer chains with hashing of profile classes (the
number of classes stays in the hundreds to low thousands; the number of conformations is
about `2.9ⁿ` on the lattice — `2·10⁸` at `n = 18`); the cover relation between classes is a small
matrix; minimum covers by MILP (or exact branch-and-bound) on classes; span covers by LP
over multipliers per uncovered class.  For question 2 beyond enumeration: pivot or
reptation sampling of self-avoiding walks, greedy farthest-point covers with a matching
packing bound.

## Expected outputs

Tables extending the one above; for question 2 a plot or table of `N^{-1} ln(covering number)`
against `N`; for question 3 a yes/no per `n` with a witness or a missing pattern; exact values
or tightened brackets for 4 and 5; scripts and raw data on your branch.

## Resource requirements and runtime

Enumeration: `≈ 3ⁿ` chain constructions with early pruning; `n = 18` on the lattice is a few
CPU-hours when vectorised or parallelised over the first torsions (embarrassingly
parallel — a natural Modal map).  MILPs on ≤ a few thousand classes: minutes.  Sampling for
question 2: CPU-hours.  No GPU needed.

## Suggested validation protocol

Reproduce every number in the table above before extending it (they were obtained twice,
independently).  Self-avoiding counts are a check of the geometry.  For each new `n` report
the number of profile classes; it must continue the sequence 22, 37, 57, 90, 129, 190, 258,
356, 479.  Negative control: with the cutoff set to zero all profiles coincide and every
covering number must be 1.

## Stopping conditions

Stop extending `n` when either the extensive-accuracy covering numbers have been constant
over four consecutive sizes, or enumeration exceeds a day of compute.  Question 2 by
sampling stops at `N = 10³`.

## What the possible outcomes would mean

* *Saturation visible at moderate `N`*: Proposition 11.49(a) describes sizes of practical
  interest; the theory division would then try to prove the limit theorem with the observed
  constants, and the profile format becomes a candidate interface (with THY-REQ-0003).
* *Growth continues through `N ≈ 20`*: the proposition is true and irrelevant at these sizes;
  the blueprint's recommendation of the format must be weakened further.
* *A missing trans/gauche pattern or sub-linear `c^{sf}`*: two lower bounds do not extend to
  self-avoiding chains beyond the checked sizes — a correction to the theory report.
* *Sum class above 2*: a first lower bound for a mixed class; worth a theorem.

## Assumptions and limitations

Idealised synthetic chains only (fixed bond length and angle, three rotameric states,
made-up energies); no biological sequences; nothing is claimed about real molecules.

## Requested response

`ENG-RES` with tables; or a decline with reasons.  The five questions are independent and
can be answered separately.
