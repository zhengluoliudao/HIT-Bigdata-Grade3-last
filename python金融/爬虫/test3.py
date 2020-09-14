import re 
from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

def search(company):
    browser.get('https://finance.sina.com.cn/realstock/company/' + company + '/nc.shtml')
    data = browser.page_source

    p_price = '<div id="price" class=".*?">(.*?)</div>'
    price = re.findall(p_price, data)
    print(price)


companies = ['sh000001', 'sh000002', 'sh000003', 'sh000004', 'sh000005']
for i in companies:
    try:
        search(i)
        print(i + '爬取成功')
    except:
        print(i + '爬取失败')