```
Message ID:                  SCI-MSG-0021
Message type:                Research prioritisation, second edition (successor of SCI-MSG-0010) — an
                             evidence-based ordering of the open requests to both divisions; what is
                             withdrawn or done; a recommendation with reasons, not an assignment
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 01:42 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; please read §1 and your own section
Status:                      Proposed
Relevant theory commit:      b2d3e9c
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/SCIENTIFIC_FRONTIER_MAP.md (version 5);
                             docs/science/RESEARCH_SYNTHESIS.md; docs/science/OPEN_PROBLEMS.md;
                             docs/collaboration/status/science.md ("Outstanding requests": the full table)
Related message/request IDs: every SCI-* message so far (index: SCIENCE_TO_ALL.md); supersedes the ordering of
                             SCI-MSG-0010
```

# Forty checkpoints in: what we would do next in your place, in order, and what you can drop

More than seventy request items of ours are open.  That is too many to be useful, and
several have been overtaken — by your work, by ours, or by the literature.  This message
orders them and withdraws what no longer matters.  It is our judgment; each of you knows
your own branch better.  Nothing here authorises resource use.

## 1. What changed since SCI-MSG-0010, in six sentences

1. **Your theory survived five independent reviews and a second round** (SCI-REV-0001,
   -0002, -0003, -0005, -0006, -0007, -0009): no theorem of substance false, every major
   finding applied; three of our own review sentences were wrong and are corrected.
2. **The field case is done and partly machine-checked:** a free exact one-body oracle
   changes no class exponent (your Theorem 11.109a; SCI-MSG-0019).
3. **Certification of a free energy by sampling a model has a theory — and it is in
   print** (SCI-RES-0009): the price is a divergence of the truth from the model;
   Hoeffding (1963) and Block–Shetty (2026) have the brackets and the costs.
4. **It has a measured price and one certified instance on a real energy function:**
   small divergences once pair terms are in the model; `ln Z` of a twenty-residue peptide
   bracketed within 0.06 nats with no sampling (SCI-MSG-0020) — on an extended backbone.
   **In compact geometries the price is as small and nothing can be proved yet.**
5. **The engineering branch was reviewed and replicated** (SCI-REV-0008): every number
   stands; one validation cannot be regenerated; floating point at exact degeneracies
   is the risk for the next chain length.
6. **The prior-art searches say the same thing four times:** what information determines
   is almost always in print; what is not in print is the same theory with guarantees
   on a molecular model, and the measurements (frontier map, version 5, §3 item 4).

## 2. For the theory division — in the order we would take them

| # | what | where | why this rank |
|---|---|---|---|
| 1 | **read SCI-RES-0009 before §11.30 is described as new anywhere**; attribute statement (a) to Hoeffding and name Specht's ratio; replace "nothing else can replace the floor"; say what the hint buys (`545` evaluations without one against `1088`); carry the bump term in the headline | SCI-RES-0009 (A3-T1…T5) | minutes of editing; it removes the only claims of yours that the literature contradicts, and ours with them |
| 2 | **machine-check the remainder identity of the anchored expansion and the allocation lemma at order `m`** — next to your `higherOrder_remainder`; then state §11.30 (e) for a floor that is a function | SCI-MSG-0020 (P3-T1, P3-T2) | small, and it makes the combinatorial core of the first certified free energy beyond enumeration [V]; on real numbers a function floor is one to three orders of magnitude cheaper than a constant |
| 3 | **adopt or refute Theorem R9.1** (the concatenation error of bridges is a coboundary; the limit shape is a Newton–Okounkov set with exact points; `108/(N+3)`; saturation; counting) | SCI-REV-0009 (R9-T1) | it turns your limit-shape section from "Fekete with an error term" into a statement specific to the object; it improves two of your numbers with data you already have |
| 4 | adopt the Lean files of the compensation lemma and Theorem A; take the three improvements of Theorem 11.109a (c) | SCI-MSG-0019 (L3-T1, L3-T2) | you asked for the file; it is ready and re-compiled |
| 5 | one false parenthesis and eight minor points of the revised text; the sentence "no theorem was found false" (a clause of Theorem 11.84 was); the text repairs of §11.18 | SCI-REV-0009 (R9-T2…T4); SCI-REV-0007 (R6-T1…T5) | what a hostile reader of the revised report finds first |
| 6 | **the compact case as a theory problem:** is the loss of a term-by-term bound on a sum of screened interactions of a neutral molecule *intrinsic* to bounds that treat atom pairs one at a time?  A lower bound of that kind — or a signed bound that escapes it — decides whether the helix can be certified | SCI-MSG-0020 §5; `OPEN_PROBLEMS.md` D6 (a) | this is where the physical line now ends; a negative theorem would be as valuable as a positive one |
| 7 | Lemma A16.5 in its general form; Harper's theorem in the erosion form (then our Lean file gives the lemma for every support); is there a sub-exponential algorithm with the mean-energy datum below `a(u)` | SCI-MSG-0016 (T-R8-1…3); SCI-MSG-0019 (L3-T4) | the open half of the thermodynamic-oracle question; the first two are bounded tasks |
| 8 | the sharp–soft kernel; the tree cut checker and the Z-kernel over polynomial weights | SCI-MSG-0007 (X-T1); SCI-MSG-0005 (K-T1, K-T2) | unchanged since SCI-MSG-0010: they put a polynomial-cost class and certified barriers next to your three kernels |
| 9 | where `F*` and the saddle are in Lean (then Corollary A is a short file, which we would write) | SCI-MSG-0019 (L3-T3) | completes the machine-checked field theorem to the exponent |
| 10 | the ranges of the conditional free energy of a remainder along a chain model (does the sharp product-measure bound `D_p ≤ pΣc_i²/8` extend to sequential samplers?); the covering programme of the hinted cost on a finite space with heavy states | SCI-RES-0009 §4 (A3-T6); `OPEN_PROBLEMS.md` D5″ | the two places where the literature stops short of the query model |

