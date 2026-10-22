import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [4321, 1946, 1536, 1872, 1369, 2109]
placeholder1 = [0, 2375, 2785, 2449, 2952, 2212]
placeholder2 = [1080.25] * 6
yoy = ['-13.6%', '-20.8%', '-9.3%', '-15.9%', '-17.9%', '-5.8%']

fig, ax = plt.subplots(figsize=(10, 7.5), facecolor='#1A1E43')
ax.set_facecolor('#1A1E43')

ax.set_position([0.15, 0.15, 0.70, 0.55])

y = np.arange(len(regions))

ax.barh(y, sales, color='#09387E', zorder=2, height=0.65)
ax.barh(y, placeholder1, left=sales, color='#82ADD7', zorder=2, height=0.65)
left2 = [s + p for s, p in zip(sales, placeholder1)]
ax.barh(y, placeholder2, left=left2, color='#9B3D4F', zorder=2, height=0.65)

for i, val in enumerate(sales):
    ax.text(val - 100, i, str(val), ha='right', va='center',
            color='white', fontsize=11, zorder=6)

for i, yt in enumerate(yoy):
    ax.text(left2[i] + placeholder2[i] / 2, i, yt, ha='center', va='center',
            color='white', fontsize=11, zorder=6)

ax.set_yticks(y)
ax.set_yticklabels(regions, color='white', fontsize=12)
ax.tick_params(axis='y', length=0)
ax.set_xticks([])
ax.tick_params(axis='x', length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

label_x = 0.05
fig.text(label_x, 0.90, '2021年各区域销量及同比情况', fontsize=28, fontweight='bold', color='white', ha='left')
fig.text(label_x, 0.82, '各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%', fontsize=20, color='white', ha='left')
fig.text(label_x, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.01.01', fontsize=12, color='white', ha='left')

plt.savefig('8 数值百分比.png', dpi=150, facecolor='#1A1E43')
print("已生成 8 数值百分比.png")
