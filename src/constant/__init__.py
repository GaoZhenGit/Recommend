# -*- coding: UTF-8 -*-

base_dir = './data/'

recommend_count = 15

# data from database constant
data_dir = base_dir + 'dataDir/'
data_named = data_dir + 'database-result-named.txt'
data_unnamed = data_dir + 'database-result-unnamed.txt'
data_sort = data_dir + 'database-result-sort.txt'
data_testset = data_dir + 'testset.txt'
data_wordmap = data_dir + 'wordmap.txt'
data_other = data_dir + 'other.json'

# lda path
lda_dir = base_dir + 'ldaDir/'
lda_theta = lda_dir + 'model-final.theta'
lda_theta_after = lda_theta + '-after'
lda_phi = lda_dir + 'model-final.phi'
lda_phi_after = lda_phi + '-after'
lda_topic_dir = lda_dir + 'topic/'
lda_fcn = lda_topic_dir + 'f_c_'
lda_gcn = lda_topic_dir + 'g_c_'
lda_topic_count = 15

# mf path
mf_dir = base_dir + 'mfDir/'

mf_matrix_dir = mf_dir + 'matrix/'
mf_matrix = mf_matrix_dir + 'z_'

mf_pq = mf_dir + 'pq/'
mf_p = mf_pq + 'p_'
mf_q = mf_pq + 'q_'
mf_matrix_rate = 20
mf_factors_count = 10

mf_score_dir = mf_dir + 'score/'
mf_score = mf_score_dir + 's_'
mf_score_threadhold = 128
mf_result_dir = mf_dir + 'result/'
mf_edge = mf_result_dir + 'score_edge.txt'
mf_sum = mf_result_dir + 'score_sum.txt'

# conclusion path
conclusion_dir = base_dir + 'resultDir/'

# other
other_edges_dir = base_dir + 'edges/'
other_dirmf_edges = other_edges_dir + 'dir_mf_edge.txt'
other_mosttop_edges = other_edges_dir + 'mosttop_edge.txt'
other_dirlda_edges = other_edges_dir + 'dir_lda_edge.txt'
other_dirfmf_edges = other_edges_dir + 'dir_fmf_edge.txt'

other_mt_lda_edge = other_edges_dir + 'mt_lda_edge.txt'
other_mt_mf_edge = other_edges_dir + 'mt_mf_edge.txt'