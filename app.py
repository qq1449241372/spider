from os import spawnl
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
import config
from chaojiying import Chaojiying_Client
import time
import datetime
import csv
from func import get_depart_by_name

now_date = datetime.datetime.now().strftime('%Y-%m-%d')
created_time=datetime.datetime.now().strftime('%Y-%m-%d%H-%M-%S')
# print(created_time)
web=Chrome()
#打开登录界面 
web.get('http://is.cfmcc.com/OA/MainPage.aspx')
# 处理验证码
# img=web.find_element_by_xpath('//*[@id="wrapper"]/div/table/tbody/tr/td[3]/img').screenshot_as_png
# chaojiying=Chaojiying_Client(config.chaojiying_username, config.chaojiying_pwd, config.chaojiying_softid)
# dic=chaojiying.PostPic(img,1902)
# verify_code=dic['pic_str']
# 填入登录信息
web.find_element_by_xpath('//*[@id="txtUser"]').send_keys(config.username)
web.find_element_by_xpath('//*[@id="txtPwd"]').send_keys(config.pwd)
# web.find_element_by_xpath('//*[@id="txtCode"]').send_keys(verify_code)
# 暂停
time.sleep(3)
# 点击登录
web.find_element_by_xpath('//*[@id="Button1"]').click()
# 跳转至公共信息链接
web.get('http://is.cfmcc.com/OA/SysFolder/AppFrame/AppQuery.aspx?tblName=Q_WebNews_Query&condition=CatCode%20like%20[QUOTES]04%[QUOTES]')
time.sleep(1.5)
# 填入搜索信息
web.find_element_by_xpath('//*[@id="CorpName"]').send_keys(config.query_copm)
# 清除日期 readonly js脚本
js0='document.getElementById("IssueTime_0").removeAttribute("readonly")'
js1='document.getElementById("IssueTime_1").removeAttribute("readonly")'
# 执行脚本
web.execute_script(js0)
web.execute_script(js1)
web.find_element_by_xpath('//*[@id="IssueTime_0"]').send_keys(config.query_date0)
web.find_element_by_xpath('//*[@id="IssueTime_1"]').send_keys(config.query_date1)
# 选择页码
web.find_element_by_xpath('//*[@id="griddiv"]/div/div[8]/div[1]/div[1]/select/option[7]').click()
# 暂停
time.sleep(1)
#遍历页面所有数据
tr_list=web.find_elements_by_xpath('//*[@id="flex1"]/tbody/tr')
url_list=[]
for tr in tr_list[0:20]:
  # 文章id
  id=tr.id
  #标题 
  title=tr.find_element_by_xpath('./td[2]/div/a').text
  # 文章链接
  url=tr.find_element_by_xpath('./td[2]/div/a').get_attribute('href')
  url_list.append(url)
print(url_list)
# 写入函数
f=open(f'./data/{created_time}.csv',mode="w",newline='')
csvWriter=csv.writer(f)
# 写入时间
csvWriter.writerow(['序号','标题','作者','部门','发布时间','点击次数','链接'])
def get_author(a1,a2):
  if(len(a1)>=len(a2)) :
    return a2
  if(len(a1)<len(a2)):
    return a1
index=0
# 遍历文章url获取数据
for url in url_list:  
  index=index+1
  try:
    web.get(url)
    info=web.find_element_by_xpath('//*[@id="content"]/div[1]')
    div=web.find_element_by_xpath('//*[@id="content"]/div[2]')
    # 查找所有p标签
    p_list=div.find_elements_by_xpath('p')  
    # 去除空内容所有p标签
    new_p_list=[p for p in p_list if p.text.strip()!='']
    # 最后一个p标签
    last_p=new_p_list[-1]
    # 遍历last_p中<span>
    span_list=last_p.find_elements_by_xpath('span')
    #根据p标签猜测的作者
    author_p=last_p.text.replace('资产公司', '').replace(' ', '').strip() 
    # 查找最后一个<p>中<span>的内容
    
    # new_span_list=[span for span in span_list if span.text.strip!='']
    # # 根据span标签猜测的作者
    # author_span=new_span_list[-1].text.replace('资产公司', '').replace(' ', '').strip() 
    #获取对应数据
    title=web.find_element_by_xpath('//*[@id="content"]/h2').text
    author=author_p
    depart=get_depart_by_name(author)
    date=info.text.split(' ')[0].replace('发布日期：', '').strip()
    click=info.text.split(' ')[1].replace('点击次数：', '').strip()
    article_info=[index,title,author,depart,date,click,url]
    print(article_info) 
    csvWriter.writerow(article_info)
    print('write done!')
  except Exception as e:
    # 写入错误信息
    errinfo=[index,title,author,e,date,click,url]
    print(errinfo) 
    csvWriter.writerow(errinfo) 
    print('write done!')
web.close()