# coding:utf-8

import urllib.request
import os
import re


basedir = 'D:\\aa874_1\\'
if not os.path.exists(basedir):
    os.makedirs(basedir)


def getHtmlContent(url):
    u = urllib.request.URLopener()
    u.addheaders = []
    u.addheader(
        'User-Agent', 'Opera/9.80 (Windows NT 6.1; WOW64; U; de) Presto/2.10.289 Version/12.01')
    u.addheader('Accept-Language', 'de-DE,de;q=0.9,en;q=0.8')
    u.addheader('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1')
    f = u.open(url)
    content = f.read().decode('UTF-8')
    print("网页解析成功")
    f.close()
    return content


def getUrl(html):
    num = 1
    # 解析第一层URL信息,通过尾页来判断总页数
    #<a href = "190.htm" > 尾页 < /a >
    first_flag = re.compile('<a href=\"(.*?)\">')
    first_url = first_flag.findall(html)
    # print(first_url[-1]) 取出总页数
    filepath, tempfilename = os.path.split(first_url[-1])
    shortname, ext = os.path.splitext(tempfilename)
    for i in range(1, int(shortname)):
        pre_url = ("https://aa874.com/htm/piclist9/%s.htm" % i)
        # print(pre_url) 取出每页的帖子信息
        html = getHtmlContent(pre_url)
        # 取出每帖图片信息
        pre_flag = re.compile('<li><a href=\"(.*?)\" target=\"_blank\">')
        pre_infos = pre_flag.findall(html)
        for m in pre_infos:
            # 构建图片真实下载地址
            sec_url = ("https://aa874.com%s" % m)
            sec_html = getHtmlContent(sec_url)
            sec_flag = re.compile('src=\"(.*?)\"><br>')
            sec_infos = sec_flag.findall(sec_html)
            for n in sec_infos:
                print("正在下载第%s张... %s" % (num, n))
                # 伪造user-agent通过采集限制
                img_opener = urllib.request.build_opener()
                img_opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                fp = img_opener.open(n)
                img_data = fp.read()
                f = open(basedir + '%s.jpg' % num, 'w+b')
                f.write(img_data)
                f.close()
                fp.close()
                # urllib.request.urlretrieve(n, basedir + '%s.jpg' % num)
                num = num + 1
    print("一共下载了%s张图片！" % num)

if __name__ == "__main__":
    url = "https://aa874.com/htm/piclist1/"
    html = getHtmlContent(url)
    getUrl(html)
