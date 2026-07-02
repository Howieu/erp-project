# ERP Dissertation — Handoff Document

> **Purpose.** Paste this file into a fresh conversation to continue the project with full context. It consolidates all project memory as of **Session 13 (2026-07-02)** and reflects the *current true state* (older planning notes are superseded where they conflict — this file wins).
>
> **One-line resume:** "Continue my ERP dissertation — see handoff.md." The canonical artifact is `notes/dissertation/FULL_DRAFT_zh.md`.

---

## 1. Project overview

- **What:** MSc Data Science dissertation, **University of Manchester**. Topic = **explainable clustering for e-commerce customer segmentation**.
- **Deadline:** September 2026 (lots of runway).
- **Repo:** https://github.com/Howieu/erp-project · **Local:** `~/erp-project` · **Branch:** `main`.
- **Supervisor:** Stefan Güttel (the CLASSIX author) — project brief `docs/ERP_M10.pdf`.
- **Language:** dissertation is written in **Chinese** (`FULL_DRAFT_zh.md`); references in **Harvard (UoM style)**. Title page may need an English version if UoM requires.
- **Length:** ~8,300 word-equivalent, **6 chapters**.

## 2. Core thesis (current, defensible version)

CLASSIX achieves clustering quality **competitive** with RFM+K-Means and is **shape-robust** — but is **NOT a uniform winner** (wins/ties on shape datasets, trails K-Means on real/high-dimensional data, mirroring Chen & Güttel's own real-data table). Its **geometric explanation has higher explanation complexity and cannot be directly turned into operational actions**, whereas the **threshold-tree rules of explainable K-Means (ExKMC, Moshkovitz et al. 2020 / Frost et al. 2020) are more parsimonious and directly actionable** — but are a *lossy approximation* of an independently trained K-Means (quantified by fidelity). The contribution is a **joint "clustering quality ↔ explanation complexity" evaluation**, not a verdict that either method is globally better.

**Two pipelines compared (RQ4):**
- **甲 (Pipeline A) = CLASSIX** — self-explaining geometric clustering.
- **乙 (Pipeline B) = K-Means++ → ExKMC** — threshold-tree rules over the K-Means partition.

**Four RQs:** RQ1 quality · RQ2 efficiency · RQ3 robustness · RQ4 explanation complexity (the novel contribution).

## 3. ⚠️ CRITICAL CONSTRAINT — no human user study

The user **cannot run a user study or interview operations staff.** So "explanation usability" is operationalized as **objective complexity proxies**, NOT human evaluation:
- **Rule side (ExKMC):** rule count (leaves), conditions/rule (tree depth), total rule size, coverage, **fidelity to K-Means**.
- **Geometric side (CLASSIX):** number of starting points, explanation dimensionality.
- **Justification ("proxy shield"):** functionally-grounded evaluation tier (Doshi-Velez & Kim 2017), size/length interpretability metrics (Lakkaraju 2016), simpler = lower cognitive load (Miller 2019, Lipton 2018). Counter-example owned: Poursabzi-Sangdeh et al. 2021 (simpler ≠ always more usable) → proxies are a **directional assumption**, not proven equivalence.
- The proxies measure **compactness/complexity**, NOT usability per se — this is stated up front (abstract, §1.4, §2.2) and the absence of a user study is the **principal acknowledged limitation**.

**Do not** reintroduce any claim about what business users "find intuitive" — that is untestable here.

## 4. Environments & footguns (macOS, Apple M4 Pro, conda)

| Env | Python | Use for | Key packages |
|---|---|---|---|
| `ds` | 3.11 | **benchmark** (RQ1–3) | ClassixClustering 1.5.1, sklearn 1.6.1, numpy 1.26.4 |
| `exkmc` | 3.10 | **domain / RQ4 / ExKMC** | numpy **1.26.4** (pinned), ExKMC 0.0.3, ClassixClustering 1.5.1, sklearn 1.4.2 |

Activate with: `source /opt/homebrew/anaconda3/etc/profile.d/conda.sh && conda activate exkmc`.

**Footguns (permanent):**
- The CLASSIX PyPI package is **`ClassixClustering`**, NOT `classix` (`pip install classix` pulls an unrelated lxml helper). Import: `from classix import CLASSIX`.
- CLASSIX API: `clx = CLASSIX(radius=r); clx.fit(X); clx.labels_; clx.splist_.shape[0]` (starting points). There is **no `fit_predict`**. Explanation: `clx.explain(X, index)`.
- ExKMC needs **numpy < 2.0** (numpy-2.x ABI breaks its C extension). Install recipe: py3.10 env, `pip install numpy==1.26.4`, then `pip install --no-build-isolation --no-cache-dir ExKMC`.
- ExKMC gotchas: `Node.is_leaf()` is a **method**; `Tree._size()`/`_max_depth()` are methods; fidelity = `(tree.predict(X)==km.labels_).mean()` (NOT `surrogate_score`, which returns raw cost).
- `uv` is **not installed** → the `paper-search` skill is unavailable; use WebFetch/WebSearch for citation grounding.

## 5. Repo layout

```
~/erp-project/
  notes/dissertation/FULL_DRAFT_zh.md   ← THE canonical dissertation (hand-maintained)
  notes/dissertation/drafts/            ← per-chapter drafts, SUPERSEDED (may hold stale numbers)
  docs/ERP_M10.pdf                      ← supervisor brief (canonical bibliography, pp.14-15)
  src/benchmark/                        ← RQ1-3: datasets.py, methods.py, metrics.py,
                                          run_benchmark.py, fidelity_check.py, plots.py
  src/domain/                           ← RQ4/domain: rfm.py (UCI), rfm_retailrocket.py,
                                          explanation_arena.py, domain_quality.py, review_analyses.py
  data/raw/                             ← gitignored (Online Retail.xlsx 23MB; retailrocket/ 304MB)
  data/processed/rfm.csv                ← UCI, 4,338 customers
  data/processed/rfm_retailrocket.csv   ← RetailRocket, 11,719 buyers
  results/benchmark_v3/                 ← current benchmark (metrics_agg.csv, selection_refresh.csv, figures/)
  results/domain_uci/                   ← domain_quality.csv, exkmc_kprime_curve.csv,
                                          cognitive_walkthrough.md, review_analyses.txt, fig4-7
  results/domain_retailrocket/          ← domain_quality.csv, exkmc_kprime_curve.csv
  results/analysis/                     ← fig3-1 distance_complexity (§3.7.2 scaling experiment)
```

**⚠️ Canonical-draft maintenance rule:** `FULL_DRAFT_zh.md` is **hand-maintained** and contains the abstract + reference list that live *nowhere else*. There is **no build script** — do NOT rebuild it by concatenating `drafts/ch1..ch6` (that would wipe the abstract + refs). Edit `FULL_DRAFT_zh.md` directly.

## 6. Chapter structure (final, in FULL_DRAFT_zh.md)

1. **Introduction** (~800w) — hook (operations decision paralysis), gap (only quality is compared, never explanation usability), 3-layer timeliness, purpose + 4 RQs + defensible thesis.
2. **Literature Review** (~1,500w) — funnel: 2.1 e-commerce segmentation (plant "quality=all" bias) → 2.2 XAI proxy shield (load-bearing) → 2.3 CLASSIX → 2.4 ExKMC threshold tree (CREAM demoted to citation-only) → 2.5 gap.
3. **Methodology** (~1,500w) — §3.1 design, §3.2 data + **interpretable-features-as-precondition**, §3.3 methods, §3.4 metrics (Approach A: separate profiles, no composite score), §3.5 k′ trade-off, §3.6 limitations, **§3.7 CLASSIX math analysis** (3 proofs: exact pruning ①, near-linear cost ②, determinism ③).
4. **Results** (~1,500w) — §4.1 quality + efficiency (RQ1–3, benchmark + both domain datasets' quality), §4.2 explanation complexity (RQ4, the novel chapter: complexity profiles, fair-comparison probe, k′ curve, proxy validity, cognitive walkthrough).
5. **Discussion** (~1,000w) — significance, scenario-dependent guidance, relation to prior work, 5 limitations, future work.
6. **Conclusion** (~500w).

## 7. Datasets & where models have run

- **Benchmark (9 datasets, `results/benchmark_v3/`):** shape = aggregation, compound, jain, pathbased, r15, spiral; real = iris, seeds, wine. 4 methods (CLASSIX [distance+density variants], K-Means++, DBSCAN, Ward) × full fair parameter grid × 5 seeds. **Fidelity anchor:** CLASSIX wrapper reproduces official CLASSIX bit-for-bit (max|ΔARI| = 0) on the sklearn toy subset.
- **Domain PRIMARY = UCI Online Retail** (`rfm.py`, 4,338 customers, real Monetary = Σ price×qty).
- **Domain ROBUSTNESS = RetailRocket** (`rfm_retailrocket.py`, 11,719 buyers, Monetary = item-count proxy, no price). Thesis **replicates**.

## 8. Canonical bibliography (supervisor's M10 brief — source of truth)

[1] Hu et al. (2024) *Interpretable clustering: a survey* · [2] Dewoprabowo et al. (2025) · [3] Chen, **J.** (2018) DReaM PhD · [4] **Chen, X.** & Güttel (2024) CLASSIX, *Pattern Recognition* 150:110298 · [5] Sabbatini & Calegari (2023) CREAM (cited only, not in experiments) · [6] Moshkovitz et al. (2020) explainable k-means, ICML → implementation **ExKMC** (Frost et al. 2020).
**Note:** three different Chens — **X.** (CLASSIX), **J.** (DReaM), **D.** (UCI dataset). Keep initials distinct.

## 9. Current state (as of Session 13, HEAD `8f8d015`, pushed)

The draft is **submission-quality**: complete, figure-consistent, whole-draft peer-reviewed **twice** (Round-1 + Round-2 all findings applied), and **fully data-verified against `results/`**.

- **Round-1** (Session 11): all 21 Tier A+B revisions applied (`07ba0c7`).
- **Round-2** (Session 12 review → Session 13 fixes): all 24 findings (3 high + 10 medium + 11 low) applied (`1b858b8`).
- **Data verification** (Session 13): every quantitative claim cross-checked against benchmark_v3 / domain CSVs; RetailRocket starting-point count re-run live. **Only one error found and fixed** (`8f8d015`): §4.1.4 Monetary–Frequency correlation was "0.80/0.81" → corrected to **0.55/0.56** (real data 0.554/0.558; strengthens the proxy argument).

### 9a. ⚠️ Most important recent change — the timing/efficiency narrative

The old "CLASSIX is fastest, ~36× over K-Means++" headline was **doubly wrong** and has been **reframed** everywhere (abstract EN+ZH, §3.7.2, §4.1.5, §4.1.6, §5.2, §6):
- The "35.68 ms" K-Means++ figure was stale (actual median **47.84 ms**).
- "0.98 ms" was CLASSIX's median over **1,620 configs** (many degenerate ultra-fast runs) vs K-Means++'s **9** — not comparable.
- **At matched best-ARI operating points: DBSCAN 1.20 ms < Ward 2.19 < CLASSIX 5.70 < K-Means++ 47.84.** So **CLASSIX is NOT the fastest — DBSCAN is.**
- CLASSIX's efficiency claim is now anchored on its **defensible** evidence: **near-linear asymptotic scaling** (§3.7.2, nr_dist ∝ n^1.09, measured n=500–16,000) + **full determinism** (std=0, proven §3.7.3). The thesis narrative shifted from "wins on speed + determinism" → "wins on **scalability + determinism**". Determinism remains rock-solid.

## 10. Verified key numbers (current true values)

- **Benchmark best-ARI (oracle) mean:** CLASSIX 0.801 · DBSCAN 0.733 · Ward ≈0.66 · K-Means++ ≈0.66. Weakest CLASSIX = **wine 0.54** (not pathbased). Shape not all-CLASSIX: compound DBSCAN 0.936 > CLASSIX 0.897.
- **Real-data best NMI:** CLASSIX 0.686 (recovers structure but misaligns boundaries/count — ARI–NMI divergence), K-Means++ 0.754, Ward 0.737, DBSCAN 0.415.
- **Silhouette-selected (deployable) ARI:** CLASSIX 0.541 (worst — hard to tune without labels), DBSCAN 0.687, K-Means++ 0.619, Ward 0.606. All methods collapse to **k=2** under free silhouette selection → justifies the **k=4 operating point** for the domain study.
- **UCI domain @ k=4:** CLASSIX sil 0.396 / DB 0.480; K-Means++ 0.338 / 1.009 (but CH 3328.5 ≫ CLASSIX 11.6). CLASSIX radius=0.9 → degenerate {4334, 3, 1}.
- **Explanation profiles:** CLASSIX = **42 starting points** (UCI) / **72** (RetailRocket @ radius=1.45), dim 3. ExKMC = **4 rules, depth 3, 7 nodes**.
- **ExKMC rules (UCI, original RFM units):** F≤6 ∧ R≤26; F≤6 ∧ R>26 ∧ M≤642; F≤6 ∧ R>26 ∧ M>642; F>6.
- **k′ curve fidelity-to-K-Means:** UCI 0.799 (k′=4) → 0.908 (k′=16), depth 3→6. RetailRocket base 4 rules = 0.945 (plateaus at k′ 9–10, 14–16).
- **Monetary proxy validity (UCI):** corr(real£, qty) = 0.923; each vs Frequency = 0.55/0.56; ARI(real£ vs qty segmentation) = 0.78.

## 11. What's done / what remains

**Done:** all experiments, all 6 chapters, abstract (bilingual), Harvard references (citation audit clean — 27 cites, 0 orphans), two peer-review rounds, full data verification. Draft pushed to `origin/main`.

**Remaining options (none blocking):**
1. **`ars-format-convert`** → export DOCX/PDF for submission (needs pandoc; embed figures from `results/*/figures/`).
2. **`ars-reviewer`** → optional Round-3 multi-agent review (~$5, ask user first).
3. English title page if UoM requires.
4. Sync the superseded `drafts/ch4-results-zh.md` if desired (it still has the old 0.80/0.81 and old timing framing; `FULL_DRAFT_zh.md` is canonical, so this is cosmetic only).
5. Optional extra experiments flagged as future work (not required): k∈{4,6,8} sensitivity; ExKMC-segment vs human-RFM-segment cross-tab.

## 12. ARS toolkit (Academic Research Skills, installed in repo)

`ars-reviewer` (peer review) · `ars-revision` (revision coaching) · `ars-format-convert` (Markdown→DOCX/PDF) · `ars-citation-check` · `ars-full` (review→revise→convert) · `ars-abstract` · `ars-lit-review` · `ars-outline` · `ars-plan`. **Remind the user of these when they resume.**

## 13. Working-style preferences

- **Be autonomous:** proceed on reasonable assumptions; avoid AskUserQuestion clarifications. Exception: surface (don't silently rewrite) any change that alters a flagship thesis claim — e.g. the timing reframe was flagged before/while applying.
- Verify numbers against `results/` before asserting them; the older planning memories contain stale figures.
- Commit style: end messages with `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`. This repo commits directly to `main`.

---
*Generated Session 13, 2026-07-02. HEAD `8f8d015`. If any claim here conflicts with an older `.claude` memory note, this handoff is newer and wins.*
