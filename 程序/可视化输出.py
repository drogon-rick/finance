# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 00:29:35 2019

@author: JOE
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 23:13:36 2019

@author: JOE
"""

import pandas as pd
import calendar
from WindPy import *
import risk_budget
import datetime
import matplotlib.pyplot as plt
import Markowitz as mz
import tool_box as tb

stock_index = '000300.SH'
bond_index = 'H11001.CSI'
history_window = 500  # 窗口长度
today = datetime.datetime.now()
start_date = datetime.date.today().replace(day=1)
_, days_in_month = calendar.monthrange(start_date.year, start_date.month)
end = today - timedelta(days=today.weekday() + 1)
start = end - timedelta(days=history_window)
end = end.strftime("%Y-%m-%d")
start = start.strftime("%Y-%m-%d")
w.start()
w_stodebt = w.wsd(stock_index + "," + bond_index, "close", start, end, "Period=W")
df_raw = pd.DataFrame(w_stodebt.Data, index=w_stodebt.Codes, columns=w_stodebt.Times)
df_raw = pd.DataFrame(df_raw.values.T, index=w_stodebt.Times, columns=w_stodebt.Codes)

df_weight, df_weight_4w, df_weight_12w, df_returns, df_netvalue = tb.exe(stock_index, bond_index, end, start, df_raw)
# %%
df_weight = round(df_weight, 3)
df_weight_4w = round(df_weight_4w, 3)
df_weight_12w = round(df_weight_12w, 3)
df_returns_out = round(df_returns - 1, 4) * 100
df_netvalue = round(df_netvalue, 3)

str_per = ''
for i in range(len(df_returns_out.columns)):
    df_returns_out=round(df_returns_out*100,2)/100
    str_per = str_per + '\n{}策略表现：上周涨跌：{}%，上月涨跌：{}%，近三月涨跌{}%，半年涨跌{}%\n'.format(df_returns_out.columns[i],
                                                                             df_returns_out.iloc[0, i],
                                                                             df_returns_out.iloc[1, i],
                                                                             df_returns_out.iloc[2, i],
                                                                             df_returns_out.iloc[3, i])

weight = ''
for i in range(len(df_weight.columns)):
    weight = weight + '\n{}上周股票配置比例是{}，过去4周股票配置比例是{}，过去12周股票配置比例是{}\n'.format(df_weight.columns[i],
                                                                              df_weight.iloc[0, i],
                                                                              df_weight_4w.iloc[0, i],
                                                                              df_weight_12w.iloc[0, i])

print('净值日期：\n{}'.format(end))
print('历史净值：\n{}'.format(df_netvalue))
# %%
import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('1000x800')

time = tk.Label(window,
                text='最近调仓日' + end,  # 使用 textvariable 替换 text, 因为这个可以变化
                font=('Arial', 10), width=17, height=2)
time.pack(side='top')

var = tk.StringVar()  # 这时文字变量储存器
l = tk.Label(window,
             textvariable=var,  # 使用 textvariable 替换 text, 因为这个可以变化
             font=('Arial', 10), bg='white', width=140, height=30)
l.pack()
on_hit = False
on_hit2 = False
on_hit3 = False


def hit_me1():
    global on_hit
    if on_hit == False:  # 从 False 状态变成 True 状态
        on_hit = True
        var.set(weight)  # 设置标签的文字
    else:  # 从 True 状态变成 False 状态
        on_hit = False
        var.set('')  # 设置 文字为空


def hit_me2():
    global on_hit2
    if on_hit2 == False:  # 从 False 状态变成 True 状态
        on_hit2 = True
        var.set(str_per)  # 设置标签的文字
    else:  # 从 True 状态变成 False 状态
        on_hit2 = False
        var.set('')  # 设置 文字为空


def hit_me3():
    global on_hit3
    if on_hit3 == False:  # 从 False 状态变成 True 状态
        on_hit3 = True
        var.set(df_netvalue)  # 设置标签的文字
    else:  # 从 True 状态变成 False 状态
        on_hit3 = False
        var.set('')  # 设置 文字为空


b1 = tk.Button(window, text='股票配置比例', width=15,
               height=2, command=hit_me1)
b1.pack()
b2 = tk.Button(window, text='策略表现', width=15,
               height=2, command=hit_me2)
b2.pack()
b2 = tk.Button(window, text='历史净值', width=15,
               height=2, command=hit_me3)
b2.pack()

window.mainloop()
