# -*- coding: UTF-8 -*-

import constant
import constant.file

class MatrixMapper:
    def __init__(self):
        print ('matrix mapper init')
        self.__read()

    def __read(self):
        self.doc_list = constant.file.get_docmap(True)
        self.doc_map = constant.file.get_docmap()
        self.word_list = constant.file.get_wordmap(True)
        self.word_map = constant.file.get_wordmap()

    def reset(self,fcn_list,gcn_list):
        self.fcn_list = fcn_list
        self.gcn_list = gcn_list

    def mapI(self,originI):
        doc_id = self.fcn_list[originI]
        return self.doc_map[doc_id]

    def mapJ(self,originJ):
        word_id = self.gcn_list[originJ]
        return self.word_map[word_id]

    def get_real_doc_id(self,i):
        return self.doc_list[i]

    def get_real_word_id(self,j):
        return self.word_list[j]