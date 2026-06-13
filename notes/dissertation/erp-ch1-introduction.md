---
name: erp-ch1-introduction
description: "ERP dissertation Chapter 1 Introduction — LOCKED plan from Socratic session 2 (2026-06-13): hook, gap, timeliness, four-part skeleton, revised defensible thesis"
metadata: 
  node_type: memory
  type: project
  originSessionId: f62599b1-95d3-46f4-8e28-3cd9bc9d22fb
---

# ERP Dissertation — Chapter 1 Introduction (LOCKED 2026-06-13)

Confirmed via Socratic plan-mode dialogue (ARS academic-paper `plan` mode). Part of [[project-erp-dissertation]]. Target ~800 words.

## Core Purpose
Make the reader feel the real pain in e-commerce customer segmentation is NOT "is the algorithm accurate" but "even with the cluster result AND its explanation in hand, the operations person still can't understand or act on it."

## Core Argument
A clustering's value ultimately depends on whether its explanation can be turned into action by business staff; therefore "explanation usability" must be evaluated alongside "clustering quality" — and that joint evaluation is the blind spot in existing work.

## Four-Part Skeleton
| Part | Content |
|------|---------|
| **Hook** | An operations person stares at Cluster 2's geometric explanation ("within distance threshold") and still can't answer "who are these people / what do I do next" — decision paralysis. |
| **Background** | E-commerce relies on customer segmentation for precision operations; clustering (RFM + K-Means) is the mainstream tool. |
| **Gap** | Literature only compares clustering QUALITY, never explanation USABILITY; geometric vs rule-based explanation never systematically compared in an e-commerce setting. |
| **Purpose & RQ** | On real e-commerce data (RetailRocket etc.), compare CLASSIX geometric explanation vs CREAM rule explanation usability, and quantify the "explanation intuitiveness <-> clustering quality" trade-off. |

## Timeliness (3-layer funnel, top→bottom)
1. XAI is hot right now but overwhelmingly focused on classification models — clustering explainability is neglected.
2. E-commerce data explosion + growing reliance on data-driven decisions → the "model gives a result nobody can use" gap is widening and increasingly painful.
3. CLASSIX (2022) and similar self-explaining clustering algorithms are new and have NOT been tested for explanation usability in real retail scenarios.

## Revised Defensible Thesis (replaces original)
CLASSIX beats RFM+K-Means on clustering quality, BUT its geometric explanation has higher explanation complexity and can't be directly turned into operational action, whereas PSyKE-extracted CREAM rules are more parsimonious and directly actionable. Trade-off "clustering quality <-> explanation usability" evaluated jointly.

**Why the rewrite:** original claim "more intuitive for business users" is a claim about humans the user CANNOT test (no user study, no access to operations staff for interviews). Reframed to objective proxies. See [[project-erp-dissertation]] Core Thesis + CRITICAL CONSTRAINT.

## Flagged Risk (must answer in Ch3 Methodology)
"Explanation usability" sounds subjective. Reviewer will ask: how do you objectively measure whether operations "understand" it? Answer = objective proxies (rule count / conditions per rule / fidelity / coverage; geometric explanation dimensionality), backed by cognitive-load literature (Miller 2019; Doshi-Velez & Kim 2017; Lipton 2018). NOT a real user study.

## Status
Chapter 1 = DONE & user-confirmed. Next chapter in queue: Chapter 2 Literature Review (Socratic planning started — narrative-line draft proposed, awaiting user's coverage self-rating + buy-in on the 5-section story line). See [[project-erp-dissertation]] "Where We Stopped (Session 2)".
