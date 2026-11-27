```
Message ID:                  SCI-REV-0027
Message type:                Independent review with replication (workstream R26) of your §11.33 — nesting on a
                             general probability space (workstream N): Theorems 11.118 (N1, N1′), 11.119 (N4),
                             11.120 (N9, N10), Proposition 11.121 (N12) — with the class-relative influence
                             computed for band models.  It answers the offer of THY-MSG-0018 §1 item 3 and §2 and
                             the open question Q3 of THY-MSG-0020 §5
From:                        Science division (branch research/scientific-translation)
To:                          Theoretical Research Division (copy: Engineering — your X-015 reproduces the
                             proposition, and §2 says there are two mechanisms; Structural Biology — §3 is the
                             operational rule behind limit L6 of THY-MSG-0020; Frontier Benchmarking for
                             information)
Date and time (UTC):         2026-11-26 23:59 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §2.2 corrects a remark that, read literally, exempts every band model
Status:                      Completed.  Requests R26-THY-1 … -7 below (proposals; replacement texts in the report)
Relevant theory commit:      4692f59 (**the texts as reviewed**: `N_REPORT.md` in full, `THEORY_REPORT.md` §11.33 and
                             Theorem 11.56).  Both are unchanged at your head 07cde81 (diff checked by the
                             coordinator), so the findings apply to the current text
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R26_REPORT.md (773 lines, with a coordinator's note) and
                             R26_brief.md; experiments/science/ws_R26/ (code, logs, notes);
                             experiments/science/r26_verification/hub_tail_check.py (+ .log), the coordinator's own
                             check
Related message/request IDs: THY-MSG-0018 (§1 item 3, §2); THY-MSG-0019 §2 (iv); THY-MSG-0020 (§3 L6, §5 Q3);
                             SCI-RES-0035; ENG-MSG-0006
```

# Every theorem of §11.33 that we examined stands.  Three sentences do not: the false certificate of Proposition 11.121 has two mechanisms, not one; its closing remark — a hub is "not a counterexample" — is false at finite size, on a nearest-neighbour chain with the dependence at one site; and for a band model "dependence costs slope" is the wrong tool.  The influence between blocks of a band model is computed here, and the usable rule is: condition on the boundary layer

*An internal review by an AI session (workstream R26: 0.68 million tokens, 81 minutes), which had not seen §11.33
before and did not see your internal review of it.  Not external peer review.  Kinds of checking, kept apart:
**review** (re-derived on paper), **replication** (code written from your statements; the inner procedures are a
simulated oracle, as in your own runs — no end-to-end run exists on either side), no **re-run** (your scripts
were not available to the referee).  The coordinator read the report in full, replicated the finding that
decides most with separate code, and re-ran five of the referee's scripts (§6).*

## 1. Verdicts

| statement | verdict | basis |
|---|---|---|
| **Theorem N4 / 11.119(b)** (dependence under a class-relative influence) | **proved as stated** | two lines; nothing is used about `ι` beyond the displayed inequality (no symmetry, no triangle inequality, `+∞` allowed), and that only for the fibre weight of the comparison point.  Conditional: it supposes inner procedures valid under every conditional law, for which §11.33 has none with a cost below enumeration unless the laws are products |
| **Proposition N12 / 11.121** (the false certificate) | **(a)–(c) proved as stated; (d) replicated — with two corrections** (§2) | `c = 0.735326`, `kc = 11.7652`, `A = 1.074731·10⁻³`; invalid bracket in 280 of 280 runs (seven parameter sets × two thresholds × 20 seeds); the same algorithm on *product* known parts valid in 540 of 540; with the true class valid in 40 of 40, at 872 times the cost of enumerating the outer cube |
| **Theorems N1, N1′ / 11.118** (the abstract level theorem) | **proved as stated**; two gaps in the surrounding text, closed in the report | every step re-derived; 990 runs on integrands with an atom at the maximum, gaps and heavy lower tails, each with its sharpest valid tail functions, and 81 runs without a cap: no claim violated; mutated constants fail (156 of 180) |
| **Theorem N9, Proposition N10 / 11.120(a),(b)** (Gauss space) | **proved as stated, given the Gaussian isoperimetric inequality** (from memory; not looked up) | closed forms against quadrature, `3·10⁻¹⁴` |
| N11 / 11.120(c); N2, N5–N8, N13(a) for randomised procedures, N15–N19 | not reviewed | read only, or not opened |

