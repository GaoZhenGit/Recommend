# -*- coding: UTF-8 -*-
import scipy.sparse as sparse
import _vector_beta_lda as lda
import constant.file
import other.mosttop as mt
import math


def get_matrix():
    relation = constant.file.get_relation()
    f_count = constant.file.get_doc_count()
    word_map = constant.file.get_wordmap()
    g_count = constant.file.get_word_count()

    matrix = sparse.lil_matrix((f_count, g_count), dtype=int)
    for i, i_t in enumerate(relation):
        for j_t in i_t:
            matrix[i, word_map[j_t]] += 1
    print 'read lda matrix end'
    return matrix


def do_lda(X, topic_count=constant.lda_topic_count, iter_count=100, alpha=0.5, beta = 0.01):
    print 'lda start'
    model = lda.LDA(n_topics=topic_count, random_state=None, n_iter=iter_count, alpha=alpha, eta = beta)
    model.fit(X)
    print 'lda end'
    return model

def print_model(model):
    # 输出theta
    theta = model.doc_topic_
    with open(constant.lda_theta, 'w') as file:
        for i in theta:
            for j in i:
                file.write(str(j) + ' ')
            file.write('\n')

    # 输出phi
    phi = model.topic_word_
    with open(constant.lda_phi, 'w') as file:
        for i in phi:
            for j in i:
                file.write(str(j) + ' ')
            file.write('\n')

def __get_beta_list():
    mt_map = mt.get_mosttop_map()
    word_list = constant.file.get_wordmap(True)
    max_lp = math.log(max(mt_map.values()))

    beta_list = []

    for w in word_list:
        p = mt_map[w]
        p = math.log(p) / max_lp / constant.lda_beta_list_rate
        beta_list.append(p)
    return beta_list

def run():
    matrix = get_matrix()
    model = do_lda(matrix,beta= __get_beta_list())
    print_model(model)

if __name__ == '__main__':
    run()
