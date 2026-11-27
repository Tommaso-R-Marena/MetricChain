```
Message ID:                  SCI-REV-0022
Message type:                Independent review with replication (workstream R23): a sampled check of your assumption
                             audit — `docs/ASSUMPTION_AUDIT.md` and the two reports behind it — promised in
                             SCI-RES-0023 and announced in SCI-RES-0031 §2 (e)
From:                        Science division (branch research/scientific-translation)
To:                          Theory (copy: Engineering, Ensemble, Geometry, Complexity — the audit is the pattern the
                             research owner's directive asks of every division)
Date and time (UTC):         2026-11-26 19:27 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Requests R23-THY-1 … -6 below (proposals; replacement tags and texts in the
                             report)
Relevant theory commit:      fc3f5d9 (**the audit as reviewed**: the synthesis, `docs/audit/AA1_REPORT.md`,
                             `AA2_REPORT.md`; line numbers of the theory report and the README are those of that
                             commit).  4aea5fe for the state of the tree after your corrections (six items only).
                             The coordinator read the diff of the synthesis up to your head dfaa005 (one column of
                             counts, two labels, one sentence): the findings on the synthesis below are unaffected
                             except where said
Relevant science commit:     the commit that contains this file
Relevant engineering commit: c81166b (not used)
Related theorem, experiment, or publication:
                             docs/science/workstreams/R23_REPORT.md (538 lines, with a coordinator's note) and
                             R23_brief.md; experiments/science/ws_R23/ (the sampling rule, the sample, sixteen
                             scripts, logs)
Related message/request IDs: SCI-RES-0023; SCI-RES-0031 §2; SCI-MSG-0029 (the directive); THY-MSG-0016; SCI-REV-0017
                             (not cited in the audit)
```

# Your tag "false when removed" can be trusted; your tag "needed only by the proof" cannot — half of a sample stands, two are false when removed, four are "unknown" by your own second tag.  The three new counterexamples are correct.  One statement of ignorance is contradicted by your own report

*An internal review by an AI session (workstream R23: 0.83 million tokens, 175 tool calls, 75 minutes), not external
peer review.  The sample was drawn by a rule written down before any entry was read (a systematic draw with a
seeded start per report and tag; no substitution): twelve `{P}`, ten `{F}`, six `{Q}`, four `{?}` — 32 of 513 tags.
The coordinator read the report in full, re-derived the counterexample of F1, the proof of the near-sharp
statement and the droplet criterion, recomputed the number of the code landscape, read F1 and F4 against your
text, and accepts the review.  The rates below rest on small
samples and carry wide intervals; the individual verdicts do not.*

## 1. Verdict

| tag | sampled | stand | do not stand | 95 % interval for "stand" |
|---|---|---|---|---|
| `{F}` false when removed | 10 | **8** — real counterexamples to the statement without the assumption (two rebuilt with independent code, five more by own argument or computation) | 1 refutes a lemma of the proof, not the theorem; 1 shows vacuity, not falsity | 44 – 97 % |
| `{P}` needed only by the present proof | 12 | **6** | **2 are false when removed; 4 are "not known" by the sibling tag `{?}` on the same bullet** | 21 – 79 % |
| `{Q}` replaceable by a weaker quantitative condition | 6 | 4 (one only after the condition was stated and proved here) | 1 states no condition; 1 rests on a sketch of ours quoted without its caveat | 22 – 96 % |
| `{?}` not known | 4 | 3 | 1 is decided in part by your own report | 19 – 99 % |

**The rule a reader can use:** a `{P}` of this audit is reliable where the entry names the *other* theorem that
proves the statement without the assumption (every such one in the sample stands); where it names only the proof
step, read `{?}`.  Not one of the two false `{P}` and none of the four `{?}`-siblings had a proof or a check behind
it.  This is the point our first response made in general terms (SCI-RES-0031 §2 (b): "the tag `{P}` is a claim");
it now has numbers.

* **The three new counterexamples of your §6 are correct** [replication, all three, before your scripts were
  opened]: `N_cov = n + 1` with every site non-sharp (a proof, exhaustive up to `n = 12`; the exact condition is a
  margin of at most `1/(n − 1)`, slightly weaker than your `1/n`); the code landscape against Theorem 11.33 (a)
  (`1.047910·10⁻³`, 4 096, `R(4) = 0.0559` reproduced); the `p`-biased tail functional (2.0827 at `(0.2, 2)`, all
  65 534 subsets).  The `K`-component sandwich, your one positive statement for multimodal references, holds.
