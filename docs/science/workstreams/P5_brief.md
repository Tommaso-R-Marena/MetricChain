# Workstream P5 (launched at checkpoint 43, 2026-11-26 02:20 UTC) — the compact case: a certified bound that sees the cancellation between self and cross terms

> **Finished 2026-11-26: report `P5_REPORT.md`, published as SCI-MSG-0024.**  The brief below is kept as launched.

*Brief written by the coordinator at checkpoint 42 (2026-11-26).  It was held back while
four workstreams were running and launched, unchanged, when the first of them (R10) had
reported.  If its agent is gone, its notes and draft are in `experiments/science/ws_P5/`
and `P5_REPORT.md`.  Read
`COMMON.md` first (pins out of date), then `P3_REPORT.md` in full — this workstream
starts where P3 stops.*

## Why — the problem the physical line of the division ends on (`OPEN_PROBLEMS.md` D6)

Workstream P3 certified `ln Z` of a twenty-residue apolar peptide on an extended backbone
(`3.5·10⁹` rotamer assignments) within 0.06 nats without sampling: it evaluates the GBn2
solvent term on a Hamming ball about an anchor and bounds the tail of order `m` term by
term (SCI-MSG-0020).  **On the helix this fails at every affordable order** (Leu₁₆:
`Γ₃ … Γ₆ = 1 819, 370, 60, 8.0` kcal/mol), although the coordinator's fitted chain models
show that the *true* remainder there is as small as anywhere (`0.002–0.004 k_BT` at twenty
and thirty residues; addendum A17 (10)): **the price is small and the proof is
missing.**  P3 identified the cause (its §2.8, §3.2): the cross term of the
generalised-Born energy is a sum over all atom pairs inside the range of the kernel with
charges of both signs, which cancels to about one per cent against the self term
(Val₆: −640 and +600, total −37 kcal/mol); a bound that treats atom pairs one at a time
cannot see the cancellation and is 250–800 times too large at every order, while term
by term it is within a factor 1.1–6 of exact.

## The question

**Is there a certified bound on the order-`m` tail of the GBn2 energy in rotamer
variables that is within a small factor (say ten) of the truth in a compact geometry —
or a proof that no bound of a stated, natural kind can be?**  Either answer is a result.

## Candidate route (P3's "next step 1"; nothing here has been tried)

*Group-wise signed tails.*  For each atom `p` and each rigid neutral group `Q` (a
backbone peptide unit; a side chain in a given rotamer) evaluate the kernel sums
`Σ_{q∈Q} q_q ∂_w^k h(ℓ̄_p + ℓ̄_q; r_pq)` **with their signs** at reference Born radii `ℓ̄`,
and bound only the deviation from the reference term by term.  Each exact order in the
deviation should gain one power of the small parameter (the relative change of a Born
radius under one rotamer flip: 0.27 for GBn2 with the neck correction, 0.06 without,
0.15 for OBC2 at Val₆ on the strand).  Things to settle first, in this order:
1. *Is the cancellation there at the order that matters?*  Measure, by enumeration on
   P3's helix instances (Leu₆, Leu₈, Ser₄–Ser₆ on the helix), the exact anchored
   constants `c_T^anch` of order 3–5 for the self part, the cross part and their sum, and
   the same after grouping the cross part by neutral groups.  If the group sums are
   already 10–100 times smaller than the pair-by-pair sums of absolute values, the route
   is alive.
2. *A lower bound for pair-by-pair bounds.*  Formalise "a bound that treats atom pairs
   one at a time" (e.g. any bound of the form `Σ_{p<q} |q_pq_q|·B_pq` with `B_pq` depending
   on the pair's own geometry and radii ranges only) and show on an explicit family (two
   neutral dipoles at distance `R`) that it must exceed the truth by a factor growing
   with the number of pairs inside the kernel's range.  This would make P3's negative
   finding a theorem.
3. *The signed bound.*  First-order response in the Born radii exact (with signs),
   second order term by term; interval enclosures as in P3's `encl.py`; the sum over all
   `m`-subsets in closed form if the structure of P3's Proposition 4 survives (it uses
   non-negativity of the terms — signed sums will need a different organisation, e.g.
   sums over groups of elementary symmetric polynomials of signed group moments).
4. *Validation*: every inequality against exact enumeration at every state of every
   enumerated instance, as P3 did; then one helix instance beyond enumeration, with the
   coordinator's fitted chain estimate (`beyond_enumeration_fit.py L H 4 …`) as an
   independent check of the value.

## What is available

`experiments/science/ws_P3/` (read-only: `p3core.py` — evaluator with self/cross split and
descreening tables; `encl.py` — interval enclosures of derivatives; `gfbound.py` — the
anchored bound summed over subsets; `run_floor.py` — the end-to-end pipeline with
enumeration checks); `experiments/science/ws_P2/` (geometry, domains, tables of the vacuum
part); `experiments/science/pi_inference/beyond_enumeration_*.py` (chain models, exact
sampling); the theory division's Theorem 11.18a and Proposition 11.18b at `24a3c27`
(pair-form penalties; share certificates) and workstream P4's test of them.

## Rules

As in the P3 brief: model-relative statements only; fixed synthetic homopeptides and the
one patterned sequence of P2; no sequence is varied or optimised; write only in
`experiments/science/ws_P5/` and `docs/science/workstreams/P5_REPORT.md`; no
state-changing git; every inequality that is claimed as a bound is checked against
enumeration at every state where a domain can be enumerated; logs only from runs that
reached their last line; a negative result with its reason is a result.
