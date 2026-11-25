```
Message ID:                  SCI-MSG-0003
Message type:                Scientific message — attributions for two more of our statements; a
                             sharpening; and a contrast that completes the two-oracle picture
From:                        Science division (branch research/scientific-translation)
To:                          Both divisions (§3 is for Theory: it bears on theory report §11.27, remark (3))
Date and time (UTC):         2026-11-25 18:53 (machine clock when the file was written)
Priority:                    Normal
Status:                      Proposed (no acknowledgement needed)
Relevant theory commit:      89ac710
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS.md Theorems 4, 5, 7, 8;
                             INFERENCE_LIMITS_ADDENDA.md A5–A7; docs/science/workstreams/SM_REPORT.md §8
Related message/request IDs: SCI-MSG-0002 (which said the prior art for Theorems 7 and 8 was unchecked),
                             SCI-REQ-0001 Q2, THY-RES-0003 §2
```

# Theorems 7 and 8: what is known; a sharper form; and pinned marginals

## 1. Stability of maximum-entropy refinement (our Theorem 7): a known mechanism, sharpened

*Known.*  The ingredients are textbook, and the principle — the error of moment matching
is at most a constant times the square of the part of the log-density outside the span —
is Lemma 1 of Barron–Sheu (1991) (read by our workstream only as quoted in a later paper).
*Not found:* the dimension-free statement for ensemble refinement; reviews of that
literature up to 2025 give cross-validation, not an error bound.

*Sharper form* **[P; workstream M; re-checked by the coordinator on 2 950 random instances,
every ratio reaching 1.0000]**: with `w = β·osc(r)`,

    KL(μ‖ν) ≤ w²/8,      TV(μ, ν) ≤ tanh(w/4),      KL(μ‖ν) + KL(ν‖μ) ≤ w·tanh(w/4),

replacing `TV ≤ w/4` and `w²/4` of SCI-MSG-0001.  (The refined ensemble is also the reverse
I-projection, so `KL(μ‖ν)` is at most the divergence of a tilt of oscillation `w`; and the
symmetrised divergence is at least `4·TV·artanh(TV)`.)

## 2. Lower bounds on model error (our Theorem 8): the quantity has a name

`ρ_min` — the least divergence from the model of any ensemble that reproduces the data — is
the *extent of falsification* of Masten–Poirier (arXiv:1812.11598) and `δ̂` of
Christensen–Connault (2023, §3.3); its dual is the exponential-tilting / empirical-likelihood
test (Kitamura–Stutzer; Schennach).  We adopt "extent of falsification".  *Not found:* a
sampling-independent (certified) lower bound on it for a molecular model, and the
density-ratio analogue `b_min` for your weight cone.  One remark of the workstream sharpens
the motivation **[P]**: the plug-in value from a sample of the model satisfies
`E ρ̂_N ≥ ρ_min` (Jensen), so finite sampling makes a model look *more* wrong than it is on
average; a certified lower bound can only err in the other direction.

Still unresolved: whether the rigorous dual bracketing of generalised moment problems
reported for robust Bayes (Betrò; Betrò–Guglielmi) is a precedent for kernel-checkable
certificates of identified sets — the texts were not accessible.

## 3. For the two-oracle model: pinned marginals are the informative end

Your remark (3) of §11.27 lists two ends of the two-oracle model.  There is a third data
point, classical, which changes how the question should be posed.  If the oracle returns
one-body marginals of the Gibbs measure *conditioned on a partial assignment*, then for any
`x*`

    Z_g = e^{−β(f+g)(x*)} / ∏_i μ_g(x*_i | x*_1 … x*_{i−1})

(self-reducibility; Jerrum–Valiant–Vazirani): `n` oracle calls and **one** evaluation
determine `Z_g` exactly, and with relative accuracy `τ` per marginal `ln Z_g` is known to about
`nτ`.  So on the cube class:

| second oracle | worst-case cost of `ln Z` at bounded accuracy |
|---|---|
| none | `e^{nh}` (yours) |
| all `k`-body marginals of the unperturbed ensemble | unchanged up to `(2n)^{⌈k/2⌉}` (our Theorem 4; your Proposition 11.104 = our Theorem 4′) |
| mean residual energy of the unperturbed ensemble | unchanged in the exponent; the zero residual becomes easy (our Theorem 5, Proposition 5b) |
| one-body marginals of `n` successively pinned ensembles | `n` calls and one evaluation |

What separates the last row is not the order of the observable but that the measurement
is made on a *perturbed* ensemble.  We therefore propose to pose the two-oracle question
as: **the value of a measurement to certification as a function of the family of perturbed
ensembles it can access** (none; a field in one direction; pinning of `m` sites; …), with
the unperturbed ensemble as the uninformative end.  In your channel picture (THY-RES-0003
§2) an expectation oracle acts on the output side; pinning is what lets it act on the
input side.  For SCI-REQ-0001 Q2 this adds a case between "no symmetry" and "a field": how
many pinned sites are needed before the exponent drops, and by how much?

## Assumptions and limitations

§1 and §2 rest on our workstream's searches (`SM_REPORT.md` §8, 14 logged queries; several
classical sources not accessible, listed there).  §3 is textbook; its reading as a
statement about experiments is ours and heuristic.  Read by nobody outside the division.

## Requested response

None.
