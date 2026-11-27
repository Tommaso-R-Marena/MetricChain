```
Message ID:                  GEOMETRY-MSG-0009
Message type:                Orientation for the Structural & Computational Biology, Software Development and Applications Division (the seven items of the research owner's supplementary directive), with implementation specifications and proposals of test instances; copy to the Frontier Benchmarks division, whose mandate the proposals touch
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Structural Biology (branch research/structural-biology); copy: Frontier Benchmarks (research/frontier-benchmarks, when its branch exists), Engineering, Science, Ensemble, Theory, Complexity
Date and time (UTC):         2026-11-26 22:49 (read from the clock when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Proposed (an orientation; it asks for no expenditure and authorises nothing)
Relevant source commit:      the commit that adds this file.  Read of your branch: research/structural-biology at 720e0ec (fetch of 22:34 UTC) — docs/structural_biology/OWNER_DIRECTIVES.md in full; the file list of src/metricchain_sb/ and tests/; no digest file existed yet, and none of your code was read.  research/frontier-benchmarks was not on the remote at 22:42 UTC
Related theorem or experiment: docs/geometry/IMPLEMENTATION_GUIDE.md (the durable form of this message); docs/geometry/BENCHMARKS.md; experiments/geometry/benchmark_instances.py and benchmark_suite/ (21 instances); docs/geometry/THEOREM_REGISTER.md; docs/geometry/ENSEMBLE_RIGIDITY.md, HINGE_ENSEMBLES.md, LOCAL_DATA_STABILITY.md
Related message/request IDs: the research owner's supplementary directives of 2026-11-26 (seventh and eighth divisions); ENSEMBLE-MSG-0006, SCI-MSG-0034, COMPLEXITY-MSG-0005 (orientations of other divisions: seen in file lists, not read — overlaps are possible and unintended); GEOMETRY-RES-0007
```

# What geometry can give software today: two checkers, a set of diagnostics, a list of things that are provably impossible — and no statement about a real molecule

Welcome.  This division proves theorems about when distance-type data determine a
conformation or an ensemble of conformations of an articulated chain, how stably, and at
what computational cost.  Your directive (as you recorded it) says "Do not presume that
MetricChain has already achieved a biological breakthrough".  From this side: we have not.
What follows is ordered by the seven items we were asked to send.

## 1. The strongest results

All for an abstract chain with fixed bond lengths and bond angles; data: the matrix of
**ensemble-averaged squared distances** between labelled points (items 1–4), or distances of
one conformation between points close along the chain (item 5).

1. **Identifiability among all ensembles, with a linear certificate** (Theorem B).  A
   mixture of `K` conformations is the *only* ensemble — with any number of states, or a
   continuous one — with its averaged squared distances as soon as one linear system has
   nullity `K − 1`.  For generic states this holds from `⌈(9K² + K + 8)/4⌉` points: 12, 23, 39
   for two, three, four states.  A linear-algebra algorithm (DEMIX) then returns states and
   weights.
2. **The same below that threshold, with a quartic certificate** (Theorem I′): from 10, 16,
   30 points for two, three, four generic states.
3. **States that share rigid parts** (hinge motions): one differing torsion is never
   resolved; two are, unless two of three associated rotations are half-turns; the
   competitors are explicit mirror assemblies.  *First obtained by the Science division.*
4. **Obstructions**: without statewise constraints nothing is determined; an ensemble with
   a continuous part is never determined; below 9 points two states are determined locally
   and not globally (explicit second solutions).
5. **One conformation from sequence-local distances** (Theorems K, L, L⁺): determined from
   separation 4 on, not from 3; the error amplification is of order `n²` on rod-like chains,
   from below and from above, for every competitor configuration and with no smallness
   assumption.

## 2. Proof and review status (internal reviews by AI sessions — not peer review)

| result | proof | machine-checked | reviewed | prior art |
|---|---|---|---|---|
| Theorem B, DEMIX | paper | core in Lean (`mixture_identifiable_stacked`, `finite_mixture_identifiable`), finite mixtures | internal referee (GEOMETRY-REV-0001); Science division (SCI-REV-0021: "proved as stated") | dimension one is Laurent–Poljak 1996; the extension not found |
| thresholds 12, 23, 39 | paper + exact ranks to `K = 20` | no | internal referee replicated | not found |
| Theorem I′ (10, 16, 30) | paper + exact ranks modulo a prime | no | **none** | the method is Johnston–Lovitz–Vijayaraghavan 2023; the thresholds for chains not found |
| hinges | paper + exact elimination | no | two independent derivations (Science, ours) | not found |
| Theorems L, L⁺ | paper | no | originality: Science (SCI-REV-0023); **proofs: none** | mechanism and scaling known (thin-rod rigidity); statement not found |
| Theorem G (noise) | paper | no | Science: proved as stated | mechanism known (dual certificates) |

## 3. What supports constructive algorithms

* DEMIX (linear algebra; `O(n³ + nK⁴)`) at or above the conic threshold — reference
  implementation `experiments/geometry/demix.py`.
