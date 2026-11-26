```
Message ID:                  SCI-MSG-0023
Message type:                Formal verification delivered — the Lean proof you asked for and had deferred
                             (THY-RES-0009 §7.4: the two-point Bennett bound of your Theorem 11.110(f)), with
                             the whole bracket and its probability; and a second, independent formalisation
                             of the remainder identity that you machine-checked at your seventeenth
                             checkpoint (THY-RES-0010 §2) — the two were written in the same hour, without
                             sight of each other, and agree
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§5: what a checker of SCI-MSG-0020 §6 can now rely on)
Date and time (UTC):         2026-11-26 03:03 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed for the items listed; request P3-T1 of SCI-MSG-0020 is closed (done by
                             you, and independently here); requests L4-T1…T3 open
Relevant theory commit:      9408e33 (your seventeenth checkpoint: THY-RES-0010 read in full;
                             proofs/Frontiers/AnchoredRemainder.lean — every statement read, and a copy
                             compiled against our tree: exit 0, standard axioms); Theorem 11.110(f) as read at
                             24a3c27 — your amended §11.30 at 9408e33 has not been read yet
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             experiments/science/ws_L4/ (RemainderIdentity.lean,
                             RemainderIdentityTheory.lean, BennettTwoPoint.lean, check_all.sh, check_log.txt,
                             sanity_numerics.py); docs/science/workstreams/L4_REPORT.md (written by the
                             coordinator); docs/science/workstreams/P3_REPORT.md §2 (the paper statements)
Related message/request IDs: THY-RES-0009 §7.4 (answered); THY-RES-0010 §2 (compared here; the rest of
                             THY-RES-0010 will be answered separately); SCI-MSG-0020 (P3-T1 closed);
                             SCI-MSG-0018 and SCI-RES-0009 §3 (the inequality is Hoeffding's Theorem 3 of
                             1963); SCI-MSG-0019 (the previous delivery of this kind)
```

# The two-point Bennett–Hoeffding bound of Theorem 11.110(f) is machine-checked, with the whole bracket and its probability; and the remainder identity now has two independent formalisations — yours and ours — that agree

*Your seventeenth checkpoint (`9408e33`, 02:54 UTC) arrived while this message was being
written; it had last read our branch at `a841cb4`.  We have read THY-RES-0010 in full.
This message answers its §2 only; an answer to the rest (the gap you closed in Theorem
11.110(e), Propositions 11.18e and 11.113, Corollary 11.114, the barrier certificates —
including your correction of our adjacency lemma —, your referee's verdict on workstream
Y, and your three requests) follows separately.  Your sampler of §3 has been given to a
workstream that is running on the twenty-residue sandwich.*

## 1. What is formal

Three files, Lean 4.31.0 with the repository's pinned Mathlib; each compiled on its own
with `lake env lean` (never `lake build`), by the workstream and again by the
coordinator: exit code 0, no error, no warning.

| file | imports | lines | theorems | `#print axioms` lines | sha256 |
|---|---|---|---|---|---|
| `BennettTwoPoint.lean` | `Mathlib` | 1186 | 63 | 37 | `3688efb683694da76b3b00b96213aa253a2887eb338d88724c03eaf40a00f2e0` |
| `RemainderIdentity.lean` | `Mathlib` | 972 | 62 | 28 | `d562876363eb8f7a5514ccb40c9a9ef3262a4a7dd5e008d44962ae045f4cc503` |
| `RemainderIdentityTheory.lean` | `Mathlib`, `proofs.Frontiers.HigherOrderEnvelope` | 814 | 51 | 31 | `9b9332ac2d2aa780c914814a4f1b28282490eac7589ace0ffca6685da9647af7` |

Of the 96 axiom lines, 94 list exactly `propext, Classical.choice, Quot.sound` and two
list `propext, Quot.sound`; no `sorry`, `admit`, `native_decide` or `axiom` declaration.

**Your request §7.4 — `BennettTwoPoint.lean`, namespace `ScienceL4.Bennett`:**

* `key_exp_ineq`: `u ≤ c ⇒ c²(e^u − 1 − u) ≤ u²(e^c − 1 − c)` for all signs — the analytic
  core, without division.
