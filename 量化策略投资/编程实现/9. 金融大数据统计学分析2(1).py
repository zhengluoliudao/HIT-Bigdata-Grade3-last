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
raw = pd.read_csv('./历史金融时间序列数据.csv',index_col=0, parse_dates=True)
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

# =============================================================================
# 2.1 无监督学习
# =============================================================================

# 基本设置
import numpy as np
import pandas as pd
import datetime as dt
from pylab import mpl, plt
import warnings; warnings.simplefilter('ignore')

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

np.random.seed(1000)
np.set_printoptions(suppress=True, precision=4)

# 模拟数据
from sklearn.datasets.samples_generator import make_blobs
X, y = make_blobs(n_samples=250, centers=4, random_state=500, cluster_std=1.25)  

X[:5]  
X.shape  

y[:5]  
y.shape 

plt.figure(figsize=(10, 6))
plt.hist(X)

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], s=50)

# k均值聚类
from sklearn.cluster import KMeans  
model = KMeans(n_clusters=4, random_state=0)  
model.fit(X)  
y_kmeans = model.predict(X)  

y_kmeans[:12]  

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans,  cmap='coolwarm')

# 高斯混合
from sklearn.mixture import GaussianMixture
model = GaussianMixture(n_components=4, random_state=0)
model.fit(X)
y_gm = model.predict(X)

y_gm[:12]
(y_gm == y_kmeans).all()  

# =============================================================================
# 2.2 有监督学习
# =============================================================================

# 模拟数据
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, n_repeated=0, random_state=250)

X[:5]  
X.shape  

y[:5]  
y.shape  

plt.figure(figsize=(10, 6))
plt.hist(X)

plt.figure(figsize=(10, 6))
plt.scatter(x=X[:, 0], y=X[:, 1], c=y, cmap='coolwarm')

# 高斯朴素贝叶斯
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(X, y)
pred = model.predict(X)   

pred[:5]  
pred[:5] == y[:5]  

model.predict_proba(X).round(4)[:5] 

from sklearn.metrics import accuracy_score
accuracy_score(y, pred)  

# 绘制GNB正确和错误预测的散点图
Xc = X[y == pred]  
Xf = X[y != pred]  

plt.figure(figsize=(10, 6))
plt.scatter(x=Xc[:, 0], y=Xc[:, 1], c=y[y == pred], marker='o', cmap='coolwarm')  
plt.scatter(x=Xf[:, 0], y=Xf[:, 1], c=y[y != pred], marker='x', cmap='coolwarm') 
 
# 逻辑回归
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1)
model.fit(X, y)
pred = model.predict(X)

model.predict_proba(X).round(4)[:5]
accuracy_score(y, pred)

# 绘制LR正确和错误预测的散点图
Xc = X[y == pred]
Xf = X[y != pred]

plt.figure(figsize=(10, 6))
plt.scatter(x=Xc[:, 0], y=Xc[:, 1], c=y[y == pred], marker='o', cmap='coolwarm')
plt.scatter(x=Xf[:, 0], y=Xf[:, 1], c=y[y != pred], marker='x', cmap='coolwarm')

# 决策树
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=1)
model.fit(X, y)
pred = model.predict(X)

model.predict_proba(X).round(4)[:5]
accuracy_score(y, pred)

# 绘制DT正确和错误预测的散点图
Xc = X[y == pred]
Xf = X[y != pred]

plt.figure(figsize=(10, 6))
plt.scatter(x=Xc[:, 0], y=Xc[:, 1], c=y[y == pred], marker='o', cmap='coolwarm')
plt.scatter(x=Xf[:, 0], y=Xf[:, 1], c=y[y != pred], marker='x', cmap='coolwarm')

# 增大决策树的最大深度参数
print('{:>8s} | {:8s}'.format('depth', 'accuracy'))
print(20 * '-')
for depth in range(1, 7):
    model = DecisionTreeClassifier(max_depth=depth)
    model.fit(X, y)
    acc = accuracy_score(y, model.predict(X))
    print('{:8d} | {:8.2f}'.format(depth, acc))

# 深度神经网络
from sklearn.neural_network import MLPClassifier
model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=2 * [75], random_state=10)
model.fit(X, y)
pred = model.predict(X)

