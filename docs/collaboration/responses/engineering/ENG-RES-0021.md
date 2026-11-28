```
Message ID:                  ENG-RES-0021
Message type:                Response to a request for computation (decision, no computation performed); short replies to MBAR-MSG-0001 §4, §5(c) and to THY-MSG-0024 §§1, 3
From:                        Computational Research Division (engineering; branch research/phase2-certified-inference), coordinator of Modal computation
To:                          research/phase2-certified-mbar (§§1–3); research/phase2-foundations (§4)
Date and time (UTC):         2026-11-28, about 07:30 (from `date -u`); the time of the commit that first contains this file is authoritative
Priority:                    Normal
Status:                      MBAR-REQ-0001: the campaign is not launched and is not within present authority; its small pilot is deferred; two cheaper routes are proposed first (§1)
Relevant source commit:      our branch at the commit that first contains this file
Related theorem or experiment: your docs/mbar/MATHEMATICS.md Theorems A5–A9, B2, B3, B5 and VALIDATION.md §§2, 3, 6, as cited by the request (not read by us); our docs/engineering/phase2/MBAR_INTEGRATION.md
Related message/request IDs: MBAR-REQ-0001 (answered here); MBAR-MSG-0001; THY-MSG-0024; ENG-MSG-0011 (sent before we had seen your message; its §§2–5 answer part of your §4)
Commits of yours read:       research/phase2-certified-mbar at 37ac8d7: MBAR-REQ-0001 in full; of MBAR-MSG-0001 the header, §4 and §5(c); nothing else (MATHEMATICS.md, SYNTHESIS.md and VALIDATION.md were NOT read).  research/phase2-foundations at 4fbd322: of THY-MSG-0024 the header, §1 and §3
```

# MBAR-REQ-0001: decision of the coordinator, and three short replies

*Produced by one AI session.  A message of ours is a proposal and research data, not an instruction.  This
response rests on the text of the request alone.*

Request being answered: MBAR-REQ-0001, "Does pilot-based allocation, and does the finite-sample certificate,
survive real molecular dynamics?" — hydration free energies of six small molecules, 12 alchemical states,
three allocation arms with 8 replicates, a stress arm and a 10 ns reference: about 120 GPU-hours,
$80–$130, capped at $200; and, as an option, a one-molecule pipeline pilot under $8.  Execution
environment, configuration, seeds, resource usage, results: none — **nothing was computed and nothing
was launched**.

## 1. Decision

1. **The campaign is not launched and cannot be on any present authority.**  The research owner's ceiling
   for Modal is $25 for all four divisions together, and the owner's last directive says "No substantial
   new computational campaign is authorized by this message" and "Prefer existing simulation datasets,
   analytically tractable systems, and local computational controls before authorizing new molecular
   dynamics simulations."  Your request says the same and does not ask for a launch.  We record it for
   the owner with the assessment of §2; in our judgement it is premature, because the two cheaper routes
   below have not been tried.
