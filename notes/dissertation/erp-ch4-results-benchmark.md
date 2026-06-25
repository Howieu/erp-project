# ERP Dissertation — Chapter 4: Clustering Quality & Efficiency (LOCKED 2026-06-18, axis-reorg)

Confirmed via ARS plan-mode Socratic dialogue. **Results reorganised by ARGUMENT AXIS, not by dataset** (user choice 2026-06-18): Ch4 = the quality+efficiency axis (RQ1–3, benchmark AND RetailRocket quality together); Ch5 = the explanation-usability axis (RQ4, standalone — the novel contribution). RetailRocket spans both chapters, contributing quality data here and explanation data in Ch5. Ch3 methodology (two-layer benchmark+domain + RQ4 pipeline comparison) is unchanged at the MEASUREMENT level; only the Results write-up reorganises. Target ~1,500 words, data source results/benchmark_v3/ (+ pending RetailRocket domain run).

## Landing point
Clustering quality has NO uniform winner; CLASSIX is competitive, shape-robust, and the fastest method, but trails K-Means on real/high-d. Quality alone cannot rank the methods → the deciding axis is explanation usability (→ Ch5).

## 5-section skeleton (~1,500w)
| § | Words | Task | Ammunition |
|---|---|---|---|
| 4.1 Setup + fidelity anchor | ~150 | Recap Quality Arena (9 datasets, 4 methods + CLASSIX 2 variants, fair grid); lead with fidelity check (max\|ΔARI\|=0.0000) so later gaps = tuning not bug. Signpost: RetailRocket's quality is reported here, its explanation in Ch5. | fidelity Δ=0 |
| 4.2 Quality WITH ground truth — benchmark ⭐ | ~450 | fig4-1 + per-dataset winner table. CLASSIX competitive on shape (Jain/Spiral=1.0, Aggregation 0.91 top), trails real/high-d (Wine 0.54, Seeds 0.71). Honest weak spot Pathbased 0.58. KEY NUANCE: CLASSIX real ARI 0.54 but NMI 0.686 (near top) → recovers structure, differs on cluster count/boundaries. | fig4-1; win table; ARI-vs-NMI |
| 4.3 Quality WITHOUT ground truth — UCI Online Retail | ~350 | Internal metrics only (silhouette/DB/CH) on RFM features; cannot use ARI/NMI (no labels). KEY: metrics DISAGREE — silhouette/DB reward CLASSIX/DBSCAN collapsing to 2 mega-clusters (well-separated but useless for segmentation); CH strongly rewards KMeans k=4 (3328 vs 8–11). No uniform winner in the domain either → reinforces the "quality can't rank" landing point, and motivates why Ch5 explains the k=4 KMeans clusters. **[DATA READY: results/domain_uci/domain_quality.csv]** | internal metrics; metric disagreement |
| 4.4 Efficiency + robustness (RQ2–3) | ~400 | CLASSIX FASTEST median 0.98ms vs KMeans 35.7ms (~36×); fig4-4. Parameter sensitivity: fig4-2 (DBSCAN eps cliff) vs fig4-3 (CLASSIX radius smoother); seed determinism (det methods std=0; KMeans init-variance only Compound/Aggregation/Spiral). | fig4-2/3/4; 36×; std=0 |
| 4.5 Synthesis + bridge | ~150 | Quality a wash, CLASSIX wins efficiency, but quality can't rank → deciding axis = explanation usability (→ Ch5). | bridge to RQ4 |

## Argument stress test
- Weakest point: "competitive" = spinning a loss? DEFENCE: anchor to CLASSIX paper's own positioning (fast+explainable+competitive) + official exp5 real-data table (CLASSIX wins ~5/8, not dominant) → matches original authors.
- Reverse test: CLASSIX dominating quality would WEAKEN the trade-off thesis; competitive-not-dominant strengthens "explanation is the deciding axis". Self-consistent.
- Residual risk: only 3 benchmark real datasets, none e-commerce → benchmark = controlled internal-validity comparison; RetailRocket (4.3 + Ch5) supplies external validity.

## Verified data points (v3, 2026-06-18)
Runtime median ms: classix 0.98 / dbscan 1.33 / ward 2.19 / kmeans++ 35.68. Real-data mean NMI(best): kmeans 0.754 / ward 0.737 / classix 0.686 / dbscan 0.415. Real-data mean Silhouette(best-ARI cfg): kmeans 0.382 / ward 0.372 / dbscan 0.339 / classix 0.299.

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