model.predict_proba(X).round(4)[:5]
accuracy_score(y, pred)

# 用TensorFlow实现DNN
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)  
fc = [tf.contrib.layers.real_valued_column('features')]  
model = tf.contrib.learn.DNNClassifier(hidden_units=5 * [250], n_classes=2, feature_columns=fc)  

def input_fn():  
    fc = {'features': tf.constant(X)}
    la = tf.constant(y)
    return fc, la

model.fit(input_fn=input_fn, steps=100)  
model.evaluate(input_fn=input_fn, steps=1)  
pred = np.array(list(model.predict(input_fn=input_fn)))  
pred[:10]  

model.fit(input_fn=input_fn, steps=750)  
model.evaluate(input_fn=input_fn, steps=1)  

# 训练-测试分离：支持向量机
# 将数据集拆分为训练数据和测试数据
from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.33, random_state=0)

# 实例化模型对象
from sklearn.svm import SVC
model = SVC(C=1, kernel='linear')

# 训练：将模型对象与训练数据拟合
model.fit(train_x, train_y)  
pred_train = model.predict(train_x)  

accuracy_score(train_y, pred_train) 

# 测试：根据测试数据预测分类
pred_test = model.predict(test_x) 
 
test_y[:5] == pred_test[:5]  
accuracy_score(test_y, pred_test)  

# 绘制SVM正确和错误预测的散点图
test_c = test_x[test_y == pred_test]
test_f = test_x[test_y != pred_test]

plt.figure(figsize=(10, 6))
plt.scatter(x=test_c[:, 0], y=test_c[:, 1], c=test_y[test_y == pred_test], marker='o', cmap='coolwarm')
plt.scatter(x=test_f[:, 0], y=test_f[:, 1], c=test_y[test_y != pred_test], marker='x', cmap='coolwarm')

# 将原始数据变换为分类特征
bins = np.linspace(-4.5, 4.5, 50)
Xd = np.digitize(X, bins=bins)
Xd[:5]

# 设置不同的核心选项
train_x, test_x, train_y, test_y = train_test_split(Xd, y, test_size=0.33, random_state=0)

print('{:>8s} | {:8s}'.format('kernel', 'accuracy'))
print(20 * '-')
for kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
    model = SVC(C=1, kernel=kernel)
    model.fit(train_x, train_y)
    acc = accuracy_score(test_y, model.predict(test_x))
    print('{:>8s} | {:8.3f}'.format(kernel, acc))
    
# =============================================================================
# 2.3 实战案例
# =============================================================================

# 实战数据
# 导入数据
import pandas as pd
df = pd.read_excel('./客户信息及违约表现.xlsx')

# 提取特征变量和目标变量
X = df.drop(columns='是否违约')
# X = df.drop('是否违约', axis=1)
y = df['是否违约']

# 模型搭建
# 将数据集拆分为训练数据和测试数据
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# 实例化模型对象
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=3)

# 训练：将模型对象与训练数据拟合
clf = clf.fit(X_train, y_train)
print(clf)  

# 模型预测
# 测试：根据测试数据预测分类
y_pred = clf.predict(X_test)
print(y_pred)

# 预测不违约&违约结果比较
a = pd.DataFrame()  
a['预测值'] = list(y_pred)
a['实际值'] = list(y_test)
print(a.tail())

from sklearn.metrics import accuracy_score
score = accuracy_score(y_pred, y_test)

# 预测不违约&违约概率
y_pred_proba = clf.predict_proba(X_test)

print(y_pred_proba[:5,:])  
print(y_pred_proba[:5, 0])
print(y_pred_proba[:5, 1])

# 模型预测效果评估
# ROC曲线
from sklearn.metrics import roc_curve
fpr, tpr, thres = roc_curve(y_test.values, y_pred_proba[:, 1])

a = pd.DataFrame()
a['阈值'] = list(thres)
a['假警报率'] = list(fpr)
a['命中率'] = list(tpr)
print(a)

# 绘制ROC曲线
import matplotlib.pyplot as plt
plt.plot(fpr, tpr)
plt.show()

# AUC值
from sklearn.metrics import roc_auc_score
score = roc_auc_score(y_test.values, y_pred_proba[:, 1])
print(score)

















