# coding:utf-8

import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

def sogou(company):
    url = 'https://search.sina.com.cn/?q='+ company + '&range=all&c=news&sort=time&ie=utf-8'

    res = requests.get(url,headers=headers, timeout=10).text
    #print(res.encode('UTF-8'))

    p_title = '<a href=".*?" id="uigs.*?" target="_blank">(.*?)</a>'
    title = re.findall(p_title, res)
    p_href = '<a href="(.*?)" id="u.*?" target="_blank">'
    href = re.findall(p_href, res)
    p_date = '<p class="news-from">.*?&nbsp;(.*?)</p>'
    date = re.findall(p_date, res)

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