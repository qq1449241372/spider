# 爬取一冶外网信息
import requests
import re
currentPage=1
url=f'http://www.cfmcc.com/eportal/ui?pageId=471529&currentPage={currentPage}&moduleId=22d8b0699a3e44ebb164aca3e2d82d88'
data={"filter_LIKE_TITLE": "资产"}

resp=requests.post(url,data)
# 页面内容
page_content=resp.text
# print(page_content)
# obj=re.compile(r'<li><a href="(?P<url>.*?)" target="_blank"><h2>(?P<title>.*?)</h2><p>(?P<content>.*?)</p><span>.*?</span></a></li>',re.S)
obj=re.compile(r'<li>.*?<a href="(?P<url>.*?)".*?target="_blank".*?>.*?<h2>(?P<title>.*?)</h2>.*?<p>(?P<content>.*?)</p>.*?<span>(?P<date>.*?)</span>.*?</a>.*?</li>',re.S)
result=obj.finditer(page_content)
article_list=[]
for it in result: 
  # print(it.group())
  url=it.group("url")
  title=it.group("title")
  # content=it.group("content")
  date=it.group("date")
  article_list=[url,title,date]
  print(article_list)
print('over')
resp.close()
