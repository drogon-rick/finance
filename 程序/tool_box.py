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
stock_index = '000300.SH'
bond_index='H11001.CSI'
history_window=500 #窗口长度
today=datetime.datetime.now()
start_date = datetime.date.today().replace(day=1)
_, days_in_month = calendar.monthrange(start_date.year, start_date.month)
end =today-timedelta(days=today.weekday()+1)
start = end-timedelta(days=history_window)
end=end.strftime( "%Y-%m-%d")
start=start.strftime( "%Y-%m-%d")
w.start()
w_stodebt = w.wsd(stock_index+","+bond_index, "close", start, end, "Period=W")    
df_raw = pd.DataFrame(w_stodebt.Data, index=w_stodebt.Codes, columns=w_stodebt.Times)
df_raw = pd.DataFrame(df_raw.values.T, index=w_stodebt.Times, columns=w_stodebt.Codes)   

# # # 读取股债数据，计算收益率
def exe(stock_index,bond_index,end,start,df_raw):
    df_raw[df_raw.columns[0] + '_收益率'] = 0
    df_raw[df_raw.columns[1] + '_收益率'] = 0
    for i in range(1, len(df_raw.index)):
        df_raw.iloc[i, 2] = df_raw.iloc[i, 0] / df_raw.iloc[i - 1, 0] - 1
        df_raw.iloc[i, 3] = df_raw.iloc[i, 1] / df_raw.iloc[i - 1, 1] - 1
#风险平价
    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算协方差矩阵窗口
    for i in range(window-1, len(df_all.index)):
        cov = df_all.iloc[i - window + 1:i + 1, 2:4].cov()
        budget = 1
        budget = pd.Series(index=df_all.columns[:2], data=[budget / (budget + 1), 1 / (budget + 1)])
        w = risk_budget.get_smart_weight(cov, budget)
        w = w.values
        df_all.iloc[i, -4] = w[0]  # 股票权重
        df_all.iloc[i, -4] = round(df_all.iloc[i, -4] * 100) / 100  # 取整
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    df_weight=pd.DataFrame(index=df_all.columns[-4:-2])
    df_weight['风险平价']=df_all.iloc[-1,-4:-2]
    df_weight_4w=pd.DataFrame(index=df_all.columns[-4:-2])
    df_weight_4w['风险平价']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w=pd.DataFrame(index=df_all.columns[-4:-2])
    df_weight_12w['风险平价']=df_all.iloc[-13:-1,-4:-2].mean()
    
    print("风险平价完成")
    df_returns=pd.DataFrame(index=["上周","一个月","近三月","半年"])
    st_name='风险平价'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue=pd.Series()
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
#风险预算
    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算协方差矩阵窗口
    for i in range(window-1, len(df_all.index)):
        cov = df_all.iloc[i - window + 1:i + 1, 2:4].cov()
        budget = 30
        budget = pd.Series(index=df_all.columns[:2], data=[budget / (budget + 1), 1 / (budget + 1)])
        w = risk_budget.get_smart_weight(cov, budget)
        w = w.values
        df_all.iloc[i, -4] = w[0]  # 股票权重
        df_all.iloc[i, -4] = round(df_all.iloc[i, -4] * 100) / 100  # 取整
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    df_weight['风险预算']=df_all.iloc[-1,-4:-2]
    df_weight_4w['风险预算']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['风险预算']=df_all.iloc[-13:-1,-4:-2].mean()
    print("风险预算完成")
    st_name='风险预算'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
