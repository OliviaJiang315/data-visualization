# -*- coding: utf-8 -*-
"""26 柱形圆 (依据 chart13.xml 复刻主图 Chart6)

组合图: barChart 销量(红 E74E69,柱顶白数值2354..) + lineChart 全4500(蓝 0070C0, marker=circle)
圆圈处白色百分比(12%等, 来自E列); 值轴0-5000(隐藏刻度?); 横轴6区域; 标题/副标题/注释; 无图例; 背景#1A1E43
几何来自 _chart26_obj1.png(2.08x, Chart 438.5x298.4) 实测
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
RED = '#E74E69'
BLUE = '#0070C0'
TXT = '#F2F2F2'

W, H = 438.5, 298.4
x = np.arange(6)
sales = [2354, 1902, 3524, 2698, 2896, 2563]
pct = [0.12, 0.25, 0.16, 0.21, 0.18, 0.25]
regions = ['华北', '华南', '东北', '西北', '西南', '华东']

fig = plt.figure(figsize=(10, 10 * H / W), facecolor=BG)
ax = fig.add_axes([0.0816, 0.155, 0.8255, 0.595], facecolor='none')

# 柱(销量) 红
ax.bar(x, sales, width=0.32, color=RED, zorder=2)
# 折线系列 noFill: 只 6 个蓝圆圈 marker; 圆大小 ∝ 百分比(气泡)
for i in range(6):
    ms = 2.0 * (pct[i] * 100) - 3    # 直径(pt) 按百分比线性(适度; 12%→~21pt, 25%→~47pt)
    ax.plot(i, 4500, marker='o', markersize=ms, color=BLUE, zorder=4)
# X 轴轴线(基线 y=0): 实测原图为灰蓝 #454866 横线, 柱间/柱外均可见、横穿全宽
for s in ax.spines.values(): s.set_visible(False)
ax.axhline(0, color='#454866', lw=2.5, zorder=1, clip_on=False)

ax.set_xlim(-0.5, 5.5); ax.set_ylim(0, 5000)
ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(axis='x', length=0)

# 柱顶数值标签(白)
for i, v in enumerate(sales):
    ax.text(i, v + 130, str(v), ha='center', va='bottom', color=TXT, fontsize=11, zorder=5)
# 圆圈处百分比标签(白, 居中压在蓝圆圈上, 与原图一致)
for i, p in enumerate(pct):
    ax.text(i, 4500, f'{p*100:.0f}%', ha='center', va='center', color=TXT, fontsize=11, zorder=5)

# 横轴区域名(fig 精确 y=0.129)
for i, cat in enumerate(regions):
    cx_fig = 0.0816 + (i+0.5)/6*0.8255
    fig.text(cx_fig, 0.118, cat, ha='center', va='center', color=TXT, fontsize=13)

# 标题/副标题(左上)
fig.text(0.063, 0.940, '各区域上半年销量及同比', ha='left', va='top',
         color=TXT, fontsize=30, fontweight='bold')
fig.text(0.062, 0.847, '东北区域销量持续保持第一，华东和华南同比去年增长最多', ha='left', va='top',
         color=TXT, fontsize=18)

# 注释(左下)
fig.text(0.061, 0.049, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', ha='left', va='center',
         color='#C8C8C8', fontsize=13)

plt.savefig('26 柱形圆.png', dpi=150, facecolor=BG)
print('已生成 26 柱形圆.png')