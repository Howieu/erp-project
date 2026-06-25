# ERP Dissertation — Chapter 3: Methodology (planning started 2026-06-25)

Status: **PLANNING COMPLETE (2026-06-25, ars-plan).** All sections locked: §3.x math analysis (drafted), §3.4–3.5 selection protocol, §3.1/3.2/3.3/3.6. The math-analysis section is the M10 deliverable-2 the submitted plan had OMITTED (that plan was purely empirical: "不打算提出新算法，而是给出结构化的实证评价"); added as a SECTION inside Ch3 (keeps the 6-chapter structure). One execution dependency remains: Ch4 §4.1 data refresh under the new selection protocol (tracked task).

## 3.x Algorithmic properties of CLASSIX (mathematical analysis)
**Drafted (zh, 2026-06-25):** `notes/dissertation/drafts/ch3-math-analysis.md` — fig3-1 + ①③④ + ② footnote. Plan: `docs/superpowers/plans/2026-06-25-ch3-math-analysis-section.md`.

Purpose: not new theorems — explain *why* the empirically observed CLASSIX behaviours hold, by proving properties of its aggregation step (`official_classix/classix/aggregate_ed.py`). Each result is tied to a measured result in Ch4, and each underpins a genuine CLASSIX advantage (see memory `classix-advantage-framing`). Scope (user-leaning, accessible): **focused speed/correctness trio ①③④, with ② stated briefly.**

| # | Property | Proof sketch | Explains (Ch4 observation) | Advantage surfaced |
|---|---|---|---|---|
| ① | Sorting-based pruning is **exact** (never skips a within-radius point) | First PC axis `v` is a unit vector; projection `p=x·v`. Cauchy–Schwarz: `|p_j−p_i| = |(x_j−x_i)·v| ≤ ‖x_j−x_i‖`. Data sorted ascending by `p`, so once `p_j−p_i > tol` (code: `sort_vals[j]-sort_vals[i] > tol → break`), every later point has `‖x_j−x_i‖ ≥ p_j−p_i > tol` → outside radius. Pruning loses nothing. | correctness of the fast path | exactness without brute force |
| ② | Membership test = exact radius test, reorganised | `‖x_i−x_j‖² ≤ tol² ⟺ ½‖x_i‖²+½‖x_j‖²−x_i·x_j ≤ tol²/2`. Code precomputes `half_nrm2=½‖x‖²` once and gets `x_i·x_j` from one BLAS matmul (`ips`), avoiding per-pair full distance recomputation. | the inner-product reformulation | fewer flops per comparison |
| ③ | Cost: sort `O(n log n)` + aggregation scanning only the projection band `[i+1, last_j)` of width `tol`; worst case `O(n²)`, typical near-linear. Code tracks `nr_dist` (number of distance evals) → **empirically measurable**. | aggregation complexity | **why CLASSIX is ~36× faster than KMeans** (Ch4 §4.1.4) |
| ④ | **Deterministic**: PCA sign ambiguity removed by `sort_vals *= sign(−sort_vals[0])`; output invariant to PC sign flip → same result every run, no seed dependence. | sign-flip normalisation | **why CLASSIX std=0 across seeds** (Ch4) whereas KMeans has init variance |

### Verified artifact for ③ (DONE 2026-06-25)
`src/analysis/distance_complexity.py` → `results/analysis/distance_complexity.csv`. 5-blob synthetic data, radius=0.5, n = 500…16000:
- Empirical scaling **log(nr_dist) ≈ 1.09·log(n)** → near-linear (brute force = 2.0, quadratic).
- nr_dist / brute-force n(n−1)/2 falls 0.0075 → **0.0003** as n grows (saves more at scale).
- dist-per-point ~flat (1.87 → 2.55) → pruned projection-band size roughly constant in n.
This is the mathematical evidence behind the ~36× speed advantage (Ch4 §4.1.4). Honesty: synthetic well-separated blobs are a favourable case; worst case remains O(n²).

### Stress test / honesty
- Worst case is still `O(n²)` (e.g. all points within one `tol`-band); state this, don't claim linear unconditionally.
- ② is algebraic bookkeeping, not deep math — frame ①③④ as the substantive trio; ② as a one-line remark on implementation.

