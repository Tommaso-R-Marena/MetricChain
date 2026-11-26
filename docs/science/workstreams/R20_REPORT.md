# R20 — adversarial reading of the Complexity division's first result: hardness of multi-stranded folding in the nearest-neighbour model (their Theorems 1 and 3)

*Workstream R20 of the science division, 2026-11-26.  **This is an internal review by one agent, not external peer review.***

Object: `docs/complexity/STRANDS_NN_HARDNESS.md` (263 lines, sha256 `47af0dcb…7691fe`; "the note") and
`docs/collaboration/messages/complexity/COMPLEXITY-MSG-0001.md`, branch `research/biological-complexity`, commit `fc4b238`, read from
the read-only export `<CX>`; their code in `<CX>/experiments/complexity/strands/`.  "l.N" = line N of the note.
Notes of this workstream: `experiments/science/ws_R20/NOTES.md`.  Everything here is combinatorics of an abstract model on synthetic
strings (a packing reduction); no sequence was designed, optimised or evaluated for any purpose.
The branch moved to `22cf1a6` while I worked (coordinator's note, received between 17:45 and 17:47 UTC by my clock): §§1–4 of the note, with Theorems 1 and 3, are unchanged
there; this review is of the version at `fc4b238`, whose line numbers it uses; §2.5 has one paragraph on the new text.

Four kinds of checking are kept apart: **review** = I re-derived the step on paper; **replication** = I recomputed with my own
code, written and frozen (sha256 in the notes) before I opened theirs; **re-run** = their code, unmodified, from a scratch copy;
**read only**.  Labels: [P] paper proof (mine unless attributed), [K] known and cited with the reading level — `[full text]`,
`[sections read]`, `[page text]`, `[fetch-tool summary]`, `[search summary]`, `[from memory — unverified]` —, [N] numerical only,
[C] conjecture.

Sources (URLs and what was read: §5): **[DSW]** Ducloz–Shalaby–Woods, arXiv:2506.19756v1, the full version of their DNA 31 paper
`[full text]`; **[CHT]** Condon–Hajiaghayi–Thachuk, DNA 27 `[sections read]`; **[SW25]** Shalaby–Woods, ICALP 2025
`[sections read]`; **[SW26]** Shalaby–Woods, arXiv:2611.27945v2 `[sections read]`; **[D07]** Dirks et al., SIAM Review 2007
`[sections read]`; **[NNDB]** Nearest Neighbor Database, RNA 2004 rules: bulge page `[page text]`, coaxial-stacking page
`[fetch-tool summary]`.  Not opened: **[L04]** Lyngsø, ICALP 2004 (the publisher's link answered with a script challenge; not worked
around); **[GJ]** Garey–Johnson 1979.

---

## 0. Verdict in ten lines

1. **Theorem 1 is proved as stated.**  Review: every step re-derived, no gap (§2.1).  Replication: 0 violations of its three
   statements on 74 instances (42 solvable, 32 not), 12.6 million structures enumerated over all strand orders and 6.9 million
   more with one order per symmetry class, five loop-energy functions inside (H0)–(H2) (§3).
2. **Theorem 3 is proved as stated** — labelled count, the set of minimisers, and the orbit count, by review and replication.
   Corollary 2 holds.  Corollary 4(i) holds: the reduction is weakly parsimonious with the explicit factor m!·24^m / Π μ_s!.
   Corollary 4(ii) is right in substance; its computational problem (encoding of the temperature, exactness of Z) is not stated.
3. **(H0) is the definition of the model in the papers that pose the question** (Dirks et al., App. B note 3; the appendix of the
   full version of Ducloz–Shalaby–Woods), not an added restriction; it fails for tables with dangles or coaxial stacking.
4. **Findings: 0 critical, 2 major, 10 minor** (§2.3), each with a replacement text.
5. *Major F1:* the gadget is Lyngsø's 2004 bin-packing reduction in the form of Ducloz–Shalaby–Woods Theorem 32, cut into strands;
   the note does not cite it (their prior-art file does).
6. *Major F2:* "(H2) is the sign pattern of every physical parameter set" is false — the 2004 RNA rules give a single-nucleotide
   bulge −0.13 kcal/mol in the database's own worked example.  (H2) can be replaced by a weaker (H2\*) with a five-line proof.
7. *Minor:* Remark 3 overstates the failure under coaxial stacking; precision of Corollaries 2 and 4; sources and exact use of
   (H0); the pairing rule and the one-complex formulation (both already promised by the authors); the base-pair model is itself a
   loop model; verification bookkeeping; small slips.
8. **Controls:** with any one hypothesis dropped the theorem fails on the same instances — a stack across a nick rewarded like a
   stack gives a wrong decision on 23 of 32 non-solvable instances.
9. **Re-run:** their small test completes ("ALL OK"); their big test does not — under a 2 GB cap it stops at its 11th case with a
   memory error, exactly where their shipped log ends; case by case, 11 of 12 pass; the option `check=True` that the note relies on is never switched on
   by their scripts (switched on by me, it passes).  Their numbers equal mine everywhere.
10. **Novelty:** it answers a question stated as open in two papers (2025), for loop functions with exterior loops 0 satisfying (H1)
    and (H2\*); it is not a corollary of the three papers named in the brief; the construction is a small step from a published
    one.  A short search cannot establish novelty.

---

## 1. The statements as I understand them, with the hypotheses the note leaves implicit

### 1.1 The model, and whether it is the multi-stranded nearest-neighbour model of the literature (brief, Item 1(i))

| element of the note (§1) | where it is in the literature | how checked |
|---|---|---|
| strands over {A,C,G,T}, pairs A–T and C–G only (l.32–35) | [DSW] §2.1; [SW25] §2; [CHT] §2 | opened |
| structure = set of disjoint pairs (l.35–36) | [DSW] Def. 4; [D07] §2.1 | opened |
| unpseudoknotted = some circular order of the strands has no crossing chords (l.39–43) | [D07] §2.1; [SW25] Def. 4; [DSW] Def. 5 (with a linear order; equivalent) | opened |
| the order is unique for a connected structure (l.43–45) | [D07] Theorem 2.1 ("Representation") — the note's citation is exact | opened; review; replication (check V4, U3) |
| loop types; a loop with one nick is an exterior loop (l.47–53) | [D07] §2.1: "all loops containing one nick are exterior loops"; [DSW] App. A.2 | opened |
| Fact 1: connected ⇔ no loop with two nicks (l.55–57) | [D07] §2.1: "A secondary structure is connected if no loop contains more than one nick" | opened; review (planar duality, §2.1 below); replication (V3) |
| ΔG = Σ loops + (c−1)ΔG_assoc + k_BT ln R (l.63–69) | [D07] Eq. (2.1); [DSW] Def. 11; [SW25] Eq. (2); [SW26] Def. 7 | opened |
| R(S) = maximal degree of rotational symmetry | [SW25] Def. 9, Remark 10; [SW26] Def. 11, Remark 12 | opened |
| physical ensemble: structures that differ by a permutation of equal strands are one structure (l.70–72) | [D07] §2.2; [SW26] Def. 7 | opened |
| MFE = minimum over connected unpseudoknotted structures of the complex of **all** strands (l.69–70) | [SW25] Remark 5 and Eq. (3); [DSW] Def. 11 with footnote 4 ("In the NN model, unlike the BPM and BPS models, multi-stranded secondary structures must be connected") | opened |
| exterior loops have energy 0 — hypothesis (H0) | [D07] App. B note 3: "Exterior loops do not contribute to the free energy because by definition ∆G^empty = 0"; [DSW] App. A.2 (arXiv version only): "Exterior loops do not contribute to the free energy because by definition [8], ∆G^exterior = 0"; [SW26] footnote 19 | opened |
| a "stack across a nick" is not a stack but an exterior loop | consequence of the definition of exterior loop in [D07]; no coaxial stacking in [D07], [DSW], [SW25], [SW26] as far as I read them | opened |
| association term | [D07] §2.1 and note 13 (ΔG_assoc = ΔG_pub − kT log ρ_H2O) | opened |

So the model of the note **is** the model of [D07]/[DSW]/[SW25]/[SW26] as these papers write it.  In particular **(H0) is not an extra
restriction relative to the papers that pose the question: it is their definition.**  (The note says this only for [SW26], l.73–74;
[DSW]'s own appendix and [D07] say it too — the Complexity division had not read [DSW]'s appendix A nor [D07], by its `PRIOR_ART.md`.)
Differences from the model as *implemented*: [D07] itself says its implementation adds "dangle free energies [...] and penalties
for helices not ending in C-G pairs", "omitted" from the exposition (caption of its Fig. A.1); rule sets with coaxial stacking
reward a flush nick ([NNDB] coaxial page: flush stacks are approximated by the helix parameters "as though there was no break in
the backbone").  Nothing in the note has a minimal hairpin length; the instances have no hairpin, so this does not matter.

### 1.2 What (H0)–(H2) exclude (Item 1(ii)), and whether §6 of the note is accurate and complete

* **(H0), exterior loops 0.**  Excludes: dangling-end energies in exterior loops (in [D07]'s implementation); coaxial stacking
  across a nick; terminal-mismatch terms.  Does *not* exclude penalties for helix ends that are not G–C pairs: all pairs of the
  instance are G–C, so these vanish.  §6.1 of the note is accurate on dangles and coaxial stacking, **except** its sentence "With
  coaxial stacking as strong as stacking the reduction fails (Remark 3)", which is true only if in addition the bulge in which an
  item crosses a separator costs nothing (finding F3).  Not said in §6: a *constant* exterior-loop energy is harmless (every
  connected structure has exactly c exterior loops); exact zero is used only on the four kinds of exterior loops of a tiling
  structure, and "≥ 0" on the others (F7).
* **(H1), GG/CC stack negative.**  No published stack table known to me violates it [from memory — unverified]; [NNDB] gives
  −3.26 kcal/mol for the RNA stack "CG followed by CG" `[page text]`.
* **(H2), bulge / interior / multiloop ≥ 0.**  The note calls this "the sign pattern of every physical parameter set" (l.14) and,
  in §6.2, says it "excludes hypothetical parameter sets with favourable bulges".  **This is false** (finding F2): in the RNA 2004
  rules a single-nucleotide bulge has loop energy *initiation + special-C bonus + stack of the closing pairs − RT ln(states)*, and
  the worked example of the [NNDB] page gives +3.81 − 0.9 − 2.36 − 0.616×1.099 = **−0.13 kcal/mol**.  The theorem survives because
  (H2) is far stronger than what the proof uses (statement (P1) below).

### 1.3 Resources of the reduction (Item 1(iii))

* **Unary encoding.**  An item of size a_i is a strand of a_i letters and the template has mB + m − 1 letters, so the instance has
  size Θ(mB): the numbers are written in unary.  The reduction is polynomial only from a problem that is NP-hard with
  polynomially bounded numbers — 3-PARTITION / 4-PARTITION are ([GJ], `[from memory — unverified]` for the theorem numbers 4.4 and
  4.3).  **Holds.**
* **Strands and species.**  n + 1 strands, and as many species as there are distinct item sizes plus one.  The number of species
  must be unbounded: exact bin packing with unary sizes and at most d distinct sizes is solved by a dynamic programme over count
  vectors in time n^{O(d)}, so no reduction from it with a bounded number of distinct sizes can be hard [P, standard].  The note
  says so (l.248–249, "unboundedly many species").  Whether hardness needs unboundedly many species for *every* reduction is the
  question of `OPEN_PROBLEMS.md` C2 and is not settled by the note.

### 1.4 The statements, with their implicit hypotheses made explicit

Setting: as §1 of the note.  I = I(a,m,B): template G^B(AG^B)^{m−1}, items C^{a_i} (a_i ≥ 1, Σa_i = mB), c = n + 1, M = mB − n.
Ω(I) = connected unpseudoknotted structures of I.  A *tiling structure* pairs every item base by base, antiparallel, with a run of
consecutive G's inside one block, the runs partitioning the G's.

* **Theorem 1.**  If g satisfies (H0)–(H2): (1) solvable ⇒ min_{Ω(I)} ΔG_g = σM + nΔG_assoc; (2) not solvable ⇒
  min ≥ σ(M−1) + nΔG_assoc; (3) S ∈ Ω(I) has energy σM + nΔG_assoc iff S is a tiling structure.
* **Corollary 2.**  For every fixed such g, ΔG_assoc, T: "is min_{Ω(I)} ΔG_g ≤ k?" is strongly NP-hard.
* **Theorem 3.**  #{S ∈ Ω(I) labelled : ΔG_g(S) = E*} = Til(a,m,B) = Σ_β Π_t |β^{-1}(t)|!; in the physical ensemble Til / Π_s μ_s!;
  Til = L·m!·6^m (3-PARTITION shape), L·m!·24^m (4-PARTITION shape).
* **Corollary 4.**  (i) #SSEL is #P-hard; (ii) the partition function of the stack-only model, temperature part of the input, is
  #P-hard.

Hypotheses the note leaves implicit (none of them is false; each should be written):

1. *Pairing rule*: among the letters A, C, G the only complementary pair is {C, G}.  True for Watson–Crick and for
   Watson–Crick + G·T/G·U wobble (no T/U in the instance).  (F8)
2. *Ensemble*: one complex containing all strands.  This is the problem of [SW25]/[DSW]; it is not the formulation of [CHT]
   (several complexes, association energy per bound strand), for which a condition is needed.  (F9, (P4))
3. *"Exterior loop" includes the flush nick*: two items abutting on the template with a template bond under the nick form an
   exterior loop of energy 0.  This is where (H0) carries the proof.  (F3, F7)
4. *Numbers*: σ and ΔG_assoc are reals; for a decision problem the threshold k must be writable — any rational in
   [σM + nΔG_assoc, σ(M−1) + nΔG_assoc) will do — and "in NP" needs a convention for k_BT ln R(S).  (F5)
5. *Counting*: #4-PARTITION must be #P-complete with polynomially bounded weights (unary encoding); the oracle of
   Corollary 4(ii) must return exact values, or enough digits.  (F4, F6)

---

## 2. Findings

### 2.1 Theorem 1 step by step (Item 2) — all **review**; replication in §3

| point of the brief | step and lines of the note | verdict | the line that decides it |
|---|---|---|---|
| (a) which pairs are possible | (a), l.117–119 | **holds**; condition to state: implicit hypothesis 1 | l.117: "`A` has no complementary letter in the system, the template contains no `C` and the items contain no `G`" — true for the rule of l.34–35 and for wobble |
| (b) st(S) ≤ M | (c), l.124–130 | **holds** | l.129: "A link lies on the boundary of exactly one face"; with l.125–128 each stack owns one item bond |
| (c) every stack has one template bond and one item bond; nick between two items in a block; separator; template ends | (c) l.125–128; (e) l.152–157 | **holds**.  A stack is nick-free with two chords and no unpaired base, so its boundary is chord, bond, chord, bond; a chord joins template and item, a bond stays in its strand ⇒ one bond of each kind; antiparallel orientation is forced by non-crossing.  *Nick between two items of one block*: the face (two chords, the template bond, the nick) has one nick ⇒ exterior loop ⇒ 0 by (H0) — not a stack; this is the load-bearing use of (H0).  *Separator*: an item that crosses `A` has its bond on a bulge (≥ 0 by (H2)); two items on either side of `A` give an exterior loop.  *Template ends*: two exterior loops with one chord each. | l.50 (definition of exterior loop), l.125 ("two chords and two links, both covalent bonds"), l.152–157 |
| (d) connectedness / unpseudoknottedness of the structure realising the bound and of every structure attaining it | (d) l.136–147; (e) l.149–159 | **holds**.  The tiling structure is nested in the order "template, items in reverse run order"; it has n + 1 faces with exactly one nick ⇒ connected.  Conversely st(S) = M forces every item bond onto a stack ⇒ runs of adjacent G's inside one block ⇒ tiling; items of length 1 are paired because S is connected. | l.140 ("a run of consecutive `G`'s contains no `A`"), l.157–158 |
| (e) symmetry term | (b) l.121–122 | **holds**: the template occurs once, a rotation fixing it is the identity, R(S) = 1 | l.121 |
| (f) association term | l.64, l.122, Cor. 2 l.162–163 | **holds** for the problem as posed (one complex: (c−1)ΔG_assoc is constant) and that is the problem of [SW25]/[DSW]; for the formulation with several complexes ([CHT]) **holds with a condition to add**: \|σ\|(a_i − 1) > ΔG_assoc for all i ((P4)) | l.69–70 |
| (g) equality case; strong NP-hardness of the packing problem | l.91–94; l.146–147; l.168 | **holds**: "MFE = σM + nΔG_assoc" ⇔ solvable by parts 1–2 (gap \|σ\| > 0); EXACT BIN PACKING (a_i ≥ 1, Σa_i = mB, any m) contains 3-PARTITION | l.93–94; l.109 |

Two auxiliary facts of §1, re-derived:
*Fact 1.*  The polymer graph with all N links is a cycle with non-crossing chords, a connected plane graph.  Removing the set F of
nick edges leaves it connected iff F contains no minimal cut, iff the dual edges F* contain no cycle.  A nick is dual to an edge
between the outer face and the inner face that contains it; so F* has a cycle iff two nicks lie on one inner face. ∎
*Uniqueness of the order.*  If S is connected, the face of the nick after the 3′-end of strand t has no other nick; walking its
boundary backwards from that 3′-end uses only pairs and covalent bonds and stops at the 5′-end of the successor of t.  The walk is
defined by S and the strands alone, so the successor of every strand, hence the cyclic order, is determined by S. ∎

**No step is a gap and none is false.  Theorem 1 is proved as stated.**

### 2.2 Theorem 3 and the partition function (Item 3) — review; replication in §3

* *How many minimum-energy structures per solution.*  By Theorem 1(3) the structures at E* are the tiling structures, and a tiling
  structure is the same thing as a sequence of labelled items along each block.  Identity of blocks: blocks are positions of the
  template, so the m classes of a partition can be assigned in m! ways; order inside a block: \|β^{-1}(t)\|! ways; identical items:
  the group Π_s Sym(μ_s) acts freely on tiling structures (indeed on all of Ω(I): every item is paired, and distinct items have
  disjoint partner sets), so orbits have Π_s μ_s! elements; symmetry number: R = 1 always.  **Holds.**
* *Is the count a known #P-hard quantity; is the reduction parsimonious?*  L(a,m,B) for 4-PARTITION-shaped instances is exactly
  the function of [DSW] Def. 29 ("the number of partitions of A into 4-tuples, such that the sum of the weights of the elements in
  each tuple is equal to B", A a set of labelled elements), #P-complete by [DSW] Lemma 31 `[full text]`.  The reduction is **weakly
  parsimonious with the explicit factor** #SSEL(E*) = L · m! · 24^m / Π_s μ_s! (labelled: L · m! · 24^m).  The same factor
  (k/4)!(4!)^{k/4} appears in [DSW] Thm 32.  Condition to state: polynomially bounded weights (F6).
* *Temperature.*  In the stack-only model with ΔG_assoc = 0, Z = Σ_k N_k x^k with x = e^{1/k_BT}, N_k = #SSEL(−k), N_M = #SSEL(E*).
  The note recovers the N_k from M + 1 temperatures by a Vandermonde system, citing [DSW] Thm 22.  As mathematics over exact reals
  this is right, and it is how [DSW] argue (their Defs 14–18 take "a temperature T ≥ 0" and "k ∈ ℝ"; no encoding is given there
  either).  As a reduction between problems with finite inputs and outputs it needs an encoding of T and exact values of Z; a
  single evaluation at an integer x larger than the number of structures already gives all N_k as digits (F4).  **Holds in
  substance; statement to be made precise.**

**Theorem 3 is proved as stated; Corollary 4(i) holds; Corollary 4(ii) holds once its computational model is written down.**

### 2.3 The findings

Classes: *critical* = a theorem of the note is false or unproved; *major* = a statement of the note is false, or a missing
attribution, in a way that changes what a reader would take from it; *minor* = precision, completeness, verification bookkeeping.

**Critical: none.**

**F1 [major] — the construction is a published one and the note does not say so.**
*Decided by:* note l.15–19 and l.24–26 ("Its novelty, if any, is that the question was posed as open in 2025 and that we found no
proof in print") — no source for the gadget; against [DSW] Thm 32 `[full text]`: "In 2004, Lyngsø [20] proved that the decision
problem BPS is NP-complete, with a reduction from BIN-PACKING.  We adapt his reduction from 4-PARTITION to BPS.  […] We proceed
exactly as Lyngsø, constructing the following DNA strand s: s = C^{w(a1)} A C^{w(a2)} A ··· A C^{w(ak)} AAA G^B A G^B A ··· A G^B
[k/4 substrings of G's] and setting the target K = Σ w(a_i) − k", with the multiplicity "(k/4)! (4!)^{k/4}".  The note's template,
items, target M = Σa_i − n and factor m!·24^m are this construction with the single strand cut at the A's between the C-runs.
The division's own `PRIOR_ART.md` (l.35–37) says "The reduction is a variant of Lyngsø's bin-packing reduction […] which A-I adapts
for counting (its Theorem 32)"; the note itself, which is what will be read and cited, does not.  ([L04] itself I could not open;
the attribution rests on [DSW]'s description of it.)
*Replacement text (for l.15–19):* "The reduction is from bin packing with exact fill (3-PARTITION / 4-PARTITION).  The gadget is not
ours: the template `G^B(AG^B)^{m−1}` and the runs `C^{a_i}` are Lyngsø's reduction from BIN PACKING to pseudoknotted folding of one
strand in the base-pair-stacking model (ICALP 2004), in the form used for counting by Ducloz–Shalaby–Woods (DNA 31, Theorem 32:
`C^{w(a_1)}A…AC^{w(a_k)} AAA G^BA…AG^B`, target Σw(a_i) − k, multiplicity (k/4)!·(4!)^{k/4}).  What is added here is one observation:
if that strand is cut at the `A`'s between the `C`-runs, the crossings of its optimal structures disappear — the cyclic order of
the k + 1 strands takes over their role — so that the same counting argument holds for *connected unpseudoknotted* structures of
many strands, in every nearest-neighbour loop-energy function satisfying (H0), (H1), (H2*), with the association and symmetry terms
present."  *(For l.24–26:)* "The mathematics is elementary and the gadget is Lyngsø's (see above).  What is new, if anything, is
the transfer to several strands without pseudoknots, which answers a question stated as open in Ducloz–Shalaby–Woods (2025,
Future work 1) and in Shalaby–Woods (ICALP 2025, caption of Table 1); we found no proof in print (`PRIOR_ART.md` §A)."

**F2 [major] — "(H2) … the sign pattern of every physical parameter set" is false; (H2) should be replaced by a weaker hypothesis.**
*Decided by:* note l.12–15 and §6.2 (l.259: "(H2) excludes hypothetical parameter sets with favourable bulges, interior loops or
multiloops"), against [NNDB] RNA-2004 bulge page `[page text]`: "ΔG°37 bulge (n=1) = ΔG°37 bulge initiation(n) + ΔG°37 (special C
bulge) + ΔG°37 (base pair stack) – RT ln(number of states)", worked example "–3.42 kcal/mol – 3.26 kcal/mol + 4.09 kcal/mol + 3.81
kcal/mol – 0.9 kcal/mol – 2.36 kcal/mol – 0.616×1.099 kcal/mol", of which the last four terms are the bulge loop: −0.13 kcal/mol.
The loop of this kind that occurs in the instances — a bulged C of an item between two G–C pairs — is exactly a "special C bulge".
So a published rule set has favourable bulges; (H2) as stated does not hold for it, and the sentence of l.14 is wrong.
*Why the theorem is not affected:* statement (P1) below — the proof needs only that a bulge, interior loop or multiloop is less
favourable than GG/CC stacks on all the item bonds on its boundary.
*Replacement text (for l.12–15):* "Yes, for every nearest-neighbour loop-energy function in which exterior loops cost nothing (the
definition of the model in Dirks et al. 2007 and in the cited papers), the `GG/CC` stack is favourable, and no bulge, interior loop
or multiloop is as favourable as `GG/CC` stacks on all the item bonds on its boundary (hypothesis (H2*); in particular whenever
these loops are not favourable at all)."  *(For l.81:)* "**(H2\*)** There is δ > 0 such that g(f) ≥ σ·b(f) + δ for every bulge,
interior loop and multiloop f of a structure of the instance, where b(f) ≥ 1 is the number of covalent bonds of items on the
boundary of f.  ((H2), g(f) ≥ 0, is the special case δ = |σ|.)"  *(Theorem 1, part 2:)* "otherwise MFE(I) ≥ σM + nΔG_assoc +
min(|σ|, δ)."  *(§6.2:)* "(H2*) must be checked for the table at hand.  (H2) itself fails for published rules: in the RNA 2004 rules
a single-nucleotide bulge has energy initiation + special-C bonus + stack of the closing pairs − RT ln(states), −0.13 kcal/mol in
the worked example of the Nearest Neighbor Database; (H2*) holds there as long as that energy stays above the energy of the stacks
on the item bonds of the loop.  A degeneracy term −RT ln(states) taken literally on arbitrarily long homopolymer runs is unbounded
below and would violate (H2*) for very long runs; we make no claim for such a rule."

**F3 [minor] — Remark 3 and §6.1 overstate the failure under coaxial stacking.**
*Decided by:* l.178–180 ("If a 'stack' across a nick were also rewarded (coaxial stacking with the same energy as a stack), the
reduction would fail: every arrangement of the items along the template would be optimal") and l.256–257.  "Every arrangement is
optimal" needs the bulge in which an item crosses a separator to cost 0; (H2) allows that (the stack-only model) but does not force
it.  Statement (P2) below: with a flush nick rewarded by κ, the reduction survives for σ < κ ≤ 0 unconditionally, and for κ = σ
whenever that bulge costs δ_A > 0 (with a different threshold).  [P], replicated (GEN3, GEN4, GEN7; control CTRL1).
*Replacement text (Remark 3):* "3. *Coaxial stacking.*  Let a flush nick — a face with one nick, two chords, one template bond and
no unpaired base — have energy κ instead of 0, everything else as in (H0)–(H2).  If σ < κ ≤ 0 the theorem holds with
E* = σM + κ(n − m) + nΔG_assoc and gap κ − σ.  If κ = σ and B ≥ 2 it holds with E* = σ·m(B − 1) + nΔG_assoc and gap min(|σ|, δ_A),
provided the bulge in which an item crosses a separator (template side `GAG`, item side `CC`) has energy δ_A > 0.  If that bulge
costs nothing, as in the stack-only model, every arrangement of the items along the template is optimal and the reduction fails.
The case κ < σ is not analysed."  *(§6.1, last sentences:)* "With coaxial stacking the reduction survives in the cases of Remark 3
and fails in the stack-only model.  With dangling-end energies we have only a sufficient condition (…); we make no claim about any
specific published parameter table."

**F4 [minor] — Corollary 4(ii): the computational problem is not stated.**
*Decided by:* l.213–215, l.219–222 ("the values of `Z` at `M + 1` temperatures determine all `N_k` by a Vandermonde system").  For a
rational T the number Z(T) is not rational; no encoding of T, no precision of Z is given (nor in [DSW] Thm 22, whose size analysis
counts only the digits before the point).
*Replacement text:* "(ii) For a system I let Z_I(x) = Σ_S x^{st(S)}, the sum over the physical ensemble: the partition function of
the stack-only model (ΔG_assoc = 0) at the temperature with e^{1/k_BT} = x.  The function (I, x) ↦ Z_I(x), x a positive integer in
binary, is #P-hard.  *Proof.*  Z_I(x) = Σ_{k≤M} N_k x^k with N_k = #SSEL(−k) ≤ W := N! (Ducloz–Shalaby–Woods, Lemma 21).  For
x > W the N_k are the digits of the integer Z_I(x) in base x; N_M = #SSEL(E*).  One oracle call.  If the oracle takes a rational
temperature and returns an approximation Z̃, it suffices that x = e^{1/k_BT} ≥ 4W and |Z̃ − Z| < x^M/4: then
N_M = ⌊Z̃/x^M + 1/4⌋; this is poly(N) bits of relative precision.  (The Vandermonde argument of Ducloz–Shalaby–Woods, Theorem 22, is
over exact real numbers.)"

**F5 [minor] — Corollary 2: "in NP" and the threshold.**
*Decided by:* l.165–166, l.169–170 ("`R(S)` and the energy are computable in polynomial time").  k_BT ln R(S) is irrational for
R(S) ≥ 2 and rational k_BT; comparing the energy with k needs a convention ([DSW] Future work 4 raises the same issue for
logarithmic loop terms).  For hardness, σ and ΔG_assoc are arbitrary reals and k = σM + nΔG_assoc need not be writable.
*Replacement text:* "*Proof.*  Theorem 1 with any rational k such that σM + nΔG_assoc ≤ k < σ(M − 1) + nΔG_assoc (computable in
polynomial time if σ and ΔG_assoc are polynomial-time computable reals), from 3-PARTITION.  Membership in NP holds for rational
g, ΔG_assoc, k on systems in which some strand occurs only once (then R ≡ 1; this includes the instances of the reduction); in
general it needs a convention for comparing k_BT ln R(S) with a rational, cf. Future work 4 of Ducloz–Shalaby–Woods."
(The same remark applies to "#P-complete" in Corollary 4(i), l.212–213, which in addition needs one witness per *physical*
structure — for instance the lexicographically least rotation of the polymer graph; the note gives no argument.)

**F6 [minor] — Corollary 4(i) needs #4-PARTITION with polynomially bounded weights.**
*Decided by:* l.189–191 and l.217.  The reduction writes the weights in unary; [DSW] Lemma 31 states "#4-PARTITION is #P-complete"
without a bound on the weights.  The bound is there: the lemma goes through Garey–Johnson's transformation from 3DM, which
is pseudo-polynomial ([GJ], `[from memory — unverified]`), and [DSW] Thm 32 uses it in unary in the same way.
*Replacement text (l.189–191):* "(for 4-PARTITION instances this is the function of Ducloz–Shalaby–Woods, Def. 29, #P-complete by
their Lemma 31; the lemma goes through Garey–Johnson's pseudo-polynomial transformation from 3DM, so it holds with weights bounded
by a polynomial in the number of elements, which is what a reduction that writes the weights in unary needs)".

**F7 [minor] — (H0): sources, and what exactly is needed.**
*Decided by:* l.72–74 (ΔG_ext = 0 attributed to [SW26] §6 only; it is footnote 19 there, and it is also in [D07] App. B note 3 and
[DSW] App. A.2), l.78, l.255–258.
*Replacement text (l.72–74):* "This is Definition 11 of Ducloz–Shalaby–Woods and Definition 7 of Shalaby–Woods.  In this model the
exterior loop has ΔG = 0 by definition (Dirks et al. 2007, App. B note 3; Ducloz–Shalaby–Woods, full version, App. A.2;
Shalaby–Woods 2026, footnote 19); the *implementation* described by Dirks et al. adds dangle energies and penalties for helix ends
that are not G–C pairs, which their exposition omits."  *(l.78:)* "**(H0)** g(f) = e_0 for every exterior loop, e_0 a constant.
(Its value is immaterial, every connected structure having exactly c exterior loops; we take e_0 = 0.  The proof uses the value
only on the four kinds of exterior loops of a tiling structure — a flush nick over a template bond, a nick opposite the unpaired
separator, the two blunt ends — and g(f) ≥ e_0 on all other exterior loops.  Penalties for helix ends that are not G–C pairs vanish
on the instances.)"

**F8 [minor] — the pairing rule the theorem needs.**  *Decided by:* l.34–35, l.117.  *Already promised:* the Complexity division
writes in `COMPLEXITY-RES-0001` (at their newer commit `22cf1a6`, read with read-only git): "the pairing rule (Watson–Crick only:
A–T, C–G; no G–U, no G–G) and that the problem is posed for the one complex containing all strands — are in §1 of the note; we
will move them into the statement when your SCI-REV-0019 arrives".  My text asks for slightly less than they promise: the
theorem does not need "no G–U", only that A, C, G admit no pair other than C–G.  *Replacement text (l.117):* "(a) *Pairs.*  Among
the letters `A`, `C`, `G` the only complementary pair is `{C,G}` — under the rule of §1 and equally if `G·T` (`G·U`) wobble pairs
are allowed, since the system contains no `T` (`U`); this is all the theorem needs of the pairing rule.  So every pair of `S` …"

**F9 [minor] — which MFE problem; Remark 2 covers only ΔG_assoc = 0.**
*Decided by:* l.69–70, l.162–163, l.174–177.  (*Already promised*, same message as under F8: "the one complex containing all
strands" will be moved into the theorem statement.  What remains of this finding is the other formulation.)  The problem is posed for one complex containing all strands — the ensemble of
[SW25] (Remark 5, Eq. (3)) and [DSW] (Def. 11, footnote 4), so the association term is a constant.  In the formulation of [CHT]
(E = −p + (m − l)K_assoc, several complexes) an item may stay out, and the equivalence can fail: a = (2,2,2), m = 2, B = 3,
ΔG_assoc ≥ |σ| — two bound items reach 2σ + 2ΔG_assoc ≤ 3σ + 3ΔG_assoc.  Statement (P4): it holds whenever binding pays for every item, and it can fail otherwise.
*Replacement text (new Remark):* "5. *Several complexes.*  If strands may be left out of the complex — a structure being a set J
of items in one complex with the template, the other items free, with energy Σ_f g(f) + |J|·ΔG_assoc — then for instances with
|σ|(a_i − 1) > ΔG_assoc for every i the minimum is σM + nΔG_assoc if the packing instance is solvable and at least
σM + nΔG_assoc + min(|σ|, min_i(|σ|(a_i − 1) − ΔG_assoc)) otherwise; multiplying all a_i and B by a constant preserves solvability,
so the problem is strongly NP-hard for every fixed ΔG_assoc.  Without the condition the statement is false
(a = (2,2,2), m = 2, B = 3, ΔG_assoc ≥ |σ|)."

**F10 [minor] — §4 claims more verification than the shipped scripts and log deliver.**
*Decided by:* l.55–56 ("re-checked exhaustively by the enumerator's `check=True` mode against a union–find computation"),
l.230–237, and the files: (i) neither test script passes `check=True` (default `False` in `ref_enum.enumerate_structures`), so the
re-run instructions of `HANDOFF.md` never execute that check; (ii) `big_run.log` holds 10 of the 12 cases of
`test_partition_reduction_big.py` and no final "ALL OK" line — it is the log of a run that did not finish; my re-run of the script
stops at the same place, the 11th case, with `MemoryError` under a 2 GB cap (their `seen` set keeps every structure); (iii) "up to
513 120 structures per instance" (l.232) — the largest instance in their log has 836 544; (iv) not tested by their scripts at all:
that the minimisers *are* the tiling structures (only their number), R(S) = 1, Theorem 3.2 (`symmetry_orbits` is never called),
Corollary 4; two loop functions only.  All of (i)–(iv) I have checked myself, with 0 violations (§3, §4).
*Replacement text (l.55–56):* "(Dirks et al. 2007, where it is the definition of 'connected'; [K].  The enumerator's `check=True`
mode compares it with a union–find computation; run on the ten cases of `…` it raised no assertion on 1 099 956 structures.)"
*(l.230–237:)* state the cases actually completed, the memory needed, and either drop the `seen` set for the large cases or store
64-bit hashes; regenerate the log.

**F11 [minor] — Remark 4 does not say why the base-pair result does not already answer the question.**
*Decided by:* l.181–183.  On the connected ensemble the base-pair model *is* a loop model: a connected unpseudoknotted S has
|S| + 1 faces, c of them exterior, so −|S| = Σ_f g(f) − (c − 1) with g = −1 on every non-exterior loop and 0 on exterior loops [P].
With the loop function part of the input and no sign condition, NP-hardness of "the NN framework" for unboundedly many strands
would therefore already follow from [CHT] (whose yes-instances have a single-complex optimum: "Our construction has the property
that structure Opt(I′) is a single complex when I has a perfect matching" `[read; the reduction itself not read]`).  The content of
the note's theorem is hardness under the *physical sign pattern*, for every *fixed* such function.
*Replacement text (Remark 4):* "4. On the connected ensemble the base-pair model is the loop model g = −1 on every non-exterior
loop (|S| = number of non-exterior loops + c − 1).  It satisfies (H0) and (H1) and violates (H2*): a bulge is as favourable as a
stack.  For it the instances `I(a,m,B)` are trivial (all `mB` pairs can always be formed), which is why the reduction of
Condon–Hajiaghayi–Thachuk is elaborate.  Conversely their theorem already gives hardness for that particular loop function; what
is shown here is hardness when loops with unpaired bases are not as favourable as the stacks they replace, for every fixed such
function."

**F12 [minor] — small slips.**  (i) `COMPLEXITY-MSG-0001.md` and `status/complexity.md` are dated "2026-11-26 17:00 UTC"; the commit
that contains them has committer date 2026-11-26T16:17:10Z (read-only `git log`): the time was not read from a clock.
(ii) l.93–94: in [GJ] Theorem 4.3 is 4-PARTITION and Theorem 4.4 is 3-PARTITION `[from memory — unverified]`; the note lists them
in the other order.  (iii) l.74: the quotation is footnote 19 of [SW26] and reads "∆G^ext = 0 for the energy contribution of an
exterior loop or equivalently in the case of having empty substructure".  (iv) l.9–10: [CHT]'s energy is −p + (m − l)K_assoc, not
only minus the number of pairs.  *Replacement:* correct the four places.

### 2.4 Statements of this review that support the replacement texts

All are [P] (my proofs, short) and were tested by **replication** on the instances of §3 only — they are not reviewed by anyone.
Notation: for S ∈ Ω(I), st = number of stacks; every item bond lies on exactly one face.

**(P1) Theorem 1 under (H2\*).**  Assume (H0), (H1) and (H2\*): g(f) ≥ σ·b(f) + δ, δ > 0, for every non-stack nick-free face f,
b(f) = number of item bonds on f.  Then (1) solvable ⇒ MFE = σM + nΔG_assoc; (2) otherwise MFE ≥ σM + nΔG_assoc + min(|σ|, δ);
(3) energy σM + nΔG_assoc iff tiling.
*Proof.*  Let e be the number of item bonds on exterior faces and ns the number of non-stack nick-free faces.  The M item bonds
split into st (one per stack), Σ b(f) over non-stack nick-free faces, and e.  Hence
Σ_f g(f) ≥ σ·st + Σ(σ b(f) + δ) = σ(M − e) + δ·ns = σM + |σ|e + δ·ns.  Equality with σM forces e = ns = 0, i.e. every item bond on a
stack, i.e. st = M, i.e. (step (d) of the note) a tiling structure; otherwise the excess is at least min(|σ|, δ).  Tiling
structures have energy σM by step (e). ∎  ((H2) ⇒ (H2\*) with δ = |σ| because b(f) ≥ 1: next to any chord of a nick-free face the
item end of the chord is followed or preceded on the face by a link, which is an item bond.)
Replication: GEN1 (every non-stack loop at σb + 1), GEN2 (mixed negative loops): 0 violations; control CTRL4 (δ = 0) violated.

**(P2) Coaxial stacking.**  Assume (H1), (H2), exterior loops 0 except flush nicks (one nick, two chords, no unpaired base), which
have energy κ.  A flush nick carries exactly one template G–G bond (its nick cannot be on the template side: there is one
template), so st + q ≤ m(B − 1), q = number of flush nicks.
(a) If σ < κ ≤ 0: Σ_f g ≥ σ·st + κ·q ≥ σ·st + κ(m(B−1) − st) = (σ − κ)st + κ·m(B−1) ≥ (σ − κ)M + κ·m(B−1) = σM + κ(n − m), with
equality only if st = M (tiling: then q = n − m); if st ≤ M − 1 the excess is ≥ κ − σ. ∎
(b) If κ = σ, B ≥ 2 and the bulge "template `GAG`, item `CC`" has energy δ_A > 0: Σ_f g ≥ σ(st + q) ≥ σ·m(B−1).  If st + q = m(B−1),
every G–G bond is on a stack or a flush nick, so every G is paired (B ≥ 2), so every C is paired.  For an item bond with partners
x < y on the template, the positions strictly between x and y are enclosed by the two chords and the bond, can pair only with each
other, hence are unpaired, hence are `A`: either y = x + 1 (a stack) or y = x + 2 around a separator (that bulge).  So the energy
is σ·m(B−1) + δ_A·(number of such bulges), equal to σ·m(B−1) iff tiling; otherwise the excess is ≥ min(|σ|, δ_A). ∎
Replication: GEN3 (κ = σ/2), GEN4 and GEN7 (κ = σ; all non-stack loops +1, resp. only that bulge +1): 0 violations; control CTRL1
(κ = σ, bulges 0) violated — e.g. a = (3,1), m = 2, B = 2, not solvable, reaches σM.

**(P3) Dangles, a sufficient condition.**  Assume (H1), (H2) and that an exterior loop has energy Σ d(u) ≤ 0 over its unpaired bases
u that are covalent neighbours of a paired base of the loop (one term per base), with |d(u)| ≤ D_G for template G's, ≤ D_C for item
C's, and the value e_A ≤ 0 for a separator `A` between two paired G's being the most favourable value an `A` can take.  If
|σ| > D_G + D_C then MFE = σM + (m − 1)e_A + nΔG_assoc for solvable instances, ≥ that + (|σ| − D_G − D_C) otherwise, and the
minimisers are the tiling structures.
*Proof.*  Let j = M − st and u = number of unpaired C's = number of unpaired G's.  An item with r < a_i unpaired bases has at least
r bonds with an unpaired end, none of them on a stack; so j ≥ u.  Then Σ_f g ≥ σ(M − j) − u(D_G + D_C) + (m − 1)e_A
≥ σM + (m − 1)e_A + j(|σ| − D_G − D_C), and a tiling structure attains σM + (m − 1)e_A. ∎
Replication: GEN5 (all dangles −1, σ = −3): 0 violations; control CTRL5 (dangles −2, σ = −3) violated.  This is an abstract "one
dangle per unpaired base" rule; I did not compare it with any published dangle table.

**(P4) Several complexes.**  As in F9.  *Proof.*  With J bound, st ≤ Σ_{i∈J}(a_i − 1), so the energy is ≥ Σ_{i∈J}(σ(a_i − 1) + ΔG_assoc)
= σM + nΔG_assoc + Σ_{i∉J}(|σ|(a_i − 1) − ΔG_assoc); for J = everything this is Theorem 1. ∎
Replication: `r20_assoc.py`, §3.5.

**(P5) Constant exterior energy.**  If every exterior loop has energy e_0, all energies shift by c·e_0.  Replication: GEN6.

### 2.5 Outside the requested review: the new "Corollary 5" (their commit `22cf1a6`, 17:33 UTC)

*This paragraph is not part of the review.  The coordinator asked, if time allowed, whether the chain of reductions of the new
Corollary 5 keeps the number of strands linear in the size of the 3-dimensional-matching instance.  I read the corollary with
read-only git (`git diff fc4b238 22cf1a6`); it replaces the conjectural bullet of l.243–247; §§1–4 of the note are unchanged.*
The chain is: (i) under ETH, 3DM with q elements per class and O(q) triples has no 2^{o(q)} algorithm (cited at second hand);
(ii) Garey–Johnson's transformation maps a 3DM instance with triple set T to a 4-PARTITION instance with 4|T| items and sizes
polynomial in q; (iii) Theorem 1 gives c = 4|T| + 1 strands and N = poly(q) bases.  **The count in (ii) is right as far as I can
check it**: by [DSW]'s overview of that transformation `[full text]` there is one item for every occurrence of an element in a
triple — "for each element x ∈ X, we introduce N(x) elements […] where N(x) is the number of times x appears in T", likewise for
Y and Z — and one item per triple, i.e. 3|T| + |T| = 4|T| items in |T| groups.  So **the number of strands is linear in the number
of triples, c = 4|T| + 1; it is linear in q exactly under the hypothesis |T| = O(q) that step (i) supplies.**  Not checked by me:
the sizes ([DSW]'s overview does not give them; that they are polynomial in q is `[from memory — unverified]`), and step (i)
itself — neither the cited source nor the paper through which it is cited was opened.  One caution from memory: the textbook
transformation from 3-SAT to 3DM is far from linear in size, so step (i) does need the dedicated linear-size result it cites.
With (H2\*) in place of (H2) the corollary is unchanged.  The closing sentence about optimality relies on `STRANDS_ALGORITHM.md`,
which is not my object and which I did not read; a lower bound for "MFE ≤ k on the connected ensemble with the symmetry term"
matches an upper bound only if the algorithm solves that same problem.

---

## 3. My enumeration, with its controls (Item 4) — **replication**

### 3.1 The code (written from §1 of the note; their code was opened only after `r20_enum.py` was frozen)

`r20_enum.py`: for each of the (c−1)! cyclic orders the bases are laid on a circle; **all** non-crossing matchings of complementary
bases are generated as words over {unpaired, open, close}; the faces are traced as the cycles of the map "after the link
p → p+1, follow the chord at p+1 if there is one"; a face is recorded with its number of nicks, its number of chords and its
segments, and typed exactly as in l.47–53; connectivity is computed separately by union–find over bases; R(S) by trying every
rotation by whole strands; "the cyclic order of S" also from S alone, by walking backwards round the face of each nick.  An
optional pruning abandons a partial structure when a face receives its second nick.  Energies are integers.

### 3.2 Validation of the enumerator, with controls (`r20_validate.py`; logs `validate_with_controls_seed20261126.log`, `…seed7.log`)

189 systems per seed (random words over subsets of {A,C,G,T}, 1–4 strands, some with wobble pairs allowed, and small packing
instances; up to 13 bases); for each, **all** matchings — crossing or not — are listed by a separate recursion and tested for each
cyclic order by a direct pairwise crossing test.  Seed 20261126: 48 034 matchings, 50 867 non-crossing (order, structure) pairs,
7 808 connected labelled structures (seed 7: 47 546 / 51 142 / 7 560).

| check | violations (both seeds) | control that must fail | its violations (seed 20261126 / seed 7) |
|---|---|---|---|
| V1 enumeration = brute force | 0 | C1: the crossing test removed from the reference | 108 / 99 systems |
| V2 number of faces = \|S\| + 1 | 0 | C2: the same count on crossing matchings | 466 114 / 466 421 |
| V3 Fact 1 (union–find = depth-first search = "no face with two nicks"; then c exterior faces) | 0 | C3: threshold "three nicks" | 29 845 / 30 124 |
| V4 a connected structure is non-crossing for exactly one cyclic order, the one computed from S alone | 0 | C4: the same demanded of disconnected structures | 9 406 / 9 332 |
| V5 the pruned enumeration yields exactly the connected structures | 0 | C5: compared with all structures | 157 / 159 systems |

(The first run of V5 failed — a bug of mine, §7.2.)

### 3.3 Theorems 1 and 3 on packing instances (`r20_theorem.py`)

For every instance the packing side is computed by brute force independently of the structures (solvability over all maps to bins;
Til by listing all arrangements; L by counting partitions; the set of tiling structures explicitly).  Then all connected
unpseudoknotted structures are enumerated over all n! cyclic orders and, for each loop-energy function, the statements are tested:
**S1** solvable ⇒ min = E\*; **S2** not solvable ⇒ min ≥ E\* + gap; **S3** the set of structures of energy E\* equals the set of
tiling structures (membership, not only the number); **S4** their number is Til; **S5** the number of their orbits under
permutations of equal items (brute-force canonical forms) is Til / Π μ_s!; and, independent of the energy: **U1** st(S) ≤ M with
equality attained iff solvable; **U2** R(S) = 1; **U3** the order computed from S alone is the order of generation; **U4** every face
has at most one nick and exactly c have one; **U5** (with `--orbits`) permutations of equal items act freely on all of Ω(I).
The terms (c−1)ΔG_assoc and k_BT ln R are the same for all structures (U2), so they are left out of the comparison.

Loop-energy functions (σ = stack energy; exterior loops 0 unless said): **class H — inside (H0)–(H2)**: H1 stack-only (σ = −1);
H2 penalties (σ = −3; bulge 2+u, interior 3+u, multiloop 4+k+u); H3, H4 pseudo-random non-negative integers per loop shape and
letters (σ = −5, values 0..9; σ = −2, values 0..3); H5 the boundary case (σ = −7, all other loops exactly 0).
**Class GEN — my statements (P1)–(P5)**: GEN1, GEN2 negative bulges/interior loops/multiloops within (H2\*); GEN3 flush nick κ = σ/2;
GEN4, GEN7 flush nick κ = σ with positive loops, resp. only the separator bulge positive (evaluated for B ≥ 2); GEN5 dangles with
|σ| > D_G + D_C; GEN6 a constant on every exterior loop.  **Class CTRL — must fail**: CTRL1 (H0) dropped — a flush nick ("stack
across a nick") gets σ, bulges 0; CTRL2 (H2) dropped — bulges get σ; CTRL3 (H1) dropped — σ = 0; CTRL4 (H2\*) at δ = 0; CTRL5
dangles with |σ| < D_G + D_C.

Runs (each reached its last line; the logs are in `logs/`):

| set | instances (solvable / not) | sizes | connected labelled structures | extra checks | log |
|---|---|---|---|---|---|
| `small` | 43 (24 / 19) | m ≤ 3, N ≤ 20, ≤ 6 strands | 2 526 779 | run 1: unpruned enumeration + union–find gives the same number of connected structures in all 43; U5 | `theorem_small_run1.log` (16 functions), `theorem_small_run2_17models.log` |
| `edge` | 14 (8 / 6) | B = 1; a single item; all items of length 1; an item longer than a block | 15 013 | as above | `theorem_edge_run2.log` |
| `medium_a` | 5 (3 / 2) | m = 2, B = 5, N = 21 | 5 125 260 | — | `theorem_medium_a_run1.log` (16 functions) |
| `medium_b` | 4 (2 / 2) | (3,3,3,1 \| 2,5), (4,2,2,2 \| 2,5), (2,2,2,1,1,1 \| 3,3), (3,3,1,1,1 \| 3,3); N ≤ 21, ≤ 7 strands | 4 379 304 | — | `theorem_medium_b_run2.log` |
| `their_extra` | 1 (1 / 0) | (3,2,2,1,1 \| 3, 3), N = 20 | 513 120 | — | `theorem_their_extra_run1.log` |
| `medium_c`, `medium_d` (one order per class) | 2 (1 / 1) | (2,2,2,2,2 \| 2,5), (3,2,2,2,1 \| 2,5); N = 21 | 7 683 480 (589 645 visited) | — | `theorem_medium_c_reduced_run1.log`, `theorem_medium_d_reduced_run1.log` |
| `large_reduced_a` (one order per class) | 3 (2 / 1) | (2,2,2,2,2,2 \| 2,6) — 3-PARTITION-shaped —, (2,2,2,2,2,2 \| 3,4), (3,3,3,3 \| 3,4); N = 25, 26 | 571 111 224 (2 376 611 visited) | — | `theorem_large_reduced_a_run1.log` |
| `large_reduced_b` (one order per class) | 2 (1 / 1) | (3,3,3,3 \| 2,6), (4,4,4 \| 2,6); N = 25 | 53 302 254 (3 969 706 visited) | — | `theorem_large_reduced_b_run1.log` |

"One order per class": only the cyclic orders in which equal items appear in increasing index order are enumerated, and counts
are multiplied by Π μ_s! — exact because relabelling equal items is a bijection on labelled structures (the free action is
checked directly by U5 in `small` and `edge`); on the `tiny` set this mode reproduces the full enumeration number for number
(`theorem_tiny_reduced_run1.log`), and its totals for (2,2,2,2,2 | 2,5) and (3,2,2,2,1 | 2,5) equal those of a separate counting
pass over all orders (`count_medium_cap45.log`: 4 363 800 and 3 319 680).

**Totals** (`logs/aggregate_full_enumeration.txt`, `aggregate_reduced_orders.txt`, `aggregate_all.txt`).  All orders: **67 instances
(38 solvable, 29 not), 12 559 476 connected labelled structures**, each decomposed into faces.  One order per class: 7 more instances
(4 solvable, 3 not), 6 935 962 structures decomposed, standing for 632 096 958 labelled ones.  Together **74 instances (42 solvable,
32 not)**.

| | violations |
|---|---|
| U1 (st ≤ M; maximum M iff solvable), U2 (R = 1), U3 (unique order), U4 (faces and nicks), on all 74; U5 (free action) on the 57 instances of `small` and `edge` | **0** |
| S1–S5 and the decision "min ≤ E\* ⇔ solvable", H1–H5 (inside (H0)–(H2)), on all 74 | **0** |
| the same for GEN1, GEN2 (statement (P1)), GEN3 ((P2a)), GEN5 ((P3)), GEN6 ((P5)), on all 74 | **0** |
| the same for GEN4 ((P2b)) on the 67 instances with B ≥ 2, and GEN7 on the 62 of them that were run with it | **0** |


A few reference values (they agree with the Complexity division's log wherever it has the instance, §4):

| instance (a \| m, B) | N | solvable | connected labelled structures | Til | Til / Π μ_s! | minimisers, stack-only |
|---|---|---|---|---|---|---|
| (3,3,2 \| 2,4) | 17 | no | 46 002 | 0 | 0 | 70 at σ(M−1) |
| (2,2,2,2 \| 2,4) | 17 | yes | 87 576 | 24 | 1 | 24 |
| (3,2,2,1,1 \| 3,3) | 20 | yes | 513 120 | 48 | 12 | 48 |
| (2,2,2,2,1 \| 3,3) | 20 | no | 676 920 | 0 | 0 | 2 400 at σ(M−1) |
| (4,3,3 \| 2,5) | 21 | no | 836 544 | 0 | 0 | 38 at σ(M−1) |
| (3,3,2,2 \| 2,5) | 21 | yes | 1 887 888 | 16 | 4 | 16 |
| (2,2,2,2,2,2 \| 2,6) | 25 | yes | 265 899 600 | 720 | 1 | 720 |

### 3.4 The controls that must fail

Number of instances (of 74; 32 not solvable) on which the note's Theorem 1, read literally, is violated when one hypothesis is
dropped — S1: a solvable instance whose minimum is not E\*; S2: a non-solvable instance whose minimum is below E\* + gap; S3: the
structures at E\* are not the tiling structures; "wrong": the decision "min ≤ E\* ⇔ solvable" is wrong:

| control | S1 | S2 | S3 | wrong decisions |
|---|---|---|---|---|
| CTRL1 — (H0) dropped: a flush nick ("stack across a nick") gets σ; bulges 0 | 30 | 23 | 53 | 23 of 32 |
| CTRL2 — (H2) dropped: every bulge gets σ | 0 | 32 | 51 | 32 of 32 |
| CTRL3 — (H1) dropped: σ = 0 | 0 | 0 | 66 | 32 of 32 |
| CTRL4 — (H2\*) at δ = 0: non-stack loops get σ·b(f) | 0 | 32 | 57 | 32 of 32 |
| CTRL5 — dangles with \|σ\| < D_G + D_C, tested against the prediction of (P3) | 34 | 24 | 52 | 24 of 32 |

Every control fails, as it must.

The control asked for in the brief — (H0) dropped by rewarding a stack across a nick — is CTRL1.  Smallest example: a = (3,1),
m = 2, B = 2 (template `GGAGG`, items `CCC` and `C`), not solvable, M = 2.  With the flush nick rewarded like a stack, the
structure "`CCC` on the last two G's with its third base on the second G (crossing the separator), `C` on the first G" has one
stack and one flush nick: energy 2σ = σM.  So the minimum of a non-solvable instance equals the value that Theorem 1 reserves for
solvable ones; the enumeration finds exactly 2 such structures.

### 3.5 Supplementary replications

* **(P4), several complexes** (`r20_assoc.py`, `assoc_run1.log`): 22 instances; for every sub-multiset J of the items the connected
  minimum of template + J was enumerated (2 036 774 structures), for the functions H1, H2, H3 and association energies
  A ∈ {−2, 0, 1, 2, 3, 4, 7}.  Cases with |σ|(a_i − 1) > A for all i: 245, **0 violations** of the claim.  Control, cases where
  some item does not gain by binding: 217, the decision "minimum ≤ σM + nA ⇔ solvable" is **wrong in 68**.
* **Counting identities on the packing side** (`r20_packing_identities.py`, `packing_identities_run2.log`): Til = L·m!·6^m on 14
  3-PARTITION-shaped instances (m = 2, 3; including two non-solvable ones), Til = L·m!·24^m on 6 4-PARTITION-shaped instances
  (m = 2); Π μ_s! divides Til; 0 violations; the control (the other factor) fails on all 17 instances with L > 0.

### 3.6 What this replication covers that their test does not

Set equality of minimisers and tiling structures (their test compares numbers); R(S) = 1 on every structure; the orbit count of
Theorem 3.2; the free action on all of Ω(I) (needed for Corollary 4(ii) in the physical ensemble); Fact 1 against two independent
connectivity computations; five loop functions inside the hypotheses, instances with B = 1, with a single item, with items longer
than a block; controls for each hypothesis.  It does **not** go beyond N = 26.

---

## 4. Re-runs of their code (Item 4) — **re-run**

Their three scripts and their log were copied to `experiments/science/ws_R20/rerun_copy/` (sha256 identical to `<CX>`) and run
unmodified with `python3 -I -B`.  Isolated mode does not put the script's directory on the module path, and their test does
`from ref_enum import *`; my drivers insert the directory and execute the script with `runpy` (no change to their files).  Every
process ran under an address-space cap of 2 GB.

1. **`test_partition_reduction.py` — completed.**  `rerun_their_small_test_run1.log`: 12 lines "OK" (6 cases × 2 loop functions),
   final line "ALL OK", 1.4 s, 16 MB.
2. **`test_partition_reduction_big.py` as shipped — does not complete.**  The first 10 cases × 2 loop functions print "OK" with
   exactly the numbers of their `big_run.log`; at the 11th case ([3,2,3,2], m = 2, B = 5; 1 887 888 structures) the process stops
   with `MemoryError` under the 2 GB cap (maximum resident size 1997 MB, after 502 s), because `run` keeps every labelled
   structure in the set `seen`.  **Their own `big_run.log` ends at exactly this point**: 20 lines for 10 cases, no line for cases
   11 and 12, no final "ALL OK".  The log of my stopped run is in `not_cited/` and is not used as evidence.
3. **The same 12 cases, one process each** (`r20_rerun_cases.py`: the list `cases` is read from their script, their function `run`
   is called exactly as their script calls it): `rerun_their_big_cases_one_process_each_run1.log`, completed in 462 s.  **11 of the
   12 cases are "OK" in both loop functions** (22 lines; the numbers of their log, and in addition case 12, [4,3,3], which their
   log lacks).  **Case 11 stops with `MemoryError` under 2 GB** — the largest case that fits, 836 544 structures, already needs
   1.4 GB, and case 11 has 1 887 888.  So for this case there is no completed run of their code, neither theirs nor mine; my
   own enumeration covers the instance (§3.3, (3,3,2,2 | 2,5): Til = 16, 0 violations).
4. **Their enumerator with `check=True`** (`r20_rerun_check_true.py`, `rerun_their_enum_check_true_run1.log`): on 10 cases, with
   `connected_only=False`, 1 099 956 non-crossing (order, structure) pairs, **no assertion failed** — the check that §1 of the note
   describes, and that their own scripts never switch on, passes.

Comparison of their numbers with mine (replication), for every instance both have:

| instance | connected structures (theirs = mine) | their "#MFE-structures", stack model = my minimisers of H1 | their "labelled tilings" = my Til |
|---|---|---|---|
| (2,2,1,1 \| 2,3) | 2 040 | 16 | 16 |
| (2,2,2 \| 2,3) | 2 262 | 102 | 0 |
| (3,1,1,1 \| 2,3) | 1 536 | 12 | 12 |
| (3,3 \| 2,3) | 1 514 | 2 | 2 |
| (3,2,2,1 \| 2,4) | 66 552 | 8 | 8 |
| (3,3,2 \| 2,4) | 46 002 | 70 | 0 |
| (3,3,1,1 \| 2,4) | 50 568 | 16 | 16 |
| (2,2,2,2 \| 2,4) | 87 576 | 24 | 24 |
| (3,2,2,1,1 \| 3,3) | 513 120 | 48 | 48 |
| (3,2,2,2 \| 3,3) | 409 488 | 300 | 0 |
| (2,2,2,2,1 \| 3,3) | 676 920 | 2 400 | 0 |
| (4,4,2 \| 2,5) | 762 294 | 70 | 0 |
| (4,3,3 \| 2,5) | 836 544 | 38 | 0 |
| (3,3,2,2 \| 2,5) | theirs: not completed; mine: 1 887 888 | mine: 16 | mine: 16 |

Two independently written enumerators (theirs by interval recursion and a walk inside each chord, mine by open/close words and
cycles of the link permutation) agree on every number.  Their minima in the "random" model with σ = −3 on the non-solvable
instances (−12, −12, −9, −18, −18) equal my minima for H2, which also has σ = −3.

---

## 5. Novelty, as far as a short search can say (Item 5)

### 5.1 The three statements of the coordinator's search, checked against the papers

1. **Condon, Hajiaghayi, Thachuk, DNA 27 (2021)** — "NP-hard and APX-hard for unboundedly many strands in a simple energy model".
   **Confirmed** `[sections read: §§1, 2.1, 2.2, end of §5, §§6–7; the reduction itself not read]`.  Abstract: "we prove that for a
   simple energy model, the problem of predicting the MFE pseudoknot-free secondary structure formed from multiple interacting
   nucleic acid strands is NP-hard and also APX-hard."  The model (§2.1) is E(S) = p(−1) + (m − l)K_assoc for m strands in l
   complexes with p base pairs — several complexes are allowed; "The hardness result holds whether or not rotational symmetries
   are accounted for in the energy model."  About richer models only: "it would seem unlikely that the prediction problem becomes
   easier if the energy model is more sophisticated."
2. **Ducloz, Shalaby, Woods, DNA 31 (2025)** — "the partition function is #P-hard for unboundedly many strands in base-pair
   models, hardness in the nearest-neighbour model conjectured".  **Confirmed** `[full text of arXiv:2506.19756v1; numbering
   checked against the proceedings PDF]`.  Table 1: unbounded strands, unpseudoknotted — "NP-hard [5]; BPM model", "#P-hard
   [Theorem 38]; BPM model"; caption: "Negative, or hardness, results are proven in the simple BPM or BPS models and are
   conjectured [5] to hold in the more complex NN model."  And the question itself, §1.3: "1. MFE hardness in two settings is
   still an open question: Is MFE NP-hard for NN single-strand pseudoknotted, or NN O(n)-strands unpseudoknotted? If so, can the
   reduction map be leveraged to show hardness results for PF and #SSEL in the NN model?" — the note quotes it verbatim.
3. **Shalaby, Woods, ICALP 2025** — "the nearest-neighbour case for unboundedly many strands listed as open".  **Confirmed for the
   proceedings version** `[sections read: abstract, Table 1, §1 footnotes, §1.4, §2]`: caption of Table 1, "Results are proven in
   the nearest neighbour energy model studied here, except the APX-hardness result which is proven in the maximum matching model
   [9], and still open for nearest neighbour model."  The sentence is **not** in arXiv:2407.09676v1 (July 2024), whose Table 1
   lists only the partition function as an open problem for unbounded strands.
4. (Not asked, but it dates the question.)  **Shalaby, Woods, arXiv:2611.27945v2 (23 Nov 2026)** `[sections read]`: Table 1
   caption, "Positive results are proven in the nearest neighbour model studied here, negative/hardness results in the simpler
   base pair matching (BPM) model [5, 16]"; footnote 9: "hardness results in such simple settings intuitively suggest hardness
   should carry over to the more realistic nearest neighbour model."  Three days before the note, the authors of the question
   still had no nearest-neighbour hardness proof to cite.  Every quotation of [DSW] and [SW26] in the Complexity division's
   files that I compared with the sources (Future work 1–5 of [DSW]; Future work 1–4, Def. 7, Def. 11, Table 1 caption of [SW26];
   the theorem and lemma numbers 22, 31, 32, 33, 38 and Defs 11, 14–18, 25 of [DSW]) is accurate.

### 5.2 Classification

* **(iii) It answers a question that two papers state as open** — [DSW] Future work 1 and the caption of Table 1 of [SW25]
  (sentences above) — *in the model as those papers define it* (connected unpseudoknotted structures, association and symmetry
  terms, exterior loops 0 "by definition"), for every loop table satisfying (H1) and (H2), or the weaker (H2\*) of F2.  I did not
  check that the particular tables those papers point to satisfy (H2\*) on every loop that can occur in the instances (I looked
  up one bulge rule), so the accurate sentence is "for every loop-energy function with exterior loops 0 satisfying (H1) and
  (H2\*)", not "for the nearest-neighbour model of [DSW]".
* **(ii) It is not a corollary of the three papers**, with two caveats.  (a) [CHT] and [DSW] Thm 38 are base-pair-model results
  and [DSW] Thm 32 / [L04] concerns one strand with pseudoknots; none gives hardness for stack-driven energies of many strands.
  But on the connected ensemble the base-pair model is itself a loop model (F11), so *for an unrestricted loop function that is
  part of the input* hardness already follows from [CHT]; the note's contribution is the physical sign pattern and a fixed
  function.  (b) The gadget is [L04]'s as used in [DSW] Thm 32 (F1); the step added — cut the strand, let the strand order replace
  the crossings — is small, as the division's own `PRIOR_ART.md` says.
* **(i) New as far as I can see**, within these limits: no such proof in the five papers opened, none in two generic searches
  (summaries only), and the authors of the question cite none in their preprint of 23 Nov 2026.  A short search cannot establish
  novelty.

### 5.3 Search log (2026-11-26; generic queries only; nothing of this project was put into a query; nothing was uploaded)

1. `Dirks Bois Schaeffer Winfree Pierce "Thermodynamic analysis of interacting nucleic acid strands" SIAM Review 2007 pdf` → the Caltech repository record.
2. `Shalaby Woods "An efficient algorithm to compute the minimum free energy of interacting nucleic acid strands" ICALP 2025 LIPIcs` → the proceedings PDF.
3. `Lyngsø "Complexity of pseudoknot prediction in simple models" ICALP 2004 bin packing base pair stacking pdf` and
4. `Lyngsø "Complexity of pseudoknot prediction in simple models" author copy pdf stats.ox.ac.uk OR citeseerx OR semanticscholar` → bibliographic data and an abstract summary only; no accessible copy.
5. `NNDB Turner 2004 bulge loops "special C bulge" "number of states" nearest neighbor database RNA folding free energy` → the [NNDB] pages.
6. `NP-hard minimum free energy multiple nucleic acid strands unpseudoknotted "nearest neighbour" OR "nearest neighbor" OR "stacking" model unbounded number of strands hardness proof 2025 2026` → only the papers above `[search summary]`.
7. `"3-partition" OR "bin packing" reduction multi-stranded DNA "base pair stacking" OR "stacking energy" complexes NP-hard template strand short strands nick coaxial` → nothing relevant beyond [DSW] `[search summary]`.

### 5.4 Sources: what was opened and what was read

| source | URL | what I read |
|---|---|---|
| [DSW] full version | https://arxiv.org/pdf/2506.19756v1 (abstract page https://arxiv.org/abs/2506.19756) | all of it (text conversion, 1706 lines, incl. Appendix A) |
| [DSW] proceedings (DNA 31, LIPIcs 347, 1:1–1:23) | https://drops.dagstuhl.de/storage/00lipics/lipics-vol347-dna31/LIPIcs.DNA.31.1/LIPIcs.DNA.31.1.pdf | numbering of Defs/Thms, Future work 1, Thm 32 in App. B.3 |
| [CHT] (DNA 27, LIPIcs 205, 9:1–9:21) | https://drops.dagstuhl.de/storage/00lipics/lipics-vol205-dna27/LIPIcs.DNA.27.9/LIPIcs.DNA.27.9.pdf | §§1, 2.1, 2.2, end of §5 (K_assoc), §§6–7 |
| [SW25] proceedings (ICALP 2025, LIPIcs 334, 130:1–130:20) | https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/LIPIcs.ICALP.2025.130/LIPIcs.ICALP.2025.130.pdf | abstract, Table 1, footnotes of §1, §1.4, §2.1–2.2 |
| [SW25] arXiv v1 | https://arxiv.org/pdf/2407.09676v1 (abstract page https://arxiv.org/abs/2407.09676) | pp. 1–10 (abstract, Table 1, §§1–2.3), the exterior-loop case of the algorithm |
| [SW26] | https://arxiv.org/pdf/2611.27945v2 (abstract page https://arxiv.org/abs/2611.27945) | Table 1 and caption, §1.5, Def. 7, Def. 11, Remark 12, footnotes 9 and 19 |
| [D07] | https://authors.library.caltech.edu/records/p98fy-fvv11/files/DIRsiamrev07.pdf (record https://resolver.caltech.edu/CaltechAUTHORS:DIRsiamrev07) | Fig. 1.1 caption, §2.1, start of §2.2, Fig. A.1 caption, Appendix B notes 3, 5, 13 |
| [NNDB] bulge loops, RNA 2004 | https://rna.urmc.rochester.edu/NNDB/rna_2004/rna_2004_bulge_loops.html | the page text (equations and the two worked examples) |
| [NNDB] coaxial stacking, RNA 2004 | https://rna.urmc.rochester.edu/NNDB/rna_2004/rna_2004_coaxial_stacking.html | only the fetch tool's summary with short quotations |
| [L04] | https://link.springer.com/content/pdf/10.1007/978-3-540-27836-8_77.pdf ; https://api.crossref.org/works/10.1007%2F978-3-540-27836-8_77 ; https://unpaywall.org/10.1007%2F978-3-540-27836-8_77 | **not obtained**: the publisher's link returned a script "client challenge" page (not worked around); Crossref metadata only; the redirect of the third link was not followed |
| (a wrong guess of mine) | https://rna.urmc.rochester.edu/NNDB/turner04/bulge.html | HTTP 404 |

Not opened at all: [GJ]; Boehmer–Berkemer–Will–Ponty (WABI 2024) and Demaine et al. (DNA 30), which the division's `PRIOR_ART.md`
lists as multi-strand hardness results in base-pair and domain-level models.

---

## 6. Requests to the Complexity division (can be sent as they stand), and next steps

### 6.1 Requests (each can be sent as it stands; the replacement texts are in §2.3)

* **REQ-A (F1).**  Put the source of the gadget into the note itself: Lyngsø (ICALP 2004) and Ducloz–Shalaby–Woods Theorem 32, with
  the replacement texts of F1; and read Lyngsø's paper, which neither you nor I have opened.
* **REQ-B (F2).**  Replace (H2) by (H2\*) — "there is δ > 0 with g(f) ≥ σ·b(f) + δ for every bulge, interior loop and multiloop f,
  b(f) the number of item bonds on f" — with the five-line proof (P1) of §2.4 of this report, change part 2 of Theorem 1 to
  "≥ σM + nΔG_assoc + min(|σ|, δ)", delete "the sign pattern of every physical parameter set" (l.14) and rewrite §6.2: the 2004 RNA
  rules have favourable single-nucleotide bulges (−0.13 kcal/mol in the worked example of the Nearest Neighbor Database).
* **REQ-C (F3).**  Replace Remark 3 by the three cases of (P2): flush nick energy κ with σ < κ ≤ 0 (survives, E\* = σM + κ(n − m));
  κ = σ with the separator bulge > 0 (survives for B ≥ 2, E\* = σ·m(B − 1)); κ = σ with that bulge = 0 (fails).  Check my proofs.
* **REQ-D (F4, F5, F6).**  State Corollary 4(ii) for an integer Boltzmann weight (one oracle call, digits in base x) or with an
  explicit precision; state NP-membership with the convention for k_BT ln R(S); state that #4-PARTITION is used with polynomially
  bounded weights and why that is legitimate.
* **REQ-E (F7, F8, F9, F11).**  Cite Dirks et al. (App. B note 3) and the appendix of the full version of Ducloz–Shalaby–Woods for
  ΔG_exterior = 0; state the pairing rule the theorem needs and the one-complex formulation in the theorem (both already promised
  in your `COMPLEXITY-RES-0001`); add the "several complexes" remark (P4); add to Remark 4 that the
  base-pair model is a loop model on the connected ensemble, so that the reader sees what the sign conditions buy.
* **REQ-F (F10).**  Repair the verification section: (i) run the enumerator with `check=True` in a script that is part of the
  re-run instructions; (ii) `test_partition_reduction_big.py` does not finish — at its 11th case it needs more than 2 GB because
  `run` stores every structure in `seen`; store 64-bit hashes or use the order computed from the structure instead, and
  regenerate `big_run.log` (the shipped one ends after 10 of 12 cases, without "ALL OK"); (iii) add assertions for what
  Theorems 1 and 3 actually say: the set of minimisers equals the set of tiling structures, R(S) = 1, the orbit count of
  Theorem 3.2.  Reference values from my independent enumeration are in §3 of this report (e.g. (3,3,2,2 | m=2, B=5): 1 887 888
  connected structures, 16 labelled minimisers, 4 orbits).
* **REQ-G (question, not a correction).**  Your `RESEARCH_LOG.md` plans "robustness of the reduction to non-zero exterior-loop
  energies".  Statements (P2) and (P3) of this report are a start: coaxial stacking alone does not break the reduction when the
  separator bulge is unfavourable; with one dangle term per unpaired base it survives if |σ| > D_G + D_C.  Is either condition
  met, or violated, by a published table with dangles and coaxial stacking (flush and mismatch-mediated)?  That decides whether
  the result extends from the model as written in the papers to the model as implemented.

### 6.2 The three most promising next steps (for whoever continues)

1. The question of REQ-G for one concrete published table: either a proof that the reduction survives (it needs the table's
   numbers for G/C dangles, the flush and mismatch-mediated coaxial terms and the separator bulge), or an explicit small instance
   on which it fails, and then a redesigned gadget (for instance blocks that are not homopolymers, to remove the degeneracy and
   dangle effects of long runs).
2. Their A3′ (#P-hardness of the partition function at a *fixed* temperature): the leading coefficient of Z_I(x) is the count of
   Theorem 3; the natural attempt is padding that makes the top level dominate at fixed x.  [C] — no evidence either way.
3. The dependence on the number of strands and species: an ETH lower bound 2^{Ω(c)} needs a linear-size chain of reductions to
   4-PARTITION with polynomially bounded numbers (their CX-C1, unverified), and hardness for boundedly many species is their C2.

Requests to the theory division or the engineering division: none.

---

## 7. What I did not check; my own errors; files

### 7.1 What I did not check

* **Sources.**  [L04] was not opened (F1 rests on [DSW]'s account of it); [GJ] was not opened (theorem numbers and the
  pseudo-polynomiality of the 3DM → 4-PARTITION transformation are from memory); of [CHT] I read the introduction, the model, the
  K_assoc paragraph and the conclusions — **not the reduction**, so the statement in F11 that its hardness holds on the connected
  ensemble rests on one sentence of the paper; [SW25], [SW26], [D07] only in the sections listed in §5.4; the [NNDB]
  coaxial-stacking page only through the fetch tool's summary; Boehmer et al. (WABI 2024) and Demaine et al. (DNA 30) not at all.
* **Tables.**  I compared exactly one published loop rule with the hypotheses (the RNA-2004 single-nucleotide bulge).  I did not
  check (H2\*), (P2) or (P3) against any published table of dangles, coaxial stacking, interior loops or multiloops; the remarks
  on which features the implemented models have are from [D07]'s own sentences and, for coaxial stacking, from the [NNDB] summary.
* **Sizes.**  Enumeration over all strand orders only up to N = 21 bases and 7 strands; with one order per symmetry class up to
  N = 26 and 7 strands.  The only 3-PARTITION-shaped instance with m ≥ 2 that I enumerated is (2,2,2,2,2,2 | 2, 6); no 4-PARTITION-shaped
  instance with m ≥ 2 (the count formulas for these shapes were checked on the packing side only).  The proof is elementary and
  does not depend on size, but the replication cannot see anything that would only appear at larger sizes.
* **My own statements (P1)–(P5)** are unreviewed paper proofs, tested on the instances of §3 only.
* **Their other material.**  Section 5 of the note (the ETH remark, "for a bounded number of species the problem is expected to be
  polynomial") was read only; `OPEN_PROBLEMS.md`, `PRIOR_ART.md` beyond the quotations listed in §5.1, and everything about
  phylogenetic networks were not reviewed; `symmetry_orbits` in `ref_enum.py` was not exercised; the 11th case of their big test
  was not re-run with their code (it needs more than 2 GB).
* No Lean formalisation.

### 7.2 My own errors (all caught before they reached a cited result)

1. A bug in my enumerator's pruning (the wrap-around nick was counted twice, so the pruned enumeration returned nothing): caught by
   my validation check V5 on its first run (135 violations); fixed; log in `not_cited/`.
2. Two invalid instances in my own lists — (6,5,4,4,4,3 | 2, 13), not 3-PARTITION-shaped, and (7 | 2, 3), sum ≠ mB — both stopped
   by my assertions; the two aborted logs are in `not_cited/`.
3. Procedure: the first `small` run took 6.5 minutes and I had not written its cost into the notes beforehand; I started two
   compute processes in parallel on a loaded machine, saw that one batch would exceed 20 minutes of wall-clock time, and stopped
   one (its empty log is in `not_cited/`); afterwards one process at a time.
4. A first version of the function counting item bonds on a loop used a non-overlapping substring count; found on re-reading,
   fixed before the first run.
5. A time in the notes was first written as "16:3x"; replaced by the clock value.
6. Two statements in my first-pass notes were from memory (that the 2004 bulge rule can be negative; the Garey–Johnson theorem
   numbers); the first was then verified at the source, the second is still from memory and is marked so.
7. The fetch tool's summary gave the title of [SW26] with a word missing; the PDF agrees with the Complexity division's citation.

### 7.3 Files

In `experiments/science/ws_R20/`:

| file | content |
|---|---|
| `NOTES.md` | chronological record (kept from the first minute); list of tool actions declined |
| `r20_enum.py` | my enumerator (frozen before I opened their code; sha256 `a1d3a901…3e286c`) |
| `r20_validate.py` | validation of the enumerator against brute force over all matchings, with five controls |
| `r20_theorem.py` | Theorems 1 and 3 on packing instances; 17 loop-energy functions (5 inside (H0)–(H2), 7 for (P1)–(P5), 5 controls) |
| `r20_assoc.py` | the "several complexes" variant (P4) |
| `r20_packing_identities.py` | Til = L·m!·6^m, L·m!·24^m on the packing side |
| `r20_count.py`, `r20_aggregate.py` | counting pass used for planning; totals of the logs |
| `r20_rerun_driver.py`, `r20_rerun_cases.py`, `r20_rerun_check_true.py` | drivers that run their unmodified code from `rerun_copy/` |
| `rerun_copy/` | scratch copy of their three scripts and their log (sha256 equal to `<CX>`; not to be committed) |
| `logs/` | logs of runs that reached their last line (the only ones cited) |
| `not_cited/` | logs of stopped or failed runs (five) |

and this report, `docs/science/workstreams/R20_REPORT.md`.  Outside the repository, in the session scratchpad only: the downloaded
papers with their text conversions (`…/scratchpad/r20_lit/`) and one debugging script.  Nothing else was written anywhere;
`<CX>` was not touched; no git command that changes state was run (read-only `git log`, `git diff`, `git show`, `git ls-tree`,
`git cat-file`, `git branch -a` only).

How to re-run (from `experiments/science/ws_R20/`, single thread, each command well under 20 minutes on a free core):
`python3 -I -B r20_validate.py 20261126` · `python3 -I -B r20_theorem.py small --crosscheck --orbits` ·
`python3 -I -B r20_theorem.py edge --crosscheck --orbits` · `python3 -I -B r20_theorem.py medium_a` (also `medium_b`, `their_extra`) ·
`python3 -I -B r20_theorem.py large_reduced_a --reduce-orders` · `python3 -I -B r20_assoc.py` ·
`python3 -I -B r20_packing_identities.py` · `python3 -I -B r20_rerun_driver.py test_partition_reduction.py 2` ·
`python3 -I -B r20_rerun_cases.py` · `python3 -I -B r20_rerun_check_true.py`.

**Tool actions declined:** none by the permission system.  Two refusals of other kinds, recorded here so that the coordinator can
judge them: (1) the page-fetch tool twice declined to reproduce an abstract verbatim (its summariser quotes at most 125
characters); I did not ask again.  To *read* the papers I downloaded the open-access PDFs with `curl` through the session proxy
into a scratch directory outside the repository and converted them with `pdftotext` — a fetch of published papers, which the brief
permits; the quotations in this report are short passages for the purpose of review.  (2) The publisher's PDF link for [L04]
returned a script "client challenge" page instead of the paper; not pursued, the paper stays unopened.

## Coordinator's note (2026-11-26, after the hand-back; the report above is the referee's, unchanged)

*What I did with this report.*  Read: §§0–2 in full (the verdict, the statements, the step tables, all twelve
findings, the supporting statements (P1)–(P5), the paragraph on Corollary 5), §3.1–3.4, §4, §5.1–5.3, §6; §3.5–3.6,
§5.4 and §7 at the level of their headings and numbers.  **Checked:** (1) *Finding F2 at the source* — a second
reading of the Nearest Neighbor Database page for bulge loops of the RNA 2004 rules, by a fetch made for me: the
formula for a single-nucleotide bulge (initiation + special C bulge + base-pair stack − RT ln(states)) and the
worked example with the printed terms −3.42, −3.26, +4.09, +3.81, −0.9, −2.36, −0.616×1.099 are on the page as the
referee quotes them; the sum of the four bulge terms is −0.13 kcal/mol (the grouping of the terms is ours and the
referee's — the page does not group them).  (2) *Finding F1* — the same fetch could read the full version of
Ducloz–Shalaby–Woods only in part: title and authors verbatim; the construction (one strand, runs of `C` separated by
`A`, then `AAA`, then runs of `G`; target Σw − k; multiplicity (k/4)!·(4!)^{k/4}; an adaptation of Lyngsø's reduction)
and the open question of its "Future work 1" confirmed at the level of a summary; the theorem's number not verified
by me.  The referee read the full text.  (3) *The proof of (P1)* — the weaker hypothesis (H2\*) — re-derived by me:
the `M` item bonds split into those on stacks, those on other nick-free faces and those on exterior faces, and
`Σ_f g ≥ σ·st + Σ(σ·b(f) + δ) = σM + |σ|e + δ·ns`; correct, and (H2) is its case `δ = |σ|`.  (4) *The replication* —
`r20_validate.py` re-run with a seed of mine (31337): all five checks 0 violations, all five controls violated;
`r20_theorem.py tiny --crosscheck --orbits` re-run: PASS, and the control asked for in the brief on the referee's
smallest example (`a = (3,1)`, `m = 2`, `B = 2`, a stack across a nick rewarded): minimum `−2 = E*` on a non-solvable
instance, decision wrong, as reported.  Both logs are in `ws_R20/logs/` (`…_by_coordinator.log`).

*Two remarks on the record.*  (i) The logs named `…_run1.log` were produced before the referee added one more loop
function (GEN7) and one flag to `r20_theorem.py`; in the tiny set every line the two versions share is identical
(compared by me), and the report's totals come from the later runs and the aggregate files — but those `run1` logs
are not logs of the committed script.  (ii) **Finding F10 (ii) describes their log at `fc4b238`** (20 lines, no
final line).  At their later commits (`9a35d2f` on) `experiments/complexity/strands/big_run.log` has 25 lines and
ends "ALL OK": their run did finish on their machine; the referee's statement that the script cannot finish within
2 GB stands, and the published review says both.

*A point of process.*  The referee reports that the fetch tool's summariser twice declined to quote an abstract
verbatim and that it then downloaded the open-access PDFs (arXiv; the Dagstuhl proceedings; an institutional
repository) with `curl` into the session scratchpad and read them there, "flagged for your judgement".  My judgement:
these are public, open-access papers, read for a review that the brief asked to base on opened sources; nothing was
uploaded and nothing of the project was sent; a publisher page that answered with a script challenge was not
pursued.  The quotations in the report are short.  I record it here and for the research owner; the downloaded
files stay outside the repository.

*Verdict.*  I accept the review.  Published as SCI-REV-0019.  The referee's statements (P1)–(P5) are its own and
are sent as proposals with their proofs, not as reviewed results.

*Not in the repository:* `ws_R20/rerun_copy/` (the Complexity division's four files), `ws_R20/not_cited/`, the
`.err` side files, and the papers downloaded by the referee.
