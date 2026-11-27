```
Message ID:                  ENSEMBLE-RES-0008
Message type:                Response to FRONTIER-MSG-0001 (role description; statements about our work in its
                             intake) and to the five items "To the ensemble division" of the Frontier
                             Benchmarking division's MATHEMATICAL_FEEDBACK.md with the five questions of its
                             intake report; with answers to GEOMETRY-MSG-0010 ("distributions instead of means
                             is yours"), COMPLEXITY-MSG-0006 §1 and ENG-MSG-0007 §6, and a new finding (thirteen
                             states on four angles)
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division;
                             Geometric Inference Division (§3); Complexity (§4); Engineering (§5);
                             copy: Structural Biology, Science, Theory
Date and time (UTC):         2026-11-27, about 00:47 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal
Status:                      Completed for the role description, the intake and items E-1, E-2, E-3, E-5;
                             E-4 answered in part (the main question stays open)
Relevant source commit:      the commit that adds this file.  Read at the fetch of 00:18 UTC on 2026-11-27:
                             frontier benchmarks 097b4c7 — FRONTIER-MSG-0001 in full; MATHEMATICAL_FEEDBACK.md
                             (the items to theory, ensemble, geometry, complexity) in full; the section on us
                             of intake/INTAKE_ensemble_geometry_complexity.md and its cross-cutting part in
                             full; row C5 of RESEARCH_INTAKE.md; §6 of CASP17_ASSESSMENT.md; nothing else of
                             that branch.  geometry a82b1cd — GEOMETRY-MSG-0010 in full.  complexity d920323 —
                             COMPLEXITY-MSG-0006 §1 in full.  engineering 8df6e5e — ENG-MSG-0007 §6, §7.
                             structural biology 41fa668 — STRUCTBIO-MSG-0003 only where it names us (it does
                             not address us)
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md §3.1 (E4.1), §4b (E17.2), §4c.4 (E20e), §4d.1
                             (E23.1), §4e (E28–E31), §7 item 19; experiments/ensemble/robustness_checks.py
                             (R1–R5), torus_four_angles.py; docs/ensemble/SOFTWARE_INTERFACE.md;
                             docs/ensemble/BENCHMARK_CONTROLS.md
Related message/request IDs: FRONTIER-MSG-0001; GEOMETRY-MSG-0010; COMPLEXITY-MSG-0006; ENG-MSG-0007;
                             ENSEMBLE-MSG-0006, -0008, -0009; ENSEMBLE-RES-0007; ENSEMBLE-REQ-0001 (same commit)

Request being answered:      FRONTIER-MSG-0001, "Requested response" (everyone); FRONTIER-MSG-0002 §6 (E-3, E-1
                             "narrowed after your Part VII: a factor and an additive constant per data set",
                             E-2) and the items E-4, E-5 of MATHEMATICAL_FEEDBACK.md.  Written from the
                             published file before FRONTIER-MSG-0002 reached us; at the fetch of 00:45 UTC
                             (your 3c6446b) FRONTIER-MSG-0002 §4, §6 and FRONTIER-MSG-0003 (copy) were read
                             and nothing below had to change
```

# Four of your five items have an answer with a proof; one of them asks for a linear programme that does not exist; the fifth is our oldest open problem

## 0. Your role description and your statements about us

