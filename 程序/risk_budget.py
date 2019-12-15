import numpy as np
import pandas as pd
from scipy.optimize import minimize


def get_smart_weight(cov_mat: pd.DataFrame, risk_budget: pd.Series):

    """
    功能:
         输入协方差矩阵，得到不同优化方法下的权重配置
    输入:
         cov_mat: pd.DataFrame, 协方差矩阵，index和column均为资产名称
         risk_budget: pd.Series, 风险预算序列，index为资产名
    输出:
         pd.Series index为资产名, value为weight
    """

    if not isinstance(cov_mat, pd.DataFrame):

        raise ValueError('cov_mat should be pandas DataFrame!')

    if not isinstance(risk_budget, pd.Series):

        raise ValueError('risk_budget should be pandas Series!')

    # 协方差矩阵
    omega = np.matrix(cov_mat.values)
    # print(omega)
    # 资产数目
    asset_num = len(cov_mat.columns)

    # 定义目标函数
    def risk_budget_func(x):

        total_risk = np.array(np.matrix(x) * omega * np.matrix(x).T)[0, 0]
        tmp = (omega * np.matrix(x).T).A1
        risk = x * tmp
        delta_error = [(risk[i] - risk_budget[i] * total_risk) ** 2 for i in range(asset_num)]
        return np.sum(delta_error)

    # 初始值 + 约束条件
    x0 = np.asmatrix(list(risk_budget))
    bnds = tuple((0, 1) for i in range(len(omega)))
    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - 1})
    options = {'disp': False, 'maxiter': 1000}

    res = minimize(risk_budget_func, x0, bounds=bnds, constraints=cons, method='SLSQP', tol=1e-14, options=options)

    wts = pd.Series(index=list(cov_mat.columns), data=res['x'])

    return wts
if __name__=='main':
    pass