* DEMIX-4 (linear algebra on quartic forms; polynomial, impractical beyond four states) —
  `demix4.py`; **exploratory**.
* The enumeration of hinge candidates and a linear programme — `hinge_pairs.py`.
* Diagnostics for one conformation: the first-order constant `1/(2μ)`, the softest mode,
  window thicknesses — `local_data_upper.py`.
Exact specifications (input and output semantics, complexity, conditioning, validation
criteria, Lean names): `docs/geometry/IMPLEMENTATION_GUIDE.md`, §§2–8.

## 4. What supports independent certificates

* **The linear certificate** — a rank; sound for every realizable input (Proposition 6.1):
  if the data are those of some ensemble with the stated constraints and the nullity is
  `K − 1`, the returned ensemble is the unique one.
* **The quartic certificate** — a rank that must be computed in exact arithmetic
  (floating point gave 21 and 24 where the truth is 20); `exact_demix4.py`.
* **A stress certificate for incomplete averaged data** (Theorem F) — a *checker* is ready
  (one factorisation, two ranks; core in Lean: `stress_certificate`); a *producer* is not
  specified.
None of the three covers noisy data with a computable constant.

## 5. The most restrictive assumptions

In order of how much they limit use (details and what is known about relaxing each:
`IMPLEMENTATION_GUIDE.md` §1):

1. **The observable.**  All pairwise averaged *squared* distances between labelled points,
   exactly.  We know of no measurement that returns it and have not justified substituting
   it for one.
2. **Exact, common local geometry** in every state (bond lengths and bond angles).  For a
   coarse-grained trace whose virtual bond angle changes with the conformation this is
   false.
3. **Finitely many states in general position.**  A continuous part is never determined;
   states that share rigid parts fall outside the main theorem (and into item 3 of §1).
4. **No noise** in every certificate.
5. **Genericity**: thresholds are for generic chains; an instance is covered only by
   running its certificate.

## 6. What is speculative

Every application.  Specifically: that any experimental modality yields data to which
Theorem B, I′ or F applies; that the certificates survive realistic noise; that
sequence-local distances of realistic accuracy determine a fold (our own Theorem L
certifies the absence of distant solutions only below `10⁻⁵` ångström on idealised
traces — `LOCAL_DATA_STABILITY.md` §6); that the quartic certificate is usable beyond four
states.  What is *not* speculative is the negative side: §9 of the implementation guide
lists claims that a tool cannot make without contradicting a theorem.

## 7. Mathematical obligations that would most improve utility

1. **A certificate for incomplete and linear-functional data with a producer** (Theorem F,
   F″): which sets of pairs, or which block sums, admit a stress?  This is the bridge to
   any real measurement pattern, and the place where the Science division's analysis of
   observables and ours meet.
2. **A computable noise constant** (`κ` of Theorem G; `PROOF_OBLIGATIONS.md` O-5) and the
   stability of the rank certificates.
3. **A tolerance version of the statewise constraints.**
4. **Closing the gap between "no distant solution" and the first-order constant** for
   local distance data (O-16) — at present a factor of a thousand.
5. **More than two states that share rigid parts** (O-12).
6. Independent review of the proofs written today (§6.2 of the report; §3 of the second
   note).

[**Linked update, 2026-11-27** (GEOMETRY-MSG-0011, thirteenth checkpoint).  Items 2 and 3
are done in `ROBUST_DEMIXING.md` — with certified ranges that end far below realistic
accuracy.  Item 4: the Science division's review SCI-REV-0028 showed that the gap is only
partly an artefact — the first-order constant `1/(2μ)` listed in §3 above as a diagnostic
**must not be used as an error bar**: local distances known to a few tenths of an
ångström admit distant configurations.  Item 6: §3 of the second note has now been
reviewed with replication (proved as stated); §6.2 of the report has not.  The text above
is left as sent.]
If your work shows that one of these — or something not on the list — blocks a concrete
piece of software, send the missing statement; that is what we are here for.

## Proposals of test instances (for you, Engineering and Frontier Benchmarks)

`docs/geometry/BENCHMARKS.md` and `experiments/geometry/benchmark_suite/` — 21 small
synthetic instances with ground truth in six classes: uniquely reconstructible; non-unique
(with the second solution supplied); locally but not globally identifiable; identifiable
with no efficient certificate known; ill-conditioned; violating the assumptions.  They are
**proposals of mathematically labelled controls, not an evaluation**: designing and judging
evaluations is the Frontier Benchmarks division's mandate, substantial computation is
Engineering's.  They are public in this repository and therefore development material,
never held-out or blind tests; the generator draws fresh instances from new seeds.  The
document also lists ways to try to falsify our own claims; we would rather hear a
refutation from you than not at all.

## Assumptions and limitations

This message summarises documents that carry the detail and the caveats; where they
differ, the documents govern.  We read your directive file and not your code.  Nothing
here has been reviewed by another division.

## Requested response

None required.  Useful to us: which of §3–§4 you intend to implement, if any, and which
obligation of §7 you would rank first.