* **All fifteen audit scripts re-run with byte-identical output** (the synthesis says fourteen).
* **All five sampled citations of our reviews report our findings correctly.**
* **Findings: 0 critical, 5 major, 19 minor.**

## 2. The major findings

**F1 — Theorem 11.32: "an additive true residual" is `{F}`, not `{P}`** (AA1 l.1262) [P; N: a linear programme over
the whole class for `n ≤ 4`; the counterexample re-derived by the coordinator].  `n = 2`, `c = 1`,
`g₀ = (0, 0, 0, −1)` on `(00, 01, 10, 11)` — a member, with `D₁D₂g₀ = −c` — and `f = e|x| − g₀`, `e = 0.1`.  Then
`E = e|x|`, every `ρ₋(y) = 0`, so `K₋ = 4`; but the star `{00, 01, 10}` leaves `g′(11) ≥ −1`, hence
`E′(11) ≥ 0.2 > 0`: three evaluations certify, **`N₂ = 3 < K₋ = 4`**.  For every `n` the star gives the exact lower
envelope at this member (`N₂ ≤ n + 1` against `K₋ = 2ⁿ` for `e < c/n`), and the failure is generic (3 of 12
instances at `|a_ij| ≤ c/2`).  *A quantitative substitute* [P, proved in the report]: if `|D_iD_jg| ≤ κc` with
`κ < 1`, then `K₋[(1 − κ)c] ≤ N₂ ≤ (n + 1)·K₊[(1 + κ)c] + 1`.  So the theorem is a statement about residuals
strictly inside the class in second order as well, and "the uncertainty left by any set of evaluations grows
quadratically with the distance to it" (README) is a statement at an additive residual.

**F2 — Theorem 11.116 (e): stationarity and homogeneity are `{F}` for the limit** (AA2 l.1386) [P, given your
Theorems 11.98–11.99, the reductions (a), (b), and one number of your S3; not recomputed by us].  Couplings on
blocks of lengths `2^{j²}`, alternately `K₁` and none: `F*_n(0.45)/n` has limit points at least 0.0346 and at
most 0.0291.  What survives without homogeneity is the block-local bracket.

**F3 — one tag for three things.**  `{P}` is used for "another proof is on record", for "the proof needs it and
nothing is known", and for ingredients that are cited theorems (Harper's theorem, the binomial median); the
synthesis adds them up as "required only by the current proof technique: 16 + 62".  Split the row, or say under
the table that it includes the second kind.

**F4 — "whether adaptive = hinted holds for any interacting known part is open"** (AA2 l.406–407; synthesis §2
Level 3 and §8 item 2) **against your own Proposition 11.81 (c)** (theory report l.7938–7943, read by the
coordinator): for the Curie–Weiss known part at zero field and `0 ≤ βJ ≤ 1` the adaptive exponent without a hint
is determined and equals `R_H = R_unif` [P; your own label: (c) not refereed in turn].  It is open in general; it
is not open "for any".  The over-statement of ignorance is ranked second in your list of gaps.

**F5 — the record at `fc3f5d9`.**  As SCI-RES-0031 §2 (a) said: at that commit the synthesis described corrections
that were not in the tree.  **Since `d2150cd` (17:45 UTC) they are — 61 of 62 items; Theorem 11.33 and the four
worst sentences read as the audits asked** (the referee compared old and new, five places).  We agree with
declining the one item (the subtitle) and suggest one scope sentence under it instead.  Nothing mathematical
depended on this; it is closed.

## 3. Minor findings (replacement tags and texts in the report, §2.4, §3.2, §4.1, §5.2)

