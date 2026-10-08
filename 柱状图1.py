import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据准备
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]

# 创建画布
fig = plt.figure(figsize=(10, 7), facecolor='#1b1e33')

# 【核心修复】极致靠左布局
# left=0.12: 极度压缩左边距，让 Y 轴数字贴近画布边缘
# width=0.84: 相应增加宽度，填满右侧
ax = fig.add_axes([0.12, 0.15, 0.84, 0.70]) 
ax.set_facecolor('#1b1e33')

# 柱子宽度
bar_width = 0.38 

# 定义渐变色 (上深下浅)
colors = ['#0056B3', '#00D2FF'] 
cmap = LinearSegmentedColormap.from_list("top_dark_blue", colors, N=256)

# 【渐变实现】使用分段 bar 模拟渐变
num_segments = 50
y_segments = np.linspace(0, 1, num_segments)

for i, (region, value) in enumerate(zip(regions, sales)):
    segment_colors = cmap(y_segments[::-1]) 
    
    segment_height = value / num_segments
    for j in range(num_segments):
        y_pos = j * segment_height
        ax.bar(i, segment_height, bottom=y_pos, width=bar_width,
               color=segment_colors[j], edgecolor='none', zorder=3)

    # 添加顶部数值标签
    ax.text(i, value + 80, str(value), 
            ha='center', va='bottom', 
            color='white', fontsize=13, fontweight='bold')

# --- 样式细节 ---

# Y轴设置
ax.set_ylim(0, 4200)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
# 【关键】
# 1. labelsize=10: 字号稍微改小，防止在窄边距下溢出
# 2. pad=2: 间距改极小，让数字紧贴轴线
# 3. direction='in': (可选) 让刻度线朝内，不占外部空间
ax.tick_params(axis='y', colors='#FFFFFF', labelsize=10, length=0, pad=2) 

# X轴设置
ax.set_xticks(range(len(regions)))
ax.set_xticklabels(regions, color='#FFFFFF', fontsize=12)
ax.tick_params(axis='x', length=0)

# 网格线
ax.yaxis.grid(True, linestyle='--', color='#4a5275', alpha=0.6, zorder=0)
ax.set_axisbelow(True)

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

# --- 标题左对齐 ---
# x=0.12 对应新的极左边缘
fig.text(0.12, 0.90, '3月各区域销量分布', 
         fontsize=28, fontweight='bold', color='white', ha='left', va='bottom')
         
fig.text(0.12, 0.84, '东北销量最多占比总销量的22%，华南销量最低', 
         fontsize=16, color='#FFFFFF', ha='left', va='bottom') 

# 底部注释
fig.text(0.12, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=9, color='#FFFFFF', ha='left', va='top')

# 保存
plt.savefig('chart_LEFT_MOST.png', dpi=150, facecolor='#1b1e33') 
print("已生成极致靠左版图表：chart_LEFT_MOST.png")