# Benchmark readiness

## The test (D-5 §4)

A result is **benchmark-ready** — may enter stage D or E, i.e. may cost real money — when
all of the following exist and are written down where the benchmark can cite them:

| # | requirement | how it is checked here |
|---|---|---|
| R1 | exact mathematical definitions | the benchmark's code is written from them, not from the originating code (stage A) |
| R2 | explicit assumptions | listed in the registry entry; stage C tests inside and outside them separately |
| R3 | a precisely stated theorem, conjecture or algorithm | cited by document, section and commit |
| R4 | a pinned source commit | in the registry entry and in every result row |
| R5 | a reference implementation or a complete algorithm description | named; if only an implementation exists, the description is reconstructed and sent back for confirmation |
| R6 | correctness and performance criteria | fixed before the run (the registry's "validation") |
| R7 | known limitations | copied into `BENCHMARK_LIMITATIONS.md` |
| R8 | a meaningful baseline | `BASELINE_SPECIFICATIONS.md` |
| R9 | a credible validation protocol | exact ground truth on a subset, negative controls, a stopping condition |

A result that fails R1–R5 gets stages A–C only: small exact examples, falsification
attempts, and a message to its authors saying what is missing.  "The specification
changes daily" is a failure of R3/R4 unless the computation is itself the tool of
discovery, in which case it is entered as an *investigation*, not a benchmark.

## Status per campaign

| campaign | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **BM-1** nested adaptive algorithms | yes (`K_REPORT.md` §§2–3; report §11.19) | yes (`L_u(Q_n)`, uniform reference measure, evaluation oracle; a hint is not assumed by Theorem 11.56) | Theorem 11.56 yes; the certified-cost rule yes (remark (1b), reviewed in SCI-REV-0016); Theorem 11.58a stated, proof unrefereed outside the theory division | theory `63efc69` for the algorithm text; `dd067f1` for remark (1b) | two independent implementations of the cost bound (theory's referee, ours) and a third of the certified column (science) | fixed in the registry (X-011) | mean-run model; searched worst cases are lower bounds | non-adaptive base bracket, enumeration, hinted lower bound | flat instance exact; literal runs for two levels only (X-006b) | **ready for stage E as a bound computation and a search in the mean-run model**; *not* ready as a literal simulation of three levels (no implementation of nested literal runs) |
| **BM-2** min-certificate kernel | yes (`P7_REPORT.md` §5; `CertificateAlgebra.lean`) | yes (pairwise integer instance; box domain) | `verify_sound` machine-checked; the format is one rule of it | science `2b4ccdf`; theory `8ff0667` | two reference checkers on the science branch; ours in progress | accept nine files, reject 27 controls, brute force agrees, no unsound acceptance in fuzz | no producer on this branch yet; instances so far are the science division's | exact solvers (not yet specified) | brute force on enumerable boxes | **stage A/B now; stage D needs a producer and a baseline specification** |
| **BM-3** sandwich certificate for `ln Z` | specification exists (SCI-MSG-0025 §8), **not read by us** | not assessed | not assessed | science `2b4ccdf` | on the science branch | — | amendment of SCI-MSG-0026 §9 is unrefereed inside its own division | — | — | **not ready**: stage A after BM-2 |
| **BM-4** chain covers and limit shape | yes (X-002, X-004) | lattice exact; off-lattice in floating point with a tie analysis | THY-REQ-0002, -0008; limit shape §11.22 | theory `63efc69` | ours | published numbers reproduced | off-lattice results rest on floating-point comparisons (SCI-REV-0008, M2) | — | exact arithmetic over `ℚ[cos θ]` (not started) | lattice part **ready**; off-lattice **not ready** until the exact-arithmetic chain exists |
| **BM-6** beyond product measures | workstream Y, review R10 (read only in summary) | a two-state chain, one coupling, one slope | bounds on three exponents by blocks | theory `8ff0667`, science `2b4ccdf` | on both branches | the stated validation value of R10-E1 | — | the uniform cube's exponents | `L = 3`: 96 vertices | **stage A in progress** |
| ensemble / geometry / complexity | — | — | — | — | — | — | — | — | — | **no request received** |
