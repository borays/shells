# coding:utf-8
import urllib.request
import os
import re

basedir = 'D:\\xinggan\\'
if not os.path.exists(basedir):
    os.makedirs(basedir)


def getHtmlContent(url):
    page = urllib.request.urlopen(url)
    Html = str(page.read())
    print("网页抓取成功")
    return Html


def getUrl(html):
        # 解析第一层URL信息
    first_flag = re.compile('<li><a href=\"(.*?)\" target=\"_blank\">')
    first_url = first_flag.findall(html)
    sec_flag = re.compile("<span>([0-9]{2})<\/span>")
    num = 0
    for i in range(len(first_url)):
        # 解析第二层URL信息
        pre_url = first_url[i]
        page_sec = urllib.request.urlopen(pre_url)
        html_sec = str(page_sec.read())
        sec_body = sec_flag.findall(html_sec)
        # print(sec_url[0])

        for i in range(1, int(sec_body[0])):
            sec_url = pre_url + '/' + str(i)
            # print(sec_url)
            # img_flag = re.compile('<img src=\"(.*?)\" alt=(.*?)>')
            # 获取图片真实下载地址
            img_flag = re.compile('<img src=\"(.*?)\"')
            img_page = urllib.request.urlopen(sec_url)
            img_html = str(img_page.read())
            img_body = img_flag.findall(img_html)
            # img_body = re.search(img_flag, img_html)
            # 下载图片
            try:
                x = urllib.request.urlretrieve(
                    img_body[0], basedir + '%s.jpg' % num)
                if x != "":
                    # print("Downloding...", html + uri, "to", fname)
                    print("Downloding...", img_body[0])
                num = num + 1
            except Exception:
                pass
    print("一共下载了%s张图片！" % num)

if __name__ == "__main__":
    url = "http://www.mzitu.com/xinggan"
    html = getHtmlContent(url)
    getUrl(html)
