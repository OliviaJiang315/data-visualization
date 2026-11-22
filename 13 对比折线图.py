# -*- coding: utf-8 -*-
"""13 对比折线图 (依据 Excel chart12.xml 精确复刻)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

months = ['1月', '2月', '3月', '4月', '5月', '6月']
v2021 = [1686, 1345, 1934, 1658, 1865, 1936]
v2022 = [1385, 1846, 1654, 1936, 2564, 2236]

BG = '#1A1E43'
PINK = '#E74E69'
BLUE = '#0070C0'

fig, ax = plt.subplots(figsize=(12, 7.5), facecolor=BG)
ax.set_facecolor(BG)
ax.set_position([0.08, 0.14, 0.85, 0.58])

x = np.arange(len(months))

# Y轴网格线 (白色长虚线)
ax.grid(axis='y', color='white', alpha=0.2, linestyle='--', linewidth=0.8, zorder=0)

# 2021年 折线 (粉红, 圆形标记)
ax.plot(x, v2021, color=PINK, linewidth=2.2, marker='o', markersize=8,
        markerfacecolor=PINK, markeredgecolor=BG, markeredgewidth=1.2, zorder=3, label='2021年')
# 2022年 折线 (蓝色, 圆形标记)
ax.plot(x, v2022, color=BLUE, linewidth=2.2, marker='o', markersize=8,
        markerfacecolor=BLUE, markeredgecolor=BG, markeredgewidth=1.2, zorder=3, label='2022年')

# 数据标签 (上面的线标上方, 下面的线标下方)
for i in range(len(months)):
    if v2021[i] >= v2022[i]:
        ax.text(x[i], v2021[i] + 60, str(v2021[i]), ha='center', va='bottom',
                color='white', fontsize=9, zorder=4)
        ax.text(x[i], v2022[i] - 60, str(v2022[i]), ha='center', va='top',
                color='white', fontsize=9, zorder=4)
    else:
        ax.text(x[i], v2022[i] + 60, str(v2022[i]), ha='center', va='bottom',
                color='white', fontsize=9, zorder=4)
        ax.text(x[i], v2021[i] - 60, str(v2021[i]), ha='center', va='top',
                color='white', fontsize=9, zorder=4)

# 坐标轴
ax.set_xlim(-0.3, len(months) - 0.7)
ax.set_xticks(x)
ax.set_xticklabels(months, color='white', fontsize=11)
ax.tick_params(axis='x', length=0)
ax.set_ylim(0, 3000)
ax.set_yticks(np.arange(0, 3001, 500))
ax.set_yticklabels([str(v) for v in np.arange(0, 3001, 500)], color='white', fontsize=10)
ax.tick_params(axis='y', length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

# 图例 (顶部右侧)
leg = ax.legend(loc='upper left', bbox_to_anchor=(0.62, 1.10), ncol=2,
                frameon=False, fontsize=11, labelcolor='white')

# 标题/副标题/注释
label_x = 0.05
fig.text(label_x, 0.88, '2022年上半年各月同比去年销量', fontsize=29, fontweight='bold',
         color='white', ha='left')
fig.text(label_x, 0.82, '上半年同比去年增长明显，5月份同比增长最多，增长近40%',
         fontsize=17, color='white', ha='left')
fig.text(label_x, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         fontsize=11, color='white', ha='left')

plt.savefig('13 对比折线图.png', dpi=150, facecolor=BG)
print("已生成 13 对比折线图.png")
