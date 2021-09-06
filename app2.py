# -*- coding: UTF-8 -*-
# 爬取一冶外网信息q
import requests
import re
import config
import time
import csv
import datetime
from func import get_depart_by_name
# 程序开始时间
start=time.time()
now_date = datetime.datetime.now().strftime('%Y-%m-%d')
created_time=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
data={"filter_LIKE_TITLE": "资产"}
headers={
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}
# 正则规则
obj=re.compile(r'<li>.*?<a href="(?P<url>.*?)".*?target="_blank".*?>.*?<h2>(?P<title>.*?)</h2>.*?<p>(?P<content>.*?)</p>.*?<span>(?P<date>.*?)</span>.*?</a>.*?</li>',re.S)
info_list=[]
url_list=[]
article_list=[]
# 自定义异常
class valid_year(Exception):
  pass

try:
  # 循环页面
  for currentPage in range(1,10) :
    url=f'http://www.cfmcc.com/eportal/ui?pageId=471529&currentPage={currentPage}&moduleId=22d8b0699a3e44ebb164aca3e2d82d88'
    resp=requests.post(url,data)
    # 页面内容
    page_content=resp.text
    result=obj.finditer(page_content)
    # 遍历正则匹配结果
    for it in result: 
      url="http://www.cfmcc.com"+it.group("url")
      title=it.group("title")
      date=it.group("date").replace('[', '').replace(']', '')
      info_list=[title,date,url]
      year=re.findall(u"\d{4}",date)[0]
      if(year==f'{config.year}'):
        url_list.append(url)
        article_list.append(info_list)
        # print(info_list)
      else:
        raise valid_year()
except valid_year:
  pass
print(url_list,"\n")
print(f'{config.year}年资产公司外网文章数量: {len(url_list)}篇')
# 关闭连接
resp.close()
# 遍历文章url获取信息
# 写入函数
f=open(f'./data/资产外网_{created_time}.csv',mode="w",newline='')
csvWriter=csv.writer(f)
# 写入第一行
csvWriter.writerow(['序号','标题','作者','部门','发布时间','链接'])
obj2=re.compile(r'<span>作者：(?P<author>.*?)</span>',re.S)
index=0
for url in url_list:
  print(url)
  resp=requests.get(url,headers=headers)
  resp.encoding='utf-8'
  page_content=resp.text
  # print(page_content)
  result=obj2.finditer(page_content)
  for it in result:
    author=it.group('author')
  # print(author)
  depart=get_depart_by_name(author)
  article_list[index].insert(0,index+1)
  article_list[index].insert(2,author)
  article_list[index].insert(3,depart)
  print(article_list[index])
  csvWriter.writerow(article_list[index])
  print('write done!')
  index=index+1
# 关闭连接
resp.close()
end=time.time()
print('用时:%.2f秒'%(end-start))