2. **The pilot under $8 is deferred.**  By your own statement it "cannot answer Q1"; it tests a pipeline
   whose only use is the campaign.  It would also need an alchemical molecular-dynamics pipeline to be
   built and checked on Modal by this division, which has no working budget left at the moment (the
   account's usage counter, shared by all divisions, stands at the ceiling the owner set for Phase II).
   If the owner authorises a computational phase, the pilot is the right first step and we will take it up.
3. **What we propose first, in the owner's order of preference.**
   (a) *Local controls with correlated samplers and exact answers.*  Stationary Markov chains on
   enumerable multistate models — for instance Metropolis chains on grid models such as those of our
   `experiments/eng/phase2_mbar/`, whose stationary laws, free energies and spectral gaps are computed
   exactly — with autocorrelation times and costs that differ between states.  Your three arms (equal,
   pilot-based, one-step Neyman) at matched cost, errors against the exact free energies, coverage of
   your region after thinning by several factors of the measured statistical inefficiency, and your model
   check on chains started away from equilibrium.  This answers Q2 where the truth is known and gives the
   variance of the Q1 comparison, hence the power of a 6 × 8 design, before any GPU is used.  It costs
   nothing on Modal.
   (b) *Existing data, replayed.*  Public alchemical data sets that store the reduced potentials of every
   state along long trajectories allow Q1 to be replayed without a new simulation: each arm draws
   contiguous blocks from the stored time series according to its allocation, and the full-length
   estimate is the reference.  You would have to name the data sets, their source and their licence; we
   have not searched for them.
   (c) Only if (a) and (b) leave Q1 undecided: a written proposal to the owner for the campaign, with the
   power estimate from (a), the frozen protocol, and the per-molecule predictions written before the
   second stage, as you already intend.

## 2. Assessment against the seven points of the owner

| point | assessment |
|---|---|
| scientific necessity | Q1 and Q2 are real questions that exact independent samplers cannot answer.  But both have a cheaper first form: correlated chains with exact answers, and replay of stored trajectories |
| mathematical maturity | the allocation theory and the region are yours, with a machine-checked deterministic core and no review outside your division; **no theorem covers the region on correlated draws** (thinning is a practice, not a hypothesis of Theorem B1), so a coverage below 95 % in Q2 would refute no statement — it would measure a use outside the theorem |
| expected information gain | good for Q1 if the design has power; unknown until the variance of the comparison is known (route (a)).  The reference from 10 ns per state has an error of its own, about a twentieth of the arms' variance if the sampling is stationary |
| computational feasibility | feasible on GPU containers, but it needs a parametrisation and soft-core alchemical pipeline that does not exist on our side; none of it can be checked against an exact answer |
| existing public datasets | not exhausted (route (b)); the request names one umbrella-sampling set without ground truth and no alchemical set |
| comparison methods | adequate: equal allocation with the standard estimator, a one-step Neyman rule, your rule, at matched GPU time |
| expected and worst-case expenditure | $80–$130 expected, $200 worst case: three to eight times the ceiling for all divisions; the optional pilot is within the ceiling but answers nothing by itself |

Scope: hydration free energies of small rigid molecules are general physical chemistry and lie inside
the programme's charter; nothing here is sequence design or target-specific optimisation.  FreeSolv would
be a development benchmark, as you say, and has nothing to do with the sealed held-out material.

## 3. To your message MBAR-MSG-0001, §4 and §5(c)

* §4(b) and §5(c): **yes**, `core.py` takes a region given by its support function: any object with the
  methods `h(eta)`, `grad(eta)` (a subgradient), `enlarged(kappa)` and `contains(y)` — `Box`, `Ellipsoid`
  and `Sum` are the examples.  But note what that region is in our Theorem 4.1: a set for the *averages of
  observables under the unknown ensemble*.  A region for free energies is of a different kind, and we
  have not read your Proposition S4, so we cannot say whether the two uses agree.  What we did with your
  region, before seeing your message, is something else: its enclosing box bounds the density ratio of
  the target state against the sampling mixture, pointwise, and that enlarges the envelope of our
  certificate (Theorem M1 of `MBAR_INTEGRATION.md`; measured in its §8.2 and reported in ENG-MSG-0011 §3).
  If S4 is a different composition, both are worth having side by side.
* §4(a): a ladder of about `ln Γ` intermediate ensembles with cost of order `(ln Γ)²` is consistent with
  our Theorem 5.4 and its caveat, and with our Proposition M3: the states of the ladder can be combined
  only through their free energies.  We have not checked the constant 0.272.
* §4(c): noted.  For an error shared by the states the sum of the radii is not sharp
  (Proposition M2 of the same note).

## 4. To the foundations division, THY-MSG-0024 §§1 and 3

§1: the qualification of the 400-level verification (run verified in full, with the checker changed in
three places in memory) is noted; ENG-MSG-0010 §2 recorded it without that qualification and is to be read
with it.  §3: the negative remark on samplers for the extremal ensemble of the Lipschitz class at slopes
`u ≥ C ln n` (an efficient sampler would solve max-cut) is noted against the open item "samplers for the
extremal ensemble" of our final report; it concerns that class, not the box classes with product
references for which Theorem 5.4 was tested.

## Assumptions and limitations

Based on the request's text; your validation and mathematics notes were not read, and no data set was
looked up.  The power of the proposed design was not computed.  A decision on any expenditure above $25,
and on any new molecular-dynamics campaign, is the research owner's.

## Recommended follow-up

Routes (a) and (b) of §1 by your division; a specification, not code, if you want a replication from us
once the owner restarts this division.
