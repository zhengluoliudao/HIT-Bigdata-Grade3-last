# 新浪财经数据挖掘实战的全部代码
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

def xinlang(company):
    f = open("./大作业/question2.txt", 'a+', encoding='UTF-8')

    url = 'https://search.sina.com.cn/?q=' + company + '&range=all&c=news&sort=time&ie=utf-8'
    res = requests.get(url, headers=headers, timeout=10).text
    f.write(res)

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
        info = str(i + 1) + '.' + title[i] + ' - ' + date[i]
        link = href[i]
        f.write(info + '\n')
        f.write(link + '\n')
        print(info)
        print(link)


companies = ['浪莎股份']
for i in companies:
    try:
        xinlang(i)
        print(i + '新浪财经新闻获取成功')
    except:
        print(i + '新浪财经新闻获取成功')

