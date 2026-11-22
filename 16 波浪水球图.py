# -*- coding: utf-8 -*-
"""16 波浪水球图 (依据 第二章 图表(后15).xlsx chart1.xml + drawing2.xml 精确复刻)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.path import Path

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

# 液面 y 坐标: 圆中间偏上一点
water_top = 0.15

# 1. 蓝色液体填充 (波浪液面 - doubleWave 双波形)
n_pts = 300
x_wave = np.linspace(-r, r, n_pts)
wave_amp = 0.04
y_top = water_top + wave_amp * np.sin(x_wave * 2.5 * np.pi)

# 构建液体多边形
x_fill = np.concatenate([x_wave, [r, -r]])
y_fill = np.concatenate([y_top, [-r, -r]])
liquid = plt.Polygon(np.column_stack([x_fill, y_fill]), facecolor=BLUE,
                     edgecolor='none', zorder=2)
ax.add_patch(liquid)

# 用圆形 clip 限制液体在圆内
clip_path = Path.circle(center=(0, 0), radius=r)
clip_patch = mpatches.PathPatch(clip_path, transform=ax.transData)
liquid.set_clip_path(clip_patch)

# 2. 圆形容器边框 (只画液面以下的弧, 对齐波浪边缘)
y_left = water_top + wave_amp * np.sin(-r * 2.5 * np.pi)
y_right = water_top + wave_amp * np.sin(r * 2.5 * np.pi)
angle_left = 180 - np.degrees(np.arcsin(y_left / r))
angle_right = np.degrees(np.arcsin(y_right / r))
ax.add_patch(mpatches.Arc((0, 0), 2*r, 2*r, angle=0,
             theta1=angle_left, theta2=360 + angle_right,
             edgecolor=BLUE, linewidth=1.5, zorder=5))

# 2b. 外圈蓝色边框
ax.add_patch(mpatches.Circle((0, 0), r + 0.10, facecolor='none', edgecolor=BLUE,
             linewidth=1.5, zorder=5))

# 3. 中心 "65%"
ax.text(0, 0, '65%', ha='center', va='center', color='white',
        fontsize=50, zorder=6)

# 标题 / 副标题 / 注释
label_x = 0.05
fig.text(label_x, 0.88, '本科及以上学历员占比', fontsize=33, fontweight='bold',
         color='white', ha='left')
fig.text(label_x, 0.82, '6月30日最新统计数据本科及以上员工占比65%',
         fontsize=21, color='white', ha='left')
fig.text(label_x, 0.04, '*注：数据来源于公司人力资源系统',
         fontsize=13, color='white', ha='left')

plt.savefig('16 波浪水球图.png', dpi=150, facecolor=BG)
print("已生成 16 波浪水球图.png")
