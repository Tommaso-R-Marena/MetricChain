# Workstream P3 — a floor by analysis: certified class constants of a real solvation term, and a certified `ln Z` beyond enumeration size

*Brief written by the coordinator after checkpoint 33 (2026-11-25).  Read `COMMON.md` first
(its commit pins are out of date: theory is now at `658b77f`, a read-only export of that
tree is `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`;
`git show 658b77f:<path>` also works).*

## Why this workstream exists

Workstream P2 (`docs/science/workstreams/P2_REPORT.md`, code in `experiments/science/ws_P2/`,
published as `docs/collaboration/messages/science/SCI-MSG-0015.md`) measured, by exact
enumeration, the class constants of the GBn2 polarisation energy against the ff14SB known
part in *rotamer variables on a fixed backbone*: third-order constants `c_ijk` of
`0.003–0.2 kcal/mol` for neutral side chains; a third-order certificate that is exact in
every enumerated instance.  **Every one of those constants was obtained by enumerating all
states — which is what a certificate is supposed to avoid.**  P2's own next step 2 (its §6)
names the missing piece: *a proved bound on the third-order constants of GB*, from the
fact that the descreening integral of every atom is exactly a sum of one-site (backbone
atoms) or one- and two-site (side-chain atoms) tables, the tables `fbmodel.py` builds.

The theory division has now asked exactly this.  In THY-RES-0007 §4
(`docs/collaboration/responses/theory/THY-RES-0007.md` in the export) it previews a theorem
for *box classes* `lo ≤ g − ĝ ≤ hi` around a known function `ĝ` whose Gibbs measure can be
sampled exactly (statements (a)–(e) are listed in `docs/RESEARCH_LOG.md` of the export,
"Resume here", item 1): the number of evaluations needed to certify `ln Z` within `ε` is
`Θ((Z(lo)/Z(g) − 1)/ε)` — the Boltzmann factor of the free-energy distance from the true
energy to the *floor* of the class; "what must be certified is the floor, and nothing
else can replace it".  Its question to us: **"is a floor certifiable by analysis for the
remainder you measured (a lower bound of a generalised-Born term minus its pair-additive
fit)?"**

## What I want, in order

1. **A theorem with a recipe.**  For the GBn2 polarisation term *exactly as OpenMM 8.6.1
   computes it* (P2 re-implemented it in `fbmodel.py` and validated it against OpenMM;
   re-use or re-write, but validate against OpenMM yourself on fresh states), on a fixed
   backbone with one rotamer variable per residue: a rigorous upper bound on
   (a) the third-order interaction constants `c_ijk` (mixed third differences over three
   sites, the other sites arbitrary), (b) the sup norm of the remainder of `g_GB` beyond
   its best — or a specified, computable — pairwise approximation, on both sides
   (`lo ≤ g_GB − ĝ₂ ≤ hi`), **computed without enumerating joint states** (cost polynomial
   in the number of sites: tables, ranges, interval arithmetic, derivative bounds —
   your choice; say what each step costs).  Every inequality proved; every place where
   floating point enters either outward-rounded or given an explicit error budget; the
   tabulated "neck" correction and the `tanh` rescaling treated honestly (if a derivative
   bound of a tabulated function is needed, say how it is obtained).  If the bound must
   assume something (e.g. no two atoms closer than a stated distance on the rotamer
   grid), state it as a checkable hypothesis and check it.
2. **How tight?**  Evaluate the bound on P2's instances (its 140 model peptides or a
   representative subset covering apolar, polar, charged; lengths 3–9) and compare with
   the enumerated constants (`experiments/science/ws_P2/out/`, tables in the report §3.4):
   ratio certified/measured per class of side chain.  A bound that is 100 times too
   large is a negative result and must be reported as such, with the reason (which
   cancellation the analysis loses).
