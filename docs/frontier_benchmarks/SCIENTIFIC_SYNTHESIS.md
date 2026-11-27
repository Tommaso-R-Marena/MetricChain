# Scientific synthesis: what is established, dimension by dimension

*Frontier Benchmarking division.  Version 1, 2026-11-27 (UTC), at the end of the founding
session.  The question put to this division is whether MetricChain's mathematics and software
produce better scientific outcomes than contemporary methods under rigorous independent
evaluation.  The answer below is given separately for the ten dimensions of the directive,
because an advantage in one is not an advantage in another.  Evidence classes: **[O]** our
own runs (all exploratory, class A-EXP, development instances); **[D]** another division's
record at a pinned commit, not replicated by us; **[L]** literature, with the read level of
the assessment it comes from.  Nothing here is held-out evidence, and none exists yet in the
programme.*

## 1. The answer in one paragraph

**Not established, in either direction, on any dimension that involves a comparison with
experiment; established as a design property on guarantees; currently negative on speed.**
MetricChain has built — on optimisation machinery that is standard in the field — a layer
that returns answers with machine-checkable certificates and that declines when it cannot
certify.  Its own authors measure it slower than the standard uncertified solver and state
that it predicts no structure; the only accuracy evidence that exists points the other way
(the certified optimum of the present energy model disagrees with the deposited side chains
at most sites of its one reported case); and the comparison that would show whether a native
certificate is worth having — against the certified solving that already exists — has been
run by nobody.  What is distinctive and testable is its behaviour when evidence is
insufficient.

## 2. Dimension by dimension

| dimension | what the evidence says today | basis | what would change it |
|---|---|---|---|
| **D1 predictive accuracy** | **No positive evidence; one unfavourable development datum.**  Nothing predicts a backbone.  For side chains on a given backbone, the software division reports that its certified optimum for ubiquitin differs from the deposited conformation at 37 of 65 sites.  Published work finds the exact optimum of a standard energy improves side-chain accuracy by under 0.1 % over a heuristic one, and that repacking predicted backbones does not help | [D] structural biology `1756529`; [L] snippet-level for the first, full-text for the second | FB-P-02 on the sealed list (FRONTIER-REQ-0001 C); its pre-declared expectation is equivalence with a heuristic optimum of the same energy |
| **D2 scientific reliability** | **Model-relative by construction, and its authors say so.**  Every certified number is about published tables; the step from a real energy to those tables is unproved; science measures its best certificate as four to five orders of magnitude more precise than the energy model is accurate, and a rigid-rotamer optimum as sometimes lying in a different well from the continuous optimum | [D] science `2796bec` | a certified evaluation of table entries (T-4); a forward model with a stated error for any observable |
| **D3 computational efficiency** | **Negative so far.**  The software division: toulbar2 finds the same optimum 7–25 times faster on its six development structures.  Our pilot on ten public instances: slower by one to two-and-a-half orders of magnitude where both finish, with abstentions where toulbar2 finishes in seconds (`RESULTS.md` §1).  Theory and engineering: the adaptive algorithms are worse than plain Monte Carlo at every simulable size | [D]; [O] | a replication with a mature implementation and longer budgets; a pre-stated crossover size (T-3) |
| **D4 numerical stability** | **Strong where arithmetic is exact; unknown at the boundary with real numbers.**  Checkers use integer arithmetic only; a certificate written to a file is accepted again after reloading [O].  Not shown: bit-identical instances across machines (its authors: one machine only); certified rounding of energies.  The geometric stability theorem is empty at realistic accuracy by its authors' account | [O]; [D] | cross-machine reproduction by engineering; interval-evaluated tables |
| **D5 uncertainty calibration** | **Correct by construction on what was checked; informativeness open.**  Nine planted controls of the ensemble division replicate under independent code: every published certificate checks exactly, every interval is reproduced [O].  The software division's first certified enclosure of ln Z for a small protein is 1.36 nats wide, "not tight enough for populations" [D] | [O]; [D] | FB-P-03 and FB-P-04 at scale: coverage is necessary, width decides usefulness |
| **D6 generalisation** | **Unknown: no held-out result exists.**  A sealed held-out list of 47 structures released after every relevant cut-off is ready (FRONTIER-FRZ-0002) | — | FRONTIER-REQ-0001 B |
| **D7 interpretability** | **A real, modest strength.**  A certificate decomposes into eliminations and dual bounds that a reader can audit; the software division's certified per-residue "flip gaps" make a point no optimum alone makes — the certified minimum is one of very many nearly degenerate configurations (61–81 % of residues can change state below 3RT) | [D]; [O] for the structure of certificates | — |
| **D8 reproducibility** | **Good practice throughout; one cross-division replication of ours.**  Pinned commits, checksummed instances, stored result rows, tables generated from artifacts.  We replicated nine ensemble controls with independently written code and reproduced the software division's agreement with toulbar2 on instances it had not seen | [O] | independent replication by engineering of the pilots themselves |
| **D9 mathematical guarantees** | **The established strength, with an unmeasured rival.**  Rule semantics machine-checked in Lean; checker implementations tested, not verified.  No published proof logging for cost-function-network solving was found by our assessor or by science; the certified alternative that does exist (pseudo-Boolean proofs checked by a formally verified checker) has not been compared.  On instances that close with little branching the certificate is in substance an exact dual of the linear relaxation plus an elimination trace | [D]; [L]; [O] | FRONTIER-REQ-0001 A (iii), (iv); theorem T-1 |
| **D10 recognising insufficient evidence** | **The most distinctive behaviour observed, on small planted cases.**  The certified producer abstains rather than return an unproved value; the identification verdicts say NOT IDENTIFIED where two standard baselines each return one perfectly fitting ensemble, sometimes far from the planted one [O].  Theory's own example shows a false certificate when a hypothesis is violated, so "fails safe" is not automatic outside the hypotheses | [O]; [D] | FB-P-09 (planted violations); a graded output (E-3) |

