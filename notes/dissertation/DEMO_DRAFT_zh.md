# 可解释的电商客户分群：CLASSIX 几何解释与可解释 K-Means 规则的质量—可用性权衡

> **DEMO 草稿（中文）· 生成于 2026-06-25**
> 这是论文当前状态的演示版，用于通览全文骨架与已有数据。
> 标注约定：**【已锁定，实质正文】** = 计划已定、数据齐全的章节；**【初稿】** = 可写但未经 Socratic 规划；**`[待补]`** = 需补检索/数据/确认之处。
> 结构：按 2026-06-25 决定，原 Ch4/Ch5 合并为单一"结果"章（6 章制）。最终成稿约 8,300 字、Harvard 引用。

---

## 摘要 【初稿】

电商精准运营依赖客户分群，但运营人员的真实痛点往往不是"算法是否准确"，而是"即便拿到了聚类结果和它的解释，依然不知道这群人是谁、下一步该做什么"——一种**决策瘫痪**。现有研究几乎只比较聚类的**质量**，极少系统比较其解释的**可用性**；几何式解释与规则式解释在电商场景下的可用性差异更是空白。

本研究在 9 个基准数据集与 UCI Online Retail 真实电商数据（4,338 名客户的 RFM 特征）上，联合评估两条流水线：流水线甲为自解释的几何聚类 **CLASSIX**，流水线乙为 **K-Means++ 加可解释 K-Means（ExKMC）阈值树规则**。质量与效率层面，CLASSIX 与 K-Means 相当且对簇形状稳健、运行最快（中位 0.98ms，约为 K-Means 的 1/36），但在真实/高维数据上略逊；在无标签的域研究中各内部指标互相矛盾，**质量维度无法分出统一赢家**。解释可用性层面（用客观复杂度代理替代无法开展的真人研究），CLASSIX 几何解释复杂度更高且不可直接转化为运营动作，而 ExKMC 规则简洁、可数、可直接执行；通过扫描 ExKMC 的叶子数 *k′*，"解释复杂度 ↔ 对 K-Means 的保真度"的权衡被画成一条可绘制的曲线。结论：当质量相当时，**解释可用性才是区分两条流水线的决定性维度**。

**关键词**：可解释聚类；客户分群；CLASSIX；可解释 K-Means；RFM；解释可用性

`[待补]`：英文摘要（双语）；定稿后核对数字一致性。

---

## 第 1 章 引言 【已锁定，实质正文】

### 1.1 痛点（Hook）

设想一名电商运营人员，面对系统给出的"簇 #2"。他不仅拿到了这群客户，还拿到了算法附带的解释——"该簇内的点都落在某个距离阈值之内"。然而他依然回答不了两个最朴素的问题：**这群人到底是谁？我下一步该对他们做什么？** 结果不是算法不准，而是**决策瘫痪**：解释存在，却无法转化为行动。

### 1.2 背景

客户分群是电商精准运营的基础设施，用于差异化营销、留存与复购。主流做法是以 **RFM（最近一次消费 Recency、消费频率 Frequency、消费金额 Monetary）** 为特征、用 **K-Means** 聚类。这套方法成熟、可扩展，但其产出的簇本身不自带可被业务直接理解的解释。

### 1.3 研究空白（Gap）

可解释人工智能（XAI）近年极热，但绝大多数工作聚焦**分类模型**，聚类的可解释性被忽视。更关键的是，已有比较几乎只衡量聚类**质量**（如轮廓系数、ARI），从不衡量解释的**可用性**；而几何式解释（如 CLASSIX）与规则式解释（如阈值树）在电商场景中孰优孰劣，**从未被系统比较**。

### 1.4 时效性（三层漏斗）

1. XAI 火热但偏分类，聚类可解释性是被忽略的洼地；
2. 电商数据爆炸、对数据驱动决策的依赖加深，"模型给了结果却没人用得上"的鸿沟在加宽、愈发痛；
3. CLASSIX（2022/2024）这类**自解释聚类算法**很新，尚未在真实零售场景中检验其解释可用性。

### 1.5 研究目的与问题

