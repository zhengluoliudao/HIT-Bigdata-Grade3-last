# =============================================================================
# 1.1 获取百度新闻网页源代码
# =============================================================================

import requests
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'
res = requests.get(url, headers=headers).text # 加上headers用来告诉网站这是通过一个浏览器进行的访问
print(res)

# =============================================================================
# 1.2 提取百度新闻信息
# =============================================================================

# 提取百度新闻的来源和日期
import re
p_info = '<p class="c-author">(.*?)</p>'
info = re.findall(p_info, res, re.S)
print(info)

# 提取百度新闻的网址
p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
href = re.findall(p_href, res, re.S)
print(href)

# 提取新闻的标题
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)
print(title)

# 提取百度新闻信息的总代吗
p_info = '<p class="c-author">(.*?)</p>'
info = re.findall(p_info, res, re.S)
p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
href = re.findall(p_href, res, re.S)
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)
# print(info)  # 常通过打印列表及列表长度，先看看获取的内容是否正确
# print(len(info))
# print(href)
# print(len(href))
# print(title)
# print(len(title))

# =============================================================================
# 1.3 百度新闻数据清洗并打印输出
# =============================================================================

# 百度新闻标题的清洗
for i in range(len(title)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])

# 百度新闻来源与和日期的清洗
source = []  
date = []
for i in range(len(info)):
    info[i] = re.sub('<.*?>', '', info[i])
    source.append(info[i].split('&nbsp;&nbsp;')[0])
    date.append(info[i].split('&nbsp;&nbsp;')[1])
    source[i] = source[i].strip()
    date[i] = date[i].strip()

# 百度新闻数据的打印输出
print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
print(href[i])
    
# 百度新闻数据清洗并打印输出的总代码
source = []  
date = []
for i in range(len(info)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    info[i] = re.sub('<.*?>', '', info[i])
    source.append(info[i].split('&nbsp;&nbsp;')[0])
    date.append(info[i].split('&nbsp;&nbsp;')[1])
    source[i] = source[i].strip()
    date[i] = date[i].strip()

    print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
    print(href[i])
    
# =============================================================================
# 百度新闻数据挖掘实战的全部代码
# =============================================================================

import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'
res = requests.get(url, headers=headers).text # 加上headers用来告诉网站这是通过一个浏览器进行的访问
# print(res)

p_info = '<p class="c-author">(.*?)</p>'
info = re.findall(p_info, res, re.S)
p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
href = re.findall(p_href, res, re.S)
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)
# print(info)  # 常通过打印列表及列表长度，先看看获取的内容是否正确
# print(len(info))
# print(href)
# print(len(href))
# print(title)
# print(len(title))