#马科维茨最大夏普比率
    df_all=df_raw.copy()
    
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算马尔科夫权重使用窗口
    for i in range(window-1, len(df_all.index)):
        df_pri=df_raw.iloc[i - window + 1:i + 1,0:2]
        w = mz.mark_max_sharpe(df_pri)
        df_all.iloc[i, -4] = w[0]  # 股票权重
        df_all.iloc[i, -4] = round(df_all.iloc[i, -4] * 100) / 100  # 取整
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    
    df_weight['mz_最大夏普比率']=df_all.iloc[-1,-4:-2]
    df_weight_4w['mz_最大夏普比率']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['mz_最大夏普比率']=df_all.iloc[-13:-1,-4:-2].mean()
    print("马科维茨最大夏普比率完成")
    st_name='mz_最大夏普比率'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]

    #确定收益最小方差
    sta_rt = 0.07
    
    df_all=df_raw.copy()
    
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算马尔科夫权重使用窗口
    for i in range(window-1, len(df_all.index)):
        print(i)
        df_pri=df_raw.iloc[i - window + 1:i + 1,0:2]
        w = mz.mark_min_variance(df_pri,sta_rt)
        df_all.iloc[i, -4] = w[0]  # 股票权重
        df_all.iloc[i, -4] = round(df_all.iloc[i, -4] * 100) / 100  # 取整
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    
    df_weight['mz_最小方差']=df_all.iloc[-1,-4:-2]
    df_weight_4w['mz_最小方差']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['mz_最小方差']=df_all.iloc[-13:-1,-4:-2].mean()
    print("马科维茨最小方差完成")
    st_name='mz_最小方差'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
    

    #确定方差最大收益
    std=0.15
    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算马尔科夫权重使用窗口
    for i in range(window-1, len(df_all.index)):
        print(i)
        df_pri=df_raw.iloc[i - window + 1:i + 1,0:2]
        w = mz.mark_max_return(df_pri,std)
        df_all.iloc[i, -4] = w[0]  # 股票权重
        df_all.iloc[i, -4] = round(df_all.iloc[i, -4] * 100) / 100  # 取整
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    
    df_weight['mz_最大收益率']=df_all.iloc[-1,-4:-2]
    df_weight_4w['mz_最大收益率']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['mz_最大收益率']=df_all.iloc[-13:-1,-4:-2].mean()
    print("马科维茨最大收益率完成")
    st_name='mz_最大收益率'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
    

    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算协方差矩阵窗口
    for i in range(window-1, len(df_all.index)):
        cov = df_all.iloc[i - window + 1:i + 1, 2:4].cov()
        df_all.iloc[i, -4] = 0.2 #股票权重
        df_all.iloc[i, -4] = round(df_all.iloc[i, -4] * 100) / 100  # 取整
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    df_weight['固定股债比2:8']=df_all.iloc[-1,-4:-2]
    df_weight_4w['固定股债比2:8']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['固定股债比2:8']=df_all.iloc[-13:-1,-4:-2].mean()
    print("固定股债比2:8完成")
    st_name='固定股债比2:8'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
    

    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算协方差矩阵窗口
    for i in range(window-1, len(df_all.index)):
        cov = df_all.iloc[i - window + 1:i + 1, 2:4].cov()
        df_all.iloc[i, -4] = 0.4 #股票权重
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    df_weight['固定股债比4:6']=df_all.iloc[-1,-4:-2]
    df_weight_4w['固定股债比4:6']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['固定股债比4:6']=df_all.iloc[-13:-1,-4:-2].mean()
    print("固定股债比4:6完成")
    st_name='固定股债比4:6'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
    

    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算协方差矩阵窗口
    for i in range(window-1, len(df_all.index)):
        cov = df_all.iloc[i - window + 1:i + 1, 2:4].cov()
        df_all.iloc[i, -4] = 0.6 #股票权重
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    df_weight['固定股债比6:4']=df_all.iloc[-1,-4:-2]
    df_weight_4w['固定股债比6:4']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['固定股债比6:4']=df_all.iloc[-13:-1,-4:-2].mean()
    print("固定股债比6:4完成")
    st_name='固定股债比6:4'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
    

    df_all=df_raw.copy()
    df_all['股票权重'] = 0
    df_all['债券权重'] = 0
    df_all['净值'] = 1
    df_all['benchmark'] = 1
    window=10  #计算协方差矩阵窗口
    for i in range(window-1, len(df_all.index)):
        cov = df_all.iloc[i - window + 1:i + 1, 2:4].cov()
        df_all.iloc[i, -4] = 0.8 #股票权重
        df_all.iloc[i, -3] = 1 - df_all.iloc[i, -4]  # 债券权重
        if i < (len(df_all.index) - 1):  # 计算净值曲线
            df_all.iloc[i + 1, -2] = df_all.iloc[i, -2] * (
                    1 + df_all.iloc[i, -4] * df_all.iloc[i + 1, 2] + df_all.iloc[i, -3] * df_all.iloc[i + 1, 3])
            df_all.iloc[i + 1, -1] = df_all.iloc[i, -1] * (1 + df_all.iloc[i + 1, 2])
    df_weight['固定股债比8:2']=df_all.iloc[-1,-4:-2]
    df_weight_4w['固定股债比8:2']=df_all.iloc[-5:-1,-4:-2].mean()
    df_weight_12w['固定股债比8:2']=df_all.iloc[-13:-1,-4:-2].mean()
    print("固定股债比8:2完成")
    st_name='固定股债比8:2'
    df_returns.loc["上周",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 2, -2] 
    df_returns.loc["一个月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 5, -2] 
    df_returns.loc["近三月",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_returns.loc["半年",st_name]=df_all.iloc[- 1, -2] / df_all.iloc[- 13, -2] 
    df_netvalue[st_name]=df_all.iloc[- 1, -2]
    return df_weight,df_weight_4w,df_weight_12w,df_returns,df_netvalue


if __name__=="__main__":

    df_weight,df_weight_4w,df_weight_12w,df_returns,df_netvalue=exe(stock_index,bond_index,end,start,df_raw)
    df_weight=round(df_weight,3)
    df_weight_4w=round(df_weight_4w,3)
    df_weight_12w=round(df_weight_12w,3)
    df_returns_out=round(df_returns-1,4)*100
    p_w={}
    p_w4={}
    p_w12={}
    for i in range(len(df_returns_out.columns)):
        a={}
        re_i=df_returns_out.iloc[:,i]
        for j in range(len(re_i)):        
            a[re_i.index[j]]=round(re_i[j],2)
        print('{}策略表现(%)：{}'.format(df_returns_out.columns[i],a))
    
    for i in range(len(df_weight.columns)):
        p_w[df_weight.columns[i]]=df_weight.iloc[0,i]
        p_w4[df_weight_4w.columns[i]]=df_weight_4w.iloc[0,i]
        p_w12[df_weight_12w.columns[i]]=df_weight_12w.iloc[0,i]
    
    print('上周股票配置比例是{}'.format(p_w))
    print('过去4周股票配置比例是{}'.format(p_w4))
    print('过去12周股票配置比例是{}'.format(p_w12))
    for i in range(len(df_returns_out.columns)):
        a={}
        re_i=df_returns_out.iloc[:,i]
        for j in range(len(re_i)):        
            a[re_i.index[j]]=round(re_i[j],2)
        print('{}策略表现(%)：{}'.format(df_returns_out.columns[i],a))
    print('净值日期：{}'.format(end))
    print('历史净值：{}'.format(df_netvalue))
