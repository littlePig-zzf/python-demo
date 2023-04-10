# python-demo
爬虫demo, 爬取小红书无水印图片、视频字幕srt文件转成txt文件等

## 一、爬取小红书、视频
### 1、爬取小红书无水印的图片，运行对应的python文件
```
python .\redBook.py
```
### tips:
1、文件中的cookie需要用你自己的cookie <br>
2、获取小红书的链接组成数组 <br>
3、默认生成的图片保存在：当前目录下的 image 文件夹下，你可以自定义文件路径 <br>

### 2、爬取小红书用户主页无水印的图片，视频
```
python .\redBookPatchAll.py
```
### tips:
1、文件中的cookie需要用你自己的cookie <br>
2、获取小红书用户主页的链接，找到136行替换链接 <br>
3、默认生成的资源保存在：当前目录下的 image 文件夹下，你可以自定义文件路径 <br>

## 二、视频字幕srt文件转成txt文件
运行对应的python文件
```
python .\srtToTxt.py
```
### tips:
1、根据自己的需要，自定义 path\targetPath 的路径 <br>
2、path为srt字幕所有文件、targetPath是转换后生成的txt文件对应的目录 <br>
