import tkinter.ttk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from CoolProp.HumidAirProp import HAPropsSI
from psychrochart import PsychroChart
from tkinter import messagebox

win = Tk()
win.title("습공기 선도 어플")
win.geometry("1980x1080")
K = 273.15

dot_dic = {}
line_dic = {}

mybox = {'facecolor': 'w', 'edgecolor': 'w', 'boxstyle': 'round', 'alpha': 1}


def callback_plus():
    if EntVar1.get() == '' or EntVar4.get() == '':
        return
    if dot_dic.get(ent8.get()):
        messagebox.showerror("error", "이미 존재하는 이름입니다.")
        return
    dot_dic[ent8.get()] = [float(EntVar1.get()), float(EntVar4.get()) * 1000, float(EntVar3.get())] # float(EntVar3.get()을 추가
    listbox.insert(END, ent8.get())
    ax1.cla()
    ax1.axis([-10, 40, 0, 30])
    for key, val in dot_dic.items():
        ax1.scatter(val[0], val[1])
        ax1.text(val[0], val[1] - 1.5, 'DB : ' + str(val[0]) +  '℃\n' + 'RH : ' +str(val[2]) + '%', bbox=mybox) # val[1], str(val[2])로 변경
    ax1.axis('off')


def callback_minus():
    del dot_dic[listbox.get(listbox.curselection())]
    listbox.delete(listbox.curselection())
    ax1.cla()
    ax1.axis([-10, 40, 0, 30])
    for key, val in dot_dic.items():
        ax1.scatter(val[0], val[1])
        ax1.text(val[0], val[1] - 1.5 , 'DB : ' + str(val[0]) +  '℃\n' + 'RH : ' +str(val[2]) + '%' , bbox=mybox) # val[1], str(var[2])로 변경
    ax1.axis('off')


def callback_plus1():
    a = listbox.get(listbox.curselection()[0])
    b = listbox.get(listbox.curselection()[1])
    if len(listbox.curselection()) != 2:
        messagebox.showerror("error", "두개의 점을 선택해 주세요.")
        return
    if line_dic.get(a + "->" + b):
        messagebox.showerror("error", "이미 존재합니다.")
        return
    line_dic[a + "->" + b] = [a, b]
    listbox1.insert(END, a + "->" + b)
    ax2.cla()
    ax2.axis([-10, 40, 0, 30])
    for key, val in line_dic.items():
        ax2.plot([dot_dic[val[0]][0], dot_dic[val[1]][0]], [dot_dic[val[0]][1], dot_dic[val[1]][1]])
    ax2.axis('off')


def callback_minus1():
    del line_dic[listbox1.get(listbox1.curselection())]
    listbox1.delete(listbox1.curselection())
    ax2.cla()
    ax2.axis([-10, 40, 0, 30])
    for key, val in line_dic.items():
        ax2.plot([dot_dic[val[0]][0], dot_dic[val[1]][0]], [dot_dic[val[0]][1], dot_dic[val[1]][1]])
    ax2.axis('off')


