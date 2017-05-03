# -*- coding: UTF-8 -*-
from __future__ import division
import time
import sys
import constant
import constant.file
from math import log

test_set_dir = constant.data_testset
conculsionDir = constant.conclusion_dir


def get_result_set(output):
    # 根据命令行参数来决定对哪个文件进行conclusion
    if len(sys.argv) == 1:
        result_set_dir = constant.mf_edge
        # result_set_dir = './test2.txt'
    elif sys.argv[1] == 'dirmf':
        result_set_dir = constant.other_dirmf_edges
    elif sys.argv[1] == 'mt':
        result_set_dir = constant.other_mosttop_edges
    elif sys.argv[1] == 'dirlda':
        result_set_dir = constant.other_dirlda_edges
    elif sys.argv[1] == 'mtlda':
        result_set_dir = constant.other_mt_lda_edge
    elif sys.argv[1] == 'mtmf':
        result_set_dir = constant.other_mt_mf_edge
    elif sys.argv[1] == 'dirfmf':
        result_set_dir = constant.other_dirfmf_edges

    print result_set_dir
    result_set = []
    with open(result_set_dir) as file:
        for line in file:
            result_set.append(line.strip())
    print 'result set size:', len(result_set)
    output.write('result set size:' + str(len(result_set)) + '\n')
    return result_set


def get_test_set(output):
    test_set = []
    with open(test_set_dir) as file:
        for line in file:
            test_set.append(line.strip())
    print 'test set size:', len(test_set)
    output.write('test set size:' + str(len(test_set)) + '\n')
    return test_set


def get_hit_set(result_set, test_set, output):
    hit_set = list(set(test_set).intersection(set(result_set)))
    print 'intersection set size:', len(hit_set)
    output.write('intersection set size:' + str(len(hit_set)) + '\n')
    return hit_set


def compute_recall_precision_f1(hit_set, result_set, test_set, output):
    recall = len(hit_set) / len(test_set)
    precision = len(hit_set) / len(result_set)
    f1 = 2 * precision * recall / (precision + recall)

    print 'recall:', recall * 100, '%'
    output.write('recall:' + str(recall * 100) + '%\n')
    print 'precision:', precision * 100, '%'
    output.write('precision:' + str(precision * 100) + '%\n')
    print 'f1:', f1
    output.write('f1:' + str(f1) + '\n')


def compute_conversion(hit_set, output):
    # 计算转化率
    doc_count = constant.file.get_doc_count()
    word_count = constant.file.get_word_count()

    left_list = []
    right_list = []
    for line in hit_set:
        left_id, right_id = line.split(' ')
        left_list.append(left_id)
        right_list.append(right_id)

    conversion1 = len(set(left_list)) / doc_count
    conversion2 = len(set(right_list)) / word_count

    print 'conversion1:', conversion1, len(set(left_list))
    print 'conversion2:', conversion2, len(set(right_list))
    output.write('conversion1: ' + str(conversion1) + '\n')
    output.write('conversion2: ' + str(conversion2) + '\n')


def compute_ndcg(hit_set, test_set, output):
    hit_map = {}
    for it in hit_set:
        fid, gid = it.split(' ')
        if hit_map.has_key(fid):
            hit_map[fid].append(gid)
        else:
            hit_map[fid] = []
            hit_map[fid].append(gid)
    flist = []
    test_map = {}
    for it in test_set:
        fid, gid = it.split(' ')
        if test_map.has_key(fid):
            test_map[fid].append(gid)
        else:
            test_map[fid] = []
            test_map[fid].append(gid)
            flist.append(fid)
    dcg_sum = 0.0
    idcn_sum = 0.0
    for fid in flist:
        if not hit_map.has_key(fid):
            continue
        hit_list = hit_map[fid]
        test_list = test_map[fid]
        pos_list = range(len(test_list))  # 使用1、0列表表示在单个用户的测试列中，是否被推荐正确
        for i, t in enumerate(test_list):
            if t in hit_list:
                pos_list[i] = 1
            else:
                pos_list[i] = 0
        dcg = 0
        one_count = 0  # 统计单个用户推荐列里正确个数
        for i, p in enumerate(pos_list):
            dcg += p / (log(i + 2, 2))
            if p == 1:
                one_count += 1
        idcg = 0
        for i in range(one_count):
            idcg += 1 / (log(i + 2, 2))

        dcg_sum += dcg
        idcn_sum += idcg

    ndcg = dcg_sum / idcn_sum
    print 'ndcg:', ndcg
    output.write('ndcg:' + str(ndcg) + '\n')


def run():
    output = open(conculsionDir + str(int(time.time())) + '.txt', 'w')
    result_set = get_result_set(output)
    test_set = get_test_set(output)
    hit_set = get_hit_set(result_set, test_set, output)
    compute_recall_precision_f1(hit_set, result_set, test_set, output)
    compute_conversion(hit_set, output)
    compute_ndcg(hit_set, test_set, output)
    output.close()


if __name__ == '__main__':
    run()
