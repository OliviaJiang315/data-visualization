# -*- coding: utf-8 -*-
"""25 子弹图 (依据 chart12.xml 复刻主图)

纵向柱子弹图: 6 组背景 3 段堆积区间(及格82ADD7 0-600 / 良好00B0F0 600-800 / 优秀0070C0 800-1000)
+ 实际销量亮蓝细条 0E5DFF + 目标黄色短横线 #FFC000(宽=柱宽)在目标值位置.
值轴 0-1200, 横轴商品名, 图例5项(上), 左上标题/副标题, 左下注释, 背景 #1A1E43.
几何来自 _chart25_obj2.png(2.08x, Chart 438.9x297.4) 实测
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
C_PASS = '#82ADD7'   # 及格(最浅)
C_GOOD = '#00B0F0'   # 良好(中)
C_EXC = '#0070C0'    # 优秀(较深)
C_ACT = '#0E5DFF'    # 实际(亮蓝)
C_TGT = '#FFC000'    # 目标(黄)
TXT = '#F2F2F2'

W, H = 438.9, 297.4
x = np.arange(6)
actual = [653, 523, 648, 856, 714, 785]
target = [700, 500, 600, 900, 600, 600]
cats = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']

fig = plt.figure(figsize=(10, 10 * H / W), facecolor=BG)
ax = fig.add_axes([0.1277, 0.168, 0.823, 0.541], facecolor='none')

# 3 段堆积背景(宽) 及格0-600 / 良好600-800 / 优秀800-1000
bw = 0.30
ax.bar(x, [600]*6, width=bw, color=C_PASS, zorder=1)
ax.bar(x, [200]*6, width=bw, bottom=[600]*6, color=C_GOOD, zorder=1)
ax.bar(x, [200]*6, width=bw, bottom=[800]*6, color=C_EXC, zorder=1)
# 实际销量(窄细条) 居中叠加
aw = 0.17
ax.bar(x, actual, width=aw, color=C_ACT, zorder=3)
# 目标短横线(宽=实际柱宽, 黄)
for i, v in enumerate(target):
    ax.hlines(v, i-aw/2, i+aw/2, colors=C_TGT, lw=2.5, zorder=4)

ax.set_xlim(-0.5, 5.5); ax.set_ylim(0, 1200)
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.tick_params(axis='y', colors=TXT, length=0, labelsize=11, pad=12)
ax.tick_params(axis='x', length=0)
ax.set_xticks(x); ax.set_xticklabels([])
for s in ax.spines.values(): s.set_visible(False)
# 横轴分类(fig 精确位置)
for i, cat in enumerate(cats):
    cx_fig = 0.1277 + (i+0.5)/6*0.823
    fig.text(cx_fig, 0.135, cat, ha='center', va='center', color=TXT, fontsize=13)

# 图例(上部 y0.708): 5 项横排 及格/良好/优秀/实际/目标
def legend_box(fx, color, filled):
    if filled:
        fig.add_artist(Rectangle((fx, 0.708-0.009), 0.012, 0.018, transform=fig.transFigure,
                                 facecolor=color, edgecolor='none'))
    else:
        fig.add_artist(Rectangle((fx, 0.708-0.009), 0.012, 0.018, transform=fig.transFigure,
                                 facecolor='none', edgecolor=color, lw=1.2))
x0 = 0.18
step = 0.079
legend_box(x0+0*step, C_PASS, True); fig.text(x0+0*step+0.017, 0.708, '及格', va='center', color=TXT, fontsize=13)
legend_box(x0+1*step, C_GOOD, True); fig.text(x0+1*step+0.017, 0.708, '良好', va='center', color=TXT, fontsize=13)
legend_box(x0+2*step, C_EXC, True); fig.text(x0+2*step+0.017, 0.708, '优秀', va='center', color=TXT, fontsize=13)
legend_box(x0+3*step, C_ACT, True); fig.text(x0+3*step+0.017, 0.708, '实际', va='center', color=TXT, fontsize=13)
# 目标: 短横线符号
fig.add_artist(Rectangle((x0+4*step, 0.708-0.002), 0.012, 0.004, transform=fig.transFigure,
                         facecolor=C_TGT, edgecolor='none'))
fig.text(x0+4*step+0.017, 0.708, '目标', va='center', color=TXT, fontsize=13)

# 标题/副标题(左上)
fig.text(0.063, 0.939, '2022年上半年各商品销量完成情况', ha='left', va='top',
         color=TXT, fontsize=30, fontweight='bold')
fig.text(0.062, 0.844, '防晒整体销量最好，达到856，面霜远超目标，超额完成30%', ha='left', va='top',
         color=TXT, fontsize=18)

# 注释(左下)
fig.text(0.061, 0.055, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', ha='left', va='center',
         color='#C8C8C8', fontsize=13)

plt.savefig('25 子弹图.png', dpi=150, facecolor=BG)
print('已生成 25 子弹图.png')