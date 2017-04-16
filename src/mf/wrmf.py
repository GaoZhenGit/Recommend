import os
import constant
import scipy.sparse as sparse
from multiprocessing import Process
import random


def matrix_change(index):
    print 'change z to file'
    matrix_file = constant.mf_matrix + str(index)
    with open(matrix_file) as file:
        with open(constant.mf_media_matrix + str(index), 'w') as output:
            row, col = file.readline().strip().split('*')
            for i, line in enumerate(file):
                line = line.strip().split(' ')
                for it in line:
                    j, it = it.split(':')
                    output.write(str(i) + ' ' + str(j) + ' ' + str(it) + '\n')


def mf(index, method='WRMF'):
    print 'start ' + method
    data_dir = '--data-dir=' + constant.mf_matrix_dir
    training_file = '--training-file=' + constant.mf_media_matrix.split('/')[-1] + str(index)
    recommender = '--recommender=' + method
    save_model = '--save-model=' + constant.mf_media_model + str(index)
    random_num = '--random-seed=' + str(random.randint(0,1000000))
    param = data_dir + ' ' + training_file + ' ' + recommender + ' ' + save_model + ' ' + random_num
    os.system('java -jar MyMediaLite.jar ' + param)


def model_change(index):
    print 'change model to p q'
    with open(constant.mf_media_model + str(index)) as file:
        print file.readline().strip()  # method
        print file.readline().strip()  # version
        # start p
        prow, pcol = file.readline().strip().split(' ')
        prow = int(prow)
        pcol = int(pcol)
        p = sparse.lil_matrix((prow, pcol), dtype=float)
        while True:
            line = file.next().strip().split(' ')
            if len(line) == 3:
                i = int(line[0])
                j = int(line[1])
                v = float(line[2])
                p[i, j] = v
            if len(line) == 2:
                qrow = int(line[1])
                qcol = int(line[0])
                break
        # start q
        q = sparse.lil_matrix((qrow, qcol), dtype=float)
        for line in file:
            line = line.strip().split(' ')
            i = int(line[1])
            j = int(line[0])
            v = float(line[2])
            q[i, j] = v

        with open(constant.mf_p + str(index), 'w') as file:
            for i in xrange(prow):
                for j in xrange(pcol):
                    v = p[i, j]
                    file.write(str(v) + ' ')
                file.write('\n')
        with open(constant.mf_q + str(index), 'w') as file:
            for i in xrange(qrow):
                for j in xrange(qcol):
                    v = q[i, j]
                    file.write(str(v) + ' ')
                file.write('\n')


def clear(index):
    if os.path.exists(constant.mf_media_matrix + str(index)):
        os.remove(constant.mf_media_matrix + str(index))
    if os.path.exists(constant.mf_media_model + str(index)):
        os.remove(constant.mf_media_model + str(index))

def media_mf(index):
    matrix_change(index)
    mf(index)
    model_change(index)
    # clear(index)


def run():
    process_list = []
    for i in xrange(constant.lda_topic_count):
        p = Process(target=media_mf, args=(i,))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()

if __name__ == '__main__':
    run()