本研究在真实电商数据上比较 **CLASSIX 几何解释**与**可解释 K-Means（ExKMC）规则解释**的可用性，并量化"解释可用性 ↔ 聚类质量"的权衡。

> **说明（与早期计划的差异）**：早期计划拟用 RetailRocket + CREAM/PSyKE。实施中改用 **UCI Online Retail**（事务级数据含真实单价×数量，Monetary 是真实金额，比 RetailRocket 的事件流更干净）与 **ExKMC**（在 Python 3.10 环境下可稳定安装并直接产出阈值树规则）。论文主线论点不变。`[待补]`：在正文或脚注正式交代此口径切换。

**论点（可辩护版）**：CLASSIX 在聚类质量上与 RFM+K-Means *相当*、对簇形状稳健，但**并非全面更优**——在 shape 数据集上胜/平，在真实/高维数据上逊于 K-Means；然而其几何解释复杂度更高、不可直接转化为运营动作，而 ExKMC 的阈值树规则更简洁、可直接执行。二者构成"质量 ↔ 解释可用性"的权衡，需联合评估。

> **方法学风险（在第 3 章回应）**："解释可用性"听上去主观。本研究**无法开展真人用户研究、无法访谈运营人员**，故将可用性操作化为**客观复杂度代理**（规则数、每条规则条件数、保真度、覆盖度；几何解释的维度与起始点数），并以认知负荷文献（Miller, 2019; Doshi-Velez and Kim, 2017; Lipton, 2018）支撑"更简洁=更低认知负荷"。无真人研究这一点写入局限。

---

## 第 2 章 文献综述 【初稿 / 骨架】

> 本章尚未经 Socratic 规划，仅给出 5 节叙事线与已锁定的核心文献骨架，`[待补]` 处需扩展检索。

### 2.1 电商客户分群与 RFM
RFM + K-Means 作为主流分群范式的综述。`[待补]`：RFM 起源与电商应用文献、K-Means 在零售分群的代表工作。

### 2.2 可解释人工智能（XAI）与可解释性的度量
可解释性的定义与分类（内在可解释 vs 事后解释）；为何"更简单/更短的解释 = 更低认知负荷"。核心文献：**Miller (2019)**（解释的社会科学视角）、**Lipton (2018)**（可解释性的迷思与定义）、**Doshi-Velez and Kim (2017)**（functionally-grounded 评估层级——本研究用客观代理而非真人研究的合法性来源）、**Lakkaraju et al. (2016)**（规则集 size/length 作为可解释性度量）。

### 2.3 自解释聚类：CLASSIX
**Chen and Güttel (2024)**：基于排序的快速、可解释聚类；其几何解释机制（起始点/距离阈值/群组合并），及作者自报的真实数据表现（并非全面碾压）。

### 2.4 可解释 K-Means：阈值树
**Moshkovitz et al. (2020, ExKMC)**：用阈值树近似 K-Means 划分，叶子=规则、深度=每条规则的条件数，并以对 K-Means 的保真度衡量近似质量。

### 2.5 空白小结
质量被反复比较，**解释可用性从未被联合评估**；几何 vs 规则解释在电商分群中未被系统对比——本研究的切入点。

`[待补]`：每节扩充至段落级，补足检索（目标 ~1,500 字），所有引用进 Harvard bib。

---

## 第 3 章 方法论 【初稿，源于已实现代码】

> 方法已由代码定死（`src/benchmark/`、`src/domain/`），本章是把"已经做了什么"正式写成文，并回应第 1 章标记的可用性度量风险。`[待补]`：经 Socratic 规划锁定后定稿。

### 3.1 研究设计：两层 + 联合评估
- **质量/效率层（RQ1–3）**：在受控基准上比较 4 种方法——CLASSIX、K-Means++、DBSCAN、层次聚类（Ward）。
- **域研究层**：UCI Online Retail 真实电商数据（无标签），仅用内部指标。
- **解释可用性层（RQ4）**：流水线甲 CLASSIX（自解释几何）对流水线乙 K-Means++ + ExKMC（阈值树规则）。

