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

recommend_count = 15

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

def pre_lda(origin_count=3, mt_count=1):
    matrix = __mt_matrix(origin_count,mt_count)
    # 开始lda
    model = lda_executor.do_lda(matrix)
    lda_executor.print_model(model)
    # 使用lda直接计算结果
    other.dir_lda.readLdaResult(constant.file.get_doc_count(),
                                constant.file.get_word_count(),
                                constant.lda_topic_count,
                                output_file=constant.other_mt_lda_edge)

def pre_mf(origin_count=3,mt_count=1):
    matrix = __mt_matrix(origin_count,mt_count)
    dir_mf.process_print(matrix,constant.other_mt_mf_edge)

def pre_lda_mf(origin_count=3,mt_count=1):
    matrix = __mt_matrix(origin_count,mt_count)
    # 开始lda
    model = lda_executor.do_lda(matrix)
    lda_executor.print_model(model)
    lda_filter.run()
    mf_runner.run()

if __name__ == '__main__':
    pre_lda_mf(origin_count=10,mt_count=1)
