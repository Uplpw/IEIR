import os
import jieba
import pickle
from math import log
def get_total():
    path = ".\\new"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    file_output = open(".\\total.txt", "w")
    for file in files:
        content = open(path + "\\" + file, 'r', encoding='utf-8').read()
        file_output.write(content)

def save_dict():
    content = open(".\\total.txt", "r").read()
    seg_list = jieba.cut_for_search(content)
    dict_total = {}
    for word in seg_list:
        if word not in dict_total:
            dict_total[word] = 0

    file = open('.\\dict_total.pickle', 'wb')
    pickle.dump(dict_total, file)
    file.close()
    print("dict_total initialized")

def compute_idf():
    with open('.\\dict_total.pickle', 'rb') as file:
        dict_idf = pickle.load(file)

    path = ".\\result"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称

    for title in files:
        set_bool = set()
        content = open(path + "\\" + title, 'r', encoding='utf-8').read()
        seg_list = jieba.cut_for_search(content)
        for word in seg_list:
            if word not in set_bool:
                set_bool.add(word)
                if word in dict_idf:
                    dict_idf[word] += 1

    orderdict = sorted(dict_idf.items(), key=lambda item: item[1], reverse=True)

    dict_final = {}
    file_txt = open(".\\idf_list.txt", "w", encoding='utf-8')
    for key, value in orderdict:
        temp = log(185 / (value + 1), 10)
        dict_final[key] = temp
        file_txt.writelines(key + " " + str(temp) + "\n")

    file = open('.\\dict_idf.pickle', 'wb')
    pickle.dump(dict_final, file)
    file.close()

    print("idf computed")


def test_idf():
    file = open(".\\idf_list.txt", "r")
    for line in file:
        word, freq = line.strip().split(' ')
        print(word, freq)


if __name__ == '__main__':
    get_total()
    save_dict()
    compute_idf()
