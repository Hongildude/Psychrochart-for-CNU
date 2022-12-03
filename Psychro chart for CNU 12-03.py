import tkinter.ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CoolProp.HumidAirProp import HAPropsSI
from psychrochart import PsychroChart
from tkinter import messagebox

win = Tk()
win.title("습공기 선도 프로그램")
win.config(bg="white")
win.maxsize(1790,1010)

width,height=1780,1000
v_dim= str(width)+'x'+str(height)
win.geometry(v_dim)


def my_resize(condition):
    global width, height
    if(condition=='increase'):
         width=width+2
         height=height+2
    elif(condition=='decrease'):
        width=width-2
        height=height-2

    H=str(width)+'x'+str(height)
    win.geometry(H)


win.bind("<a>", lambda event: my_resize('increase'))
win.bind("<s>", lambda event: my_resize('decrease'))

K = 273.15
pressure = 101325  # Pa / 압력을 입력받는다.
rho = 1.2
g = 9.8
altitude_m = 0
cal_pressure = rho * g * altitude_m
pressure = 101325 - cal_pressure
dot_dic = {}
line_dic = {}
state_dot_check = [1, 1, 0, 0]

mybox = {'facecolor': 'w', 'edgecolor': 'w', 'boxstyle': 'round', 'alpha': 1}



def callback_plus():
    if EntVar1.get() == '' or EntVar4.get() == '':
        return
    if dot_dic.get(ent8.get()):
        messagebox.showerror("error", "이미 존재하는 이름입니다.")
        return
    dot_dic[ent8.get()] = [float(EntVar1.get()), float(EntVar3.get()), float(EntVar4.get()) * 1000,
                           float(EntVar5.get())]
    listbox.insert(END, ent8.get())

    ax1.clear()
    ax1.axis([custom_style['limits']['range_temp_c'][0], custom_style['limits']['range_temp_c'][1],
              0, custom_style['limits']['range_humidity_g_kg'][1]])
    for key, val in dot_dic.items():
        ax1.scatter(val[0], val[2])
        dot_info_str = ""
        if state_dot_check[0]:
            dot_info_str += 'DB : ' + str(val[0]) + '℃\n'
        if state_dot_check[1]:
            dot_info_str += 'RH : ' + str(val[1]) + '%'
        if state_dot_check[2]:
            dot_info_str += '\nw : %.4f' %(val[2]/1000) + 'kg/kg'
        if state_dot_check[3]:
            dot_info_str += '\nh : %.2f'%val[3] + 'kJ/kg'
        ax1.text(val[0] + 0.5, val[2]  + 0.5,  dot_info_str, bbox=mybox)  # val[1], str(val[2])로 변경
    ax1.axis('off')
    my_resize('decrease')
    after(1000)
    my_resize('increase')


def callback_minus():
    del dot_dic[listbox.get(listbox.curselection())]
    listbox.delete(listbox.curselection())
    ax1.cla()

    ax1.axis([custom_style['limits']['range_temp_c'][0], custom_style['limits']['range_temp_c'][1],
              0, custom_style['limits']['range_humidity_g_kg'][1]])
    for key, val in dot_dic.items():
        ax1.scatter(val[0], val[2])
        dot_info_str = ""
        if state_dot_check[0]:
            dot_info_str += 'DB : ' + str(val[0]) + '℃\n'
        if state_dot_check[1]:
            dot_info_str += 'RH : ' + str(val[1]) + '%'
        if state_dot_check[2]:
            dot_info_str += '\nw : %.6f' %(val[2]/1000) + 'kg/kg'
        if state_dot_check[3]:
            dot_info_str += '\nh : %.2f'%val[3] + 'kJ/kg'
        ax1.text(val[0] + 0.5, val[2] + 0.5, dot_info_str, bbox=mybox)  # val[1], str(val[2])로 변경
    ax1.axis('off')
    my_resize('decrease')
    after(1000)
    my_resize('increase')


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
    ax2.axis([custom_style['limits']['range_temp_c'][0], custom_style['limits']['range_temp_c'][1],
              0, custom_style['limits']['range_humidity_g_kg'][1]])
    for key, val in line_dic.items():
        ax2.plot([dot_dic[val[0]][0], dot_dic[val[1]][0]], [dot_dic[val[0]][2], dot_dic[val[1]][2]], linewidth = 3)
    ax2.axis('off')
    my_resize('decrease')
    after(1000)
    my_resize('increase')


