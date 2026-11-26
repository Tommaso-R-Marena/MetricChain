# Workstream A3 — prior art: certifying a free energy by sampling from a model (box classes, floors, Rényi balls)

Science division, independent workstream A3.  Started 2026-11-25 23:33 UTC.
Statements positioned: **T1–T4** (theory division, forthcoming theory report §11.30; read in
`THY-RES-0007.md` §4 and in the theory `RESEARCH_LOG.md`, "Resume here (cycle 10, fourteenth
checkpoint)", item 1 (a)–(e), export `thy_ro_658b77f`) and **O1–O2** (ours: addendum A17 of
`docs/science/INFERENCE_LIMITS_ADDENDA.md`, statements A17.1–A17.6, which the coordinator declared
the authoritative version while this workstream was running).
Working files: `experiments/science/ws_A3/` (`NOTES.md` = step-by-step log with the complete search
log; `check_math.py` / `check_math.out` = numerical checks; `getpdf.sh`, `arxiv_q.py`,
`arxiv_batch.py` = the download helpers).  Downloaded papers are kept outside the repository
(scratchpad `a3_dl/`, text in `a3_txt/`) and are identified below by arXiv number, DOI or PMC id.

**Reading levels** (COMMON rule 5): `[full text]` — I had the paper's own text (PDF converted with
`pdftotext`, or the PMC full text) and read the passages named; `[abstract]`; `[search snippet]` —
only what a search engine or an automatic page summary returned; `[from memory — unverified]`.
**Epistemic labels** (rule 6): **[V]** machine-checked, **[P]** paper proof given here, **[K]** known and
cited, **[N]** numerical evidence only, **[C]** conjecture, **[H]** heuristic.
**Classification scheme of the brief:** **(1)** in print as stated; **(2)** a known special case or a
direct corollary; **(3)** folklore without a locatable statement; **(4)** not found after the searches
listed.  "Not found" never means "new".

## How far I got

*(status line, updated as the work proceeds — see the end of the file for what could not be accessed)*

IN PROGRESS — skeleton written 23:55 UTC; sections are filled as sources are read.

### Interim verdicts (written 00:04 UTC, 26 Nov; superseded by §1 when that is written)

* **T1** — **(1) in print as stated.**  Lower half: Jensen / Gibbs–Bogoliubov.  Upper half with the sharp
  constant: Specht's reverse arithmetic–geometric-mean inequality (1960) in its weighted form — `L(w) = ln S(e^w)`,
  `S` = Specht's ratio — and, independently, the maximal Kullback–Leibler divergence of a "bounded-range" pair
  in differential privacy (`maxkl`, Dong–Durfee–Rogers 2020), where the two laws are literally Gibbs
  measures (exponential mechanism).  `L(w) ≤ w²/8` is Hoeffding's lemma.
* **O2 / A17.6** — **(2) direct corollary of statements in print, and improvable:** `D_p(π_g‖π) ≤ (p−1)K/8 + Σ_i L(c_i)
  ≤ pK/8` (so `D_2 ≤ K/4`, not `K/2`; the factor `p/(p−1)` of A17.6 disappears) by "bounded range ⇒ zCDP"
  (Cesar–Rogers) and adaptive composition of Rényi divergences (Bun–Steinke Lemma 2.2).  Checked numerically.
* **O1 / A17.2–A17.4** — the unhinted rates (A17.3) are **in print** (Kunsch–Novak–Rudolf 2019, incl. lower
  bounds for general randomised algorithms using function values; Bubeck–Cesa-Bianchi–Lugosi 2013;
  Devroye–Lerasle–Lugosi–Oliveira 2016); the hinted cost for `p ≤ 2` is the same rate read backwards; the hinted
  exponent `p/(p−1)` for `p > 2` and the KL case were **not found as stated**, but the same family of classes
  with the same extremal pairs is in print for a neighbouring task (Block–Polyanskiy 2023: approximate
  rejection sampling, cost smaller by exactly the factor `ε`).
* **T2–T4** — still being read (K\* family, Dagum–Karp–Luby–Ross through secondary sources, free-energy
  perturbation literature).