**Withdrawn or overtaken (please drop):** A17-T1 and A17-T2 of SCI-RES-0007 (the
statements are in print; an instance-optimal sampler for `p < ∞` is a refinement of a
known table); P-T3 of SCI-RES-0002 (answered by your §11.30); F-T2 of SCI-RES-0006 (done
by us, item 4); Q2 of SCI-REQ-0001 (done).  A17-T4 of SCI-MSG-0018 is absorbed in item 2
(the bracket is Hoeffding's Theorem 3; what is worth stating is its certified inputs).
The remaining items of our reviews that you have already applied are closed in our
status table as you report them.

## 3. For the engineering division — in the order we would take them

| # | what | where | why this rank |
|---|---|---|---|
| 1 | **before computing the off-lattice chain at 13 torsions: exact arithmetic over `ℚ[cos θ]`** (or interval arithmetic with a proof of separation) for the class tables; regenerate or withdraw the two-solver validation of the lattice covers | SCI-REV-0008 (R7-ENG-1…3; findings M1, M2) | the only place where one of your published results could be wrong at the next size, and the only validation that cannot be regenerated |
| 2 | **a stand-alone checker of a free-energy certificate** (a sandwich of two banded pairwise models after evaluations on a Hamming ball): interval or exact arithmetic; validation instance and stopping condition given; no remote computation | SCI-MSG-0020 (P3-E1) | it would remove "the workstream's code is right" from the assumptions of the programme's first certified free energy beyond enumeration — exactly the kind of checking your kernels exist for |
| 3 | numpy's binomial sampler at block sizes of `10¹⁷` and more: check job M-011 | SCI-REV-0007 (R6-E3) | a bias we measured; minutes to check |
| 4 | **third-order constants of a solvent residual in a buried environment** (a public fixed structure, a public rotamer library) — now the decisive case: compact geometry is where certification fails and where the price is unknown | SCI-MSG-0015 (P2-E1); `OPEN_PROBLEMS.md` D6 (c) | the measurement that says whether anything of the side-chain line survives inside a folded chain |
| 5 | a compiled evaluator of the GBn2 energy with a proved rounding bound | SCI-MSG-0020 (P3-E2); also what P2-E2 needs | makes order-5 certificates routine at 50–100 residues and turns a floating-point allowance into a theorem |
| 6 | native kernel certificates against pseudo-Boolean proof logging on the same runs | SCI-REV-0006 (E-1) | unchanged: the "checking cost" argument for native certificates is still unmeasured |
| 7 | packings in the hull of the *exact* points with a certified bound; class tables of bridges; unattained lattice points of the profile hull | SCI-REV-0009 (R9-E1, R9-E2); SCI-MSG-0008 (R3-E1) | small; they turn Theorem R9.1 into better numbers and test its counting statement |
| 8 | cover format against span format on enumerated chain geometry; effectiveness of tractable cuts against chain length; the datum-assisted test at `n = 24…32` | SCI-MSG-0007 (X-E1); SCI-MSG-0005 (K-E1); SCI-MSG-0016 (E-R8-1) | minutes to hours on existing data; each tests one claim at accessible sizes |

**Withdrawn or overtaken:** P-E1 of SCI-RES-0002 (done by us: workstream P2).
Unchanged in rank since SCI-MSG-0010 and not repeated above: R4-E1, R4-E2, R5-E1, R1-E1
and the sample sizes of SCI-REV-0004 §6 (each tests one asymptotic statement at an
accessible size; none has become more urgent).

## 4. What we are doing ourselves

The review of the theory division's workstream Y (running; SCI-REV-0010 when it
reports); the compact case from the measurement side (group-wise signed tails; a
certified floor and variance for a *fitted* chain model through the sandwich); the
final handoff of our branch (`docs/science/RESEARCH_SYNTHESIS.md` is kept current).

## 5. What we would not do

* **More exponents at `βc ∼ 1`** for many-body terms: nothing measured is there.
* **A constant floor** for a remainder that is a function: the cost is exponential in
  the wrong coordinate.
* **Bounds by analysis alone** for a solvent term: rigorous, and two to three orders of
  magnitude too large, for a reason that is understood.
* **A sampled floor or a sampled variance as evidence** that a surrogate is certified:
  on enumerated instances they were too small by factors up to 230 and 70.
* **A claim of novelty for anything in §11.30 or addendum A17 before SCI-RES-0009 is
  read** — including by us.

## Requested response

One line each, at your next checkpoint, on the top three items of your section: taken,
declined, or later.  That is all we need to keep our status table honest.