## 3. Four statements we can defend, and four we cannot

**Can be defended today**

1. MetricChain is not a structure predictor, was not a CASP17 participant, and has no
   CASP17 result of any class.
2. Its certified minimum-energy computations agree with an established exact solver on every
   instance where both finished — six development structures in its authors' own run, and
   the four of ten public instances, never seen by its authors, on which both finished in
   our pilot.
3. Those computations are, at present, much slower than that solver and reach fewer
   instances within a fixed budget.
4. Its certified statements about ensembles replicate under independent code on the planted
   controls we recomputed, and behave differently from point-estimate methods exactly where
   the data underdetermine the answer.

**Cannot be defended today**

1. That a native certificate is cheaper, smaller or more trustworthy than proof logging with
   a verified checker — never measured.
2. That exactness improves agreement with experiment — no evidence, and published evidence
   against.
3. That any certified interval is informative for a real molecule — the discretisation and
   the energy model dominate the budget, and no forward model with a stated error exists.
4. That the theory's asymptotic advantages appear at accessible sizes — measured not to, so
   far.

## 4. Where the mathematics meets experiment, and what stands between

| meeting point | MetricChain's mathematics | community evidence | what is missing |
|---|---|---|---|
| ensembles from averaged data | exact identification criteria and intervals for linear data on a finite pool; partial results for one unknown factor | blind assessments found no submission fitting combined RDC and SAXS data; reweighting depends on prior and forward model; this year's CASP has seven targets judged against such data | a forward model with a stated, structured error; verdicts that survive enlarging the pool; a graded "how far apart" output |
| reconstruction from distances | exact identifiability thresholds for mixtures; a stability theorem | documented degeneracies (reflection; single alignment media); 5 Å accuracy of FRET distances | noise guarantees; data in the form instruments deliver (block sums, r⁻⁶ averages) |
| side chains on a backbone | certified optimum; certified flip gaps | learned packers lead on experimental backbones; repacking predicted backbones does not help | the evaluation itself (FB-P-02), with its expectation written down |
| free energies | certified enclosures of ln Z | emulators disclaim calibrated probabilities; stability predictors compress toward zero | enclosures tight enough to matter; a model whose error is smaller than the enclosure |

The connection the directive asks us to look for — between identifiability, statistical
mechanics, geometry and complexity — shows most clearly in the first row: the same
underdetermination that the ensemble division formalises is what the community's blind
assessments keep measuring empirically, and the complexity division's results say that
certifying the answer can itself be hard.  That is a research direction, not a result.

## 5. The three evaluations that would move this synthesis most

1. **FRONTIER-REQ-0001 parts A–C** — the certified incumbents as comparators; the first
   held-out run; the accuracy question with its null expectation.
2. **FB-P-04 at scale with the established reweighting packages** — whether "declines when
   the data cannot decide" is a usable advantage or only a correct one.
3. **One observable taken through science's six prerequisites** — until then no statement
   about a molecule can be evaluated at all.

## 6. Standing caveats

Every review in this programme, including this synthesis, is an internal reading by an AI
session; it is not external peer review.  Our pilots are exploratory and ran on a shared
machine.  The literature rows we rely on carry read levels, and one that we could check was
wrong.
