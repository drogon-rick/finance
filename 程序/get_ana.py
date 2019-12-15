
def get_analyse(curse):
    '''
    要求curse数据中index为时间，columns为策略名称，每一列为该策略净值

    '''
    qf_drawdown = []
    qf_yeild = []
    qf_std = []
    date = curse.index
    y = curse.copy()
    for i in curse.columns:
        # 计算当前日之前的资金曲线最高点
        y["max2here"] = y[i].expanding().max()
        # 计算历史最高值到当日的剩余量
        y["dd2here"] = y[i] / y["max2here"]

        # 计算完回撤后剩余量的最小值（即最大回撤的剩余量），以及最大回撤的结束时间
        remain = y.sort_values(by="dd2here").iloc[0]["dd2here"]
        end_date = y.sort_values(by="dd2here").iloc[0]
        drawdown = round((1 - remain) * 100, 2)
        qf_drawdown.append(drawdown)
        daylenth = len(date) - 1
        yeild = round(((y[i][daylenth]) ** (52 / daylenth) - 1) * 100, 2)
        qf_yeild.append(yeild)
        y1 = y[i]
        r1 = y1 / y1.shift(1) - 1
        std = round(np.nanstd(r1) * 52 ** 0.5 * 100, 2)
        qf_std.append(std)
    drawdown = pd.DataFrame(qf_drawdown, index=curse.columns, columns=["最大回撤"])
    drawdown["年化收益率"] = qf_yeild
    drawdown["Calmar比率"] = drawdown["年化收益率"] / drawdown["最大回撤"]
    drawdown["年波动率"] = qf_std
    drawdown["夏普比率"] = drawdown["年化收益率"] / drawdown["年波动率"]
    return drawdown