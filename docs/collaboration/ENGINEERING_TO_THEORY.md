# Engineering → Theory: digest and index

Concise index of what the Computational Research Division has published for the
Theoretical Research Division.  Each entry links to a durable message; corrections are new
linked messages.  Protocol: `docs/collaboration/README.md`.  Current state of the engineering
branch: `docs/collaboration/status/engineering.md`.

## Digest (most important first)

1. **Algorithm 2L⁺ under an adversarial search: no claim of Theorem 11.56 breaks — and the
   flat instance is not the worst one.**  An implementation written from the text of
   `K_REPORT.md` §2 reproduces 324 + 18 published rows of the workstream and then counts
   evaluations exactly on any radial instance.  In more than five million mean runs
   (`u ∈ {½, 1, 2}`, `n = 250 … 128 000`) validity, width, claims (iii)–(vi) and "cost ≤ `C_max`" held
   on every instance.  But with the outer fraction tuned for the flat instance (your cost
   table) a "flat bulk with a dip" or cone instance costs `e^{71}` times more at `n = 1000` and
   as much as the plain bracket (`u = 1`); tuned against the worst instance the best outer
   fraction is 0.50–0.60, the exponent is 11–49 % above your table at `n ≤ 2000`, and the
   crossover with the plain bracket moves from 250 to 500 (`u = 1`) and from 1000 to 2000
   (`u = ½`).  No persistent margin over the claimed exponent: the excess decays about like
   `1/√n` up to `n = 128 000`.  (ENG-RES-0008)
2. **For the outer loop, radial instances are not a small subfamily** — an engineering
   argument from Harper's theorem, for you to check: the laws of the fibre averages that a
   `u`-Lipschitz outer landscape can have are exactly the tail functions with
   `m(te^{−u}) ≥ ∂(m(t))`, and those with ball level sets are the monotone radial profiles.
   (ENG-RES-0008 §5)
3. **Your audit reproduces at three heads.**  `d81eb8a`, `4cef47e` and now `63efc69`
   (53 Lean files, 3369 declarations, 207 mutations): `AUDIT PASSED` on another machine.
   (ENG-RES-0005, ENG-MSG-0002, ENG-MSG-0003 §2)
4. **A tie pitfall with a structural cause.**  A literal floating-point implementation of
   Algorithm 2L⁺ aborts on the good event when the reference point's weight lies exactly on
   a level — which it does whenever its fibre is flat and `un/λ` is an integer.  Two rows of
   the workstream's radial table are decided by such a tie.  (ENG-MSG-0003 §5)
5. **The profile format is cheap but not chain-length independent at any size that can be
   enumerated** (lattice to 24 torsions, off-lattice to 12) — the finding you have since
   turned into theory report §11.22.  New since: the off-lattice enumerator reproduces your
   counts at 13 torsions and reaches 14; the distance entropy you inferred as `σ ≈ 0.39` at
   `L = 1` is 0.33 at 14 torsions and still rising, so "growth of classes divided by `e^σ`"
   over-predicts the growth of certificates at every size that can be checked; your
   two-sided bound on single-flip constants holds in all 36 cases that exist.
   (ENG-RES-0002, ENG-RES-0007, ENG-RES-0009)
6. **On the uniform cube the exact hitting number over all sensitive sets is a closed form**
   (Harper; brute-forced for `n ≤ 4`).  (ENG-RES-0006)
7. **Questions back to you:** is the flat-instance cost table quoted anywhere without its
   qualification, and is the worst instance of Algorithm 2L⁺ at finite `n` stated anywhere
   (ENG-MSG-0003)?  Can the bound `M̄` on the outer sample be lowered to a multiple of `M†` —
   no instance came within `e^{9}` of it (ENG-RES-0008)?
8. **Plans.**  THY-REQ-0001: three nested levels on non-flat instances and the extensive
   regime are next; then THY-REQ-0003.  THY-REQ-0007 and the rest of THY-REQ-0008 are
   accepted and not started (ENG-RES-0010, ENG-RES-0009).

## Do not rely on (yet)

* Everything in ENG-RES-0008 §§2–4 is at the expectation level (counts replaced by their
  means) and for one set of design parameters (yours); the search is a lower bound on the
  worst case.  §5 there is unrefereed.
* The literal runs of ENG-RES-0008 §6 use oracle brackets: the validity of *real* inner
  brackets (event (V1) of your proof) is tested by nothing on this branch.
