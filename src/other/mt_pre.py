# -*- coding: UTF-8 -*-

import constant
import constant.file
import mosttop
import mylda.lda_executor as lda_executor
import mylda.lda_filter as lda_filter
import mf.runner as mf_runner
import other.dir_mf as dir_mf
import other.dir_lda
import scipy.sparse as sparse
import sys
sys.path.append('./other')
import math



def __mt_matrix(origin_count=3, mt_count=1):
    relation = constant.file.get_relation()
    f_count = constant.file.get_doc_count()
    word_map = constant.file.get_wordmap()
    g_count = constant.file.get_word_count()

    mt_list = mosttop.get_mosttop()

    matrix = sparse.lil_matrix((f_count, g_count), dtype=int)
    for i, i_t in enumerate(relation):
        for j_t in i_t:
            if j_t in mt_list:
                matrix[i, word_map[j_t]] = mt_count
            else:
                matrix[i, word_map[j_t]] = origin_count
    return matrix


def __pop_mt_matrix(base_num=50):
    mt_map = mosttop.get_mosttop_map()
    mt_list = mosttop.sort_by_value(mt_map)
    max_count = mt_map[mt_list[0]]
    max_count_log = math.log(max_count)
    for g in mt_list:
        p = mt_map[g]
        p = base_num - (math.log(p) / max_count_log) * base_num + 1
        mt_map[g] = p
    del mt_list

    relation = constant.file.get_relation()
    f_count = constant.file.get_doc_count()
    word_map = constant.file.get_wordmap()
    g_count = constant.file.get_word_count()

    matrix = sparse.lil_matrix((f_count, g_count), dtype=int)
    for i, gs in enumerate(relation):
        for g in gs:
            j = word_map[g]
            matrix[i, j] = mt_map[g]
    return matrix


def pre_lda(origin_count=3, mt_count=1):
    matrix = __mt_matrix(origin_count, mt_count)
    # 开始lda
    model = lda_executor.do_lda(matrix)
    lda_executor.print_model(model)
    # 使用lda直接计算结果
    other.dir_lda.readLdaResult(constant.file.get_doc_count(),
                                constant.file.get_word_count(),
                                constant.lda_topic_count,
                                output_file=constant.other_mt_lda_edge)


def pre_mf(origin_count=3, mt_count=1):
    matrix = __mt_matrix(origin_count, mt_count)
    dir_mf.process_print(matrix, constant.other_mt_mf_edge)


def pre_lda_mf(origin_count=3, mt_count=1):
    # matrix = __mt_matrix(origin_count, mt_count)
    matrix = __pop_mt_matrix()
    # 开始lda
    model = lda_executor.do_lda(matrix)
    lda_executor.print_model(model)
    lda_filter.run()
    mf_runner.run()


def run():
    if len(sys.argv) == 1:
        pre_lda_mf(origin_count=10, mt_count=1)
    elif len(sys.argv) == 3:
        count = int(sys.argv[2])
        print sys.argv[1], count
        if sys.argv[1] == 'lda':
            pre_lda(origin_count=count, mt_count=1)
        elif sys.argv[1] == 'mf':
            pre_mf(origin_count=count, mt_count=1)
        elif sys.argv[1] == 'lda_mf':
            pre_lda_mf(origin_count=count, mt_count=1)


if __name__ == '__main__':
    run()
