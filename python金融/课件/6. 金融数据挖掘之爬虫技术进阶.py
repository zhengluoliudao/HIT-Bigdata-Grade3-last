# =============================================================================
# 1.2 IP代理的使用方法
# =============================================================================

# IP代理的使用基础
import requests
proxy = 'IP代理地址'
proxies = {"http": "http://"+proxy, "https": "https://"+proxy}
url = 'https://httpbin.org/get'
res = requests.get(url, proxies=proxies).text
print(res)

# 从API链接的网页源代码中提取IP代理地址
proxy = requests.get('API链接').text
proxy = proxy.strip()  

# IP代理的使用实战的全部代码
import requests
proxy = requests.get('API链接').text
proxy = proxy.strip()
print(proxy)
proxies = {"http": "http://"+proxy, "https": "https://"+proxy}
url = 'https://httpbin.org/get'
res = requests.get(url, proxies=proxies).text
print(res)

# =============================================================================
# 2.1 网络数据挖掘的难点
# =============================================================================

# 获取新浪财经上证综合指数的网页源代码
import requests
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url = 'https://finance.sina.com.cn/realstock/company/sh000001/nc.shtml'
res = requests.get(url,headers=headers, timeout=10).text
print(res)

# =============================================================================
# 2.3 Selenium库的安装
# =============================================================================

# 小试牛刀
from selenium import webdriver
browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")

# =============================================================================
# 2.4 Selenium库的使用
# =============================================================================

# 网页基本操作
# 打开网页
from selenium import webdriver
browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")

# 关闭网页
browser.quit()

# 网页最大化
browser.maximize_window()

# 查找元素模拟鼠标和键盘操作
# XPath方法
browser.find_element_by_xpath('XPath内容')

from selenium import webdriver
browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")
browser.find_element_by_xpath('//*[@id="kw"]').clear()
browser.find_element_by_xpath('//*[@id="kw"]').send_keys('python')
browser.find_element_by_xpath('//*[@id="su"]').click()

# css_selector方法
browser.find_element_by_css_selector('css_selector内容')

from selenium import webdriver
browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")
browser.find_element_by_css_selector('#kw').clear()
browser.find_element_by_css_selector('#kw').send_keys('python')
browser.find_element_by_css_selector('#su').click()

# 获取网页真正源代码
# 跳转网址获取源代码
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get("https://www.baidu.com/")
browser.find_element_by_xpath('//*[@id="kw"]').send_keys('python')
browser.find_element_by_xpath('//*[@id="su"]').click()
time.sleep(3)  
data = browser.page_source
print(data)

# 直接访问网址获取源代码
from selenium import webdriver
browser = webdriver.Chrome()
browser.get("https://www.baidu.com/s?&wd=python&ie=utf-8")
data = browser.page_source
print(data)

# 无界面浏览器设置
# Chrome Headless方法
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get("https://www.baidu.com/s?&wd=python&ie=utf-8")
data = browser.page_source
print(data)