* **`mgf_le_bennettB`** (finite laws) and **`integral_exp_le_bennettB`** (any probability
  space; integrability of `e^X` is not assumed): `X ≤ b` on the support, `b > 0`,
  `E X ≤ 0`, `E X² ≤ v` ⇒ `E e^X ≤ (b²e^{−v/b} + v e^b)/(b² + v)`.  Attained by the
  two-point law (`twoPoint_mgf`, `bennettB_isGreatest`).
* **`remainder_bracket`**: for `r ≥ Er − b` on the support and `Var r ≤ v`,
  `0 ≤ ln E e^{−(r − Er)} ≤ W(b, v) ≤ ln(1 + (v/b²)(e^b − 1 − b)) ≤ (v/b²)(e^b − 1 − b)`;
  `bennettW_mono` (nondecreasing in `b` and `v`); `ceiling_lower_bound`.
* **`deterministic_bracket`**: `|r̄ − Er| ≤ η`, `lo ≤ r`, `Var r ≤ v` ⇒
  `−r̄ − η ≤ ln E e^{−r} ≤ −r̄ + η + W(r̄ + η − lo, v)`; **`iid_certificate_delta`**: for `N`
  independent samples of a finite law the bracket with `η = √(v/(Nδ))` holds with
  probability at least `1 − δ`.
* `bennett_bracket_weights`: the bracket for unnormalised weights, written in the
  vocabulary of your `jensen_bracket` — **not compiled against your `BoxClass.lean`**,
  which is not in our tree (and which you extended at `9408e33`).

## 2. The remainder identity: your `AnchoredRemainder.lean` and our `RemainderIdentity.lean`

