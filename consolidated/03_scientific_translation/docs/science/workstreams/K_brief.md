# Workstream K — certified kinetics: barriers, rates and the third semiring

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_K/`; your report: `docs/science/workstreams/SK_REPORT.md`
(named `SK` because the theory division already has a `K_REPORT.md`).

## Motivation

MetricChain certifies two kinds of quantities: minimum energies (the `(min,+)` semiring) and
partition functions (the `(+,×)` semiring) — both *equilibrium, static* quantities.  The
primary experimental signatures of conformational landscapes are often *kinetic*: exchange
rates, folding and unfolding times, relaxation spectra.  And the basic object of
energy-landscape theory — the disconnectivity graph (the merge tree of the energy function:
which minima are connected below which energy) — lives in a third algebra, `(min,max)`
(bottleneck / minimax paths).  Neither of the other divisions has touched kinetics or
barriers.  A computed barrier or rate today comes with no certificate that a lower pathway
does not exist.  Your question: **what can be certified about barriers and rates, with which
certificates, at what cost, and does the existing machinery (envelope classes, the verified
min-kernels and Z-kernels) already suffice?**

The coordinator's starting observations (unverified sketches — check, correct, extend, or
replace them):

1. *Barrier lower bounds are cut certificates.*  For a graph on the configuration space
   (e.g. single-site moves on a product space) and energy `E`, the minimax barrier
   `B(a,b) = min_{paths a→b} max_{x on path} E(x)` satisfies `B(a,b) ≥ t` iff there is a set
   `S ∋ a`, `b ∉ S`, such that every vertex of its boundary (inner or outer, depending on the
   convention) has `E ≥ t`.  So a barrier lower bound is a *minimisation* certificate over a
   separating surface: the `(min,max)` problem reduces to the `(min,+)` kernel on a
   constrained set.  Which cuts keep the constrained minimisation pairwise-decomposable
   when `E` is pairwise (coordinate cuts; cuts defined by a linear or counting statistic —
   "number of native contacts = q" needs a counting constraint: tree-decomposable?)?
2. *Robust barriers under an envelope class.*  With `E = f + g`, `g(x) − g(y) ≤ d(x,y)`: since
   `x ↦ d(x,a)` and `x ↦ −d(a,x)` are admissible, the barrier **height above the basin `a`**,
   `B_g(a,b) − E_g(a)`, should range exactly over
   `[ B_{f − d(a,·)}(a,b) − f(a),  B_{f + d(·,a)}(a,b) − f(a) ]` — the analogue of the contact-set
   and sharp-minimum theorems (theory report §2.3) one semiring further.  True?  With
   anchors?  For the *saddle energy* itself the range is `[B_{f+L}, B_{f+U}]` by monotonicity.
   What is the query complexity of certifying a barrier (the analogue of "certificates are
   coverings", §11.2)?  Is there a persistent-homology statement (the stability theorem
   gives `2‖g‖_∞`; envelope classes should give position-dependent, sharper bounds)?
3. *Finite temperature: rates from partition functions.*  For a reversible Markov chain with
   stationary law `π ∝ e^{−βE}` (Metropolis or heat-bath single-site dynamics on a product
   space): (i) the escape rate from a set `A` started from its quasi-stationary law is
   `λ_A ≤ Q(A,A^c)/π(A)` (Dirichlet form of the indicator) — so an *upper* bound on a
   boundary partition function and a *lower* bound on `Z(A)` certify a **lower bound on a
   mean exit time** ("certified kinetic trap"); (ii) the spectral gap is at most
   `Q(A,A^c)/(π(A)π(A^c))`; (iii) capacities have two variational principles — Dirichlet
   (test functions give upper bounds) and Thomson (test flows give lower bounds), and mean
   hitting times are ratios of such sums (Bovier–den Hollander's potential-theoretic
   approach to metastability) — which of these become checkable certificates with the
   existing Z-kernel, and for which families of test functions / flows on product spaces
   are the sums tractable (functions of a low-dimensional reaction coordinate; product
   flows)?  (iv) what does envelope uncertainty in `E` do to these bounds (rates are
   exponentially sensitive: quantify)?
4. *Which kinetic statement is physically meaningful* for a chain molecule, given that the
   certified object is a discrete-state Markov model with a chosen move set, not Newtonian
   or Langevin dynamics?  Transition-state theory gives rigorous upper bounds on rates for
   classical dynamics; what is the honest statement here?

## What to deliver

* Precise theorems with proofs for whatever of 1–3 is true (and counterexamples for what is
  not); the exact statement of what a "barrier certificate" and a "rate certificate" are
  (certificate format, checker, soundness statement), in a form the theory division could
  formalise in Lean next to `proofs/CertificateAlgebra.lean` (read its top-level soundness
  theorems first so that your formats compose with the existing kernels).
* Numerics: exact computations on small systems (product landscapes; an Ising chain; a short
  lattice or bead chain) that test every theorem, including the tightness of the variational
  bounds against exact spectral gaps / mean first-passage times from linear algebra.
* Prior art (search log): disconnectivity graphs and their computation (Becker–Karplus;
  Wales); lower bounds on barriers / "certified transition states"; minimax path duality;
  merge trees and persistence stability (Cohen-Steiner–Edelsbrunner–Harer) with Lipschitz
  rather than sup-norm perturbations; potential-theoretic metastability (Bovier, Eckhoff,
  Gayrard, Klein; Bovier–den Hollander); Cheeger / conductance bounds; canonical paths;
  variational transition-state theory; Markov-state-model error bounds; any existing
  *certified* or *verified* rate bounds.  Classify what is known, what is a new combination,
  what might be new.
* An assessment: is "certified kinetics" a real new capability for the programme, or a
  relabelling of classical variational principles?  What is the one experiment-facing
  statement it could support that current practice cannot?
