import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
sales = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
colors = ['#87CEEB', '#3CB371', '#FF6B47', '#FFC107', '#00A8E8', '#0077C8', '#5B5FC7', '#4A4DB8']

subtitle_text = '口红销量最好达9221，是眼影最低值2645近3.5倍'

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1a1f3c')
ax.set_facecolor('#1a1f3c')

ax.set_position([0.12, 0.20, 0.85, 0.50])
ax.set_ylim(0, 10000)
ax.set_yticks(range(0, 10001, 2000))

ax.bar(range(len(products)), sales, color=colors, width=0.35, zorder=2)

text_objs = []
for i, val in enumerate(sales):
    t = ax.text(i, val + 700, str(val),
                ha='center', va='center',
                color='white', fontsize=10, fontweight='bold', zorder=6,
                bbox=dict(boxstyle="round,pad=0.4", fc=colors[i], ec="none", alpha=0.9))
    text_objs.append((t, i, val))

fig.canvas.draw()
inv = ax.transData.inverted()
for t, i, val in text_objs:
    bbox_ext = t.get_bbox_patch().get_window_extent()
    cx_disp = (bbox_ext.x0 + bbox_ext.x1) / 2
    tri_w_disp = (bbox_ext.x1 - bbox_ext.x0) * 0.15
    offset_disp = (bbox_ext.x1 - bbox_ext.x0) * 0.2
    if i % 2 == 0:
        tip_cx = cx_disp - offset_disp
    else:
        tip_cx = cx_disp + offset_disp
    top_left = inv.transform((tip_cx - tri_w_disp, bbox_ext.y0))
    top_right = inv.transform((tip_cx + tri_w_disp, bbox_ext.y0))
    ax.fill([top_left[0], top_right[0], i],
            [top_left[1], top_right[1], val],
            color=colors[i], zorder=5)

ax.set_xticks(range(len(products)))
ax.set_xticklabels(products, color='white', fontsize=11)
ax.tick_params(axis='y', colors='white', labelsize=10, length=0)
ax.tick_params(axis='x', length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.yaxis.grid(True, linestyle='--', color='#2f3552', alpha=0.8, zorder=0)
ax.axhline(y=10000, linestyle='--', color='#2f3552', alpha=0.8, zorder=0)
ax.set_axisbelow(True)

fig.canvas.draw()
label_x = min(label.get_window_extent().x0 for label in ax.get_yticklabels()) / fig.canvas.get_width_height()[0]
fig.text(label_x, 0.88, '2021年商品销量情况', fontsize=28, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.78, subtitle_text, fontsize=22, color='white', ha='left')
fig.text(label_x, 0.08, '*注：数据来源于公司销售系统，统计日期截至2022.08.31', fontsize=12, color='white', ha='left')

plt.savefig('2.png', dpi=150, facecolor='#1a1f3c')
print("已生成 2.png")
