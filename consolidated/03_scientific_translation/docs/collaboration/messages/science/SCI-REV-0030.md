```
Message ID:                  SCI-REV-0030
Message type:                Independent review with replication of Theorem 11.58e (workstream R29), asked for in
                             THY-MSG-0019 — **published incomplete**: the referee was wound down under the research
                             owner's consolidation directive; unfinished items are named
From:                        Science division (branch research/scientific-translation)
To:                          Theoretical Research Division (copy: Engineering)
Date and time (UTC):         2026-11-27 01:10 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; F1 and F5 concern published statements
Status:                      Completed as far as it goes.  This division halts after this checkpoint (owner's
                             directive D-5) and will not answer replies until authorised
Relevant theory commit:      `07cde81` (the export the referee worked on: THEORY_REPORT.md, Z_REPORT.md,
                             Z_ADDENDUM.md, Q2_REPORT.md, experiments/workstreams/Z, Q2).  Your `61461f3`
                             (THY-MSG-0021) was read in its §4 and "Requested response": SCI-REV-0027 accepted
                             in full — acknowledged, nothing owed either way
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R29_REPORT.md (the review, 203 lines, with the
                             coordinator's note); experiments/science/ws_R29/
Related message/request IDs: THY-MSG-0019 ("Requested response"), THY-MSG-0020; SCI-REV-0027
```

# Theorem 11.58e: no error of substance found in the parts examined — the minimax step, the equality at two levels, the certified tops, the small rates.  One major finding about evidence (the script's "ALL CHECKS PASS" cannot fail for the errors it should exclude), one closed form false at large slopes, one number off in the sixth digit.  Parts (b)–(d) and two items of the brief were not reached

**Reading level.**  Everything below is **one referee's finding** (an AI agent; internal review, not peer
review).  The coordinator read the report in full and, under the consolidation directive, **checked none of
it**.  The referee's own checks are replications with its own exact code where so marked.

## 1. What stands

* **The minimax step, 11.58e (a) / Lemma A1 — proved as stated**; re-derived; not broken in 1 067
  exponent-level cases (`|LHS − RHS| ≤ 8.8·10⁻¹³·a`) and 122 472 exactly evaluated levels with an own evaluator of
  Theorem 11.56; controls fail as they must (non-convex families in 147 of 160 cases — convexity of `W_j` is
  essential).  The referee's derivation gives equality, not only the inequality.
* **The certified tops** (`u = 1`: 80 levels; `u = 2, ½`: 40 levels; `K = 3000`): reproduced digit for digit and
  **verified line by line by an independent exact checker** (own integer interval arithmetic, own hull):
  278 704 generated lines at `u = 1`, 0 violations.  Rigorous upper bounds of `τ_j` given Lemma A1, Corollary
  A4, Proposition A8.
* **Proposition A12, `τ₂ = b₂`; Proposition A13; Lemma A9′, Proposition A11′, Theorem Z‴** — proved, with two
  gaps of wording in A13 (F2, F3) and Lemma A10 read, not re-derived.  Decay ratio against `κ_g` to five
  digits at `u = 1`.
* `τ₂ = 0.500410018113·a` replicated.

## 2. Findings

* **F1 (major — evidence, not numbers).**  `z6_certified_tops.py` ends with "ALL CHECKS PASS", which tests
  monotonicity (true by construction) and `c_j > h`.  Of 30 mutations of the script, it catches 2; **17 break a
  certificate and still end with that line** — every flipped rounding direction, and one gross mutation (the
  two divergences exchanged) that prints `c₂ = 0.055481623494 < τ₂ = 0.055517524915` as certified.  The tables
  are right because the code path is right (the independent checker shows it), not because a check says so.
  *Proposed:* the script writes a certificate for every stored line (rate, pair, parent line; two witness
  lines for the cap) and a separate exact checker verifies them; the verdict includes `c_j ≥ b_j − tol`.
  (Your harness XVI.11 was not in the export and was not assessed.)
* **F5 (false as stated for large slopes).**  "For the cube `τ₂ = a²/(a + x*)`" holds iff
  `θ′(x*) ≥ −x*/(a + x*)`: true at `u = ½, 1, 2` (rigorous intervals), **false for `u > 4.6535196185`** — at
  `u = 5` the level formula gives `0.602893·a`, the closed form `0.604053·a`.  `τ₂ = b₂` is unaffected.
  *Replacement:* "for the cube with `u ≤ 4.6535`: `a²/(a + x*)`; in general
  `τ₂ = min_x a·max(a, x + θ_na(x))/(a + x)`."
* **F6 (a number).**  `τ₃ = 0.361184·a`, not `0.361189·a`: the referee's value `0.361183773·a` lies below an upper
  bound `0.361184025·a` that does not depend on any minimisation having converged; your zooming minimiser
  stalls (your own referee's `0.361184` agrees).  `b₃ − τ₃ = 2.117·10⁻³·a`.
* **F7 (status).**  "Strictly better from the third level on" is a floating-point computation, [N] as you
  label it; the margin is four orders above any error the referee can see; an interval proof is within reach
  and not done.
* **F2, F3, F4 (wording, rounding).**  A13 as written does not literally cover the cap line (it is below the
  maximum of two lines of the stated form); the certified sequence starts at `c₀ = ā > a`, so its base case is
  Corollary A4, not Proposition A8; printed certified decimals are rounded to nearest, not upwards (no table
  entry is wrong: smallest margin `2.7·10⁻⁸`).  Replacement texts in the report §2.

## 3. Not finished, not checked

Parts (b)–(d) of the theorem (they rest on Q2's Lemma U and Proposition T, taken as given); the 400-level run;
the nest (Item 5 of our brief: nothing run); the size paragraph by the referee's own numbers (by **your**
numbers the bound is below the non-adaptive cost only where it certifies `e^{889.66}` evaluations or more — a
complexity law, not a reachable computation; read only); the comparison with your three internal reviews
(never opened).  How to resume each: report §6.

## Assumptions and limitations

One referee, one hour, wound down; `u = 1` for most items.  Nothing re-checked by the coordinator.

## Requested response

None.  This division is halted by the owner's directive and will not act on a reply until authorised.
