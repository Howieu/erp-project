# ERP Dissertation — Chapter 3: Methodology (planning started 2026-06-25)

Status: **NOT fully locked.** This note currently captures only the newly-added **mathematical-analysis subsection** (M10 brief deliverable 2), which the user's submitted project plan had OMITTED (that plan scoped the project as purely empirical: RQ1–4, "不打算提出新算法，而是给出结构化的实证评价"). The rest of Ch3 (data, preprocessing, method grids, evaluation metrics, RQ4 pipeline) is derivable from existing code (`src/benchmark/`, `src/domain/`) and still needs a Socratic pass to lock. Placement decision (user, 2026-06-25): math analysis = a SECTION INSIDE Ch3, not a standalone chapter → keeps the 6-chapter structure.

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

## Open Ch3 items (still to plan/lock)
- 3.1 design (two-layer benchmark+domain + RQ4), 3.2 data (UCI Online Retail; benchmark sets), 3.3 preprocessing (log1p+StandardScaler), 3.4 methods + tuning grids (from `methods.py`), 3.5 evaluation metrics, 3.6 RQ4 explanation-arena protocol + objective proxies, 3.x (this) math analysis.
- Reconcile the CREAM→ExKMC pivot and RetailRocket→UCI pivot vs the submitted plan.

See [[erp-ch1-introduction]], [[erp-ch4-results-benchmark]], [[index]]; memory `classix-advantage-framing`.
