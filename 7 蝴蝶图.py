import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

regions = ['华东', '西北', '东北', '华北', '华南']
data_2022 = [36, 31, 18, 13, 9]
data_2021 = [42, 26, 19, 12, 5]

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1A1E43')
ax.set_facecolor('#1A1E43')

ax.set_position([0.12, 0.15, 0.76, 0.55])

y = np.arange(len(regions))
gap = 4

ax.barh(y, [-v for v in data_2022], left=-gap, color='#0070C0', zorder=2, height=0.35)
ax.barh(y, data_2021, left=gap, color='#E74E69', zorder=2, height=0.35)

for i, region in enumerate(regions):
    ax.text(0, i, region, ha='center', va='center', color='white', fontsize=12, zorder=6,
            bbox=dict(boxstyle='square,pad=0.3', fc='#1A1E43', ec='none'))

ax.set_xlim(-50, 50)
ax.set_xticks([])
ax.set_yticks(y)
ax.set_yticklabels([f'{v}%' for v in data_2022], color='white', fontsize=11)
ax.tick_params(axis='y', length=0)
ax.tick_params(axis='x', length=0)
ax.invert_yaxis()

for i, val in enumerate(data_2021):
    ax.text(52, i, f'{val}%', ha='left', va='center', color='white', fontsize=11, zorder=6)

for spine in ax.spines.values():
    spine.set_visible(False)

label_x = 0.05
fig.text(label_x, 0.90, '2022年第一季度销售目标完成情况', fontsize=28, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.82, '华东区域完成率最高达到36%，但是相比去年的42%有所下降', fontsize=20, color='white', ha='left')
fig.text(label_x, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.03.31', fontsize=12, color='white', ha='left')

plt.savefig('5.png', dpi=150, facecolor='#1A1E43')
print("已生成 5.png")