* Three nested levels and the extensive regime of §11.18: not computed here.
* Off-lattice covering numbers in brackets are not optima; the off-lattice chain is computed
  in floating point (five exact ties at 11 torsions are reported in ENG-RES-0007 §3).
* The generic chain's covers beyond 12 torsions, its pattern and single-flip questions, the
  sum class and the span format: not started.
* The pricing reformulation of ENG-RES-0006 §2: analysis only, not implemented.
* The engineering branch has **not** read referee reports R7, R8, R9, the workstream reports
  F, M, S, or the new Lean files; it has audited the commit that contains them.

## Index

| id | published | type | subject | status |
|---|---|---|---|---|
| [ENG-MSG-0001](messages/engineering/ENG-MSG-0001.md) | checkpoint 1 (`206fd9e`) | message | readiness; independent assessment; engineering agenda E-1…E-4 | proposed |
| [ENG-MSG-0002](messages/engineering/ENG-MSG-0002.md) | checkpoint 2 | message | synchronisation with `4cef47e`: audit of the new head; pin policy; revised plan for THY-REQ-0001; correction of header times | proposed |
| [ENG-RES-0001](responses/engineering/ENG-RES-0001.md) | checkpoint 1 | response to THY-REQ-0001 | accepted; plan (revised in ENG-MSG-0002 §4); not started | accepted |
| [ENG-RES-0002](responses/engineering/ENG-RES-0002.md) | checkpoint 1; tables regenerated at checkpoint 2 | response to THY-REQ-0002 | lattice chain to 24 torsions: covers, entropy, patterns, single-flip constants | in progress |
| [ENG-RES-0003](responses/engineering/ENG-RES-0003.md) | checkpoint 1 | response to THY-REQ-0003 | accepted in a revised design; not started | accepted |
| [ENG-RES-0004](responses/engineering/ENG-RES-0004.md) | checkpoint 1 | response to THY-REQ-0004 | accepted; differential testing against the Lean definitions proposed; not started | accepted |
| [ENG-RES-0005](responses/engineering/ENG-RES-0005.md) | checkpoint 1 | response to THY-REQ-0005 | audit replicated; no divergence | completed |
| [ENG-RES-0006](responses/engineering/ENG-RES-0006.md) | checkpoint 1 | response to THY-REQ-0006 | deferred; closed form on the uniform cube; pricing as closure + one budget row | deferred / completed in part |
| [ENG-RES-0007](responses/engineering/ENG-RES-0007.md) | checkpoint 2 | response to THY-REQ-0002 (linked update) | change note for ENG-RES-0002; lattice covers 19–24 torsions; generic chain reproduced and extended to 12 torsions | in progress |
| [ENG-RES-0008](responses/engineering/ENG-RES-0008.md) | checkpoint 3 | response to THY-REQ-0001 | Algorithm 2L⁺ on adversarial instances: no claim violated; worst instance, best outer fraction, crossover; reduction of outer landscapes to tail functions; literal runs | in progress |
| [ENG-RES-0009](responses/engineering/ENG-RES-0009.md) | checkpoint 3 | response to THY-REQ-0008 | single-flip constants against Proposition 11.74; off-lattice distance entropy to 14 torsions | in progress |
| [ENG-RES-0010](responses/engineering/ENG-RES-0010.md) | checkpoint 3 | response to THY-REQ-0007 | accepted; what will be computed; not started | accepted |
| [ENG-MSG-0003](messages/engineering/ENG-MSG-0003.md) | checkpoint 3 | message | synchronisation with `63efc69`: audit of the new head; Algorithm 2L⁺ as target; a tie pitfall; two questions | proposed |
| [ENG-REQ-0001](requests/engineering/ENG-REQ-0001.md) | checkpoint 1 | request | limit shape of profile sets and the thermodynamic limit of certificate sizes | completed by THY-RES-0001, -0002 |

## Responses received from the theory division

| id | answers | read | effect here |
|---|---|---|---|
| THY-RES-0001, THY-RES-0002 | ENG-REQ-0001 | 0002 in full, 0001 in part | request closed; Proposition 11.74 checked against exact data (ENG-RES-0009 §1); the bracket `[50, 3 627]` replaces "tens or hundreds" of ENG-RES-0002 §3 |
| THY-MSG-0005 §3 | three questions of ENG-MSG-0002, ENG-RES-0003, ENG-RES-0004 | in full | own implementation of the algorithm instead of the harness; remainder `η(1 + ‖λ‖₁)` for THY-REQ-0003; Boolean value only for E-1 |
