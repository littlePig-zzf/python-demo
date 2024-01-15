import requests
from bs4 import BeautifulSoup
import os
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
        'cookie':'xhsTrackerId=7ff0cee2-d318-4845-a5f1-7f4fb9acb9c3; xhsTrackerId.sig=hrWK6Hw0SUZ8mRCiVj0KO1K4nyb5Rbr3cxcAneVDyJY; a1=186823c9460khhoyfzypkmiw8cprofje475xhyso150000115335; webId=bbb653427b6f8ad0d223ff07d448275f; gid=yYKYJqSjjJ4dyYKYJqSj4WvMK8TxxlviuvUT2ly63EYSUC28FliVdx888yy2qq28j0DDy2dS; gid.sign=SVNqT90rFZJP8Hpu1fDr6lxAv7Q=; web_session=030037a4cb351b0516ff232780244a0727192f; customerClientId=918124472893177; x-user-id-ark.xiaohongshu.com=62b982519a415e00014f6c2f; timestamp2=1677477939195dfe19d311adbcb4966d1bc2c3da33a8ec424ce52a391b32474; timestamp2.sig=RuqNBEIFoHscqX8BtjGLcla6Yn5Z36oIRc4hMvXN1iI; gr_user_id=711f3d34-fd16-4ba2-bc61-f09ca8023256; x-user-id-eva.xiaohongshu.com=62b982519a415e00014f6c2f; xhsTracker=url=user-profile&xhsshare=CopyLink; xhsTracker.sig=WS8d3HYlzoIfhHjyJtY_Y1QP5iYacJ96TpUFr1hgfm4; extra_exp_ids=yamcha_0327_exp,h5_1208_exp3; extra_exp_ids.sig=ANlofVKSDcIxHrXW_rvDettMT1wABiN2baUCClhZnYI; webBuild=2.0.3; websectiga=82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28; sec_poison_id=18a62e3c-9284-4e5d-a196-c777ed2a4c6a; xsecappid=yamcha',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    
    r = requests.get(url, headers = headers)
    return r.text

def parsing_link(html):
    '''
    解析html文本，提取无水印图片的 url
    '''
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find('script', string=re.compile('window\.__INITIAL_STATE__'))

    # print(script.string, '🚀🚀🚀🚀')
    test = re.split(r'_=', script.string)
    # 处理字符串json数据不合理的地方
    string = test[1].replace('undefined', 'null') 
    # 转换成json数据
    result = json.loads(string, strict=False)
    # # 获取对应字段
    video = ''
    videoId = ''
    imageList = []

    noteDetailMap = result['note']['noteDetailMap']
    # 获取第一个键
    first_key = next(iter(noteDetailMap))
    first_value = noteDetailMap[first_key]
    if 'video' in first_value['note'] :
        video = first_value['note']['video']['media']['stream']['h264'][0]['masterUrl']
        videoId = first_value['note']['video']['media']['videoId']
    else:
        imageList = first_value['note']['imageList']
    
    title = first_value['note']['title']
    print('标题：', title)
    print('开始下载啦！🚀')

    # # 调用生成以title为名的文件夹, 可自定义要保存的路径
    file = os.path.dirname(__file__) + '/image/' + title
    mkdir(file) 

    print(video, '🚀🚀🚀🚀')
    if video:
        downloadVideo(video, videoId, title)
    # 提取图片
    for index, i in enumerate(imageList):
        picUrl = i['urlDefault']
        yield picUrl, index, title

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

def downloadVideo(url, filename, folder):
    '''
    下载视频
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36',
    }

    with open(f'image/{folder}/{filename}.mp4', 'wb') as v:
        try:
            r = requests.get(url, headers=headers)
            v.write(r.content)
        except Exception as e:
            print('视频下载错误！')

def roopLink(urls):
  '''
  遍历urls,批量下载去水印图片
  '''
  for item in urls:
    html = fetchUrl(item)
    parsing_link(html)
    for url, traceId, title in parsing_link(html):
        print(f"download image {url}")
       
        download(url, traceId, title)

if __name__ == '__main__':
  

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
    option.add_argument("--disable-blink-features")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option("detach", True)

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    # 指定 chromedriver 的路径
    chromedriver_path = '/Users/hongdazhu/chromedriver/120/chromedriver'

    # 创建Chrome浏览器对象
    browser = webdriver.Chrome(executable_path=chromedriver_path,options = option)
    # version = browser.capabilities['browserVersion']
    # print(version, 'versionversion')

    # 小红书主页的地址
    urls = [
        'https://www.xiaohongshu.com/user/profile/5f2e6cb800000000010063e2?m_source=pinpai',
        # 可以添加更多的链接
        # 'https://www.xiaohongshu.com/user/profile/另一个用户的ID',
    ]

    for url in urls:
        browser.get(url)

        # 设置隐式等待时间为10秒
        time.sleep(3)
        browser.refresh()
        time.sleep(5)
    
        pages = browser.page_source
        soup = BeautifulSoup(pages, 'html.parser')

        postId = []
        hrefArr = []

        for span in soup.find_all('a', class_='cover ld mask'):
            # titles.append(span.find('h2').text)
            postId.append('https://www.xiaohongshu.com/explore/'+span.get('href').split('/')[4])
        
        # print(soup, 'noteItem')
        print(postId)

        roopLink(postId)
    print("Finished!🎉")
