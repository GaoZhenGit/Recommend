# -*- coding: UTF-8 -*-

import constant
import constant.file



def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0, len(backitems))]

def get_mosttop(recommend_count = 15):
    word_map = {}
    relation = constant.file.get_relation()
    for line_words in relation:
        for word in line_words:
            if word_map.has_key(word):
                word_map[word] += 1
            else:
                word_map[word] = 1

    print 'words count:', len(word_map)

    word_list = sort_by_value(word_map)[0:recommend_count]
    return  word_list

def run():
    word_list = get_mosttop()
    doc_list = constant.file.get_docmap(True)

    # 输出edge
    output = open(constant.other_mosttop_edges, 'w')
    for it in doc_list:
        for w in word_list:
            output.write(it + ' ' + w + '\n')
    output.close()

if __name__ == '__main__':
    run()