# -*- coding: UTF-8 -*-

import mf_matrix
import mf
import mf_score
import mf_result
import wrmf

import constant

def run():
    print 'start read'
    mf_matrix.read(-1)
    print 'start mf'
    if constant.mf_method == 'ifmf':
        mf.run()
    if constant.mf_method == 'wrmf':
        wrmf.run()
    print 'start score'
    mf_score.run()
    print 'start result'
    mf_result.run()

if __name__ == '__main__':
    run()