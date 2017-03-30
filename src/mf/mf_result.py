# -*- coding: UTF-8 -*-
import scipy.sparse as sparse
import sys
import gc
import matrixMapper as Mp
import time
import constant
import constant.file


recommend_count = 15


def makeMatrix():
    user_num = constant.file.get_doc_count()
    item_num = constant.file.get_word_count()
    matrix = sparse.lil_matrix((user_num, item_num), dtype=float)
    return matrix


def addScore(index, matrix, mapper):
    # f_c_n文件读入
    fcnMap = constant.file.getfcn(index,True)  # user_id到概率P的映射
    fcnList = constant.file.getfcn(index)  # 下标的

    # g_c_n文件读入
    gcnList = constant.file.getgcn(index)

    mapper.reset(fcnList, gcnList)

    # s文件读入,并直接加入最终矩阵
    s_file = open(constant.mf_score + str(index))
    for i, line in enumerate(s_file):
        real_i = mapper.mapI(i)
        userP = float(fcnMap[fcnList[i]])
        cur_user_score_list = line.strip().split(' ')
        for score_pair in cur_user_score_list:
            j, score = score_pair.split(':')
            real_j = mapper.mapJ(int(j))
            score = float(score)
            if (score != 0):
                matrix[real_i, real_j] += score * userP

    s_file.close()
    del s_file


def printMatrix(matrix, mapper):
    print('start print matrix')
    t0 = time.time()
    score_output = open(constant.mf_result_dir + 'score_sum.txt', 'w')
    score_edge = open(constant.mf_result_dir + 'score_edge.txt', 'w')
    row = matrix.shape[0]
    for i in xrange(row):
        list = matrix[i].toarray()[0].tolist()
        clist = sorted(list, reverse=True)[0:recommend_count]
        row_id = mapper.get_real_doc_id(i)
        for j in xrange(len(clist)):
            word_index = list.index(clist[j])
            word_id = mapper.get_real_word_id(word_index)
            word_score = clist[j]
            score_output.write(word_id + ':' + str(word_score) + ' ')
            score_edge.write(row_id + ' ' + word_id + '\n')
        score_output.write('\n')
    t1 = time.time()
    print(str(t1 - t0) + " cost")

def run():
    result_holder = makeMatrix()
    mapper = Mp.MatrixMapper()
    topicCount = constant.lda_topic_count
    for i in xrange(topicCount):
        print(str(i) + 'start')
        addScore(i, result_holder, mapper)
    printMatrix(result_holder, mapper)

if __name__ == '__main__':
    run()
