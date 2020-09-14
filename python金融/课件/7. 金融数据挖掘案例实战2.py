# =============================================================================
# 1. 新浪股票实时数据挖掘实战
# =============================================================================

# 获取新浪财经股票的网页源代码
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml')
data = browser.page_source
print(data)

# 获取新浪财经股票的网页源代码(无界面浏览器设置)
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml')
data = browser.page_source
print(data)

# 提取新浪财经股票实时数据信息（股价）
import re
p_price = '<div id="price" class=".*?">(.*?)</div>'
price = re.findall(p_price, data)
print(price)

# 新浪股票实时数据挖掘实战全部代码（股价）
from selenium import webdriver
import re
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml')
data = browser.page_source
# print(data)
browser.quit()

p_price = '<div id="price" class=".*?">(.*?)</div>'
price = re.findall(p_price, data)
print(price)

# 新浪股票实时数据挖掘实战全部代码（成交量）
from selenium import webdriver
import re
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml')
data = browser.page_source
# print(data)
browser.quit()

p_volume = '<th>成交量：</th>.*?<td>(.*?)</td>'
volume = re.findall(p_volume, data, re.S)
print(volume)

# 新浪股票实时数据挖掘实战全部代码（多家指数股价）
from selenium import webdriver
import re

def xinlang(index):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    url = 'http://finance.sina.com.cn/realstock/company/' + index + '/nc.shtml'
    browser.get(url)
    data = browser.page_source
    browser.quit()
    # print(data)
    
    p_price = '<div id="price" class=".*?">(.*?)</div>'
    price = re.findall(p_price, data)
    print(price)
    
indices = ['sh000001', 'sh000002', 'sh000003', 'sh000006', 'sh000009']
for i in indices:
    try:
        xinlang(i)
        print(i + '该指数新浪财经网爬取成功')
    except:
        print(i + '该指数新浪财经网爬取失败')     
    
# =============================================================================
# 2. 东方财富网数据挖掘实战
# =============================================================================

# 通过Requests库获取东方财富网页源代码（信息不全）
import requests
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url = 'http://so.eastmoney.com/news/s?keyword=阿里巴巴'
res = requests.get(url, headers=headers).text # 加上headers用来告诉网站这是通过一个浏览器进行的访问
print(res)

# 获取东方财富网页源代码(无界面浏览器设置)
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://so.eastmoney.com/news/s?keyword=阿里巴巴')
data = browser.page_source
print(data)

# 提取东方财富网数据信息（标题、网址和发布日期）
import re
p_title = '<div class="news-item"><h3><a href=".*?">(.*?)</a>'
title = re.findall(p_title,data)
p_href = '<div class="news-item"><h3><a href="(.*?)">.*?</a>'
href = re.findall(p_href,data)
p_date = '<p class="news-desc">(.*?)</p>'
date = re.findall(p_date,data,re.S)

# 东方财富网数据清洗和打印输出
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])
    date[i] = date[i].split(' ')[0]
    print(str(i+1) + '.' + title[i] + ' - '+ date[i])
    print(href[i])

# 批量获取多家公司的东方财富网信息
def dongfang(company):
    url = 'http://so.eastmoney.com/news/s?keyword=' + company
    browser.get(url)
    
companies = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companies:
    try:
        dongfang(i)
        print(i + '该公司东方财富网爬取成功')
    except:
        print(i + '该公司东方财富网爬取失败') 
   
# 东方财富网数据挖掘实战全部代码
from selenium import webdriver
import re

def dongfang(company):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    url = 'http://so.eastmoney.com/news/s?keyword=' + company
    browser.get(url)
    data = browser.page_source
    browser.quit()
    # print(data)

    p_title = '<div class="news-item"><h3><a href=".*?">(.*?)</a>'
    p_href = '<div class="news-item"><h3><a href="(.*?)">.*?</a>'
    p_date = '<p class="news-desc">(.*?)</p>'
    title = re.findall(p_title,data)
    href = re.findall(p_href,data)
    date = re.findall(p_date,data,re.S)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[0]
        print(str(i+1) + '.' + title[i] + ' - '+ date[i])
        print(href[i])

companies = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companies:
    try:
        dongfang(i)
        print(i + '该公司东方财富网爬取成功')
    except:
        print(i + '该公司东方财富网爬取失败') 

# =============================================================================
# 3 裁判文书网数据挖掘实战 
# =============================================================================

