import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

products = ['口红', '面膜', '隔离', '防晒', '精华']
sales_2021 = [3568, 4135, 4436, 4106, 4936]
sales_2022 = [2569, 3241, 2965, 3209, 3541]

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1A1E43')
ax.set_facecolor('#1A1E43')

ax.set_position([0.12, 0.15, 0.76, 0.55])

x = np.arange(len(products))
width = 0.25

offset = 0.175
ax.bar(x - offset, sales_2021, width, color='#0070C0', zorder=2)
ax.bar(x + offset, sales_2022, width, color='#82ADD7', zorder=2)

for i, val in enumerate(sales_2021):
    ax.text(i - offset, val + 80, str(val), ha='center', va='bottom',
            color='white', fontsize=11, zorder=6)
for i, val in enumerate(sales_2022):
    ax.text(i + offset, val - 80, str(val), ha='center', va='top',
            color='white', fontsize=11, zorder=6)

for i in range(len(products)):
    diff = sales_2021[i] - sales_2022[i]
    ax.plot([i - offset, i + offset], [sales_2021[i], sales_2021[i]],
            color='#0070C0', linewidth=1.0, zorder=4)
    ax.annotate('', xy=(i + offset, sales_2021[i]), xytext=(i + offset, sales_2022[i]),
                arrowprops=dict(arrowstyle='->', color='white', lw=1.5),
                zorder=5)
    ax.text(i + offset + 0.03, (sales_2021[i] + sales_2022[i]) / 2, str(diff),
            ha='left', va='center', color='white', fontsize=10, zorder=6)

ax.set_ylim(0, 5500)
ax.set_yticks([])
ax.set_xticks(x)
ax.set_xticklabels(products, color='white', fontsize=12)
ax.tick_params(axis='x', length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.axhline(y=0, color='white', linewidth=1, zorder=1)

label_x = 0.05
fig.text(label_x, 0.90, '2022年商品对比去年销售情况', fontsize=28, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.82, '商品整体比去年销量有所下降，其中隔离下降最多，下降33%', fontsize=18, color='white', ha='left')

fig.text(label_x, 0.75, '■', fontsize=14, color='#0070C0', ha='left', va='center')
fig.text(label_x + 0.025, 0.75, '2021销量', fontsize=11, color='white', ha='left', va='center')
fig.text(label_x + 0.15, 0.75, '■', fontsize=14, color='#82ADD7', ha='left', va='center')
fig.text(label_x + 0.175, 0.75, '2022销量', fontsize=11, color='white', ha='left', va='center')
fig.text(label_x, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.01.01', fontsize=12, color='white', ha='left')

plt.savefig('9 对比柱形图.png', dpi=150, facecolor='#1A1E43')
print("已生成 9 对比柱形图.png")
