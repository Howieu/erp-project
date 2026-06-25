## 3.x CLASSIX 的算法性质（数学分析）

本节不提出新方法，而是用数学解释第 4 章观测到的三个现象——通过分析 CLASSIX 的聚合步骤（`aggregate_ed.py` 中的例程）。三个结果构成一条逻辑链：排序搜索是**精确的**（因此提速没有牺牲精度），所以测得的**近线性成本**是真实的效率收益，而该过程是**确定的**（因此第 4 章中跨随机种子方差为零是必然，而非偶然）。下文记号均针对标准化后的数据；$\mathrm{tol}$ 表示聚合半径。

### 3.x.1 精确剪枝（①）

CLASSIX 按数据点在第一主成分轴 $v\in\mathbb{R}^d$（$\lVert v\rVert = 1$）上的投影排序，记 $p_i=\langle x_i,v\rangle$ 为点 $x_i$ 的排序值。数据点按 $p$ 的非降序扫描。当以某个起始点 $x_i$ 生长一个群组时，内层循环在遇到第一个满足 $p_j-p_i>\mathrm{tol}$ 的后续点 $x_j$ 处停止。

**引理（精确性）.** 若 $p_j-p_i>\mathrm{tol}$，则 $\lVert x_j-x_i\rVert>\mathrm{tol}$。

*证明.* 由于 $\lVert v\rVert=1$，Cauchy–Schwarz 不等式给出
$$p_j-p_i=\langle x_j-x_i,\,v\rangle \le |\langle x_j-x_i,\,v\rangle| \le \lVert x_j-x_i\rVert\,\lVert v\rVert = \lVert x_j-x_i\rVert.$$
故 $p_j-p_i>\mathrm{tol}$ 蕴含 $\lVert x_j-x_i\rVert>\mathrm{tol}$。$\qquad\blacksquare$

由于 $p$ 非降，第一个这样的 $x_j$ 之后的每一个点的投影差也都 $>\mathrm{tol}$，因而都在半径之外。提前终止只丢弃**可证**超出 $\mathrm{tol}$ 的点，所以排序聚合产生的群组与穷举半径搜索完全一致——§3.x.2 的提速是**无损的**。这与保真校验一致：在该校验中，本实现复现官方 CLASSIX 结果，$\max|\Delta\mathrm{ARI}|=0$。
