# =============================================================================
# 1.2 贝叶斯回归
# =============================================================================

# 基本设置
import numpy as np
from pylab import mpl, plt

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

# 模拟数据
np.random.seed(1000)
x = np.linspace(0, 10, 500)
y = 4 + 2 * x + np.random.standard_normal(len(x)) * 2

# 线性回归
reg = np.polyfit(x, y, 1)
reg

# 绘制OLS回归线
plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=y, marker='v', cmap='coolwarm')
plt.plot(x, reg[1] + reg[0] * x, lw=2.0)
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')

# 贝叶斯回归
import pymc3 as pm
with pm.Model() as model:
    alpha = pm.Normal('alpha', mu=0, sd=20)  
    beta = pm.Normal('beta', mu=0, sd=10)  
    sigma = pm.Uniform('sigma', lower=0, upper=10)  
    y_est = alpha + beta * x  
    likelihood = pm.Normal('y', mu=y_est, sd=sigma, observed=y)  
    
    start = pm.find_MAP()  
    step = pm.NUTS()  
    trace = pm.sample(100, tune=1000, start=start, progressbar=True) 

# 贝叶斯回归结果
pm.summary(trace) 
trace[0] 

# 绘制后验分布及轨迹图
pm.traceplot(trace)

# 绘制贝叶斯回归线
plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=y, marker='v', cmap='coolwarm')
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
for i in range(len(trace)):
    plt.plot(x, trace['alpha'][i] + trace['beta'][i] * x)

# =============================================================================
# 1.3 实战演练
# =============================================================================

# 历史金融时间序列数据基本特征
# 导入数据
import pandas as pd
raw = pd.read_csv(r'./历史金融时间序列数据.csv',index_col=0, parse_dates=True)
data = raw[['GDX', 'GLD']].dropna()
data = data / data.iloc[0]

# 查看数据信息
data.info()
# data.iloc[-1] / data.iloc[0] - 1 
data.corr()

# 绘制GDX和GLD规范化价格数据的线图
data.plot(figsize=(10, 6))

# 绘制GDX和GLD规范化价格的散点图
data.index[:3]
mpl_dates = mpl.dates.date2num(data.index.to_pydatetime())  
mpl_dates[:3]

plt.figure(figsize=(10, 6))
plt.scatter(data['GDX'], data['GLD'], c=mpl_dates, marker='o', cmap='coolwarm')
plt.xlabel('GDX')
plt.ylabel('GLD')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250), format=mpl.dates.DateFormatter('%d %b %y'))

# 贝叶斯回归
# 回归模型和MCMC采样代码
import pymc3 as pm
with pm.Model() as model:
    alpha = pm.Normal('alpha', mu=0, sd=20)
    beta = pm.Normal('beta', mu=0, sd=20)
    sigma = pm.Uniform('sigma', lower=0, upper=50)
    y_est = alpha + beta * data['GDX'].values
    likelihood = pm.Normal('GLD', mu=y_est, sd=sigma, observed=data['GLD'].values)
    
    start = pm.find_MAP()
    step = pm.NUTS()
    trace = pm.sample(250, tune=2000, start=start, progressbar=True)
    
# 贝叶斯回归结果
pm.summary(trace) 

# 绘制后验分布及轨迹图
pm.traceplot(trace)

# 绘制贝叶斯回归线
plt.figure(figsize=(10, 6))
plt.scatter(data['GDX'], data['GLD'], c=mpl_dates, marker='o', cmap='coolwarm')
plt.xlabel('GDX')
plt.ylabel('GLD')
for i in range(len(trace)):
    plt.plot(data['GDX'], trace['alpha'][i] + trace['beta'][i] * data['GDX'])
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250), format=mpl.dates.DateFormatter('%d %b %y'))

# =============================================================================
# 1.4 随时更新估计值
# =============================================================================

# 指定随机游走的贝叶斯回归模型
from pymc3.distributions.timeseries import GaussianRandomWalk
subsample_alpha = 50
subsample_beta = 50

import pymc3 as pm
model_randomwalk = pm.Model()
with model_randomwalk:
    sigma_alpha = pm.Exponential('sig_alpha', 1. / .02, testval=.1)  
    sigma_beta = pm.Exponential('sig_beta', 1. / .02, testval=.1)  
    alpha = GaussianRandomWalk('alpha', sigma_alpha ** -2, shape=int(len(data) / subsample_alpha))  
    beta = GaussianRandomWalk('beta', sigma_beta ** -2, shape=int(len(data) / subsample_beta))  
    alpha_r = np.repeat(alpha, subsample_alpha)  
    beta_r = np.repeat(beta, subsample_beta)  
    regression = alpha_r + beta_r * data['GDX'].values[:1950]  
    sd = pm.Uniform('sd', 0, 20)  
    likelihood = pm.Normal('GLD', mu=regression, sd=sd, observed=data['GLD'].values[:1950])  
    
# 指定随机游走的MCMC采样
import scipy.optimize as sco
with model_randomwalk:
    start = pm.find_MAP(vars=[alpha, beta], fmin=sco.fmin_l_bfgs_b)
    step = pm.NUTS(scaling=start)
    trace_rw = pm.sample(250, tune=1000, start=start, progressbar=True)
    
# 回归结果
pm.summary(trace_rw).head()  

# 收集参数估计值
import datetime as dt
sh = np.shape(trace_rw['alpha'])  
#sh  
part_dates = np.linspace(min(mpl_dates), max(mpl_dates), sh[1])  
index = [dt.datetime.fromordinal(int(date)) for date in part_dates]  
alpha = {'alpha_%i' % i: v for i, v in enumerate(trace_rw['alpha']) if i < 20}  
beta = {'beta_%i' % i: v for i, v in enumerate(trace_rw['beta']) if i < 20}  

df_alpha = pd.DataFrame(alpha, index=index)  
df_beta = pd.DataFrame(beta, index=index)  

# 绘制轨迹图
ax = df_alpha.plot(color='b', style='-.', legend=False, lw=0.7, figsize=(10, 6))
df_beta.plot(color='r', style='-.', legend=False, lw=0.7, ax=ax)
plt.ylabel('alpha/beta')

# 绘制贝叶斯回归线
plt.figure(figsize=(10, 6))
plt.scatter(data['GDX'], data['GLD'], c=mpl_dates, marker='o', cmap='coolwarm')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250), format=mpl.dates.DateFormatter('%d %b %y'))
plt.xlabel('GDX')
plt.ylabel('GLD')
x = np.linspace(min(data['GDX']), max(data['GDX']))
for i in range(sh[1]):  
    alpha_rw = np.mean(trace_rw['alpha'].T[i])
    beta_rw = np.mean(trace_rw['beta'].T[i])
    plt.plot(x, alpha_rw + beta_rw * x, '--', lw=0.7, color=plt.cm.coolwarm(i / sh[1]))