### 3.2 数据
- **基准**：9 个数据集，含 shape 集（Jain、Spiral、Aggregation、Compound、Pathbased 等）与真实/高维集（Wine、Seeds 等），部分含 ground truth 以算 ARI/NMI。
- **域数据**：UCI Online Retail（Chen, 2015）。清洗：剔除缺失 CustomerID、撤单（InvoiceNo 以 'C' 开头）、非正的 Quantity/UnitPrice；按客户聚合得 **RFM**（Recency=距快照日天数、Frequency=不同发票数、Monetary=Σ 数量×单价），共 **4,338 名客户**。

### 3.3 预处理
RFM 经 **log1p 变换 + StandardScaler 标准化**（消偏态、统一量纲）。质量层与解释层共用同一特征空间，确保第 4 章质量数字与解释数字一致。

### 3.4 方法与参数搜索
- KMeans++ / Ward：需给定 *k*，域研究取 RFM 惯例 **k=4**（亦为 ExKMC 规则所近似的基）。
- DBSCAN / CLASSIX：无 *k*，在标准化数据上分别扫描 eps / radius 网格。基准层（有标签）按 **最优 ARI** 选配置；域层（无标签）按**最优轮廓系数**选配置（带退化保护：2–12 簇、噪声<50%）。
- **保真度校验**（`src/benchmark/fidelity_check.py`）：CLASSIX 封装与官方实现 max|ΔARI| = 0.0000，确保后续任何差距来自调参而非实现缺陷。

### 3.5 解释可用性的客观代理（回应第 1 章风险）
不开展真人研究，改用 **functionally-grounded**（Doshi-Velez and Kim, 2017）客观代理，分别（Approach A，不做合成总分）报告各方法自己的复杂度画像：
- **CLASSIX 几何**：起始点数、解释维度、解释原语（到原型的距离）。
- **ExKMC 规则**：规则数（叶子）、每条规则条件数（深度）、树节点总数、对 K-Means 的保真度。
并通过扫描 ExKMC 最大叶子数 *k′*，绘制"复杂度 ↔ 保真度"权衡曲线。合法性依据：Doshi-Velez and Kim (2017)、Lakkaraju et al. (2016)、Miller (2019)、Lipton (2018)。

### 3.6 评估指标
- 有标签：ARI、NMI。
- 无标签（内部）：轮廓系数（Silhouette，越高越好）、Davies–Bouldin（越低越好）、Calinski–Harabasz（越高越好）。
- 效率：运行时间。

---

## 第 4 章 结果 【已锁定，实质正文；数据齐全】

> 按 2026-06-25 决定，质量+效率与解释可用性合并为本章两大节。

### 4.1 聚类质量与效率（RQ1–3）

**4.1.1 设置与保真锚点。** 质量竞技场含 9 数据集、4 方法（CLASSIX 含 distance/density 两变体），公平网格搜索。先给保真校验：max|ΔARI| = 0.0000，故后续任何差距属调参而非 bug。

**4.1.2 有标签质量（基准）。** 无统一赢家：CLASSIX 在 shape 集上有竞争力（Jain、Spiral 达 1.0，Aggregation 0.91 居首），在真实/高维集上落后（Wine ARI 0.54，Seeds 0.71），最弱点 Pathbased 0.58。关键细节：CLASSIX 在真实数据 ARI 仅 0.54，但 **NMI 0.686（接近最高）**——说明它恢复了结构，只是在簇数/边界上有别。真实数据均值 NMI（最优配置）：K-Means 0.754 / Ward 0.737 / CLASSIX 0.686 / DBSCAN 0.415。（图 4-1：各数据集最优 ARI）

**4.1.3 无标签质量（UCI Online Retail 域研究）。** 仅内部指标（无标签，不能用 ARI/NMI）。4,338 客户、RFM（log1p+标准化）：

| 方法 | 簇数 | Silhouette↑ | Davies–Bouldin↓ | Calinski–Harabasz↑ |
|---|---|---|---|---|
| K-Means++ (k=4) | 4 | 0.338 | 1.009 | **3328.5** |
| Ward (k=4) | 4 | 0.242 | 1.120 | 2615.1 |
| DBSCAN (eps=0.6, 最优轮廓) | 2 (+33 噪声) | 0.534 | 1.820 | 111.3 |
| CLASSIX (radius=0.8, 最优轮廓) | 2 | **0.563** | **0.311** | 8.1 |
| CLASSIX (radius=0.9, 解释操作点) | 3 | 0.396 | 0.480 | 11.6 |

