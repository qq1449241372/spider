import os
# print(os.path.abspath('data'))
dataFilePath=os.path.abspath('data')
# 遍历
for file in os.listdir(dataFilePath) :
  # print(file)
  print(os.path.join(dataFilePath,file))