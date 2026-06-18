# ERP Dissertation — Chapter 5: Explanation Usability (RQ4) (LOCKED 2026-06-18)

Confirmed via ARS plan-mode Socratic dialogue. **Results reorganised by argument axis** (user choice 2026-06-18): Ch5 = the explanation-usability axis, the dissertation's NOVEL CONTRIBUTION, given its own chapter. Implements RQ4 from the locked Ch3 methodology (pipeline-vs-pipeline, Approach A separate complexity profiles, ExKMC k' trade-off curve). Target ~1,500 words.

## Landing point
Quality is competitive across methods (Ch4), but explanation usability is where the two pipelines diverge sharply: CLASSIX's geometric explanation has higher complexity and is not directly actionable, whereas ExKMC's threshold-tree rules are parsimonious, countable, and directly actionable — and the ExKMC k' knob makes the quality↔explanation trade-off a drawable curve. This answers the thesis.

## 5-section skeleton (~1,500w)
| § | Words | Task | Ammunition |
|---|---|---|---|
| 5.1 Explanation arena setup | ~200 | Pipeline 甲 = CLASSIX (self-explaining geometric) vs 乙 = K-Means++ + ExKMC (threshold-tree rules over k-means clusters). Why pipeline-vs-pipeline not explainers-of-same-clustering (Ch3 path-2: CLASSIX geometric explanation is intrinsic to its own clusters → "same clustering" infeasible). | Ch3 lock |
| 5.2 Complexity profiles (Approach A, separate) ⭐ | ~450 | Each method reports its OWN profile, no composite score. CLASSIX geometric: #starting points, explanation dimensionality, explanation length. ExKMC rules: #rules (leaves), conditions-per-rule (depth), total rule size, fidelity-to-k-means. Per-metric + qualitative comparison. | CLASSIX.explain(); ExKMC tree |
| 5.3 k' trade-off curve ⭐⭐ | ~400 | Sweep ExKMC max_leaves (k' from k upward) → record (explanation complexity vs fidelity-to-k-means) per k'; plot the curve; place CLASSIX on the same quality-vs-complexity plane. THE differentiator — turns the trade-off claim into a drawable curve nobody else has. | k' sweep |
| 5.4 Proxy validity (functionally-grounded shield) | ~250 | Why these proxies are legitimate without a user study: Doshi-Velez & Kim (2017) functionally-grounded tier; Lakkaraju (2016) size/length metrics; Miller (2019) / Lipton (2018) simpler = lower cognitive load. Closes the Ch1-flagged "no user study" attack. | Doshi-Velez & Kim; Lakkaraju; Miller; Lipton |
| 5.5 Synthesis | ~200 | Answer the thesis: quality competitive (Ch4), but explanation usability is the dividing axis → the trade-off, evaluated jointly. Hand off to Discussion. | closes RQ4 |

## Data / build dependencies
- **ExKMC install BLOCKED** on Python 3.11 (`longintrepr.h` removed) — needs a Python 3.9/3.10 env or a header patch before 5.2/5.3 data exists.
- CLASSIX `.explain()` complexity capture: implement an extractor (starting points / dimensionality / length).
- Apply on benchmark clusters and/or RetailRocket RFM clusters (RetailRocket also pending domain run).

## Success points
- 5.2 carries the functionally-grounded proxy shield (operationalises usability without humans).
- 5.3 is the standout: the ExKMC k' knob → an actual drawable trade-off curve.

## Status
Ch5 PLANNED & user-confirmed (axis-reorg, novel-contribution chapter). BLOCKED on ExKMC install + CLASSIX .explain() extractor + (optionally) RetailRocket run before prose can be drafted. See [[erp-ch4-results-benchmark]], [[erp-ch3-methodology]].
