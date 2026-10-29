# -*- coding: utf-8 -*-
"""12 菱形走势图 (依据 Excel chart11.xml 精确复刻)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
vals = [0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704]

BG = '#1A1E43'
PINK = '#E74E69'

fig, ax = plt.subplots(figsize=(12, 7.5), facecolor=BG)
ax.set_facecolor(BG)
ax.set_position([0.08, 0.14, 0.85, 0.58])

x = np.arange(len(months))

# dropLines: 每个点垂直线到X轴(底部)
y_min = 0.2
for xi, vi in zip(x, vals):
    ax.plot([xi, xi], [y_min, vi], color=PINK, linewidth=1.2, zorder=1)

# 菱形标记 (深蓝填充, 粉红边框), 无连线
ax.plot(x, vals, linestyle='None', marker='D', markersize=9,
        markerfacecolor=BG, markeredgecolor=PINK, markeredgewidth=1.8, zorder=3)

# 数据标签 (顶部, 百分比, 白色)
for xi, vi in zip(x, vals):
    ax.text(xi, vi + 0.018, '%.2f%%' % (vi * 100), ha='center', va='bottom',
            color='white', fontsize=10, zorder=4)

# X轴
ax.set_xlim(-0.5, len(months) - 0.5)
ax.set_xticks(x)
ax.set_xticklabels(months, color='white', fontsize=11)
ax.tick_params(axis='x', length=0)

# Y轴隐藏
ax.set_ylim(y_min, 0.72)
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# X轴底线
ax.axhline(y=y_min, color='white', linewidth=1, alpha=0.4, zorder=0)

# 标题/副标题/注释
label_x = 0.05
fig.text(label_x, 0.88, '2022年1-8月公司计划完成率', fontsize=29, fontweight='bold',
         color='white', ha='left')
fig.text(label_x, 0.82, '公司整体完成率55%，4月和8月超过70%，2月和6月较低未过半',
         fontsize=20, color='white', ha='left')
fig.text(label_x, 0.04, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         fontsize=13, color='white', ha='left')

plt.savefig('12 菱形走势图.png', dpi=150, facecolor=BG)
print("已生成 12 菱形走势图.png")
