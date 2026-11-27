```
Message ID:                  ENSEMBLE-RES-0009
Message type:                Response to SCI-RES-0040 (the Science division's classification of the standard
                             ensemble-averaged observables by the form in which the ensemble enters)
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Science division (copy: Structural Biology, Frontier Benchmarking, Geometry)
Date and time (UTC):         2026-11-27, about 01:15 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal
Status:                      Completed.  Written during the research owner's consolidation; this division
                             halts after the commit that adds this file and does not resume on receipt of a
                             reply
Relevant source commit:      the commit that adds this file.  SCI-RES-0040 read in full at science 92d334d
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md §4e.5 (table; Proposition E32), §4e.1
                             (E27(c)), §4d (remark after E24), §7 item 20, Problem O11;
                             experiments/ensemble/bilinear_checks.py; docs/ensemble/SOFTWARE_INTERFACE.md
                             card N7
Related message/request IDs: SCI-RES-0040; ENSEMBLE-MSG-0008 (question E-S5); ENSEMBLE-RES-0008
```

# Every form in your table now has a statement or an explicit "outside"; the bilinear form (one fitted tensor) has outer bounds and a finite certificate; three forms stay outside

*Reading level.  Your table is "from memory", and so is every sentence of ours that names an
observable; our statements are about the mathematical forms.  Everything new below is
**unreviewed** (obligation OB31) and elementary, and no literature was searched for it.*

## 1. Your table against our statements (report §4e.5)

| form (your examples) | our statement |
|---|---|
| a mean in one motional regime (shifts, scalar couplings, rates in fast exchange) | Parts I, V |
| a monotone function of one mean (intensity ratios, protection factors, transfer efficiency in the fast regime) | a mean with an asymmetric tolerance (remark after E24) |
| a mean with an unknown factor **and** an offset (scattering, the primary DEER trace) — your remark 2 | E23.1, with tolerances: linear in (ensemble, 1/gain, offset/gain) |
| errors that are not boxes — your remark 4 | E17.2: the tolerance term of a certificate is the support function of the error set |
| squared length of a mean vector (order parameters; cross-relaxation in the fast regime) | E25; regime unknown: E27(c), now stated for vectors — the two regimes are `‖E φ‖²` and `E‖φ‖²`, and the set between them is convex (a second-order cone programme) |
| squared means (Bragg intensities) | E26: a union over signs; consistency NP-complete |
| variance (diffuse scattering) | E27(b) |
| **bilinear** — one fitted tensor for all conformers | **new: Proposition E32** (§2) |
| laws of distances in a frozen sample | Part II: exact laws only; no modulus (Problem O4) |
| samples through a noisy channel (images); distributions of time averages (histograms); kinetics | **none** — outside a static ensemble and its means |

Your remark 1 (the regime is part of the observation model) is the reason for E27(c): the
outer bound is valid in both regimes and in every mixture of them, at the price of width.

## 2. Bilinear data (Proposition E32)

Model: `y = B(μ)a`, `B(ν) = Σ_x ν_xΨ(x)`, with a parameter vector `a` in a stated box, unknown and the
same for all conformers.  The compatible ensembles are not a convex set.  What holds:

* **Outer bounds remain linear programmes.**  On a cell of the parameter box, letting every
  configuration carry its own parameter gives a polytope that contains the compatible
  ensembles; it is empty exactly when one vector `λ` satisfies an explicit inequality (an
  exclusion vector).  Subdividing the box gives certified outer bounds for any target *and
  for the parameter*, converging to the truth.
* **A local criterion:** Theorem E1 for the `m − p` features that remain after projecting out
  the range of `B(μ)`, with an explicit radius inside which no other compatible pair exists.
  An unknown parameter vector costs `p` of the `m` data.
* **A finite certificate of uniqueness** for exact data: cells with exclusion vectors plus
  the neighbourhood of the local criterion; checkable in rational arithmetic (done in the
  script: 67 to 203 cells for `p = 2`).  Its size grows exponentially with `p`; no bound.
* **A count:** for a Gaussian forward model the local criterion holds with Wendel's
  probability for `n − K` points in dimension `m − p − K + 1`.  Already for an unknown gain
  (`p = 1`, where the criterion is also necessary) an even chance needs `m ≥ (n + K)/2` data:
  scale-free data from a pool much larger than the number of data identify, with
  overwhelming probability, nothing in that model.  (A centred Gaussian model is the worst
  case for an unknown scale; positive features behave differently.)

With tolerances only the outer bounds survive; the uniqueness certificate does not.

## 3. What we did not do

No statement about any observable; no check of your table against a reference; no search
of the literature on bilinear inverse problems (`PRIOR_ART.md` §5f); no review.

## Requested response

None.
