# -*- coding: utf-8 -*-
"""29 滑珠图 (依据 chart16.xml + drawing28.xml + _chart29_obj1.png 实测复刻)

barChart(barDir=bar, stacked, gapWidth=150): 完成率蓝#0070C0 + 未完成灰(#F3F3F3 40% over BG -> #717389)
  + scatter 滑珠(circle size15, 蓝填充 白描边1pt), x=完成率, y=类别中点; 值轴 0-1.2 隐藏
数据按类别自下而上: 华东0.35 西北0.51 东北0.62 华北0.74 华南0.86
文字(userShapes): 标题 18pt 加粗 / 副标题 11 / 注释 11, 白 #FFFFFF; 背景 #1A1E43
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'; BLUE = '#0070C0'; GRAY = '#717389'; TXT = '#FFFFFF'
W, H = 444.9, 299.1

regions = ['华东', '西北', '东北', '华北', '华南']
pct = [0.35, 0.51, 0.62, 0.74, 0.86]
y = np.arange(5)

fig = plt.figure(figsize=(W / 72, H / 72), facecolor=BG)
ax = fig.add_axes([0.1615, 0.1313, 0.6767, 0.6129], facecolor='none')

K = 0.5522847498

def bar_path(x0, x1, yc, h, rx, ry, left, right):
    """胶囊端帽路径: 左右端各自可选半圆(半径 rx/ry), 中间为直边."""
    y0, y1 = yc - h/2, yc + h/2
    xl = x0 + rx if left else x0
    xr = x1 - rx if right else x1
    v = [(xl, y1)]; c = [Path.MOVETO]
    v += [(xr, y1)]; c += [Path.LINETO]
    if right:
        v += [(xr + K*rx, y1), (x1, yc + K*ry), (x1, yc)]; c += [Path.CURVE4]*3
        v += [(x1, yc - K*ry), (xr + K*rx, y0), (xr, y0)]; c += [Path.CURVE4]*3
    else:
        v += [(x1, y0)]; c += [Path.LINETO]
    v += [(xl, y0)]; c += [Path.LINETO]
    if left:
        v += [(xl - K*rx, y0), (x0, yc - K*ry), (x0, yc)]; c += [Path.CURVE4]*3
        v += [(x0, yc + K*ry), (xl - K*rx, y1), (xl, y1)]; c += [Path.CURVE4]*3
    else:
        v += [(x0, y0)]; c += [Path.LINETO]
        v += [(x0, y1)]; c += [Path.LINETO]
    v += [(xl, y1)]; c += [Path.CLOSEPOLY]
    return Path(v, c)

BH, RY, RX = 0.4, 0.2, 0.0322   # 条高(类别) / 端帽半径(y) / 端帽半径(x, 与 y 等像素)
for yy, p in zip(y, pct):
    ax.add_patch(PathPatch(bar_path(p, 1.0, yy, BH, RX, RY, False, True),
                           facecolor=GRAY, linewidth=0, zorder=1))
    ax.add_patch(PathPatch(bar_path(0.0, p, yy, BH, RX, RY, True, False),
                           facecolor=BLUE, linewidth=0, zorder=2))
ax.scatter(pct, y, s=220, c=BLUE, edgecolors='#FFFFFF', linewidths=0.9, zorder=4)

for p, yy in zip(pct, y):
    ax.text(p - 0.029, yy - 0.027, f'{int(round(p*100))}%', ha='right', va='center',
            color=TXT, fontsize=9, zorder=5)

ax.set_xlim(0, 1.2); ax.set_ylim(-0.5, 4.5)
ax.set_xticks([])
ax.set_yticks(y); ax.set_yticklabels(regions, fontsize=9, color=TXT)
ax.tick_params(axis='y', length=0, pad=8)
for s in ax.spines.values(): s.set_visible(False)

fig.text(0.0733, 1 - 0.0625, '2022年上半年产品销量目标达成率情况',
         ha='left', va='top', color=TXT, fontsize=18.2, fontweight='bold')
fig.text(0.0735, 1 - 0.1554, '华南完成率最高达到86%，华东最低35%',
         ha='left', va='top', color=TXT, fontsize=11)
fig.text(0.0723, 1 - 0.9415, '*注：数据来源于公司销售系统，统计日期截至2022.06.30',
         ha='left', va='center', color='#D9D9D9', fontsize=8)

plt.savefig('29 滑珠图.png', dpi=243, facecolor=BG)
print('已生成 29 滑珠图.png')