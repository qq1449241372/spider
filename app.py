# 爬取OA公共信息页面
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import config
from chaojiying import Chaojiying_Client
import time
import datetime
import csv
from func import get_depart_by_name, is_author
# 程序开始时间
start = time.time()
now_date = datetime.datetime.now().strftime('%Y-%m-%d')
created_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
web = Chrome()
# 打开登录界面
web.get('http://is.cfmcc.com/OA/MainPage.aspx')
# 填入登录信息
web.find_element_by_xpath('//*[@id="txtUser"]').send_keys(config.username)
web.find_element_by_xpath('//*[@id="txtPwd"]').send_keys(config.pwd)
# 自动验证处理验证码
if(config.isAuto == True):
    img = web.find_element_by_xpath(
        '//*[@id="wrapper"]/div/table/tbody/tr/td[3]/img').screenshot_as_png
    chaojiying = Chaojiying_Client(
        config.chaojiying_username, config.chaojiying_pwd, config.chaojiying_softid)
    dic = chaojiying.PostPic(img, 1902)
    verify_code = dic['pic_str']
    web.find_element_by_xpath('//*[@id="txtCode"]').send_keys(verify_code)
    # 延迟后登陆
    time.sleep(2)
    web.find_element_by_xpath('//*[@id="Button1"]').click()
elif(config.isAuto == False):
    # 延迟后登录
    time.sleep(config.delayTime)
    web.find_element_by_xpath('//*[@id="Button1"]').click()

# 跳转至公共信息链接
web.get(
    'http://is.cfmcc.com/OA/SysFolder/AppFrame/AppQuery.aspx?tblName=Q_WebNews_Query&condition=CatCode%20like%20[QUOTES]04%[QUOTES]')
time.sleep(1.5)
# 填入搜索信息
web.find_element_by_xpath(
    '//*[@id="CorpName"]').send_keys(config.DEFAULT_COMPANY)
# 清除日期 readonly js脚本
js0 = 'document.getElementById("IssueTime_0").removeAttribute("readonly")'
js1 = 'document.getElementById("IssueTime_1").removeAttribute("readonly")'
# 改变页面条数脚本
js_changevalue = f'document.querySelector("#griddiv > div > div.pDiv > div.pDiv2 > div:nth-child(1) > select > option:nth-child(7)").value={config.pagesize}'
js_changetext = f'document.querySelector("#griddiv > div > div.pDiv > div.pDiv2 > div:nth-child(1) > select > option:nth-child(7)").text={config.pagesize}'
# 执行脚本
web.execute_script(js0)
web.execute_script(js1)
web.execute_script(js_changevalue)
web.execute_script(js_changetext)
# 输入查询日期
web.find_element_by_xpath(
    '//*[@id="IssueTime_0"]').send_keys(config.DEFAULT_START)
web.find_element_by_xpath(
    '//*[@id="IssueTime_1"]').send_keys(config.DEFAULT_END)
# 选择页码
web.find_element_by_xpath(
    '//*[@id="griddiv"]/div/div[8]/div[1]/div[1]/select/option[7]').click()
# 暂停
time.sleep(1)
# 遍历页面所有数据
tr_list = web.find_elements_by_xpath('//*[@id="flex1"]/tbody/tr')
url_list = []
for tr in tr_list:
    # 文章id
    id = tr.id
    # 标题
    title = tr.find_element_by_xpath('./td[2]/div/a').text
    # 文章链接
    url = tr.find_element_by_xpath('./td[2]/div/a').get_attribute('href')
    url_list.append(url)
print(url_list)
# 写入函数
f = open(f'./data/资产信息平台_{created_time}.csv', mode="w", newline='')
csvWriter = csv.writer(f)
# 写入第一行
csvWriter.writerow(['序号', '标题', '作者', '部门', '发布时间', '点击次数', '链接'])
index = 0
# 遍历文章url获取数据
for url in url_list:
    index = index+1
    try:
        web.get(url)
        info = web.find_element_by_xpath('//*[@id="content"]/div[1]')
        div = web.find_element_by_xpath('//*[@id="content"]/div[2]')
        # 查找所有p标签
        p_list = div.find_elements_by_xpath('p')
        # 去除空内容所有p标签
        new_p_list = [p for p in p_list if p.text.strip() != '']
        # 最后一个p标签
        last_p = new_p_list[-1]
        # 由last_p 得到的作者
        author_p = last_p.text.replace('资产公司', '').replace(' ', '').strip()
        # 由div得到的作者
        last_div = div.find_elements_by_xpath('div')
        # print("last_div:", last_div)
        # if(len(last_div) > 0):
        #     print('div->span!!!!', last_div[-1].find_elements_by_xpath('span'))
        # 优先获取数据
        title = web.find_element_by_xpath('//*[@id="content"]/h2').text
        date = info.text.split(' ')[0].replace('发布日期：', '').strip()
        click = info.text.split(' ')[1].replace('点击次数：', '').strip()

        if(is_author(author_p) == True):
            author = author_p
        if(is_author(author_p) == False):
            # 遍历last_p中<span>
            span_list = []
            # 判断是否存在span
            if(len(last_p.find_elements_by_xpath('span')) > 0):
                span_list = last_p.find_elements_by_xpath('span')
            if(len(last_div[-1].find_elements_by_xpath('span')) > 0):
                span_list = last_div[-1].find_elements_by_xpath('span')
            # 遍历span_list中<span>的内容
            print("span_list", span_list)
            author_span_list = []
            # 指示器
            i = 0
            for span in span_list:
                # 第一层span遍历
                i = i+1
                if(is_author(span.text.strip())):
                    author_span_list.append(span.text)
                # 重点检测最后存在嵌套的span标签
                if(i == len(span_list)):
                    # 第二层span遍历(通常在嵌套span出现在最后一个span)
                    inner_span_list = span.find_elements_by_xpath('span')
                    for inner_span in inner_span_list:
                        if(is_author(inner_span.text.strip())):
                            author_span_list.append(inner_span.text)
                author_span = '、'.join(author_span_list).strip()
            author = author_span
        # 获取对应数据
        depart = ''
        if(len(get_depart_by_name(author)) > 0):
            depart = get_depart_by_name(author)

        article_info = [index, title, author, depart, date, click, url]
        print(article_info)
        csvWriter.writerow(article_info)
        print('write done!')
    except Exception as e:
        # 写入错误信息
        author = last_p.text
        errinfo = [index, title, author, e, date, click, url]
        print(errinfo)
        csvWriter.writerow(errinfo)
        print('write done!')
web.close()
end = time.time()
print('用时:%.2f秒' % (end-start))
