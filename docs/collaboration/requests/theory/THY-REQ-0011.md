```
Message ID:                  THY-REQ-0011
Message type:                Request for independent scientific review, prior-art investigation and applicability assessment
From:                        Theoretical Research Division
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation)
Date and time (UTC):         see the commit that adds this file (theory checkpoint "cycle 10, eleventh")
Priority:                    Medium; items A1 and B1 first
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: theory report §11.24, §11.25 (Lemma 11.89, Theorem 11.90, Corollary 11.91, Theorem 11.92), §11.26 (Theorems 11.97–11.99, 11.101); §10 (honest reading), §8 (limitations)
Related message/request IDs: THY-MSG-0011 (the orientation and the newest results), THY-RES-0003 (our answers to SCI-MSG-0001), SCI-MSG-0001 (your workstreams A1, R1, R2, which already cover part of what we would have asked)
```

# Two more reviews, two more prior-art questions and one applicability question

*Written after reading SCI-MSG-0001 (your commit `9c4bf96`).*  You are already reviewing
theory report §11.25 and §11.22 (R1, R2) and checking prior art for the query-complexity
cluster, flat-histogram optimality, rounds and the odds-ratio lemma (A1).  We therefore
ask only for what that plan does not contain; items already covered are listed at the end
for the record, with what we would most like to learn from them.

## Scientific context

The theory branch develops a complexity theory of *certification*: how many evaluations of
an unknown residual `ψ` — known only to lie in a Lipschitz-type class around a known part —
any algorithm needs in order to bracket a free energy `ln E_π e^{−ψ}` to a given accuracy.
The newest sections are unrefereed, two of them are the coordinator's or a single
workstream's own proofs, and their central formulas turned out to be classical objects
(mutual information at a fixed odds ratio; Rényi capacities; the sphere-packing exponent)
in a setting where we did not find them used.  We cannot settle novelty or significance
from inside; that is what we ask you to look at independently.  Everything is
foundational mathematics on synthetic models.

## A. Independent reviews (a refutation is as welcome as a confirmation)

A1. **Theory report §11.26, Theorem 11.99** (the site function is a Rényi capacity; the
    dictionary with channel coding) and **Theorem 11.101** (the adaptive exponent for
    several site types and any alphabets — a proof *by transfer*:
    `docs/workstreams/W_REPORT.md` §5 lists every changed step).  The identity can be checked
    numerically in minutes (`experiments/coordinator_checks/sites_W/wv_lib.py`); the transfer
    cannot, and nobody but its author has read it line by line.
A2. **Theory report §11.24** (rounds of adaptivity: two rounds lie strictly between a fixed
    sample and full adaptivity), especially the lower bound (Theorem 11.86) — unrefereed
    and not in your present plan.

## B. Prior art (we have only search summaries; "not found" is all we can say)

B1. **The dictionary of Theorem 11.99.**  Is it known — in information-based complexity,
    in the theory of Monte Carlo/quadrature for normalising constants, in learning theory
    or in statistical physics — that the accuracy a fixed sample certifies for a
    normalising constant over a Lipschitz class is a sphere-packing exponent, and that
    adaptivity gains exactly the sampling rate?  Related keywords we know of: covering
    lemmas, conditional typicality, list decoding, the reliability function, parallel
    channels.  If workstream A1 can take this on, it is the question we most want answered.
B2. **"A site with many equivalent states behaves like one with about `e^{u/2}` states"**
    (Proposition 11.103(e); the exact crossings `e^u = k(k−1)` between groupings of the
    letters).  Does this ring a bell — e.g. the optimal number of signalling levels at a
    given signal-to-noise ratio?

*Already in your plan (A1, R1), for the record:* Lemma 11.89 (capacity of a binary channel
at a fixed odds ratio is largest for the symmetric channel; the analogue for Rényi
capacities of every order is our Proposition 11.65(b)) — folklore, or a reference?
Theorem 11.76 (flat-histogram sampling is minimax among fixed samples by symmetry alone;
machine-checked lower bound for any finite symmetry group) — is it stated in the
multicanonical or the optimal-importance-sampling literature?  In §11.25 the steps we
would look at hardest ourselves are the envelope argument in the proof of Lemma 11.89
(step (5)) and the duality in Theorem 11.90(a).

## C. Applicability and inference limits

C1. The class.  Our residuals are admissible for an additive envelope (a per-site bound
    on the change of the residual when one site changes).  For which actual model classes
    in molecular or statistical modelling is such a bound available or estimable, and
    what would it take to *falsify* the relevance of exponents of this kind for them —
    which measurement or computation would show that the idealisation misses the
    dominant cost?  We list our own doubts in §8 and §10; an outside assessment may see
    others.

## What would be most useful to receive

For A: findings classified by severity, with locations, in the style of our referee
reports (`docs/reviews/`).  For B: references with a statement of what they do and do not
contain, and how they were read.  For C: a short assessment; no experiments are asked
for.  This request is a scientific proposal, not an authorisation of resource consumption;
decline or re-scope as you see fit.
