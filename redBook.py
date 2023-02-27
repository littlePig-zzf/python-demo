import requests
from bs4 import BeautifulSoup
import os
import re
import json

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

def fetchUrl(url):
    '''
    发起网络请求，获取网页源码
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 ',
        'cookie':'', # 换成自己的cookie哦~
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36',
    }
    
    r = requests.get(url, headers = headers)
    return r.text

def parsing_link(html):
    '''
    解析html文本，提取无水印图片的 url
    '''
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find('script', string=re.compile('window\.__INITIAL_STATE__'))

    test = re.split(r'=', script.string)
    # 处理字符串json数据不合理的地方
    string = test[1].replace('undefined', 'null') 
    # 转换成json数据
    result = json.loads(string, strict=False)
    # 获取对应字段
    imageList = result['note']['note']['imageList']
    title = result['note']['note']['title']
    print('标题：', title)
    print('开始下载啦！🚀')
    
    # 调用生成以title为名的文件夹, 可自定义要保存的路径
    file = os.path.dirname(__file__) + '/image/' + title
    mkdir(file) 
    
    # 提取图片
    for i in imageList:
        picUrl = f"https://sns-img-qc.xhscdn.com/{i['traceId']}"
        yield picUrl, i['traceId'], title

def download(url, filename, folder):
    '''
    下载图片
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36',
    }

    with open(f'image/{folder}/{filename}.jpg', 'wb') as v:
        try:
            r = requests.get(url, headers=headers)
            v.write(r.content)
        except Exception as e:
            print('图片下载错误！')

def roopLink(urls):
  '''
  遍历urls,批量下载去水印图片
  '''
  for item in urls:
    html = fetchUrl(item)
    for url, traceId, title in parsing_link(html):
        print(f"download image {url}")
       
        download(url, traceId, title)

if __name__ == '__main__':
    # 输入小红书的链接
    links = ['https://www.xiaohongshu.com/explore/63f07247000000001300d67b','https://www.xiaohongshu.com/explore/60a5f16f0000000021034cb4']
    roopLink(links)
    print("Finished!🎉")
