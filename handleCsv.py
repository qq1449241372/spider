import csv
import os
from pyecharts.charts import Bar
from pyecharts import options as opts
# 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType
import datetime

from pyecharts.options.global_options import LegendOpts
created_time=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
count_by_depart={
  "纪检部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "办公室":[0,0,0,0,0,0,0,0,0,0,0,0],
  "财务部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "商务部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "安环部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "项目部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "房地产管理部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "房地产运营部":[0,0,0,0,0,0,0,0,0,0,0,0],
  "机械部":[0,0,0,0,0,0,0,0,0,0,0,0]
}

dataFilePath=os.path.abspath('data')
# 遍历
for file in os.listdir(dataFilePath) :
  # print(file)
  csvPath=os.path.join(dataFilePath,file)
  print(csvPath)
  with open(csvPath,'r') as fp:
    reader=csv.reader(fp)
    next(reader)
    for x in reader:
      name=x[2]
      depart=x[3]
      month=int(x[4][5:7])


      #判断多部门
      if (depart.find('、')!=-1):
        depart_list=depart.split('、')
        #去重
        new_depart_list=list(set(depart_list))
        #累加
        for item in new_depart_list:
          count_by_depart[item][month-1]=count_by_depart[item][month-1]+1
      #奇葩数据统计至办公室
      elif(len(depart)>10):
        count_by_depart['办公室'][month-1]=count_by_depart['办公室'][month-1]+1
      else:
        count_by_depart[depart][month-1]=count_by_depart[depart][month-1]+1
    print(count_by_depart)
# x轴数据
M=[str(i)+'月' for i in range(1,13)]
# for item in count_by_depart:
#   bar=(
#     Bar()
#     .add_xaxis(M)
#     .add_yaxis(item, count_by_depart[item])
#     .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
#     .render(f"./charts/信息平台_{item}_{created_time}.html")
#   )
# 所有部门柱状图
bar=(
    Bar(
      init_opts=opts.InitOpts(theme=ThemeType.SHINE,width="1800px",height='800px'),
      )
    .set_colors(colors=["#cd000e","#ffff00","#525357","#b77760","#5c2019","#339ca8","#2b821d","#e4bd51","#474f77"])
    .add_xaxis(M)
    .add_yaxis("纪检部", count_by_depart["纪检部"])
    .add_yaxis("办公室", count_by_depart["办公室"]) 
    .add_yaxis("机械部", count_by_depart["机械部"])
    .add_yaxis("房地产运营部", count_by_depart["房地产运营部"])
    .add_yaxis("房地产管理部", count_by_depart["房地产管理部"])
    .add_yaxis("项目部", count_by_depart["项目部"])
    .add_yaxis("安环部", count_by_depart["安环部"])
    .add_yaxis("财务部", count_by_depart["财务部"])
    .add_yaxis("商务部", count_by_depart["商务部"])
    .set_global_opts(title_opts=opts.TitleOpts(title=f"资产公司信息平台统计_{created_time}", subtitle="文章数量"))
    .set_global_opts(datazoom_opts=opts.DataZoomOpts(is_show=True))
)
bar.render(f"./charts/信息平台_资产公司_{created_time}.html")
