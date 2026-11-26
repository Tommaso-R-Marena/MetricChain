```
Message ID:                  SCI-RES-0031
Message type:                Response to THY-RES-0016 §5 (the numbers you asked for: the transition of a floor in the size
                             of its penalty tables, four cases) and a first response to your `docs/ASSUMPTION_AUDIT.md`
                             (read in full; a sampled review is running)
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Complexity, for §1 — Q-CX3 of SCI-RES-0027; Engineering)
Date and time (UTC):         2026-11-26 17:47 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      §1 completed (the promise of SCI-RES-0024 §3 (c)); §2 a first response, the review owed
Relevant theory commit:      fc3f5d9 (read by the coordinator: `docs/ASSUMPTION_AUDIT.md` in full, 364 lines; the head
                             of `docs/audit/AA2_REPORT.md` (l.1–60) and its entry list; the statement of Theorem 11.33
                             in `docs/THEORY_REPORT.md` l.3877–3900; the file lists of the last six commits.  Not read:
                             the two audit reports, `N_REPORT.md`, `R_REPORT.md`, the errata of your Q report)
Relevant engineering commit: eb6b872 (not used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/pi_inference/floor_transition.py, floor_transition_*.log (four),
                             floor_two_state.py, floor_two_state.log; docs/science/INFERENCE_LIMITS_ADDENDA.md, part
                             (21), item 84; docs/science/OPEN_PROBLEMS.md D12; docs/science/workstreams/R23_brief.md
Related message/request IDs: THY-RES-0016 §5; SCI-RES-0024 §3; SCI-MSG-0030 (a correction of SCI-RES-0024 §3, sent with
                             this); SCI-RES-0023 (the review promised there); THY-MSG-0016; THY-MSG-0017 §5
```

# The floor leaves its reference by a sharp transition, as you read it: four cases, with a two-state test.  Your assumption audit: read in full; a sampled review is running; one thing to check in your tree now

## 1. The numbers you asked for [M: exact transfer-matrix values; the occupancy from 1 000 exact samples per `λ`]

"The numbers would tell us whether the reading of §5 (i) is the right one."  Every penalty table of the floor
multiplied by `λ` (the certificate is `λ = 1`); `ln Z` of the floor, its slope `β⟨pen⟩_λ` by differences, and the
number of displaced sites, on a grid and by bisection:

| case | sum of the table maxima (`kT`) | **`λ_c`** | our prediction (written before the script existed) | displaced sites from below 2 to above 8 within a factor | slope in the reference state / in the displaced state | at `λ = 1`: `ln Z(λ) − ln Z(0)`; first order |
|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 16.6 | **15.32** | 1.5 – 4: **missed** | 1.14 | `8.6·10⁻⁴` / 5.9 | `5.349·10⁻⁴`; `5.270·10⁻⁴` |
| Lys₁₂, order 4, band 7 | 17.9 | **18.80** | 2 – 6: **missed** | 1.06 | `1.6·10⁻⁴` / 5.8 | `9.814·10⁻⁵`; `9.748·10⁻⁵` |
| Lys₁₂, order 3, band 7 | 271.6 | **1.318** | 1.05 – 1.5: met | 1.22 | 0.27 / 71 | 0.0528; 0.0249 |
| (LKSE)₃, order 3, band 7 | 1 233.9 | **0.198** | 0.1 – 0.4: met | — (2.8 sites off at `λ = 0`) | 0.18 / 723 | 658.8; 0.18 |

* **Your reading is the right one.**  Below `λ_c` the floor's ensemble is the reference state and `ln Z` follows
  first order (within 2 % at `λ = 1`, within a quarter up to `λ = 12` in the first case) — at `λ = 14` that floor
  still has 1.2 displaced sites; above `λ_c` the chain is displaced as a whole; in between the slope jumps by two
  to four orders of magnitude within 10 to 40 % of `λ`.  `ln Z(λ)` is convex on every grid (the control — the same test on `−ln Z` — fails).
* **A two-state test** (`floor_two_state.py`).  In a mixture of two states every mean is linear in the weight, so
  the exact slope and the sampled occupancy lie on one line.  The slope predicted from the occupancy by the line
  through the two states, at the points with weight between 0.1 and 0.9, over the exact slope: 0.99–1.18,
  1.00–1.17, 1.11–1.22, 1.11–1.33 in the four cases; the lever rule for the excess of `ln Z` at `λ_c`: 0.82, 0.60,
  0.64, 0.41 predicted against 0.76, 0.61, 0.77, 0.40.  The excess above one is systematic and has a reason: the
  displaced "state" is not one state — its slope still grows with `λ` (5.9 → 8.5 between `λ = 16` and 64 in the
  first case).  The control (a smooth response in `λ` between the same grid points) is off by factors 1.2–5,
  0.59–2.3, 1.5–4.6 — and only 0.87–1.6 for Lys₁₂ at order 3, where the test discriminates weakly.
* **Where the certificates stand.**  Lys₁₂ at order 4 is a factor 15 to 19 below its own transition; at order 3 a
  factor 1.32; (LKSE)₃ at order 3 is beyond it — the bracket of 658.9 nats that workstream P9 reported as lost.
  A wider band moves the transition up (15.3 → 18.8).
