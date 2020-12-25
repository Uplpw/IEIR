import re
import os

def get_content(post):
    pattern = '\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*.*?\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*'
    content = re.search(pattern, post, flags=re.DOTALL).group()
    content = content[40:-40].strip()
    # 去掉html转义字符
    content = content.replace('&nbsp;', '')
    content = content.replace('&quot;', '')
    content = content.replace('&amp;', '')
    content = content.replace('&lt;', '')
    content = content.replace('&gt;', '')
    content = content.replace('&nbsp;', '')
    pattern = '※ 修改:.*'
    content = re.sub(pattern, '', content).strip()
    # 提取标题
    pattern = '标题:.*'
    title = ''
    if re.search(pattern, content):
        title = re.search(pattern, content).group()[4:]
    pattern = '发信人:.*?, 站内'
    content = re.sub(pattern, '', content, flags=re.DOTALL).strip()
    content = title + '\n' + content
    return content

def traverse():
    # root_path = 'F:\\研究生阶段\\研一上\\信息抽取与信息检索\\爬虫以及爬取数据\\corpora_raw\\'
    # result_path = 'F:\\研究生阶段\\研一上\\信息抽取与信息检索\\爬虫以及爬取数据\\content\\'
    root_path = ".\\content_raw"
    result_path = ".\\result\\"
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    if not os.path.exists(root_path):
        print(root_path + ' is not exist!')
    else:
        file_name = 1
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if os.path.getsize(root + '\\' + file) and 'Re:' not in file:
                    with open(root + '\\' + file, 'r', encoding='gbk') as fin:
                        print(root, file)
                        content = get_content(fin.read())
                        with open(result_path + file, 'w', encoding='utf-8') as fout:
                            fout.write(content)
                        file_name += 1
traverse()
