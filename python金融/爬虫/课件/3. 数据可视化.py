# =============================================================================
# 1.1 matplotlib库
# =============================================================================

# 引入matplotlib库和matplotlib.pyplot字库
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

# =============================================================================
# 1.2 一维数据集
# =============================================================================

# 创建一维数据集
import numpy as np
np.random.seed(1000)
y = np.random.standard_normal(20)

# 按照给定的x和y值的图表
x = range(len(y))
plt.plot(x, y)

# 按照一维数组给出的数据集的图表
plt.plot(y)

# 按照给定的一维数组和附加方法的图表
plt.plot(y.cumsum())

# 无网格和相同轴刻度的图表
plt.plot(y.cumsum())
plt.grid(False) 
plt.axis('equal') 
#plt.axis([0, 20, -3, 1])

# 带有自定义坐标限制的图表
plt.plot(y.cumsum())
plt.xlim(-1, 20) 
plt.ylim(np.min(y.cumsum()) - 1, np.max(y.cumsum()) + 1) 

# 带有典型标签的图表
plt.figure(figsize=(10, 6)) 
plt.plot(y.cumsum(), 'b', lw=1.5) 
plt.plot(y.cumsum(), 'ro') 
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

# =============================================================================
# 1.3 二维数据集
# =============================================================================

# 创建二维数据集
np.random.seed(2000)
y = np.random.standard_normal((20, 2)).cumsum(axis=0)

# 常规二维数据集的图表
# 按照二维数组给出的数据集的图表
plt.figure(figsize=(10, 6)) 
plt.plot(y, lw=1.5) 
plt.plot(y, 'ro') 
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

# 带有注释图例的绘图
plt.figure(figsize=(10, 6)) 
plt.plot(y[:,0], lw=1.5, label='1st')
plt.plot(y[:,1], lw=1.5, label='2nd')
plt.plot(y, 'ro') 
plt.legend(loc=0) 
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

# 问题1：两个数据集可能有不同的刻度
# 包含两个不同刻度数据集的图表
y[:,0] = y[:,0] * 100
plt.figure(figsize=(10, 6)) 
plt.plot(y[:,0], lw=1.5, label='1st')
plt.plot(y[:,1], lw=1.5, label='2nd')
plt.plot(y, 'ro') 
plt.legend(loc=0) 
plt.xlabel('index')
plt.ylabel('value')
plt.title('A Simple Plot')

