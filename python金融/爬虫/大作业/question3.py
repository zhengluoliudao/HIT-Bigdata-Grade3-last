'''
1)	运用 selenium 库从东方财富个股吧中获取上市公司 A 的网页源代码。
2)	编写正则表达式获取新闻标题、网址、 来源 和发布日期等信息。
3)	对获取的新闻信息进行简单的数据清洗。
4)	将数据信息保存到一个文本文件中。（除了最终的大作业报告，还需提交相应源代码以及txt文件）
'''
from selenium import webdriver
import re

def dongfang(company):
    f = open("./大作业/question3.txt", 'a+', encoding='UTF-8')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    url = 'http://so.eastmoney.com/news/s?keyword=' + company
    browser.get(url)
    data = browser.page_source
    browser.quit()
    
    f.write(data)

    p_title = '<div class="news-item"><h3><a href=".*?">(.*?)</a>'
    p_href = '<div class="news-item"><h3><a href="(.*?)">.*?</a>'
    p_date = '<p class="news-desc">(.*?)</p>'
    title = re.findall(p_title,data)
    href = re.findall(p_href,data)
    date = re.findall(p_date,data,re.S)

    
    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[0]
        info = str(i+1) + '.' + title[i] + ' - '+ date[i]
        link = href[i]
        f.write(info)
        f.write(link)
        print(info)
        print(link)

companies = ['浪莎股份']
for i in companies:
    try:
        dongfang(i)
        print(i + '该公司东方财富网爬取成功')
    except:
        print(i + '该公司东方财富网爬取失败') 