source = []  # 先创建两个空列表来储存等会分割后的来源和日期
date = []
for i in range(len(info)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    info[i] = re.sub('<.*?>', '', info[i])
    source.append(info[i].split('&nbsp;&nbsp;')[0])
    date.append(info[i].split('&nbsp;&nbsp;')[1])
    source[i] = source[i].strip()
    date[i] = date[i].strip()

    print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
    print(href[i])

# =============================================================================
# 2.1 批量获取多家公司百度新闻信息
# =============================================================================

# 自定义函数并调用函数
def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=' + company 
    print(url)

companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for i in companies:
    baidu(i)

# 批量获取多家公司百度新闻信息的全部代码
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=' + company  
    res = requests.get(url, headers=headers).text
    # print(res)
    p_info = '<p class="c-author">(.*?)</p>'
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    info = re.findall(p_info, res, re.S)
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

    source = []  
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        print(href[i])


companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for i in companies:  # 这个i只是个代号，可以换成其他内容
    baidu(i)
    print(i + '百度新闻爬取成功')

# =============================================================================
# 2.2 自动生成百度新闻数据报告文本文件
# =============================================================================

# open()函数打开文本文件
file = open('E:\\202004Python金融大数据分析\\测试.txt', 'a')
# write()函数和close()函数写入文本和关闭文本文件
file.write('1234567890')
file.close()

# 自动生成百度新闻数据报告文本文件的全部代码
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=' + company
    res = requests.get(url, headers=headers).text
    # print(res)

    p_info = '<p class="c-author">(.*?)</p>'
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    info = re.findall(p_info, res, re.S)
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        print(href[i])

    file1 = open('E:\\202004Python金融大数据分析\\数据挖掘报告.txt', 'a')
    file1.write(company + '数据挖掘completed！' + '\n' + '\n')
    for i in range(len(title)):
        file1.write(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')' + '\n')
        file1.write(href[i] + '\n')  # '\n'表示换行
    file1.write('——————————————————————————————' + '\n' + '\n')
    file1.close()


companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for i in companies:
    baidu(i)
    print(i + '百度新闻爬取成功')

print('数据获取及生成报告成功')

# =============================================================================
# 3.1 异常处理实战
# =============================================================================

# try/except()函数处理异常情况
companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for i in companies:
    try:
        baidu(i)
        print(i + '百度新闻爬取成功')
    except:
        print(i + '百度新闻爬取失败')

# =============================================================================
# 3.2 24小时数据挖掘实战
# =============================================================================

# while True()函数实现实时数据挖掘
while True:
    companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
    for i in companies:
        try:
            baidu(i)
            print(i + '百度新闻爬取成功')
        except:
            print(i + '百度新闻爬取失败')

# time.sleep()函数实现数据挖掘的间断运行
import time
while True:
    companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
    for i in companies:
        try:
            baidu(i)
            print(i + '百度新闻爬取成功')
        except:
            print(i + '百度新闻爬取失败')
    time.sleep(10800)

# 异常处理与24小时数据挖掘实战的全部代码
import requests
import re
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=' + company
    res = requests.get(url, headers=headers).text
    # print(res)

    p_info = '<p class="c-author">(.*?)</p>'
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    info = re.findall(p_info, res, re.S)
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()

        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        print(href[i])


while True:
    companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
    for i in companies:
        try:
            baidu(i)
            print(i + '百度新闻爬取成功')
        except:
            print(i + '百度新闻爬取失败')
    time.sleep(10800)  # 每10800秒运行一次，即3小时运行一次，注意缩进

# =============================================================================
# 4.1 按时间顺序爬取百度新闻
# =============================================================================

def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 把rtt参数换成4即是按时间排序，默认为1按焦点排序
    res = requests.get(url, headers=headers).text

# 按时间顺序爬取百度新闻的全部代码
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 把rtt参数换成4即是按时间排序，默认为1按焦点排序
    res = requests.get(url, headers=headers).text
    # print(res)

    p_info = '<p class="c-author">(.*?)</p>'
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    info = re.findall(p_info, res, re.S)
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        print(href[i])


companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for i in companies:  
    baidu(i)
    print(i + '百度新闻爬取成功')

# =============================================================================
# 4.2 批量爬取百度新闻的多页信息
# =============================================================================

# 批量爬取一家公司百度新闻的多页信息
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

# 批量爬取一家公司百度新闻的多页信息
def baidu(page):
    num = (page - 1) * 10
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=阿里巴巴&pn=' + str(num)
    res = requests.get(url, headers=headers).text
    # print(res)

    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    p_info = '<p class="c-author">(.*?)</p>'
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)
    info = re.findall(p_info, res, re.S)

    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()

        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')  # i是数字，所以要用str函数转换一下，且i是从0开始的序号，所以要写str(i+1)
        print(href[i])

for i in range(20):
    baidu(i+1)
    print('第' + str(i+1) + '页爬取成功')

# 批量爬取多家公司百度新闻的多页信息
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

# 爬取多个公司的多页, 可以给函数传入两个参数，供参考
def baidu(company, page):
    num = (page - 1) * 10
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company + '&pn=' + str(num)
    res = requests.get(url, headers=headers).text
    # print(res)

    p_info = '<p class="c-author">(.*?)</p>'
    info = re.findall(p_info, res, re.S)
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)

    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()

        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')  # i是数字，所以要用str函数转换一下，且i是从0开始的序号，所以要写str(i+1)
        print(href[i])


