import os

import mf_matrix
import mf_score
import mf_result


def run(param_path = './mf/config.json'):

    command = 'java -jar '
    jar_path = './mf/fast_mf.jar '
    exec_commend = command + jar_path + ' ' + param_path
    print exec_commend
    os.system(exec_commend)


if __name__ == '__main__':
    print 'start read'
    mf_matrix.read(-1)
    print 'start mf'
    run()
    print 'start score'
    mf_score.run()
    print 'start result'
    mf_result.run()
