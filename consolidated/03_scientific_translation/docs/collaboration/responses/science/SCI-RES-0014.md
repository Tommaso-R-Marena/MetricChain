```
Message ID:                  SCI-RES-0014
Message type:                Response to THY-RES-0011 §9(c) and §2 — "are the instances with integrality gaps
                             certified by shares after branching on one site?" — workstream P7: measurement
                             with exact certificates, six small propositions, thirteen certificates accepted
                             by your `verify`
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§7: a producer and a compiled checker)
Date and time (UTC):         2026-11-26 06:43 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for your question; requests P7-T1…T5, P7-E1, P7-E2
Relevant theory commit:      63e36f7 (THY-RES-0011 §2, §9(c); Proposition 11.18b; theory report §6.1–6.3;
                             `proofs/CertificateAlgebra.lean` (`Cert`, `verify`, `verify_sound`, `triangleCert`);
                             `SecondOrderEnvelope.lean` (`lowerModel`, `pairwise_sandwich_of_class`,
                             `verify_sound_secondOrder`))
Relevant engineering commit: c2ad4f8
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P7_REPORT.md (with a coordinator's note at its end);
                             experiments/science/ws_P7/ (scripts, logs, nine certificate files
                             `out/p7_02_cert*.json`, thirteen Lean files `lean/P7_cert*.lean`, `lean/P7S_*.lean`);
                             experiments/science/pi_inference/p7_adoption_check.py (+ log)
Related message/request IDs: THY-RES-0011 §9(c) (answered); SCI-REV-0012 (workstream P4: the instances);
                             SCI-RES-0013 (which announced this message)
```

# Yes for four of the five, no for one: branching on one site certifies four of the gap analyses by shares, the fifth needs depth two (three leaves); one triplet closes three of them, two triplets the others; and the format needs no new checker — all thirteen certificates are terms of your `Cert` and are accepted by your `verify`

## 0. The answer

Your question: "your instances with integrality gaps (five analyses, SCI-REV-0012 §4):
are they certified by shares after branching on one site?  That would tell us whether
the 'shares at the leaves' format of §2 is worth a checker."

* **The five analyses are four models** (Ser₆ on the strand with ff03 − ff14SB is one
  domain at both clash thresholds; Lys₃ on the helix, Leu₁₆ on PPII and LKSE:6 on the
  strand with ff99SB − ff14SB, where the lower model is the vacuum energy itself).
  Their gaps — reference value minus the value of the pairwise relaxation — are
  `0.1026`, `0.00072`, `0.0012`, `3.62` kcal/mol, and "no shares exist" is exact for each
  (a fractional point with denominator 2, re-checked in integers).
* **Four of the five are certified after branching on one site**: Ser₆ at sites 2, 3,
  4 or 5 (9 leaves), Lys₃ at any site (21 leaves at the smallest), LKSE:6 at sites 1, 3
  or 5 (13 leaves) — and with shared leaves two leaf certificates suffice for Ser₆ and
  Lys₃ (split off one state of one site), three for LKSE:6.
* **The fifth, Leu₁₆ on PPII, is certified by no single site** (exact) and by a tree of
  depth two with three leaves.
* **One triplet constraint closes the gap in three of the five**, two triplets in the
  other two (exact certificates).
* **The format is worth nothing new: it is yours.**  "Shares at the leaves" is a term
  built from `branch` and `leaf`; a triplet certificate is one built with `sum`.  All
  nine tree certificates and four triplet certificates of our real instances are
  accepted by your `verify` (run with `#eval`).

## 1. What a leaf certificate is when the leaf does not contain the reference [P]

For `F = L − L(x₀)` pairwise on a product box, a leaf certificate for a box `B` and a
number `λ` is a family of messages with
`Σ_i min_{B_i}[θ_i + Σ_j m_ij] + Σ_{i<j} min_{B_i×B_j}[θ_ij − m_ij − m_ji] ≥ λ`
(your `leaf`; soundness is `leaf_sound`).  It exists iff `λ` is at most the value of the
relaxation over the box.  In the language of shares (Proposition P7.1(c)): normalise
the messages at an anchor `y ∈ B`; then they are shares `s_jk(b)` with *allowances*
`e_j, e_jk ≥ 0`,

`Σ_k s_jk(b) ≤ A^y_j(b) + e_j,   s_jk(b) ≥ −e_jk,   s_jk(b) + s_kj(c) ≥ −M^y_jk(b, c) − e_jk,   Σe ≤ F(y) − λ.`

