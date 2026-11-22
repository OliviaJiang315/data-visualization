# -*- coding: utf-8 -*-
"""23 柱形折线图 (依据 第二章 图表(后15).xlsx chart8.xml 精确复刻)

barChart 销售量(蓝0070C0,左轴0-6000) + lineChart 同比(红E74E69,右轴-1.2~0.5,显示百分比)
深蓝背景 #1A1E43, 柱顶数值标签, 折线点百分比标签, 横轴年份2017-2022,
左上标题/副标题, 底部图例(中上部), 左下注释.
几何来自 _chart23_clip.png(2.08x) 实测; 图例位于 y≈0.26(图上部) x≈0.67-0.85
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
RED = '#E74E69'
TXT = '#F2F2F2'

W, H = 438.86, 299.57
x = np.arange(6)
vals = [1603, 2106, 2406, 3265, 3721, 3921]
yoy = [0.27, 0.31378665003119144, 0.14245014245014254,
       0.35702410640066495, 0.1396630934150076, 0.053748992206396062]
years = ['2017', '2018', '2019', '2020', '2021', '2022']

fig = plt.figure(figsize=(10, 10 * H / W), facecolor=BG)
ax = fig.add_axes([0.076, 0.162, 0.846, 0.585], facecolor='none')
ax2 = ax.twinx()

ax.bar(x, vals, width=0.31, color=BLUE, zorder=2)
ax.set_xlim(-0.5, 5.5); ax.set_ylim(0, 6000)
ax2.set_ylim(-1.2, 0.5)
ax2.plot(x, yoy, color=RED, lw=1.5, marker='o', markersize=5, zorder=3)

ax.set_yticks([]); ax2.set_yticks([])
for a in (ax, ax2):
    for s in a.spines.values():
        s.set_visible(False)
ax.tick_params(axis='x', colors=TXT, length=0, labelsize=9)
ax.set_xticks(x); ax.set_xticklabels(years, color=TXT)

# 柱顶数值标签
for i, v in enumerate(vals):
    ax.text(i, v + 130, str(v), ha='center', va='bottom', color=TXT, fontsize=11)

# 折线点百分比标签(白色)
for i, v in enumerate(yoy):
    ax2.text(i, v + 0.035, f'{v*100:.0f}%', ha='center', va='bottom', color=TXT, fontsize=11)

# 图例 (中上部偏右, 手绘): 蓝线段"销售量" + 红线段(带点)"同比"
fig.add_artist(Line2D([0.673, 0.716], [0.741, 0.741], transform=fig.transFigure,
                       color=BLUE, lw=5, solid_capstyle='butt'))
fig.text(0.722, 0.741, '销售量', ha='left', va='center', color=TXT, fontsize=10)
fig.add_artist(Line2D([0.800, 0.823, 0.846], [0.741, 0.741, 0.741], transform=fig.transFigure,
                       color=RED, lw=1.5, marker='o', markersize=6, markevery=[1]))
fig.text(0.852, 0.741, '同比', ha='left', va='center', color=TXT, fontsize=10)

# 标题/副标题(左上): 主标题再加大(fontsize24), 副标题字号不变(14)下移避让
fig.text(0.063, 0.933, '近六年销售量及增长率', ha='left', va='top',
         color=TXT, fontsize=24, fontweight='bold')
fig.text(0.063, 0.868, '平台销量近6年持续增长，但近两年增长率有所放缓', ha='left', va='top',
         color=TXT, fontsize=14)

# 注释(左下)
fig.text(0.059, 0.035, '*注：数据来源于公司销售系统', ha='left', va='bottom',
         color='#C8C8C8', fontsize=13)

plt.savefig('23 柱形折线图.png', dpi=150, facecolor=BG)
print('已生成 23 柱形折线图.png')