# -*- coding: UTF-8 -*-
import scipy.sparse as sparse
import gc
import constant
import constant.file

baseDir = './'
theta_dir = constant.lda_theta
phi_dir = constant.lda_phi



def readLdaResult(user_num, item_num, topic_num, output_file=constant.other_dirlda_edges):
    word_list = constant.file.get_wordmap(True)
    doc_list = constant.file.get_docmap(True)

    theta = sparse.lil_matrix((user_num, topic_num), dtype=float)
    with open(theta_dir) as file:
        for i, line in enumerate(file):
            items = line.strip().split(' ')
            for j, it in enumerate(items):
                theta[i, j] = float(it)

    phi = sparse.lil_matrix((topic_num, item_num), dtype=float)
    with open(phi_dir) as file:
        for i, line in enumerate(file):
            items = line.strip().split(' ')
            for j, it in enumerate(items):
                phi[i, j] = float(it)

    print 'read lda finish'
    score = theta.dot(phi)
    print 'multiply finish'
    del theta, phi
    gc.collect()

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
    edge.close()

def run():
    user_num = constant.file.get_doc_count()
    item_num = constant.file.get_word_count()
    topic_num = constant.lda_topic_count

    readLdaResult(user_num, item_num, topic_num)

if __name__ == '__main__':
    run()