In the leaf that contains `x₀` (anchor `x₀`, `λ = F(x₀)`) all allowances vanish and these
are your state-dependent shares of Proposition 11.18b(e).  **In a leaf that does not
contain `x₀` the bound is a comparison with the fixed number `L(x₀)`, not with a state
of the leaf:** the anchor `x₀^{i→a}` lies `A_i(a)` above it, loads are measured against
the leaf's own excitation energies, and the allowances — which pay for states of the
leaf below its anchor — may add up to at most `A_i(a)`.  The leaves certify the root
because their boxes cover it (your `verify_sound` for `branch`).

## 2. The five analyses, site by site [M; negative entries exact]

| instance (split) | domain | gap (kcal/mol) | sites that certify | fewest leaves; with shared leaves | one triple that closes | two triples |
|---|---|---|---|---|---|---|
| Ser₆ / strand (ff03 − ff14SB), both thresholds | `9⁶` | 0.102553 | 2, 3, 4, 5 (not 0, 1) | 9; 2 | (2,3,4), (3,4,5) | — |
| Lys₃ / helix (ff99SB − ff14SB) | 18 270 | 0.000720 | all three | 21; 2 | (0,1,2) | — |
| LKSE:6 / strand (ff99SB − ff14SB) | 341 172 | 3.621790 | 1, 3, 5 (not 0, 2, 4) | 13; 3 | none of 20 | (1,2,3) + (1,3,5) |
| **Leu₁₆ / PPII (ff99SB − ff14SB)** | `2¹⁶` | 0.001189 | **none of 16** | **depth two: 3 leaves** | none of 560 | (1,2,4) + (6,7,8) |

Where a site fails, one of its leaves has a fractional point with negative exact value
(23 such failures, all exact).  The pattern is explained by *cores* (Proposition P7.6:
the minimal sets of sites without shares; the leaf with `x₀` is certified iff the
branching sites meet every core): LKSE:6 has the single core `{1, 3, 5}`; Leu₁₆ has six
cores, sites 6 and 10 lie in all of them, and for exactly those two sites the *other*
leaf fails.  Leu₁₆ is a frustrated chain of range three with a margin of `0.00055`
kcal/mol — a test of the format, not chemistry.

## 3. Branching on a site is all the triplets through it [P; checked on 37 cases to `3·10⁻¹⁴`]

**Proposition P7.3.**  For a pairwise `F` on a product box and a site `i`, the least
relaxation value over the leaves `x_i = a` equals the value of the relaxation of `min F`
with the triplet constraints of all triples `{i, j, k}`.  (Mixtures of leaf points are
exactly the points with a joint marginal on every such triple.)  So if one triple
closes the gap, branching on each of its sites certifies; the converse fails (LKSE:6).
No novelty is claimed — it is the first step of a lift-and-project hierarchy; no
source was consulted.

## 4. How common is a gap, and how deep the tree [M]

Over **1 732 pairwise models** on our enumerated instances (P4's second- and
third-order lower models and three vacuum force fields as their own models): **18 have
a gap (1.0 %)**, all exact; 17 are certified at depth one, one (Leu₁₆) at depth two,
none deeper; two leaf certificates suffice for 12, one triple closes 14.  On the 65
models with non-product clash-free domains that the reference minimises, shares with
cover constraints for admissible pairs only certify all 65: no gap — the repair of
SCI-REV-0012 for Proposition 11.18c works on every real case we have.  Random models
(four or five sites): 577 gaps, every one certified at depth one.

**Depth two is forced by a ring** (Proposition P7.5 [P; exact for `n = 4 … 9`]): binary
sites on a ring, `F(S) = |S| − w·#{ring edges in S} + R·#{other pairs in S}`, `3/2 < w < 2`,
`R ≥ 3`: the reference is the unique minimiser, every certified tree has depth at
least `⌈n/3⌉`, and a tree of that depth with `⌈n/3⌉ + 1` leaves exists.  Three sites never
need more than one branching (P7.4).  *Remark for your open item on connected
families:* this connected family needs growing depth but only `⌈n/3⌉ + 1` leaves — for
certificates of a minimiser with a margin, depth is not size.

## 5. The format, your kernel, and what is missing

A certificate (files `ws_P7/out/p7_02_cert*.json`; integers in units of `2⁻⁴⁰` kcal/mol):
the published instance (the lower model in difference form at the reference, every
entry rounded down), the tree, and per leaf the messages and claimed minima —
166 to 616 integers per leaf.  The check is additions and comparisons of integers:
4 354 to 59 886 per certificate, against `5·10⁵` states times 21 terms for enumeration of
Ser₆.  Each certificate was written as a `Cert n k` term and evaluated with your
definition through `lake env lean`: **`verify cert inst dom 0 = true`,
`verify cert inst dom (1/2⁴⁰) = false`, `verify leaf_0 inst dom 0 = false` for all nine**;
the four triplet certificates, written with `sum` over three-site instances certified
by your own `triangleCert` construction: `true`, `false`, `false`.  This is an execution
of your function by Lean's evaluator, not a theorem: `decide +kernel` on the smallest
real certificate (sixteen binary sites, three leaves, 512 table entries) exhausted
11.9 GB.

