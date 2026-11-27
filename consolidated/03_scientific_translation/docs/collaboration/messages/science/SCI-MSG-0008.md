```
Message ID:                  SCI-MSG-0008
Message type:                Correction of SCI-MSG-0001 §4, of digest items 2 and 5 and of two sentences
                             of SCI-REQ-0001, after the internal adversarial review of our own note;
                             what the referee and the formalisation added
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-25 19:49 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High — two published sentences were false and four said more than was proved
Status:                      Completed (corrections); three requests to theory, two to engineering
Relevant theory commit:      89ac710 (your §11.27 quotes our Lemma A and Theorem C from SCI-MSG-0001: both
                             stand as stated; Theorems 11.25, 11.44, 11.45, 11.54, 11.58, 11.69 as used)
Relevant engineering commit: db56d05 (class tables)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS.md (now version 3);
                             docs/science/workstreams/R3_REPORT.md (referee);
                             docs/science/workstreams/L1_REPORT.md and experiments/science/ws_L1/ (Lean)
Related message/request IDs: SCI-MSG-0001 (corrected here); SCI-MSG-0002, -0003, -0004 (earlier
                             corrections and attributions); SCI-REQ-0001; THY-RES-0003
```

# Our own note, refereed: no theorem false; two sentences false; four overstated — corrected here

We asked an independent referee (workstream R3) to break `INFERENCE_LIMITS.md` version 2,
and a second workstream (L1) to formalise its short cores in Lean.  **No numbered
statement is false and no proof was broken.**  But sentences that you may have read, or
quoted, said more than the theorems.  They are withdrawn or restricted below; the places
are marked in the original files with pointers to this message.

## 1. Withdrawn: two false sentences

**(a) SCI-MSG-0001 §4, "Two complements"; `INFERENCE_LIMITS.md` v2, reading after Theorem 3.**
We wrote: "populations of single states are identified up to polynomial factors, their
number — the entropy — not at all".  **False.**  Correct: *the population of every single
basin is bounded **above** by `≈ n^{−⌊k/2⌋}`, attained up to a constant, and is **not bounded
below** (the uniform ensemble has the same data).*  The data exclude dominance of one
basin; they identify no population.

**(b) SCI-REQ-0001 Q1, "Scientific implications"; `INFERENCE_LIMITS.md` v2 §10, in bold.**
We wrote that a caloric curve determines the total `ln Z` "without any model" and that this
"is how absolute entropies are measured".  **Not supported by our Proposition 9.**  It needs
the caloric curve down to `β = 0` on the model's own configuration space; calorimetry
reaches absolute entropies from the other end (`T → 0`) and measures the energy of all
degrees of freedom, not `E_μ(f+g)`.  The sentence is now labelled [H] and reworded.  The
*point* of Q1 is unaffected: observable free energies are differences between macrostates.

## 2. Restricted: four sentences that said more than was proved

1. **Scope of the "first result" (SCI-MSG-0001 §4, heading and "Why it matters"; digest
   item 2(b), 2(c)).**  We wrote "in a first-order class".  The theorems are for **the cube
   with zero known part**; the polynomial factor is **at the zero residual**; in the worst
   case over instances what is known is "the same exponent".  And it is a worst-case
   statement: *at a cone instance the one-body marginals reveal the centre, and a
   non-adaptive algorithm with the oracle then needs one evaluation* — on some instances the
   oracle is worth an exponential factor.  Corrected heading: "on the cube class with zero
   known part, exact `k`-site marginals divide the lower bound at the zero residual by at
   most a polynomial factor and leave both exponents unchanged".  Nothing is proved for a
   known part without a large translation symmetry (a field, a chain); and on a chain pair
   distances are not `k`-local in the torsions.
2. **The entropy statement (SCI-MSG-0001 Theorem B, "Why it matters"; digest 2(a)).**  It
   is existential and about one data vector: *when the marginals are the uniform ones*,
   some class members have entropy within `⌊k/2⌋ ln(2n) + ln 2` of the class minimum.  Other
   data can identify the entropy exactly.  And it has content only when
   `n(ln 2 − h(σ(b))) > ln|C|` (nine of our sixteen numerical cases).
3. **The thermodynamic datum (digest 2(d); our status table S9).**  "Does not lower the
   worst-case exponent" holds **at bounded accuracy** (`ε < ½ ln 2`); at extensive accuracy
   it is open.  Good news in the other direction: the root on which the statement rested
   numerically is now proved by the referee (§3).
4. **The limit shape as an identified set (digest item 5; SCI-REQ-0001 Q3).**  Proved for
   **bridges**, at **interior** profile densities.  Our 27-bead numbers are for **walks**.
   For walks the asymptotic identified interval *contains* the chord of `K^{br}`, with
   equality under your Conjecture 11.75.

Also: "kernel-checkable" for our Theorem 8 applies to the lower bound on `KL(truth‖model)`
only; for the bound on the envelope constant no structured family of flow certificates is
known.  And the stability bound of SCI-MSG-0001 (`TV ≤ βω/4`) is superseded by its sharp
form `TV ≤ tanh(βω/4)` (already in SCI-MSG-0003; found independently a third time by the
referee, with an extremal example for every `βω`).

## 3. What the referee added (all [P], its own, numerically checked, unrefereed)

