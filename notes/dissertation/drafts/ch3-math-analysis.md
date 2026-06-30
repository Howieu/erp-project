## 3.7 CLASSIX 的算法性质（数学分析）

本节不提出新方法，而是用数学解释第 4 章观测到的三个现象——通过分析 CLASSIX 的聚合步骤（`aggregate_ed.py` 中的例程）。三个结果构成一条逻辑链：排序搜索是**精确的**（因此提速没有牺牲精度），所以测得的**近线性成本**是真实的效率收益，而该过程是**确定的**（因此第 4 章中跨随机种子方差为零是必然，而非偶然）。下文记号均针对标准化后的数据；$\mathrm{tol}$ 表示聚合半径。

### 3.7.1 精确剪枝（①）

CLASSIX 按数据点在第一主成分轴 $v\in\mathbb{R}^d$（$\lVert v\rVert = 1$）上的投影排序，记 $p_i=\langle x_i,v\rangle$ 为点 $x_i$ 的排序值。数据点按 $p$ 的非降序扫描。当以某个起始点 $x_i$ 生长一个群组时，内层循环在遇到第一个满足 $p_j-p_i>\mathrm{tol}$ 的后续点 $x_j$ 处停止。

**引理（精确性）.** 若 $p_j-p_i>\mathrm{tol}$，则 $\lVert x_j-x_i\rVert>\mathrm{tol}$。

*证明.* 由于 $\lVert v\rVert=1$，Cauchy–Schwarz 不等式给出
$$p_j-p_i=\langle x_j-x_i,\,v\rangle \le |\langle x_j-x_i,\,v\rangle| \le \lVert x_j-x_i\rVert\,\lVert v\rVert = \lVert x_j-x_i\rVert.$$
故 $p_j-p_i>\mathrm{tol}$ 蕴含 $\lVert x_j-x_i\rVert>\mathrm{tol}$。$\qquad\blacksquare$

由于 $p$ 非降，第一个这样的 $x_j$ 之后的每一个点的投影差也都 $>\mathrm{tol}$，因而都在半径之外。提前终止只丢弃**可证**超出 $\mathrm{tol}$ 的点，所以排序聚合产生的群组与穷举半径搜索完全一致——§3.7.2 的提速是**无损的**。这与保真校验一致：在该校验中，本实现复现官方 CLASSIX 结果，$\max|\Delta\mathrm{ARI}|=0$。

### 3.7.2 近线性成本（③）

对 $n$ 个点排序的代价是 $O(n\log n)$。随后聚合时，对每个起始点 $x_i$，只扫描投影落在区间 $(p_i,\,p_i+\mathrm{tol}]$ 内的点；记该带内点数为 $b_i$。距离计算总次数为 $\mathrm{nr\_dist}=\sum_i b_i$。最坏情况下所有点落在同一条带内（例如数据被压缩到一个 $\mathrm{tol}$ 区间上），代价为 $O(n^2)$；但当投影把数据展开时，平均带宽大致与 $n$ 无关，从而得到近线性成本。

图 3-1 从实证上证实了这一点。在五簇合成数据上（$\mathrm{tol}=0.5$，$n=500$–$16{,}000$），实测 $\mathrm{nr\_dist}$ 按 $n^{1.09}$ 增长（对数–对数斜率为 $1.09$，而暴力法为 $2$）；实际评估的距离计算次数占暴力配对总数 $n(n-1)/2$ 的比例从 $0.0075$ 降到 $0.0003$；每点的距离计算次数基本保持平稳（约 $1.9$–$2.6$）。这种次二次成本正是 §4.1.5 中所测运行时差距的数学原因：CLASSIX 中位 $0.98\,\mathrm{ms}$，K-Means++ 为 $35.68\,\mathrm{ms}$（约 $36\times$）。需声明 favourable case 的前提——分离良好的簇沿第一主轴干净地展开；对抗性数据会使该过程退回到 $O(n^2)$ 上界。

### 3.7.3 确定性（④）

**命题.** CLASSIX 的划分是数据的确定性函数：在任意随机种子下重复运行都返回完全相同的标签。

*论证.* 唯一取方向值的量是第一主成分轴 $v$，特征值/SVD 求解器只能将其确定到符号（$v$ 或 $-v$）。实现通过用 $s=\operatorname{sign}(-p_1)$ 缩放排序值、并按 $s\,p_i$ 排序来固定该符号。在 $v\mapsto -v$ 下，每个 $p_i\mapsto -p_i$，故 $s\mapsto -s$，而缩放后的值 $s\,p_i$ 保持不变；因此排序次序、条带搜索以及成员判定（它们只依赖内积与范数，不依赖 $v$ 的朝向）都完全相同。没有任何一步抽取随机性，故标签仅由数据决定。$\qquad\blacksquare$

第 4 章证实了这一点：跨 5 个种子，CLASSIX（以及其他确定性方法）的 ARI 标准差为 $0$，而 K-Means++ 因其随机初始化呈现 $0.0093$。

> **脚注（②，实现层面）.** 成员判定是精确半径判定的代数重组：$\lVert x_i-x_j\rVert^2\le\mathrm{tol}^2 \iff \tfrac12\lVert x_i\rVert^2+\tfrac12\lVert x_j\rVert^2-\langle x_i,x_j\rangle\le \tfrac12\mathrm{tol}^2$。CLASSIX 把 $\tfrac12\lVert x\rVert^2$ 预计算一次，并用一次矩阵–向量乘积得到整条带的内积，因此每次比较只需一次点积，而非重新计算一次欧氏距离。

综合这三条性质，可以把 CLASSIX 的速度与稳定性（第 4 章）当作**结构性保证**，而非某个特定数据集或某次运行的偶然产物。
