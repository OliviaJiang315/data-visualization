# -*- coding: utf-8 -*-
"""30 对比滑珠图 (chart17 + drawing30 userShapes + _chart30_obj1.png 实测复刻)

barChart(bar/stacked/gapWidth=500): 2022完成率蓝#0070C0 直角条 + 未完成段(#F2F2F2 40% -> #717389)
scatter: 蓝珠(2022, x=C) + 灰珠(#A6A6A6, 2021, x=D), 均 circle size10 + 白描边, 无连线
值轴 0-1.2 隐藏; 条端为直角(非胶囊); 无数据标签
文字(userShapes): 标题 18pt 加粗 / 副标题 11pt / 注释 8pt #D9D9D9 / 自绘图例(蓝点+灰点+8pt 文字)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Ellipse

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'; BLUE = '#0070C0'; GRAY = '#717389'; GRAY2 = '#A6A6A6'
TXT = '#FFFFFF'; LABEL = '#F2F2F2'
W, H = 438.9, 299.1

regions = ['华东', '西北', '东北', '华北', '华南']
p22 = [0.35, 0.51, 0.62, 0.74, 0.86]
p21 = [0.45, 0.39, 0.53, 0.69, 0.92]
y = np.arange(5)

fig = plt.figure(figsize=(W / 72, H / 72), facecolor=BG)
ax = fig.add_axes([0.14914, 0.10639, 0.77488, 0.62248], facecolor='none')

BH = 1 / 6.0
for yy, a, b in zip(y, p22, p21):
    ax.add_patch(Rectangle((0, yy - BH/2), a, BH, facecolor=BLUE, linewidth=0, zorder=2))
    ax.add_patch(Rectangle((a, yy - BH/2), 1 - a, BH, facecolor=GRAY, linewidth=0, zorder=1))
ax.scatter(p21, y - 0.012, s=108, c=GRAY2, edgecolors='#FFFFFF', linewidths=1.0, zorder=3)
ax.scatter(p22, y - 0.012, s=108, c=BLUE, edgecolors='#FFFFFF', linewidths=1.0, zorder=4)
# 蓝色滑珠(2022)上方标注完成率百分比
for p, yy in zip(p22, y):
    ax.text(p, yy + 0.115, f'{int(round(p * 100))}%', ha='center', va='bottom',
            color=TXT, fontsize=8.2, zorder=6)

ax.set_xlim(0, 1.2); ax.set_ylim(-0.5, 4.5)
ax.set_xticks([])
ax.set_yticks([])
for yy, nm in zip(y, regions):
    ax.text(-0.0277, yy + 0.016, nm, ha='right', va='center', fontsize=9,
            color=TXT, clip_on=False)
for s in ax.spines.values(): s.set_visible(False)

# 自绘图例: 蓝点/灰点 + 文字
fig.add_artist(Ellipse((0.0946, 1 - 0.2617), 0.0229, 0.0321, transform=fig.transFigure,
                       facecolor=BLUE, edgecolor='#F2F2F2', lw=0.9, zorder=5))
fig.text(0.1235, 1 - 0.2617, '2022完成率', ha='left', va='center', color=LABEL, fontsize=8)
fig.add_artist(Ellipse((0.2498, 1 - 0.2624), 0.0229, 0.0321, transform=fig.transFigure,
                       facecolor=GRAY2, edgecolor='#F2F2F2', lw=0.9, zorder=5))
fig.text(0.2645, 1 - 0.2624, '2021完率', ha='left', va='center', color=LABEL, fontsize=8)

fig.text(0.0700, 1 - 0.0722, '2022年上半年销量目标达成率同比去年情况',
         ha='left', va='top', color=TXT, fontsize=18.1, fontweight='bold')
fig.text(0.0700, 1 - 0.1653, '华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年',
         ha='left', va='top', color=TXT, fontsize=11)
fig.text(0.0788, 1 - 0.9431, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='center', color='#D9D9D9', fontsize=8)

plt.savefig('30 对比滑珠图.png', dpi=243, facecolor=BG)
print('已生成 30 对比滑珠图.png')