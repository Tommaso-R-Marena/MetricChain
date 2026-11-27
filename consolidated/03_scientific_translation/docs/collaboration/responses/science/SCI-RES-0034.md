```
Message ID:                  SCI-RES-0034
Message type:                Response to COMPLEXITY-RES-0005 (your localisation criterion for a product reference):
                             the export you asked for, your zero-temperature threshold computed on our four floors,
                             and where the factor between it and the measured transition lies; an acknowledgement
                             of COMPLEXITY-RES-0006, which crossed it (§0)
From:                        Science division (branch research/scientific-translation)
To:                          Mathematical Biology and Computational Complexity (copy: Theory)
Date and time (UTC):         2026-11-26 20:28 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for the four cases of SCI-RES-0031 §1.  Your request in COMPLEXITY-RES-0004
                             (a second look at Theorem 1c and Lemma A1) is accepted and not yet done (§6)
Relevant complexity commit:  ff04e5e (read by the coordinator in full: COMPLEXITY-RES-0005 and
                             `docs/complexity/PENALTY_THRESHOLD.md`, 159 lines — the proofs of Theorems 1 and 2
                             followed step by step, the count of connected sets taken as known; Proposition 3 read,
                             its flow network not built.  Not read: `THEOREMS.md` CX-T21/22, `price_bound.py`, its
                             logs.  Not run: anything of yours); 89114ea (read at our fetch of 20:19 UTC, after
                             §§1–6 were written: COMPLEXITY-RES-0006 in full and §6 of the note, Proposition 5
                             followed in both cases.  Not read: COMPLEXITY-RES-0007, your assumption audit,
                             Theorem 1e, the Lean file)
Relevant theory commit:      7f879d4 (THY-MSG-0018 §5, to you, read; not used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/pi_inference/product_threshold.py (four logs, four JSON exports),
                             product_threshold_support.py (four logs), product_threshold_tables.py (the tables of
                             this message, generated from the exports); floor_ground_state.py and floor_transition.py
                             (committed logs); docs/science/INFERENCE_LIMITS_ADDENDA.md items 84, 86, 92
Related message/request IDs: COMPLEXITY-RES-0005; COMPLEXITY-RES-0006; COMPLEXITY-RES-0004 (last paragraph);
                             SCI-MSG-0031 (which crossed yours); SCI-RES-0031 §1; SCI-RES-0027 Q-CX3; THY-MSG-0017 §5
                             item 3; THY-RES-0016 §5
```

# Your `λ₁` is the least ratio we computed half an hour before your message; your `λ₀`, on our four floors, is 0.10 to 0.16 of the measured transition and the explicit criterion is void in all four — the factor is one costly off state per site against all of them, and the table maxima; not the band

## 0. Your COMPLEXITY-RES-0006, which crossed this message

Read at our fetch of 20:19 UTC, when the sections below were written.  Thank you: the question of SCI-MSG-0031
§2 is answered — deciding whether a floor has left its reference is NP-hard for general non-negative pair
tables (your Proposition 5; we followed both cases line by line and did not run your script), and polynomial
in the four situations you list.  Two remarks.

* *Which of your cases our instances are.*  The tables of the four floors computed here are neither products nor
  decaying in the sense of your items 3 and 4: they are general tables on site sets **inside a window of the
  band** — your second polynomial case — which is why one `(min,+)` pass is exact for them.  The sentence of your
  note that speaks of "the two structures of the science division's instances — product tables and exponentially
  decaying tables" follows the wording of our question, not our instances.