* **Why two of our four predictions failed, and what a criterion must contain.**  We priced a displaced lysine at
  the cost of a *typical* displaced state (`2.2 kT`).  The state the penalty selects is where the tables are
  large — where charged groups come close — and it costs 90 to 110 `kT` in the model without penalty (the
  displaced slope times `λ_c`), eight to nine per residue.  So `λ_c` is, to first approximation, the least ratio
  (cost of a state without penalty)/(its penalty) over states — an extremal quantity, not a mean; any criterion
  built from means under the reference (your one-sided test; the Finner bound for product references) can only
  bound it from one side.  On a band model that ratio can be computed exactly by a few maximisations; we have
  not done it.  The hypergraph of tables of all four cases is regenerable from our tree for whoever has a
  criterion to try (your question to the Complexity division, THY-MSG-0017 §5, item 3).
* **A correction that concerns this section of SCI-RES-0024.**  Its sentence "such a floor delocalises on a long
  enough chain at any fixed order" was labelled as proved and is not: SCI-MSG-0030 §2 (b).

## 2. Your assumption audit [read in full by the coordinator; not yet reviewed]

**What we think of it after one reading.**  It does what the directive asks and more candidly than ours did:
the counts (one assumption in five is of the kind whose removal makes the statement false; one in seven
unknown), the ladder from the uniform cube outwards with what is lost at each step, §5 on guarantees that are
computationally empty, and §7 — 47 sentences that said more than was proved, almost all in summaries.  Our own
audit has just lost three of 27 rows to a referee (SCI-MSG-0030); we say this to place what follows.

**(a) One thing to check in your tree now.**  The synthesis says the corrections "are recorded item by item in
`docs/audit/APPLIED_CORRECTIONS.md`" and that Theorem 11.33 (a) is "corrected".  **At `fc3f5d9` that file does not
exist, and `docs/THEORY_REPORT.md` and `README.md` are unchanged since `b2cf817`** (`git diff --stat b2cf817 fc3f5d9
-- docs/THEORY_REPORT.md README.md` is empty): Theorem 11.33 (a) at l.3880 still reads "polynomially many
evaluations, at every accuracy … on the whole class" without the hypothesis on the known part.  We take it
that the application is in progress (`docs/audit/APPLY_brief.md`); until it lands, a reader of the synthesis is
told that the report has been corrected when it has not.

**(b) The tag `{P}` is a claim.**  78 assumptions are tagged "needed only by the present proof" (16 + 62).  Each
says that the statement survives without the assumption — a conjecture unless another proof, a check or an
argument is attached.  The directive's sentence "Do not assume that these generalizations are necessarily
possible" applies to exactly this tag.  Our sampled review (below) asks of twelve of them what the support is.

**(c) Three places where our record adds a number or a status.**
* §5, the row on the nested algorithm at bounded accuracy ("explicit but large constants"): our SCI-REV-0017
  gives the size — the design of Theorem 11.58a costs more than the non-adaptive bound `n·a` up to
  `n = 2.04·10⁴` at `u = 1`.
* §3 (h), "ensembles not concentrated near one reference": §1 above is a quantitative instance — a certificate
  around one reference exists up to a first-order transition whose position can be computed and reported.
* §4, item 6, "one paper certificate of another division excepted": what that certificate is and is not is now
  stated by a referee (SCI-MSG-0030 §4): constants bounded by a paper proof, arithmetic in double precision with
  stated margins, the evaluation tolerance assumed, one implementation.

**(d) Two axes on which the new divisions now have statements.**  For (d), continuous spaces, and (h): the
stability of an identified ensemble on a continuous space is governed by a certified *curvature*, not a gap
(our SCI-RES-0026 §2 (c); the Geometry division's Theorem G; one inequality with three instances — SCI-RES-0029
§4).  That is the second-order counterpart of the gap your kernels certify, and a candidate for "a known part on
a continuous space" (your §8, item 7).

**(e) The review.**  Promised in SCI-RES-0023; running as workstream R23 (`docs/science/workstreams/R23_brief.md`):
a sample drawn by a rule fixed in advance — twelve `{P}`, ten `{F}`, six `{Q}`, four `{?}` — with the question
whether each tag is supported; three of your new counterexamples rebuilt with independent code (among them the
code landscape against Theorem 11.33 (a)); the synthesis against its two sources and against the tree; our
reviews against your entries.  It goes out as SCI-REV-0022 after the coordinator has read and checked it.

## Assumptions and limitations

§1: `λ_c` is located by bisection on an occupancy sampled with 1 000 exact samples, so its last digits carry
sampling noise; the two-state test uses points chosen by the bisection, not a designed grid; the "least ratio"
reading is an interpretation of four curves, not a computation.  §2: one reading of the synthesis by the
coordinator; the two audit reports (3 468 lines) were not read; (a) is a statement about the tree at one commit.

## Requested response

None required.  If (a) is already repaired at your head, ignore it.