**关键发现——指标互相矛盾**：Silhouette/DB 偏爱 CLASSIX/DBSCAN 把数据压成 2 个大簇（分得开，但对分群营销无用）；Calinski–Harabasz 强烈偏爱 K-Means 的 k=4（3328 ≫ 8–11）。**域研究里同样没有统一赢家**——也正因如此，解释层（4.2）选 k=4 的 K-Means 簇来做 ExKMC 规则。

**4.1.4 效率与稳健性（RQ2–3）。** CLASSIX 最快：运行时间中位 **0.98ms**，K-Means++ 35.68ms（约 **36×**）；DBSCAN 1.33ms、Ward 2.19ms（图 4-4）。参数敏感性：DBSCAN 对 eps 有"悬崖"式突变（图 4-2），CLASSIX 对 radius 更平滑（图 4-3）。确定性：确定性方法 seed 间 std=0；K-Means 仅在少数集（Compound/Aggregation/Spiral）有初始化方差。

**4.1.5 小结与过渡。** 质量打成一团、CLASSIX 胜在效率，但**质量维度无法给方法排名**——决定性维度是解释可用性（→ 4.2）。

### 4.2 解释可用性（RQ4）——本研究的新颖贡献

**4.2.1 竞技场设置。** 流水线甲=CLASSIX（自解释几何）对流水线乙=K-Means++ + ExKMC（在 K-Means 簇上拟合阈值树规则）。采用流水线对流水线而非"同一聚类的两种解释"，因为 CLASSIX 的几何解释内生于它自己的簇，"同一聚类"不可行。

**4.2.2 复杂度画像（Approach A，分别报告，不做合成分）。**

| 维度 | 甲 CLASSIX（几何） | 乙 ExKMC（规则） |
|---|---|---|
| 解释原语 | 到原型的距离 | 单特征阈值 |
| 起始点数 / 规则数 | 起始点 **42** | 规则（叶子）**4** |
| 解释维度 / 每规则条件数 | 维度 **3** | 最大深度 **3** |
| 规模 | — | 树节点 **7** |

ExKMC 规则（已换算回原始 RFM 单位，**可直接执行**）：
- IF F(orders) ≤ 6 AND R(days) ≤ 26 → （近期活跃的低频客户）
- IF F(orders) ≤ 6 AND R(days) > 26 AND M(£) ≤ 642 → （流失中的低价值客户）
- IF F(orders) ≤ 6 AND R(days) > 26 AND M(£) > 642 → （流失中的高价值客户，需挽回）
- IF F(orders) > 6 → （高频忠诚客户）

CLASSIX 对单个客户的几何解释形如："Data point 1689 is in group 1, which was merged into cluster #0."——可追溯但**不能直接翻译成运营动作**，且需理解 42 个起始点构成的几何结构。

**4.2.3 *k′* 权衡曲线（核心差异点）。** 扫描 ExKMC 最大叶子数 *k′*（从 k=4 起），记录（规则复杂度 ↔ 对 K-Means 保真度）：

| 叶子数 k′ | 深度 | 对 K-Means 保真度 |
|---|---|---|
| 4 | 3 | 0.799 |
| 6 | 3 | 0.833 |
| 8 | 4 | 0.864 |
| 10 | 5 | 0.883 |
| 12 | 5 | 0.896 |
| 16 | 6 | 0.908 |

保真度从 4 叶的 0.799 单调升到 16 叶的 0.908——**用更多规则换更高保真**，把"质量↔解释"的权衡变成一条可绘制的曲线（图 5-1 / fig5-1），CLASSIX 可放在同一平面对照。这是别人没做过的可视化差异点。

**4.2.4 代理有效性（functionally-grounded 盾牌）。** 为何无真人研究仍合法：Doshi-Velez and Kim (2017) 的 functionally-grounded 评估层级允许用客观代理；Lakkaraju et al. (2016) 用 size/length 度量可解释性；Miller (2019)、Lipton (2018) 论证更简单的解释=更低认知负荷。由此回应第 1 章标记的"无用户研究"攻击；无真人研究写入局限。