companies = ['阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for company in companies:
    for i in range(20):  # i是从0开始的序号，所以下面要写i+1，这里一共爬取了20页
        baidu(company, i+1)
        print(company + '第' + str(i+1) + '页爬取成功')


# =============================================================================
# 5.1 搜狗新闻数据挖掘实战
# =============================================================================

# 获取网页源代码
import requests
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url = 'https://news.sogou.com/news?mode=1&sort=0&fixrank=1&query=阿里巴巴&shid=djt1'
res = requests.get(url,headers=headers, timeout=10).text
# print(res)

# 提取搜狗新闻信息（标题、网址和发布日期）
import re
p_title = '<a href=".*?" id="uigs.*?" target="_blank">(.*?)</a>'
title = re.findall(p_title, res, re.S)
p_href = '<a href="(.*?)" id="uigs.*?" target="_blank">'
href = re.findall(p_href, res, re.S)
p_date = '<p class="news-from">.*?&nbsp;(.*?)</p>'
date = re.findall(p_date, res, re.S

# 搜狗新闻数据的清洗和打印输出
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])
    title[i] = re.sub('&.*?;', '', title[i])
    date[i] = re.sub('<.*?>', '', date[i])
    print(str(i+1) + '.' + title[i] + '-' + date[i])
    print(href[i])

# 批量获取多家公司的搜狗新闻信息
def sogou(company):
    url = 'https://news.sogou.com/news?mode=1&sort=0&fixrank=1&query=' + company + '&shid=djt1'
    res = requests.get(url,headers=headers, timeout=10).text

companies = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companies:
    try:
        sogou(i)
        print(i + '搜狗新闻爬取成功')
    except:
        print(i + '搜狗新闻爬取失败')

# 搜狗新闻数据挖掘实战的全部代码
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def sogou(company):
    url = 'https://news.sogou.com/news?mode=1&sort=0&fixrank=1&query=' + company + '&shid=djt1'
    res = requests.get(url,headers=headers, timeout=10).text
    # print(res)

    p_title = '<a href=".*?" id="uigs.*?" target="_blank">(.*?)</a>'
    title = re.findall(p_title, res, re.S)
    p_href = '<a href="(.*?)" id="u.*?" target="_blank">'
    href = re.findall(p_href, res, re.S)
    p_date = '<p class="news-from">.*?&nbsp;(.*?)</p>'
    date = re.findall(p_date, res, re.S)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        title[i] = re.sub('&.*?;', '', title[i])
        date[i] = re.sub('<.*?>', '', date[i])
        print(str(i+1) + '.' + title[i] + '-' + date[i])
        print(href[i])


companies = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companies:
    try:
        sogou(i)
        print(i + '搜狗新闻爬取成功')
    except:
        print(i + '搜狗新闻爬取失败')

# =============================================================================
# 5.2 新浪财经数据挖掘实战
# =============================================================================

# 获取新浪财经的网页源代码
import requests
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url = 'https://search.sina.com.cn/?q=' + company + '&range=all&c=news&sort=time&ie=utf-8'
res = requests.get(url,headers=headers, timeout=10).text
# print(res)

# 提取新浪财经信息（标题、网址和发布日期）
import re
p_title = '<h2><a href=".*?" target="_blank">(.*?)</a>'
title = re.findall(p_title, res, re.S)
p_href = '<h2><a href="(.*?)" target="_blank">'
href = re.findall(p_href, res, re.S)
p_date = '<span class="fgray_time">(.*?)</span>'
date = re.findall(p_date, res, re.S)

# 新浪财经数据的清洗和打印输出
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])
    date[i] = date[i].split(' ')[1]
    print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
    print(href[i])

# 批量获取多家公司的新浪财经信息
def xinlang(company):
    url = 'https://search.sina.com.cn/?q=' + company + '&range=all&c=news&sort=time&ie=utf-8'
    res = requests.get(url, headers=headers, timeout=10).text

companies = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companies:
    try:
        xinlang(i)
        print(i + '新浪财经新闻获取成功')
    except:
        print(i + '新浪财经新闻获取失败')
        
# 新浪财经数据挖掘实战的全部代码
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def xinlang(company):
    url = 'https://search.sina.com.cn/?q=' + company + '&range=all&c=news&sort=time&ie=utf-8'
    res = requests.get(url, headers=headers, timeout=10).text
    # print(res)

    p_title = '<h2><a href=".*?" target="_blank">(.*?)</a>'
    p_href = '<h2><a href="(.*?)" target="_blank">'
    p_date = '<span class="fgray_time">(.*?)</span>'
    title = re.findall(p_title, res)
    href = re.findall(p_href, res)
    date = re.findall(p_date, res)
    # print(title)
    # print(href)
    # print(date)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[1]
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])


companies = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companies:
    try:
        xinlang(i)
        print(i + '新浪财经新闻获取成功')
    except:
        print(i + '新浪财经新闻获取失败')

