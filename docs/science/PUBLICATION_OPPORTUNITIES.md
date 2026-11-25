# Publication-level assessment

*Science division.  Version 1 (2026-11-25).  An assessment for the research owner of which
results in the three branches are mature, which are provisional, and what each would need
before anyone could defend it in public.  Nothing here is a recommendation to submit; no
manuscript, preprint or external contact is proposed.  Verdicts marked "pending" wait for a
review of ours that is still running; they will be updated, not silently replaced.*

Sources of every judgment: `docs/science/workstreams/A1_REPORT.md` (SCI-REV-0004),
`A2_REPORT.md` (SCI-REV-0006), `SM_REPORT.md` (SCI-MSG-0002), the engineering division's
ENG-RES-0008, the theory division's own §10 and §12, and the coordinator's reading.

## 0. Summary table

| # | candidate | precise claim | verification | originality after our searches | maturity |
|---|---|---|---|---|---|
| P1 | **Adaption on a cone** (theory: Theorems 11.44/11.45 with 11.54/11.58) | exact exponents of adaptive (`= hinted`) and non-adaptive randomised algorithms for the normalising constant over the log-Lipschitz class of the Hamming cube; "adaption gains the cardinality" | lower bounds machine-checked; adaptive upper bound a paper proof refereed twice internally (R7, R8); engineering: no violation in 7·10⁶ adversarial mean runs (two levels, bounded accuracy, expectation level); **not** reviewed by us | the pair of exponents and their coincidence **not found** (A1, full text of the closest sources); the formulas are in print at the cone (Suárez–Silbey–Oppenheim 2012; Chatterjee–Diaconis 2018); method of the non-adaptive bound is Mathé–Novak's | **the strongest candidate; provisional** |
| P2 | Several site types, any alphabet: the channel-coding dictionary (theory §11.26) | site function = Rényi capacity of a vertex channel; non-adaptive exponent = inverse sphere-packing exponent; adaptivity gains the sampling rate | a workstream's paper proofs, upper bounds "by transfer"; two steps machine-checked; **our review R5 running**; one reference number replicated by us (`a = 0.294791`) | capacity reading found independently by our A1; whether the sphere-packing identification is in print: follow-up running | pending (R5, A1) |
| P3 | Rounds of adaptivity (theory §11.24) | two rounds lie strictly between a fixed sample and full adaptivity | paper proofs; one lemma machine-checked; unrefereed; **our review R4 running** | not found (A1); round questions for partition functions are a 2026 topic in a different oracle model | pending (R4) |
| P4 | Verified certificate kernels (theory §6; Lean) | soundness of three kernels; in particular one certificate valid for *every* residual of an envelope class consistent with interval anchor data | machine-checked; audit replicated at four heads by two divisions on independent machines | no proof logging for cost-function networks / MAP found; the class-wide kernel has no counterpart found; the pairwise kernel competes with verified pseudo-Boolean proof checking, now also importable into Lean 4 (A2; coordinator) | mature as a formalisation; its *advantage* unmeasured |
| P5 | Certification geometry (theory §§11.1–11.9) | certificates are coverings in a slack quasi-metric; a dichotomy and a rate–distortion exponent on product landscapes; finite-temperature counterpart | cores machine-checked; refereed internally (R2: "a coherent note, not a theorem-driven paper") | G4 plausibly original (an application of type covering); G1, G13 reformulations of named objects; G7's formula is an example in Merhav 2011 | mature as a note |
| P6 | Limit shape of profile sets of lattice chains (theory §11.22) | convex limit body for bridges; certificate sizes converge to its covering number; bounds 50…3627 | abstract theorems machine-checked; lattice lemmas paper proofs; **our review R2 running** | "Fekete for sets" is the approximate-semigroup form of the Newton–Okounkov body; the lattice application plausibly original (A2) | pending (R2) |
| P7 | **What local and thermodynamic data are worth to certification** (science; theory's Proposition 11.104) | on the cube class, free exact knowledge of all `k`-body marginals changes neither the adaptive nor the non-adaptive exponent; a mean-energy datum makes the zero residual easy and leaves the worst-case exponent unchanged | paper proofs by one author, enumerated; the non-adaptive half proved independently by the theory division; hidden-twin root numerical; **our referee R3 and formalisation L1 running** | value-of-information theorems of this kind not found (M); the code mechanism is known | provisional; a short note at best unless the field case is settled |
| P8 | Certified inference from averaged data (science) | identified sets under a model, an envelope class and data as linear-fractional programmes with flow duals; data certify a *lower* bound on model error; numbers on lattice chains | soundness proofs elementary; exact linear programmes to 10 beads (27 for one target) | the model-free and divergence-ball versions are **known** (moment problem; maximum occurrence; Christensen–Connault); the envelope-class version, guaranteed numbers and the lower-bound-on-model-error reading not found (M; follow-up running) | not a mathematics paper; a methods contribution only with a physical instance |
| P9 | Non-identifiability statements (science; A2) | (a) in a Gibbs class with bounded energy differences uniform `k`-body marginals are compatible with the whole a-priori entropy interval; (b) lattice chains are not identifiable from complete distance distributions; (c) Debye intensities lie in the profile class with constant `q²/6` | (a) paper proof, enumerated; (b) exhaustive enumeration; (c) proved, checked | (a) an observation with textbook ingredients, the Gibbs-class statement not found; (b), (c) simple, apparently not written down for chains | supporting material |

## 1. P1 in detail — the one result that would survive a hostile referee

1. **Claim.**  For `(ε/2, δ)`-correct randomised algorithms that evaluate a `u`-Lipschitz
   function on `{0,1}ⁿ` and return `ln Σ e^{−g}`: worst-case cost `exp(n·KL((Λ₁+ε₁)/u‖½) + o(n))` for
   adaptive algorithms, `exp(n·θ_na(ε₁) + o(n))` for non-adaptive ones, at extensive
   accuracies and (with `h`, `a`) at every bounded accuracy.
2. **Verification.**  Lower bounds: Lean.  Non-adaptive upper bound: paper proof through
   Harper's theorem — and now, at bounded accuracy, a second proof without it for every `n`
   (workstream A1's Proposition A1.1: chain rule, convexity, Azuma), which also covers a
   field.  Adaptive upper bound: a nested algorithm whose cost is a paper proof with a
   history of five repaired accountings (`DEAD_ENDS.md` D45), refereed twice by the theory
   division's own referees.  Independent evidence: engineering's X-005.  **No review by
   this division.**
3. **Literature.**  SCI-REV-0004.  Anchors: Mathé–Novak 2007; Krieg–Novak–Ullrich 2025 and
   Novak 1995 (size of adaption gains on convex non-symmetric classes); Suárez–Silbey–
   Oppenheim 2012; Chatterjee–Diaconis 2018; Karnin 2016 for "verification vs search".
4. **Originality.**  The coincidence "adaptive = hinted" with exact exponents and the
   matching adaptive upper bound *without log-concavity and without a sampler*.
5. **Computational implications.**  None at accessible sizes: the nested algorithm beats
   the plain bracket only from `n ≈ 500–2000` against the worst instance (ENG-RES-0008).
6. **Scientific applicability.**  A statement about an idealised class; it says what
   evaluations cannot do, and (with P7) what local measurements cannot add.
7. **Limitations.**  Exponents only; exact evaluations; fixed `δ`; one Lipschitz constant;
   unquantified `o(n)`.
8. **Independent validation.**  Audit replicated (Lean parts); engineering's adversarial
   search; our replication of the tables of §11.20 and of `h`, `a`; nobody outside the theory
   division has re-derived the cost of the nested algorithm.
9. **Stands alone?**  Yes: it is a theorem of information-based complexity independent of
   molecules.
10. **Needed.**  A self-contained proof of the nested algorithm's cost with the `o(n)`
    explicit on a sub-class and an every-`n` statement somewhere (the radial class); the
    positioning "linear functional, convex non-symmetric cone, relative error, gain =
    cardinality"; removal of novelty claims on the formulas; an external reader for the
    cost proof.  **The single most valuable investment in the whole programme, if a
    publication is wanted, is an independent line-by-line check of Theorems 11.52/11.56.**

## 2. P7 in detail — ours, judged by the same standard

1. **Claim.**  Theorems 4, 4′ (= theory's Proposition 11.104), 5 and Proposition 5b of
   `INFERENCE_LIMITS.md`.
2. **Verification.**  One author; exact enumeration for the code facts; exact arithmetic
   for the hidden twin (the root is found numerically, not proved); the non-adaptive half
   derived twice independently.  Referee and Lean formalisation running.
3. **Literature.**  SCI-MSG-0002.  The mechanism (codes of dual distance `> k`) is textbook.
4. **Originality.**  A query model with two oracles and theorems about what the second is
   worth were not found.  The proofs are short.
5. **Implications.**  None computational.
6. **Applicability.**  The uniform cube is symmetric; the result may owe everything to
   that symmetry (with a field a marginal oracle may strictly lower the exponent:
   SCI-REQ-0001 Q2).  Until the field case is settled, "local data are worth nothing" is a
   statement about one model.
7. **Limitations.**  Exact marginals; zero known part; exponents.
8. **Validation.**  The theory division's independent derivation of one half.
9. **Stands alone?**  As a remark inside P1's paper, yes.  As a paper, no.
10. **Needed.**  The field case; a proof of the hidden-twin root; the exchange rate
    between evaluations and expectations in classes between linear and first-order.

## 3. What is *not* a publication, and why

* **The identified-set framework (P8)** is known mathematics under four names.  Its value
  for the programme is as an *interface*: it is what turns the kernels into checkers of
  statements about measurements.  It becomes a contribution only with one physical
  instance carried through — a fixed-backbone side-chain ensemble with public averaged
  data, a certified range and a certified lower bound on model error — and with the
  comparison against maximum occurrence as practised (`BENCHMARK_DESIGN.md`, B3, B4).
* **Theorem 2 (invisible order)** is an observation.  Its use is as a deception instance
  for benchmarks and as the reason why entropy inference from local data must state its
  assumption on interaction order.
* **The exponent refinements beyond P1–P3** (mean-field known parts, type classes,
  several site types) are extensions whose publication value depends entirely on P1
  standing.

## 4. Ranking for further investment (justified, not mandatory)

1. An external-quality check of the adaptive upper bound (P1, item 10).
2. The physical instance for P8 with B1's measured class constants — the only route by
   which any of this touches a molecule.
3. The field case of P7 and the robust interval of a ratio (SCI-REQ-0001 Q1, Q2): both
   change what the theory is *about* (measurable targets; non-symmetric models).
4. The native-versus-pseudo-Boolean measurement for P4 (SCI-REV-0006, E-1).
5. Completing the reviews of P2, P3, P6.

Lower: further exponents on symmetric models; constants in the limit shape.
