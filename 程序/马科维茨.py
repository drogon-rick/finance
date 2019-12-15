# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 22:21:27 2019

@author: JOE
"""
# -*- coding: utf-8 -*-
# 导入本地其他程序

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from WindPy import *
import os
import datetime
import calendar
# %%
# 文件夹所在位置
path0 = os.path.abspath('..')
result_filepath = path0.replace("\\", "/")
w.start()
stock_index = '000300.SH'
month_start = "2006-01-29"
day_start = "2005-06-01"
today=datetime.datetime.now()
start_date = datetime.date.today().replace(day=1)
_, days_in_month = calendar.monthrange(start_date.year, start_date.month)
if today == days_in_month:   
    month_end = datetime.datetime.now().strftime( "%Y-%m-%d")    
    day_end = datetime.datetime.now().strftime( "%Y-%m-%d")
else:
    month_end =start_date-timedelta(days=1)
    day_end = start_date - timedelta(days=1)
window = 10
history_window=250
# %%
# # # 读取股债数据，计算收益率
w.start()
w_stodebt = w.wsd("000300.SH,CBA00101.CS", "close", month_start, month_end, "Period=W")

df_raw = pd.DataFrame(w_stodebt.Data, index=w_stodebt.Codes, columns=w_stodebt.Times)
df_raw = pd.DataFrame(df_raw.values.T, index=w_stodebt.Times, columns=w_stodebt.Codes)
returns =  np.log(df_raw / df_raw.shift(1))
noa=len(returns.columns)
#%%
def statistics(weights):
    weights = np.array(weights)
    port_returns = np.sum(returns.mean()*weights)*52
    port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*52,weights)))
    return np.array([port_returns, port_variance, port_returns/port_variance])
#最优化投资组合的推导是一个约束最优化问题
import scipy.optimize as sc

weights = np.random.random(noa)
weights /= np.sum(weights)
weights

def max_return(weights):
    return statistics(weights)[1]

#在不同目标收益率水平（target_returns）循环时，最小化的一个约束条件会变化。

tar=50
cons = ({'type':'eq','fun':lambda x:statistics(x)[0]-tar},{'type':'eq','fun':lambda x:np.sum(x)-1})
res = sco.minimize(min_variance, noa*[1./noa,],method = 'SLSQP', bounds = bnds, constraints = cons)


#%%
import Markowitz as mz
weights=mark_max_return(df_raw, 0)


        
        
        
        
        
        
        
        