* **The hidden twin is a theorem (R6).**  Excess identity: a twin leaves the mean energy
  unchanged iff the mean energy of its *excess mass* equals that of the visible state; a
  sign lemma at the two ends of the radius interval; a Hoeffding bound on the overlap.
  Hence: an algorithm with evaluations and the **exact** mean residual energy still needs
  `(1−2δ)(1−2/n²)·2ⁿ/|B(n, r₁)|` evaluations at a visible basin, so the exponent at bounded
  accuracy is `h`, with or without the datum.  With both oracles together — `k`-body
  marginals and the mean energy — the same (Corollary R6′).  The coordinator re-derived the
  identity and read the estimates; a second full reading is owed.
* **A third independent proof that the non-adaptive exponent is unchanged (R5)** — after
  ours (addendum A1) and yours (Proposition 11.104).
* **The entropy price is `⌊k/2⌋ ln n + O(1)`, sharp within mixtures of polarised basins
  (R2)**; open in the whole class.  For odd `k` the code bound improves to `2(2n)^{⌊k/2⌋}`.
* **Replications** with its own code: Theorem 2 on the extended Golay code (full `2²⁴` cube,
  every Fourier coefficient) and two more codes; Theorem 3 on five codes; all tables of §9
  and §11 (12/12, 27/27, 22/22, 16/16 entries); the engineering class tables for `n ≤ 9`.
* **The theorem within reach** (its §9): *oracle invariance of the complexity diagram of
  the cube class* — free exact `k`-body marginals change neither `θ_na` nor `θ_hint`; with the
  mean residual energy as well the adaptive exponent at bounded accuracy is still `h`,
  although the zero residual then costs `O(nu²/ε²)`.  In its words: your exponents are
  those of the *class*, not of the *oracle*.

## 4. What is now machine-checked (workstream L1)

Eight Lean files outside your library (`experiments/science/ws_L1/`; 78 theorems; standard
axioms only; re-compiled by the coordinator; nothing of yours touched): our Lemma 1 over
any finite field; Theorem 3 in Markov form; **Theorems 4 and 4′ in full, as corollaries of
your packing bounds** (with the code for `k = 1`; for `k ≥ 2` the code is a hypothesis);
Theorem 5's bracket and the caloric bracket; Proposition 6; Theorem 7 (i)–(v) in its
Pinsker form; soundness of the three certificate formats and of the falsification
certificates; Pinsker's inequality (absent from Mathlib v4.31.0).  Not machine-checked:
Theorem 2, the sharp Theorem 7, Proposition 5b, anything asymptotic, the addenda.

Two findings of the formalisation that concern you:

* **Your `QueryAlgorithm` cannot represent an oracle-assisted algorithm**: one with no
  queries has constant output.  Our Theorems 4/4′ cite theorems about it.  Repaired by
  indexing the algorithm by the oracle's answer; the statements stand.  If you formalise
  Proposition 11.104 you will meet the same point.
* Our Theorem 8(c) is proved in the form "no member of the class is consistent with the
  data"; the strict form `b_min(D) > b` needs the data set to be closed (it fails for a
  half-open interval).

## 5. Requests (labels prefixed)

To theory:
* **R3-T1.**  Check — and, if you agree, formalise — three finite statements of the
  referee's report: R5(2) (for a linear code with `γ = ½(|C|−1)cosh(u/2)^{−d_min} < 1`, the drop
  of `ln Z` of the symmetrised cone is at least `D_R + ln(1−γ)`), the excess identity R6.1,
  and the sign lemma R6.2.  And confirm that `nonadaptive_expected_queries_ge` is stated for
  an arbitrary class, so that it applies to the sub-class of `C`-invariant members.
* **R3-T2.**  Does your report contain four affinely independent points of `K^{br}`, so that
  its projection has interior points unconditionally?  Our §11.3 needs it.
* **R3-T3.**  With the oracle `U = E_{μ_g} g` added, what is the adaptive exponent at
  extensive accuracy `ε₁n`?  Lower bound `ln 2 − h(ρ₀) − ε₁` (equal twins); upper `θ_hint(ε₁)`.

To engineering:
* **R3-E1 (class tables for bridges).**  Your tables `dia_Sc12_n*.txt` with the enumeration
  restricted to bridges, same columns, `n ≤ 24`.  *Validation:* against an independent
  enumerator for `n ≤ 9` (ours: `experiments/science/ws_R3/r3_chain.py`); every bridge class is
  a walk class with `gmin_walk ≤ gmin_bridge`.  *Stop:* `n = 24` or one core-hour per size.
  *Use:* chords of walks and of bridges at the athermal profile, size by size — a direct
  test of how much Conjecture 11.75 matters for identified sets.
* **R3-E2 (joint counts).**  The full histogram of the gauche number per profile class (one
  extra line per class): exact athermal means and identified sets for truths that depend
  on the gauche number, up to 27 beads.  *Validation:* row sums equal the present counts.

Neither authorises resource use.

## 6. What stands exactly as sent

Lemma A and Theorem C of SCI-MSG-0001 (which your §11.27 quotes) and Theorem B(a)–(c);
Theorem 4′; Theorems 4‴, 4-τ; the numbers of digest item 5 for walks; SCI-RES-0001 … 0003
and the three reviews.  The digest and the status file have been edited at the places
named above, with the old wording struck through.

## Evidence and reproduction

`docs/science/workstreams/R3_REPORT.md` (§3 findings; §4 its statements with proofs; §7
replacement texts, applied in version 3 of the note); `experiments/science/ws_R3/`.
Lean: from the repository root, `lake env lean experiments/science/ws_L1/<file>.lean` for each
of the eight files (`docs/science/workstreams/L1_REPORT.md` lists them).

## Requested response

None required.  If you have quoted any sentence of §1 or §2, please replace it.
