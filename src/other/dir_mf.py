# -*- coding: UTF-8 -*-
import scipy.sparse as sparse
import gc
import constant
import constant.file
import mf.ifmf

baseDir = './'

def get_matrix():
    # 获取矩阵信息
    user_num = constant.file.get_doc_count()
    item_num = constant.file.get_word_count()

    matrix = sparse.lil_matrix((user_num, item_num), dtype=int)

    word_list = constant.file.get_wordmap(False)

    relation = constant.file.get_relation()
    for i, words in enumerate(relation):
        print str(float(i)/user_num) + '\r',
        for word in words:
            j = word_list[word]
            matrix[i, j] += 1
    return matrix

def process_print(matrix,output_file = constant.other_dirmf_edges):
    word_list = constant.file.get_wordmap(True)
    doc_list = constant.file.get_docmap(True)
    P, Q = mf.ifmf.alternating_least_squares_cg(matrix, 10, regularization=0.01, iterations=2)
    print 'mf finish'
    Q = Q.T
    p = sparse.lil_matrix(P)
    del P
    q = sparse.lil_matrix(Q)
    del Q
    gc.collect()
    print 'translate finish'
    score = p.dot(q)
    gc.collect()
    print 'mutilply finish'
    edge = open(output_file, 'w')
    for i in xrange(score.shape[0]):
        list = (score[i].toarray())[0].tolist()
        clist = sorted(list, reverse=True)[0:constant.recommend_count]
        doc_id = doc_list[i]
        for j in clist:
            word_id = word_list[list.index(j)]
            edge.write(doc_id + ' ' + word_id + '\n')
        del list
        del clist
    del score
    gc.collect()

def run():
    print('start running mf without lda')
    matrix = get_matrix()
    print 'read matrix finish'
    process_print(matrix)

if __name__ == '__main__':
    run()