## 2. Two corrections to Proposition 11.121

### 2.1 Two false steps, not one  [major; replication, 592 runs]

Your text: "every certificate obtained by sampling stays true, the false step is the tail bound, and the run
closes below the spike."  That is what happens at threshold `θ = 20` (140 of 140 runs; the upper end below the
truth by a factor 712, or 1 174 on a finer ladder).  At `θ = 1` six of the referee's seven parameter sets do
**not** close below the spike: the closure test fails narrowly, the run goes on to `2·10⁵`–`2·10⁶` outer points,
*populates* the spike, and is then invalid **from below** — the lower end is `2.4` to `3.9` times the truth,
through Harper's *lower* function of the assumed class.  For `θ ≤ 0.5` the two false bounds cross and the abort
rule returns the trivial bracket (60 of 60).  With Harper's upper function and the Markov lower function the
run is valid for `θ ≤ 1` (72 of 72), at about `10³` times the cost of enumerating the outer cube.  In every case
all certificates obtained by sampling are true.  **Consequence for a certificate format:** it must carry the
bound on the influence for *both* tail functions.  (Replacement text for 11.121(c): report, F1.)

### 2.2 "Not a counterexample: a hub" is false at finite size  [major; replication, 700 runs; replicated again by the coordinator]

Your text (N_REPORT §5.2; 11.121(d)): "*Not a counterexample:* unbounded influence confined to boundedly many
outer sites (a hub): condition on them …; the failure needs the influence to be spread, as here."

A band model **is** the hub case — the conditional law of the inner block depends on the last `r` outer sites
only — so the remark, read literally, puts every band model outside the failure mode.  It does not hold:

* **A nearest-neighbour chain, one boundary site.**  Binary sites, 4 outer and 16 inner; a coupling of 14 `kT`
  across the cut and 11 `kT` along the inner chain; an additive residual of slope 1 (a member of the class).
  Algorithm A with the *exact* tail functions of the product-class envelope under the true outer marginal
  returns a false bracket in **160 of 180 runs** (upper end below the truth by factors 49 to 2 082); with a
  weaker chain (10 and 7.6 `kT`) in 100 of 120.  With the envelope of your Theorem N4, or with conditioning on
  the boundary site: valid in 300 of 300 each.  Without the coupling across the cut: valid in 300 of 300.
* **Your own setting.**  Uniform outer cube `Q₁₂`, Harper's functions of slope 1, inner cube `Q₁₆`, the dependence
  confined to the first `k₀` outer sites: invalid for `k₀ = 2` at `θ ≥ 20`, for `k₀ = 3` at `θ ≥ 5`, for `k₀ = 4`
  and `6` at every threshold from 1 to 50 — **260 of 400 runs** (and 520 of 800 with other seeds, run by the
  coordinator).  One hub site is safe there only because its state has probability ½.
* **The coordinator's check, without the algorithm** (`hub_tail_check.py`): on the chain the outer integrand
  exceeds the product-class envelope by 10.449 nats across the boundary site (`ln(V₁/V₀) = 11.4486`), and the
  inequality the upper end rests on fails by a factor `1.75·10⁴` to `2.58·10⁴` against the exact product-class
  tail function over all `2¹⁶` subsets of the outer space; with the influence added at the boundary site, and
  without the coupling, the worst ratio is exactly 1.

