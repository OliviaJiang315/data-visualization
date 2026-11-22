# -*- coding: utf-8 -*-
"""20 南丁格尔（PPT） (依据 第二章 图表(后15).xlsx drawing11.xml Freeform贝塞尔精确复刻)

南丁格尔玫瑰图: 6扇区, 用drawing11.xml中的Freeform贝塞尔曲线形状绘制.
通过完整变换链(path -> Freeform xfrm -> 组合8 xfrm -> 组合6 xfrm -> sheet)
将贝塞尔曲线转换到sheet坐标(pt), 再映射到figure坐标.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np
import os, re, zipfile

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
TXT = '#F2F2F2'
TXT_DIM = '#D9D9D9'

# ============================================================
# 1. 从 xlsx 直接读取 drawing11.xml 中的 Freeform 形状
# ============================================================
XLSX_PATH = r'C:\Users\Lenovo\Desktop\jiaxinyu\数据可视化\第二章 图表(后15).xlsx'
with zipfile.ZipFile(XLSX_PATH) as z:
    draw_content = z.read('xl/drawings/drawing11.xml').decode('utf-8')

# --- 变换链 (使用Excel COM精确位置) ---
# 组合6: twoCellAnchor from(col=4,row=1) to(col=12,row=23)
# Excel COM: left=219.43pt, top=14.14pt, w=438.86pt, h=313.71pt
# xfrm: off=(272,18.5)pt, ext=(544,407)pt, chOff=(272,351.5)pt, chExt=(544,407)pt
GRP6_LEFT = 219.43
GRP6_TOP = 14.14
GRP6_WIDTH = 438.86
GRP6_HEIGHT = 313.71
GRP6_CHOFF = (272.0, 351.5)
GRP6_CHEXT = (544.0, 407.0)

# 组合8 (嵌套在组合6内)
# xfrm: off=(446.9,444)pt, ext=(244.2,274.5)pt, chOff=(272,21)pt, chExt=(194,225.5)pt
GRP8_OFF = (446.9, 444.0)
GRP8_EXT = (244.2, 274.5)
GRP8_CHOFF = (272.0, 21.0)
GRP8_CHEXT = (194.0, 225.5)

def child8_to_sheet(x_pt, y_pt):
    """组合8子坐标(pt) -> sheet坐标(pt)"""
    # 组合8子坐标 -> 组合6子坐标
    sx8 = GRP8_EXT[0] / GRP8_CHEXT[0]
    sy8 = GRP8_EXT[1] / GRP8_CHEXT[1]
    child6_x = GRP8_OFF[0] + (x_pt - GRP8_CHOFF[0]) * sx8
    child6_y = GRP8_OFF[1] + (y_pt - GRP8_CHOFF[1]) * sy8

    # 组合6子坐标 -> sheet坐标 (关键: 用 chOff 而非 off, 因为 off != chOff)
    sx6 = GRP6_WIDTH / GRP6_CHEXT[0]
    sy6 = GRP6_HEIGHT / GRP6_CHEXT[1]
    sheet_x = GRP6_LEFT + (child6_x - GRP6_CHOFF[0]) * sx6
    sheet_y = GRP6_TOP + (child6_y - GRP6_CHOFF[1]) * sy6
    return sheet_x, sheet_y

# --- 解析Freeform形状 ---
sp_blocks = re.findall(r'<xdr:sp\b.*?</xdr:sp>', draw_content, re.DOTALL)

freeforms = []
for sp in sp_blocks:
    name_m = re.search(r'<xdr:cNvPr[^>]*name="([^"]+)"', sp)
    name = name_m.group(1) if name_m else ''
    if 'Freeform' not in name:
        continue

    off_m = re.search(r'<a:off x="(\d+)" y="(\d+)"', sp)
    ext_m = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', sp)
    off_pt = (int(off_m.group(1)) / 9525, int(off_m.group(2)) / 9525)
    ext_pt = (int(ext_m.group(1)) / 9525, int(ext_m.group(2)) / 9525)

    fill_m = re.search(r'<a:solidFill>.*?srgbClr val="([0-9A-Fa-f]{6})"', sp, re.DOTALL)
    color = '#' + fill_m.group(1) if fill_m else None

    path_m = re.search(r'<a:pathLst>(.*?)</a:pathLst>', sp, re.DOTALL)
    if not path_m:
        continue

    path_info = re.search(r'<a:path w="(\d+)" h="(\d+)"', path_m.group(1))
    path_w = int(path_info.group(1))
    path_h = int(path_info.group(2))

    path_content = re.search(r'<a:path[^>]*>(.*?)</a:path>', path_m.group(1), re.DOTALL).group(1)

    tokens = re.findall(r'<a:(moveTo|lnTo|cubicBezTo|close)\b([^>]*)/?>', path_content)
    pts_all = re.findall(r'<a:pt x="(-?\d+)" y="(-?\d+)"', path_content)

    cmd_list = []
    pt_idx = 0
    for cmd_name, _ in tokens:
        if cmd_name in ('moveTo', 'lnTo'):
            x, y = int(pts_all[pt_idx][0]), int(pts_all[pt_idx][1])
            pt_idx += 1
            cmd_list.append((cmd_name, [(x, y)]))
        elif cmd_name == 'cubicBezTo':
            pts = []
            for _ in range(3):
                x, y = int(pts_all[pt_idx][0]), int(pts_all[pt_idx][1])
                pts.append((x, y))
                pt_idx += 1
            cmd_list.append((cmd_name, pts))
        elif cmd_name == 'close':
            cmd_list.append((cmd_name, []))

    freeforms.append({
        'name': name,
        'color': color,
        'off_pt': off_pt,
        'ext_pt': ext_pt,
        'path_w': path_w,
        'path_h': path_h,
        'cmds': cmd_list,
    })

print(f'Freeforms parsed: {len(freeforms)}')
for ff in freeforms:
    print(f"  {ff['name']}: color={ff['color']}, off={ff['off_pt']}, ext={ff['ext_pt']}, path={ff['path_w']}x{ff['path_h']}")

# --- 将Freeform路径转换到sheet坐标(pt) ---
def path_to_sheet_pts(freeform):
    off = freeform['off_pt']
    ext = freeform['ext_pt']
    pw = freeform['path_w']
    ph = freeform['path_h']

    def transform(px, py):
        x8 = off[0] + ext[0] * px / pw
        y8 = off[1] + ext[1] * py / ph
        return child8_to_sheet(x8, y8)

    return transform

# --- 文本框位置 (Excel COM精确位置, 单位pt) ---
TB11_LEFT = 235.55
TB11_TOP = 23.89
TB11_WIDTH = 393.00
TB11_HEIGHT = 74.30

TB12_LEFT = 231.80
TB12_TOP = 300.70
TB12_WIDTH = 308.91
TB12_HEIGHT = 21.02

# --- 计算所有形状的边界 (pt) ---
all_pts = []
for ff in freeforms:
    transform = path_to_sheet_pts(ff)
    for cmd_name, pts in ff['cmds']:
        for px, py in pts:
            sx, sy = transform(px, py)
            all_pts.append((sx, sy))

all_pts.extend([(TB11_LEFT, TB11_TOP), (TB11_LEFT + TB11_WIDTH, TB11_TOP + TB11_HEIGHT)])
all_pts.extend([(TB12_LEFT, TB12_TOP), (TB12_LEFT + TB12_WIDTH, TB12_TOP + TB12_HEIGHT)])

content_min_x = min(p[0] for p in all_pts)
content_min_y = min(p[1] for p in all_pts)
content_max_x = max(p[0] for p in all_pts)
content_max_y = max(p[1] for p in all_pts)
print(f'Content bbox: ({content_min_x:.1f}, {content_min_y:.1f}) to ({content_max_x:.1f}, {content_max_y:.1f})')

# 画布 = Chart 7 / 组合6 全范围 (深蓝背景 chartArea 的实际范围, Excel COM 实测)
# Chart 7: Left=219.43 Top=14.14 W=438.86 H=313.71
min_x, min_y = 219.43, 14.14
max_x, max_y = 219.43 + 438.86, 14.14 + 313.71

img_w = max_x - min_x
img_h = max_y - min_y

print(f'Image bounds: ({min_x:.1f}, {min_y:.1f}) to ({max_x:.1f}, {max_y:.1f}) pt')
print(f'Image size: {img_w:.1f} x {img_h:.1f} pt, aspect={img_w/img_h:.3f}')

def sheet_to_fig(sx, sy):
    """sheet坐标(pt, y向下) -> figure坐标(y向上), 需翻转y轴"""
    fx = (sx - min_x) / img_w
    fy = 1.0 - (sy - min_y) / img_h
    return fx, fy

# ============================================================
# 2. 画图
# ============================================================
FIG_W = 10          # inch
DPI = 150           # -> 1500px wide
# 字号换算(等比): figure逻辑宽=FIG_W*72 pt 对应 sheet画布 img_w pt
# 故 sheet 1pt -> matplotlib 逻辑pt = FIG_W*72/img_w
FONT_SCALE = FIG_W * 72 / img_w
FS_TITLE = 18 * FONT_SCALE      # Excel 18pt
FS_SUBTITLE = 12 * FONT_SCALE   # Excel 12pt
FS_NOTE = 8 * FONT_SCALE        # Excel 8pt

fig = plt.figure(figsize=(FIG_W, FIG_W * img_h / img_w), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# 画Freeform形状 (贝塞尔曲线)
for ff in freeforms:
    transform = path_to_sheet_pts(ff)
    path_cmds = []
    for cmd_name, pts in ff['cmds']:
        if cmd_name == 'moveTo':
            sx, sy = transform(*pts[0])
            fx, fy = sheet_to_fig(sx, sy)
            path_cmds.append((Path.MOVETO, (fx, fy)))
        elif cmd_name == 'lnTo':
            sx, sy = transform(*pts[0])
            fx, fy = sheet_to_fig(sx, sy)
            path_cmds.append((Path.LINETO, (fx, fy)))
        elif cmd_name == 'cubicBezTo':
            for px, py in pts:
                sx, sy = transform(px, py)
                fx, fy = sheet_to_fig(sx, sy)
                path_cmds.append((Path.CURVE4, (fx, fy)))
        elif cmd_name == 'close':
            path_cmds.append((Path.CLOSEPOLY, (0, 0)))

    codes = [c for c, _ in path_cmds]
    verts = [v for _, v in path_cmds]
    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=ff['color'],
                               edgecolor='none', zorder=3)
    ax.add_patch(patch)

# ---------------------------------------------------------------
# 引线: 每根 = 内端(扇区侧) -> 拐点 -> 圆点(外端); 颜色=对应扇区色
# 坐标从 chart7 复制图(_chart_clip_ChartObject.png)定量提取,
# 归一化于 chart7 画布(图像 y 向下); figure 坐标 y=1-ny
# ---------------------------------------------------------------
LEADERS = {
    'red':    ((0.745, 0.402), (0.784, 0.343), (0.930, 0.343)),
    'yellow': ((0.687, 0.787), (0.717, 0.849), (0.861, 0.849)),
    'cyan':   ((0.345, 0.798), (0.305, 0.862), (0.162, 0.862)),
    'blue':   ((0.411, 0.464), (0.381, 0.405), (0.190, 0.405)),
    'dblue':  ((0.318, 0.570), (0.280, 0.633), (0.136, 0.633)),
    'purple': ((0.479, 0.413), (0.448, 0.355), (0.304, 0.355)),
}
LEADER_COLORS = {
    'red': '#E74E69', 'yellow': '#F5C353', 'cyan': '#11A7AD',
    'blue': '#37A2DA', 'dblue': '#0070C0', 'purple': '#7030A0',
}
LEADER_LW = 0.6 * FONT_SCALE
DOT_MS = 3.6 * FONT_SCALE
for key, (inner, kneck, dot) in LEADERS.items():
    c = LEADER_COLORS[key]
    ax.plot([inner[0], kneck[0], dot[0]],
            [1-inner[1], 1-kneck[1], 1-dot[1]],
            color=c, lw=LEADER_LW, solid_capstyle='round',
            solid_joinstyle='miter', zorder=2.5)
    # 小圆点画在内端(靠近扇区那一端), 置于扇区之上一层以便可见
    ax.plot(inner[0], 1-inner[1], marker='o', ms=DOT_MS, color=c,
            markeredgewidth=0, zorder=4)

# 文本框11: 标题 + 副标题
tb11_fx, tb11_fy = sheet_to_fig(TB11_LEFT, TB11_TOP)
fig.text(tb11_fx, tb11_fy, '2021年各部门人数分布',
         fontsize=FS_TITLE, fontweight='bold', color=TXT,
         ha='left', va='top', family='Microsoft YaHei')

# 副标题在标题下方 (标题18pt行高约22pt + 文本框内边距)
sub_fy = 1.0 - (TB11_TOP + 26 - min_y) / img_h
fig.text(tb11_fx, sub_fy, '公司总人数1664，销售部人数最多451，占比29.2%',
         fontsize=FS_SUBTITLE, fontweight='bold', color=TXT,
         ha='left', va='top', family='Microsoft YaHei')

# 文本框12: 注释
tb12_fx, tb12_fy = sheet_to_fig(TB12_LEFT, TB12_TOP)
fig.text(tb12_fx, tb12_fy, '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01',
         fontsize=FS_NOTE, fontweight='bold', color=TXT_DIM,
         ha='left', va='top', family='Microsoft YaHei')

plt.savefig('20 南丁格尔（PPT）.png', dpi=DPI, facecolor=BG)
print("已生成 20 南丁格尔（PPT）.png")