# =============================================================================
# 1.1 模拟数据
# =============================================================================

# 基本设置
import math
import numpy as np
import scipy.stats as scs
import statsmodels.api as sm
from pylab import mpl, plt

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

# 定义gen_paths()函数：几何布朗运动
def gen_paths(S0, r, sigma, T, M, I):
    ''' Generate Monte Carlo paths for geometric Brownian motion.
    
    Parameters
    ==========
    S0: float
        initial stock/index value
    r: float
        constant short rate
    sigma: float
        constant volatility
    T: float
        final time horizon
    M: int
        number of time steps/intervals
    I: int
        number of paths to be simulated

    Returns
    =======
    paths: ndarray, shape (M + 1, I)
        simulated paths given the parameters
    '''
    dt = T / M
    paths = np.zeros((M + 1, I))
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal(I)
        rand = (rand - rand.mean()) / rand.std()  
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * rand)  
    return paths    

# 设置蒙特卡洛模拟参数
S0 = 100.  
r = 0.05  
sigma = 0.2  
T = 1.0  
M = 50  
I = 250000  
np.random.seed(1000)

# 调用gen_paths()函数生成股票价格模拟数据(S_t)
paths = gen_paths(S0, r, sigma, T, M, I)
S0 * math.exp(r * T) 
paths[-1].mean() 
paths[:, 0].round(4) 

# 股票价格前10次模拟数据的线图
plt.figure(figsize=(10, 6))
plt.plot(paths[:, :10])
plt.xlabel('time steps')
plt.ylabel('price')

# 生成对数收益率模拟数据(log("S_t"/ S_s)
log_returns = np.log(paths[1:] / paths[:-1])
log_returns[:, 0].round(4) 

# 定义print_statistics()函数：描述性统计
def print_statistics(array):
    ''' Prints selected statistics.

    Parameters
    ==========
    array: ndarray
        object to generate statistics on
    '''
    sta = scs.describe(array)
    print('%14s %15s' % ('statistic', 'value'))
    print(30 * '-')
    print('%14s %15.5f' % ('size', sta[0]))
    print('%14s %15.5f' % ('min', sta[1][0]))
    print('%14s %15.5f' % ('max', sta[1][1]))
    print('%14s %15.5f' % ('mean', sta[2]))
    print('%14s %15.5f' % ('std', np.sqrt(sta[3])))
    print('%14s %15.5f' % ('skew', sta[4]))
    print('%14s %15.5f' % ('kurtosis', sta[5]))
    
# 调用print_statistics()函数进行对数收益率模拟数据的描述性统计
print_statistics(log_returns.flatten())
log_returns.mean() * M + 0.5 * sigma ** 2 
log_returns.std() * math.sqrt(M) 

# 正态性检验方法1：对比频率分布(直方图)与理论化正态密度函数(PDF)
plt.figure(figsize=(10, 6))
plt.hist(log_returns.flatten(), bins=70, normed=True, label='frequency', color='b')
plt.xlabel('log return')
plt.ylabel('frequency')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, loc=r / M, scale=sigma / np.sqrt(M)), 'r', lw=2.0, label='pdf')  
plt.legend()

# 正态性检验方法2：对比样本分位数值与理论分位数值(QQ图)
sm.qqplot(log_returns.flatten()[::500], line='s')
plt.xlabel('theoretical quantiles')
plt.ylabel('sample quantiles')

# 正态性检验方法3：normality_tests()函数
# 定义normality_tests()函数：正态性测试
def normality_tests(arr):
    ''' Tests for normality distribution of given data set.

    Parameters
    ==========
    array: ndarray
        object to generate statistics on
    '''
    print('Skew of data set  %14.3f' % scs.skew(arr))
    print('Skew test p-value %14.3f' % scs.skewtest(arr)[1])
    print('Kurt of data set  %14.3f' % scs.kurtosis(arr))
    print('Kurt test p-value %14.3f' % scs.kurtosistest(arr)[1])
    print('Norm test p-value %14.3f' % scs.normaltest(arr)[1])

# 调用normality_tests()函数进行对数收益率模拟数据的正态性测试
normality_tests(log_returns.flatten()) 

# 对数股票价格模拟数据的基本特征
# 股票价格和对数股票价格模拟数据的直方图
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
ax1.hist(paths[-1], bins=30)
ax1.set_xlabel('price')
ax1.set_ylabel('frequency')
ax1.set_title('regular data')
ax2.hist(np.log(paths[-1]), bins=30)
ax2.set_xlabel('log price')
ax2.set_title('log data')

