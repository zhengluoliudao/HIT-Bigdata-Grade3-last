# =============================================================================
# 3.1 获取百度新闻网页源代码
# =============================================================================

import requests
url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'
res = requests.get(url).text
print(res)

import requests
headers = {'User-Agent':''} # 请通过在谷歌浏览器网址中输入about:version查找
url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'
res = requests.get(url, headers=headers).text
print(res)

# =============================================================================
# 4.1 findall()函数
# =============================================================================

import re
content = 'Welcome to Python for Finance on May 26 at 19 pm by Huang 20'
result = re.findall('\d\d', content)
result

# 获取列表中某个元素
result[0]
result[1]
result[2]

# 更简单的遍历方法
for i in range(len(result)):
    print(result[i])

# =============================================================================
# 4.2 非贪婪匹配之(.*?)
# =============================================================================

# 结合findall()函数和非贪婪匹配(.*?)
import re
res = '文本A百度新闻文本B'
source = re.findall('文本A(.*?)文本B', res)
source

import re
res = '文本A百度新闻文本B'
p_source = '文本A(.*?)文本B'
source = re.findall(p_source, res)
source

# 有多个符合非贪婪匹配(.*?)的内容
import re
res = '文本A百度新闻文本B，新闻标题文本A新浪财经文本B，文本A搜狗新闻文本B新闻网址'
p_source = '文本A(.*?)文本B'
source = re.findall(p_source, res)
source

# 非贪婪匹配(.*?)的实战操作
import re
res = '<p class="c-author">新浪&nbsp;&nbsp;17分钟前</p>'
p_info = '<p class="c-author">(.*?)</p>'
info = re.findall(p_info, res)
info

# =============================================================================
# 4.3 非贪婪匹配之.*?
# =============================================================================

# 结合findall()函数和非贪婪匹配(.*?)与.*?
import re
res = '<h3>文本C<变化的网址>文本D新闻标题</h3>'
p_title = '<h3>文本C.*?文本D(.*?)</h3>'
title = re.findall(p_title, res)
title

# 非贪婪匹配.*?的实战操作
# 获取新闻标题
import re
res = '<h3 class="c-title"><a href="网址" data-click="{英文&数字}" target="_blank">"投资者提问：四月三十的"<em>新闻</em>"采访拍视频没。啥时候"<em>央视</em>"播出"</a>'
p_title = '<h3 class="c-title">.*?>"(.*?)"</a>'
title = re.findall(p_title, res)
title

# 获取新闻链接(练习)
import re
res = '<h3 class="c-title"><a href="网址" data-click="{英文&数字}" target="_blank">"投资者提问：四月三十的"<em>新闻</em>"采访拍视频没。啥时候"<em>央视</em>"播出"</a>'
p_href = '<h3 class="c-title"><a href="(.*?)"'
href = re.findall(p_href, res)
href

# =============================================================================
# 4.4 自动考虑换行的修饰符re.S
# =============================================================================

# 结合findall()函数、非贪婪匹配和re.S
import re
res = '''文本A
      百度新闻文本B'''
p_source = '文本A(.*?)文本B'
source = re.findall(p_source, res, re.S)
source

# 修饰符re.S的实战操作
import re
res = '''<h3 class="c-title">
 <a href="https://baijiahao.baidu.com/s?id=1631161702623128831&amp;wfr=spider&amp;for=pc"
    data-click="{
      英文&数字
      }"
                target="_blank"
    >
      <em>阿里巴巴</em>代码竞赛现全球首位AI评委 能为代码质量打分
    </a>
'''

p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
href = re.findall(p_href, res, re.S)
title = re.findall(p_title, res, re.S)
href
title

# =============================================================================
# 4.5 文本初步清洗
# =============================================================================

# strip()函数清除换行符\n和空格字符
title = ['\n      <em>阿里巴巴</em>代码竞赛现全球首位AI评委 能为代码质量打分\n    ']
title[0] = title[0].strip()
title

# sub()函数清洗获得的无效内容
# sub()函数的使用范例1
title = ['<em>阿里巴巴</em>代码竞赛现全球首位AI评委 能为代码质量打分']
title[0] = re.sub('<em>', '', title[0])
title[0] = re.sub('</em>', '', title[0])
title

# sub()函数的使用范例1
import re
title = ['<em>阿里巴巴</em>代码竞赛现全球首位AI评委 能为代码质量打分']
title[0] = re.sub('<.*?>', '', title[0])
title

# 结合sub()函数与中括号[]
name = ['*Python金融大数据分析']
name[0] = re.sub('[*]', '', name[0])
name
