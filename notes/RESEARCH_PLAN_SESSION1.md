# ERP Research Plan — Session 1 Output
# Date: 2026-06-10

---

## Project Overview

**Title (working):** Benchmarking Explainable Clustering: A Comparative Study of CLASSIX, CREAM and Baseline Methods
**Degree:** MSc Data Science, University of Manchester
**Deadline:** September 2026
**Target length:** ~8,000 words
**Citation format:** Harvard (UoM)

---

## Core Thesis Statement

> In an e-commerce setting, CLASSIX produces clustering quality competitive with the industry-standard RFM + K-Means approach and is robust across cluster shapes (rather than uniformly better), and provides geometric explanations of cluster structure — but those explanations carry higher explanation complexity and are harder to turn into operational actions than the parsimonious threshold-tree rules of explainable k-means (ExKMC). Neither is a perfect solution; the right choice depends on whether the priority is cluster quality or explanation usability.

---

## Revised Experimental Design

### Clustering comparison (RQ1–3)
- CLASSIX (nla-group/classix)
- K-Means++ (scikit-learn)
- DBSCAN (scikit-learn)
- Agglomerative Hierarchical Clustering (scikit-learn)

### Explainability comparison (RQ4)
- CLASSIX `.explain()` — geometric, distance-based
- CREAM rules via PSyKE — decision-tree rules applied post-hoc on K-Means results

**Key design decision:** CREAM is treated as a post-hoc explanation layer, not a standalone clustering algorithm. This is more architecturally accurate and avoids dependency on an immature library.

---

## Research Questions

- **RQ1:** How do CLASSIX and baseline methods compare in clustering quality across benchmark datasets? (ARI, NMI, Silhouette, Davies-Bouldin, Calinski-Harabasz)
- **RQ2:** How do methods differ in runtime, memory use, and scalability?
- **RQ3:** How robust are methods to parameter choices, noise, outliers, and repeated runs?
- **RQ4:** Do CLASSIX and CREAM provide clearer, more practically useful explanations on e-commerce data (RetailRocket)?

---

## Chapter Structure

| Chapter | Title | Target words |
|---------|-------|-------------|
| 1 | Introduction | ~800 |
| 2 | Literature Review | ~1,500 |
| 3 | Methodology | ~1,500 |
| 4 | Results: Benchmark | ~1,500 |
| 5 | Results: Domain Study (RetailRocket) | ~1,500 |
| 6 | Discussion | ~1,000 |
| 7 | Conclusion | ~500 |
| **Total** | | **~8,300** |

---

## Chapter 2 — Literature Review Structure

- 2.1 E-commerce customer segmentation (RFM, K-Means as industry default)
- 2.2 Why explainability matters in clustering
- 2.3 CLASSIX: mechanism, strengths, limitations
- 2.4 CREAM: mechanism, rule-based explanations, architectural role
- 2.5 Research gap

---

## Key Algorithms & Libraries

| Tool | Role | Install |
|------|------|---------|
| classix | Main explainable clustering | `pip install classix` |
| psyke | CREAM rule extraction | `pip install psyke` |
| scikit-learn | Baseline methods | `pip install scikit-learn` |

---

## Datasets

- **Benchmark:** Standard clustering benchmark datasets (varying shape, dimensionality, noise)
- **Domain:** RetailRocket (e-commerce user events) — backup: UCI Online Retail

---

## One-Month Timeline

| Week | Focus |
|------|-------|
| Week 1 (Jun 10–16) | Understand CLASSIX + CREAM, set up environment, literature review |
| Week 2 (Jun 17–23) | Implement all methods, run benchmark experiments |
| Week 3 (Jun 24–30) | RetailRocket domain study, results analysis |
| Week 4 (Jul 1–7) | Write dissertation (8,000 words) |

---

## Next Step in Planning (where we stopped)

Working through Chapter 1 Introduction via Socratic dialogue.

**Pending question:** In an e-commerce setting (e.g. Shopee/Tmall), when K-Means tells the operations team "these 3,200 users are in Cluster 2" — what does the operations team say next? This answer becomes the opening hook of the Introduction.
