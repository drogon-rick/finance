import scipy.optimize as sco
import pandas as pd
import numpy as np


def mark_max_sharpe(df_raw):
    '''
    :param df_raw: 投资组合收盘价，列名为投资组合中各资产名称
    :return: 返回投资组合权重
    '''
    # 求收益率

    areturns = df_raw / df_raw.shift(1) - 1
    areturn = areturns.dropna()
    re = pd.DataFrame(np.ones([areturn.shape[0], areturn.shape[1]]), index=areturn.index)
    for j in range(areturn.shape[1]):
        for i in range(1, areturn.shape[0]):
            re.iloc[i, j] = re.iloc[i - 1, j] * (areturn.iloc[i, j] + 1)


    noa = len(areturns.columns)

    # 最优化投资组合的推导是一个约束最优化问题
    # 最小化夏普指数的负值
    def min_sharpe(weights):
        return -statistics(weights)[2]

    # 随机（均匀分布）确定初始权重
    weights = np.random.random(noa)
    weights /= np.sum(weights)
    weights

    # 定义目标函数
    def statistics(weights):
        weights = np.array(weights)
        day_re = np.divide(re.dropna()[-1:], re.dropna()[0:1]).apply(lambda x: x ** (52 / areturn.shape[0]) - 1)
        std = np.sqrt(np.dot(weights.T, np.dot(areturn.cov() * 52, weights)))
        port_returns = np.dot(day_re,weights)
        port_variance = std
        return np.array([port_returns, port_variance, port_returns / port_variance])

    # 约束是所有参数(权重)的总和为1。这可以用minimize函数的约定表达如下
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # 我们还将参数值(权重)限制在0和1之间。这些值以多个元组组成的一个元组形式提供给最小化函数
    bnds = tuple((0, 1) for x in range(noa))

    # 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。简单的使用平均分布。
    opts = sco.minimize(min_sharpe, weights, method='SLSQP', bounds=bnds, constraints=cons)
    return opts['x']


def mark_min_variance(df_raw, tar):
    '''

    :param df_raw: 投资组合收盘价，列名为投资组合中各资产名称
    :param tar: 限制收益率
    :return: 返回权重
    '''
    # 求收益率
    areturns = df_raw / df_raw.shift(1) - 1
    areturn = areturns.dropna()
    re = pd.DataFrame(np.ones([areturn.shape[0], areturn.shape[1]]), index=areturn.index)
    for j in range(areturn.shape[1]):
        for i in range(1, areturn.shape[0]):
            re.iloc[i, j] = re.iloc[i - 1, j] * (areturn.iloc[i, j] + 1)

    noa = len(areturns.columns)

    # 最优化投资组合的推导是一个约束最优化问题
    # 最小化方差
    def min_variance(weights):
        return statistics(weights)[1]

    # 随机（均匀分布）确定初始权重
    weights = np.random.random(noa)
    weights /= np.sum(weights)

    # 定义目标函数
    def statistics(weights):
        weights = np.array(weights)
        day_re = np.divide(re.dropna()[-1:], re.dropna()[0:1]).apply(lambda x: x ** (52 / areturn.shape[0]) - 1)
        std = np.sqrt(np.dot(weights.T, np.dot(areturn.cov() * 52, weights)))
        port_returns = np.dot(day_re,weights)
        port_variance = std
        return np.array([port_returns, port_variance, port_returns / port_variance])

    # 约束是所有参数(权重)的总和为1。这可以用minimize函数的约定表达如下
    cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[0] - tar}, {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # 我们还将参数值(权重)限制在0和1之间。这些值以多个元组组成的一个元组形式提供给最小化函数
    bnds = tuple((0, 1) for x in range(noa))

    # 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。简单的使用平均分布。
    opts = sco.minimize(min_variance, weights, method='SLSQP', bounds=bnds, constraints=cons)
    return opts['x']
    


def mark_max_return(df_raw, tar):
    '''

    :param df_raw: 投资组合收盘价，列名为投资组合中各资产名称
    :param tar: 限制方差
    :return: 返回权重
    '''
    # 求收益率
    areturns = df_raw / df_raw.shift(1) - 1
    areturn = areturns.dropna()
    re = pd.DataFrame(np.ones([areturn.shape[0], areturn.shape[1]]), index=areturn.index)
    for j in range(areturn.shape[1]):
        for i in range(1, areturn.shape[0]):
            re.iloc[i, j] = re.iloc[i - 1, j] * (areturn.iloc[i, j] + 1)

    noa = len(areturns.columns)

    # 最优化投资组合的推导是一个约束最优化问题
    # 最小化收益率的负值
    def max_return(weights):
        return -statistics(weights)[1]

    # 随机（均匀分布）确定初始权重
    weights = np.random.random(noa)
    weights /= np.sum(weights)

    # 定义目标函数
    def statistics(weights):
        weights = np.array(weights)
        day_re = np.divide(re.dropna()[-1:], re.dropna()[0:1]).apply(lambda x: x ** (52 / areturn.shape[0]) - 1)
        std = np.sqrt(np.dot(weights.T, np.dot(areturn.cov() * 52, weights)))
        port_returns = np.dot(day_re,weights)
        port_variance = std
        return np.array([port_returns, port_variance, port_returns / port_variance])

    # 约束是所有参数(权重)的总和为1。这可以用minimize函数的约定表达如下
    cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[1] - tar}, {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # 我们还将参数值(权重)限制在0和1之间。这些值以多个元组组成的一个元组形式提供给最小化函数
    bnds = tuple((0, 1) for x in range(noa))

    # 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。简单的使用平均分布。
    opts = sco.minimize(max_return, weights, method='SLSQP', bounds=bnds, constraints=cons)
    # if opts['success'] == False:
    #     return [np.nan]
    # if opts['success'] == True:
    #     return opts['x']
    return opts['x']