custom_style = {
    "figure": {
        "title": "Psychrometric Chart (see level)",
        "x_label": "DRY-BULB TEMPERATURE, $°C$",
        "y_label": "HUMIDITY RATIO $w, g_w / kg_{da}$",
        "x_axis": {"color": [0.0, 0.0, 0.0], "linewidth": 1.5, "linestyle": "-"},
        "x_axis_labels": {"color": [0.0, 0.0, 0.0], "fontsize": 8},
        "x_axis_ticks": {"direction": "out", "color": [0.0, 0.0, 0.0]},
        "y_axis": {"color": [0.0, 0.0, 0.0], "linewidth": 1.5, "linestyle": "-"},
        "y_axis_labels": {"color": [0.0, 0.0, 0.0], "fontsize": 8},
        "y_axis_ticks": {"direction": "out", "color": [0.0, 0.0, 0.0]},
        "partial_axis": False,  # 외부 테두리
        "position": [0.025, 0.075, 0.925, 0.875]  # [0.025, 0.075, 0.925, 0.875]
    },
    "limits": {
        "range_temp_c": [-10, 40],
        "range_humidity_g_kg": [0, 30],
        "altitude_m": 0,  # 고도를 입력하세요
        "step_temp": 1.0
    },
    "saturation": {"color": [0.0, 0.0, 0.0], "linewidth": 2, "linestyle": "-"},
    "constant_rh": {"color": [0.0, 0.5, 0.5], "linewidth": 1, "linestyle": "-"},
    "constant_v": {"color": [0.0, 0.0, 0.0], "linewidth": 0.5, "linestyle": "-"},
    "constant_h": {"color": [0.0, 0.0, 0.0], "linewidth": 0.75, "linestyle": "-"},
    "constant_wet_temp": {"color": [0.0, 0.0, 0.0], "linewidth": 1, "linestyle": "--"},
    "constant_dry_temp": {"color": [0.0, 0.0, 0.0], "linewidth": 0.25, "linestyle": "-"},
    "constant_humidity": {"color": [0.0, 0.0, 0.0], "linewidth": 0.25, "linestyle": "-"},
    "chart_params": {
        "with_constant_rh": True,
        "constant_rh_curves": [10, 20, 30, 40, 50, 60, 70, 80, 90],
        "constant_rh_labels": [20, 40, 60, 80],
        "with_constant_v": True,
        "constant_v_step": 0.01,
        "range_vol_m3_kg": [0.75, 0.96],
        "with_constant_h": True,
        "constant_h_step": 10,
        "constant_h_labels": [0],
        "range_h": [10, 130],
        "with_constant_wet_temp": True,
        "constant_wet_temp_step": 1,
        "range_wet_temp": [-10, 35],
        "constant_wet_temp_labels": [0, 5, 10, 15, 20, 25, 30],
        "with_constant_dry_temp": True,
        "constant_temp_step": 1,

        "with_constant_humidity": True,
        "constant_humid_step": 0.5,

        "with_zones": False
    }
}

fig, ax = plt.subplots(figsize=(15, 9))

chart = PsychroChart(custom_style)
chart.plot(ax)

ax1 = ax.twinx()
ax1.axis([-10, 40, 0, 30])
ax2 = ax.twinx()
ax2.axis([-10, 40, 0, 30])
ax.yaxis.tick_right()

# # Append zones:
# zones_conf = {
#     "zones":[{
#             "zone_type": "dbt-rh",
#             "style": {"edgecolor": [1.0, 0.749, 0.0, 0.8],
#                       "facecolor": [1.0, 0.749, 0.0, 0.2],
#                       "linewidth": 2,
#                       "linestyle": "--"},
#             "points_x": [23, 28],
#             "points_y": [40, 60],
#             "label": "Summer"
#         },
#         {
#             "zone_type": "dbt-rh",
#             "style": {"edgecolor": [0.498, 0.624, 0.8],
#                       "facecolor": [0.498, 0.624, 1.0, 0.2],
#                       "linewidth": 2,
#                       "linestyle": "--"},
#             "points_x": [18, 23],
#             "points_y": [35, 55],
#             "label": "Winter"
#         }]}
# chart.append_zones(zones_conf)
#
# chart.plot(ax)

