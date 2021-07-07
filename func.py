from logging import fatal
from os import stat_result
import numpy as np
# 职工列表
stuff_dic={
  # 纪检部
  "李海波":"纪检部",
  # 办公室
  "金雅":"办公室",
  "夏勉":"办公室",
  "宁浩廷":"办公室",
  "杨楚":"办公室",
  "机关党支部":"办公室",
  # 财务部
  "吴红维":"财务部",
  "邓红云":"财务部",
  "文磊":"财务部",
  "曾可可":"财务部",
  # 商务部
  "周利娟":"商务部",
  "徐嘉琪":"商务部",
  "陈雨晴":"商务部",
  # 安环部
  "董武":"安环部",
  "李方方":"安环部",
  # 项目部
  "任灿":"项目部",
  "郭军":"项目部",
  "赵恒":"项目部",
  "朱则彦":"项目部",
  "唐杰":"项目部",
  "戚璘":"项目部",
  "陈学凯":"项目部",
  "王武":"项目部",
  "朱金波":"项目部",
  # 房产管理部
  "彭霞":"房地产管理部",
  "丁湛":"房地产管理部",
  "刘子禺":"房地产管理部",
  # 房产运营部
  "鄢红华":"房地产运营部",
  "王娟":"房地产运营部",
  "高艳霞":"房地产运营部",
  "黄鑫":"房地产运营部",
  "胡瑞":"房地产运营部",
  "周围":"房地产运营部",
  "赵李志":"房地产运营部",
  "唐陈成":"房地产运营部",
  "谢浩雨":"房地产运营部",
  "李爱园":"房地产运营部",   #已离职
  # 机械部
  "刘聪志":"机械部",
  "林骞":"机械部",
  "黄欢":"机械部",
  "程童":"机械部",
  "徐瑞宜":"机械部",
  "詹海英 ":"机械部",
  "李孟军 ":"机械部",
}
# 获取部门函数
def get_depart_by_name(name):
  depart_list=[]
  name_list=name.split('、')
  for name in name_list:
    depart_list.append(stuff_dic.get(name)) 
  return '、'.join(depart_list)

# 是否是作者函数
def is_author(name):
  find=0
  unfind=0
  name_list=name.split('、')
  for name in name_list:
    if name in stuff_dic:
      find+=1
    else:
      unfind+=1
  if(find==len(name_list)):
    return True
  else:
    return False