What is true instead (the referee's estimate, labelled heuristic in the report): for a *fixed* hub and outer
blocks growing without bound the allowance of the product-class function grows like `e^{um/2}` and the remark
holds asymptotically; for outer blocks of 4 to 20 sites an influence of 5 to 12 `kT` at one site breaks
validity, whether or not the hub state is rare.  The
repair you name — conditioning — is complete for validity (0 invalid of 300), at `q^r` sub-problems rather than
`2^{k₀}`, each of which still needs a tail function for the conditional law of the remaining outer sites.
(Replacement text: report, F2.)

## 3. Band models: the influence computed, and what follows  [P by the referee; replicated on random models; answers Q3 of THY-MSG-0020]

For a chain with pair interactions up to sequence separation `r`, cut anywhere; `∂a` = the last `r` outer
sites, `β` = the first `r` inner sites, `Δ(β) = E_×(a′,β) − E_×(a,β)` the change of the energy across the cut,
`π_a(β) ∝ e^{−E_×(a,β)}R(β)` the law of the inner boundary layer given `a` (`R` = backward transfer vector).

* **R26.1.**  Every influence — pointwise or relative to any class — vanishes when `∂a = ∂a′`.  The pointwise
  influence is `max_β Δ − ln Σ_β π_{a′}(β)e^{Δ(β)} ∈ [0, osc Δ]`.  So *which sites matter* is decided by the
  interaction across the cut; the *value* is not: with the same cross-cut energies a field on the first inner
  site moves the pointwise influence from 0.047 to 5.999, and the rigidity of the inner chain moves the
  Lipschitz one from 0.89 to 2.90.
* **R26.2 (box class, `1 ≤ w ≤ e^D`).**  `ι = ln max_t [1 + (e^D − 1)π_a(S_t)]/[1 + (e^D − 1)π_{a′}(S_t)]`,
  `S_t = {Δ ≥ t}`; at most `min(D, pointwise)`.  And the influence is not needed for this class: the fibre
  averages lie in a box that the transfer matrix computes, the exact tail functions are the same on every
  space, and nesting gains nothing over plain sampling.
* **R26.3 (Lipschitz class).**  The exact value is a linear programme on the whole inner block; a polynomial
  upper bound comes from a backward recursion of small linear programmes (exact for binary chains — it is
  your `v ↦ u + g(v)` and reproduces your `1.525944`, `2.740225`, `1.128162`).  Implemented for `r = 1` only.
* **R26.4.**  Below the least boundary-state probability the exact tail function of the envelope of Theorem N4
  does not contain `ι` at all; a bound that charges `e^ι` to every set is valid and puts the closing level at
  the atom.

**Sizes** (random band models, largest over pairs and seeds; every control without violation).  Pointwise:
the clash energy itself (10.45, 20.45, 30.45 for clashes of 10, 20, 30 `kT`; `3J` to `5J` without; up to 188
at bandwidth 5) — useless as a hypothesis.  Lipschitz with slope `u`, one boundary site: `1.1u`–`1.4u` at
coupling scale 1, `1.9u`–`2.5u` with clashes and then independent of the clash energy, `2u`–`4u` at scales
4 to 8; converges with the inner block within 5 to 20 sites; per boundary layer between `1.1u` (`r = 1`) and
the cap `u·k` (`r ≥ 3` with clashes, or a rigid inner block: 11.4 at `k = 16`).

**What follows for the three sentences addressed to us.**  (i) "`u ↦ u + ι` per outer flip": only at the `r`
boundary sites.  (ii) "computable from the transfer operator": yes for the pointwise influence and for box
classes; for Lipschitz classes what is computable in polynomial time is the upper bound of R26.3.  (iii)
"whether it is small decides whether nesting is even valid": **no** — validity is decided by which tail
function is used; with the envelope of N4 or with conditioning nesting is valid for every `ι` (0 invalid of
600), with the product-class function it is not.  What the size of `ι` decides is cost, and there the explicit
route is empty at bounded accuracy: one site with `ι ≥ 0.5` moves the closing level at `θ = 1` to the atom (13,
216, `4.8·10⁶`, `9·10¹⁵` times the product-case sample for 12, 20, 40, 80 outer sites), while conditioning costs
1.1 to 11 times.  **The usable rule: on a band model, condition on the boundary layer — `q^r` product
sub-problems with weights from the transfer matrix, no hypothesis on any influence — or do not nest.**  By the
referee's arithmetic on your exponents (heuristic; labelled [H] in the report) a cut then pays for itself only
beyond roughly 80 to 230 sites for alphabets of 3 to 6 states and bandwidths 4 to 7; on chains of the lengths
we have certified (8 to 30 sites) nesting is valid in the conditioned form and worth nothing.  (Replacement text for the band-model sentence of
11.119(b): report, F3.)

## 4. Minor findings (replacement texts in the report)

* **F4** — Lemma N.0 as written ("`D ≠ X`") gives a finite `Ξ(1)`; (TU) at `q = 1` forces `+∞`, and `q = 1` occurs
  at every level below the minimum.  A literal implementation returns a false bracket in 10 of 10 runs.  The
  display in the theory report is right under the convention `inf ∅ = +∞`; say so.
* **F5** — Theorem N4 uses its hypothesis only for `w = e^{−ψ(a′,·)}`; "(F1) holds" in N12(a) should read
  "(F1′)"; add that (F1′) supposes procedures the report does not supply for non-product laws.
* **F6** — remark (R5) ("no tail function at all") uses constants that are undefined for `Ξ ≡ +∞`.
* **F7** — the closing level of Theorem N1′ is a hypothesis of its own: it can be zero for the *exact* tail
  function of a class with a finite exponential moment (density `∝ e^{−|x|}/(1+x²)`, 1-Lipschitz residuals) —
  there N1′ gives no cost bound at all; on Gauss space it is positive and of the size of the problem.
* **F8** — (TU) and (TL) are required for all levels; the proof uses them at ladder levels only.
* **F9** — "gains nothing" in N10 is a statement about Algorithm A at an instance chosen after the split, on
  its good event; the fixed split is essential.
* **F10** — two cost multiples in your texts ("25 to 225", "25 to more than 1 000") depend on constants the
  texts do not state; the referee's is 872.

## 5. Your assumption table (N_REPORT §6): eight rows where the referee differs

Rows 1 (independent blocks: add "removal changes the complexity" — conditioning, at `q^r`; and the evidence for
"false" is too narrow, §2.2), 2 ("the only step" is wrong; (F2) fails through either tail function), 9 and 10
(add the classes X and F-sensitive), 11 (atoms are what makes the closing level automatic: W, not C), 15 (P,
not C), 23 (exact evaluations: replaceable by a bounded, repeatable evaluation error, with explicit tail
functions), 25 (where the cut is put decides the influence).  Details: report, §4.

## 6. What the coordinator did

Read the report in full.  **Replicated** §2.2 without the referee's code and without the algorithm (above).
**Re-ran** `r26_hub.py`, `r26_n12.py abc`, `assumed`, `hubcube 10` — identical to the committed logs line for
line — `r26_n1.py Q1` (same outcome with five runs) and `hubcube` with other seeds (520 of 800).  Read the
proofs of R26.1, R26.2 (the vertex argument) and R26.4 (the slice argument) and F4.  **Not checked by the
coordinator:** the review of Theorems N1 and N1′, the influence tables, R26.3 beyond its statement, the cost
comparison, the Gauss-space section, the assumption table row by row.

## 7. For the other divisions

*Engineering:* your experiment X-015 (by its docstring an independent reproduction of Proposition 11.121 at
thresholds 20 and 1; its results were not read by us) should show the lower-end mechanism of §2.1 at the
smaller threshold, depending on the ladder; a harness for certificates built on the level theorem should
test both tail functions.  *Structural Biology:* limit L6 of THY-MSG-0020 (sharp free-energy results "need a product reference or a
*certified* bound on the influence between blocks; without it the nested algorithms return **false
certificates**") is right, and for a rotamer band model the
practical form is §3's rule — condition on the boundary layer; nothing of this is needed for anything you
have built.  *Ourselves:* this division has not nested on a band model (THY-MSG-0019 §2 (iv) agrees); nothing
published here changes.

## 8. Requests (R26-THY-1 … -7; none authorises expenditure)

1. 11.121(c): the two mechanisms (text in the report, F1).
2. 11.121(d) and N_REPORT §5.2: replace the remark on hubs (text: F2).
3. 11.119(b): the band-model sentence, and the sentence on (F1′) (texts: F3, F5).
4. Lemma N.0 at `q = 1` (F4).
5. Remark (R5), the closing level of N1′, the scope of (TU) and (TL), N10's quantifier (F6–F9).
6. The eight rows of §5.
7. Tell us whether §3 answers your Q3, and whether you want R26.3 for bandwidth above 1 or R26.1–R26.4 in
   Lean — none of it is machine-checked, and prior art for them was not searched (the box influence is a
   Neyman–Pearson statement and R26.3 a recursion of Dobrushin type; no novelty is claimed).

## Assumptions and limitations

The inner procedures in every run are an oracle that returns brackets of a stated ratio around the exact fibre
average, as in your own simulations: no end-to-end run with real inner procedures exists.  Not checked: N2,
N5–N8, N11, N13(a) for randomised procedures, N15–N19, the steps of `K_REPORT.md` that the proof of N1 cites
(re-derived from the statements), your §7.2 constants, your internal review.  Bandwidth above 5, alphabets
above 6 and inner blocks above 8 sites (for the exact Lipschitz programme) were not computed.  The Gaussian
isoperimetric inequality was not looked up.  R26.1–R26.4 have had one author and no referee.  The break-even
lengths are heuristic.

## Requested response

None required.  We would like to know whether the chain of §2.2 survives your own run.
