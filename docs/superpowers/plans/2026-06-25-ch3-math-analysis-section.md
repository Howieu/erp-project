# Ch3 §3.x Mathematical-Analysis Section — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft the supporting mathematical-analysis section of Chapter 3 that explains *why* the observed CLASSIX behaviours hold — exact (①) → fast (③) → deterministic (④) — backed by one figure and verified numbers.

**Architecture:** One figure script reads the existing `results/analysis/distance_complexity.csv` and renders `fig3-1`. The section prose is drafted in one focused markdown file with inline LaTeX math; every cited number is checked against the source CSVs before commit. No changes to CLASSIX or the experiment pipeline — this section only *analyses* artefacts already produced.

**Tech Stack:** Python 3.10 (conda env `exkmc`), matplotlib, pandas; Markdown + inline LaTeX for prose.

## Global Constraints

- Language of the drafted section: **English** (submission language per the project plan's English-facing sections). Math in inline LaTeX (`$...$`). If the user prefers Chinese, switch before executing.
- Run all Python via `conda run -n exkmc python ...` (CLASSIX/pandas live there; base env lacks pandas).
- Every numeric claim must match a source file verbatim: speed/determinism from `results/benchmark_v3/metrics_raw.csv`; complexity from `results/analysis/distance_complexity.csv`.
- Honesty clauses are mandatory, not optional: worst case is `O(n²)`; the nr_dist evidence uses well-separated synthetic blobs (favourable case); ① is a correctness guarantee, not a measured observation.
- Framing: supporting role only; do NOT present these as standalone CLASSIX selling points or over-claim quality superiority (see memory `classix-advantage-framing`).
- Figures output BOTH `.png` and `.pdf` (matches existing `fig5-1` convention).

---

### Task 1: Figure fig3-1 — distance computations vs n

**Files:**
- Create: `src/analysis/plot_distance_complexity.py`
- Test: `src/analysis/test_plot_distance_complexity.py`
- Reads: `results/analysis/distance_complexity.csv`
- Produces: `results/analysis/fig3-1_distance_complexity.png` and `.pdf`

**Interfaces:**
- Consumes: `distance_complexity.csv` columns `n, nr_dist, brute_force_n2, fraction_of_brute, dist_per_point` (already on disk).
- Produces: function `make_figure(csv_path: Path, out_stem: Path) -> float` returning the fitted log-log slope (float ≈ 1.09); writes `<out_stem>.png` and `<out_stem>.pdf`.

- [ ] **Step 1: Write the failing test**

```python
# src/analysis/test_plot_distance_complexity.py
from pathlib import Path
from src.analysis.plot_distance_complexity import make_figure

def test_make_figure_slope_and_files(tmp_path):
    out = tmp_path / "fig3-1_distance_complexity"
    slope = make_figure(Path("results/analysis/distance_complexity.csv"), out)
    assert 0.9 <= slope <= 1.3              # near-linear, not quadratic
    assert out.with_suffix(".png").exists()
    assert out.with_suffix(".pdf").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `conda run -n exkmc python -m pytest src/analysis/test_plot_distance_complexity.py -v`
Expected: FAIL with `ModuleNotFoundError` / `cannot import name 'make_figure'`.

- [ ] **Step 3: Write minimal implementation**

```python
# src/analysis/plot_distance_complexity.py
"""Render fig3-1: CLASSIX distance computations vs n (near-linear vs brute force).
Reads results/analysis/distance_complexity.csv (produced by distance_complexity.py).
Run: conda run -n exkmc python -m src.analysis.plot_distance_complexity
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = Path("results/analysis/distance_complexity.csv")
OUT = Path("results/analysis/fig3-1_distance_complexity")


def make_figure(csv_path: Path, out_stem: Path) -> float:
    df = pd.read_csv(csv_path)
    slope = float(np.polyfit(np.log(df["n"]), np.log(df["nr_dist"]), 1)[0])
    fig, ax = plt.subplots(figsize=(5.0, 3.6))
    ax.loglog(df["n"], df["nr_dist"], "o-", label=f"CLASSIX nr_dist (slope ≈ {slope:.2f})")
    ax.loglog(df["n"], df["brute_force_n2"], "s--", color="grey",
              label="brute force  n(n−1)/2  (slope = 2)")
    ax.set_xlabel("number of points  n")
    ax.set_ylabel("distance computations")
    ax.set_title("CLASSIX aggregation cost is near-linear")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_stem.with_suffix(".png"), dpi=200)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)
    return slope


def main() -> None:
    slope = make_figure(CSV, OUT)
    print(f"wrote {OUT}.png/.pdf  (fitted slope ≈ {slope:.2f})")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `conda run -n exkmc python -m pytest src/analysis/test_plot_distance_complexity.py -v`
Expected: PASS.

- [ ] **Step 5: Generate the figure and eyeball it**

Run: `conda run -n exkmc python -m src.analysis.plot_distance_complexity`
Expected: prints `wrote results/analysis/fig3-1_distance_complexity.png/.pdf  (fitted slope ≈ 1.09)`; the CLASSIX curve sits far below the brute-force line and the gap widens with n.

- [ ] **Step 6: Commit**

```bash
git add src/analysis/plot_distance_complexity.py src/analysis/test_plot_distance_complexity.py results/analysis/fig3-1_distance_complexity.png results/analysis/fig3-1_distance_complexity.pdf
git commit -m "feat(analysis): fig3-1 distance-complexity plot for Ch3 math analysis"
```

---

### Task 2: Draft §3.x scaffold + property ① (pruning exactness)

**Files:**
- Create: `notes/dissertation/drafts/ch3-math-analysis.md`

**Interfaces:**
- Produces: the section file with a stable heading structure later tasks append to: `## 3.x Algorithmic properties of CLASSIX`, then subsections `### 3.x.1 Exact pruning (①)`, to be followed by `3.x.2 Cost (③)`, `3.x.3 Determinism (④)`.

- [ ] **Step 1: Create the file with framing + property ①**

Write exactly this content:

````markdown
## 3.x Algorithmic properties of CLASSIX

This section does not propose new methods; it explains *why* three behaviours
observed in Chapter 4 hold, by analysing CLASSIX's aggregation step (the routine
in `aggregate_ed.py`). The three results form a chain: the sorted search is
**exact** (so the speed-up costs no accuracy), therefore the measured **near-linear
cost** is a genuine efficiency gain, and the procedure is **deterministic** (so the
zero seed-variance in Chapter 4 is expected, not luck). All notation follows the
data after standardisation; $\mathrm{tol}$ denotes the aggregation radius.

### 3.x.1 Exact pruning (①)

CLASSIX sorts the points by their projection onto the first principal axis
$v\in\mathbb{R}^d$, $\lVert v\rVert = 1$, writing $p_i=\langle x_i,v\rangle$ for the
sort value of point $x_i$. Points are scanned in nondecreasing order of $p$. When a
starting point $x_i$ is being grown into a group, the inner loop stops at the first
later point $x_j$ with $p_j-p_i>\mathrm{tol}$.

**Lemma (exactness).** If $p_j-p_i>\mathrm{tol}$ then $\lVert x_j-x_i\rVert>\mathrm{tol}$.

*Proof.* Since $\lVert v\rVert=1$, the Cauchy–Schwarz inequality gives
$p_j-p_i=\langle x_j-x_i,\,v\rangle \le |\langle x_j-x_i,\,v\rangle| \le
\lVert x_j-x_i\rVert\,\lVert v\rVert = \lVert x_j-x_i\rVert.$
Hence $p_j-p_i>\mathrm{tol}$ implies $\lVert x_j-x_i\rVert>\mathrm{tol}$. $\qquad\blacksquare$

Because $p$ is nondecreasing, every point after the first such $x_j$ also has
projection gap $>\mathrm{tol}$ and is therefore outside the radius. The early
termination discards only points *provably* beyond $\mathrm{tol}$, so the sorted
aggregation produces exactly the groups an exhaustive radius search would — the
speed-up of §3.x.2 is lossless. This is consistent with the fidelity check
(§3.x / Methods), where the implementation reproduced the official CLASSIX results
to $\max|\Delta\mathrm{ARI}|=0$.
````

- [ ] **Step 2: Verify the math and the cited number**

Re-read the proof: confirm `‖v‖=1` is used, the inequality direction is correct, and the fidelity number `max|ΔARI|=0` matches `src/benchmark/fidelity_check.py` output / the Ch4 note. Fix wording if any mismatch.

- [ ] **Step 3: Commit**

```bash
git add notes/dissertation/drafts/ch3-math-analysis.md
git commit -m "docs(ch3): math-analysis scaffold + property ① exact pruning proof"
```

---

### Task 3: Property ③ (near-linear cost) prose

**Files:**
- Modify: `notes/dissertation/drafts/ch3-math-analysis.md` (append `### 3.x.2`)

**Interfaces:**
- Consumes: `fig3-1` (Task 1); numbers from `results/analysis/distance_complexity.csv` and `results/benchmark_v3/metrics_raw.csv`.

- [ ] **Step 1: Append the §3.x.2 subsection**

Append exactly:

````markdown
### 3.x.2 Near-linear cost (③)

Sorting the $n$ points costs $O(n\log n)$. The aggregation then scans, for each
starting point $x_i$, only the points whose projection lies within the band
$(p_i,\,p_i+\mathrm{tol}]$; let $b_i$ be that band's size. The total number of
distance computations is $\mathrm{nr\_dist}=\sum_i b_i$. In the worst case every
point falls in one band (e.g. data collapsed onto a $\mathrm{tol}$-interval) and the
cost is $O(n^2)$; but when the projection spreads the data, the average band size is
roughly constant in $n$, giving near-linear cost.

Figure 3-1 confirms this empirically. On five-blob synthetic data
($\mathrm{tol}=0.5$, $n=500$–$16{,}000$) the measured $\mathrm{nr\_dist}$ scales as
$n^{1.09}$ (a log–log slope of $1.09$ versus $2$ for brute force); the fraction of
the $n(n-1)/2$ brute-force pairs actually evaluated falls from $0.0075$ to $0.0003$
as $n$ grows, and the distance computations per point stay essentially flat
($\approx 1.9$–$2.6$). This sub-quadratic cost is the mathematical reason behind the
runtime gap measured in §4.1.4: a median $0.98\,\mathrm{ms}$ for CLASSIX against
$35.68\,\mathrm{ms}$ for K-Means++ ($\approx 36\times$). The favourable case caveat
applies — well-separated blobs spread cleanly along the first axis; adversarial data
returns the procedure to its $O(n^2)$ bound.
````

- [ ] **Step 2: Verify every number against source**

Run: `conda run -n exkmc python -c "import pandas as pd; d=pd.read_csv('results/analysis/distance_complexity.csv'); print(d[['n','fraction_of_brute','dist_per_point']].to_string(index=False))"`
Expected: `fraction_of_brute` runs 0.00749→0.00032; `dist_per_point` 1.87→2.55. Confirm the prose's `0.0075→0.0003` and `≈1.9–2.6` are faithful.

Run: `conda run -n exkmc python -c "import pandas as pd; d=pd.read_csv('results/benchmark_v3/metrics_raw.csv'); print((d.groupby('method')['runtime_seconds'].median()*1000).round(2))"`
Expected: classix 0.98, kmeans++ 35.68. Confirm the `36×`.

- [ ] **Step 3: Commit**

```bash
git add notes/dissertation/drafts/ch3-math-analysis.md
git commit -m "docs(ch3): property ③ near-linear cost prose + verified numbers"
```

---

### Task 4: Property ④ (determinism) + ② footnote + bridge

**Files:**
- Modify: `notes/dissertation/drafts/ch3-math-analysis.md` (append `### 3.x.3` + footnote + closing bridge)

- [ ] **Step 1: Append the §3.x.3 subsection, footnote, and bridge**

Append exactly:

````markdown
### 3.x.3 Determinism (④)

**Proposition.** CLASSIX's partition is a deterministic function of the data: repeated
runs (any random seed) return identical labels.

*Argument.* The only direction-valued quantity is the first principal axis $v$, which an
eigen/SVD solver returns only up to sign ($v$ or $-v$). The implementation fixes this by
scaling the sort values with $s=\operatorname{sign}(-p_1)$ and sorting by $s\,p_i$. Under
$v\mapsto -v$ every $p_i\mapsto -p_i$, so $s\mapsto -s$ and the scaled values $s\,p_i$ are
unchanged; the sort order, the band searches, and the membership tests (which depend only
on inner products and norms, not on the orientation of $v$) are therefore identical. No
step draws randomness, so the labels depend on the data alone. $\qquad\blacksquare$

Chapter 4 confirms this: across five seeds the ARI standard deviation is $0$ for CLASSIX
(and the other deterministic methods), whereas K-Means++ shows $0.0093$ from its random
initialisation.

> **Footnote (②, implementation).** The membership test is the exact radius test
> reorganised: $\lVert x_i-x_j\rVert^2\le\mathrm{tol}^2 \iff
> \tfrac12\lVert x_i\rVert^2+\tfrac12\lVert x_j\rVert^2-\langle x_i,x_j\rangle\le
> \tfrac12\mathrm{tol}^2$. CLASSIX precomputes $\tfrac12\lVert x\rVert^2$ once and obtains
> the inner products for a whole band from a single matrix–vector product, so each
> comparison costs one dot product rather than a freshly recomputed Euclidean distance.

Together these properties justify treating CLASSIX's speed and stability (Chapter 4) as
structural guarantees rather than artefacts of a particular dataset or run.
````

- [ ] **Step 2: Verify the determinism numbers**

Run: `conda run -n exkmc python -c "import pandas as pd; d=pd.read_csv('results/benchmark_v3/metrics_raw.csv'); print(d.groupby(['dataset','method','params'])['ari'].std().groupby('method').max().round(4))"`
Expected: classix 0.0, kmeans++ 0.0093. Confirm the prose.

- [ ] **Step 3: Commit**

```bash
git add notes/dissertation/drafts/ch3-math-analysis.md
git commit -m "docs(ch3): property ④ determinism + ② footnote + closing bridge"
```

---

### Task 5: Section self-check + link into Ch3 note

**Files:**
- Modify: `notes/dissertation/erp-ch3-methodology.md` (point §3.x to the draft)

- [ ] **Step 1: Full-section read-through**

Read `notes/dissertation/drafts/ch3-math-analysis.md` top to bottom. Confirm: the exact→fast→deterministic chain reads in order; ① is labelled a guarantee (not a measurement); all three honesty caveats are present (O(n²) worst case, favourable-blob caveat, ① not measured); no `$...$` typos; figure referenced as "Figure 3-1".

- [ ] **Step 2: Link the draft from the Ch3 plan note**

In `notes/dissertation/erp-ch3-methodology.md`, under the `## 3.x Algorithmic properties` heading, add a line: `**Drafted:** notes/dissertation/drafts/ch3-math-analysis.md (fig3-1; ①③④ + ② footnote).`

- [ ] **Step 3: Commit**

```bash
git add notes/dissertation/erp-ch3-methodology.md
git commit -m "docs(ch3): link drafted math-analysis section into Ch3 plan note"
```

---

## Self-Review

**Spec coverage:** §3 of the spec (math-analysis: ①③④ + ② footnote, supporting role, honesty notes, ties to §4.1.4) → Tasks 2/3/4. The fig/table artefact → Task 1. Determinism/speed numbers verified → Tasks 3/4 verify steps. Overall structure (§2) and lit-review decisions (§4) are intentionally NOT in this plan — they are recorded in the notes and Ch2 needs its own search+plan cycle; flagged to user below.

**Placeholder scan:** No TBD/TODO; all prose and proofs are written out in full; figure code is complete.

**Type consistency:** `make_figure(csv_path, out_stem) -> float` defined in Task 1 and consumed identically in Task 1's test; CSV column names match the on-disk file (`n, nr_dist, brute_force_n2, fraction_of_brute, dist_per_point`).

**Note on scope:** This plan delivers only the §3.x section. Ch2 (3-survey review, taxonomy organisation, CREAM-pivot justification) and the full Ch3 lock are separate future cycles per the spec's §6.
