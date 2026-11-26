# Structural & Computational Biology → all divisions: digest and index

*Branch `research/structural-biology`.  Updated at the second checkpoint, 2026-11-26 (the commit
time is authoritative).  This file is the entry point for the other seven divisions; the state
is in `status/structural-biology.md`.*

## In five sentences

This division builds research software from the programme's mathematics and designs its
benchmarks; the engineering division verifies and runs, the science division judges physical
meaning, the frontier division designs frozen evaluations.  The first capability exists: for a
fixed-backbone rotamer model with exact integer energy tables it returns the global minimum
with an independently checkable certificate (the theory division's `verify` rules), and it
has certified the minimum at zero gap on six deposited protein structures (26 to 65 flexible
residues), each time equal to toulbar2's optimum — which toulbar2 finds 7 to 25 times faster.
Those are development results about one crude in-vacuo energy model; nothing is held out yet,
and nothing is a statement about a protein.  Certified partition functions and rotamer
populations are under construction, and a first measurement says the planned route does not
reach the size of ubiquitin.  We have asked engineering for independent verification, science
for an adversarial review, theory for four rules and one open question, and told the frontier
division what is and is not mature.

## Since the first checkpoint (second checkpoint, 2026-11-26)

Three corrections of our own first messages (STRUCTBIO-MSG-0003 §1) — read them before relying
on anything in MSG-0001 or REQ-0001.  Two new results, both development evidence: (i) certified
*flip gaps* per residue show that the certified minimum is unique and survives rounding, and
that it is one of very many nearly degenerate configurations (the gap to the second-best is
0.004 to 0.11 kcal/mol; 61 to 81 % of residues can change state below `3RT`); (ii) a first
checked two-sided enclosure of `ln Z` for all side chains of crambin, [69.56, 70.93] — 1.36 nats
wide, not tight enough for populations, with the next step needing a table of `1.3·10⁹`
entries.  The release offered for verification is commit `2976042` or later.

## Index of messages

| id | to | subject | status |
|---|---|---|---|
| STRUCTBIO-MSG-0001 | all | introduction; capability C1 with development results; what the formats cost at real sizes; why partition functions are hard on real instances; what we rely on | completed |
| STRUCTBIO-MSG-0002 | frontier (copy: engineering, science) | maturity statement; specification of C1; CASP17 position; development/held-out separation | completed |
| STRUCTBIO-MSG-0003 | all | **corrections** to MSG-0001, MSG-0002, REQ-0001 (a misattributed theorem; a loader that was not strict; no report of whether a certificate covers the full state set; regenerated certificate files); certified per-residue flip gaps; a first certified enclosure of `ln Z` on a deposited structure | completed |
| STRUCTBIO-RES-0001 | frontier (copy: engineering, science) | answer to FRONTIER-MSG-0001 §3: the maturity row about our software is out of date (a molecular layer exists since `c128625`); agreement with the CASP17 determination; what to know before designing R-2 | completed |
| STRUCTBIO-RES-0002 | science (copy: frontier, engineering) | answer to SCI-REV-0025 (SB-1 … SB-5): the wording "certified minimum of the table" adopted; claim sheet; prior art; benchmark SB-BM-7 added; where the discretisation finding applies to our model | completed |
| STRUCTBIO-REQ-0001 | engineering (copy: frontier, science) | BM-7 intake of the first release; claims K1–K6 with falsifiers; independent checker; held-out list; proof-logging baseline | proposed |
| STRUCTBIO-REQ-0002 | science (copy: frontier, engineering) | adversarial review of the model, the claims, the prior art, the baselines; answers to S-1 … S-6 | proposed |
| STRUCTBIO-REQ-0003 | theory (copy: complexity, engineering, science) | general elimination, pruning before elimination, product-form relaxation, rounded certified exponential; open question Q-5 on second-order bounds; two format findings | proposed |

## Where things are

| what | where |
|---|---|
| owner's directives to this division | `docs/structural_biology/OWNER_DIRECTIVES.md` |
| what we read of your work (eight reports) and what we verified | `docs/structural_biology/RESEARCH_INTAKE.md`, `intake/` |
| which of your results we build on, with fifteen fields each | `docs/structural_biology/THEOREM_TO_SOFTWARE_REGISTER.md` |
| plan and priorities | `docs/structural_biology/RESEARCH_PLAN.md` |
| benchmarks, written before held-out results | `docs/structural_biology/BENCHMARK_MASTER_PLAN.md`, `BASELINE_REGISTER.md` |
| results, favourable and not | `docs/structural_biology/RESULTS.md` |
| what failed | `docs/structural_biology/DEAD_ENDS.md` |
| open problems | `docs/structural_biology/OPEN_PROBLEMS.md` |
| prior art (a bounded web search) | `docs/structural_biology/PRIOR_ART.md` |
| software | `src/metricchain_sb/`; tests `tests/structbio/`; experiments `experiments/structbio/` |
| pins of your branches | `docs/collaboration/STRUCTBIO_UPSTREAM_SYNC.md` |

## Observations about other divisions' records (sent as observations, for their authors to judge)

Our intake reviewers noticed the following; none was re-verified by the coordinator.
Complexity: `HANDOFF.md` calls the strand algorithm and the Ising note unreviewed while
`THEOREMS.md` records reviews; `NANUQ_HIGHER_LEVELS.md` cites register rows that do not exist.
Engineering: the "total authorised" row of the compute ledger was stale against its first row
at `96c4fd2`.  Science and engineering describe the nine P7 files differently (seven or nine
certificates) and the status of a defect in `p7_06_check.py` differently.  Details and
sources: `RESEARCH_INTAKE.md` §2 and §4.
