import os
import shutil
import re
def move():
    for i in range(7):
        list_dirs = os.walk(".\\"+str(i+1))
        for root, dirs, files in list_dirs:
            for f in files:
                shutil.move(os.path.join(root, f), ".\\content_raw\\" + f)


def rename():
    list=os.listdir(".\\content_raw")
    i=1
    for f in list:
        os.rename(".\\content_raw\\"+f, ".\\content_raw\\"+str(i)+".txt")
        i=i+1

def deleteBlank():
    list = os.listdir(".\\content_raw")

    for f in list:
        content=open(".\\content_raw\\"+f).read()
        if content=="":
            print("NULL")
            os.remove(".\\content_raw\\"+f)

def ModifyName():
    list = os.listdir(".\\content_raw")
    list.sort(key = lambda x: int(x[:-4]))
    i = 1
    for f in list:
        os.rename(".\\content_raw\\" + f, ".\\content_raw\\" + str(i) + ".txt")
        i = i + 1

def GBK2UTF():
    path=".\\content"
    if not os.path.exists(path):
        os.mkdir(path)
    list = os.listdir(".\\content_raw")
    for f in list:
        content = open(".\\content_raw\\" + f).read()
        content = content.replace('&nbsp;', '')
        content = content.replace('&quot;', '')
        content = content.replace('&amp;', '')
        content = content.replace('&lt;', '')
        content = content.replace('&gt;', '')
        content = content.replace('&nbsp;', '')
        content = content.replace('*', '')
        with open(path + "\\" + f, "w", encoding="UTF-8") as file:
            file.write(content)
# move()
# rename()
# deleteBlank()

# print(len(os.listdir(".\\content_raw")))
# ModifyName()
GBK2UTF()