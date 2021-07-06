from os import close
from requests.api import head
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import config
from chaojiying import Chaojiying_Client
import time
web=Chrome()
#打开登录界面 
web.get('http://is.cfmcc.com/OA/MainPage.aspx')
# 处理验证码
# img=web.find_element_by_xpath('//*[@id="wrapper"]/div/table/tbody/tr/td[3]/img').screenshot_as_png
# chaojiying=Chaojiying_Client('qq1449241372', 'abc123', '919268')
# dic=chaojiying.PostPic(img,1902)
# verify_code=dic['pic_str']
# 填入登录信息
web.find_element_by_xpath('//*[@id="txtUser"]').send_keys(config.username)
web.find_element_by_xpath('//*[@id="txtPwd"]').send_keys(config.pwd)
# web.find_element_by_xpath('//*[@id="txtCode"]').send_keys(verify_code)
# 暂停2s
time.sleep(3)
# 点击登录
web.find_element_by_xpath('//*[@id="Button1"]').click()
# 跳转至公共信息
web.get('http://is.cfmcc.com/OA/SysFolder/AppFrame/AppQuery.aspx?tblName=Q_WebNews_Query&condition=CatCode%20like%20[QUOTES]04%[QUOTES]')
time.sleep(1)
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
time.sleep(1)
#遍历页面所有数据
tr_list=web.find_elements_by_xpath('//*[@id="flex1"]/tbody/tr')
web.find_elements_by_class_name
url_list=[]
for tr in tr_list[0:10]:
  id=tr.id
  title=tr.find_element_by_xpath('./td[2]/div/a').text
  url=tr.find_element_by_xpath('./td[2]/div/a').get_attribute('href')
  url_list.append(url)
  # print(id,title,url)
print(url_list)
def delete_null(list):
    return list.strip()
for url in url_list:
  web.get(url)
  div=web.find_element_by_xpath('//*[@id="content"]/div[2]')
  p=div.find_elements_by_xpath('p')
  new_p=[p for p in p if p.text!='']
  str=new_p[-1].text.strip()
  print(str)
# web.close()