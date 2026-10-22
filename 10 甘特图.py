import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import datetime

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

tasks = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
start_dates = [44621, 44633, 44642, 44653, 44667, 44692, 44707]
durations = [11, 8, 10, 13, 24, 14, 7]
percents = ['51%', '32%', '21%', '85%', '36%', '68%', '68%']

def excel_date(serial):
    return datetime.datetime(1899, 12, 30) + datetime.timedelta(days=int(serial))

def format_date(serial):
    d = excel_date(serial)
    return f'{d.year}/{d.month}/{d.day}'

fig, ax = plt.subplots(figsize=(12, 7.5), facecolor='#1A1E43')
ax.set_facecolor('#1A1E43')

ax.set_position([0.15, 0.15, 0.75, 0.60])

y = np.arange(len(tasks))

pct_vals = [51, 32, 21, 85, 36, 68, 68]

for i in range(len(tasks)):
    d = durations[i]
    p = pct_vals[i]
    w_light = d * p / 100
    w_dark = d * (100 - p) / 100
    ax.barh(y[i], w_light, left=start_dates[i], color='#009ACD', zorder=2, height=0.5)
    ax.barh(y[i], w_dark, left=start_dates[i] + w_light, color='#0070C0', zorder=2, height=0.5)
    ax.text(start_dates[i] + d / 2, y[i], percents[i], ha='center', va='center',
            color='white', fontsize=11, zorder=6)

ax.set_yticks(y)
ax.set_yticklabels(tasks, color='white', fontsize=12)
ax.tick_params(axis='y', length=0)
ax.invert_yaxis()

ax.set_xlim(44610, 44735)
date_ticks = list(range(44621, 44727, 15))
ax.set_xticks(date_ticks)
ax.set_xticklabels([format_date(t) for t in date_ticks],
                   color='white', fontsize=9, rotation=0)
ax.tick_params(axis='x', length=0)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

for spine in ax.spines.values():
    spine.set_visible(False)

ax.xaxis.grid(True, linestyle='--', color='white', alpha=0.3, zorder=0)
ax.set_axisbelow(True)

label_x = 0.05
fig.text(0.5, 0.90, '2022年化妆品类目采购项目进度', fontsize=28, fontweight='bold', color='white', ha='center')

plt.savefig('10 甘特图.png', dpi=150, facecolor='#1A1E43')
print("已生成 10 甘特图.png")
