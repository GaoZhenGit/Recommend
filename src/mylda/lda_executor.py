# -*- coding: UTF-8 -*-
import scipy.sparse as sparse
import lda
import constant.file


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


def do_lda(X, topic_count=constant.lda_topic_count, iter_count=100, alpha=0.5):
    print 'lda start'
    model = lda.LDA(n_topics=topic_count, random_state=None, n_iter=iter_count, alpha=alpha)
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

def run():
    matrix = get_matrix()
    model = do_lda(matrix)
    print_model(model)

if __name__ == '__main__':
    run()
