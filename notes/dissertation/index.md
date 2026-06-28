---
name: dissertation-index
description: "Map of Content for the ERP dissertation knowledge base — entry point for Obsidian"
metadata:
  type: index
---

# ERP Dissertation — Knowledge Base (MOC)

MSc Data Science, University of Manchester. Explainable customer segmentation: CLASSIX vs RFM+K-Means, geometric vs rule-based (CREAM/PSyKE) explanation.

> These notes are mirrored from Claude's memory system (`~/.claude/.../memory/`). The memory copies are the source Claude reads to auto-resume planning sessions; this folder is the Obsidian-managed, git-tracked mirror.

## Notes
- [[project-erp-dissertation]] — top-level project: thesis, experimental design, chapter structure, timeline, libraries, current status
- [[erp-ch1-introduction]] — Chapter 1 Introduction, LOCKED plan (hook, gap, timeliness, four-part skeleton, revised thesis)
- [[erp-ch4-results-benchmark]] — Results §4.1 quality+efficiency plan + verified data (benchmark v3 + UCI domain)
- [[erp-ch5-explanation-usability]] — Results §4.2 explanation usability (RQ4) plan + Explanation Arena data
- `DEMO_DRAFT_zh.md` — full Chinese demo draft of the whole dissertation (2026-06-25)

## Chapter status (6-chapter structure — Results merged 2026-06-25)
| Ch | Title | Status |
|----|-------|--------|
| 1 | Introduction | ✅ Locked (Socratic session 2, 2026-06-13); demo prose drafted |
| 2 | Literature Review | ✅ **Drafted** (drafts/ch2-literature-review-zh.md, 2026-06-28) — 5-section funnel, proxy shield, M10 bibliography; 3 backbone surveys (Hu 2024 / Dewoprabowo 2025 / Chen 2018) content-verified. Not yet peer-reviewed. |
| 3 | Methodology | ✅ Locked (ars-plan 2026-06-25): §3.x math analysis drafted, §3.4–3.5 selection protocol, §3.1/3.2/3.3/3.6. ⚠️ triggers Ch4 §4.1 data refresh |
| 4 | Results (4.1 Quality+Efficiency / 4.2 Explanation Usability) | ✅ **Drafted → reviewed → revised → re-review ACCEPTED** (drafts/ch4-results-zh.md, 2026-06-25). Dual-lens §4.1 + §4.2 RQ4; fig4-5/fig4-6 added. 2 residuals carried to Ch5. |
| 5 | Discussion | ⬜ demo initial draft |
| 6 | Conclusion | ⬜ demo initial draft |

> **Merge note (2026-06-25):** former Ch4 (benchmark quality+efficiency) and Ch5 (explanation usability, RQ4) merged into a single Results chapter (Ch4) with two major sections; Discussion/Conclusion renumbered to Ch5/Ch6. The two locked plan notes still hold at the section level.

## Open deliverable gaps vs the M10 brief (proposer: Stefan Güttel — CLASSIX's author)
The M10 brief asks to **describe, analyse, and COMPARE** explainable clustering (not prove CLASSIX superior). Three deliverables: unified review / **mathematical analysis** / benchmarking. Two are under-served and now IN PLAN:
1. **Mathematical analysis** (brief deliverable 2 — e.g. convergence / numerical stability). ⚠️ Currently ABSENT. Needs scoping (likely a CLASSIX-focused analysis: sorting/aggregation step, radius/tolerance behaviour, or stability of the greedy merging). → new section/chapter.
2. **Unified review covering the 3 brief surveys** in Ch2: Hu et al. (2024, arXiv:2409.00743); Dewoprabowo et al. (2025, J. Intelligent Systems 34(1)); Chen, J. (2018, PhD, Northeastern). Plus methods [4] CLASSIX, [5] CREAM (Sabbatini & Calegari 2023), [6] ExKMC.
3. Framing note: surface CLASSIX's real advantages honestly (intrinsic/faithful-by-construction/k-free/fast) — see memory `classix-advantage-framing`. NOT over-claim quality superiority.

## To resume planning with Claude
Say: *"继续 ERP 论文。6 章制，结果章已合并。下一步规划 Ch3 方法论（代码已定，正式写定以消除不一致），或扩展 Ch2 文献检索。记得我没法做用户研究，可解释性用客观代理衡量。"*
