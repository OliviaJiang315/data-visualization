# -*- coding: utf-8 -*-
"""27 簇状柱形折线图 (依据 chart14.xml 复刻主图 Chart4)

barChart 簇状柱2系列(2022销量蓝0070C0 + 2021销量红E74E69 并排, 主轴0-5000, 柱顶白数值)
+ lineChart 同比去年(黄FFC000, circle marker, 次轴 min-1.1, 折线白%标签)
X轴灰蓝横线#454866(基线), 横轴6区域, 左上标题/副标题, 左下注释, 背景#1A1E43, 无图例
几何来自 _chart27_obj1.png(2.08x, Chart 438.9x311.4) 实测
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'; BLUE = '#0070C0'; RED = '#E74E69'; YEL = '#FFC000'; TXT = '#F2F2F2'
W, H = 438.9, 311.4
x = np.arange(6)
s2022 = [2354, 1902, 3524, 2698, 2896, 2563]
s2021 = [2021, 1563, 3213, 2531, 2631, 2361]
yoy = [0.16, 0.22, 0.10, 0.07, 0.10, 0.09]
regions = ['华北', '华南', '东北', '西北', '西南', '华东']

fig = plt.figure(figsize=(10, 10 * H / W), facecolor=BG)
ax = fig.add_axes([0.0811, 0.159, 0.844, 0.576], facecolor='none')
ax2 = ax.twinx()

# 簇状柱: 蓝2022(左) 红2021(右)
ax.bar(x - 0.145, s2022, width=0.22, color=BLUE, zorder=2)
ax.bar(x + 0.145, s2021, width=0.22, color=RED, zorder=2)
# 同比黄折线(次轴)
ax2.plot(x, yoy, color=YEL, lw=1.5, marker='o', markersize=5,
         markerfacecolor=YEL, markeredgecolor=YEL, zorder=4)

ax.set_xlim(-0.5, 5.5); ax.set_ylim(0, 5000)
ax2.set_ylim(-1.1, 0.30)
ax.set_yticks([]); ax2.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
for s in ax2.spines.values(): s.set_visible(False)
ax.tick_params(axis='x', length=0)
# X轴灰蓝横线(基线)
ax.axhline(0, color='#454866', lw=2.5, zorder=1, clip_on=False)

# 柱顶白数值(2022蓝柱左/2021红柱右)
for i in range(6):
    ax.text(i - 0.145, s2022[i] + 90, str(s2022[i]), ha='center', va='bottom', color=TXT, fontsize=9, zorder=5)
    ax.text(i + 0.145, s2021[i] + 90, str(s2021[i]), ha='center', va='bottom', color=TXT, fontsize=9, zorder=5)
# 折线白%标签(黄点上方)
for i in range(6):
    ax2.text(i, yoy[i] + 0.03, f'{yoy[i]*100:.0f}%', ha='center', va='bottom', color=TXT, fontsize=9, zorder=6)

# 横轴区域名
for i, cat in enumerate(regions):
    cx = 0.0811 + (i+0.5)/6*0.844
    fig.text(cx, 0.121, cat, ha='center', va='center', color=TXT, fontsize=12)

# 标题/副标题(左上)
fig.text(0.054, 0.937, '上半年各月商品销量同比去年情况', ha='left', va='top', color=TXT, fontsize=30, fontweight='bold')
fig.text(0.053, 0.844, '2022年相比于2021年销量都有提升，半年整体提升17%', ha='left', va='top', color=TXT, fontsize=20)
# 注释(左下)
fig.text(0.052, 0.049, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', ha='left', va='center', color='#C8C8C8', fontsize=13)

# 华东组红蓝柱正中间: 2022/2021 垂直叠放(2022上蓝框/2021下红框, 深蓝底, 白字居中)
cx = 0.8545; bw, bh, gap = 0.052, 0.032, 0.011
for name, cy, ec in [('2022', 0.335, BLUE), ('2021', 0.335 - bh - gap, RED)]:
    fig.add_artist(Rectangle((cx - bw/2, cy - bh/2), bw, bh, transform=fig.transFigure,
                             facecolor=BG, edgecolor=ec, lw=1.8, zorder=8))
    fig.text(cx, cy - 0.002, name, ha='center', va='center', color=TXT, fontsize=11, zorder=9)

plt.savefig('27 簇状柱形折线图.png', dpi=150, facecolor=BG)
print('已生成 27 簇状柱形折线图.png')