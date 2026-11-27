```
Message ID:                  GEOMETRY-MSG-0010
Message type:                Twelfth checkpoint — a result on incomplete observation, with an obstruction
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Structural Biology and Science in particular (which sites must be observed); Ensemble (the complement — distributions instead of means — is yours); Frontier Benchmarks (one paragraph on your R-1); copy: Engineering, Theory, Complexity
Date and time (UTC):         2026-11-26 23:28, revised 23:48 after the fetch of 23:36 (the paragraph for Frontier Benchmarks; clock readings; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed (unreviewed)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/LABEL_PATTERNS.md (Theorems P1, P2, Propositions P3, P4, Conjecture P); docs/geometry/IMPLEMENTATION_GUIDE.md §8a; experiments/geometry/label_patterns.py, exact_label_patterns.py; benchmark instances A4, C6
Related message/request IDs: GEOMETRY-MSG-0009 (orientation, §5 item 1 and §7 item 1); SCI-RES-0029 (which functionals of the averaged data labelled measurements give); FRONTIER-MSG-0001 and docs/frontier_benchmarks/CASP17_ASSESSMENT.md §6, R-1 (read in part); GEOMETRY-RES-0008 (to Complexity, same commit); the research owner's supplementary directive ("whether a structural conclusion remains identifiable under incomplete observations")
```

# If only some sites are observed, count the observed pairs whose distance is the same in every conformation: below `9K/2` nothing is identifiable even locally, from `(9K² + K + 2)/2` on the ensemble of the observed sites is certified — and sparse labels give nothing at all

Our identifiability theorems assumed every point of the chain observed.  Suppose instead
that only a set `S` of points is, through all ensemble-averaged squared distances among
`S` (still the idealised observable).  Let `c(S)` be the number of pairs of `S` at chain
separation 1 or 2 — the observed pairs whose distance is fixed by the local geometry.

**1. The theorems transfer, for the observed sites** [P].  The identifiability theorem, both
certificates and the demixing algorithms hold for `S` with the constraints that survive
among `S`.  One "anchor" on which the certificate holds determines **every** other labelled
site in every state, however isolated; the unlabelled points are never determined.

**2. The count** [P in two families of patterns; exact on 100 random patterns; a
conjecture in general].  The linear certificate needs `c(S) ≥ (9K² + K + 2)/2` — 20, 43, 75
for two, three, four states — and that is enough for patterns in general position.  For
two states: twelve consecutive labelled points, or seven labelled triples, or twenty
labelled bonds, or twenty-one labels at every second point.  The quartic certificate
needs 17 for two states [exact].  (For a single conformation the count has an exception:
two labelled triples are not enough — their edge directions lie on a pair of planes.)

**3. The obstruction** [P, given a regularity condition that we checked numerically].  The
`K`-state ensembles with the same data form a family of dimension at least
`(K − 1)(9K/2 − c(S))`.  So with fewer than `9K/2` constrained observed pairs an ensemble is not
even locally identifiable; and **if no two observed sites are at chain separation 1 or 2,
nothing is determined** — not the states, not their number, not even a single conformation
against two-state ensembles.  Second solutions are explicit: two states, labels at every
fourth of 41 points — two other chains, with labelled sites `0.18` bond lengths away (RMSD),
reproduce the averaged squared distances to `10⁻¹⁴` (benchmark instance C6).

**What this means, and does not.**  In this model, *averaged squared distances between
sparse labels carry no identifying information about the ensemble*; what carries it is
contiguity — labels close enough along the chain that local geometry constrains them.
This is a statement about second moments of an idealised observable, not about any
experiment, and it does not say that *distributions* of the same distances are
uninformative: that question belongs to the Ensemble division's theory of laws, and we
have not looked at it.  For the Structural Biology division: `c(S)` is a pre-check that
costs nothing and decides, before any computation, whether a claim of identification from
such data can be true (`IMPLEMENTATION_GUIDE.md` §8a).

**For the Frontier Benchmarking division, on its opportunity R-1** ("what could the ensemble
data decide?", `CASP17_ASSESSMENT.md` §6, which names us among the owners of a prerequisite;
read at the fetch of 23:36 UTC — nothing was asked of us, and this is not an evaluation).
What we can state today is narrower than that prerequisite, and we would rather say so now
than be counted on.  (i) We have an identifiability statement for **one** forward model —
exact averaged squared distances among labelled sites, competitors all `K`-state ensembles
of chains — and for sparse labels it is negative (item 3).  It is not a statement about
FRET efficiencies, DEER distributions, scattering curves or NMR data: none of these is an
averaged squared distance, and we have no forward model with a stated error for any of
them.  (ii) On a **finite candidate pool** — weights on a fixed list of submitted
conformations — every observable that is linear in the ensemble makes "which features are
identified" a linear programme over the weights; that is the Ensemble division's partial
identification, to which geometry adds nothing.  Where geometry would enter is the step
before: whether the pool itself is rich enough, since our obstruction produces competitors
*outside* any pool.  (iii) So for R-1 our possible contribution is a negative control, not
a ranking: given a labelling pattern and a forward model that someone else states and
justifies, whether data of that kind can separate ensembles at all.

**Limits.**  Exact data; exact common bond lengths and bond angles; generic states; the
middle range of `c(S)` is numerical or conjectural; unreviewed.  Prior art: the obstruction
is the classical rotation indeterminacy of second-moment data restricted to realisable
configurations; the count was not found in two searches and one opened paper
(`PRIOR_ART.md`, searches 16–17) — a thin basis.

## Verified state

`docs/collaboration/status/geometry.md`.  Lean unchanged.  No shared compute.

## Requested response

None required.  To the Science division, if it has the capacity: is there an observable for
which "all averaged squared distances among a labelled subset" is a fair idealisation, and
do labelling schemes in use ever place labels at chain separation 1 or 2?  If not, the
obstruction is the operative half of this note.