def callback_minus1():
    del line_dic[listbox1.get(listbox1.curselection())]
    listbox1.delete(listbox1.curselection())
    ax2.cla()
    ax2.axis([custom_style['limits']['range_temp_c'][0], custom_style['limits']['range_temp_c'][1],
              0, custom_style['limits']['range_humidity_g_kg'][1]])
    for key, val in line_dic.items():
        ax2.plot([dot_dic[val[0]][0], dot_dic[val[1]][0]], [dot_dic[val[0]][2], dot_dic[val[1]][2]], linewidth = 3)
    ax2.axis('off')
    my_resize('decrease')
    after(1000)
    my_resize('increase')



CheckVar1_tool = IntVar()
CheckVar2_tool = IntVar()


def my_upd_tool1(ent1_tool, ent2_tool, checkbutton1_tool, checkbutton2_tool):
    checkbutton1_tool.select()
    checkbutton2_tool.deselect()
    ent2_tool.config(state='disabled')
    ent1_tool.config(state='normal')

    return


def my_upd_tool2(ent1_tool, ent2_tool, checkbutton1_tool, checkbutton2_tool):
    checkbutton2_tool.select()
    checkbutton1_tool.deselect()
    ent1_tool.config(state='disabled')
    ent2_tool.config(state='normal')
    return


def tool_print():
    def callack_tool_save():
        save_route_str = EntVar1_tool.get()
        save_route_str += '.png'
        plt.savefig(save_route_str)
        messagebox.showinfo("저장 완료", "이미지가 저장되었습니다.")
        return

    EntVar1_tool = StringVar()
    new_win = Toplevel(win)
    new_win.title("이미지 저장")
    new_win.geometry("400x150")
    label_tool = Label(new_win, text="저장할 이미지 이름 : ",
                       justify="left")
    label_tool.place(x=30, y=50)
    ent1_tool = Entry(new_win, textvariable=EntVar1_tool)
    ent1_tool.config(width=25)
    ent1_tool.place(x=160, y=50)
    label_tool = Label(new_win, text=".png",
                       justify="left")
    label_tool.place(x=320, y=50)
    btn1_tool = Button(new_win, text="저장", width=6, command=callack_tool_save)
    btn1_tool.pack()
    btn1_tool.place(x=170, y=100)


