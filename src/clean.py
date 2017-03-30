import os
import constant
import shutil
import sys


def clean():
    if os.path.exists(constant.lda_dir):
        shutil.rmtree(constant.lda_dir)
    if os.path.exists(constant.mf_dir):
        shutil.rmtree(constant.mf_dir)
    if os.path.exists(constant.mf_dir):
        shutil.rmtree(constant.mf_dir)
    if os.path.exists(constant.other_edges_dir):
        shutil.rmtree(constant.other_edges_dir)

    if len(sys.argv) == 2:
        if sys.argv[1] == 'all':
            if os.path.exists(constant.data_dir):
                shutil.rmtree(constant.data_dir)
            if os.path.exists(constant.conclusion_dir):
                shutil.rmtree(constant.conclusion_dir)

if __name__ == '__main__':
    clean()
