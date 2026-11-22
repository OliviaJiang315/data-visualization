# -*- coding: utf-8 -*-
"""17 玉玦图 (依据 第二章 图表(后15).xlsx chart2.xml + drawing4.xml + 原图像素测量精确复刻)

doughnutChart: 4 同心圆环 (holeSize=35%). Excel 第一个系列=最内环.
扇区角度 = 值/系列总和*360. 每系列 占比+占位=0.5 => 占比角度 = pct*720.
firstSliceAng=0 => 顶部 12 点顺时针. 占位段 noFill + 1A1E43 1.5pt 边框 = 缺口轮廓.
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
    ('>=50',    0.125,      '#37A2DA'),   # 系列0 最内环, 占比90°
    ('[40,50)', 0.20833333, '#11A7AD'),   # 系列1, 占比150°
    ('[30,40)', 0.29166667, '#F5C353'),   # 系列2, 占比210°
    ('[20,30)', 0.375,      '#E74E69'),   # 系列3 最外环, 占比270°
]

# 数据标签精确位置 (图框归一化, 左下原点; 原图像素测量)
label_pos = {
    '>=50':    (0.588, 0.393),
    '[40,50)': (0.531, 0.252),
    '[30,40)': (0.404, 0.252),
    '[20,30)': (0.314, 0.458),
}

# 图框比例 438.857:298.446 = 1.47
fig = plt.figure(figsize=(10, 6.8), facecolor=BG)

# 圆环区 plotArea: x=0.28560 y=0.27528 w=0.43861 h=0.61417
ax = fig.add_axes([0.28560, 1 - 0.27528 - 0.61417, 0.43861, 0.61417], facecolor=BG)
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.set_aspect('equal')
ax.axis('off')

r_outer = 1.0
r_inner = 0.35
ring_width = (r_outer - r_inner) / 4
start_angle = 90.0
edge_lw = 1.5

for i, (label, pct, color) in enumerate(layers):
    r_in = r_inner + i * ring_width      # i=0 最内
    r_out = r_in + ring_width
    ratio_angle = pct * 720.0            # 占比段角度 (pct/0.5*360)
    a1 = start_angle                     # 占比段起点 (12点)
    a2 = start_angle - ratio_angle       # 占比段终点 / 占位段起点
    a3 = start_angle - 360.0             # 占位段终点 (回到12点)
    # 占比段 (彩色填充)
    ax.add_patch(mpatches.Wedge((0, 0), r_out, a2, a1, width=ring_width,
                                facecolor=color, edgecolor=BG, linewidth=edge_lw, zorder=3))
    # 占位段 (透明, 仅边框 = 缺口轮廓)
    ax.add_patch(mpatches.Wedge((0, 0), r_out, a3, a2, width=ring_width,
                                facecolor='none', edgecolor=BG, linewidth=edge_lw, zorder=3))

# 数据标签 (精确位置, 9pt)
for label, pct, _ in layers:
    x, y = label_pos[label]
    fig.text(x, y, f'{pct*100:.1f}%', fontsize=9, color=TXT,
             ha='center', va='center', family='Microsoft YaHei', zorder=5)

# 标题 / 副标题 (20pt bold / 14pt; 原图像素 y=0.897/0.812)
fig.text(0.069, 0.897, '2022年上半年龄分布', fontsize=26, fontweight='bold',
         color=TXT_TITLE, ha='left', va='center', family='Microsoft YaHei')
fig.text(0.069, 0.812, '公司平均年龄32.5，23-30员工比例最高',
         fontsize=18, color=TXT_TITLE, ha='left', va='center', family='Microsoft YaHei')

# 图例 (原图像素: x=0.422, y 0.701/0.650/0.600/0.553; 11pt; 顺序 [20,30)→>=50)
legend_x = 0.422
legend_y = [0.701, 0.650, 0.600, 0.553]
for j, (label, *_) in enumerate(reversed(layers)):
    fig.text(legend_x, legend_y[j], label, fontsize=11, color=TXT,
             ha='left', va='center', family='Microsoft YaHei')

# 注释 (原图像素 y=0.054; 8pt)
fig.text(0.062, 0.054, '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30',
         fontsize=8, color=TXT_DIM, ha='left', va='center', family='Microsoft YaHei')

plt.savefig('17 玉玦图.png', dpi=150, facecolor=BG)
print("已生成 17 玉玦图.png")