def tool_option():
    def callback_tool_confirm():

        def callback_tool_confirm_confirm():
            custom_style['limits']['altitude_m'] = int(float(EntVar1_tool.get()))
            custom_style['limits']['range_temp_c'][0] = int(EntVar3_tool.get())
            custom_style['limits']['range_temp_c'][1] = int(EntVar4_tool.get())
            custom_style['limits']['range_humidity_g_kg'][1] = int(EntVar5_tool.get())
            custom_style['chart_params']['with_constant_dry_temp'] = int(CheckVar3_tool.get())
            custom_style['chart_params']['with_constant_rh'] = int(CheckVar4_tool.get())
            custom_style['chart_params']['with_constant_h'] = int(CheckVar5_tool.get())
            custom_style['chart_params']['with_constant_wet_temp'] = int(CheckVar6_tool.get())
            custom_style['chart_params']['with_constant_humidity'] = int(CheckVar7_tool.get())
            custom_style['chart_params']['with_constant_v'] = int(CheckVar9_tool.get())
            state_dot_check[0] = CheckVar12_tool.get()
            state_dot_check[1] = CheckVar13_tool.get()
            state_dot_check[2] = CheckVar14_tool.get()
            state_dot_check[3] = CheckVar15_tool.get()
            listbox.delete(0, END)
            listbox1.delete(0, END)
            ax.cla()
            ax1.cla()
            ax2.cla()
            plt.cla()
            ax1.axis('off')
            ax2.axis('off')
            chart = PsychroChart(custom_style)
            chart.plot(ax)
            line_dic.clear()
            dot_dic.clear()

            very_win.destroy()

        def callback_tool_confirm_cancle():
            very_win.destroy()

        def disable_event():
            pass

        new_win.destroy()
        very_win = Toplevel(win)
        very_win.geometry("250x100")
        label_tool = Label(very_win, text="고도값 변화로 기존 데이터가 삭제됩니다.\
        \n삭제할까요?", height=4, justify="left")
        label_tool.place(x=10, y=1)
        very_win.protocol("WM_DELETE_WINDOW", disable_event)
        btn1_tool = Button(very_win, text="확인", width=3, command=callback_tool_confirm_confirm)
        btn1_tool.pack()
        btn1_tool.place(x=75, y=50)
        btn1_tool = Button(very_win, text="취소", width=3, command=callback_tool_confirm_cancle)
        btn1_tool.pack()
        btn1_tool.place(x=125, y=50)
        return

    def callback1_tool(var):
        if CheckVar1_tool.get() == 1:
            ent2_tool.config(state='normal')
            ent2_tool.delete(0, END)
            ent2_tool.insert(0, (101325 - rho * g * int(var.get())) / 1000)
            ent2_tool.config(state='disable')
            if int(var.get()) < 0 or int(var.get()) > 3000:
                messagebox.showerror("error", "범위를 벗어났습니다(0~3000)", parent=new_win)
                ent1_tool.delete(0, END)
                ent1_tool.insert(0, round(altitude_m, 0))
                ent2_tool.config(state='normal')
                ent2_tool.delete(0, END)
                ent2_tool.insert(0, (101325 - rho * g * altitude_m) / 1000)
                ent2_tool.config(state='disable')

        return

    def callback2_tool(var):
        if CheckVar2_tool.get() == 1:
            ent1_tool.config(state='normal')
            ent1_tool.delete(0, END)
            ent1_tool.insert(0, round(float(101325 - float(var.get()) * 1000) / rho /g , 0))
            ent1_tool.config(state='disable')
            if float(var.get()) > 101.325:
                messagebox.showerror("error", "범위를 벗어났습니다(66.045~101.325)", parent=new_win)
                ent2_tool.delete(0, END)
                ent2_tool.insert(0, 66.045)
                ent1_tool.config(state='normal')
                ent1_tool.delete(0, END)
                ent1_tool.insert(0, float((101325 - pressure) / rho) / g)
                ent1_tool.config(state='disable')
        return

    def callback3_tool(var):
        if int(var.get()) < -40 or int(var.get()) >= int(EntVar4_tool.get()):
            messagebox.showerror("error", "범위를 벗어났습니다(-40~" + str(int(EntVar4_tool.get()) - 1) + ")", parent=new_win)
            ent3_tool.delete(0, END)
            ent3_tool.insert(0, -40)
        return

    def callback4_tool(var):
        if int(var.get()) > 60 or int(var.get()) <= int(EntVar3_tool.get()):
            messagebox.showerror("error", "범위를 벗어났습니다(" + str(int(EntVar3_tool.get()) + 1) + "~60)", parent=new_win)
            ent4_tool.delete(0, END)
            ent4_tool.insert(0, 60)
        return

    def callback5_tool(var):
        if int(var.get()) > 60 or int(var.get()) <= 0:
            messagebox.showerror("error", "범위를 벗어났습니다(1~60)", parent=new_win)
            ent5_tool.delete(0, END)
            ent5_tool.insert(0, 60)
        return

    EntVar1_tool = StringVar()
    EntVar2_tool = DoubleVar()
    EntVar3_tool = StringVar()
    EntVar4_tool = StringVar()
    EntVar5_tool = StringVar()
    CheckVar1_tool = IntVar()
    CheckVar2_tool = IntVar()
    CheckVar3_tool = IntVar()
    CheckVar4_tool = IntVar()
    CheckVar5_tool = IntVar()
    CheckVar6_tool = IntVar()
    CheckVar7_tool = IntVar()
    CheckVar8_tool = IntVar()
    CheckVar9_tool = IntVar()
    CheckVar10_tool = IntVar()
    CheckVar11_tool = IntVar()
    CheckVar12_tool = IntVar()
    CheckVar13_tool = IntVar()
    CheckVar14_tool = IntVar()
    CheckVar15_tool = IntVar()

    new_win = Toplevel(win)
    new_win.title("도구 - 옵션")
    new_win.geometry("450x350")
    label_tool = Label(new_win, text=" ▲    해      발:           0 ~ 3000 m\n\
        건구온도:        -10 ~    50 ℃\n\
        절대습도:           0 ~    60 g/kg dry air.", bg='orange', relief="solid", height=4,
                       justify="left", width=40)
    label_tool.place(x=10, y=140)
    ent1_tool = Entry(new_win, textvariable=EntVar1_tool)
    ent1_tool.config(width=15)
    ent1_tool.place(x=100, y=10)
    ent1_tool.delete(0, END)
    ent1_tool.insert(0, round(custom_style['limits']['altitude_m'], 0))
    frame_tool = Frame(new_win, width=300, height=300)

    frame_tool.pack()

    text_label = LabelFrame(frame_tool, text='선도 표시 항목', relief='solid', bd=1, pady=30)
    text_label.pack()
    text_label.place(x=0, y=0, width=135, height=205)

    checkbutton3_tool = Checkbutton(frame_tool, variable=CheckVar3_tool)
    checkbutton3_tool.place(x=10, y=15)
    checkbutton4_tool = Checkbutton(frame_tool, variable=CheckVar4_tool)
    checkbutton4_tool.place(x=10, y=35)
    checkbutton5_tool = Checkbutton(frame_tool, variable=CheckVar5_tool)
    checkbutton5_tool.place(x=10, y=55)
    checkbutton6_tool = Checkbutton(frame_tool, variable=CheckVar6_tool)
    checkbutton6_tool.place(x=10, y=75)
    checkbutton7_tool = Checkbutton(frame_tool, variable=CheckVar7_tool)
    checkbutton7_tool.place(x=10, y=95)
    checkbutton8_tool = Checkbutton(frame_tool, variable=CheckVar8_tool)
    checkbutton8_tool.place(x=10, y=115)
    checkbutton9_tool = Checkbutton(frame_tool, variable=CheckVar9_tool)
    checkbutton9_tool.place(x=10, y=135)
    checkbutton10_tool = Checkbutton(frame_tool, variable=CheckVar10_tool)
    checkbutton10_tool.place(x=10, y=155)
    checkbutton11_tool = Checkbutton(frame_tool, variable=CheckVar11_tool)
    checkbutton11_tool.place(x=10, y=175)

    label = Label(frame_tool, text="건구온도")
    label.place(x=30, y=15)
    label = Label(frame_tool, text="상대습도")
    label.place(x=30, y=35)
    label = Label(frame_tool, text="엔탈피")
    label.place(x=30, y=55)
    label = Label(frame_tool, text="습구온도")
    label.place(x=30, y=75)
    label = Label(frame_tool, text="절대습도")
    label.place(x=30, y=95)
    label = Label(frame_tool, text="수증기분압")
    label.place(x=30, y=115)
    label = Label(frame_tool, text="비체적")
    label.place(x=30, y=135)
    label = Label(frame_tool, text="열수분비/현열비")
    label.place(x=30, y=155)
    label = Label(frame_tool, text="기준점-현열비선")
    label.place(x=30, y=175)

    frame_tool1 = Frame(new_win, width=500, height=300)

    frame_tool1.pack()
    text_label = LabelFrame(frame_tool1, text='상태 점 표시 항목', relief='solid', bd=1, pady=30)
    text_label.pack()
    text_label.place(x=0, y=0, width=425, height=70)

    checkbutton12_tool = Checkbutton(frame_tool1, variable=CheckVar12_tool)
    checkbutton12_tool.place(x=20, y=25)
    checkbutton13_tool = Checkbutton(frame_tool1, variable=CheckVar13_tool)
    checkbutton13_tool.place(x=110, y=25)
    checkbutton14_tool = Checkbutton(frame_tool1, variable=CheckVar14_tool)
    checkbutton14_tool.place(x=200, y=25)
    checkbutton15_tool = Checkbutton(frame_tool1, variable=CheckVar15_tool)
    checkbutton15_tool.place(x=290, y=25)
    label = Label(frame_tool1, text="건구온도")
    label.place(x=40, y=25)
    label = Label(frame_tool1, text="상대습도")
    label.place(x=130, y=25)
    label = Label(frame_tool1, text="절대습도")
    label.place(x=220, y=25)
    label = Label(frame_tool1, text="엔탈피")
    label.place(x=310, y=25)
    if custom_style['chart_params']['with_constant_dry_temp']:
        checkbutton3_tool.select()
    if custom_style['chart_params']['with_constant_rh']:
        checkbutton4_tool.select()
    if custom_style['chart_params']['with_constant_h']:
        checkbutton5_tool.select()
    if custom_style['chart_params']['with_constant_wet_temp']:
        checkbutton6_tool.select()
    if custom_style['chart_params']['with_constant_humidity']:
        checkbutton7_tool.select()
    if custom_style['chart_params']['with_constant_v']:
        checkbutton9_tool.select()
    if state_dot_check[0]:
        checkbutton12_tool.select()
    if state_dot_check[1]:
        checkbutton13_tool.select()
    if state_dot_check[2]:
        checkbutton14_tool.select()
    if state_dot_check[3]:
        checkbutton15_tool.select()

    frame_tool1.place(x=10, y=210)
    frame_tool.place(x=300, y=0)

    ent2_tool = Spinbox(new_win, from_=66.045, to=101.325, increment=0.5, textvariable=EntVar2_tool)
    ent2_tool.config(width=13)
    ent2_tool.place(x=100, y=35)
    ent2_tool.delete(0, END)
    ent2_tool.insert(0, (101325 - rho * g * custom_style['limits']['altitude_m']) / 1000)

    ent3_tool = Entry(new_win, textvariable=EntVar3_tool)
    ent3_tool.config(width=5)
    ent3_tool.place(x=100, y=60)
    ent3_tool.delete(0, END)
    ent3_tool.insert(0, custom_style['limits']['range_temp_c'][0])

    ent4_tool = Entry(new_win, textvariable=EntVar4_tool)
    ent4_tool.config(width=5)
    ent4_tool.place(x=171, y=60)
    ent4_tool.delete(0, END)
    ent4_tool.insert(0, custom_style['limits']['range_temp_c'][1])

    ent5_tool = Entry(new_win, textvariable=EntVar5_tool)
    ent5_tool.config(width=5)
    ent5_tool.place(x=171, y=85)
    ent5_tool.delete(0, END)
    ent5_tool.insert(0, custom_style['limits']['range_humidity_g_kg'][1])

    ent1_tool.config(state='disabled')
    ent2_tool.config(state='disabled')

    label = Label(new_win, text="해발")
    label.place(x=20, y=10)
    label = Label(new_win, text="건구온도")
    label.place(x=20, y=60)
    label = Label(new_win, text="절대습도")
    label.place(x=20, y=85)
    label = Label(new_win, text="m")
    label.place(x=210, y=10)
    label = Label(new_win, text="kPa")
    label.place(x=210, y=35)
    label = Label(new_win, text="°C")
    label.place(x=210, y=60)
    label = Label(new_win, text="g/kg dry air")
    label.place(x=210, y=85)
    label = Label(new_win, text="0      ~")
    label.place(x=113, y=85)
    label = Label(new_win, text="~")
    label.place(x=145, y=60)

    btn1_tool = Button(new_win, text="확인", width=6, command=callback_tool_confirm)
    btn1_tool.pack()
    btn1_tool.place(x=200, y=300)

    checkbutton1_tool = Checkbutton(new_win, variable=CheckVar1_tool)
    checkbutton2_tool = Checkbutton(new_win, variable=CheckVar2_tool)

    checkbutton1_tool.place(x=70, y=8)
    checkbutton2_tool.place(x=70, y=32)
    checkbutton1_tool.config(command=lambda: my_upd_tool1(ent1_tool, ent2_tool, checkbutton1_tool, checkbutton2_tool))
    checkbutton2_tool.config(command=lambda: my_upd_tool2(ent1_tool, ent2_tool, checkbutton1_tool, checkbutton2_tool))

    EntVar1_tool.trace("w", lambda name, index, mode, EntVar1_tool=EntVar1_tool: callback1_tool(EntVar1_tool))
    EntVar2_tool.trace("w", lambda name, index, mode, EntVar2_tool=EntVar2_tool: callback2_tool(EntVar2_tool))
    EntVar3_tool.trace("w", lambda name, index, mode, EntVar3_tool=EntVar3_tool: callback3_tool(EntVar3_tool))
    EntVar4_tool.trace("w", lambda name, index, mode, EntVar4_tool=EntVar4_tool: callback4_tool(EntVar4_tool))
    EntVar5_tool.trace("w", lambda name, index, mode, EntVar5_tool=EntVar5_tool: callback5_tool(EntVar5_tool))

    checkbutton2_tool.deselect()
    checkbutton1_tool.deselect()


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
        "range_temp_c": [-10, 50],  # x축 건구온도범위
        "range_humidity_g_kg": [0, 30],  # y축 절대습도범위
        "altitude_m": 0,  # 고도를 입력하세요 # 해발 입력받는다.
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
        "with_constant_rh": True,  # 상대습도
        "constant_rh_curves": [10, 20, 30, 40, 50, 60, 70, 80, 90],
        "constant_rh_labels": [20, 40, 60, 80],
        "with_constant_v": True,  # 비체적
        "constant_v_step": 0.01,
        "range_vol_m3_kg": [0.75, 0.96],
        "with_constant_h": True,  # 엔탈피
        "constant_h_step": 10,
        "constant_h_labels": [0],
        "range_h": [10, 130],
        "with_constant_wet_temp": True,  # 습구온도
        "constant_wet_temp_step": 1,
        "range_wet_temp": [-10, 35],
        "constant_wet_temp_labels": [0, 5, 10, 15, 20, 25, 30],
        "with_constant_dry_temp": True,  # 건구온도
        "constant_temp_step": 1,

        "with_constant_humidity": True,  # 절대습도
        "constant_humid_step": 0.5,

        "with_zones": False
    }
}

