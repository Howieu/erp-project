# Design: Mathematical-Analysis Section + Overall Dissertation Structure

**Date:** 2026-06-25
**Project:** ERP dissertation — *Explainable customer segmentation: CLASSIX vs RFM+K-Means+ExKMC* (MSc Data Science, University of Manchester; supervisor & M10 proposer: **Stefan Güttel, CLASSIX's author**).
**Scope of this design:** (1) the new mathematical-analysis section (Ch3 §3.x), and (2) the locked overall 6-chapter narrative spine. Not in scope: drafting full chapter prose, full Ch3 lock, Ch2 search execution.

---

## 1. Central thesis (the through-line)

In e-commerce customer segmentation, when clustering **quality is competitive (no uniform winner)**, the deciding axis is whether the explanation can be acted upon. CLASSIX offers an **intrinsic, faithful-by-construction, k-free, fast, deterministic** self-explanation (structural advantages); K-Means + ExKMC offers **directly readable rules that are only a lossy post-hoc approximation** of a separate model (surface advantage). Evaluated jointly, the trade-off is "quality ↔ explanation usability."

**Framing rule (locked):** surface CLASSIX's *genuine* advantages honestly; do **NOT** over-claim overall quality superiority. Rationale: (a) data shows CLASSIX trails on real/high-d quality and internal metrics disagree; (b) the supervisor is CLASSIX's author — over-claiming is high-risk; (c) the M10 brief asks to "describe, analyse, **compare**", not prove superiority; (d) the submitted project plan framed the work as a fair empirical comparison. See memory `classix-advantage-framing`.

## 2. Overall 6-chapter narrative spine (locked)

Results merged 2026-06-25 (former Ch4 quality + Ch5 explanation → one Results chapter). ~8,300 words.

| Ch | ~Words | Role in the argument (how it hands off downstream) | RQ / evidence |
|----|--------|-----------------------------------------------------|---------------|
| 1 Introduction | 800 | Pain: operator has cluster + explanation, still can't act (decision paralysis) → thesis: explanation usability must be evaluated *jointly* with quality; that joint evaluation is the gap. | Locked |
| 2 Literature Review | 1,500 | RFM segmentation → XAI is classification-focused, clustering explainability neglected → three methods (CLASSIX/ExKMC/CREAM) → close on the gap. | 6 core refs + 3 surveys |
| 3 Methodology | 1,500 | The measuring stick: two-layer (benchmark + domain) design, data, preprocessing, method grids, metrics, RQ4 explanation-arena protocol, **§3.x mathematical analysis**. | code-defined; math analysis supports |
| 4 Results | 3,000 | Main arena. **4.1** quality+efficiency: no uniform winner, CLASSIX fast/stable → quality can't rank the methods. **4.2** explanation usability: fidelity reversal surfaces CLASSIX's structural advantage + k′ trade-off curve → answers the thesis. | RQ1–4, all data ready |
| 5 Discussion | 1,000 | Generalise: when quality ties, explanation usability decides; CLASSIX's structural vs ExKMC's surface advantage; consistent with Güttel's own results; limitations (no user study). | synthesis |
| 6 Conclusion | 500 | Close + future work (real user study, more e-commerce data). | — |

Argument chain: Intro creates tension → Lit shows it's an unstudied gap → Methodology supplies a fair ruler (with math backing for "fast/exact/deterministic" claims) → Results show quality can't decide (4.1) then explanation usability decides and favours CLASSIX's real strengths (4.2) → Discussion generalises → Conclusion closes.

## 3. Mathematical-analysis section (Ch3 §3.x) design

**Role (user-chosen):** *explain the experiments* — a supporting section, not a standalone contribution and not box-ticking. It proves *why* observed CLASSIX behaviours hold, by analysing the aggregation step in `official_classix/classix/aggregate_ed.py`. Placement: a section **inside Ch3** (keeps the 6-chapter structure).

**Logical chain (the three properties form a closed loop):** exact (①) → therefore the speed is real, not corner-cutting (③) → and it is identical every run (④).

| # | Property | Proof idea | Status / empirical anchor |
|---|----------|-----------|---------------------------|
| ① | Sorting-based pruning is **exact** (never drops a within-radius point) | First-PC axis `v` is unit-norm; projection `p=x·v`. Cauchy–Schwarz: `|p_j−p_i| ≤ ‖x_j−x_i‖`. Sorted ascending by `p`, so `p_j−p_i>tol ⇒ ‖x_j−x_i‖>tol` → safe to `break`. | **Theoretical guarantee, NOT a measured observation.** Defends ③ (speed costs no accuracy). Empirical cousin: fidelity check max\|ΔARI\|=0 vs official CLASSIX. |
| ③ | **Cost is near-linear in practice**: sort `O(n log n)` + aggregation scans only the width-`tol` projection band; worst case `O(n²)`. | Count `clx.nrDistComp_` vs brute force `n(n−1)/2` as n grows. | **VERIFIED (measured):** `src/analysis/distance_complexity.py` → exponent ≈ **1.09** (near-linear), fraction of brute force falls 0.0075→0.0003, dist/point ~flat. Explains the **36.4×** speed (classix 0.98ms vs kmeans++ 35.68ms). |
| ④ | **Deterministic**: PCA sign ambiguity fixed by `sort_vals *= sign(−sort_vals[0])` → output invariant to PC sign flip → seed-independent. | Algebraic + invariance argument. | **VERIFIED (measured):** classix ARI std across 5 seeds = 0.00000; kmeans++ = 0.00934. |
| ② | Membership test = exact radius test, reorganised: `‖x_i−x_j‖²≤tol² ⟺ ½‖x_i‖²+½‖x_j‖²−x_i·x_j ≤ tol²/2`; `½‖x‖²` precomputed once, `x_i·x_j` via one BLAS matmul. | Algebraic identity. | One-line **footnote** to ③ (implementation flops), not a headline result. |

**Honesty notes (must appear):** worst case is still `O(n²)` (e.g. all points in one tol-band); the nr_dist evidence uses well-separated synthetic blobs, a favourable case; ① is a correctness guarantee, not an observed measurement.

**What this section supports:** Ch4 §4.1.4 (efficiency) and the determinism/robustness claims (RQ2–3). It is NOT presented as a CLASSIX selling point on its own.

## 4. Literature-review decisions (Ch2)

- **Three M10 surveys are "starting points," not a mandatory deep-coverage checklist.** Decision: **cite all three** (low cost, signals engagement with the brief's pointers) but **deep-read only Hu et al. (2024)** "Interpretable clustering: A survey" as the anchor for the field taxonomy; Dewoprabowo et al. (2025) and Chen (2018, PhD) get one–two sentences each.
- **Organise Ch2 by taxonomy, not as a list:** intrinsic self-explaining clustering (CLASSIX) vs post-hoc rule extraction (ExKMC / CREAM). This dichotomy feeds Ch4's argument (intrinsic+faithful vs post-hoc+lossy) so the review does real work.
- **Keep CREAM in Ch2** as the rule-extraction exemplar; state explicitly why the implementation pivoted to **ExKMC** (clean install/run, directly comparable threshold-tree rules, quantifiable fidelity-to-K-Means).

## 5. Out of scope (YAGNI)

- No new clustering algorithm, no new interpretability metric (per submitted plan).
- No real user study (operationalised via objective proxies; written into Limitations).
- Math analysis stays supporting; no convergence proofs of the merging step (that would be the "independent contribution" tier the user declined).

## 6. Next step

After user review of this spec → invoke writing-plans to produce the implementation plan (draft §3.x prose + the formal ①④ proofs; fold Ch2/CREAM decisions into the Ch2 plan).
