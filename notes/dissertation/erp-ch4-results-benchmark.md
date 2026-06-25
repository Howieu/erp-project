# ERP Dissertation — Chapter 4: Clustering Quality & Efficiency (LOCKED 2026-06-18, axis-reorg)

Confirmed via ARS plan-mode Socratic dialogue. **Results reorganised by ARGUMENT AXIS, not by dataset** (user choice 2026-06-18): Ch4 = the quality+efficiency axis (RQ1–3, benchmark AND RetailRocket quality together); Ch5 = the explanation-usability axis (RQ4, standalone — the novel contribution). RetailRocket spans both chapters, contributing quality data here and explanation data in Ch5. Ch3 methodology (two-layer benchmark+domain + RQ4 pipeline comparison) is unchanged at the MEASUREMENT level; only the Results write-up reorganises. Target ~1,500 words, data source results/benchmark_v3/ (+ pending RetailRocket domain run).

## Landing point (revised 2026-06-25, dual-lens)
Clustering quality has NO uniform winner under EITHER selection lens. Under optimal tuning (Güttel convention) CLASSIX is competitive — top overall, shape-strong, trails real/high-d. Under realistic label-free selection no method dominates and CLASSIX is the hardest to tune (largest oracle gap). CLASSIX's robust wins are speed (~36×) and determinism. Quality alone cannot rank the methods → deciding axis = explanation usability (→ §4.2).

## NOTE: this is now §4.1 of the merged Results chapter (Ch4); §4.2 = explanation usability ([[erp-ch5-explanation-usability]]). Dual-reporting locked 2026-06-25.

## §4.1 skeleton (~1,500w) — Güttel-convention primary + realistic-selection secondary
| § | Words | Task | Ammunition |
|---|---|---|---|
| 4.1.1 Setup + fidelity anchor | ~150 | 9 datasets, 4 methods (+CLASSIX 2 variants), fair grid; lead with fidelity max\|ΔARI\|=0 (later gaps = tuning not bug). **State the dual selection protocol** (§3.4): PRIMARY = best-over-grid (optimal tuning, Chen & Güttel convention); SECONDARY = label-free silhouette selection. | fidelity Δ=0 |
| 4.1.2 Quality under OPTIMAL tuning (primary, Güttel) ⭐ | ~400 | **Frame = "best achievable quality (capability)."** best-over-grid ARI: CLASSIX top overall mean 0.801; shape strong (Jain/Spiral=1.0, Aggregation 0.91 top), trails real/high-d (Wine 0.54, Seeds 0.71). NUANCE: real ARI 0.54 but NMI 0.686 (near top). Explicitly comparable to Chen & Güttel's table. | fig4-1; win table; ARI-vs-NMI |
| 4.1.3 Deployment realism: LABEL-FREE selection (secondary) ⭐NEW | ~350 | **Frame = "realistically obtainable without labels (deployability)" — a DIFFERENT question, not a re-ranking.** silhouette-selected ARI: CLASSIX drops to 0.541 (Spiral −0.00, Jain 0.40); DBSCAN robust on shape 0.872; KMeans best on real 0.649. FINDING: oracle−realistic gap largest for CLASSIX (0.26) → highest potential, hardest to tune label-free. State silhouette's compact-cluster bias. **Reconcile with 4.1.5:** radius→partition is smooth, but silhouette→ARI-optimal radius is misaligned (different things). | realistic-vs-oracle table; gap finding |
| 4.1.4 Quality WITHOUT ground truth — UCI domain | ~250 | Internal metrics only (silhouette/DB/CH) on RFM; metrics DISAGREE — silhouette/DB reward 2 mega-clusters, CH rewards KMeans k=4 (3328 vs 8–11). No uniform winner in domain either; motivates why §4.2 explains the k=4 KMeans clusters. | domain_quality.csv |
| 4.1.5 Efficiency + robustness (RQ2–3) | ~250 | CLASSIX fastest 0.98ms vs KMeans 35.7ms (~36×); determinism std=0 vs KMeans 0.0093; param sensitivity fig4-2/4-3 (radius→partition smoothness, NOT a quality-tuning claim — see 4.1.3). | fig4-2/3/4; 36×; std=0 |
| 4.1.6 Synthesis + bridge | ~100 | No uniform quality winner under EITHER lens; CLASSIX competitive-under-optimal-tuning but hardest to tune label-free, yet fastest + deterministic; quality cannot rank → deciding axis = explanation usability (→ §4.2). | bridge to RQ4 |