**4.2.5 小结。** 质量相当（4.1），但解释可用性把两条流水线清晰分开：CLASSIX 几何解释复杂度高、不可直接执行；ExKMC 规则简洁、可数、可直接执行，且 *k′* 旋钮让权衡可被绘制——**这回答了论点**。

---

## 第 5 章 讨论 【初稿】

- **主发现**：当聚类质量相当时，**解释可用性是区分方法的决定性维度**；CLASSIX 胜在速度与自解释性，但其几何解释难以转化为运营动作；ExKMC 规则以可控的复杂度换取对 K-Means 的高保真，且天然可执行。
- **对实践的意义**：电商运营若以"拿来即用的分群规则"为目标，K-Means+ExKMC 流水线更友好；CLASSIX 适合需要极速、探索性、且能接受几何解释的场景。
- **与已有工作的关系**：CLASSIX 在真实数据非全面更优，与 Chen and Güttel (2024) 自报结果一致；本研究的增量是把比较从"质量"推进到"解释可用性"。
- **局限**：(1) 无真人用户研究，可用性以客观代理近似；(2) 基准中真实电商数据有限，外部效度主要靠单一 UCI 数据集；(3) ExKMC 规则的"可执行性"是结构论证，未经业务方实证。`[待补]`：逐条展开。

---

## 第 6 章 结论 【初稿】

本研究在基准与真实电商 RFM 数据上联合评估了 CLASSIX 与 K-Means+ExKMC 两条流水线。质量与效率上 CLASSIX 与 K-Means 相当、对形状稳健且最快，但真实/高维略逊，且无监督内部指标互相矛盾、无法给方法排名。解释可用性上，CLASSIX 几何解释复杂度高、不可直接执行，ExKMC 规则简洁可执行，且 *k′* 权衡可绘成曲线。**核心结论：质量相当时，解释可用性才是决定性维度。** 未来工作：开展真人用户研究验证代理、扩展到更多真实电商数据集、探索几何解释的动作化转换。`[待补]`：精炼至 ~500 字。

---

## 参考文献 【骨架，Harvard，待核】

> 以下为已锁定的核心文献，细节（卷期页/出版方）`[待核]`，定稿前跑一次 citation-check。

- Chen, D. (2015) *Online Retail* [Dataset]. UCI Machine Learning Repository. `[待核 id 352]`
- Chen, X. and Güttel, S. (2024) 'Fast and explainable clustering based on sorting', *Pattern Recognition*. `[待核卷期页]`
- Doshi-Velez, F. and Kim, B. (2017) 'Towards a rigorous science of interpretable machine learning', *arXiv:1702.08608*.
- Lakkaraju, H., Bach, S.H. and Leskovec, J. (2016) 'Interpretable decision sets: A joint framework for description and prediction', *Proceedings of KDD '16*.
- Lipton, Z.C. (2018) 'The mythos of model interpretability', *Communications of the ACM*, 61(10), pp. 36–43. `[待核]`
- Miller, T. (2019) 'Explanation in artificial intelligence: Insights from the social sciences', *Artificial Intelligence*, 267, pp. 1–38.
- Moshkovitz, M., Dasgupta, S., Rashtchian, C. and Frost, N. (2020) 'Explainable k-means and k-medians clustering', *Proceedings of ICML 2020*.

---

## 附录：图表索引

- 图 4-1 各数据集最优 ARI（`results/benchmark_v3/figures/fig4-1`）
- 图 4-2 DBSCAN eps 扫描（fig4-2）
- 图 4-3 CLASSIX radius 扫描（fig4-3）
- 图 4-4 各数据集运行时间（fig4-4）
- 图 5-1 ExKMC *k′* 权衡曲线（`results/domain_uci/fig5-1_kprime_tradeoff.png/pdf`）
- 表（4.1.3）UCI 域内部质量（`results/domain_uci/domain_quality.csv`）
- 表（4.2.3）*k′* 曲线数据（`results/domain_uci/exkmc_kprime_curve.csv`）
