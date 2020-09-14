# 导入数据
import pandas as pd
import math
import numpy as np
import scipy.stats as scs
import statsmodels.api as sm
from pylab import mpl, plt

raw = pd.read_csv(r'.\历史金融时间序列数据.csv',index_col=0, parse_dates=True).dropna()

symbols = ['AAPL.O', 'MSFT.O', 'SPY', 'GLD']  
noa = len(symbols)
data = raw[symbols]

# 生成对数收益率
rets = np.log(data / data.shift(1))
rets.hist(bins=40, figsize=(10, 8))

rets.mean() * 252 
rets.cov() * 252

# 投资组合的资产权重
weights = np.random.random(noa)  
weights /= np.sum(weights)  

print(weights)
weights.sum()

# 投资组合的预期收益
print(np.sum(rets.mean() * weights) * 252)

# 投资组合的预期方差（波动率）
print(np.dot(weights.T, np.dot(rets.cov() * 252, weights)) )
print(np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))

# 投资组合的预期超额收益（夏普指数）
print( (np.sum(rets.mean() * weights) * 252)  / (np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))) )

# 投资组合的蒙特卡洛模拟
def port_ret(weights):
    return np.sum(rets.mean() * weights) * 252
         
def port_vol(weights):
    return np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))

prets = []
pvols = []
for p in range (2500):  
    weights = np.random.random(noa)  
    weights /= np.sum(weights)  
    prets.append(port_ret(weights))  
    pvols.append(port_vol(weights))  
prets = np.array(prets)
pvols = np.array(pvols)

# 投资组合资产权重的预期收益和波动率散点图
plt.figure(figsize=(10, 6))
plt.scatter(pvols, prets, c=prets / pvols, marker='o', cmap='coolwarm')
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')

# 投资组合的预期超额收益（夏普指数）最大化
# 目标函数、约束条件和初始值设定
def min_func_sharpe(weights):  
    return -port_ret(weights) / port_vol(weights)
cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})  
bnds = tuple((0, 1) for x in range(noa))  
eweights = np.array(noa * [1. / noa,])  
# eweights

# 通过sco.minimize()函数实现最优投资组合
import scipy.optimize as sco

opts = sco.minimize(min_func_sharpe, eweights, method='SLSQP', bounds=bnds, constraints=cons)
print(opts)

opts['x'].round(3)
port_ret(opts['x']).round(3) 
port_vol(opts['x']).round(3) 
port_ret(opts['x']) / port_vol(opts['x'])

cons = ({'type': 'eq', 'fun': lambda x:  port_ret(x) - tret}, {'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
bnds = tuple((0, 1) for x in weights)

trets = np.linspace(0.05, 0.2, 50)
tvols = []
for tret in trets:
    res = sco.minimize(port_vol, eweights, method='SLSQP', bounds=bnds, constraints=cons)  
    tvols.append(res['fun'])
tvols = np.array(tvols)

# 最优投资组合的有效边界图
plt.figure(figsize=(10, 6))
plt.scatter(pvols, prets, c=prets / pvols, marker='.', alpha=0.8, cmap='coolwarm')
plt.plot(tvols, trets, 'b', lw=4.0)
plt.plot(port_vol(opts['x']), port_ret(opts['x']), 'y*', markersize=15.0)
plt.plot(port_vol(optv['x']), port_ret(optv['x']), 'r*', markersize=15.0)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')
