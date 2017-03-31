# -*- coding: UTF-8 -*-
import constant
import constant.file
from multiprocessing import Process


def read(n=-1):
    if n == -1:
        relation = constant.file.get_relation()
        doc_list = constant.file.get_docmap()
        processlist = []
        for i in xrange(constant.lda_topic_count):
            print str(i) + ' start'
            p = Process(target=__read_matrix, args=(i, relation, doc_list))
            p.start()
            processlist.append(p)
            # __read_matrix(i, relation, doc_list)
        for p in processlist:
            p.join()
    else:
        relation = constant.file.get_relation()
        doc_list = constant.file.get_docmap()
        __read_matrix(n,relation,doc_list)


def __read_matrix(n, relation, doc_list):
    fcn_list = constant.file.getfcn(n)
    gcn_list = constant.file.getgcn(n)
    gcn_map = constant.file.getgcn_map(n)
    row = len(fcn_list)
    col = len(gcn_list)
    output = open(constant.mf_matrix + str(n), 'w')
    output.write(str(row) + '*' + str(col) + '\n')
    for i, f in enumerate(fcn_list):
        glist = relation[doc_list[f]]
        for g in glist:
            gi = gcn_map[g]
            output.write(str(gi) + ' ')
        output.write('\n')
    output.close()
    print str(n) + ' finish'

if __name__ == '__main__':
    read(-1)