# # Add Vertical lines
# t_min, t_opt, t_max = 16, 23, 30
# chart.plot_vertical_dry_bulb_temp_line(
#     t_min, {"color": [0.0, 0.125, 0.376], "lw": 2, "ls": ':'},
#     '  TOO COLD ({}°C)'.format(t_min), ha='left', loc=0., fontsize=14)
# chart.plot_vertical_dry_bulb_temp_line(
#     t_opt, {"color": [0.475, 0.612, 0.075], "lw": 2, "ls": ':'})
# chart.plot_vertical_dry_bulb_temp_line(
#     t_max, {"color": [1.0, 0.0, 0.247], "lw": 2, "ls": ':'},
#     'TOO HOT ({}°C)  '.format(t_max), ha='right', loc=1,
#     reverse=True, fontsize=14)
#
# # Add labelled points and connections between points
# points = {'exterior': {'label': 'Exterior',
#                        'style': {'color': [0.855, 0.004, 0.278, 0.8],
#                                  'marker': 'X', 'markersize': 15},
#                        'xy': (31.06, 32.9)},
#           'exterior_estimated': {
#               'label': 'Estimated (Weather service)',
#               'style': {'color': [0.573, 0.106, 0.318, 0.5],
#                         'marker': 'x', 'markersize': 10},
#               'xy': (36.7, 25.0)},
#           'interior': {'label': 'Interior',
#                        'style': {'color': [0.592, 0.745, 0.051, 0.9],
#                                  'marker': 'o', 'markersize': 30},
#                        'xy': (29.42, 52.34)}}
# connectors = [{'start': 'exterior',
#                'end': 'exterior_estimated',
#                'label': 'Process 1',
#                'style': {'color': [0.573, 0.106, 0.318, 0.7],
#                          "linewidth": 2, "linestyle": "-."}},
#               {'start': 'exterior',
#                'end': 'interior',
#                'label': 'Process 2',
#                'style': {'color': [0.855, 0.145, 0.114, 0.8],
#                          "linewidth": 2, "linestyle": ":"}}]
# chart.plot_points_dbt_rh(points, connectors)

chart.plot_legend(markerscale=.7, frameon=True, fontsize=10, labelspacing=1.2)

canvas = FigureCanvasTkAgg(fig, master=win)
canvas.draw()
canvas.get_tk_widget().pack()
# 배경
# win.configure(bg='white')

# 파일메뉴
menu = Menu(win)
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="새파일")
menu_file.add_command(label="새 창")
menu_file.add_separator()
menu_file.add_command(label="파일 열기")
menu_file.add_separator()
menu_file.add_command(label="저장")
menu_file.add_separator()
menu_file.add_command(label="나가기", command=win.quit)  # 나가기 활성화
menu.add_cascade(label="파일", menu=menu_file)

win.config(menu=menu)

# 편집메뉴
menu.add_cascade(label="편집")

# 뷰 메뉴 추가
# menu_view = Menu(menu, tearoff=0)
# menu_view.add_checkbutton(label="미니맵으로 보기")
# menu_view.add_checkbutton(label="맥스맵으로 보기")
# menu.add_cascade(label="뷰", menu=menu_view)

# 도움말
menu_help = Menu(menu, tearoff=0)
menu_help.add_command(label="pdf 파일")
menu.add_cascade(label="도움말", menu=menu_help)

text_label = LabelFrame(win, text='', relief='solid', bd=1, pady=50)
text_label.pack()
text_label.place(x=0, y=35, width=263, height=940)

label = Label(win, text="JJH CHART", bg="white", relief="solid", bd=1, width=37, height=2)
label.place(x=0, y=0)

label = Label(win, text="Enter two parameters.", bg='skyblue', relief="solid", bd=1, width=33, height=2)
label.place(x=13, y=36)

label = Label(win, text="DB")
label.place(x=30, y=70)

label = Label(win, text="℃")
label.place(x=175, y=70)

label = Label(win, text="WB")
label.place(x=30, y=95)

label = Label(win, text="℃")
label.place(x=175, y=95)

label = Label(win, text="RH")
label.place(x=30, y=120)

label = Label(win, text="%")
label.place(x=175, y=120)

label = Label(win, text="x")
label.place(x=30, y=145)

label = Label(win, text="kg/kg dry air")
label.place(x=175, y=145)

label = Label(win, text="h")
label.place(x=30, y=170)

label = Label(win, text="kJ/kg dry air")
label.place(x=175, y=170)

label = Label(win, text="D.P")
label.place(x=30, y=195)

label = Label(win, text="℃")
label.place(x=175, y=195)

label = Label(win, text="Pw")
label.place(x=30, y=220)

