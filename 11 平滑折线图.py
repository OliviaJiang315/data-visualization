import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

cats = ['5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
vals = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]

fig, ax = plt.subplots(figsize=(12, 7.5), facecolor='#1A1E43')
ax.set_facecolor('#1A1E43')

ax.set_position([0.08, 0.22, 0.85, 0.55])

x = np.arange(len(cats))

from matplotlib.path import Path
import matplotlib.patches as patches

tangents = np.zeros_like(vals, dtype=float)
tangents[0] = (vals[1] - vals[0]) / (x[1] - x[0])
tangents[-1] = (vals[-1] - vals[-2]) / (x[-1] - x[-2])
for i in range(1, len(vals) - 1):
    tangents[i] = (vals[i+1] - vals[i-1]) / (x[i+1] - x[i-1])

verts = [(x[0], vals[0])]
codes = [Path.MOVETO]
for i in range(len(x) - 1):
    dx = x[i+1] - x[i]
    cp1 = (x[i] + dx / 3, vals[i] + tangents[i] * dx / 3)
    cp2 = (x[i+1] - dx / 3, vals[i+1] - tangents[i+1] * dx / 3)
    verts.extend([cp1, cp2, (x[i+1], vals[i+1])])
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])

path = Path(verts, codes)
patch = patches.PathPatch(path, facecolor='none', edgecolor='#E66B4C', linewidth=2.5, zorder=3)
ax.add_patch(patch)

ax.set_ylim(0, 4500)
ax.set_yticks(range(0, 4501, 1000))
ax.tick_params(axis='y', colors='#E66B4C', labelsize=10, length=0)
ax.set_xticks(x)
ax.set_xticklabels(cats, color='white', fontsize=11)
ax.tick_params(axis='x', length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.axhline(y=0, color='white', linewidth=1, zorder=1)

max_x = 0
max_y = 0
for i in range(len(x) - 1):
    dx = x[i+1] - x[i]
    P0 = (x[i], vals[i])
    P1 = (x[i] + dx / 3, vals[i] + tangents[i] * dx / 3)
    P2 = (x[i+1] - dx / 3, vals[i+1] - tangents[i+1] * dx / 3)
    P3 = (x[i+1], vals[i+1])
    for t in np.linspace(0, 1, 200):
        bx = (1-t)**3*P0[0] + 3*(1-t)**2*t*P1[0] + 3*(1-t)*t**2*P2[0] + t**3*P3[0]
        by = (1-t)**3*P0[1] + 3*(1-t)**2*t*P1[1] + 3*(1-t)*t**2*P2[1] + t**3*P3[1]
        if by > max_y:
            max_y = by
            max_x = bx
ax.plot([max_x, max_x], [0, max_y], linestyle='--', color='#E66B4C', linewidth=1.5, zorder=2)

from matplotlib.patches import FancyBboxPatch
xl, xr = ax.get_xlim()
mid = 7.5
fx_left = 0.08
fx_right = 0.93
fx_mid = 0.08 + 0.85 * (mid - xl) / (xr - xl)
gap = 0.006
fig.add_artist(FancyBboxPatch((fx_left, 0.10), fx_mid - fx_left - gap, 0.04,
                              transform=fig.transFigure, boxstyle='round,pad=0,rounding_size=0.008',
                              facecolor='#A6CEE3', edgecolor='#A6CEE3', linewidth=1.8, zorder=0))
fig.add_artist(FancyBboxPatch((fx_mid + gap, 0.10), fx_right - fx_mid - gap, 0.04,
                              transform=fig.transFigure, boxstyle='round,pad=0,rounding_size=0.008',
                              facecolor='#FDB863', edgecolor='#FDB863', linewidth=1.8, zorder=0))
fig.text((fx_left + fx_mid) / 2, 0.12, '2021', ha='center', va='center',
         color='white', fontsize=13, fontweight='bold')
fig.text((fx_mid + fx_right) / 2, 0.12, '2022', ha='center', va='center',
         color='white', fontsize=13, fontweight='bold')

ax.text(max_x, max_y + 180, '3782', ha='center', va='bottom',
        color='white', fontsize=14, fontweight='bold', zorder=4)

label_x = 0.05
fig.text(label_x, 0.90, '化妆品品类月度销量走势', fontsize=31, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.82, '2022年销量迅速增加，1月最高，销量达到3782', fontsize=20, color='white', ha='left')
fig.text(label_x, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.03.31', fontsize=12, color='white', ha='left')

plt.savefig('11 平滑折线图.png', dpi=150, facecolor='#1A1E43')
print("已生成 11 平滑折线图.png")
