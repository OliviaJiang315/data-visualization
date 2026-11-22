# -*- coding: utf-8 -*-
"""20 南丁格尔圆环图 (依据 第二章 图表(后15).xlsx chart5.xml + drawing10.xml 精确复刻)

doughnutChart: 5环, holeSize=60%, 从内到外可见扇区递减(4→4→3→2→1)形成螺旋.
4扇区从12点顺时针. 椭圆环(随plotArea拉伸). 有引出线+数据标签+标题/副标题/注释.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TXT = '#F2F2F2'
TXT_DIM = '#D9D9D9'

# 扇区数据 (从12点顺时针)
categories = ['[20,30)', '[30,40)', '[40,50)', '>=50']
values = [0.375, 0.29166666666666669, 0.20833333333333334, 0.125]
colors = ['#512DCB', '#6073F3', '#66CBDD', '#F5C353']
pct_text = ['37.5%', '29.2%', '20.8%', '12.5%']

# 5环可见性 (True=可见, 从内到外)
ring_visible = [
    [True, True, True, True],   # Ring 0 (最内)
    [True, True, True, True],   # Ring 1
    [True, True, True, False],  # Ring 2
    [True, True, False, False], # Ring 3
    [True, False, False, False],# Ring 4 (最外, 有数据标签)
]

# 引出线 (dot_pt=圆环边缘圆点, diag_end=斜线终点/水平线起点, hline_end=水平线终点/标签端)
# figure坐标, Excel y从上往下. 从 drawing10.xml 完整变换链计算:
# cxnSp flip/rot -> group transform(chOff/chExt->off/ext) -> group rot180 -> chart fraction
leaders = [
    ((0.73322, 0.41601), (0.77141, 0.35495), (0.92131, 0.35373), '#512DCB', 0),  # [20,30) 右
    ((0.63707, 0.85319), (0.66843, 0.91710), (0.83151, 0.91710), '#6073F3', 1),  # [30,40) 右下
    ((0.29489, 0.54587), (0.26009, 0.60937), (0.09341, 0.60815), '#66CBDD', 2),  # [40,50) 左
    ((0.38372, 0.36228), (0.35501, 0.30366), (0.19597, 0.30407), '#F5C353', 3),  # >=50 左上
]

# 字号: 原图1027px/168dpi, 生成图1500px/150dpi → ×1.461
FS_TITLE = 29       # 18pt
FS_SUBTITLE = 20    # 12pt
FS_NOTE = 13        # 8pt
FS_LABEL = 14       # 9pt (区间标签)
FS_PCT = 14         # 9pt (百分比, 同字号但加粗)

# 图框比例 1027:735 = 1.397
fig = plt.figure(figsize=(10, 7.161), facecolor=BG)

# plotArea: x=0.28232, y=0.31258, w=0.43308, h=0.57743 (Excel坐标, y从上)
ax = fig.add_axes([0.28232220972378458, 1 - 0.31257832353285042 - 0.5774333878222413,
                    0.43307509638218294, 0.5774333878222413], facecolor=BG)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis('off')

# 画5环doughnut: holeSize=60%, 每环厚度=0.08, 加微小间隙增强阶梯感
n_rings = 5
r_min = 0.6
ring_gap = 0.001
ring_thickness = (1.0 - r_min) / n_rings - ring_gap  # 0.077

cum_angles = []
cum = 0
for v in values:
    cum_angles.append(cum)
    cum += v
cum_angles.append(cum)

for ring_idx in range(n_rings):
    r_inner = r_min + ring_idx * (ring_thickness + ring_gap)
    r_outer = r_inner + ring_thickness
    for seg_idx in range(4):
        if not ring_visible[ring_idx][seg_idx]:
            continue
        a_start = cum_angles[seg_idx] * 360.0
        a_end = cum_angles[seg_idx + 1] * 360.0
        theta2 = 90.0 - a_start
        theta1 = 90.0 - a_end
        ax.add_patch(mpatches.Wedge((0, 0), r_outer, theta1, theta2,
                                    width=ring_thickness,
                                    facecolor=colors[seg_idx],
                                    edgecolor='none', zorder=3))

# 画引出线(圆点→斜线→水平线) — 精确端点从 drawing10.xml 变换链计算
for (dx, dy), (bx, by), (lx, ly), color, idx in leaders:
    # 斜线: 圆点 → 折点
    line1 = mlines.Line2D([dx, bx], [1 - dy, 1 - by], color=color,
                          linewidth=0.6, transform=fig.transFigure, zorder=5)
    fig.lines.append(line1)
    # 水平线: 折点 → 标签端
    line2 = mlines.Line2D([bx, lx], [1 - by, 1 - ly], color=color,
                          linewidth=0.6, transform=fig.transFigure, zorder=5)
    fig.lines.append(line2)
    # 端点圆点
    dot = mpatches.Circle((dx, 1 - dy), 0.002, facecolor=color,
                          edgecolor='none', transform=fig.transFigure, zorder=6)
    fig.patches.append(dot)

# 数据标签 (位置从原图像素精确校准: 1027x735)
# (x, ha, cat_y_excel, pct_y_excel) — figure坐标, Excel y从上
label_text_pos = [
    (0.801, 'left',  0.302, 0.335),  # [20,30) 右
    (0.733, 'left',  0.853, 0.884),  # [30,40) 右下
    (0.217, 'right', 0.546, 0.574),  # [40,50) 左
    (0.315, 'right', 0.272, 0.305),  # >=50 左上
]

for i, (tx, ha, cat_y, pct_y) in enumerate(label_text_pos):
    color = colors[i]
    # 区间标签 (白色, 不加粗)
    fig.text(tx, 1 - cat_y, categories[i],
             fontsize=FS_LABEL, color=TXT, ha=ha, va='center',
             family='Microsoft YaHei')
    # 百分比 (扇区色+加粗)
    fig.text(tx, 1 - pct_y, pct_text[i],
             fontsize=FS_PCT, color=color, ha=ha, va='center',
             fontweight='bold', family='Microsoft YaHei')

# 标题
fig.text(0.064, 0.951, '2022年上半年各年龄段人数分布',
         fontsize=FS_TITLE, fontweight='bold', color=TXT,
         ha='left', va='top', family='Microsoft YaHei')
# 副标题 (增大与标题间距)
fig.text(0.063, 0.864, '公司平均年龄32.5，20-30员工比例最高占比37.5%',
         fontsize=FS_SUBTITLE, color=TXT,
         ha='left', va='top', family='Microsoft YaHei')

# 注释
fig.text(0.062, 0.064, '*注：数据来源于公司人力资源系统，统计日期至2022.06.30',
         fontsize=FS_NOTE, color=TXT_DIM,
         ha='left', va='top', family='Microsoft YaHei')

plt.savefig('20 南丁格尔圆环图.png', dpi=150, facecolor=BG)
print("已生成 20 南丁格尔圆环图.png")
