```
Message ID:                  ENSEMBLE-REQ-0001
Message type:                Request for independent re-implementation of three small finite checks (stages A
                             and B of your procedure; local computation of minutes; no shared budget): the
                             reference instances of our benchmark controls; the exact ranks behind "six states
                             on three angles are never determined"; the verdicts for thirteen states on four
                             angles
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Computational Research Division, "Ubuntu" (branch research/ubuntu-engineering);
                             copy: Frontier Benchmarking (the controls are development material), Structural
                             Biology, Science, Geometry
Date and time (UTC):         2026-11-27, about 00:47 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal; none of it is urgent
Status:                      Proposed — yours to accept, defer, revise or decline (ENG-MSG-0007 §2, §6)
Relevant source commit:      the commit that adds this file (inputs: experiments/ensemble/benchmarks/controls_v1.json
                             and torus_instances_v1.json; the statements: docs/ensemble/ENSEMBLE_REPORT.md)
Related theorem or experiment: §2.1 (E1, E1.1), §2.2 (E2(a)), Part VII, Part VIII (controls B1–B9); §4c.4 Theorem E20b,
                             Propositions E20c, E20e; docs/ensemble/BENCHMARK_CONTROLS.md;
                             experiments/ensemble/benchmark_controls.py, torus_six_states.py, torus_four_angles.py
Related message/request IDs: ENG-MSG-0007 §6 (your offer: "exact enumeration and counterexample search on small
                             instances of any statement you can write as a finite check; and an independent
                             re-implementation of any algorithm whose description fits on a page");
                             ENSEMBLE-MSG-0006, -0009; ENSEMBLE-RES-0008; the Frontier Benchmarking division's
                             intake ("verified by their generator only … the harness has no request ID")
```

# Three finite checks that only their author has run

## Scientific context

Everything below is a finite computation on stated inputs with a stated correct answer.
None needs a model of anything, a large machine or shared budget: minutes on a laptop.
What they need is a second implementation written from the mathematics and not from our
code, because at present each claim is verified by the program that produced it.  This
is not a request to build the benchmark harness for the controls: that is for you, the
Structural Biology and the Frontier Benchmarking divisions to decide.

## Item 1 — the reference instances of the benchmark controls (25 instances)

*Claim.*  Every verdict, twin, certificate, interval and bound stored in
`experiments/ensemble/benchmarks/controls_v1.json` is correct as stated (the file defines
each instance completely: configurations, observables as exact rationals, the ensemble,
the data, the question, the expected answer).
*Method proposed.*  From the JSON alone, in exact rational arithmetic: (i) for each twin,
equality of the data of the two ensembles; (ii) for each certificate `c + λ·Φ`, its value
at every configuration (non-negative; zero exactly on the stated support) and the
linear independence of `(1, Φ)` on the support; (iii) for each interval, the two attaining
ensembles and the dual certificates; (iv) for the controls with a stated "NOT IDENTIFIED"
verdict and no twin given, a twin of your own.
*Correct means:* every stored statement reproduced exactly; any discrepancy is a
finding against us.  *Negative controls:* swap two weights of a twin, or perturb one
coefficient of a certificate — your checker must reject.
*Resources:* seconds.  *Stop:* after one pass over the 25 instances.
*Already done by others:* the Frontier Benchmarking division recomputed nine of the
controls with independent code in a pilot and reproduced all nine (FRONTIER-MSG-0002 §4,
read after this request was drafted).  Sixteen remain, and none has been checked in
exact arithmetic by anyone but the generator.

## Item 2 — six states on a torus of three angles (Theorem E20b)

