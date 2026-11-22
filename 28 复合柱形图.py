# -*- coding: utf-8 -*-
"""28 复合柱形图 (依据 chart15.xml + _chart28_obj1.png 实测复刻)

两个 clustered barChart 复合: 月度销量窄柱(按季度 4 色: 4A5BD1/FC6C0F/F6A50B/A2417B, 柱顶数值)
+ 季度销量宽柱(同色 20% alpha, 宽=整组无间隙) 完全重叠; 双轴 max=12000;
X 轴线 #454866 位于基线下 1-2px; 背景 #1A1E43; 无图例/无刻度数字
文字(标题/副标题/注释/横轴)由位图 OCR + 测量, 无 XML 标题
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'; TXT = '#F2F2F2'; AXIS = '#454866'
W, H = 444.9, 303.4

# 15 个类别槽: 4 组 x 3 月, 组间空一槽; 12 个有值
valid = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14]
vals = [2354, 1902, 3524, 2698, 2896, 2563, 3156, 2896, 3621, 2635, 2963, 2789]
cols = ['#4A5BD1']*3 + ['#FC6C0F']*3 + ['#F6A50B']*3 + ['#A2417B']*3
labels = ['1月', '2月', '3月', '', '4月', '5月', '6月', '',
          '7月', '8月', '9月', '', '10月', '11月', '12月']
q_center = [1.0, 5.0, 9.0, 13.0]
q_vals = [7780, 8157, 9673, 8387]
q_cols = ['#4A5BD1', '#FC6C0F', '#F6A50B', '#A2417B']

fig = plt.figure(figsize=(W / 72, H / 72), facecolor=BG)
ax = fig.add_axes([0.0966, 0.1695, 0.7923, 0.6589], facecolor='none')

# 季度销量: 宽柱=3 个类别宽, 无缝, 20% 透明
ax.bar(q_center, q_vals, width=3.0, color=q_cols, alpha=0.2, linewidth=0, zorder=1)
# 月度销量: 窄柱
ax.bar(valid, vals, width=0.41, color=cols, linewidth=0, zorder=2)

ax.set_xlim(-0.5, 14.5); ax.set_ylim(0, 12000)
ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(axis='y', length=0)
ax.set_xticks(range(15)); ax.set_xticklabels(labels, fontsize=8, color=TXT)
ax.tick_params(axis='x', length=0, pad=6.5)
# X 轴灰蓝横线(基线)
ax.axhline(0, color=AXIS, lw=0.9, zorder=5, clip_on=False)

# 柱顶数值标签(白 95%, 字号按原图位图字宽校准)
for i, v in zip(valid, vals):
    ax.text(i, v + 300, str(v), ha='center', va='bottom', color=TXT, fontsize=7.4, zorder=6)
# 季度宽块顶部标签: XML 该系列仅保留每季度中间柱(idx1/5/9/13)标签
for cx, qv in zip(q_center, q_vals):
    ax.text(cx, qv + 300, str(qv), ha='center', va='bottom', color=TXT, fontsize=8, zorder=6)

# 标题/副标题/注释
fig.text(0.0662, 0.9305, '2021年各月化妆品销量走势', ha='left', va='top', color='#FFFFFF', fontsize=18.5)
fig.text(0.068, 0.8404, '2021年第三季度销量最多9673，9月单月销量最大3621', ha='left', va='top', color='#FFFFFF', fontsize=11)
fig.text(0.055, 0.0466, '*注：数据来源于公司销售系统，统计日期截至2021.12.31', ha='left', va='center', color='#D9D9D9', fontsize=8)

plt.savefig('28 复合柱形图.png', dpi=243, facecolor=BG)
print('已生成 28 复合柱形图.png')