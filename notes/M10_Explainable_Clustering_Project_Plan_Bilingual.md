# M10 Explainable Clustering Project Plan
# M10 可解释聚类项目计划

> Revised to match `DSM Project Plan Outline.docx`
> 已按 `DSM Project Plan Outline.docx` 的提交结构和字数要求重组

**Student name / 学生姓名**: [Add]  
**Student number / 学号**: [Add]  
**Project title / 题目**: Benchmarking Explainable Clustering: A Comparative Study of CLASSIX, CREAM and Baseline Methods  
**Supervisor / 导师**: [Add]  
**Project partner / 合作方**: N/A

---

## 1. Non-technical Project Summary / 非技术项目摘要

**English submission version (121/150 words)**  
This project investigates whether explainable clustering methods can provide clearer and more useful results than standard clustering techniques. The main focus is on CLASSIX and CREAM, which will be compared with common benchmark methods including k-means++, hierarchical clustering, and DBSCAN. Two types of data will be used. First, standard benchmark datasets will allow fair comparison with earlier studies. Second, one publicly available domain-specific dataset will test whether these methods remain useful in a realistic application setting where interpretable groupings matter. The comparison will consider cluster quality, computational efficiency, robustness to data and parameter changes, and the clarity of the explanations each method provides. The project aims to show when explainable clustering offers real practical value and when it mainly adds complexity.

**中文参考**  
本项目研究可解释聚类方法是否比传统聚类方法更清晰、更有实际价值。研究重点是 CLASSIX 和 CREAM，并将它们与 k-means++、层次聚类和 DBSCAN 等常见方法进行比较。项目将同时使用两类数据：一类是标准 benchmark 数据集，用于与已有研究做公平对比；另一类是一个公开的领域数据集，用于检验这些方法在真实应用场景中是否仍然有用。比较维度包括聚类质量、计算效率、对参数与数据变化的鲁棒性，以及解释结果是否清楚易懂。项目不打算提出新算法，而是给出一个结构化的实证评价，说明可解释聚类何时真正有价值、何时只是增加复杂度。

---

## 2. Aim and Research Questions / 研究目标与研究问题

**Aim**  
To evaluate whether explainable clustering methods, especially CLASSIX and CREAM, offer practical advantages over standard clustering methods across benchmark and domain-specific datasets.

**RQ1**  
How do CLASSIX and CREAM compare with k-means++, hierarchical clustering, and DBSCAN in clustering quality across benchmark datasets?

**RQ2**  
How do the selected methods differ in runtime, memory use, and scalability as dataset size and dimensionality increase?

**RQ3**  
How robust are these methods to parameter choices, preprocessing decisions, noise, outliers, and repeated runs?

**RQ4**  
Do CLASSIX and CREAM provide clearer and more practically useful explanations of cluster structure and cluster membership, and do these advantages remain on a domain-specific dataset?

**中文参考**  
研究目标是评估以 CLASSIX 和 CREAM 为代表的可解释聚类方法，是否在标准 benchmark 数据集和领域数据集上比传统聚类方法具有实际优势。四个研究问题分别聚焦：聚类质量、计算效率、鲁棒性，以及解释结果在真实场景中的清晰度和实用性。

---

## 3. Methodology / 研究方法

**English submission version (333/400 words)**  
This project will use a comparative empirical design. It will begin with a focused literature review on explainable clustering, especially CLASSIX and CREAM, to define the comparison criteria and identify suitable baseline methods. The core comparison set will be CLASSIX, CREAM, k-means++, agglomerative hierarchical clustering, and DBSCAN. Keeping this set fixed will control scope and allow consistent evaluation.

Two types of data will be used. First, standard benchmark datasets, including synthetic and real datasets commonly used in clustering studies, will provide controlled cases with different shapes, separation levels, dimensionalities, and noise conditions. Second, the RetailRocket dataset will be used as the domain-specific e-commerce dataset because it contains real user interaction events where interpretable behavioural groupings are commercially meaningful. Data preparation will include cleaning, user-level aggregation, standardisation, and, if necessary, dimensionality reduction.

Feature engineering will group RetailRocket variables into RFM-like activity, conversion, category-diversity/preference, and temporal/session patterns, following recent extended RFM customer-segmentation work. Feature-block ablation and alternative scaling/PCA settings will check whether results are driven by one feature family rather than stable behavioural structure.

All methods will be implemented in Python using established libraries or official code where available. Each method will be run under a clearly documented tuning procedure so that comparisons are as fair and reproducible as possible. Evaluation will cover clustering quality, for example ARI or NMI when labels exist, plus silhouette, Davies-Bouldin, and Calinski-Harabasz scores, efficiency through runtime and memory use, and robustness through sensitivity to parameter settings, preprocessing choices, noise, outliers, and repeated runs. Stability will also be assessed through fixed-seed repeated runs, bootstrap or subsample comparisons, and cluster agreement across dimensionality-reduction settings.

Interpretability will be assessed through explicit qualitative criteria rather than a single invented metric. These criteria will include how clearly a method explains cluster formation, how easily cluster membership can be justified for individual samples, and how practically useful those explanations are on the domain dataset. Results will be analysed using tables and figures, followed by a comparative discussion of strengths, limits, and trade-offs.