## §3.4–3.5 Selection protocol & metrics (LOCKED 2026-06-25, ars-plan)
**Decision: dual-reporting, label-free primary selection.** No method uses ground-truth labels to tune. Hyperparameters (and k for KMeans/Ward) selected by an INTERNAL index (silhouette) — the realistic, deployment-faithful protocol; ARI/NMI reported as held-out OUTCOME metrics. Additionally report **best-over-grid ARI as an "oracle" upper bound** (the convention in Chen & Güttel and most clustering benchmarks → preserves direct comparability to the supervisor's own table). The gap between realistic and oracle is itself a finding ("best achievable vs realistically obtainable").

- §3.4 metrics-for-selection: silhouette (primary). §3.5 outcome metrics: ARI, NMI (labelled benchmark only); silhouette, Davies–Bouldin, Calinski–Harabasz (all, incl. unlabelled UCI domain); runtime.
- **Limitation to state explicitly:** internal-index selection is NOT neutral — silhouette favours compact/convex clusters, so it can UNDER-credit density methods (DBSCAN/CLASSIX) on shape sets (already seen in the UCI domain run where silhouette rewarded a 2-blob collapse). Acknowledge in Limitations.
- **Verified citations (web-checked 2026-06-25):** Rousseeuw (1987) *Silhouettes…* J. Comput. Appl. Math. 20:53–65, DOI 10.1016/0377-0427(87)90125-7 (avg silhouette to select clusters); von Luxburg, Williamson & Guyon (2012) *Clustering: Science or Art?* PMLR v27 (evaluation/parameter-selection problem); a clustering-validation-indices survey (arXiv 2407.20246) for internal-vs-external taxonomy; clustering-benchmark methodology (e.g. bioRxiv 2025.08.20.671270; arXiv 2108.11053) explicitly recommending comparison on BOTH optimally-tuned AND realistically-obtainable performance, and warning that tuning to the label's k undermines fairness + internal-index tuning is algorithm-biased. (Re-verify exact attributions during Ch2 citation work.)
- ⚠️ **CONSEQUENCE — Ch4 data refresh required:** the current §4.1.2 "best-ARI per dataset" numbers (Jain/Spiral=1.0, Aggregation 0.91, Wine 0.54…) must be re-derived. raw experiments need NOT be fully re-run — `results/benchmark_v3/metrics_raw.csv` already holds every config's ARI+silhouette, so re-select by silhouette and add the oracle column; ONLY KMeans/Ward need a cheap extra k-grid sweep (currently run at true_k only). Tracked as a task.

## §3.1 / 3.2 / 3.3 / 3.6 (LOCKED 2026-06-25, ars-plan)

**§3.1 Research design — two layers + RQ4.** Layer 1 = benchmark (labelled): controlled internal-validity comparison, 4 methods × 9 datasets, ARI/NMI computable. Layer 2 = UCI domain (unlabelled): external validity, internal metrics only. RQ4 explanation arena sits on top of both layers' outputs.

**§3.2 Data.** Benchmark = 9 datasets: 3 real (iris 150×4 k3, seeds 210×7 k3, wine 178×13 k3) + 6 shape (aggregation 788×2 k7, compound 399×2 k6, jain 373×2 k2, pathbased 300×2 k3, r15 600×2 k15, spiral 312×2 k3). Domain = UCI Online Retail cleaned → RFM, 4338 customers.
- **Deviations-from-proposal note (place at end of §3.2):** (1) RetailRocket→UCI Online Retail — UCI is transaction-level with genuine UnitPrice×Quantity so Monetary is real money; RetailRocket's event stream has no clean price. UCI was already the proposal's backup; here promoted to primary. (2) CREAM→ExKMC (justified in §3.6).

**§3.3 Preprocessing.** RFM via log1p (de-skew) + StandardScaler (common scale). Quality layer and explanation layer share one feature space so Ch4 numbers and explanations are consistent.

**§3.6 RQ4 protocol + objective proxies.** Pipeline-vs-pipeline: 甲 CLASSIX (self-explaining geometric) vs 乙 K-Means++ + ExKMC (threshold-tree rules). Why NOT "one clustering, two explainers": CLASSIX's geometric explanation is intrinsic to its own clusters, so "same clustering" is infeasible for it. Objective proxies (Approach A, reported separately, no composite): CLASSIX = #starting points / explanation dimensionality / explanation length; ExKMC = #rules / depth / tree size / fidelity-to-K-Means. Proxy legitimacy: Doshi-Velez & Kim (2017), Miller (2019), Lipton (2018), Lakkaraju (2016).
- **CREAM→ExKMC pivot:** ExKMC installs/runs cleanly on conda py3.10, yields directly comparable threshold-tree rules, and gives a quantifiable fidelity-to-K-Means; CREAM retained in Ch2 as the rule-extraction paradigm.

## Ch3 status
**PLANNING COMPLETE (2026-06-25).** §3.x math analysis drafted ([[ch3-math-analysis]]); §3.4–3.5 selection protocol locked; §3.1/3.2/3.3/3.6 locked. Outstanding execution dependency: Ch4 §4.1 data refresh under the new selection protocol (tracked task). Next: draft Ch3 prose, or refresh Ch4 then draft Ch4.

See [[erp-ch1-introduction]], [[erp-ch4-results-benchmark]], [[index]]; memory `classix-advantage-framing`.