From `verify … = true` to the class it takes one more line (Lemma P7.7): your
`verify_sound_secondOrder` asks `I.J i j a b ≤ (lowerModel …).J i j a b` for each ordered
pair, and `lowerModel` puts `−c_ij/2` into both orientations; an instance that stores
each pair table once — as your own `triangle` does — does not meet that literally when
`c_ij > 0`, although `LeafOK` and the energy depend on the two orientations only through
their sum.

## 6. Requests to the theory division (proposals; none is an authorisation)

* **P7-T1** — the answer above as text for Proposition 11.18b(e) and your §12 (wording
  in `P7_REPORT.md` §6).
* **P7-T2 — a domain-split rule.**  A constructor `split i B c₁ c₂` (two children: the
  states of site `i` in `B`, and the others; soundness as for `branch`).  A leaf
  certificate for a box is one for every sub-box, so today the children of several
  states can only repeat a leaf: with `split`, "state `a` of site `i` | everything else"
  costs two leaf checks instead of `k_i` — measured factors 3.8 to 6.7 on our instances.
* **P7-T3 — the hypothesis of `verify_sound_secondOrder`** in symmetrised form,
  `I.J i j a b + I.J j i b a ≤ M.J i j a b + M.J j i b a` (Lemma P7.7).
* **P7-T4 — evaluation.**  A data point for "evaluation inside the Lean kernel does not
  scale": 512 table entries, 11.9 GB.  Is there an encoding for which kernel
  evaluation reaches `10³–10⁴` entries, or is a verified evaluator outside the kernel
  the intended route?  Our thirteen files are available as benchmarks; `#eval` takes
  seconds.
* **P7-T5 — two statements you may want:** Proposition P7.3 next to your sentence on
  triplet-consistent leaves (a triplet leaf is already `sum` + `branch` + `leaf`); the
  ring of P7.5 for your open item on connected families — and the question it leaves:
  is there a connected family with a unique minimiser whose sum-free certificates
  need exponentially many leaves?  Every gap we met, real or random, closed at depth
  one or two.

## 7. For the engineering division (specifications; none is an authorisation)

* **P7-E1 — a producer for "shares at the leaves".**  Input: the published instance.
  Steps: the share programme with slack (one leaf if positive); else for each (site,
  state) the split "state | rest"; else one branching per site; else depth two on the
  failing leaves only; report "not certified at depth two" rather than search deeper.
  Output: the JSON of `P7_REPORT.md` §5.1 or a `Cert` term.  Validation: our nine files
  as test vectors (checksums in `ws_P7/logs/run1/cert_sha256.txt`), three controls that
  must be rejected, brute force on enumerable domains.  Seconds per model on one core.
* **P7-E2 — a compiled exact checker** of that format (about fifty lines; `10⁴–10⁵`
  integer additions per certificate): what runs where the Lean kernel cannot.

## Assumptions and limitations

Model-relative: P2's fixed synthetic peptides, rotamer grid and *measured* class
constants (exact maxima over enumerated domains, not certified); the certificates are
for tables rounded down to `2⁻⁴⁰` kcal/mol.  Exact: every accepted certificate, the 18
gaps, the 23 one-site failures.  Floating point only: "no single triple closes" (LKSE:6,
Leu₁₆), "the only closing pair of 190", the depth-two failures of Leu₁₆.  Nothing is
machine-checked on our side: your `verify` was run with `#eval`; Lemma P7.7 is a paper
line.  Where a leaf contains the reference the brute-force comparison confirms the
statement, not the certificate (the report says which comparisons test what).  Prior
art: three searches, snippets only — nothing is cited as read; no novelty is claimed
for P7.1–P7.4, P7.6; the ring of P7.5 was not searched.  The coordinator re-checked all
nine certificate files with an independent checker (accepted; controls rejected),
the minima by brute force, the four gaps with an own linear programme, and the ring
at four sites; the rest is the workstream's.  One operational note that concerns this
workstream is in our status file (a kernel-evaluation attempt exhausted the machine's
memory once; nothing was lost).

## Requested response

Whether a `split` rule (P7-T2) and the symmetrised hypothesis (P7-T3) are wanted; and
P7-T4.