**中文参考**  
本项目采用比较型实证研究设计。首先进行聚焦式文献综述，明确 CLASSIX、CREAM 与基线方法的比较标准。方法集合固定为 CLASSIX、CREAM、k-means++、层次聚类和 DBSCAN，以控制研究范围。数据部分分为两层：一是标准 benchmark 数据集，用于考察不同簇形状、分离度、维度和噪声条件下的表现；二是 RetailRocket 电商用户行为数据集，用于检验解释性聚类在真实业务场景中的表现。特征工程会按 RFM-like 活跃度、转化、品类偏好/多样性、时间与会话行为分组，并通过 feature-block ablation、不同标准化方式和 PCA 设置检查结果是否过度依赖某一类特征。实验将在 Python 中完成，尽量使用成熟库或官方实现。评价维度包括聚类质量、运行时间、内存占用、参数敏感性、bootstrap/subsample 稳定性、降维敏感性与解释能力。最后通过表格和图形汇总结果，并讨论不同方法的优势、局限与权衡。

---

## 4. Project Timetable / 项目时间表

**English submission version (130/250 words)**  
April: confirm scope, collect core papers, select the domain-specific dataset, and set up the coding and evaluation pipeline. Milestone 1: final method and data selection.

May: complete the focused literature review, implement or verify CLASSIX, CREAM, and the baseline methods, and run pilot experiments on a small benchmark set. Milestone 2: pilot benchmark completed.

June to July: run the full benchmark experiments, record clustering, efficiency, and robustness measures, and refine parameter ranges and preprocessing choices. Milestone 3: benchmark evaluation completed.

August: carry out the domain-specific evaluation, compare interpretability outputs, and begin results analysis and visualisation. Milestone 4: domain study completed.

Late August to September: draft the dissertation chapters, discuss findings with the supervisor, revise the analysis, and finalise figures, references, and appendices. Milestone 5: full draft and submission-ready version completed.

**中文参考**  
时间安排分为五个阶段：2026 年 4 月完成范围确认、文献收集、领域数据选择和实验管线搭建；5 月完成聚焦综述、方法实现与预实验；6 月至 7 月完成标准 benchmark 的主要实验；8 月完成领域数据评估与结果分析；8 月下旬至 9 月完成论文写作、与导师讨论、修订和最终整理。整个计划设置五个里程碑，分别对应方法与数据确定、预实验完成、benchmark 完成、领域研究完成和完整初稿完成。

### Indicative Gantt Table / 简要 Gantt 表

| Task | Apr 2026 | May 2026 | Jun 2026 | Jul 2026 | Aug 2026 | Sep 2026 |
|---|---|---|---|---|---|---|
| Scope, literature, dataset selection | X | X |  |  |  |  |
| Implementation and pilot tests |  | X | X |  |  |  |
| Benchmark experiments |  |  | X | X |  |  |
| Domain-specific evaluation |  |  |  |  | X |  |
| Analysis and chapter drafting |  |  |  |  | X | X |
| Revision and submission preparation |  |  |  |  |  | X |

**Milestones**  
M1: Scope and dataset finalised  
M2: Pilot benchmark complete  
M3: Full benchmark complete  
M4: Domain study complete  
M5: Full draft complete

---

## 5. Risk Assessment and Management / 风险评估与管理

**English submission version (144/150 words)**  
Five risks are identified, each with a mitigation. First, data suitability: RetailRocket event logs may yield weak or noisy user-level clusters, so the smaller, more curated UCI Online Retail dataset is held as a backup. Second, feature-engineering bias: cluster structure may be an artefact of feature choices, so features are grouped into RFM-like activity, conversion, category-diversity, and temporal blocks, then stress-tested through feature-block ablation and alternative scaling/PCA settings to confirm the structure is not driven by one feature family. Third, high-dimensional clustering instability: sparse retail features weaken distance metrics, so a cluster is treated as meaningful only after agreement across repeated runs, bootstrap/subsample resampling, and dimensionality-reduction settings. Fourth, software and runtime limits: managed via small pilots, fixed seeds, sample caps, and logged runtime and memory. Fifth, weak interpretability signal: if rule-count and feature-count proxies are insufficient, CLASSIX explain() and CREAM rule examples supplement them.

**中文参考**  
共识别五项风险，每项均配有缓解措施。第一，数据适用性：RetailRocket 事件日志在用户级聚合后可能产生较弱或较噪声的簇，因此保留较小且更成熟的 UCI Online Retail 数据集作为备选。第二，特征工程偏差：簇结构可能只是特征选择的产物，因此把特征分为 RFM-like 活跃度、转化、品类多样性和时间行为四个模块，并通过 feature-block ablation 和不同标准化/PCA 设置进行压力测试，确认结构不是由某一类特征单独驱动。第三，高维聚类不稳定：高维稀疏零售特征会削弱距离度量，因此只有在重复运行、bootstrap/subsample 重采样和降维设置三者结果一致时，才把某个簇视为有意义。第四，软件与运行时间限制：通过小规模预实验、固定随机种子、必要时限制样本量、记录运行时间与内存来控制。第五，解释信号偏弱：若 rule count 与 feature count 代理指标不足以区分解释质量，则补充 CLASSIX explain() 与 CREAM 规则的定性案例。

---

## 6. Alignment Notes / 对齐说明

- This markdown version now mirrors the structure of the official outline rather than the earlier exploratory draft.
- The English sections are the submission-facing text; the Chinese sections are reference notes for your own use.
- If needed, this file can now be copied directly into the university template with only personal details added.
