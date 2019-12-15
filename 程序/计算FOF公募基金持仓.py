import pandas as pd
import numpy as np
from WindPy import *
import datetime
import calendar

#自动确定上一季度时间 
z = datetime.datetime.now()
rptime = z + pd.tseries.offsets.DateOffset(months=-((z.month - 1) % 3), days=1 - z.day) - timedelta(days=1)
rptime=rptime.strftime( "%Y-%m-%d")
w.start()
w_fundcode = w.wset("sectorconstituent", "date="+rptime+";sectorid=2001020400000000")
fund_code_list = []
fund_code_list = (w_fundcode.Data[1])

# fund_name=''
# for i in range(len(fund_code_list)):
#     fund_name=fund_name+fund_code_list[i]+','
# fund_name=fund_name[:-1]
df_weights=pd.DataFrame(columns=["bond","stock"])
top_fund=pd.DataFrame(index=fund_code_list)
for i in range(10):
    num=str(i+1)
    w_top_fund = w.wss(fund_code_list, "prt_topfundwindcode,prt_heavilyheldfundtofund", "rptDate="+rptime+";topNum="+num)
    top_fund_1=pd.DataFrame(w_top_fund.Data)
    top_fund_1=pd.DataFrame(top_fund_1.values.T,columns=w_top_fund.Fields,index=w_top_fund.Codes)
    top_fund=pd.merge(top_fund, top_fund_1, how='outer',left_index=True, right_index=True)
top_fund.dropna(inplace=True)
bond_weight=0
stock_weight=0
for r in range(len(top_fund.index)):
    for i in range(10):
        w_weight=w.wss(top_fund.iloc[r,i*2], "prt_bondtoasset,prt_stocktoasset","rptDate="+rptime)
        df_weight=pd.DataFrame(w_weight.Data)
        df_weight=df_weight.fillna(0.0)
        bond_weight=bond_weight+top_fund.iloc[r,i*2+1]*df_weight.values[0][0]
        stock_weight=stock_weight+top_fund.iloc[r,i*2+1]*df_weight.values[1][0]
    bond_weight=bond_weight/100
    stock_weight=stock_weight/100
    df_weight=pd.DataFrame({"bond":bond_weight,"stock":stock_weight},index=[top_fund.index[r]],columns=["bond","stock"])
    df_weights=df_weights.append(df_weight)
    print(top_fund.index[r])