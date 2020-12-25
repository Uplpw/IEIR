import os

path=".\\result"
stop=".\\stopwords1.txt"
list=os.listdir(path)
with open(stop, 'r', encoding='UTF-8') as file:
    for i in list:
        content=open(path+"\\"+i, 'r', encoding='UTF-8').read()
        str=file.readline()
        while str!="":
            content=content.replace(str, "")
            str=file.readline()

        with open(".\\new\\" + i, 'w', encoding='UTF-8') as new_file:
            new_file.write(content)
