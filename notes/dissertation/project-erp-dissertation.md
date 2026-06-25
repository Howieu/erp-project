---
name: project-erp-dissertation
description: "User's MSc Data Science ERP dissertation at University of Manchester — research plan, scope, progress"
metadata: 
  node_type: memory
  type: project
  originSessionId: cc3219b9-5623-4ea8-ac7d-16de24043c42
---

> ⚠️ **SUPERSEDED (2026-06-25).** This note predates the structural changes: the chapter spine is now **6 chapters (Results merged)**, datasets pivoted **RetailRocket→UCI Online Retail**, rule extractor pivoted **CREAM→ExKMC**, and a **mathematical-analysis section** was added to Ch3. For the current authoritative state, structure, and where-to-continue, see **`index.md`** and the memory file **`erp-paper-architecture.md`**. The text below is kept for history only.

## ERP Dissertation — Explainable Clustering

**Degree:** MSc Data Science, University of Manchester
**Deadline:** September 2026
**GitHub:** https://github.com/Howieu/erp-project
**Local path:** ~/erp-project
**Plan file:** notes/RESEARCH_PLAN_SESSION1.md

### Core Thesis (REVISED 2026-06-13 — defensible version)
CLASSIX achieves clustering quality competitive with RFM + K-Means and is robust across cluster shapes — NOT uniformly superior (Ch4 v3 benchmark: CLASSIX wins/ties on the shape sets but trails K-Means on real/high-dimensional data, mirroring Chen & Güttel's own real-data results) — BUT its geometric explanations have higher explanation complexity and cannot be directly translated into operational actions, whereas the threshold-tree rules from explainable k-means (Moshkovitz et al. 2020, ExKMC) are more parsimonious and directly actionable. Trade-off: "clustering quality <-> explanation usability", evaluated jointly.

**CRITICAL CONSTRAINT (user confirmed):** User CANNOT do a real user study and CANNOT interview operations staff. So "intuitiveness/usability" is operationalized as OBJECTIVE PROXIES, NOT human evaluation:
- Rule side (CREAM/PSyKE): rule count, conditions per rule, total rule length, coverage, fidelity to K-Means
- Geometric side (CLASSIX): explanation dimensionality, number of starting points, explanation size
- Argument leans on XAI cognitive-load literature (Miller 2019; Doshi-Velez & Kim 2017) that simpler/shorter explanations = lower cognitive load
- Absence of real user study written into Limitations (acknowledged)
- Original wording "more intuitive for business users" was a claim about humans the user can't test — deliberately reframed to "lower explanation complexity + directly actionable"

### Experimental Design
- Clustering (RQ1-3): CLASSIX, K-Means++, DBSCAN, Hierarchical
- Explainability (RQ4): CLASSIX.explain() vs CREAM rules via PSyKE (post-hoc on K-Means)
- CREAM is NOT a standalone clustering algorithm in this study — it's a post-hoc rule extractor
- Datasets: benchmark datasets + RetailRocket (backup: UCI Online Retail)

### Chapter Structure (~8,300 words total)
1. Introduction (~800w)
2. Literature Review (~1,500w) — 2.1 E-commerce segmentation, 2.2 Explainability, 2.3 CLASSIX, 2.4 CREAM, 2.5 Gap
3. Methodology (~1,500w)
4. Results: Benchmark (~1,500w)
5. Results: Domain Study RetailRocket (~1,500w)
6. Discussion (~1,000w)
7. Conclusion (~500w)

### One-Month Timeline
- Week 1: Understand algorithms, set up env, lit review
- Week 2: Implement methods, run benchmark
- Week 3: RetailRocket domain study, analysis
- Week 4: Write dissertation

### Citation Format
Harvard (University of Manchester style)

### Libraries
- `pip install classix` (CLASSIX official)
- `pip install psyke` (CREAM via PSyKE)
- scikit-learn for baselines

### Where We Stopped (Session 2 — 2026-06-13)
Chapter 1 Introduction CONFIRMED & LOCKED via Socratic dialogue. Key results:
- Hook: operations staff get cluster result + explanation, still can't decide next action ("decision paralysis", not algorithm accuracy)
- Gap (sharpened): existing work only compares clustering QUALITY, nobody compares explanation USABILITY; geometric vs rule explanation in e-commerce never systematically compared
- Timeliness = 3-layer funnel: XAI hot but classifier-focused -> e-commerce data-driven decision gap widening -> CLASSIX-type self-explaining clustering algos new & untested in retail
- Intro word count ~800w, four-part skeleton: Hook -> Background -> Gap -> Purpose & RQ
- Thesis revised to defensible proxy-based version (see Core Thesis above)

NEXT: Chapter 2 Literature Review Socratic planning. Need to find lit on "measuring interpretability via explanation complexity" (Miller 2019, Doshi-Velez & Kim 2017) to back the proxy approach.
Still pending: email supervisor about CREAM's role in the project.

**Why:** User started with no code written, no algorithm understanding. Full planning was done in session 1 before any implementation.
**How to apply:** When user returns, load RESEARCH_PLAN_SESSION1.md and resume from Chapter 1 Introduction planning, or pivot to implementation if they're ready.
