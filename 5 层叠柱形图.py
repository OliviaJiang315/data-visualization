import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
sales = [3121, 4086, 4321, 4601, 4936, 4231]
profits = [1020, 1421, 1502, 1623, 1781, 1432]

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1a1f3c')
ax.set_facecolor('#1a1f3c')

ax.set_position([0.12, 0.20, 0.85, 0.50])

x = np.arange(len(quarters))
width = 0.22

ax.bar(x - width/3, sales, width, color='#0e7ddc', zorder=2, label='销售额')
ax.bar(x + width/3, profits, width, color='#f05a6a', zorder=3, label='利润额')

for i, val in enumerate(sales):
    ax.text(i - width/3, val + 100, str(val),
            ha='center', va='bottom',
            color='white', fontsize=12, zorder=6)
for i, val in enumerate(profits):
    ax.text(i + width/3, val + 100, str(val),
            ha='center', va='bottom',
            color='white', fontsize=12, zorder=6)

ax.set_ylim(0, 6000)
ax.set_yticks([])

ax.set_xticks(x)
ax.set_xticklabels(quarters, color='white', fontsize=11)
ax.tick_params(axis='x', length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

last_x = len(quarters) - 1 - width/3
bar_left = last_x - width/2
ax.text(bar_left, 3700, '   销售额   ',
        ha='left', va='center',
        color='white', fontsize=14, zorder=7,
        bbox=dict(boxstyle="square,pad=0.25", fc='#1a1f3c', ec='#0e7ddc', lw=1.5))
ax.text(bar_left, 2800, '   利润额   ',
        ha='left', va='center',
        color='white', fontsize=14, zorder=7,
        bbox=dict(boxstyle="square,pad=0.25", fc='#1a1f3c', ec='#f05a6a', lw=1.5))

label_x = 0.12
fig.text(label_x, 0.88, '2021年至今季度销售额(万)和利润额(万)', fontsize=24, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.78, '2022年第二季度销售额首次出现下降，降幅达到15%', fontsize=16, color='white', ha='left')
fig.text(label_x, 0.08, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', fontsize=12, color='white', ha='left')

plt.savefig('3.png', dpi=150, facecolor='#1a1f3c')
print("已生成 3.png")