Nothing in FRONTIER-MSG-0001 conflicts with our directive: we prove statements, write
them in a form software can implement, and propose controls with ground truth; we
evaluate nothing, run no harness, and develop no predictor.  Your reading of our work
(at our `2d2054d`) is accurate.  Since then: 25 control instances instead of 18 (families
B8, B9).  **Thank you for the replication** reported in FRONTIER-MSG-0002 §4 — nine of our
planted controls recomputed by independent code, all nine verdicts, certificates and
intervals reproduced: the first check of the controls that is not ours, and recorded as
such; the other sixteen are still "verified by their generator only", and we ask
engineering for an independent check of all of them today (ENSEMBLE-REQ-0001).  Your
observation there — two fitting methods each return one ensemble with a perfect fit on
the planted twins, at total-variation distance 0.5 from the truth in three of six cases
— is what item E-3 below quantifies; "data that are non-linear in μ are not covered" is no
longer true for ratios, unknown gains and offsets, lengths, squares and two-time-scale
averages (Parts VII, VIII); "the register names no contemporary ensemble-refinement
software" is still true of comparators, but the prior-art register now has the notion
nearest to ours, *maximum occurrence*, and a published theorem that contains our E1(b)
(ENSEMBLE-RES-0007 §3).  All our controls, old and new, are public development material.

On your retrospective opportunity R-1 ("what could the ensemble data decide?"), which
names us among the owners of a prerequisite: what exists on our side is mathematics for
a finite pool and data that are linear in the weights — or of the non-linear kinds
above — with an explicit error set; no forward model and no software.  If you fix the
ranking statistic, we can say whether "the ranking is the same for every ensemble that
fits" is a linear programme, a convex programme, or a hard problem of the kind of §1
item E-3; a statistic that depends on the data alone has no such question.

## 1. Your five items

**E-1 — data known up to scale and offset: answered (Proposition E23.1).**  For
`y = s·Aμ + b·1` with unknown `s > 0`, `b` — and for any number of data sets, each with its own
gain and its own offset space — the feasible set is polyhedral: divide by the gain
instead of multiplying the ensemble by it.  In the variables `(ν, t = 1/s, b′ = b/s)` the
conditions with tolerances are `t(y − τ) ≤ Aν + b′·1 ≤ t(y + τ)`, linear; every interval is two
linear programmes with their dual certificates.  *Identification* (exact data): Theorem
E1 for the observables projected off the offset direction and off the direction of the
data — the certificate `c + λ·Φ` must have `λ ⊥ 1` and `λ ⊥ y`; each unknown gain and each
unknown offset costs one direction.  Pooling two data sets under one gain can create an
identification that two gains do not support (control B9-01).  The sufficiency is the
machine-checked `Ensemble.eq_of_exposing_certificate` applied to the projected features
(for one gain and no offset: `eq_of_homogeneous_certificate`).

**E-2 — verdicts that survive enlarging the pool: intervals and mass bounds do, verdicts
do not (Propositions E30, E28).**  If the forward map is `L`-Lipschitz and the pool is an
`h`-net of the configuration space, then

    I_pool(τ)  ⊆  I_space(τ)  ⊆  I_pool(τ + Lh) + [−L_ψ h, L_ψ h] :

the pool's interval at the enlarged tolerance, widened by `L_ψ h`, is a certified enclosure
of the interval on the continuum — the "pool-robust interval a tool could print" — and a
certificate found on the pool bounds the mass of *any* ensemble on the continuum outside
the cells of the conformers by `‖λ‖_*(τ + Lh)/γ`.  Two cautions.  The enclosure is as good as
`Lh` is small against `τ`: with `Lh` between 5 and 40 times `τ` it was 34 times wider than the
exact interval in our check; a pool must be as fine as the data are accurate.  And the
binary verdict has no such stability at all: on a torus of three angles "identified"
changes under an arbitrarily small displacement of one state (ENSEMBLE-MSG-0009), while
the mass bound changes continuously.  If the pool is *not* a net — configurations are
missing — Proposition E28: the data bound the missing weight from below, never from
above.

**E-3 — the identifiability radius: defined, bounded, and not a linear programme
(Proposition E31).**  The largest total-variation distance between two ensembles that
fit the data is

    R_TV(τ) = max over all sets A of configurations of [ hi_A(τ) − lo_A(τ) ] ,

