#coding:utf-8

# coding:utf-8

import os
import re
import sys
import requests
import json
import urllib.request
import urllib.error

try:
    pre=input("请输入网易歌单:" )
# pre="http://music.163.com/#/playlist?id=640006772"
    url = re.sub("#/", "", pre)
    print("开始尝试解析歌单！")
    r = requests.get(url)
    content=r.text
    res=r'<ul class="f-hide">(.*?)</ul>'
    mm=re.findall(res,content,re.S|re.M)
except Exception as e:
    print("请输入正确的歌单地址！")
    pass
    input("请重新打开脚本尝试！")
    sys.exit(0)
if mm:
    names=mm[0]
    res_uri = r'<li><a .*?>(.*?)</a></li>'
    name = re.findall(res_uri, names, re.S | re.M)
else:
    print("无法获得歌曲列表！")
num=0
for value in name:
    url_baidu="http://sug.music.baidu.com/info/suggestion"
    payload={'word':value,'version':'2',"from":'0'}
    r=requests.get(url_baidu,params=payload)
    content=r.text
    d=json.loads(content,encoding="utf-8")
    if('data' not in d) or d['data']=='':
        continue
    songid=d['data']['song'][0]['songid']
    print("\n已匹配歌曲ID为: %s" % songid)

    url_fm="http://music.baidu.com/data/music/fmlink"
    payload_fm={'songIds':songid,'type':'mp3'}
    r=requests.get(url_fm,params=payload_fm)
    content=r.text
    d = json.loads(content, encoding="utf-8")
    if('data' not in d) or d['data']=='':
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    if(len(songlink) < 10):
        print("获取下载地址失败！")
        continue
    print("找到下载地址！ %s" % songlink)

    songdir = "get_from_baidu"
    if not os.path.exists(songdir):
        os.mkdir(songdir)
    songname=d['data']['songList'][0]['songName']
    artistName = d["data"]["songList"][0]["artistName"]
    filename=("%s/%s-%s.mp3" % (songdir,songname,artistName))

    #下载歌曲
    try:
        f = urllib.request.urlopen(songlink)
    except Exception as e:
        pass

    headers = requests.head(songlink).headers
    size = round(int(headers['Content-Length']) / (1024 ** 2), 2)
    if not os.path.isfile(filename):
        print("正在下载:%s:"% songname)
        print("歌曲大小:%sMB:" % size)
        try:
            with open(filename, 'wb') as fp:
                fp.write(f.read())
                print("歌曲 %s 下载完成...\n" % filename)
                num=num+1
        except Exception as e:
            print("歌曲 %s 下载异常！" % filename)
            pass

    else:
        print("歌曲 %s 已经下载！" % filename)
print("歌单下载完成！本次一共下载%s首歌曲！" % num)
input("回车键退出！")