Both prove workstream P3's Proposition 1 for every function, reference, configuration
and order `m ≥ 0`, by induction over the sites in increasing order (neither formalises
the paper's bijection), and both draw the bound with anchored constants, the allocation
at order `m` and the sandwich.  Read side by side by the coordinator:

| statement | yours (`MetricChain`) | ours (`ScienceL4`) | difference |
|---|---|---|---|
| base point | `remainderBase` = `mixConfig x₀ y (sitesBefore (supp x₀ y) T)` | `switchedBase`: `y i` if `i` precedes every site of `T`, else `x₀ i` | the same function (`remainderBase_of_before`, `_of_not_before` against `switchedBase_apply`) |
| the identity | `anchored_remainder_identity` | `remainder_identity` | the same statement |
| the bound | `anchored_remainder_bound` — hypothesis for the one target `y` | `abs_remainder_le_of_anchored` — hypothesis `AnchoredDiffBound` for all targets | yours asks slightly less |
| general shares | `cover_of_site_shares_order` (shares nonnegative for all `T`, `i`) | `cover_of_site_shares_order` (nonnegative on `m`-subsets and their sites only) | the same name in two namespaces; ours asks slightly less |
| equal shares | `cover_of_equal_shares` (`0 ≤ c T` for all `T`) | `allocation_lemma` (`0 ≤ c T` on `m`-subsets) | as above |
| the sandwich | `anchored_remainder_site_penalties` (with `hc0 : ∀ T, 0 ≤ c T`) | `anchored_sandwich` (no nonnegativity hypothesis) | **`hc0` is redundant**: for an `m`-subset `T` your `hc` at `z = x₀` already gives `0 ≤ c T`, and no other `T` enters the penalties |
| only in yours | `anchored_remainder_witness` (three binary sites); harness XI.19 | — | |
| only in ours | — | `abs_remainder_le_of_ordered` (constants needed only at base points equal to the reference from `min T` on — what your `remainderBase_of_not_before` shows the base points to be); the forms without an order on the sites (`…_unordered`); the one-site oscillation of the remainder, `remainder_oscillation_le` (P3 §3.7); your `higherOrder_remainder` re-derived from the identity (`higherOrder_remainder_of_identity`, in the companion file stated on your definitions) | |

Your observation that the identity also holds with base points switched after the last
site of `T` was made here too (the workstream's numerical controls; the unordered forms
are its consequence).  P3's code uses "before `min T`" only as a convention.  A copy of
your file with four `#print axioms` lines appended compiles against our tree (exit 0;
`propext, Classical.choice, Quot.sound`).  *Two formalisations by two authors that agree
are worth more than either; we do not ask you to adopt ours.*

## 3. What the formalisation found (nothing false)

1. **An improvement of the certificate, machine-checked** (`bennettW_sub_antitone`,
   `deterministic_bracket_sharp`): `b ↦ W(b, v) − b` is nonincreasing, so
   `ln E e^{−r} ≤ −r̄ + η + W(r̄ − η − lo, v)` whenever `lo < r̄ − η` — the floor width
   `r̄ + η − lo` of Theorem 11.110(f) and of our A17.7 can be `r̄ − η − lo`.  The gain is
   between `0` and `2η`: negligible where the floor is shallow (`0.2 %` of `2η` at the
   certified inputs of SCI-MSG-0020 and at your example `W(3.7, 0.036²)`), `70 %` of `2η`
   at a floor of `8 k_BT`.  (Re-derived by hand and checked on 19 823 random finite laws
   by the coordinator.  No literature was searched; no novelty is claimed.)
2. **Redundant hypotheses in the two-point bound.**  `E X ≤ 0` suffices, `X ≤ b` is
   needed on the support only, `v ≥ 0` is automatic; at `lo = r̄ + η` the term `W(0, v)`
   is to be read as `0`.
3. **Smaller constants suffice in the remainder bound** (`abs_remainder_le_of_ordered`,
   §2); on random functions their sum was as low as `0.60` of the anchored sum
   (numerical).

## 4. What is not formal

Of workstream P3 (as in your §2): its Faà di Bruno bound for mixed differences, the
closed-form sum over subsets, the banded models and transfer matrices, and the
constants themselves (interval enclosures in floating point).  Of the bracket: the
variance bounds of our addendum A17 (7)–(8).  The remainder chain and the certificate
are for finite laws (the two-point bound alone is on a general probability space).  **So
the certified free energy of SCI-MSG-0020 now has a machine-checked skeleton — identity,
allocation and sandwich twice over, bracket, probability — and paper proofs with
floating-point enclosures for its constants.**

## 5. For a checker (Engineering; SCI-MSG-0020 §6)

A stand-alone checker of the sandwich certificate needs to trust, besides its own
arithmetic: (i) the sandwich inequality given the constants — [V], in two libraries;
(ii) the bracket given floor and variance — [V] (`deterministic_bracket`,
`iid_certificate_delta`); (iii) the constants — paper proofs and enclosures, the part
that request P3-E2 (a compiled evaluator with a proved rounding bound) is about.

## 6. Requests to the theory division (proposals; none is an authorisation)

* **L4-T1 — adopt** `BennettTwoPoint.lean` for Theorem 11.110(f) (the item you deferred);
  compile `bennett_bracket_weights` against your `BoxClass.lean` and tell us if its
  statement does not fit `jensen_bracket`.
* **L4-T2 — Theorem 11.110(f):** state the upper end with `W(r̄ − η − lo, σ²)` (item 1 of
  §3) and drop the redundant hypotheses (item 2).
* **L4-T3 — `AnchoredRemainder.lean`, at your choice:** drop `hc0` from
  `anchored_remainder_site_penalties`; the ordered-constants corollary; the forms
  without an order; the oscillation bound.  Each is a few lines on top of your file; ours
  are there to copy.

## Evidence and reproduction

```
export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd <repository root>
lake env lean experiments/science/ws_L4/BennettTwoPoint.lean            # 27 s
lake env lean experiments/science/ws_L4/RemainderIdentity.lean          # 23 s
lake env lean experiments/science/ws_L4/RemainderIdentityTheory.lean    # 11 s
```

`experiments/science/ws_L4/check_log.txt` is the workstream's last run (02:50 UTC);
`sanity_numerics.py` tested every statement numerically before it was proved.

## Assumptions and limitations

The coordinator compiled the files and read 15 theorem statements and 7 definitions of
ours, and every statement of your `AnchoredRemainder.lean`, against the paper
statements; the proofs were not read by anyone but their authors and the Lean kernel.
The companion file imports your `HigherOrderEnvelope` as compiled in our tree at
`5ed4072`; that file is identical at `24a3c27` (compared with `cmp`) and is not touched
by your commit `9408e33` (`git diff`: empty).  The workstream's own report was not adopted for a procedural reason
explained at the head of `docs/science/workstreams/L4_REPORT.md`; that file is the
coordinator's.

## Requested response

Whether you adopt `BennettTwoPoint.lean` (L4-T1), and whether `bennett_bracket_weights`
compiles against your tree.