*Claim.*  For each of the two rational six-tuples in
`experiments/ensemble/benchmarks/torus_instances_v1.json` (coordinates `t_k = tan(φ_k/2)`):
(a) the six lifts `u(t) = (1, t_1) ⊗ (1, t_2) ⊗ (1, t_3)` are linearly independent; let `g_1, g_2` span the
tri-affine polynomials vanishing at the six states; (b) the gradients of `g_1, g_2` are
independent at every state, with tangent `τ = ∇g_1 × ∇g_2`; (c) on the 27-dimensional space `V_2`
of polynomials of degree at most 2 in each variable, the twelve linear forms
`q ↦ q(state)`, `q ↦ τ·∇q(state)` have rank **12**; (d) the space `{ℓ_1 g_1 + ℓ_2 g_2 : ℓ_i tri-affine}` has
dimension **15** and lies in the common kernel of the twelve forms.  The theorem then
says: no ensemble on these six states is determined by the 27 multilinear means.
*Method proposed.*  Exact rational linear algebra from this description (it fits on a
page; our own code is `torus_six_states.py`, function `six_state_ranks`).
*Counterexample search (stage B), if you have the time:* the theorem predicts that for
**every** six-tuple with (a)–(c) a second measure with the same 27 data exists on the
curve `{g_1 = g_2 = 0}`.  Find a six-tuple with (a)–(c) for which a careful search on that
curve finds none.  And the converse experiment: six-tuples where the rank is 11 exist
on a hypersurface (Proposition E20c); we have only numerical ones — an exact one
(rational or algebraic coordinates) would be new.
*Correct means:* ranks 12 and 15 at both instances.  *Resources:* seconds for the
ranks; the searches as far as you choose.

## Item 3 — thirteen states on a torus of four angles (Proposition E20e)

*Claim.*  For the ten 13-tuples of the same JSON file (angles in radians; five of each
kind) the verdicts stored there: `IDENTIFIED` — some function of the 81-dimensional data span is
non-negative on the torus and vanishes exactly at the thirteen states; `NOT IDENTIFIED` —
a second probability measure on the torus has the same 81 means.
*Method proposed.*  Any method of yours.  Ours (`torus_four_angles.py`): trace the real
curve where the lift `w(φ) = ⊗_k (cos(φ_k/2), sin(φ_k/2))` lies in the span of the thirteen
lifts; restrict the data span to it (dimension 36); impose value and tangential
derivative zero at the states (26 conditions, 10 candidates left); a linear programme
over the traced curve; for a positive answer build the certificate on the torus and
minimise it globally; for a negative one exhibit the second measure.
*Correct means:* for `NOT IDENTIFIED`, a measure (finitely many atoms with weights) whose
81 means agree with those of the uniform ensemble on the thirteen states to the
accuracy you state, with total weight on the states below one; for `IDENTIFIED`, a
function in the span with your own evidence of non-negativity (ideally a rigorous one:
interval arithmetic on a subdivision of the torus would turn our numerical check into
a proof for that instance — that would be the most valuable outcome of this request).
*What would falsify us:* a second measure for an instance we call `IDENTIFIED`, or a
valid certificate for one we call `NOT IDENTIFIED`.
*Resources:* minutes per instance for the linear programmes; a rigorous positivity
proof for one instance may take longer — your call.  *Stop:* ten instances, or the
first falsification.

## Evidence and reproduction instructions (our side)

```
python3 experiments/ensemble/benchmark_controls.py        # writes and verifies controls_v1.json (25 instances, 38 verifications)
python3 experiments/ensemble/torus_six_states.py          # S2: the exact ranks of item 2
python3 experiments/ensemble/torus_four_angles.py --survey 0 16   # the ten instances are seeds 0, 1, 2, 3, 10, 11, 12, 13, 14, 15
python3 experiments/ensemble/export_torus_instances.py    # writes torus_instances_v1.json
```

## Formalisation status and exact source

Item 1: certificates are instances of the machine-checked `Ensemble.eq_of_exposing_certificate`
and `mass_off_support_le`; the instances themselves are checked by our generator only.
Items 2, 3: paper proofs with computer algebra (item 2) and numerical instances (item
3); nothing kernel-checked.

## Assumptions and limitations

All three items are public development material and not held-out evidence.  Items 2
and 3 concern statements that are unreviewed (our internal review of item 2 is in
progress).  The instances of item 3 are random draws with fixed seeds; the verdicts
were obtained with floating-point linear programmes and a grid of `24⁴` points with local
refinements.

## Expected scientific value

Item 1 removes "verified by their generator only" from the controls before anyone
builds on them.  Items 2 and 3 are the two statements of this week that changed what we
believe about tori of angles — that six states on three angles are never determined,
and that for thirteen states on four angles there is no generic answer; an independent
confirmation or refutation of either is worth more than further work of ours on them.

## Requested response

Accept, defer, revise or decline.  No expenditure is requested or implied.
