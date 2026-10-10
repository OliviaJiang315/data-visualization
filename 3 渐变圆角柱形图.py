import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

# ================= 配置区 =================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据准备
products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
sales = [653, 523, 648, 856, 714, 785]

# 计算极值用于副标题
max_sales = max(sales)
min_sales = min(sales)
max_prod = products[sales.index(max_sales)]
min_prod = products[sales.index(min_sales)]
subtitle_text = f"{max_prod}销量最多，3月销量{max_sales}；{min_prod}最少，3月销量{min_sales}"

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1b1e33')
ax.set_facecolor('#1b1e33')

# 定义渐变色（底部改为#0064B7，与Excel原图3一致）
colors = ['#0064B7', '#00E5FF']
cmap = LinearSegmentedColormap.from_list("capsule_gradient", colors, N=256)

# ================= 绘图核心逻辑 =================
line_width = 16
num_segments = 60
cap_r = (line_width / 2) * (1200 - 0) / (7.5 * 0.50 * 72)

for i, val in enumerate(sales):
    segment_height = val / num_segments
    segment_colors = cmap(np.linspace(0, 1, num_segments))

    for j in range(num_segments):
        y_start = cap_r + j * segment_height
        y_end = cap_r + (j + 1) * segment_height

        ax.plot([i, i], [y_start, y_end],
                color=segment_colors[j],
                linewidth=line_width,
                solid_capstyle='round',
                zorder=2)

# ================= 绘制数据标签 =================
text_objs = []
circle_info = []

for i, val in enumerate(sales):
    top = val + 2 * cap_r  # 柱子顶端（半圆顶部）
    ax.plot([i, i], [top, top + 85], color='#5B9BD5', linewidth=1.5, zorder=3)
    ax.scatter(i, top + 85, color='#5B9BD5', s=60, zorder=6)
    t = ax.annotate(str(val), xy=(i, top + 85), xytext=(12, 0),
                    textcoords='offset points',
                    ha='left', va='center',
                    color='white', fontsize=10, fontweight='bold', zorder=6)
    text_objs.append(t)
    circle_info.append((i, top + 85))

fig.canvas.draw()
circle_r_disp = np.sqrt(60 / np.pi)

for t, (cx, cy) in zip(text_objs, circle_info):
    txt_ext = t.get_window_extent()
    circ_disp = ax.transData.transform((cx, cy))
    bx0 = circ_disp[0] - circle_r_disp - 6
    bx1 = txt_ext.x1 + 6
    by0 = min(circ_disp[1] - circle_r_disp, txt_ext.y0) - 8
    by1 = max(circ_disp[1] + circle_r_disp, txt_ext.y1) + 8
    bd = ax.transData.inverted().transform([[bx0, by0], [bx1, by1]])
    rect = FancyBboxPatch((bd[0, 0], bd[0, 1]),
                          bd[1, 0] - bd[0, 0], bd[1, 1] - bd[0, 1],
                          boxstyle="round,pad=0.01",
                          fc="#243B5D", ec="none", zorder=4,
                          transform=ax.transData)
    ax.add_patch(rect)

# ================= 样式调整 =================
ax.set_position([0.12, 0.20, 0.85, 0.50])

# Y轴设置（改为0-1200，与Excel原图3一致）
ax.set_ylim(0, 1200)
ax.set_yticks(range(0, 1201, 200))
ax.tick_params(axis='y', colors='white', labelsize=10, length=0)
ax.spines['left'].set_visible(False)

ax.set_xticks(range(len(products)))
ax.set_xticklabels(products, color='white', fontsize=11)
ax.tick_params(axis='x', length=0)

ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.yaxis.grid(True, linestyle='--', color='#2f3552', alpha=0.8, zorder=0)
ax.axhline(y=1200, linestyle='--', color='#2f3552', alpha=0.8, zorder=0)
ax.set_axisbelow(True)

# 标题位置（与Y轴数字左边缘对齐）
fig.canvas.draw()
label_x = min(label.get_window_extent().x0 for label in ax.get_yticklabels()) / fig.canvas.get_width_height()[0]
fig.text(label_x, 0.88, '3月商品销量对比', fontsize=28, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.78, subtitle_text, fontsize=22, color='white', ha='left')

# 底部注释
fig.text(label_x, 0.08, '*注：数据来源于公司销售系统，统计日期截至2022.03.31', fontsize=12, color='white', ha='left')

# 保存为1.png
plt.savefig('1.png', dpi=150, facecolor='#1b1e33')
print("已生成 1.png")
