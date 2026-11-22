# -*- coding: utf-8 -*-
"""15 水球图 (依据 Excel chart14.xml + drawing29.xml 精确复刻)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'

fig = plt.figure(figsize=(12, 7.5), facecolor=BG)

# 水球区域 (居中)
ax = fig.add_axes([0.30, 0.15, 0.40, 0.60], facecolor=BG)
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')
ax.axis('off')

pct = 0.65
r = 1.0  # 圆半径

# 1. 蓝色液体填充 (底部 65%), 用 clip 限制在圆内
# 液面 y 坐标: 从 -1 到 1, 65% 高度
water_top = -r + 2 * r * pct  # -1 + 1.3 = 0.3

# 创建圆形 clip path
circle = mpatches.Circle((0, 0), r, transform=ax.transData)
ax.add_patch(mpatches.Circle((0, 0), r, facecolor='none', edgecolor=BLUE,
             linewidth=1.5, zorder=5))

# 液体填充 (直线液面)
x_fill = np.array([-r, r, r, -r])
y_fill = np.array([water_top, water_top, -r, -r])
liquid = plt.Polygon(np.column_stack([x_fill, y_fill]), facecolor=BLUE,
                     edgecolor='none', zorder=2)
ax.add_patch(liquid)

# 用圆形 clip
from matplotlib.path import Path
clip_path = Path.circle(center=(0, 0), radius=r)
clip_patch = mpatches.PathPatch(clip_path, transform=ax.transData)
liquid.set_clip_path(clip_patch)

# 2. 圆形容器边框 (再画一次确保在顶层)
ax.add_patch(mpatches.Circle((0, 0), r, facecolor='none', edgecolor=BLUE,
             linewidth=1.5, zorder=5))

# 2b. 外圈蓝色边框
ax.add_patch(mpatches.Circle((0, 0), r + 0.06, facecolor='none', edgecolor=BLUE,
             linewidth=1.5, zorder=5))

# 3. 中心 "65%"
ax.text(0, 0, '65%', ha='center', va='center', color='white',
        fontsize=50, fontweight='bold', zorder=6)

# 标题 / 副标题 / 注释
label_x = 0.05
fig.text(label_x, 0.88, '2022年上半年目标完成率', fontsize=33, fontweight='bold',
         color='white', ha='left')
fig.text(label_x, 0.82, '截至6月30日销售目标总体完成率达到65%',
         fontsize=21, color='white', ha='left')
fig.text(label_x, 0.04, '*注：数据来源于公司销售系统',
         fontsize=13, color='white', ha='left')

plt.savefig('15 水球图.png', dpi=150, facecolor=BG)
print("已生成 15 水球图.png")
