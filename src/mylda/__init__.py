# -*- coding: UTF-8 -*-
import constant.file
import os

if not os.path.exists(constant.lda_dir):
    os.mkdir(constant.lda_dir)
if not os.path.exists(constant.lda_topic_dir):
    os.mkdir(constant.lda_topic_dir)