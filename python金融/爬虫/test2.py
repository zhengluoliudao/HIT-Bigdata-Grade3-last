from selenium import webdriver
import time

def main():
    # 跳转网址获取源代码
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)

    browser.get('https://www.baidu.com')
    browser.find_element_by_xpath('//*[@id="kw"]').send_keys('python')
    browser.find_element_by_xpath('//*[@id="su"]').click()
    time.sleep(3)  
    data = browser.page_source
    print(data.encode("utf-8"))

    # 直接访问网址获取源代码
    browser.get("https://www.baidu.com/s?&wd=python&ie=utf-8")
    data = browser.page_source
    print(data.encode("utf-8"))

    time.sleep(5)
    browser.quit()

if __name__ == '__main__':
    main()