# 调用print_statistics()函数进行股票价格和对数股票价格模拟数据的描述性统计
print_statistics(paths[-1])
print_statistics(np.log(paths[-1]))

# 对数股票价格模拟数据的正态性检验
# 正态性检验方法1：对比频率分布(直方图)与理论化正态密度函数(PDF)
plt.figure(figsize=(10, 6))
log_data = np.log(paths[-1])
plt.hist(log_data, bins=70, normed=True, label='observed', color='b')
plt.xlabel('log price')
plt.ylabel('frequency')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, log_data.mean(), log_data.std()), 'r', lw=2.0, label='pdf')
plt.legend()

# 正态性检验方法2：对比样本分位数值与理论分位数值(QQ图)
sm.qqplot(log_data, line='s')
plt.xlabel('theoretical quantiles')
plt.ylabel('sample quantiles')
    
# 正态性检验方法3：normality_tests()函数
normality_tests(log_data.flatten()) 

# =============================================================================
# 1.2 实战演练
# =============================================================================

# 历史金融时间序列数据基本特征
# 导入数据
import pandas as pd
raw = pd.read_csv(r'C:\Users\Admin\Desktop\Python金融大数据分析\历史金融时间序列数据.csv',index_col=0, parse_dates=True).dropna()

symbols = ['SPY', 'GLD', 'AAPL.O', 'MSFT.O']    
data = raw[symbols]
data = data.dropna()   

# 查看数据信息
data.info()
data.head()    

# 绘制股票规范化价格数据的线图
plt.figure(figsize=(10, 6))
plt.plot((data / data.iloc[0] * 100)['SPY'], lw=1.5, label='SPY')
plt.plot((data / data.iloc[0] * 100)['GLD'], lw=1.5, label='GLD')
plt.plot((data / data.iloc[0] * 100)['AAPL.O'], lw=1.5, label='AAPL.O')
plt.plot((data / data.iloc[0] * 100)['MSFT.O'], lw=1.5, label='MSFT.O')
plt.xlabel('date')
plt.ylabel('price')
plt.legend()

(data / data.iloc[0] * 100).plot(figsize=(10, 6))

# 生成对数收益率
log_returns = np.log(data / data.shift(1))
log_returns.head()

# 对数收益率的直方图
plt.figure(figsize=(10, 8))
plt.subplot(221)
plt.hist(log_returns['AAPL.O'], bins=50)
plt.title('AAPL.O')
plt.subplot(222)
plt.hist(log_returns['GLD'], bins=50)
plt.title('GLD')
plt.subplot(223)
plt.hist(log_returns['MSFT.O'], bins=50)
plt.title('MSFT.O')
plt.subplot(224)
plt.hist(log_returns['SPY'], bins=50)
plt.title('SPY')

log_returns.hist(bins=50, figsize=(10, 8))

# 调用print_statistics()函数进行对数收益率的描述性统计
for sym in symbols:
    print('\nResults for symbol {}'.format(sym))
    print(30 * '-')
    log_data = np.array(log_returns[sym].dropna())
    print_statistics(log_data)
    
# 历史金融时间序列数据的正态性检验    
# 正态性检验方法1：对比频率分布(直方图)与理论化正态密度函数(PDF)
plt.figure(figsize=(10, 8))
log_returns1 = log_returns.dropna()
plt.subplot(221)
plt.hist(log_returns1['AAPL.O'], bins=50, normed=True, label='observed', color='b')
plt.title('AAPL.O')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, log_returns1['AAPL.O'].mean(),log_returns1['AAPL.O'].std()), 'r', lw=2.0, label='pdf')
plt.legend()
plt.subplot(222)
plt.hist(log_returns1['GLD'], bins=50, normed=True, label='observed', color='b')
plt.title('GLD')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, log_returns1['GLD'].mean(),log_returns1['GLD'].std()), 'r', lw=2.0, label='pdf')
plt.legend()
plt.subplot(223)
plt.hist(log_returns1['MSFT.O'], bins=50, normed=True, label='observed', color='b')
plt.title('MSFT.O')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, log_returns1['MSFT.O'].mean(),log_returns1['MSFT.O'].std()), 'r', lw=2.0, label='pdf')
plt.legend()
plt.subplot(224)
plt.hist(log_returns1['SPY'], bins=50, normed=True, label='observed', color='b')
plt.title('SPY')
x = np.linspace(plt.axis()[0], plt.axis()[1])
plt.plot(x, scs.norm.pdf(x, log_returns1['SPY'].mean(),log_returns1['SPY'].std()), 'r', lw=2.0, label='pdf')
plt.legend()