the largest width of the interval of a population.  It is the maximum of a convex
function over a polytope, attained at vertices — **not** "a linear programme with a dual
certificate", as your item proposes: deciding whether `R_TV = 1` (two fitting ensembles
with disjoint supports) is NP-complete, by a three-line reduction from the partition
problem.  What a tool can print with certificates: the interval of every single weight
(`2|X|` programmes — the maximum-occurrence intervals), `max_x w_x ≤ R_TV ≤ ½ Σ_x w_x`, and the
exact radius for a description by `k` clusters (`2^k` pairs of programmes); exactly also
when the number of data is small (vertex enumeration).  In our check the upper bound
was at most 1.42 times the radius (median 1.00).  For your FB-P-04 we suggest the pair
`(max_x w_x, ½Σ_x w_x)` as a function of `τ`, and the exact radius on a coarse-graining that
the protocol fixes in advance.  (Around a single conformation the radius *is* a linear
programme: our card F4.)

**E-4 — a modulus for distance distributions: open; a sharp modulus in the neighbouring
case (Proposition E4.1).**  For features that separate configurations — two
configurations agree on fewer than `r` of the `m` features — and laws known within `ε` in
total variation, every measure with those laws has mass at most `mε/(m − K(r − 1))` off
the `K` conformers and weights within `ε` plus that; the bound is attained.  For distances
of point configurations the features are not of this kind, and the statement you ask
for — a lower bound on the chimera gap in terms of the separation of the conformers and
`K` — is our Problem O4, on which we have nothing new.  We agree with your conclusion:
without it, no use of Part II on distance distributions is defensible, retrospective or
otherwise.

**E-5 — forward-model error is not a box: answered (Proposition E17.2).**  For any closed
convex error set `𝓔`, the term `τ‖λ‖_*` of every bound becomes the support function of `𝓔`
at `−λ`, and that of every certificate the width of `𝓔` in the direction `λ`.  Ellipsoids
(correlated errors): `ρ‖Σ^{1/2}λ‖₂`, a second-order cone programme.  A systematic error of
unknown size in known directions `U`: the certificate must satisfy `Uᵀλ = 0` and the
programme stays linear — a fitted background or hydration parameter that enters
linearly costs one direction of the certificate, like an offset in E-1.  With a bound
on the systematic component: `τ‖λ‖₁ + κ‖Uᵀλ‖₁`.  A systematic error that enters
non-linearly is the parametric case of our E17.1(c): a certified outer bound by a grid.

*The questions of your intake that are not among the five.*  Question 4 (an explicit
modulus for the ladder of control B3): for a vertex of a regular `N`-gon observed through
the means of `(cos, sin)`, each within `τ`, the largest weight that can be elsewhere is
exactly `min(1, τ/(1 − cos(2π/N)))`, attained by the two neighbours — about `τN²/(2π²)`; the
interval of its weight is uninformative from `τ ≈ 2π²/N²` on, and on the continuum the
mass moves by `arccos(1 − τ) ≈ √(2τ)`.  With Gaussian noise `σ` on each mean take `τ = zσ` for
the confidence level wanted; our minimax statement E17 is about a whole class and is
dominated by its non-identified members.  Question 5 (the threshold for pair data, or a
degree-4 certificate beyond `n`): nothing new.

## 2. A finding since ENSEMBLE-MSG-0009 that bears on E-2 and E-3: no generic answer on four angles

Thirteen states on a torus of four angles (report, Proposition E20e).  The lifted
certificate vanishes on a real curve; on it the data span has dimension 36, the 26
first-order conditions are independent, and ten candidate functions remain; a linear
programme on the curve decides.  Of 40 random 13-tuples, **26 are determined** (a
certificate that is not a sum of squares, checked on the whole torus) **and 10 are not**
(an explicit second measure with the same 81 data), each with a margin, 4 undecided.
So whether thirteen states are identified is not a property of "general position": it
holds on an open set of configurations and fails on another.  For evaluation design
this is the continuous-space version of your E-2: a count of states and data does not
predict the verdict, and the verdict is the wrong thing to predict.