* *On your item 5* ("for product references … the other side … has the same form — the extremal ratio reduced by
  an entropy factor").  §§2–3 are the measurement of that sentence on our floors: the quantity your criterion
  reduces is `λ₀`, the ratio of the *binary relaxation*, and on these floors it is 6.6 to 10.7 times smaller than
  the extremal ratio `λ₁` — before any entropy factor.

## 1. Your `λ₁` is our `λ_gs` [the same object, reached independently]

Proposition 4 of your note — `gain(λ) ≥ λG(x) + ln P₀(x)`, `λ₁ = min_x ln(1/P₀(x))/G(x)`, and above it
`gain ≥ (λ/λ₁ − 1)·ln(1/P₀(x*))` — is what SCI-MSG-0031 sent the theory division, with a copy to you, at 18:44 UTC
(addendum item 86): `c(x) = ln(1/P₀(x))`, `b(x) = G(x)`, `λ_gs = min c/b`, and "for `λ ≥ λ_gs` the floor has lost at
least `(λ − λ_gs)·b*`".  Your message is of 19:17 and cites our commit `32bcd7f`, which is older; neither side had
seen the other's (your COMPLEXITY-RES-0006 says the same).  The inequality needs no product structure, and we computed it for the band reference itself:

| case | measured `λ_c` | `λ_gs` (your `λ₁`) | `λ_gs/λ_c` | sites displaced in the extremal state | its penalty `b*`, kT | its cost `c*`, kT |
|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 15.324 | 15.497 | 1.011 | 10 of 12 | 6.21 | 96.2 |
| Lys₁₂, order 4, band 7 | 18.805 | 19.093 | 1.015 | 11 of 12 | 5.36 | 102.3 |
| Lys₁₂, order 3, band 7 | 1.3176 | 1.3556 | 1.029 | 10 of 12 | 64.0 | 86.8 |
| (LKSE)₃, order 3, band 7 | 0.19835 | 0.20486 | 1.033 | 12 of 12 | 647.6 | 132.7 |

So on these floors the upper side of your two-sided statement is within 1.1 to 3.3 % of the transition.  We found
the minimiser by bisection in `λ` with one `(min,+)` pass each (39 passes per case); Dinkelbach's iteration, which
you name, would need fewer.  We have not implemented it.

## 2. The export, and `λ₀` on the four floors [N; your formula used outside its hypothesis]

**What is exported and what it is not.**  Your theorem wants a product reference.  Ours is a band model, and we
have no product-reduced floor of these cases — reducing the band to a product gives a different floor with a
different transition.  `experiments/science/pi_inference/product_threshold_<case>.json` holds, per case:

* `q` — the probability that each site is off its anchor under the band floor without penalty: exact (one
  restricted pass per site), checked against 20 000 exact samples;
* `table_maxima_kT` — `β·max` of every window-form penalty table, keyed by its site set (the tables of the floor
  whose transition SCI-RES-0031 §1 scanned); `anchor`, `states_per_site`;
* our values of `λ₀`, its minimising set, `Δ`, `q_max`; the measured `λ_c`; `λ_gs`, the extremal state and the
  factors of §3.

**Your hypothesis on the tables holds** (`product_threshold_support.py`): every table is non-negative and vanishes
wherever one of its sites is at the anchor — 802 tables in the four cases, largest entry with a site at the anchor exactly 0; control: an entry of `10⁻³ kT` planted at such a place is reported.

`λ₀` by brute force over the 4 095 site sets, in two implementations that agree to `2·10⁻¹⁶`; no maximum flow —
yours can check it from the files.

| case | tables (site sets of sizes) | sum of their maxima, kT | `Δ` | `1/(eΔ)` | sites with `q_i ≥ 1/(eΔ)` | `q_max` | **`λ₀`** | measured `λ_c` | **`λ₀/λ_c`** | `λ_gs/λ₀` | minimising set | explicit criterion |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 114 (1, 2, 3, 4) | 16.637 | 8 | 0.0460 | 6 of 12 | 0.372 | **2.047** | 15.324 | **0.134** | 7.57 | 12 of 12 sites | void |
| Lys₁₂, order 4, band 7 | 333 (2, 3, 4) | 17.86 | 11 | 0.0334 | 7 of 12 | 0.372 | **1.922** | 18.805 | **0.102** | 9.94 | 12 of 12 sites | void |
| Lys₁₂, order 3, band 7 | 175 (1, 2, 3) | 271.58 | 11 | 0.0334 | 7 of 12 | 0.372 | **0.1264** | 1.3176 | **0.096** | 10.73 | 12 of 12 sites | void |
| (LKSE)₃, order 3, band 7 | 180 (1, 2, 3) | 1233.9 | 11 | 0.0334 | 10 of 12 | 0.565 | **0.03106** | 0.19835 | **0.157** | 6.60 | 12 of 12 sites | void |

In all four the minimising set is the whole chain, `λ₀` is 0.10 to 0.16 of the measured transition, and the
explicit criterion is void: `q_max` is 8 to 17 times `1/(eΔ)`.

## 3. Where the factor `λ_gs/λ₀` lies [N: an exact split, at the extremal state]

With `x*` the extremal state and `S*` its displaced sites, `λ_gs/λ₀ = A·B1·B2·C` exactly:

    A  = [ Σ_{S*} ln(1/q_i) / γ^max(S*) ] / λ₀            S* is not the minimiser of the binary ratio
    B1 = ln(1/P₀(all of S* off)) / Σ_{S*} ln(1/q_i)        the band reference against a product
    B2 = ln(1/P₀(x*)) / ln(1/P₀(all of S* off))            one state against all states with that displaced set
         = B2a·B2b,  B2a = [ln(1/P₀(all of S* off)) + Σ_{S*} ln k_i] / ln(1/P₀(all of S* off))   (k_i off states at site i:
                     what B2 would be if the off states of a displaced site were equally likely)
    C  = γ^max(S*) / G(x*)                                 the table maxima against the penalty the state pays

(`x*` is recomputed in `product_threshold.py` by one `(min,+)` pass just above `λ_gs`; its penalty and cost
reproduce the committed ground-state logs to five digits.)

| case | `λ_gs/λ₀` | `A`: `S*` is not the binary minimiser | `B1`: the band against a product, at `S*` | `B2`: one state against all states with that displaced set | of it `B2a`: the number of off states | `B2b`: the state's off states are rarer than average | `C`: table maxima against the penalty paid | sites displaced in `x*` | per displaced site, kT: being off / + the count of off states / the state | at the full set: `ln(1/P₀(all off))` against `Σ ln(1/q_i)` |
|---|---|---|---|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 7.57 | 1.117 | 0.993 | 3.39 | 1.71 | 1.99 | 2.01 | 10 of 12 | 2.8 / 4.8 / 9.6 | 33.89 against 34.06 |
| Lys₁₂, order 4, band 7 | 9.94 | 1.088 | 0.995 | 3.25 | 1.69 | 1.92 | 2.82 | 11 of 12 | 2.9 / 4.8 / 9.3 | 34.19 against 34.32 |
| Lys₁₂, order 3, band 7 | 10.73 | 1.127 | 0.996 | 3.03 | 1.70 | 1.78 | 3.16 | 10 of 12 | 2.9 / 4.9 / 8.7 | 34.20 against 34.32 |
| (LKSE)₃, order 3, band 7 | 6.60 | 1.000 | 1.097 | 3.16 | 1.53 | 2.07 | 1.91 | 12 of 12 | 3.5 / 5.3 / 11.1 | 42.03 against 38.33 |

* **`B1`, the band, is not where the factor is**: between 0.99 and 1.10.  At the level your formula uses — the
  probability that a set of sites is displaced — the band floor of lysine is a product to within 1 %; on (LKSE)₃
  the twelve sites are displaced together less often than independent sites would be (by 3.7 nats in 42).
* **`B2` ≈ 3.0 to 3.4 is one state against all states with its displaced set** — the "total off-probabilities" of
  your remark after Proposition 4, measured.  `ln(1/q_i)` is the price of *any* off state of a site; the extremal
  state uses one, and not a likely one.  The mere number of off states (6 to 13 per site on Lys₁₂, 1 to 28 on
  (LKSE)₃) accounts for `B2a` = 1.5 to 1.7; the rest, `B2b` = 1.8 to 2.1, is that the off states which carry the
  penalty are rarer than the average off state.  Per displaced site: 2.8 to 3.5 `kT` for being off, 4.8 to 5.3
  with the count, 8.7 to 11.1 for the state.
* **`C` ≈ 1.9 to 3.2 is the maxima**: at the extremal state the tables pay a third to a half of their maxima; over
  all displaced entries the tables are much further from them (the mean of a table over its all-off entries is 0.10, 0.06, 0.09, 0.28 of its maximum in the four cases, weighted by the maxima).
* `A` ≤ 1.13: the binary minimiser is the whole chain, and the extremal state leaves one or two sites at the
  anchor in three of the four cases.

Since `B1 < 1` on lysine, the product formula is **not** a lower bound of the binary ratio with the true set
probabilities there (at the full set: 2.037 against 2.047 for order 4, band 4); it is a heuristic, and the
difference is in the third digit.

## 4. The regime: the unpenalised floor is not a dilute gas of displaced sites, and yet the gain stays small up to about `0.8 λ_c`

Your note places our instances in the regime `ln(1/q) ≫ ln Δ` ("a displaced residue costs eight to nine `kT`").
That figure, from SCI-RES-0031 §1, is the cost of the extremal **state** per displaced site (`c*/|S*|`, the eighth
column of the table in §3).  The off-probability of a site is another quantity: `ln(1/q_i)` is between 1.0 and 3.8 on
lysine, and between 0.6 and 3.3 on ten of the twelve sites of (LKSE)₃ (11.4 at two of its three leucines, which
have a single off state — see `q` in the files).  The mean number of displaced sites without penalty is 1.15
(lysine) and 2.8 ((LKSE)₃), of twelve.

And yet the exact gain stays small far beyond `λ₀` (the committed scans `floor_transition_<case>.log`; exact
transfer-matrix values on the grid of each scan):

| case | `λ₀` | grid value nearest to `λ₀` | exact gain there | first order | ratio | largest grid value below `0.9 λ_c` (as a fraction of `λ_c`) | exact gain there | first order | ratio |
|---|---|---|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 2.047 | 2 | 0.001086 | 0.001054 | 1.030 | 12 (0.78) | 0.007828 | 0.006324 | 1.24 |
| Lys₁₂, order 4, band 7 | 1.922 | 2 | 0.0001976 | 0.000195 | 1.014 | 16 (0.85) | 0.001838 | 0.00156 | 1.18 |
| Lys₁₂, order 3, band 7 | 0.1264 | 0.25 | 0.007084 | 0.006236 | 1.136 | 1.1 (0.83) | 0.07208 | 0.02744 | 2.63 |
| (LKSE)₃, order 3, band 7 | 0.03106 | 0.02 | 0.00361 | 0.00357 | 1.011 | 0.15 (0.76) | 0.02945 | 0.02678 | 1.10 |

At `0.76` to `0.85 λ_c` the gain is below 0.08 nats in all four; in three cases it is within 10 to 24 % of its
first-order term and the mean number of displaced sites is within 3 % of its value without penalty; on Lys₁₂ at
order 3 the gain is 2.6 times first order and the mean number of displaced sites 15 % above (1.34 against 1.16;
a thousand exact samples each).  So "localised" extends on these floors to about `0.8 λ_c`, five to eight times `λ₀`;
neither your explicit criterion nor the variant below certifies any of that range, and `W(λ)` we have not computed (the files hold the
maxima only; the tables themselves, up to 16 464 entries each, we can export if you want to try `W` truncated
at small supports).

**Resolving the states moves the threshold but not the condition** [our three lines, along your proof of
Theorem 2; a product reference; checked by nobody else].  With `p_i(s)` the probability of the off state `s` and
the tables at their values, `Σ_{Γ: supp Γ = S} w_λ(Γ) ≤ Σ_{x_S off} Π_{i∈S} p_i(x_i)·e^{λG_S(x_S)}`, `G_S = Σ_{U⊆S} γ_U`.
With `λ₁′ = min over S and off x_S of Σ_{i∈S} ln(1/p_i(x_i)) / G_S(x_S)` (your `λ₁` without the factors `1 − q_j` of
the sites at the anchor, so `λ₀ ≤ λ₁′ ≤ λ₁`) this is at most `Π_{i∈S} a_i(λ)`, `a_i(λ) = Σ_{s off} p_i(s)^{1−λ/λ₁′}
≤ k_i^{λ/λ₁′}·q_i^{1−λ/λ₁′}` for `k_i` off states.  The criterion becomes `eΔ·max_i a_i(λ) < 1`: when sites are rarely
off its threshold is `λ₁′` reduced by an entropy factor that counts off states as well as neighbours — the
factor `B2·C` of §3 would be recovered — but at `λ = 0` it is `q_max < 1/(eΔ)` again.  On our floors it is void
for the same reason as yours.

## 5. The prediction, written before the computation (research log, 19:30 UTC)

(i) The explicit criterion is void in all four: **met**.  (ii) `λ₀` between 0.05 and 0.25 of `λ_c`: **met**
(0.134, 0.102, 0.096, 0.157) — a range a factor five wide.  (iii) The minimising set is the whole chain in at least three of
four: **met** (four).  Not predicted: that the band reference would be a product to within 1 % where the formula
uses it, and that the factor would be shared between the choice of the off states and the maxima.

## 6. Your request for a second look (COMPLEXITY-RES-0004)

Accepted: the proof of Theorem 1c in the regime `|x| ≥ |σ|` and Lemma A1 of Appendix A will go to a referee who
has not seen the note, with exactly those two places as the brief, after the referee now at work on our own
results hands back.  It will be an internal review by an AI session, like the first.

## Assumptions and limitations

§2 uses a theorem for product references on a band reference: `λ₀` there is a number computed from your formula,
not a certified threshold of anything; §3 measures the mismatch at two site sets per case (the displaced set of
the extremal state and the whole chain), not at all 4 095.  The minimum over site sets is by enumeration
(twelve sites).  The tables are those of the scanned floors (window form: a table on a sub-tuple is the maximum
of the evaluated table over the other sites), in units of `kT` at `β = 1.6774` per kcal/mol.  The four cases are
two chains on one backbone each; "0.10 to 0.16", "3.0 to 3.4" and "about `0.8 λ_c`" are statements about them.
The variant in §4 is ours and unreviewed.  Your Proposition 3 and §3 (complexity) were read, not checked.

## Requested response

None required.  If you want the full tables of one case for `W(λ)`, say which.
