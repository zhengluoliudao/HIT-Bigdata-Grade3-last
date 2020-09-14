import tushare as ts

stock_code = '600137'
stock_name = '浪莎股份'
start_date = '2018-01-01'  
end_date = '2019-12-31'
stock_k = ts.get_hist_data(stock_code, start=start_date, end=end_date) 
stock_k[['p_change']]

# 调取多天的前10分钟成交量
import pandas as pd

stock_table = pd.DataFrame()
for current_date in stock_k.index:
    current_k_line = stock_k.loc[current_date]

    # 调取current_date的前20分钟成交量
    df = ts.get_tick_data(stock_code, date=current_date, src='tt')
    df['time'] = pd.to_datetime(current_date + ' ' + df['time'])
    t = pd.to_datetime(current_date).replace(hour=9, minute=50)
    df_10 = df[df.time <= t]
    vol = df_10.volume.sum()  

    # 将数据信息放入字典中
    current_stock_info = {
        '名称': stock_name,
        '日期': pd.to_datetime(current_date),
        '股价涨跌幅(%)': current_k_line.p_change,
        '20分钟成交量': vol
    }
    stock_table = stock_table.append(current_stock_info, ignore_index=True)

stock_table = stock_table.set_index('日期')

# 调整列的顺序
order = ['名称', '股价涨跌幅(%)', '20分钟成交量']
stock_table = stock_table[order]
print(stock_table)

# 2)获取衍生变量数据
# 公式1：根据当日成交量和昨日成交量计算涨跌幅
stock_table['昨日20分钟成交量'] = stock_table['20分钟成交量'].shift(-1)
stock_table['成交量涨跌幅1(%)'] = (stock_table['20分钟成交量']-stock_table['昨日20分钟成交量'])/stock_table['昨日20分钟成交量']*100
print(stock_table)

# 屏蔽警告信息
import warnings
warnings.filterwarnings('ignore')

# 公式2：根据当日成交量和多日成交量的均值计算涨跌幅
ten_mean = stock_table['20分钟成交量'].sort_index().rolling(20, min_periods=1).mean()
stock_table['20分钟成交量10日均值'] = ten_mean
stock_table['成交量涨跌幅2(%)'] = (stock_table['20分钟成交量']-stock_table['20分钟成交量10日均值'])/stock_table['20分钟成交量10日均值']*100
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

# 绘制第二个折线图：20分钟成交量涨跌幅(%)
plt.twinx()  # 生成双坐标轴
plt.plot(final_table.index, final_table['20分钟成交量涨跌幅(%)'].apply(lambda x: abs(x)), label='20分钟成交量涨跌幅(%)', linestyle='--')
plt.legend(loc='upper right')

# 设置图片标题，自动调整x坐标轴刻度的角度并展示图片
plt.title(stock_name) 
plt.gcf().autofmt_xdate() 

sht.pictures.add(fig, name='图1', update=True, left=300)