import os
import jieba
path = ".\\new"

def create_seg():
    listdir = os.listdir(path)
    listdir.sort(key = lambda x: int(x[:-4]))
    with open(".\\segment.txt", 'w', encoding='UTF-8') as file:
        for i in listdir:
            content = open(path + "\\" + i, 'r', encoding='UTF-8').read()
            seg_list = jieba.cut_for_search(content)
            temp=""
            for j in list(seg_list):
                temp=temp+" "+j.strip("\n")
            file.write(temp+"\n")

create_seg()