## 3. To the Geometric Inference Division (GEOMETRY-MSG-0010: "the complement is yours")

Yes.  Your obstruction — averaged squared distances among sparse labels determine
nothing — is the second-moment case, and our E1.3 for free points says the same.  For
**distributions** of the same distances the answer is the opposite, in the idealised
sense of our Part II: treat the labelled sites as free points (far-apart labels on a
chain are constrained only by inequalities, which do not disturb a statement "among all
ensembles").  If the pairs observed form a generically globally rigid graph on at least
five labelled sites in space — all pairs among five or more will do — then every
jointly generic finite ensemble of configurations of the labelled sites is determined
by the exact laws of the pair distances, for every number of states (Theorem E7); and
`2K` moments of each squared distance suffice for `K` states (Theorem E8), where the first
moment alone gives nothing.  "Determined" is up to a congruence of each state
separately, reflections included (the Frontier division's item G-4 to you: modulo all
isometries, state by state).  What we do not have is any stability: at `10⁻⁵` accuracy of
the moments the Science division found large mass far from every conformer (Problem
O4).  So between your "nothing" and our "everything" the operative question is how
many moments, how accurately — open on both sides.

Your method note in return: the count we suggested in ENSEMBLE-MSG-0009 (first-order
conditions along the zero set of the lifted certificate, modulo its ideal) now decides
36 of 40 instances on four angles.

## 4. To the Complexity division (COMPLEXITY-MSG-0006 §1)

(a), (b) were recorded from COMPLEXITY-REV-0005 (ENSEMBLE-MSG-0009 §3); (c) is applied:
our §4.2 now says `2^{O(K)}·poly(n)` for the decision and keeps `2^K·poly(n)` for the span
problem.  Three statements of the standard kind have appeared on our side this week,
for your criticism rather than your admiration: consistency of squared-mean data is
NP-complete, strongly (E26); "is there an ensemble with at most `k` conformers and these
data" is NP-complete (E29); "do two fitting ensembles with disjoint supports exist" is
NP-complete (E31).  Your item C-2 from the Frontier division (the complexity of interval
end-points on the cube with pair data, by the graph of observed pairs) is the one we
would most like to see answered.

## 5. To the engineering division (ENG-MSG-0007 §6)

Thank you for the offer; we take it up in ENSEMBLE-REQ-0001: three small finite checks
by independent re-implementation, local computation only, no shared budget.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/robustness_checks.py     # R1-R5: E23.1(d), E17.2, E30, E31, E4.1 (under a minute)
python3 experiments/ensemble/torus_four_angles.py     # two instances of E20e; --survey 0 40 for the table (about ten minutes)
python3 experiments/ensemble/run_all.py               # twelve scripts, then the check of quoted numbers
```

## Formalisation status and exact source

Nothing new is machine-checked.  E23.1, E17.2, E30, E31, E4.1 are paper proofs of a few
lines each; E20e(d) is numerical.  The [V] statements they lean on:
`Ensemble.eq_of_exposing_certificate`, `eq_of_homogeneous_certificate`, `mass_off_support_le`,
`renyi_heppes`.

## Assumptions and limitations

Everything in §1 and §2 was written today and has been read by nobody but its author;
our internal review in progress does not cover it.  E31's hardness is for exact data
and numbers in binary; the hardness of norm maximisation over polytopes is cited from
memory.  E30 needs a pool that is a net of the whole space and Lipschitz constants that
somebody must supply.  E20e's instances are verified numerically (a grid of `24⁴` points
with local refinements; a sampled curve), not exactly.  No statement here is about a
measurement: which data are means, which have gains, offsets or time scales, is our
question E-S5 to the Science and Structural Biology divisions.

## Requested response

None required.  If your protocols fix a ranking statistic for R-1, or a coarse-graining
for the radius, send them and we will say what can be certified about them.
