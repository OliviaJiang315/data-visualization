# -*- coding: utf-8 -*-
"""22 仪表盘图 (依据 第二章 图表(后15).xlsx chart7.xml 精确复刻)

由 combo 图表构成:
- doughnutChart: 同心三层环 (holeSize=70, firstSliceAng=225)
    内环深蓝(1A1E43) 0.70-0.85R / 中环彩色刻度 0.85-0.94R / 外环蓝(0070C0) 0.94-1.0R
    270°弧(开口朝下): 红-45~36, 黄36~144, 青绿144~225 (各27°分段), 底部深蓝
- pieChart: 系列"大小" 70.2/0/289.8, 指针=0度扇区描边(浅灰白), 指向值76(155°)
刻度 50-150, 当前值 76, 深蓝背景 #1A1E43
数据来自拟合 chart22_clip 真实几何: 圆心(0.517,0.617), R=0.2264*W
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
GREEN = '#087E8B'
YELLOW = '#FFC54D'
RED = '#F94C66'
BLUE = '#0070C0'
POINTER = '#E6E6E6'

W, Ht = 438.86, 320.57
cx = W * 0.5172
cy = Ht * (1 - 0.6174)      # 转 y 向上
R = W * 0.2264              # 蓝外环外径

fig = plt.figure(figsize=(10, 10*Ht/W), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, Ht)
ax.axis('off')

def ring(r_outer, width, a1, a2, color, z=2):
    ax.add_patch(Wedge((cx, cy), r_outer, a1, a2, width=width,
                       facecolor=color, edgecolor='none', zorder=z))

# 半径 (拟合): 外蓝 0.94-1.0, 彩 0.85-0.94, 内深蓝 0.70-0.85
r_blue_out = R;      w_blue = 0.06 * R
r_col_out  = 0.94*R; w_col  = 0.09 * R
r_in_out   = 0.85*R; w_in   = 0.15 * R

# 仪表盘 270° 弧(mpl逆时针), 底部开口
ring(r_blue_out, w_blue, -45, 315, BLUE, z=2)        # 外环 蓝 360
ring(r_in_out, w_in, -45, 315, '#1A1E43', z=2)       # 内环 深蓝 360
ring(r_col_out, w_col, -45, 36, RED, z=3)            # 中环 红
ring(r_col_out, w_col, 36, 144, YELLOW, z=3)         # 中环 黄
ring(r_col_out, w_col, 144, 225, GREEN, z=3)         # 中环 青绿
ring(r_col_out, w_col, 225, 315, '#1A1E43', z=3)     # 中环 底部深蓝

# 中环 27° 刻度分隔线(深蓝)
r_col_in = r_col_out - w_col
for a in range(-45, 226, 27):
    rad = np.radians(a)
    x1, y1 = cx + r_col_in*np.cos(rad), cy + r_col_in*np.sin(rad)
    x2, y2 = cx + r_col_out*np.cos(rad), cy + r_col_out*np.sin(rad)
    ax.plot([x1, x2], [y1, y2], color='#1A1E43', lw=1.0, zorder=4)

# 指针: 圆心沿 154.8°(值76) 到外径, 浅灰白
ang = 154.8
rad = np.radians(ang)
ax.plot([cx, cx + r_blue_out*0.81*np.cos(rad)], [cy, cy + r_blue_out*0.81*np.sin(rad)],
        color=POINTER, lw=1.2, zorder=10, solid_capstyle='round')

# 刻度数字 50-150 (贴彩环内侧, 水平正向显示)
for i, val in enumerate(range(50, 151, 10)):
    a = 225 - 27*i
    r_ = np.radians(a)
    rr = 0.76 * R
    x = cx + rr*np.cos(r_); y = cy + rr*np.sin(r_)
    ax.text(x, y, str(val), ha='center', va='center', color=POINTER, fontsize=13)

# 中心数值 76 —— 在圆心下方(底部开口区中央, 约0.55R), 非圆心
ax.text(cx, cy - 0.55*R, '76', ha='center', va='center', color='white',
        fontsize=30, fontweight='bold')

# 顶部标题
ax.text(W/2, Ht*0.876, '2022年6月29公司整体运营指数良好', ha='center', va='top',
        color='white', fontsize=30, fontweight='bold')

plt.savefig('22 仪表盘图.png', dpi=150, facecolor=BG)
print('已生成 22 仪表盘图.png')
print(f'center=({cx:.1f},{cy:.1f}) R={R:.1f}')