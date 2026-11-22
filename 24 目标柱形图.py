# -*- coding: utf-8 -*-
"""24 目标柱形图 (依据 chart10.xml 复刻主图)

6 组: 目标销量=宽空心灰白线框柱(背景) + 实际销量=窄实心蓝柱(居中叠加)
左轴0-1000(隐藏), 实际柱顶白数值标签, 横轴:口红/面膜/隔离/防晒/精华/面霜
图例(左上): □目标销量 ■实际销量 ; 左上标题/副标题 ; 左下注释 ; 深蓝背景#1A1E43
几何来自 _chart24_obj2.png(2.08x, chart 444.9x297.4) 实测
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
GRAY = '#C0C4D0'   # 目标空心柱边框(灰白)
TXT = '#F2F2F2'

W, H = 444.9, 297.4
x = np.arange(6)
actual = [653, 523, 648, 856, 714, 785]
target = [700, 500, 600, 900, 600, 600]
cats = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']

fig = plt.figure(figsize=(10, 10 * H / W), facecolor=BG)
ax = fig.add_axes([0.0749, 0.193, 0.848, 0.543], facecolor='none')

# 目标柱(宽空心) 在底层
ax.bar(x, target, width=0.26, facecolor='none', edgecolor=GRAY, linewidth=1.2, zorder=2)
# 实际柱(窄实心蓝) 居中叠加
ax.bar(x, actual, width=0.18, color=BLUE, zorder=3)

ax.set_xlim(-0.5, 5.5); ax.set_ylim(0, 1000)
ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(axis='x', length=0)
ax.set_xticks(x); ax.set_xticklabels([])
# 横轴分类(fig 精确位置 y=0.156 ≈ 基线下方近处, 与原图 y523/620 一致)
for i, cat in enumerate(cats):
    cx_fig = 0.0749 + (i + 0.5) / 6 * 0.848
    fig.text(cx_fig, 0.156, cat, ha='center', va='center', color=TXT, fontsize=13)

# 实际柱顶白数值标签
for i, v in enumerate(actual):
    ax.text(i, v + 50, str(v), ha='center', va='bottom', color=TXT, fontsize=11)

# 图例(左上, 标题下方): □目标销量  ■实际销量
def legend_item(fx, fy, filled, label):
    w_, h_ = 0.013, 0.016
    if filled:
        fig.add_artist(Rectangle((fx, fy - h_/2), w_, h_, transform=fig.transFigure,
                                 facecolor=BLUE, edgecolor='none'))
    else:
        fig.add_artist(Rectangle((fx, fy - h_/2), w_, h_, transform=fig.transFigure,
                                 facecolor='none', edgecolor=GRAY, lw=1.2))
    fig.text(fx + w_ + 0.006, fy, label, ha='left', va='center', color=TXT, fontsize=11)
legend_item(0.114, 0.727, False, '目标销量')
legend_item(0.224, 0.727, True, '实际销量')

# 标题/副标题(左上)
fig.text(0.074, 0.934, '2022年上半年各商品销量完成情况', ha='left', va='top',
         color=TXT, fontsize=28, fontweight='bold')
fig.text(0.073, 0.840, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%', ha='left', va='top',
         color=TXT, fontsize=18)

# 注释(左下)
fig.text(0.066, 0.060, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', ha='left', va='center',
         color='#C8C8C8', fontsize=10)

plt.savefig('24 目标柱形图.png', dpi=150, facecolor=BG)
print('已生成 24 目标柱形图.png')