fig, ax = plt.subplots(figsize=(15, 9))  # 피드백 --> 나중에 수정
chart = PsychroChart(custom_style)
chart.plot(ax)

ax.yaxis.tick_right()
canvas = FigureCanvasTkAgg(fig, master=win)
canvas.draw()
canvas.get_tk_widget().pack()
ax1 = ax._make_twin_axes()
ax2 = ax._make_twin_axes()
ax1.axis([custom_style['limits']['range_temp_c'][0], custom_style['limits']['range_temp_c'][1],
          0, custom_style['limits']['range_humidity_g_kg'][1]])
ax2.axis([custom_style['limits']['range_temp_c'][0], custom_style['limits']['range_temp_c'][1],
          0, custom_style['limits']['range_humidity_g_kg'][1]])

ax1.axis('off')
ax2.axis('off')

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

# 도구메뉴
menu_tool = Menu(menu, tearoff=0)
menu_tool.add_command(label="옵션", command=tool_option)
menu_tool.add_command(label="이미지 저장", command=tool_print)
menu.add_cascade(label="도구", menu=menu_tool)

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

label = Label(win, text="Psychrometry CHART for CNU", bg="white", relief="solid", bd=1, width=37, height=2)
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

label = Label(win, text="w")
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
    pressure = 101325 - rho * g * custom_style['limits']['altitude_m']
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
    pressure = 101325 - rho * g * custom_style['limits']['altitude_m']
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
        ss = str(
            HAPropsSI('T', 'B', float(EntVar2.get()) + 273.15, 'P', pressure, 'D', float(EntVar6.get()) + 273.15)) - K
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
    pressure = 101325 -rho*g*custom_style['limits']['altitude_m']
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
    pressure = 101325 -rho*g*custom_style['limits']['altitude_m']
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
    pressure = 101325 -rho*g*custom_style['limits']['altitude_m']
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
    pressure = 101325 -rho*g*custom_style['limits']['altitude_m']
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

