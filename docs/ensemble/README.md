# Ensemble Identifiability and Certified Inference Division

Branch: `research/ensemble-identifiability` (created 2026-11-26 from the theory division's
head `a844b5a`).  This division writes only to this branch.  It reads the other branches
(`claude/determined-ride-og1u7j`, `research/ubuntu-engineering`,
`research/scientific-translation`, `research/geometric-inference`,
`research/biological-complexity`, `research/structural-biology` — the seventh division,
authorised by the research owner on 2026-11-26 — and, once it exists,
`research/frontier-benchmarks`, the eighth, authorised the same day) and never merges,
force-pushes or modifies them.

## Mandate

An unknown probability measure `μ` on a configuration space `C` is seen only through
observations

    y_i = ∫ f_i dμ + ε_i .

What can be rigorously inferred about `μ`, or about properties of `μ`, from incomplete,
noisy, indirect, heterogeneous or adaptively selected observations of this kind?  When is
`μ` identified, when is only a part of it identified (and which part, with what certificate),
and when is inference impossible whatever the algorithm?

Scope: foundational mathematics, theoretical computer science, statistical mechanics,
certified computation, mathematical inverse problems, synthetic mathematical examples.
No biological sequence engineering, no target-specific functional optimisation, no
experimental execution.

## Layout

```
docs/ensemble/
    README.md               this file
    ENSEMBLE_REPORT.md      the mathematics: definitions, theorems, proofs, labels (the main document)
    THEOREM_REGISTER.md     one row per statement: label, where proved, how checked, novelty class
    PRIOR_ART.md            closest published results, exact differences, search log
    DEAD_ENDS.md            claims made and withdrawn, approaches that failed, with reasons
    OPEN_OBLIGATIONS.md     unresolved proof obligations and open problems, by priority
    RESEARCH_LOG.md         chronological log; "Resume here" at the top
    HANDOFF.md              what a successor needs to continue after an interruption
    SOFTWARE_INTERFACE.md   which results are computationally effective: inputs, outputs, costs, readiness levels
    BENCHMARK_CONTROLS.md   synthetic controls with ground truth for ensemble-inference software
    reviews/                internal adversarial reviews (ER1, ER2, …) with the reviewers' own scripts
proofs/Ensemble/            Lean 4 modules of this division (imported by proofs/AxiomAudit.lean)
experiments/ensemble/       numerical experiments, falsification scripts, their recorded output
experiments/ensemble/benchmarks/   reference instances: controls_v1.json (written by benchmark_controls.py) and
                            torus_instances_v1.json (written by export_torus_instances.py) — a specification, not a harness
                            (run_all.py runs thirteen check scripts and check_quotes.py; long computations — thresholds,
                            the survey of thirteen states on four angles — are stored in output_threshold.txt)
experiments/ensemble/scratch/      unreviewed prototypes preserved at the consolidation; not results (see its README)
docs/collaboration/
    consolidation/ensemble.md   the division's critical assessment at the halt of 2026-11-27 (read this first)
    ENSEMBLE_TO_ALL.md      digest and index of what this division has sent
    status/ensemble.md      current state, synchronisation record
    messages/ensemble/      ENSEMBLE-MSG-nnnn.md, ENSEMBLE-REV-nnnn.md
    requests/ensemble/      ENSEMBLE-REQ-nnnn.md
    responses/ensemble/     ENSEMBLE-RES-nnnn.md
```

## Epistemic labels (those of the programme, unchanged)

| label | meaning |
|---|---|
| **[V]** | machine-checked in Lean 4 + Mathlib; the exact declaration is named; axioms `propext`, `Classical.choice`, `Quot.sound` only |
| **[P]** | paper proof, written out in `ENSEMBLE_REPORT.md`; "reviewed" only if a named independent review covers it |
| **[K]** | known result, cited; the register says how the source was read (full text / abstract / from memory) |
| **[N]** | numerical evidence only; the script is named |
| **[C]** | conjecture |

A statement is never labelled [V] unless that exact statement has been kernel-checked.
Internal review by another AI session or subagent is called *internal review*; it is not
academic peer review and is never described as such.

Novelty classes used in the register: **new** (not found after a documented search — which
is not a proof of novelty), **formulation** (known mathematics in a formulation not found in
print), **synthesis** (known results combined), **formalisation** (known result, first
machine check we know of), **rediscovery** (found in print after we proved it), **known**.

## How to verify

```
source scripts/lean_env.sh && lake build           # all Lean modules, including proofs/Ensemble
python3 experiments/ensemble/run_all.py            # every numerical check quoted in the report, then check_quotes.py (about 20 minutes)
python3 experiments/ensemble/run_all.py --quotes-only   # after a change of the report's text alone
bash scripts/audit_all.sh                          # the programme's full audit (inherited from theory)
```
