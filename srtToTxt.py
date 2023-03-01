import os

def split2step(alist,step):
	rs = []
	for i in range(0,len(alist),step):
		rs.append(alist[i:i+step])
	
	return rs
	
def mkdir(path):
  '''
  创建文件夹
  '''
  folder = os.path.exists(path)
  if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
      print("---  创建新的文件夹😀  ---")
      os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
      print("---  OK 🚩 ---")
  else:
      print("--- ⚠️ 文件夹已存在!  ---")

path = "D:/python-demo/text" #文件夹目录
targetPath = 'D:/python-demo/targetText' #存储的目标文件夹
files= os.listdir(path) #得到文件夹下的所有文件名称

mkdir(targetPath) # 创建目标结果文件夹

for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
        flines = open(path+"/"+file, 'r', encoding='utf-8').readlines()  
        f4 = split2step(flines,4)
        result = ""
        for item in f4:
            result = result+item[2].replace("\n","，")

        targetFileName = file.split('.')[0]+'.txt'

        with open(f'targetText/{targetFileName}','w',encoding='utf-8') as r:
            print(f'---{targetFileName} 转换成功 🚩---')
            r.write(result)