#btn3 = Button(win, text="edit", width=3)
#btn3.pack()
#btn3.place(x=65, y=300)

text_label = LabelFrame(win, text='', relief='solid', bd=1, pady=50)
text_label.pack()
text_label.place(x=15, y=340, width=205, height=150)

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

# btn6 = Button(win, text="Point", width=10, command=lambda:my_resize('increase'))  # 크기변경
# btn6.pack()
# btn6.place(x=65, y=300)
#
# btn7 = Button(win, text="Line", width=3, command=lambda:my_resize('decrease'))
# btn7.pack()
# btn7.place(x=65, y=530)

text_label = LabelFrame(win, text='', relief='solid', bd=1, pady=50)
text_label.pack()
text_label.place(x=15, y=570, width=205, height=150)

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

#a = ["LINE", "POINT-DB", "POINT-WB", "POINT-x", "POINT-h", "POINT-SHF", "POINT-v"]  # 콤보 박스에 나타낼 항목 리스트
#combobox = tkinter.ttk.Combobox(win)  # root라는 창에 콤보박스 생성
#combobox.config(height=7, width=15)  # 높이 설정
#combobox.config(values=a)  # 나타낼 항목 리스트(a) 설정
#combobox.config(state="readonly")  # 콤보 박스에 사용자가 직접 입력 불가
#combobox.set("LINE")  # 맨 처음 나타낼 값 설정
#combobox.pack()
#combobox.place(x=70, y=532)

label = Label(win, text="/")
label.place(x=225, y=570)

label = Label(win, text="Item")
label.place(x=15, y=770)

a = ["DB", "WB", "x", "h", "SHF", "w"]  # 콤보 박스에 나타낼 항목 리스트
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