3. **What the floor buys — the theory division's formula with your numbers.**  With
   certified constants, P2's pairwise lower model (its Statement 5(d); the theory
   division states it as: for constants `c_T`, `|T| = 3`, and `γ_i = ⅓ Σ_{T∋i} c_T`, the
   function `f + I₂g − Σ_i γ_i[x_i ≠ x_i⁰]` is a pairwise lower bound of the energy) is a
   *certified floor that is a function*, not a constant.  Compute for it
   `ρ = sup(g − m)` and — where enumeration is still possible — the exact cost number
   `Z(m)/Z(g) − 1` of the theory division's formula, in units of `k_BT` at 300 K.  How do
   they grow with chain length for apolar, polar, charged side chains?  At which length
   does certification by sampling from the lower model become cheaper than enumeration,
   and at which length does it become impossible (`e^{ρ}` too large)?
4. **One instance beyond enumeration, end to end, if (3) says it is feasible** (e.g. an
   apolar homopeptide of 14–30 residues on a fixed backbone — a *fixed synthetic
   sequence*): (i) certified constants by your recipe; (ii) the pairwise lower model `m`
   and the exact `Z(m)` and exact samples from `π_m` (transfer matrix / junction tree if
   the pair graph is banded once pairs beyond a range are bounded and moved into the
   remainder — say what you did with them, rigorously); (iii) `N` evaluations of the true
   energy at samples of `π_m`; (iv) a **valid** two-sided confidence bracket for
   `ln Z(g) = ln Z(m) + ln E_{π_m} e^{−(g−m)}` with stated `δ` (the variable is in
   `[e^{−ρ}, 1]`; use a bound that is valid at every `N` — Hoeffding, empirical Bernstein,
   Bentkus, a betting bound — not a normal approximation; the theory division's own
   harness documents "mean plus two standard errors" as *not* a certificate); (v) the
   Gibbs–Bogoliubov side for comparison.  Report the bracket, `N`, wall time, and what
   remains assumed (the force-field model itself; the rotamer grid; the fixed backbone).
   If it is not feasible, say precisely which number makes it infeasible.
5. **Optional, if time remains.**  (a) The coordinator is writing an addendum (A17) which
   says that a certified bound on a *moment* `E_π e^{−p(g−ĝ)}` (`p > 1`) can replace the
   floor at cost `e^{D_p}/ε^{p/(p−1)}`, `D_p` the Rényi divergence bound; for a product
   reference measure and a remainder with certified one-site oscillations `c_i` this
   gives `D_2 ≤ Σ_i c_i²/2`.  Report `Σ_i c_i²` (in `(k_BT)²`) for the certified remainder
   of your instances, so that the two routes can be compared.  (b) The same analysis for
   a second implicit-solvent model available in OpenMM (OBC2), to see whether anything
   depends on the neck correction.

## Scope (hard)

Fixed synthetic sequences only (homopeptides and the model peptides of P2); no sequence
optimisation, no design, no target; nothing about biological function.  The object is the
*energy function as a mathematical object* and what can be certified about it.

## Rules

Write only in `experiments/science/ws_P3/` (create it) and `docs/science/workstreams/P3_REPORT.md`.
You may read and import from `experiments/science/ws_P2/` but not modify it.  No
state-changing git command.  OpenMM 8.6.1 is installed (`import openmm`); 4 cores shared
with other workstreams and with a long Lean build — keep single computations under about
20 minutes.  Keep `experiments/science/ws_P3/NOTES.md` from the first minute.  Labels: [P]
proved here, [M] measured, [N] numerical, [K] known with reading level, [C], [H].  The
report starts with "How far I got" and "Verdicts in one paragraph" and ends with "What I
did not check".  Prior art: P2's §4 has a search log (LUTE; provable ε-approximations of
partition functions in protein design; pairwise GB) — extend it only where your new
statements need it (rigorous bounds on Born radii or on the many-body part of GB;
interval arithmetic on implicit-solvent energies), with reading levels, never a citation
you did not open.