# 正态性检验方法2：对比样本分位数值与理论分位数值(QQ图)
sm.qqplot(log_returns['SPY'].dropna(), line='s')
plt.title('SPY')
plt.xlabel('theoretical quantiles')
plt.ylabel('sample quantiles')

sm.qqplot(log_returns['GLD'].dropna(), line='s')
plt.title('GLD')
plt.xlabel('theoretical quantiles')
plt.ylabel('sample quantiles')

sm.qqplot(log_returns['MSFT.O'].dropna(), line='s')
plt.title('MSFT.O')
plt.xlabel('theoretical quantiles')
plt.ylabel('sample quantiles')

sm.qqplot(log_returns['AAPL.O'].dropna(), line='s')
plt.title('AAPL.O')
plt.xlabel('theoretical quantiles')
plt.ylabel('sample quantiles')

# 正态性检验方法3：normality_tests()函数
for sym in symbols:
    print('\nResults for symbol {}'.format(sym))
    print(32 * '-')
    log_data = np.array(log_returns[sym].dropna())
    normality_tests(log_data)
    
# =============================================================================
# 2.1 数据
# =============================================================================

# 导入数据
import pandas as pd
raw = pd.read_csv(r'C:\Users\Admin\Desktop\Python金融大数据分析\历史金融时间序列数据.csv',index_col=0, parse_dates=True).dropna()

symbols = ['AAPL.O', 'MSFT.O', 'SPY', 'GLD']  
noa = len(symbols)
data = raw[symbols]

# 生成对数收益率
rets = np.log(data / data.shift(1))
rets.hist(bins=40, figsize=(10, 8)) 

# 计算年化平均收益率和协方差矩阵
rets.mean() * 252 
rets.cov() * 252

# =============================================================================
# 2.2 基本理论
# =============================================================================

# 投资组合的资产权重
weights = np.random.random(noa)  
weights /= np.sum(weights)  

weights
weights.sum()

# 投资组合的预期收益
np.sum(rets.mean() * weights) * 252 

# 投资组合的预期方差（波动率）
np.dot(weights.T, np.dot(rets.cov() * 252, weights)) 
np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))) 

# 投资组合的预期超额收益（夏普指数）
(np.sum(rets.mean() * weights) * 252)  / (np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))

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

# =============================================================================
# 2.3 最优投资组合
# =============================================================================

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
opts

opts['x'].round(3)
port_ret(opts['x']).round(3) 
port_vol(opts['x']).round(3) 
port_ret(opts['x']) / port_vol(opts['x'])

# 投资组合的波动率最小化
# 通过sco.minimize()函数实现最优投资组合
optv = sco.minimize(port_vol, eweights, method='SLSQP', bounds=bnds, constraints=cons) 
optv

optv['x'].round(3)
port_vol(optv['x']).round(3)
port_ret(optv['x']).round(3)
port_ret(optv['x']) / port_vol(optv['x'])

# =============================================================================
# 2.4 有效边界
# =============================================================================

# 目标收益率水平下的投资组合波动率最小化
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

# =============================================================================
# 2.5 资本市场线
# =============================================================================

# 定义有效边界函数f(x)和对应的一阶导数函数df(x)
import scipy.interpolate as sci

ind = np.argmin(tvols)  
evols = tvols[ind:]  
erets = trets[ind:]  

tck = sci.splrep(evols, erets)  

def f(x):
    ''' Efficient frontier function (splines approximation). '''
    return sci.splev(x, tck, der=0)

def df(x):
    ''' First derivative of efficient frontier function. '''
    return sci.splev(x, tck, der=1) 
         
# 定义资本市场线的方程式
def equations(p, rf=0.01):
    eq1 = rf - p[0]  
    eq2 = rf + p[1] * p[2] - f(p[2])  
    eq3 = p[1] - df(p[2])  
    return eq1, eq2, eq3

# 求取最优参数值
opt = sco.fsolve(equations, [0.01, 0.5, 0.15])
opt
np.round(equations(opt), 6) 

# 最优投资组合和资本市场线图
plt.figure(figsize=(10, 6))
plt.scatter(pvols, prets, c=(prets - 0.01) / pvols, marker='.', cmap='coolwarm')
plt.plot(evols, erets, 'b', lw=4.0) 
cx = np.linspace(0.0, 0.3)
plt.plot(cx, opt[0] + opt[1] * cx, 'r', lw=1.5)
plt.plot(opt[2], f(opt[2]), 'y*', markersize=15.0)
plt.axhline(0, color='k', ls='--', lw=2.0)
plt.axvline(0, color='k', ls='--', lw=2.0)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')