## Argument stress test
- Weakest point: "competitive" = spinning a loss? DEFENCE: anchor to CLASSIX paper's own positioning (fast+explainable+competitive) + official exp5 real-data table (CLASSIX wins ~5/8, not dominant) → matches original authors.
- Reverse test: CLASSIX dominating quality would WEAKEN the trade-off thesis; competitive-not-dominant strengthens "explanation is the deciding axis". Self-consistent.
- Residual risk: only 3 benchmark real datasets, none e-commerce → benchmark = controlled internal-validity comparison; RetailRocket (4.3 + Ch5) supplies external validity.

## Verified data points (v3, 2026-06-18)
Runtime median ms: classix 0.98 / dbscan 1.33 / ward 2.19 / kmeans++ 35.68. Real-data mean NMI(best): kmeans 0.754 / ward 0.737 / classix 0.686 / dbscan 0.415. Real-data mean Silhouette(best-ARI cfg): kmeans 0.382 / ward 0.372 / dbscan 0.339 / classix 0.299.

## Verified dual-lens benchmark data (selection_refresh, 2026-06-25)
Source: `src/benchmark/selection_refresh.py` → `results/benchmark_v3/selection_refresh.csv`. Mean ARI per method:
- **OPTIMAL (best-over-grid, primary):** classix 0.801 / dbscan 0.733 / ward 0.662 / kmeans++ 0.661. Shape: dbscan 0.936, classix 0.894, ward 0.626, kmeans 0.610. Real: kmeans 0.764, ward 0.734, classix 0.615, dbscan 0.325.
- **REALISTIC (label-free silhouette, secondary):** classix 0.541 / dbscan 0.687 / ward 0.606 / kmeans++ 0.619. Shape: dbscan 0.872, kmeans 0.604, classix 0.561, ward 0.608. Real: kmeans 0.649, ward 0.603, classix 0.501, dbscan 0.317.
- **Oracle−realistic gap (tunability):** classix 0.26 (largest), ward 0.06, dbscan 0.05, kmeans 0.04. CLASSIX shape collapse under silhouette: spiral 1.00→−0.00, jain 1.00→0.40.
- The OPTIMAL numbers equal the original v3 best-ARI figures (so 4.1.2 reuses them); KMeans/Ward k selected over k=2..20 by silhouette for the realistic lens.

## Verified domain data points (UCI Online Retail, §4.3, 2026-06-25)
4338 customers, RFM (log1p + StandardScaler — same space as Ch5 Explanation Arena). Internal metrics (silhouette / Davies-Bouldin↓ / Calinski-Harabasz↑):
- kmeans++ (k=4): 0.338 / 1.009 / **3328.5** — moderate silhouette, dominant CH
- ward (k=4): 0.242 / 1.120 / 2615.1
- dbscan (eps=0.6, best-silhouette): 2 clusters + 33 noise · 0.534 / 1.820 / 111.3
- classix (radius=0.8, best-silhouette): 2 clusters · **0.563** / **0.311** / 8.1
- classix (radius=0.9, Ch5 operating point): 3 clusters · 0.396 / 0.480 / 11.6
Selection rule: k=4 fixed for KMeans/Ward (RFM convention, = Ch5 base); DBSCAN/CLASSIX knobs chosen by best silhouette (guarded 2–12 clusters, noise<50%). Story: silhouette/DB favour coarse 2-cluster splits (not actionable for segmentation), CH favours KMeans k=4 → no uniform winner; the quality axis can't rank → Ch5. Source: src/domain/domain_quality.py.

## Figures (results/benchmark_v3/figures/)
fig4-1 best_ari_per_dataset · fig4-2 dbscan_eps_sweep · fig4-3 classix_radius_sweep · fig4-4 runtime_per_dataset.

## Status
Ch4 PLANNED & user-confirmed (axis-reorg). Data ready for ALL sections: 4.2/4.4 (benchmark v3), 4.3 (UCI domain, results/domain_uci/domain_quality.csv, 2026-06-25). Next: draft Ch4 prose. See [[erp-ch5-explanation-usability]].