# 获取裁判文书网源代码（XPath方法）
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get('http://wenshu.court.gov.cn/')
browser.maximize_window()
browser.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[2]/input').clear()  # 清空原搜索框
browser.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[2]/input').send_keys('房地产')  # 在搜索框内模拟输入'房地产'三个字
browser.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[3]').click()  # 点击搜索按钮
time.sleep(10)  # 如果还是获取不到你想要的内容，你可以把这个时间再稍微延长一些，现在裁判文书网反爬非常厉害，所以可能等待也等不到刷新，所以这里主要给大家练习下模拟键盘鼠标操作
data = browser.page_source
browser.quit()
print(data)

# 获取裁判文书网源代码（css_selector方法）
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get('http://wenshu.court.gov.cn/')
browser.maximize_window()
browser.find_element_by_css_selector('#_view_1540966814000 > div > div.search-wrapper.clearfix > div.search-middle > input').clear()  # 清空原搜索框
browser.find_element_by_css_selector('#_view_1540966814000 > div > div.search-wrapper.clearfix > div.search-middle > input').send_keys('银行')  # 在搜索框内模拟输入'房地产'三个字
browser.find_element_by_css_selector('#_view_1540966814000 > div > div.search-wrapper.clearfix > div.search-rightBtn.search-click').click()  # 点击搜索按钮
time.sleep(10)  # 如果还是获取不到你想要的内容，你可以把这个时间再稍微延长一些，现在裁判文书网反爬非常厉害，所以可能等待也等不到刷新，所以这里主要给大家练习下模拟键盘鼠标操作
data = browser.page_source
browser.quit()
print(data)

# 获取裁判文书网源代码(无界面浏览器设置)
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=482b3aed8f61a6cb323d169ecd9358ca&s21=%E6%88%BF%E5%9C%B0%E4%BA%A7')
data = browser.page_source
print(data)

# =============================================================================
# 4. 巨潮资讯网数据挖掘实战
# =============================================================================

# 获取巨潮资讯网页源代码
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=理财')
data = browser.page_source
print(data)
browser.quit()

# 获取巨潮资讯网页源代码(无界面浏览器设置)
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=理财')
data = browser.page_source
print(data)
    
# 提取巨潮资讯网数据信息
import re
p_title = '<span title="" class="r-title">(.*?)</span>'
title = re.findall(p_title, data)
p_href = '<a target="_blank" href="(.*?)data-id='
href = re.findall(p_href, data)
p_date = '<span class="time">(.*?)</span>'
date = re.findall(p_date, data, re.S) 

# 巨潮资讯网数据清洗和打印输出
for i in range(len(title)):
    title[i] = re.sub(r'<.*?>', '', title[i])
    href[i] = 'http://www.cninfo.com.cn' + href[i]
    href[i] = re.sub('amp;', '', href[i])
    date[i] = date[i].strip()  # 清除空格和换行符
    date[i] = date[i].split(' ')[0]  # 只取“年月日”信息，不用“时分秒”信息
    print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
    print(href[i])

# 批量获取多个关键词的巨潮资讯网信息
def juchao(keyword):
    url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=' + keyword
    browser.get(url)
    
keywords = ['理财', '现金管理', '纾困']
for i in keywords:
    juchao(i)

# 巨潮资讯网数据挖掘实战的全部代码
from selenium import webdriver
import re

def juchao(keyword):
    browser = webdriver.Chrome()
    url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=' + keyword
    browser.get(url)
    data = browser.page_source
    # print(data)
    browser.quit()

    p_title = '<span title="" class="r-title">(.*?)</span>'
    p_href = '<a target="_blank" href="(.*?)data-id='
    p_date = '<span class="time">(.*?)</span>'
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data, re.S)  

    for i in range(len(title)):
        title[i] = re.sub(r'<.*?>', '', title[i])
        href[i] = 'http://www.cninfo.com.cn' + href[i]
        href[i] = re.sub('amp;', '', href[i])
        date[i] = date[i].strip()  # 清除空格和换行符
        date[i] = date[i].split(' ')[0]  # 只取“年月日”信息，不用“时分秒”信息
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

keywords = ['理财', '现金管理', '纾困']
for i in keywords:
    juchao(i)
# 该代码不完善，1)没有无界面浏览器设置；2)没有使用try/except语句，同学们可以试着完善。