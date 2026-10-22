import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

regions = ['华东', '西北', '东北', '华北', '华南']
sales_2022 = [1215, 1321, 1426, 1531, 2238]
sales_2021 = [1003, 1265, 1531, 1436, 2066]

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1A1E43')
ax.set_facecolor('#1A1E43')

ax.set_position([0.15, 0.15, 0.70, 0.55])

y = np.arange(len(regions))

gap = 400
ax.barh(y, [-v for v in sales_2022], left=-gap, color='#0070C0', zorder=2, height=0.4)
ax.barh(y, sales_2021, left=gap, color='#E74E69', zorder=2, height=0.4)

for i, region in enumerate(regions):
    ax.text(0, i, region, ha='center', va='center', color='white', fontsize=12, zorder=6,
            bbox=dict(boxstyle='square,pad=0.3', fc='#1A1E43', ec='none'))

for i, val in enumerate(sales_2022):
    ax.text(-gap - val/2, i, str(val), ha='center', va='center',
            color='white', fontsize=10, zorder=6)
for i, val in enumerate(sales_2021):
    ax.text(gap + val/2, i, str(val), ha='center', va='center',
            color='white', fontsize=10, zorder=6)

ax.set_xlim(-2500, 2500)
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(axis='x', length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.text(-1500, len(regions) - 0.3, '2022', ha='center', va='center',
        color='#0070C0', fontsize=14, fontweight='bold')
ax.text(1500, len(regions) - 0.3, '2021', ha='center', va='center',
        color='#E74E69', fontsize=14, fontweight='bold')

label_x = 0.05
fig.text(label_x, 0.90, '2022年上半年各区域对比去年销量', fontsize=28, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.82, '2022年整体销量高于2021年，只有东北区域较2021有所下降', fontsize=20, color='white', ha='left')
fig.text(label_x, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', fontsize=12, color='white', ha='left')

plt.savefig('4.png', dpi=150, facecolor='#1A1E43')
print("已生成 4.png")
