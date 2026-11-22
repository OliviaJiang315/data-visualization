# -*- coding: utf-8 -*-
"""14 单值圆环图 (依据 Excel chart13.xml 精确复刻)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
PURPLE = '#7030A0'
PINK = '#E74E69'

fig = plt.figure(figsize=(12, 7.5), facecolor=BG)

# 圆环区域 (居中偏下)
ax = fig.add_axes([0.28, 0.18, 0.44, 0.58], facecolor=BG)
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')


def lerp_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f'#{r:02X}{g:02X}{b:02X}'


# 圆环参数
r_outer = 1.0
r_inner = 0.90  # holeSize=90%
pct = 0.85

# 起始角度: Excel firstSliceAng=300 (顺时针, 0=顶部)
# 转换到 matplotlib (0=右侧, 逆时针): 90 - 300 = -210 = 150度
start_angle = 150

# 85% 弧: 渐变填充 (底部紫色 -> 顶部粉红), 顺时针绘制
arc_85 = pct * 360  # 306度
n_seg = 100
for i in range(n_seg):
    a1 = start_angle - (i / n_seg) * arc_85
    a2 = start_angle - ((i + 1) / n_seg) * arc_85
    a_center = (a1 + a2) / 2
    # 渐变: 底部(紫)到顶部(粉红), 基于 Y 坐标 (ang=90度, 从下到上)
    y = np.sin(np.radians(a_center))
    t = (y + 1) / 2
    color = lerp_color(PINK, PURPLE, t)
    w = mpatches.Wedge((0, 0), r_outer, a2, a1, width=r_outer - r_inner,
                       facecolor=color, edgecolor='none', zorder=2)
    ax.add_patch(w)

# 15% 弧: 淡白色 (alpha=10%)
arc_15 = (1 - pct) * 360  # 54度
a1 = start_angle - arc_85
a2 = a1 - arc_15
w = mpatches.Wedge((0, 0), r_outer, a2, a1, width=r_outer - r_inner,
                   facecolor=(1, 1, 1, 0.10), edgecolor='none', zorder=2)
ax.add_patch(w)

# 圆环中心 "85%"
ax.text(0, 0.05, '85%', ha='center', va='center', color='white',
        fontsize=44, fontweight='bold', zorder=3)
# 圆环下方 "目标完成率"
ax.text(0, -0.28, '目标完成率', ha='center', va='center',
        color='#AAAAAA', fontsize=15, zorder=3)

# 标题 / 副标题 / 注释
label_x = 0.05
fig.text(label_x, 0.88, '2022年上半年目标完成率', fontsize=29, fontweight='bold',
         color='white', ha='left')
fig.text(label_x, 0.82, '截至6月30日销售目标总体完成率达到85%',
         fontsize=18, color='white', ha='left')
fig.text(label_x, 0.04, '*注：数据来源于公司销售系统',
         fontsize=13, color='white', ha='left')

plt.savefig('14 单值圆环图.png', dpi=150, facecolor=BG)
print("已生成 14 单值圆环图.png")