# 解决方法1：使用2个y轴（左/右）
fig, ax1 = plt.subplots()
plt.plot(y[:,0], 'b', lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.legend(loc=8) 
plt.xlabel('index')
plt.ylabel('value 1st')
plt.title('A Simple Plot')
ax2 = ax1.twinx()
plt.plot(y[:,1], 'g', lw=1.5, label='2nd')
plt.plot(y[:,1], 'ro')
plt.legend(loc=0) 
plt.ylabel('value 2nd')

# 解决方法2：使用两个子图（上/下，左/右）
plt.figure(figsize=(10, 6))
plt.subplot(211)
plt.plot(y[:,0], 'b', lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.legend(loc=0) 
plt.ylabel('value')
plt.title('A Simple Plot')
plt.subplot(212)
plt.plot(y[:,1], 'g', lw=1.5, label='2nd')
plt.plot(y[:,1], 'ro')
plt.legend(loc=0) 
plt.xlabel('index')
plt.ylabel('value')

# 问题2：可能以不同的方式可视化两组不同的数据。
# 组合线/点子图和柱状子图
plt.figure(figsize=(10, 6)) 
plt.subplot(121)
plt.plot(y[:,0], 'b', lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.legend(loc=0) 
plt.xlabel('index')
plt.ylabel('value')
plt.title('1st Data Set')
plt.subplot(122)
plt.bar(np.arange(len(y)), y[:,1], width=0.5, color='g', label='2nd')
plt.legend(loc=0) 
plt.xlabel('index')
plt.title('2nd Data Set')

# 练习
# 创建二维数据集
np.random.seed(2000)
y = np.random.standard_normal((20, 3)).cumsum(axis=0)

# 有三个子图的线/点图
plt.figure(figsize=(10, 6))
plt.subplot(221)
plt.plot(y[:,0], 'b', lw=1.5, label='1st')
plt.plot(y[:,0], 'ro')
plt.legend(loc=0) 
plt.ylabel('value')
plt.title('1st Data Set')
plt.subplot(222)
plt.plot(y[:,1], 'g', lw=1.5, label='2nd')
plt.plot(y[:,1], 'ro')
plt.legend(loc=0) 
plt.xlabel('index')
plt.ylabel('value')
plt.title('2nd Data Set')
plt.subplot(223)
plt.plot(y[:,2], 'y', lw=1.5, label='1st')
plt.plot(y[:,2], 'ro')
plt.legend(loc=0) 
plt.xlabel('index')
plt.ylabel('value')
plt.title('3rd Data Set')

# =============================================================================
# 1.4 其他绘图样式
# =============================================================================

# 创建二维数据集
np.random.seed(2000)
y = np.random.standard_normal((1000, 2))

# 散点图
# 运用plot()函数绘制的散点图
plt.figure(figsize=(10, 6))
plt.plot(y[:,0], y[:,1], 'ro')
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

# 运用scatter()函数绘制的散点图
plt.figure(figsize=(10, 6))
plt.scatter(y[:,0], y[:,1], marker='o')
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

# 具备第三维的散点图
c = np.random.randint(0, 10, len(y))

plt.figure(figsize=(10, 6))
plt.scatter(y[:,0], y[:,1], c=c, cmap='coolwarm', marker='o')
plt.colorbar()
plt.xlabel('1st')
plt.ylabel('2nd')
plt.title('Scatter Plot')

# 直方图
# 两个数据集的直方图
plt.figure(figsize=(10, 6))
plt.hist(y, label=['1st', '2nd'], bins=25)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')

# 两个数据集堆叠的直方图
plt.figure(figsize=(10, 6))
plt.hist(y, label=['1st', '2nd'], color=['b', 'g'], rwidth=0.8, stacked=True, bins=25)
plt.legend(loc=0)
plt.xlabel('value')
plt.ylabel('frequency')
plt.title('Histogram')

# 箱形图
# 两个数据集的箱型图
fig, ax=plt.subplots(figsize=(10, 6))
plt.boxplot(y)
plt.setp(ax, xticklabels=['1st', '2nd'])
plt.xlabel('data set')
plt.ylabel('value')
plt.title('Boxplot')

# =============================================================================
# 1.5 2D绘图实战
# =============================================================================

# Step1：引入数据库，定义需要求取积分的函数
from matplotlib.patches import Polygon
def func(x):
    return 0.5 * np.exp(x) + 1

# Step2：定义积分区间，生成必须的数值
a, b = 0.5, 1.5
x = np.linspace(0, 2)
y = func(x)

# Step3：绘制函数图形
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(x, y, 'b', linewidth=2)
plt.ylim(bottom=0)

# Step4：使用Polygon()函数生成阴影部分，表示积分面积
Ix = np.linspace(a, b)
Iy = func(Ix)
verts = [(a, 0)] + list(zip(Ix, Iy)) + [(b, 0)]
poly = Polygon(verts, facecolor='0.7', edgecolor='0.5')
ax.add_patch(poly)

# Step5：使用plt.text和plt.figtext在图表上添加数学公式和坐标轴标签
plt.text(0.5 * (a + b), 1, r"$\int_a^b f(x)\mathrm{d}x$", horizontalalignment='center', fontsize=20)
plt.figtext(0.9, 0.075, '$x$')
plt.figtext(0.075, 0.9, '$f(x)$')

# Step6：分别设置x和y轴刻度标签的位置，在图表上添加刻度标签和网格
ax.set_xticks((a, b))
ax.set_xticklabels(('$a$', '$b$'))
ax.set_yticks([func(a), func(b)])
ax.set_yticklabels(('$f(a)$', '$f(b)$'))

# =============================================================================
# 1.6 3D绘图
# =============================================================================

# 包含行权价的一维数组
strike = np.linspace(50, 150, 24)

# 包含到期日的一维数据
ttm = np.linspace(0.5, 2.5, 24)

# 生成二维坐标系
strike, ttm = np.meshgrid(strike, ttm)
strike[:2].round(1)

# 计算隐含波动率值
iv = (strike - 100) ** 2 / (100 * strike) / ttm
iv[:5, :3]

# 3D绘图
# 引入3D绘图功能
from mpl_toolkits.mplot3d import Axes3D

# 隐含波动率的3D曲面图
fig = plt.figure(figsize=(10, 6))
ax = fig.gca(projection='3d')
surf = ax.plot_surface(strike, ttm, iv, rstride=2, cstride=2, cmap=plt.cm.coolwarm, linewidth=0.5, antialiased=True)
ax.set_xlabel('strike')
ax.set_ylabel('time-to-manurity')
ax.set_zlabel('implied volatility')
fig.colorbar(surf, shrink=0.5, aspect=5)

# 隐含波动率的3D散点图
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(30, 60)
ax.scatter(strike, ttm, iv, zdir='z', s=25, c='b', marker='^')
ax.set_xlabel('strike')
ax.set_ylabel('time-to-manurity')
ax.set_zlabel('implied volatility')

# =============================================================================
# 2.1 Tushare库介绍
# =============================================================================

import tushare as ts

# 调取日线级别的数据
df = ts.get_hist_data('000002', start='2020-04-01', end='2020-04-30')
print(df)
# 如果想显示所有列
import pandas as pd
pd.set_option('display.max_columns', None)

# 调取分钟级别的数据
df = ts.get_hist_data('000002', ktype='5')
print(df)
 
# 调取实时行情数据
df = ts.get_realtime_quotes('000002')
print(df)
# 如果觉得列数过多，通过DataFrame选取列的方法选取相应的列
df = df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
print(df)
# 如果想同时调取多个股票代码的实时行情数据
df = ts.get_realtime_quotes(['000002', '000980', '000981'])
print(df)

# 调取分笔数据
df = ts.get_tick_data('000002', date='2020-05-20', src='tt')
print(df)
# 如果想调取当日分笔数据
df = ts.get_today_ticks('000002')  # 注意在非交易日无法用该代码
print(df)

# 调取指数信息
df = ts.get_index()
print(df)

# =============================================================================
# 2.2 股票基本数据
# =============================================================================

# 调取单天的前10分钟成交量
# 调取分笔数据
import tushare as ts
stock_code = '000002'  
current_date = '2020-05-18'
df = ts.get_tick_data(stock_code, date=current_date, src='tt')
print(df)

# 提取前10分钟信息
import pandas as pd
df['time'] = pd.to_datetime(current_date + ' ' + df['time'])
t = pd.to_datetime(current_date).replace(hour=9, minute=40)
df_10 = df[df.time <= t]
print(df_10)

# 计算前十分钟成交量
vol = df_10.volume.sum()
print(vol)

# 调取股价涨跌幅及多天的前10分钟成交量
# 调取股价涨跌幅
import tushare as ts
stock_code = '000002'
stock_name = '万科A'
start_date = '2020-01-01'  
end_date = '2020-03-31'
stock_k = ts.get_hist_data(stock_code, start=start_date, end=end_date) 
stock_k[['p_change']]

# 调取多天的前10分钟成交量
import tushare as ts
import pandas as pd
stock_table = pd.DataFrame()
for current_date in stock_k.index:
    current_k_line = stock_k.loc[current_date]

    # 调取current_date的前10分钟成交量
    df = ts.get_tick_data(stock_code, date=current_date, src='tt')
    df['time'] = pd.to_datetime(current_date + ' ' + df['time'])
    t = pd.to_datetime(current_date).replace(hour=9, minute=40)
    df_10 = df[df.time <= t]
    vol = df_10.volume.sum()  

    # 将数据信息放入字典中
    current_stock_info = {
        '名称': stock_name,
        '日期': pd.to_datetime(current_date),
        '股价涨跌幅(%)': current_k_line.p_change,
        '10分钟成交量': vol
    }
    stock_table = stock_table.append(current_stock_info, ignore_index=True)

stock_table = stock_table.set_index('日期')

# 调整列的顺序
order = ['名称', '股价涨跌幅(%)', '10分钟成交量']
stock_table = stock_table[order]
print(stock_table)

# =============================================================================
# 2.3 衍生变量数据
# =============================================================================

# 公式1：根据当日成交量和昨日成交量计算涨跌幅
stock_table['昨日10分钟成交量'] = stock_table['10分钟成交量'].shift(-1)
stock_table['成交量涨跌幅1(%)'] = (stock_table['10分钟成交量']-stock_table['昨日10分钟成交量'])/stock_table['昨日10分钟成交量']*100
print(stock_table)

# 屏蔽警告信息
import warnings
warnings.filterwarnings('ignore')

# 公式2：根据当日成交量和多日成交量的均值计算涨跌幅
ten_mean = stock_table['10分钟成交量'].sort_index().rolling(10, min_periods=1).mean()
stock_table['10分钟成交量10日均值'] = ten_mean
stock_table['成交量涨跌幅2(%)'] = (stock_table['10分钟成交量']-stock_table['10分钟成交量10日均值'])/stock_table['10分钟成交量10日均值']*100
print(stock_table)
 
# =============================================================================
# 2.4 相关性分析
# =============================================================================

from scipy.stats import pearsonr

# 成交量涨幅1(%)和股价涨幅的相关性分析
corr = pearsonr(abs(stock_table['股价涨跌幅(%)'][:-1]), abs(stock_table['成交量涨跌幅1(%)'][:-1]))
print('通过公式1计算的相关系数r值为' + str(corr[0]) + '，显著性水平P值为' + str(corr[1]))

# 成交量涨幅2(%)和股价涨幅的相关性分析
corr = pearsonr(abs(stock_table['股价涨跌幅(%)']), abs(stock_table['成交量涨跌幅2(%)']))
print('通过公式2相关系数r值为' + str(corr[0]) + '，显著性水平P值为' + str(corr[1]))

# =============================================================================
# 2.5 数据可视化呈现
# =============================================================================

# 数据优化
target_columns = ['名称', '股价涨跌幅(%)', '成交量涨跌幅2(%)']
final_table = stock_table[target_columns]
final_table = final_table.rename(columns={'成交量涨跌幅2(%)':'10分钟成交量涨跌幅(%)'})
# final_table.rename(columns={'成交量涨跌幅2(%)':'10分钟成交量涨跌幅(%)'}, inplace=True)
print(final_table)

# 数据可视化
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False

# 绘制第一个折线图：股价涨跌幅(%)
plt.plot(final_table.index, final_table['股价涨跌幅(%)'].apply(lambda x: abs(x)), label='股价涨跌幅(%)', color='red')
plt.legend(loc='upper left')  

# 绘制第二个折线图：10分钟成交量涨跌幅(%)
plt.twinx()
plt.plot(final_table.index, final_table['10分钟成交量涨跌幅(%)'].apply(lambda x: abs(x)), label='10分钟成交量涨跌幅(%)', linestyle='--')
plt.legend(loc='upper right')

# 设置图片标题，自动调整x坐标轴刻度的角度并展示图片
plt.title(stock_name)  
plt.gcf().autofmt_xdate()  
plt.show()

# =============================================================================
# 2.6 生成Excel工作簿
# =============================================================================

# xlwings库的引用和常规设置
import xlwings as xw
app = xw.App(visible=False)

# 创建新Excel工作簿
wb = app.books.add()

# 创建新工作表
sht = wb.sheets.add('新工作表')

# xlwings库与pandas库的交互（导入表格）
import pandas as pd
df = pd.DataFrame([[1, 2], [2, 4], [3, 6]], columns=['x', 'y'])
sht.range('A1').value = df

# xlings库与Matplotlib库的交互（导入图片）
import matplotlib.pyplot as plt
fig = plt.figure()
x = [1, 2, 3]
y = [2, 4, 6]
plt.plot(x, y)
sht.pictures.add(fig, name='图片1', update=True, left=200)

# 保存生成的Excel工作簿
wb.save(r'E:\text.xlsx')
#wb.save('E:\\text.xlsx')
wb.close()  
app.quit()  

# 打开已有Excel工作簿
app.books.open(r'E:\text.xlsx')
#app.books.open('E:\\text.xlsx')

# 选取单个工作表
sht = wb.sheets['新工作表']

# 实战：导出金融数据和图表至Excel工作簿
# 1)设置Excel程序在后台运行
import xlwings as xw
app = xw.App(visible=False)

# 2)创建新Excel工作簿并命名为wb
wb = app.books.add()

# 3)创建新Excel工作表并命名为stock_name
sht = wb.sheets.add(stock_name)

# 4)将final_table金融数据导出到Excel中
sht.range('A1').value = final_table

# 5)将可视化图表fig导出到Excel当中
import matplotlib.pyplot as plt
fig = plt.figure()  
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False  

# 绘制第一个折线图：股价涨跌幅(%)
plt.plot(final_table.index, final_table['股价涨跌幅(%)'].apply(lambda x: abs(x)), label='股价涨跌幅(%)', color='red')
plt.legend(loc='upper left')  # 设置图例位置

# 绘制第二个折线图：10分钟成交量涨跌幅(%)
plt.twinx()  # 生成双坐标轴
plt.plot(final_table.index, final_table['10分钟成交量涨跌幅(%)'].apply(lambda x: abs(x)), label='10分钟成交量涨跌幅(%)', linestyle='--')
plt.legend(loc='upper right')

# 设置图片标题，自动调整x坐标轴刻度的角度并展示图片
plt.title(stock_name) 
plt.gcf().autofmt_xdate() 

sht.pictures.add(fig, name='图1', update=True, left=300)

# 6)保存生成的Excel工作簿
wb.save('金融数据分析及可视化.xlsx')
wb.close()
app.quit()

print('金融数据分析及可视化于Excel生成完毕')

# =============================================================================
# 2 金融数据分析及可视化全部代码
# =============================================================================

# 1)获取股票基本数据
# 调取股价涨跌幅
import tushare as ts

stock_code = '000002'
stock_name = '万科A'
start_date = '2020-01-01'  
end_date = '2020-03-31'
stock_k = ts.get_hist_data(stock_code, start=start_date, end=end_date) 
stock_k[['p_change']]

# 调取多天的前10分钟成交量
import pandas as pd

stock_table = pd.DataFrame()
for current_date in stock_k.index:
    current_k_line = stock_k.loc[current_date]

    # 调取current_date的前10分钟成交量
    df = ts.get_tick_data(stock_code, date=current_date, src='tt')
    df['time'] = pd.to_datetime(current_date + ' ' + df['time'])
    t = pd.to_datetime(current_date).replace(hour=9, minute=40)
    df_10 = df[df.time <= t]
    vol = df_10.volume.sum()  

    # 将数据信息放入字典中
    current_stock_info = {
        '名称': stock_name,
        '日期': pd.to_datetime(current_date),
        '股价涨跌幅(%)': current_k_line.p_change,
        '10分钟成交量': vol
    }
    stock_table = stock_table.append(current_stock_info, ignore_index=True)

stock_table = stock_table.set_index('日期')

# 调整列的顺序
order = ['名称', '股价涨跌幅(%)', '10分钟成交量']
stock_table = stock_table[order]
print(stock_table)

# 2)获取衍生变量数据
# 公式1：根据当日成交量和昨日成交量计算涨跌幅
stock_table['昨日10分钟成交量'] = stock_table['10分钟成交量'].shift(-1)
stock_table['成交量涨跌幅1(%)'] = (stock_table['10分钟成交量']-stock_table['昨日10分钟成交量'])/stock_table['昨日10分钟成交量']*100
print(stock_table)

# 屏蔽警告信息
import warnings
warnings.filterwarnings('ignore')

# 公式2：根据当日成交量和多日成交量的均值计算涨跌幅
ten_mean = stock_table['10分钟成交量'].sort_index().rolling(10, min_periods=1).mean()
stock_table['10分钟成交量10日均值'] = ten_mean
stock_table['成交量涨跌幅2(%)'] = (stock_table['10分钟成交量']-stock_table['10分钟成交量10日均值'])/stock_table['10分钟成交量10日均值']*100
print(stock_table)

# 3)相关性分析
from scipy.stats import pearsonr

# 成交量涨幅1(%)和股价涨幅的相关性分析
corr = pearsonr(abs(stock_table['股价涨跌幅(%)'][:-1]), abs(stock_table['成交量涨跌幅1(%)'][:-1]))
print('通过公式1计算的相关系数r值为' + str(corr[0]) + '，显著性水平P值为' + str(corr[1]))

# 成交量涨幅2(%)和股价涨幅的相关性分析
corr = pearsonr(abs(stock_table['股价涨跌幅(%)']), abs(stock_table['成交量涨跌幅2(%)']))
print('通过公式2相关系数r值为' + str(corr[0]) + '，显著性水平P值为' + str(corr[1]))

# 数据优化
target_columns = ['名称', '股价涨跌幅(%)', '成交量涨跌幅2(%)']
final_table = stock_table[target_columns]
final_table = final_table.rename(columns={'成交量涨跌幅2(%)':'10分钟成交量涨跌幅(%)'})
# final_table.rename(columns={'成交量涨跌幅2(%)':'10分钟成交量涨跌幅(%)'}, inplace=True)
print(final_table)

# 4)数据可视化及生成Excel工作簿
import xlwings as xw

app = xw.App(visible=False)
wb = app.books.add()
sht = wb.sheets.add(stock_name)
sht.range('A1').value = final_table

# 创建可视化图表fig并导入Excel工作簿
import matplotlib.pyplot as plt

fig = plt.figure()  
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False  

# 绘制第一个折线图：股价涨跌幅(%)
plt.plot(final_table.index, final_table['股价涨跌幅(%)'].apply(lambda x: abs(x)), label='股价涨跌幅(%)', color='red')
plt.legend(loc='upper left')  # 设置图例位置

# 绘制第二个折线图：10分钟成交量涨跌幅(%)
plt.twinx()  # 生成双坐标轴
plt.plot(final_table.index, final_table['10分钟成交量涨跌幅(%)'].apply(lambda x: abs(x)), label='10分钟成交量涨跌幅(%)', linestyle='--')
plt.legend(loc='upper right')

# 设置图片标题，自动调整x坐标轴刻度的角度并展示图片
plt.title(stock_name) 
plt.gcf().autofmt_xdate() 

sht.pictures.add(fig, name='图1', update=True, left=300)

# 保存生成的Excel工作簿
wb.save('金融数据分析及可视化.xlsx')
wb.close()
app.quit()

print('金融数据分析及可视化于Excel生成完毕')