# -*- encoding: utf-8 -*-
import requests
import os
import re
import chardet

my_header = {'x-requested-with': 'XMLHttpRequest'}
byr_data = {'id': 'Gx370899893', 'passwd': 'LiGengxi1998'}
print('本脚本可以帮助您下载某个版块的帖子' + '\n')
boarddic = {'1': 'Python', '2': 'AimGraduate', '3': 'Job', '4': 'Linux', '5': 'Friends', '6': 'Java'}
print('1 ---> Python')
print('2 ---> AimGraduate')
print('3 ---> Job')
print('4 ---> Linux')
print('5 ---> Friends')
print('6 ---> Java')
boardnum = input('请直接输入您所选择查询的版面数字(1-6): ')
board = boarddic[boardnum]
i = int(input('您想从哪一页开始下载: '))
PAGE = int(input('请输入您想下载的页数，一页代表最新的30篇帖子: '))
bourl = "http://bbs.byr.cn/board/" + board + "?p="
count_valid = 0
count_invalid = 0
PAGE = PAGE + i

while i < PAGE:
    bbourl = bourl + str(i)
    print(bbourl)
    session = requests.Session()
    r_url = 'https://bbs.byr.cn/user/ajax_login.json'
    req = session.post(r_url, data=byr_data, headers=my_header)
    bbocont = session.get(bbourl, data=byr_data, headers=my_header).content
    res = b'<td\sclass="title_9"><a\shref="(.*?)">(.*?)</a>'
    reg = re.compile(res)
    articletitle = re.findall(res, bbocont)

    for art in articletitle:
        headline_name = str(art[1], encoding='GBK')
        if art[1][:2] == b'Re':
            print("!!!!!!!!!!---原贴已删，跳过---!!!!!!!!!!")
            count_invalid += 1
        else:
            count_valid += 1
            link = str(art[0], encoding="utf-8")
            articleurl = "http://bbs.byr.cn" + link
            pathname = './' + str(i)
            if os.path.exists(pathname):
                pass
            else:
                os.makedirs(pathname)
            filename = pathname + '/' + headline_name.replace('?', '').replace('.', '') \
                .replace(':', '').replace('<', '').replace('>', '').replace('|', '') \
                .replace('*', '').replace('/', '').replace('\\', '') + ".txt"
            print(filename)

            if os.path.exists(filename):
                continue
            else:
                articlename = open(filename, 'w+')

            articlecontent = session.get(articleurl, data=byr_data, headers=my_header).content
            regpage = b'<li\sclass="page-pre">.*?<i>(.*?)</i>'
            respage = re.compile(regpage)
            pagedata = re.search(respage, articlecontent)
            if pagedata:
                pageall = int(pagedata.group(1))
            else:
                continue
            print(pageall)
            temp = 0
            if (pageall % 9) > 0:
                temp = 1
            page = pageall / 9 + temp
            j = 1
            while page > 0:
                pageurl = articleurl + '?p=' + str(j)
                pagecontent = session.get(pageurl, data=byr_data, headers=my_header).content
                regname = b'<span\sclass="a-u-name"><a\shref=".*?">(.*?)</a>.*?<div\sclass="a-content-wrap">(.*?)<font\sclass="f000"></font>'
                resname = re.compile(regname)
                namecontent = re.findall(resname, pagecontent)
                for nc in namecontent:
                    encode_type = chardet.detect(nc[1])
                    if encode_type['encoding'] == 'GB2312':
                        encode_type['encoding'] = 'GB18030'
                        nc = str(nc[1], encoding=encode_type['encoding'])
                        tempsrc = nc.replace('<br />', '\n').replace(' ', '  ')
                        resformat = r'<a.*?>.*?</a>'
                        tempstr2 = re.sub(resformat, '', tempsrc)
                        resformat2 = r'<font.*?>|</font>'
                        tempstr3 = re.sub(resformat2, '', tempstr2)
                        resformat3 = r'<img.*?/>'
                        tempstr4 = re.sub(resformat3, '', tempstr3)
                        sepe = '*' * 40
                        tempstr = sepe + '\n' + tempstr4 + '\n'
                        articlename.write(tempstr)
                page -= 1
                j += 1
    i += 1
print("有效帖子数: %d" % count_valid)
print("无效帖子数: %d" % count_invalid)
