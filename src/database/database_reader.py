# -*- coding: UTF-8 -*-
import MySQLdb
import os
import shutil
import constant
import constant.file
import json

testset_rate = 0.1
testset_mod = int(1 / testset_rate)


def __read():
    db = MySQLdb.connect("localhost", "root", "123456", "twitter")
    cursor = db.cursor()

    # sql = 'select `srcid`, `desid` from `chinese_relation` order by `srcid`'
    # sql = 'select `desid`, `srcid` from `chinese_relation` order by `desid`'
    sql = 'select `f`,`g` from `filter10_5` order by `f`'
    # sql = 'select `g`,`f` from `filter10_5` order by `g`'

    cursor.execute(sql)

    query_result = cursor.fetchall()

    testset_file = open(constant.data_testset, 'w')
    named_data_file = open(constant.data_named, 'w')
    unnamed_data_file = open(constant.data_unnamed, 'w')
    sorted_data_file = open(constant.data_sort, 'w')

    query_map = {}
    query_follower_list = []  # 用于标记follower顺序（dict没有顺序）
    for i, result_set in enumerate(query_result):
        follower = str(result_set[0])
        followee = str(result_set[1])
        if query_map.has_key(follower):
            query_map[follower].append(followee)
        else:
            query_follower_list.append(follower)
            query_map[follower] = []
            query_map[follower].append(followee)
    for f in query_follower_list:
        followee_list = query_map[f]
        has_write_f = False
        for gi, g in enumerate(followee_list):
            if gi % testset_mod == 0:
                testset_file.write(f + ' ' + g + '\n')
            else:
                if has_write_f:
                    named_data_file.write(g + ' ')
                    unnamed_data_file.write(g + ' ')
                else:
                    named_data_file.write('\n' + f + ':')
                    named_data_file.write(g + ' ')
                    unnamed_data_file.write('\n' + g + ' ')
                    sorted_data_file.write('\n' + f)
                    has_write_f = True
    testset_file.close()
    named_data_file.close()
    unnamed_data_file.close()
    sorted_data_file.close()
    db.close()


def __addTitle():
    # 为unname添加行数并移动
    with open(constant.data_unnamed) as file:
        line_counts = len(file.readlines())
    line_counts -= 1

    tmp_file = 'tmp.txt'
    with open(constant.data_unnamed) as file:
        with open(tmp_file, 'w') as output:
            for i, line in enumerate(file):
                if i == 0:
                    output.write(str(line_counts) + '\n')
                else:
                    output.write(line)

    if os.path.exists(tmp_file) and os.path.exists(constant.data_unnamed):
        shutil.copyfile(tmp_file, constant.data_unnamed)
        os.remove(tmp_file)

    # 为sort去除开头回车符号
    with open(constant.data_sort) as file:
        with open(tmp_file,'w') as output:
            for i, line in enumerate(file):
                if i == 0:
                    pass
                else:
                    output.write(line)

    if os.path.exists(tmp_file) and os.path.exists(constant.data_sort):
        shutil.copyfile(tmp_file, constant.data_sort)
        os.remove(tmp_file)

def __print_info():
    list = constant.file.get_relation()
    word_map = {}
    count = 0
    for line in list:
        for word in line:
            if word_map.has_key(word):
                pass
            else:
                word_map[word] = count
                count += 1

    # 输出wordmap
    with open(constant.data_wordmap, 'w') as file:
        file.write(str(len(word_map)) + '\n')
        for it in word_map.items():
            file.write(it[0])
            file.write(' ')
            file.write(str(it[1]))
            file.write('\n')

    # 输出其他信息
    with open(constant.data_other, 'w') as file:
        other = {}
        other['ndocs'] = len(constant.file.get_docmap())
        other['nwords'] = len(constant.file.get_wordmap())
        s = json.dumps(other,indent=4)
        file.write(s)

if __name__ == '__main__':
    __read()
    __addTitle()
    __print_info()
