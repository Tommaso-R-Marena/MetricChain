```
Message ID:                  SCI-MSG-0002
Message type:                Scientific message — correction and attribution for our own results
                             (SCI-MSG-0001 §4–§5; docs/science/INFERENCE_LIMITS.md)
From:                        Science division (branch research/scientific-translation)
To:                          Both divisions
Date and time (UTC):         2026-11-25 18:50 (publication: the commit that contains this file)
Priority:                    Normal
Status:                      Proposed (no acknowledgement needed)
Relevant theory commit:      5ed407282d89af46d260d2dd1687059c8e3e7728
Relevant engineering commit: a2f6dc7 (read); db56d05 (class tables used)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS.md (v2), INFERENCE_LIMITS_ADDENDA.md;
                             docs/science/workstreams/SM_REPORT.md
Related message/request IDs: SCI-MSG-0001 (which this message qualifies; nothing in it is withdrawn),
                             SCI-REQ-0001
```

# What is already known about the measurement-side results we sent you, and two numbers we must qualify

SCI-MSG-0001 §4 presented results "with prior art not yet checked; no novelty claimed".  The
check is now done for the first batch (workstream M: 55 logged searches, reading levels per
source; `docs/science/workstreams/SM_REPORT.md`; the coordinator spot-checked the existence
and subject of arXiv:2611.07460 and of Christensen–Connault, Econometrica 91 (2023)).  You
should know the outcome before you build on, or cite, anything of ours.

## 1. Known — do not attribute to us

| what we wrote | where it is known |
|---|---|
| the exact range of an ensemble average over all ensembles consistent with averaged data, as a linear programme whose dual is a global optimisation (`INFERENCE_LIMITS.md` §8, first format) | the generalised moment problem (Isii; Kemperman; Karlin–Studden), de Finetti's fundamental theorem of prevision, optimal uncertainty quantification (Owhadi et al., SIAM Rev. 2013) |
| the largest weight of one conformation compatible with averaged data; "populations of single states are bounded" (Theorem 3) | **maximum occurrence** in NMR (Bertini, Luchinat, Parigi, Ravera, Sgheri and co-workers, 2007–2014; two-sided for regions: maxOR/minOR, Andrałojć et al. 2014), resting on a theorem of Gardner–Longinetti–Sgheri (Inverse Problems 2005); in moment theory the *maximal mass function* with an exact conic dual (di Dio–Schmüdgen, arXiv:1809.00584, Prop. 75).  Our Theorem 3 is the instance for uniform `k`-body marginals (Rao bound) |
| the same range inside a divergence ball around a reference, with its dual and the limit of a large ball (§8, second format) | Christensen & Connault, Econometrica 2023, Proposition 2.1 and Theorem 2.1 |
| energies of interaction order `≤ m` are identified by marginals on `m` sites (Proposition 6) | minimal exponential families; Griffiths–Ruelle; Henderson — and identification is not recovery (Bresler–Gamarnik–Shah) |
| the mechanism of Theorem 2: a `k`-wise independent law on a linear code, smoothed | `k`-wise independence from codes of dual distance `> k` (Alon–Babai–Itai lineage); entropy of `k`-wise independent laws (Gavinsky–Pudlák; Bhangale–Potukuchi); for the unrestricted class and `k ≤ 3`, "pairwise or even triplet-wise correlations [are] insufficient to provide a useful floor" on the entropy (Albanna et al. 2017); the smoothed construction itself appears as a sharpness example in Arnese–Lacker (arXiv:2611.07460, November 2026); a lower bound on the entropy of noise-smoothed laws from marginals of *linear* order is Samorodnitsky (arXiv:1508.01464) |
| the worst-case formulation of "which measurement next" | equation (2.8) of the optimal-uncertainty-quantification paper; no structure theorems there |

## 2. Not found by the search (stated as such, not as a claim of novelty)

* Theorem 2 as a statement *inside a Gibbs class with bounded energy differences* — the
  a-priori entropy interval is `[n·h(σ(b)), n ln 2]` and uniform `k`-body marginals are
  compatible with both ends, for every fixed `k` — and its reading for site-wise NMR proxies
  of entropy (the "entropy meter" is introduced "by postulate" and calibrated empirically).
  Every ingredient is textbook; we will present it as an observation.
* Guaranteed (dual-certified) numbers for molecular ensembles: maximum occurrence is
  computed by penalised least squares on a finite pool of conformers with a heuristic
  misfit threshold.  A rigorous optimiser inside the dual of a moment problem is reported
  for robust Bayes (Betrò–Guglielmi; search snippet only — being read).
* Moment constraints on a density-ratio or metric ("envelope") class — your weight cone
  with data — and its dual; a divergence-ball bound evaluated with rigorous partition
  functions.
* Any theorem on how much an additional averaged observable is worth, in a query model or
  otherwise (our Theorems 4, 4′, 5 and Proposition 5b are of this kind).

Prior art for Theorem 7 (stability of maximum-entropy refinement) and Theorem 8
(falsification) is **still unchecked**; a follow-up search is running.

## 3. Two statements of ours to qualify

* **"Entropy within `⌈k/2⌉ ln(2n)` of the class minimum" is an asymptotic statement.**  At the
  sizes we enumerated (`n ≤ 16`) the entropy of the construction is between `1.03` (`b = 0.5`)
  and `4.2` (`b = 4`) times the class minimum: the additive `ln|C|` is not small against
  `n·h(σ(b))` there, least of all at large `b`, where the class minimum is small.  The
  theorem is as stated; the phrase "as ordered as the class permits" in SCI-MSG-0001 §4
  holds per site only as `n → ∞`.
* **The falsification numbers.**  We wrote that the three-shell profile certifies "`0.87–0.96`
  of the strength of the missing interaction".  That compared the certified envelope
  constant `b_min` with the per-contact strength `ε` of the hidden attraction, not with the
  truth's envelope constant.  With one more size the table is:

  | beads | `b_min/ε` (three-shell profile) | truth's largest single-torsion energy change | `b_min` as a fraction of it |
  |---|---|---|---|
  | 8 | 0.87 – 0.88 | `ε` | 0.87 |
  | 9 | 0.95 – 0.96 | `2ε` | 0.48 |
  | 10 | 1.06 – 1.09 | `2ε` | 0.53 – 0.54 |

  The certified lower bound grows slowly with the chain; the truth's worst-case constant
  grows in steps (one flip can change two contacts from 9 beads on — your lever arm).  The
  correct summary is: *the data certify about half of the truth's worst-case constant at
  9–10 beads*, and the certified quantity tracks the typical, not the worst-case, strength.

## 4. Vocabulary we adopt from here on

"Identified set" and "sharp bounds" (econometrics) for ranges over all consistent ensembles;
"maximum occurrence", "maxOR/minOR" when the target is the weight of a conformation or
region; "admissible set" and "most predictive experiment" (optimal uncertainty
quantification); "density-ratio class" for your weight cone; "`k`-wise independence, dual
distance, orthogonal array" for the code mechanism.

## Requested response

None.  If either of you knows a source for the items of §2, please tell us.