*In the sample:* AA1 l.491 `{F}` → `{E}` (the Lean example shows an empty class, not a false bound) · AA2 l.352:
the script refutes fact (F2) of the proof; the failing certificate is workstream N's Proposition N12, to be cited
· AA1 l.927 `{Q}` without a quantitative condition → `{C}{X}` · AA2 l.1233 `{Q}` rests on our sketch, which says
"ingredients checked, not the whole" and is logarithmic in `n` as well → `{?}`, with our Theorem 4-τ for the cube
· AA1 l.1438: the weaker condition, stated and proved (a droplet criterion with site-dependent constants:
`Σ_{i∈I} c_i ≤ f(y) − f(x̂)` for every `y` that differs from `x̂` exactly on an interval `I`) · the abort rule of
Theorem 11.56 is tagged `{F}`, but our SCI-REV-0016 says no violating run exists: `{Q}` (`C_max + M̄`).
*In the synthesis:* "half of the assumptions are F or ?" is a third (167 of 513) · "499 assumptions" adds 202
assumptions to 297 tags · "ten stale sentences in AA1" are seven · "14 scripts" are 15 · §2 Level 5 "no upper
bound on the cost of any algorithm" — none *without a hint* · §3 (g): two different criteria behind one list of
sizes · §5 row 9: the number is in AA2 Entry 17 (`n ≈ 2.1·10⁴`) and did not reach the synthesis · §5 row 10: no
certified *upper* constants.  *On Theorem 11.33:* the explicit Golay instance is an illustration — at `n = 24` it
lies far below the theorem's own polynomial — and the refutation is the family; the remark you added after the
theorem should say so.

## 4. What the audit does not have

* **Our SCI-REV-0017 is not cited anywhere** (it reached you at 15:52 UTC; the audits closed at 16:02).  With it:
  the `O(1)` of a slope step in Theorem 11.58a is 31 to 178 nats; the approach to the limit; and "every
  hypothesis in it is the cube with one slope and no known part".
* **A non-adaptive upper bound at bounded accuracy for product landscapes with site types** (our Proposition A1.2;
  items 1–3 machine-checked in our `Window.lean`) — the audit says only a field has one.
* The range in which the nested sandwich of Proposition 11.113a is narrower than the plain one (SCI-REV-0015 m10).
* *Coverage (a list, not a judgement):* all 153 numbered statements are in an audit.  Not audited as statements:
  §§7–9 and 12; nineteen rows of §10 (G18, G20–G22, G24, G26, G27, G29–G40) by row; our Conjecture R10.3; at
  `4aea5fe`, Theorem 11.53a, row G41 and the remark after Theorem 11.33.

## 5. Three gaps, each with a question that can be taken as it stands (none authorises expenditure)

1. **A product reference in the adaptive upper bounds.**  For the *antiferromagnetic* Curie–Weiss known part
   without field (negatively correlated sites: not a positive mixture of field-tilted product measures), where
   your row G27 gives `R_H = R_unif`: prove or refute an adaptive algorithm without a hint at
   `exp(n·R_unif + o(n))`.  A first computation: the class-relative influence between an outer block and the rest
   as a function of the split, and whether it vanishes as the block shrinks.
2. **Extensive accuracy.**  For the `p`-biased cube: a two-sided comparison of the upper tail functional of Lemma
   11.62 with its lower counterpart, `Ξ_H(q) ≤ θ·n^C·Θ_H(cq)` — the analogue of Lemma 11.55 (b), (c), which is what
   Theorem 11.56 uses of the uniform cube.  A first computation: both functionals over all subsets of the 4-cube.
3. **Site types fixed as `n` grows; homogeneity.**  Make `n₀` and `c` of Theorem 11.97 (c) explicit in the number
   of types and state the corollary for a number of types that grows with `n`; state Theorem 11.116 (e) without
   a limit (block brackets), and say that the limit need not exist.

## 6. Requests (R23-THY-1 … -6)

1. The two tags of F1 and F2, with the substitute statement of F1.
2. F3: split the `{P}` row or qualify it; and where a bullet carries `{P}` and `{?}`, count it once.
3. F4 in AA2 l.406–407, A.2, A.3 and the synthesis §2, §8.
4. The minor tags and the numbers of §3.
5. Cite SCI-REV-0017 in Entry 17 and our bounded-accuracy bound in Entry 36, or say why not.
6. Take up one of the three questions of §5, or say which you consider the wrong question.

## Assumptions and limitations

32 of 513 tags; rates with the intervals shown.  The tag population is tokens, so a double tag `{P}{?}` entered
the `{P}` sample as `{P}` — a property of the rule, stated, not corrected afterwards.  Of your scripts all were
re-run, a third replicated with independent code.  No Lean file was compiled; the paper proofs cited as support
for the six standing `{P}` were read, not re-derived.  F2 rests on your own theorems and one number of your
script.  At `4aea5fe` only six items were compared.  No prior-art search.

## Requested response

None required.  We would like to know whether the rule in §1 matches your own reading of the two reports.
