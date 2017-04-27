# -*- coding: UTF-8 -*-
from __init__ import *
import json


# 关注关系
def get_relation(is_doc=True):
    list = []
    with open(data_unnamed) as file:
        file.readline()  # 忽略首行
        for line in file:
            items = line.strip().split(' ')
            list.append(items)
    if is_doc:
        return list
    else:
        doc_list = get_docmap(True)
        map = {}
        for i, gs in enumerate(list):
            doc_id = doc_list[i]
            for g in gs:
                if map.has_key(g):
                    map[g].append(doc_id)
                else:
                    l = []
                    l.append(doc_id)
                    map[g] = l
        return map


# 关注者矩阵顺序
def get_docmap(need_list=False):
    if need_list:
        list = []
        with open(data_sort) as file:
            for i, line in enumerate(file):
                list.append(line.strip())
        return list
    else:
        map = {}
        with open(data_sort) as file:
            for i, line in enumerate(file):
                map[line.strip()] = i
        return map


# 关注者数量
def get_doc_count():
    with open(data_other) as file:
        s = file.read()
        other = json.loads(s)
    return other['ndocs']


# 被关注者矩阵排序
def get_wordmap(need_list=False):
    if need_list:
        with open(data_wordmap) as file:
            count = int(file.readline())
            list = range(count)
            for line in file:
                g, i = line.strip().split(' ')
                i = int(i)
                list[i] = g
        return list
    else:
        map = {}
        with open(data_wordmap) as file:
            file.readline()
            for line in file:
                f, g = line.strip().split(' ')
                map[f] = int(g)
        return map


# 被关注者数量
def get_word_count():
    with open(data_other) as file:
        s = file.read()
        other = json.loads(s)
    return other['nwords']


def getfcn(n, need_p=False):
    if need_p:
        fcnmap = {}
        with open(lda_fcn + str(n)) as file:
            for line in file:
                f, p = line.strip().split(' ')
                fcnmap[f] = float(p)
        return fcnmap
    else:
        fcnlist = []
        with open(lda_fcn + str(n)) as file:
            for line in file:
                f, p = line.strip().split(' ')
                fcnlist.append(f)
        return fcnlist


def getgcn(n):
    gcnlist = []
    with open(lda_gcn + str(n)) as file:
        for line in file:
            line = line.strip().split(' ')
            g = line[0]
            gcnlist.append(g)
    return gcnlist


def getgcn_map(n):
    gcn_map = {}
    with open(lda_gcn + str(n)) as file:
        for i, line in enumerate(file):
            line = line.strip().split(' ')
            g = line[0]
            gcn_map[g] = i
    return gcn_map


def get_raw_fcn(n):
    list = []
    with open(lda_theta) as file:
        for i, line in enumerate(file):
            line = line.strip().split(' ')
            p = line[n]
            list.append(float(p))
    return list


def get_raw_gcn(n):
    list = []
    with open(lda_phi) as file:
        for i, line in enumerate(file):
           if i == n:
               line = line.strip().split(' ')
               for it in line:
                   list.append(float(it))
               break
    return list