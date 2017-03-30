# -*- coding: UTF-8 -*-
import constant.file
import os

if not os.path.exists(constant.mf_dir):
    os.mkdir(constant.mf_dir)
if not os.path.exists(constant.mf_matrix_dir):
    os.mkdir(constant.mf_matrix_dir)
if not os.path.exists(constant.mf_pq):
    os.mkdir(constant.mf_pq)
if not os.path.exists(constant.mf_score_dir):
    os.mkdir(constant.mf_score_dir)
if not os.path.exists(constant.mf_result_dir):
    os.mkdir(constant.mf_result_dir)