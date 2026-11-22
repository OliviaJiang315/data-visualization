# -*- coding: utf-8 -*-
"""19 南丁格尔圆饼图 (依据 第二章 图表(后15).xlsx chart4.xml + drawing8.xml 精确复刻)

pieChart: 6 扇区普通饼图, 从12点顺时针. 正圆饼图(axes box英寸正方形).
有引出线(userShapes连接线) + 标题/副标题/注释文本框. 无数据标签文字.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import math

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TXT = '#FFFFFF'
TXT_DIM = '#D9D9D9'

# 数据 (从12点顺时针)
data = [
    ('销售部', 0.292, '#E74E69'),
    ('采购部', 0.227, '#F5C353'),
    ('工程部', 0.175, '#11A7AD'),
    ('财务部', 0.136, '#0070C0'),
    ('行政部', 0.103, '#37A2DA'),
    ('人力部', 0.067, '#7030A0'),
]

# 引出线折点和标签端 (从 drawing8.xml 变换链精确计算)
# figure坐标, Excel y从上往下. 格式: (bend_pt, label_pt, color)
leader_pts = [
    ((0.78497, 0.34358), (0.92927, 0.34235), '#E74E69'),   # 销售部
    ((0.71717, 0.84919), (0.86055, 0.84919), '#FAB250'),    # 采购部
    ((0.30379, 0.86083), (0.16041, 0.86206), '#11A7AD'),    # 工程部
    ((0.27819, 0.63320), (0.13572, 0.63197), '#0070C0'),    # 财务部
    ((0.37982, 0.40488), (0.18956, 0.40488), '#37A2DA'),   # 行政部
    ((0.44757, 0.35416), (0.30418, 0.35416), '#7030A0'),   # 人力部
]

# 字号缩放: 原图168dpi/1024px, 生成图150dpi/1500px → ×1.641
FS_TITLE = 30       # 18pt
FS_SUBTITLE = 20    # 12pt
FS_NOTE = 14        # 8pt → 14 (匹配原图2.73%高度)

# 图框比例 1024:732 = 1.398
fig = plt.figure(figsize=(10, 7.15), facecolor=BG)

# 饼图区: 正圆 → axes box 在英寸上为正方形
# 原axes [0.252, 0.094, 0.490, 0.632] → 4.90in × 4.52in, 取较小尺寸做正方形
_pie_cx = 0.252 + 0.490 / 2   # 0.497 (figure x)
_pie_cy = 0.094 + 0.632 / 2   # 0.410 (figure y)
_pie_h_in = 0.632 * 7.15      # 4.52in
_pie_w_frac = _pie_h_in / 10  # 0.452 (figure x fraction)
ax = fig.add_axes([_pie_cx - _pie_w_frac / 2, 0.094, _pie_w_frac, 0.632], facecolor=BG)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')

# 画饼图: 从12点(90°)顺时针
cum = 0
for name, val, color in data:
    angle = val * 360.0
    a1 = 90.0 - cum * 360.0
    a2 = a1 - angle
    ax.add_patch(mpatches.Wedge((0, 0), 1.0, a2, a1, facecolor=color,
                                edgecolor='none', zorder=3))
    cum += val

# 画引出线(圆点→斜线→水平线)
# 圆点在正圆边缘, 按各扇区中点角度计算; 折点x随圆点x同步偏移(保持斜线角度), 标签端不变
_pie_rx = _pie_w_frac / 2   # figure x 半径(正圆)
_pie_ry = 0.632 / 2          # figure y 半径
_pie_rx_old = 0.490 / 2      # 原椭圆 x 半径
cum = 0
for (name, val, color), ((bx, by), (lx, ly), _) in zip(data, leader_pts):
    mid_deg = 90.0 - (cum + val / 2) * 360.0
    mid_rad = math.radians(mid_deg)
    dx = _pie_cx + math.cos(mid_rad) * _pie_rx
    dy = _pie_cy + math.sin(mid_rad) * _pie_ry  # matplotlib y (from bottom)
    # 折点x偏移: 圆点x从椭圆→正圆的位移, 同步应用到折点(保持斜线角度)
    bx_adj = bx + math.cos(mid_rad) * (_pie_rx - _pie_rx_old)
    # 斜线: 圆点 → 折点
    line1 = mlines.Line2D([dx, bx_adj], [dy, 1 - by], color=color,
                          linewidth=0.6, transform=fig.transFigure, zorder=5)
    fig.lines.append(line1)
    # 水平线: 折点 → 标签端
    line2 = mlines.Line2D([bx_adj, lx], [1 - by, 1 - ly], color=color,
                          linewidth=0.6, transform=fig.transFigure, zorder=5)
    fig.lines.append(line2)
    # 端点圆点
    dot = mpatches.Circle((dx, dy), 0.005, facecolor=color,
                          edgecolor='none', transform=fig.transFigure, zorder=6)
    fig.patches.append(dot)
    cum += val

# 标题 (原图y_frac=0.052, figure y=0.948)
fig.text(0.045, 0.948, '2021年各部门人数分布', fontsize=FS_TITLE,
         fontweight='bold', color=TXT, ha='left', va='top', family='Microsoft YaHei')
# 副标题 (原图y_frac=0.141, figure y=0.859)
fig.text(0.045, 0.859, '公司总人数1664，销售部人数最多451，占比29.2%',
         fontsize=FS_SUBTITLE, color=TXT, ha='left', va='top', family='Microsoft YaHei')

# 注释 (原图y_frac=0.934, figure y=0.066)
fig.text(0.046, 0.066, '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01',
         fontsize=FS_NOTE, color=TXT_DIM, ha='left', va='top', family='Microsoft YaHei')

plt.savefig('19 南丁格尔圆饼图.png', dpi=150, facecolor=BG)
print("已生成 19 南丁格尔圆饼图.png")
