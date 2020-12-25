from django.shortcuts import render, redirect
import time, datetime, random
from IEAndIR.forms import *
from IEAndIR.ir import *
from IEAndIR.segment import *

path_root = 'E:\\Applications\\Python\\Tools\\djangoProject'
path_root += '\\search'
with open(path_root + '\\sender.pickle', 'rb') as file:
    dict_sender = pickle.load(file)
with open(path_root + '\\time.pickle', 'rb') as file:
    dict_time = pickle.load(file)
path_keywords = path_root + "\\keywords"  # 关键词目录
path = path_root + "\\new"  # 文档文件夹目录

print("path_root:", path_root)


class result:
    def __init__(self, title, value, sender, time, keywords, abstract):
        self.title = title
        self.value = value
        self.sender = sender
        self.time = time
        self.keywords = keywords
        self.abstract = abstract


# 接收请求数据
def index(request):
    request.encoding = 'utf-8'
    titles = ["一日不见，如隔三秋", "有缘千里一线牵", "好久不见，甚是想念"]
    message = ""
    if request.POST:
        message = request.POST["txt"]
    if message=="":
        rand = random.randint(0, 2)
        list = []
        return render(request, "search.html", {"title": titles[rand], "list": list, "size": len(list)})
    else:
        rand = random.randint(0, 2)
        mylist=[]
        result, embedding, query, extra=IR(request, message)
        for i in result:
            fpath=path+"\\"+i.title
            with open(fpath, "r", encoding="UTF-8") as file:
                result_title=file.readline()
                mylist.append(result_title)
        end=zip(result, mylist)
        return render(request, "search.html", {"title": titles[rand], "list": end, "size": len(result), "flag": 1,
                                               "message": message})

def IR(request, message):
    query = message
    print("query:", query)
    order_dict, order_dict_embedding = work(query)
    order_dict_xieyang = retrieval(query)
    itmp = 0
    result_list = []
    for key, value in order_dict:
        itmp += 1
        if itmp ==6:
            break
        sender = dict_sender[key]
        time = dict_time[key]
        keywords = ""
        file = open(path_keywords + "\\" + key, "r", encoding="UTF-8")
        for line in file:
            word, freq = line.strip().split(' ')
            keywords += word + " "
        file.close()
        contents = open(path + "\\" + key, "r", encoding="UTF-8").read().split('\n')
        abstract = ""
        for content in contents:
            abstract += content
        r = result(key, value, sender, time, keywords, abstract[len(key) - 4:100])
        result_list.append(r)

    itmp = 0
    result_list_embed = []
    for key, value in order_dict_embedding:
        itmp += 1
        if itmp == 6:
            break
        sender = dict_sender[key]
        time = dict_time[key]
        keywords = ""
        file = open(path_keywords + "\\" + key, "r", encoding="UTF-8")
        for line in file:
            word, freq = line.strip().split(' ')
            keywords += word + " "
        file.close()
        contents = open(path + "\\" + key, "r", encoding="UTF-8").read().split('\n')
        abstract = ""
        for content in contents:
            abstract += content
        r = result(key, value, sender, time, keywords, abstract[len(key) - 4:100])
        result_list_embed.append(r)

    itmp = 0
    result_list_xieyang = []
    for key, value in order_dict_xieyang.items():
        itmp += 1
        if itmp == 6:
            break
        sender = dict_sender[key]
        time = dict_time[key]
        keywords = ""
        file = open(path_keywords + "\\" + key, "r", encoding="UTF-8")
        for line in file:
            word, freq = line.strip().split(' ')
            keywords += word + " "
        file.close()
        contents = open(path + "\\" + key, "r", encoding="UTF-8").read().split('\n')
        abstract = ""
        for content in contents:
            abstract += content
        r = result(key, value, sender, time, keywords, abstract[len(key) - 4:100])
        result_list_xieyang.append(r)
    for i in result_list:
        print(i.title, i.value, i.sender, i.time)
    for i in result_list_xieyang:
        print(i.title, i.value, i.sender, i.time)
    return result_list, result_list_embed, query, result_list_xieyang

def search_html(request):
    request.encoding = 'utf-8'
    if 'url' in request.GET and request.GET['url']:
        message = '你搜索的内容为: ' + request.GET['url']
    else:
        message = '你提交了空表单'
    print(message)
    fpath = path + "\\" + request.GET['url']
    with open(fpath, "r", encoding="UTF-8") as file:
        title=file.readline()
        body = file.read()
    print(request.GET['query'])
    result, embedding, query, extra=IR(request, request.GET['query'])
    #temp=""
    for i in result:
        if request.GET['url']==i.title:
            temp=i
    new_keywords=""
    temp_key=temp.keywords.split(" ")
    if int(0.33*len(temp_key))<1:
        for i in range(int(len(temp_key))):
            new_keywords=new_keywords+" "+ temp_key[i]
    else:
        for i in range(int(0.33*len(temp_key))):
            new_keywords=new_keywords+" "+ temp_key[i]
    temp.keywords=new_keywords
    array_text=open(path_root+"\\content\\"+request.GET['url'],"r", encoding="UTF-8" ).read().split("--")
    text=[]
    for i in range(len(array_text)):
        if i!=0:
            text.append(array_text[i].replace("站内", "\n回复内容："))

    return render(request, "message.html", {"title": title, "body": body, "object": temp, "txt": text})