label = Label(win, text="kPa")
label.place(x=175, y=220)


def my_upd():
    i = 0
    if (CheckVar1.get() == 1): i = i + 1
    if (CheckVar2.get() == 1): i = i + 1
    if (CheckVar3.get() == 1): i = i + 1
    if (CheckVar4.get() == 1): i = i + 1
    if (CheckVar5.get() == 1): i = i + 1
    if (CheckVar6.get() == 1): i = i + 1
    if (i >= 2):
        if (CheckVar1.get() != 1):
            checkbutton1.config(state='disabled')
            ent1.config(state='disabled')
        if (CheckVar2.get() != 1):
            checkbutton2.config(state='disabled')
            ent2.config(state='disabled')
        if (CheckVar3.get() != 1):
            checkbutton3.config(state='disabled')
            ent3.config(state='disabled')
        if (CheckVar4.get() != 1):
            checkbutton4.config(state='disabled')
            ent4.config(state='disabled')
        if (CheckVar5.get() != 1):
            checkbutton5.config(state='disabled')
            ent5.config(state='disabled')
        if (CheckVar6.get() != 1):
            checkbutton6.config(state='disabled')
            ent6.config(state='disabled')
    else:
        checkbutton1.config(state='normal')
        ent1.config(state='normal')
        checkbutton2.config(state='normal')
        ent2.config(state='normal')
        checkbutton3.config(state='normal')
        ent3.config(state='normal')
        checkbutton4.config(state='normal')
        ent4.config(state='normal')
        checkbutton5.config(state='normal')
        ent5.config(state='normal')
        checkbutton6.config(state='normal')
        ent6.config(state='normal')


CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()
CheckVar4 = IntVar()
CheckVar5 = IntVar()
CheckVar6 = IntVar()

checkbutton1 = Checkbutton(win, command=my_upd, variable=CheckVar1)
checkbutton2 = Checkbutton(win, command=my_upd, variable=CheckVar2)
checkbutton3 = Checkbutton(win, command=my_upd, variable=CheckVar3)
checkbutton4 = Checkbutton(win, command=my_upd, variable=CheckVar4)
checkbutton5 = Checkbutton(win, command=my_upd, variable=CheckVar5)
checkbutton6 = Checkbutton(win, command=my_upd, variable=CheckVar6)
checkbutton7 = Checkbutton(win)

checkbutton1.place(x=2, y=70)
checkbutton2.place(x=2, y=95)
checkbutton3.place(x=2, y=120)
checkbutton4.place(x=2, y=145)
checkbutton5.place(x=2, y=170)
checkbutton6.place(x=2, y=195)


def callback1(var):
    pressure = 101325
    if CheckVar1.get() == 1 and CheckVar2.get() == 1:
        ss = HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss - K, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar1.get() == 1 and CheckVar3.get() == 1:
        ss = HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100)
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar1.get() == 1 and CheckVar4.get() == 1:
        ss = HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) * 100
        ss = round(ss, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get()))
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar1.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H',
                       float(EntVar5.get()) * 1000) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = str(
            HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get()) * 1000) * 100)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get()) * 1000)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar1.get() == 1 and CheckVar6.get() == 1:
        ss = str(round(HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D',
                                 float(EntVar6.get()) + 273.15) - 273.15, 1))
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = str(round(HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D',
                                 float(EntVar6.get()) + 273.15) * 100, 1))
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = round(HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D',
                             float(EntVar6.get()) + 273.15) / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    elif CheckVar1.get() == 1 and CheckVar2.get() == 1:
        ss = HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')

    return


