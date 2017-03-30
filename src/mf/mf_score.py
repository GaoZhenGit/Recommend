# -*- coding: UTF-8 -*-
import scipy.sparse as sparse
import sys
import gc
import constant
from multiprocessing import Process


def compute_score(threadHold,P, Pshape, Q, Qshape, scoreFile):
    Pmatrix = sparse.lil_matrix(Pshape, dtype=float)
    with open(P) as file:
        for row, fileLine in enumerate(file):
            lines = fileLine.strip().split(' ')
            for col, element in enumerate(lines):
                Pmatrix[row, col] = float(element)

    Qmatrix = sparse.lil_matrix(Qshape, dtype=float)
    with open(Q) as file:
        for row, fileLine in enumerate(file):
            lines = fileLine.strip().split(' ')
            for col, element in enumerate(lines):
                Qmatrix[row, col] = float(element)

    print('size of p:' + str(sys.getsizeof(Pmatrix)))
    print('size of q:' + str(sys.getsizeof(Qmatrix)))
    score = Pmatrix.dot(Qmatrix)
    del Pmatrix, Qmatrix
    gc.collect()
    print(score.shape)

    output = open(scoreFile,'w')
    for i in xrange(score.shape[0]):
        list = (score[i].toarray())[0].tolist()
        clist = sorted(list, reverse=True)[0:threadHold]
        for j in clist:
            output.write(str(list.index(j)) + ":" + str(j))
            output.write(' ')
        output.write('\n')
        del list
        del clist
    output.close()
    del score
    gc.collect()
    print str(scoreFile + ' finish')


def getShape(matrixFile):
    with open(matrixFile) as file:
        list = file.readline().strip().split('*')
    list[0] = int(list[0])
    list[1] = int(list[1])
    return list

def run():
    topicCount = constant.lda_topic_count
    factorsCount = constant.mf_factors_count
    threadHold = constant.mf_score_threadhold
    plist = []
    for i in xrange(topicCount):
        pFile = constant.mf_p + str(i)
        qFile = constant.mf_q + str(i)
        pShape = (getShape(constant.mf_matrix + str(i))[0], factorsCount)
        qShape = (factorsCount, getShape(constant.mf_matrix + str(i))[1])
        p = Process(target=compute_score, args=(threadHold,pFile, pShape, qFile, qShape, constant.mf_score + str(i)))
        # compute_score(threadHold,pFile, pShape, qFile, qShape, constant.mf_score + str(i))
        p.start()
        plist.append(p)
    for p in plist:
        p.join()
    print 'all finish'

if __name__ == '__main__':
    run()
