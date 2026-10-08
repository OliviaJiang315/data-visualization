import matplotlib.pyplot as plt
import numpy as np

# ================= 配置区 =================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
avg_sales = np.mean(sales) # 2656
# ==========================================

# 1. 创建画布
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#1b1e33')
ax.set_facecolor('#1b1e33')

# 2. 调整绘图区位置
ax.set_position([0.10, 0.18, 0.75, 0.65])

# 3. 绘制纯色柱子
bar_color = '#0070C0' 
bars = ax.bar(regions, sales, color=bar_color, width=0.35, zorder=2)

# 4. 添加数值标签
for i, value in enumerate(sales):
    ax.text(i, value + 60, str(value), 
            ha='center', va='bottom', 
            color='white', fontsize=12, fontweight='bold', zorder=5)

# 5. 绘制平均值参考线
ax.axhline(y=avg_sales, color='#FFD700', linestyle='-', linewidth=1.5, zorder=3)

# 6. 【核心修改】平均值文字位置优化
# x = len(regions) - 0.1 : 之前是 -0.2，现在改为 -0.1，更靠右，利用边缘空白
# y = avg_sales + 150  : 之前是 +80，现在改为 +150，大幅抬高，彻底避开 2563
ax.text(len(regions) - 0.1, avg_sales + 150, f'平均值：{int(avg_sales)}',
        color='#FFD700', fontsize=13, ha='right', va='bottom', fontweight='bold', zorder=5)

# 7. 样式调整
ax.set_ylim(0, 4600) 
ax.yaxis.set_ticks([]) 

# X 轴设置
ax.tick_params(axis='x', colors='#FFFFFF', labelsize=12, length=0)
ax.spines['bottom'].set_color('#4a5275') 
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# --- 标题位置 (保持图2的舒适感) ---
fig.text(0.10, 0.88, '3月各区域销量分布', 
         fontsize=30, fontweight='bold', color='white', ha='left')
         
fig.text(0.10, 0.83, '东北销量最多占比总销量的22%，华南销量最低', 
         fontsize=18, color='white', ha='left') 

# --- 底部注释 ---
fig.text(0.10, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=10, color='#FFFFFF', ha='left')

# 保存
plt.savefig('chart_NO_OVERLAP_FINAL.png', dpi=150, facecolor='#1b1e33')
print("已生成无重叠最终版图表")