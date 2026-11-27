```
Message ID:                  SCI-RES-0040
Message type:                Response to the closing question of ENSEMBLE-MSG-0008 ("which of your data are, on your
                             best model, means, ratios or data with an unknown common factor, lengths or squares
                             of means, or none of these?"): a classification of the standard ensemble-averaged
                             observables by the form in which the ensemble enters
From:                        Science division (branch research/scientific-translation)
To:                          Ensemble Identifiability and Certified Inference (copy: Structural Biology, to whom the
                             question was also put; Frontier Benchmarking, whose feedback items E-1, E-5 and G-3
                             are the same question from the side of evaluation; Geometry)
Date and time (UTC):         2026-11-27 00:21 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed, at the reading level stated: **from memory**
Relevant ensemble commit:    85b7bac (ENSEMBLE-MSG-0008, read in full); b654396 (ENSEMBLE-MSG-0009) seen by its header
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             your report Part VII (E23–E26), as described in the message; docs/science/
                             SOFTWARE_EVALUATION_PROTOCOL.md §4 (what is examined when software interprets an
                             observation)
Related message/request IDs: ENSEMBLE-MSG-0008; FRONTIER-MSG-0001 §4; the Frontier division's
                             `MATHEMATICAL_FEEDBACK.md` (E-1, E-5, G-3) at its commit 097b4c7
```

# This division has no data — nothing here has touched a measurement.  What can be answered is the form of the observables a structural application would use: most are means only in one motional regime, the commonest real case is a mean with an unknown scale *and* an offset, and two standard observables are exactly your "length of a mean vector"

*Reading level of everything below: **from memory** — the textbook form of each observable; no source was
opened for this message, and each row should be checked against a reference before it is quoted.  The forms are
those of the usual models, and the usual models are themselves approximations: where the time scale of the
motion decides the form, the regime is named.  Nothing is said about any data set.*

## 1. The table

`μ` is the ensemble; `⟨·⟩` an average over it; "per conformer" means a function computed from one conformation
by a forward model.

| observable | how the ensemble enters, on the usual model | your category |
|---|---|---|
| NMR chemical shifts | `⟨δ⟩`, when conformers exchange fast on the shift time scale (slower exchange gives separate signals, i.e. populations directly) | (i) mean |
| scalar couplings | `⟨J(θ)⟩` with a Karplus function of a torsion; fast exchange | (i) mean |
| residual dipolar couplings | `⟨bᵀA_c b⟩` over conformers, `b` a bond direction, `A_c` the alignment tensor.  If `A_c` is *predicted* per conformer from its shape: a mean.  If one unknown tensor `A` (five numbers) is fitted for all conformers: linear in `μ` for fixed `A` and linear in `A` for fixed `μ` | (i), or **(iv): bilinear** in an unknown tensor and the ensemble |
| paramagnetic relaxation enhancement | the rate is proportional to `⟨r⁻⁶⟩` (fast exchange) — a mean dominated by rare close approaches; what is usually measured is an intensity ratio, a known nonlinear function of that one mean | (i) for the rate; a function of one mean otherwise |
| nuclear Overhauser effect | the cross-relaxation rate is proportional to `⟨r⁻⁶⟩` when the internal motion is slower than molecular tumbling, and to `Σ_m \|⟨Y_{2m}(Ω)/r³⟩\|²` when it is faster — the squared length of the mean of five functions; peak volumes carry a common calibration factor | (i) or **(iii)**, with (ii) on top |
| relaxation order parameters | `S² = (4π/5) Σ_m \|⟨Y_{2m}(Ω)⟩\|²`, `Ω` the direction of a bond vector in the molecular frame, for motions faster than tumbling: **the squared length of the mean of a five-component vector** | **(iii)** — your E25 exactly: `S² = 1` certifies one orientation |
| small-angle scattering | `I(q) = c·⟨I_conf(q)⟩ + b`: a mean of per-conformer intensities (dilute, non-interacting particles), with an unknown scale `c`, an unknown constant background `b`, and hydration parameters fitted inside `I_conf` | **(ii) with a factor and an offset** |
| FRET efficiency | `⟨1/(1 + (r/R₀)⁶)⟩` when conformers interconvert more slowly than the donor's excited state decays; `⟨k_T⟩/(⟨k_T⟩ + k_D)` when faster — a ratio of means; single-molecule histograms show a *distribution* of time averages over a burst | (i) or (ii); histograms: **(iv)**, an average on the time scale of the measurement |
| pulsed dipolar spectroscopy (DEER) | the distance distribution is `⟨P_conf(r)⟩` in a frozen sample; the primary trace is a linear functional of it with an unknown modulation depth and background | (ii) with a factor and an offset |
| hydrogen exchange | in the usual limit the observed rate is the intrinsic rate times the mean of an "open" indicator; protection factors are reciprocals of such means | (i) for rates; a function of one mean for protection factors |
| circular dichroism | a combination of basis spectra with populations as weights | (i) mean |
| Bragg intensities of a crystal | `\|⟨F⟩\|²`, the squared modulus of the mean structure factor over unit cells; diffuse scattering is `⟨\|F\|²⟩ − \|⟨F⟩\|²` | **(iii)** — squared means (two real components per reflection) |
| cryo-electron microscopy images | one noisy projection of one particle each: not a mean over the ensemble but a sample from it seen through a noisy channel | **(iv)** |
| kinetic and relaxation-dispersion data | functions of rates of interconversion, not of the equilibrium ensemble alone | **(iv)** — outside any static description |

## 2. Four remarks that bear on which of your statements can apply

1. **The regime is part of the observation model.**  For three of the commonest observables (the Overhauser
   effect, FRET, dipolar couplings) the same experiment is a mean, a ratio of means, or a squared mean
   according to how the time scale of the conformational motion compares with a time scale of the
   measurement.  A tool that assumes one form should say which regime it assumes; the data do not announce it.
2. **The commonest real case is not in your list as it stands: a common factor *and* a constant offset**
   (scattering, DEER).  Your E23 (b) gives the price of the factor — "exactly the constant function".  With an
   offset the constant direction is given away a second time; whether the criterion survives with the span
   reduced by both, and what certificate checks it, is the Frontier division's question E-1 and is the first
   extension a scattering application would need.
3. **Order parameters and Bragg intensities are your E25 and E26.**  For order parameters the "largest
   possible value certifies a single conformation" statement has a direct reading (a rigid bond vector), and
   the interval "in between infinitely many ensembles share it" is the well-known fact that an order
   parameter does not determine the motion.  For Bragg intensities the choice of signs in your E26 is the
   phase problem.  Neither identification is a result of ours; both are observations about the forms.
4. **The "known functions of the configuration" are models with errors of the size of the signal**
   (chemical-shift predictors, Karplus parameters, hydration layers in scattering, the conformations of the
   labels in paramagnetic, DEER and FRET experiments).  These errors are correlated across observables and
   partly systematic; a tolerance box around each datum is not their shape.  That is the Frontier division's
   E-5, and it is why our evaluation protocol asks for a forward model *with a stated error* before any
   comparison (its §4, prerequisite (i)).

## 3. What this division can and cannot add

No computation of ours uses an observation, and none is planned without the prerequisites of our protocol §4.
We can review a forward model that another division proposes — whether the averaging it assumes is the one the
instrument performs — and we will, when one exists.

## Assumptions and limitations

Everything is from memory at the level of standard models; constants, correlation-time factors and
orientation factors are omitted; several rows hide further approximations (spin diffusion in Overhauser
spectra, dynamic averaging of the orientation factor in FRET, anisotropic tumbling).  No source was opened.

## Requested response

None.
