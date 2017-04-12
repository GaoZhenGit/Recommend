import constant
import constant.file
import scipy.sparse as sparse
import mf.fast_mf as mf
import gc


def get_listmatrix():
    # 获取矩阵信息
    user_num = constant.file.get_doc_count()
    item_num = constant.file.get_word_count()

    matrix = [([0] * item_num) for i in range(user_num)]

    word_list = constant.file.get_wordmap(False)

    relation = constant.file.get_relation()
    for i, words in enumerate(relation):
        print str(float(i) / user_num) + '\r',
        for word in words:
            j = word_list[word]
            matrix[i][j] += 1
    return matrix


def print_listmatrix(matrix, file_name, need_title_count=True):
    row = len(matrix)
    col = len(matrix[0])
    with open(file_name, 'w') as file:
        if (need_title_count):
            file.write(str(row) + '*' + str(col) + '\n')
        for i in xrange(row):
            print str(float(i) / row) + '\r',
            for j in xrange(col):
                val = matrix[i][j]
                if val != 0:
                    file.write(str(j) + ':' + str(val) + ' ')
            file.write('\n')
    del matrix
    gc.collect()


def multiply(matrix_p, matrix_q, factors):
    user_num = constant.file.get_doc_count()
    item_num = constant.file.get_word_count()
    p = sparse.lil_matrix((user_num, factors), dtype=float)
    with open(matrix_p) as file:
        for i, line in enumerate(file):
            line = line.strip().split(' ')
            for j, it in enumerate(line):
                p[i, j] = float(it)
    q = sparse.lil_matrix((factors, item_num), dtype=float)
    with open(matrix_q) as file:
        for i, line in enumerate(file):
            line = line.strip().split(' ')
            for j, it in enumerate(line):
                q[i, j] = float(it)

    score = p.dot(q)
    del q
    del p
    gc.collect()

    print 'mutilply finish'
    edge = open(constant.other_dirfmf_edges, 'w')
    word_list = constant.file.get_wordmap(True)
    doc_list = constant.file.get_docmap(True)
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
    matrix = get_listmatrix()
    print_listmatrix(matrix, constant.mf_matrix_dir + 't_0')
    mf.run('./other/dir_fastmf_config.json')
    multiply(constant.mf_pq + 't_p_0', constant.mf_pq + 't_q_0', constant.mf_factors_count)


if __name__ == '__main__':
    run()
