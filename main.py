import requests
# from selenium.webdriver import Chrome


# web.get('http://is.cfmcc.com/OA/Default.aspx?ReturnUrl=%2fOA%2fMainPage.aspx.com')
# 设置请求头
header={
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  "Referer":"http://is.cfmcc.com/OA/SysFolder/AppFrame/AppQuery.aspx?tblName=Q_WebNews_Query&condition=CatCode%20like%20[QUOTES]04%[QUOTES]",
  "Cookie":"ASP.NET_SessionId=s05lxt3pba3kv1svokxsvzb3; .ASPXAUTH=340293FDEC500B496C237F85B44126BE6C59F75B75FDB7179C02DFC8C6C47DB09CD5165D3573AD0CBFEA128AEAEA8D2EAE9634B6514A2E9133DF26075A55028375F73E6E5FA811DCDD9CA5D598113AA86EC5BF406825FF76F222DCF12193B93557706F09",
  "Origin":"http://is.cfmcc.com",
  "X-Requested-With":"XMLHttpRequest"
}
# 查询时间
date="2021-01-01,2021-12-31"
Q_WebNews_Query={"CorpName":"资产","IssueTime":date,"Title":"","IssueDeptCn":"","MainCat":""}
dat={"page": 1,"rp": 200,"queryid":Q_WebNews_Query,"condition":"CatCode like [QUOTES]04%[QUOTES]"}
# 设置参数
param={
  "tblName:":"Q_WebNews_Query",
  "condition":"CatCode like [QUOTES]04%[QUOTES]"
}
# 登陆链接
login_url="http://is.cfmcc.com/OA/Default.aspx?ReturnUrl=%2fOA%2fMainPage.aspx"
# 数据链接
data_url='http://is.cfmcc.com/OA/SysFolder/getxml.ashx'
# 新闻链接``
news_id='http://is.cfmcc.com/OA/News/Read2.aspx?newsId=8b3552c2-933a-407d-820b-bfc58a111937'

session=requests.session()
resp=requests.post(url=data_url,headers=header,data=dat,params=param)
resp.encoding='utf-8'
# print(resp.request.headers)
print(resp.text)
resp.close()
# web.close()