# -*- coding: utf-8 -*-
import os
import jieba

path = ".\\new"
all = ".\\all_terms.txt"


def compute_terms():
    listdir = os.listdir(path)
    all_terms = set()
    with open(all, 'w', encoding='utf-8') as file:
        for i in listdir:
            content = open(path + "\\" + i, 'r', encoding='utf-8').read()
            seg_list = jieba.cut_for_search(content)
            for j in list(seg_list):
                all_terms.add(j)
        for i in all_terms:
            file.write(i + "\n")


def compute_tf():
    tf = ".\\tf.txt"
    terms_file = open(all, "r", encoding='utf-8')
    with open(tf, 'w+', encoding='utf-8') as file:
        for line in terms_file:
            listdir = os.listdir(path)
            total_str = line.strip("\n")
            temp = ""
            sum = 0
            for i in listdir:
                content = open(path + "\\" + i, 'r', encoding='utf-8').read()
                count = content.count(line.strip("\n"))
                if count != 0:
                    temp = temp + " " + i + " " + str(count)
                    sum = sum + 1
            total_str = total_str + " " + str(sum) + temp
            file.write(total_str + "\n")


def test():
    file = open(".\\tf.txt", "r", encoding='utf-8')
    for line in file:
        print(line, end="")


if __name__ == '__main__':
    compute_terms()
    compute_tf()
    test()