def callback2(var):
    pressure = 101325
    if CheckVar1.get() == 1 and CheckVar2.get() == 1:
        ss = HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'B', float(EntVar2.get()) + 273.15)
        ss = round(ss - K, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar3.get() == 1:
        ss = HAPropsSI('Tdb', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R',
                       float(EntVar3.get()) / 100) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('W', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R', float(EntVar3.get()) / 100)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R', float(EntVar3.get()) / 100)
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R', float(EntVar3.get()) / 100) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar4.get() == 1:
        ss = HAPropsSI('Tdb', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('R', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get()))
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get()))
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('Tdb', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get())) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar6.get() == 1:
        ss = str(HAPropsSI('T', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)) - K
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = str(HAPropsSI('RH', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15))
        ss = round(ss * 100, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = str(HAPropsSI('W', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15))
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = str(HAPropsSI('H', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15))
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
    return


def callback3(var):
    pressure = 101325
    if CheckVar1.get() == 1 and CheckVar3.get() == 1:
        ss = HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100)
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'RH', float(EntVar3.get()) / 100) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')
    elif CheckVar2.get() == 1 and CheckVar3.get() == 1:
        ss = HAPropsSI('Tdb', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R',
                       float(EntVar3.get()) / 100) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('W', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R', float(EntVar3.get()) / 100)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R', float(EntVar3.get()) / 100)
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'R', float(EntVar3.get()) / 100) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar3.get() == 1 and CheckVar4.get() == 1:
        ss = HAPropsSI('Tdb', 'R', float(EntVar3.get()) / 100, 'P', pressure, 'W', float(EntVar4.get())) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')

    elif CheckVar3.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('T', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('W', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('D', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar3.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K) - K
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('W', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss / 1000, 2)
        ent4.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    return


def callback4(var):
    pressure = 101325
    if CheckVar1.get() == 1 and CheckVar4.get() == 1:
        ss = HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) * 100
        ss = round(ss, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get()))
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar4.get() == 1:
        ss = HAPropsSI('Tdb', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('R', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get()))
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get()))
        ss = round(ss / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
        ss = HAPropsSI('D', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'W', float(EntVar4.get())) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar3.get() == 1 and CheckVar4.get() == 1:
        ss = HAPropsSI('Tdb', 'R', float(EntVar3.get()) / 100, 'P', pressure, 'W', float(EntVar4.get())) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')

    elif CheckVar4.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('T', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('D', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar4.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    return


def callback5(var):
    pressure = 101325
    if CheckVar1.get() == 1 and CheckVar5.get() == 1:
        ss = str(round(HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H',
                                 float(EntVar5.get()) * 1000) - 273.15, 1))
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get()) * 1000) * 100
        ss = round(ss, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get()) * 1000)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('D', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('Tdb', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'H', float(EntVar5.get())) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')

    elif CheckVar3.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('T', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('W', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('D', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar4.get() == 1 and CheckVar5.get() == 1:
        ss = HAPropsSI('T', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('D', 'W', float(EntVar4.get()), 'P', pressure, 'H', float(EntVar5.get()) * 1000) - K
        ss = round(ss, 1)
        ent6.config(state='normal')
        ent6.delete(0, END)
        ent6.insert(0, ss)
        ent6.config(state='disable')

    elif CheckVar4.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    elif CheckVar5.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss * 100, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')

    return


def callback6(var):
    pressure = 101325
    if CheckVar1.get() == 1 and CheckVar6.get() == 1:
        ss = round(HAPropsSI('B', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D',
                             float(EntVar6.get()) + 273.15) - 273.15, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = str(round(HAPropsSI('RH', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D',
                                 float(EntVar6.get()) + 273.15) * 100, 1))
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = round(HAPropsSI('H', 'T', float(EntVar1.get()) + 273.15, 'P', pressure, 'D',
                             float(EntVar6.get()) + 273.15) / 1000, 1)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    elif CheckVar2.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15) - K
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('RH', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)
        ss = round(ss * 100, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    elif CheckVar3.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('B', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K) - K
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('W', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')
        ss = HAPropsSI('H', 'RH', float(EntVar3.get()) / 100, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss / 1000, 2)
        ent4.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')
    elif CheckVar4.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss * 100, 1)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('H', 'W', float(EntVar4.get()), 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss / 1000, 2)
        ent5.config(state='normal')
        ent5.delete(0, END)
        ent5.insert(0, ss)
        ent5.config(state='disable')

    elif CheckVar5.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss * 100, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')

    elif CheckVar5.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
    elif CheckVar5.get() == 1 and CheckVar6.get() == 1:
        ss = HAPropsSI('T', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent1.config(state='normal')
        ent1.delete(0, END)
        ent1.insert(0, ss)
        ent1.config(state='disable')
        ss = HAPropsSI('B', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K) - 273.15
        ss = round(ss, 1)
        ent2.config(state='normal')
        ent2.delete(0, END)
        ent2.insert(0, ss)
        ent2.config(state='disable')
        ss = HAPropsSI('RH', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss * 100, 2)
        ent3.config(state='normal')
        ent3.delete(0, END)
        ent3.insert(0, ss)
        ent3.config(state='disable')
        ss = HAPropsSI('W', 'H', float(EntVar5.get()) * 1000, 'P', pressure, 'D', float(EntVar6.get()) + K)
        ss = round(ss, 4)
        ent4.config(state='normal')
        ent4.delete(0, END)
        ent4.insert(0, ss)
        ent4.config(state='disable')

    return


# def callback7(var):
#     ss = Psychrometry.Psat_water(CheckVar1.get())
#     ent7.config(state='normal')
#     ent7.delete(0, END)
#     ent7.insert(0, ss)
#     ent7.config(state='disable')
#     return


EntVar1 = StringVar()
EntVar2 = StringVar()
EntVar3 = StringVar()
EntVar4 = StringVar()
EntVar5 = StringVar()
EntVar6 = StringVar()
EntVar7 = StringVar()

EntVar1.trace("w", lambda name, index, mode, EntVar1=EntVar1: callback1(EntVar1))
EntVar2.trace("w", lambda name, index, mode, EntVar2=EntVar2: callback2(EntVar2))
EntVar3.trace("w", lambda name, index, mode, EntVar3=EntVar3: callback3(EntVar3))
EntVar4.trace("w", lambda name, index, mode, EntVar4=EntVar4: callback4(EntVar4))
EntVar5.trace("w", lambda name, index, mode, EntVar5=EntVar5: callback5(EntVar5))
EntVar6.trace("w", lambda name, index, mode, EntVar6=EntVar6: callback6(EntVar6))
EntVar7.trace("w", lambda name, index, mode, EntVar7=EntVar7: callback7(EntVar7))

ent1 = Entry(win, textvariable=EntVar1)
ent1.config(width=15)
ent1.place(x=60, y=72)

ent2 = Entry(win, textvariable=EntVar2)
ent2.config(width=15)
ent2.place(x=60, y=95)

ent3 = Entry(win, textvariable=EntVar3)
ent3.config(width=15)
ent3.place(x=60, y=120)

ent4 = Entry(win, textvariable=EntVar4)
ent4.config(width=15)
ent4.place(x=60, y=145)

ent5 = Entry(win, textvariable=EntVar5)
ent5.config(width=15)
ent5.place(x=60, y=170)

ent6 = Entry(win, textvariable=EntVar6)
ent6.config(width=15)
ent6.place(x=60, y=195)

ent7 = Entry(win, textvariable=EntVar7)
ent7.config(width=15)
ent7.place(x=60, y=220)

ent1.config(state='disable')
ent2.config(state='disable')
ent3.config(state='disable')
ent4.config(state='disable')
ent5.config(state='disable')
ent6.config(state='disable')
ent7.config(state='disable')

text_label = LabelFrame(win, text='Points', relief='solid', bd=1, pady=30)
text_label.pack()
text_label.place(x=5, y=250, width=245, height=250)

label = Label(win, text="Name")
label.place(x=15, y=270)

ent8 = Entry(win)
ent8.config(width=15)
ent8.place(x=75, y=270)

btn1 = Button(win, text="+", width=2, command=callback_plus)
btn1.pack()
btn1.place(x=15, y=300)

btn2 = Button(win, text="-", width=2, command=callback_minus)
btn2.pack()
btn2.place(x=40, y=300)

btn3 = Button(win, text="edit", width=3)
btn3.pack()
btn3.place(x=65, y=300)

text_label = LabelFrame(win, text='', relief='solid', bd=1, pady=50)
text_label.pack()
text_label.place(x=15, y=340, width=200, height=150)

frame = Frame(win, height=8, width=26)

scrollbar = Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

listbox = Listbox(frame, height=8, width=24, yscrollcommand=scrollbar.set)

scrollbar["command"] = listbox.yview

listbox.config(selectmode="multiple")

listbox.pack(side="left")

listbox.config(height=8)

frame.pack()

frame.place(x=20, y=350)

checkbutton8 = Checkbutton(win)
checkbutton8.place(x=220, y=360)

radio1 = Radiobutton(win)
radio1.place(x=220, y=345)

text_label = LabelFrame(win, text='Lines', relief='solid', bd=1, pady=30)
text_label.pack()
text_label.place(x=5, y=500, width=245, height=250)

btn4 = Button(win, text="+", width=2, command=callback_plus1)
btn4.pack()
btn4.place(x=15, y=530)

btn5 = Button(win, text="-", width=2, command=callback_minus1)
btn5.pack()
btn5.place(x=40, y=530)

text_label = LabelFrame(win, text='', relief='solid', bd=1, pady=50)
text_label.pack()
text_label.place(x=15, y=570, width=200, height=150)

frame1 = Frame(win, height=8, width=26)

scrollbar1 = Scrollbar(frame1)
scrollbar1.pack(side="right", fill="y")

listbox1 = Listbox(frame1, height=8, width=24, yscrollcommand=scrollbar1.set)

scrollbar1["command"] = listbox1.yview

listbox1.config(selectmode="multiple")

listbox1.pack(side="left")

listbox1.config(height=8)

frame1.pack()

frame1.place(x=20, y=580)

checkbutton8 = Checkbutton(win)
checkbutton8.place(x=220, y=590)

a = ["LINE", "POINT-DB", "POINT-WB", "POINT-x", "POINT-h", "POINT-SHF", "POINT-v"]  # 콤보 박스에 나타낼 항목 리스트
combobox = tkinter.ttk.Combobox(win)  # root라는 창에 콤보박스 생성
combobox.config(height=7, width=15)  # 높이 설정
combobox.config(values=a)  # 나타낼 항목 리스트(a) 설정
combobox.config(state="readonly")  # 콤보 박스에 사용자가 직접 입력 불가
combobox.set("LINE")  # 맨 처음 나타낼 값 설정
combobox.pack()
combobox.place(x=70, y=532)

label = Label(win, text="/")
label.place(x=225, y=570)

label = Label(win, text="Item")
label.place(x=15, y=770)

a = ["DB", "WB", "x", "h", "SHF", "v"]  # 콤보 박스에 나타낼 항목 리스트
combobox = tkinter.ttk.Combobox(win)  # root라는 창에 콤보박스 생성
combobox.config(height=7, width=15)  # 높이 설정
combobox.config(values=a)  # 나타낼 항목 리스트(a) 설정
combobox.config(state="readonly")  # 콤보 박스에 사용자가 직접 입력 불가
combobox.set("DB")  # 맨 처음 나타낼 값 설정
combobox.pack()
combobox.place(x=65, y=770)

label = Label(win, text="Value")
label.place(x=15, y=800)

spin = Spinbox(win, from_=0, to=100, width=16)
spin.place(x=65, y=800)

btn6 = Button(win, text="Add intersection", width=33, height=2)
btn6.place(x=13, y=830)

label = Label(win,
              text="△ Finds and adds the intersection point of the currently selected line or point and the entered reference value.",
              wraplength=200, bg='skyblue', relief="solid", bd=1, width=33, height=4)
label.place(x=13, y=880)
plt.scatter(EntVar1.get(), EntVar3.get())
win.mainloop()