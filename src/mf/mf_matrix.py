# -*- coding: UTF-8 -*-
import constant
import constant.file
from multiprocessing import Process


def read(n=-1):
    if n == -1:
        relation = constant.file.get_relation()
        doc_map = constant.file.get_docmap()
        processlist = []
        for i in xrange(constant.lda_topic_count):
            print str(i) + ' start'
            p = Process(target=__read_matrix, args=(i, relation, doc_map))
            p.start()
            processlist.append(p)
            # __read_matrix(i, relation, doc_map)
        for p in processlist:
            p.join()
    else:
        relation = constant.file.get_relation()
        doc_map = constant.file.get_docmap()
        __read_matrix(n, relation, doc_map)


def __read_matrix(n, relation, doc_map):
    fcn_list = constant.file.getfcn(n)
    gcn_list = constant.file.getgcn(n)
    gcn_map = constant.file.getgcn_map(n)
    row = len(fcn_list)
    col = len(gcn_list)
    output = open(constant.mf_matrix + str(n), 'w')
    output.write(str(row) + '*' + str(col) + '\n')
    for i, f in enumerate(fcn_list):
        glist = relation[doc_map[f]]
        for g in glist:
            if gcn_map.has_key(g):
                __double_relation(output, f, g, gcn_map, doc_map, relation)
        output.write('\n')
    output.close()
    print str(n) + ' finish'


# 对于双向关系加重矩阵中的权重
def __double_relation(output, f, g, gcn_map, doc_map, relation, rate=constant.mf_matrix_rate):
    if gcn_map.has_key(g):
        gi = gcn_map[g]
        flist = relation[doc_map[g]]
        if f in flist:
            output.write(str(gi) + ':' + str(rate) + ' ')
        else:
            output.write(str(gi) + ':1 ')


if __name__ == '__main__':
    read(-1)
