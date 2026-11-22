# -*- coding: utf-8 -*-
"""18 跑道图 (依据 第二章 图表(后15).xlsx chart3.xml + drawing6.xml + 原图像素测量精确复刻)

doughnutChart: 6 同心圆环 (跑道, holeSize=45%). Excel 第一个系列=最内环.
每系列 人数+占位=832, 扇区角度=值/832*360. firstSliceAng=0 顶部顺时针.
人数段填色, 占位段透明, 均带 1A1E43 3pt 边框.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TXT = '#F2F2F2'
TXT_TITLE = '#FFFFFF'
TXT_DIM = '#D9D9D9'

# 从内到外 (Excel 系列顺序)
layers = [
    ('人力部', 130, '#7030A0'),
    ('行政部', 226, '#0070C0'),
    ('财务部', 238, '#37A2DA'),
    ('工程部', 293, '#11A7AD'),
    ('采购部', 326, '#F5C353'),
    ('销售部', 451, '#E74E69'),
]
SERIES_TOTAL = 832          # 人数+占位
n = len(layers)

# 图框比例 438.857:313.714 = 1.399
fig = plt.figure(figsize=(10, 7.15), facecolor=BG)

# 圆环区 plotArea: x=0.20435 y=0.24570 w=0.49081 h=0.65602
# Excel plotArea 非正方形, 圆环被拉伸为椭圆. 不用 aspect='equal'.
# 根据原图像素测量调整: center=(0.4524, 0.4307), R_x=0.2273, R_y=0.3217
ax = fig.add_axes([0.2138, 0.0930, 0.4773, 0.6755], facecolor=BG)
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.axis('off')

r_outer = 1.0
r_inner = 0.45
ring_width = (r_outer - r_inner) / n
start_angle = 90.0
edge_lw = 3.0      # 38100 EMU = 3pt

for i, (label, val, color) in enumerate(layers):
    r_in = r_inner + i * ring_width      # i=0 最内
    r_out = r_in + ring_width
    ratio_angle = val / SERIES_TOTAL * 360.0
    a1 = start_angle
    a2 = start_angle - ratio_angle
    a3 = start_angle - 360.0
    # 人数段 (彩色填充)
    ax.add_patch(mpatches.Wedge((0, 0), r_out, a2, a1, width=ring_width,
                                facecolor=color, edgecolor=BG, linewidth=edge_lw, zorder=3))
    # 占位段 (透明, 仅边框)
    ax.add_patch(mpatches.Wedge((0, 0), r_out, a3, a2, width=ring_width,
                                facecolor='none', edgecolor=BG, linewidth=edge_lw, zorder=3))

# 中心标签 (6行; 字号放大匹配原图视觉; x中心0.396, y从上到下)
center_x = 0.396
center_y = [0.739, 0.710, 0.682, 0.653, 0.624, 0.596]   # 销售部→人力部
for j, (label, val, _) in enumerate(reversed(layers)):
    fig.text(center_x, center_y[j], f'{label} {val}', fontsize=12, color=TXT,
             ha='center', va='center', family='Microsoft YaHei')

# 标题 / 副标题 (字号放大匹配原图视觉; y=0.896/0.814)
fig.text(0.067, 0.896, '2022年上半年各部门人数', fontsize=33, fontweight='bold',
         color=TXT_TITLE, ha='left', va='center', family='Microsoft YaHei')
fig.text(0.066, 0.814, '公司总人数1664，销售部人数最多451，占比27%',
         fontsize=23, color=TXT_TITLE, ha='left', va='center', family='Microsoft YaHei')

# 注释 (字号放大; y=0.055)
fig.text(0.047, 0.055, '*注：数据来源于公司人力资源系统，统计日期截止2022.06.30',
         fontsize=13, color=TXT_DIM, ha='left', va='center', family='Microsoft YaHei')

plt.savefig('18 跑道图.png', dpi=150, facecolor=BG)
print("已生成 18 跑道图.png")
