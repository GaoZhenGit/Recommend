import scipy.sparse as sparse
import sys
sys.path.append('./mf')
import ifmf
import constant
import constant.file
from multiprocessing import Process

def doMatrixF(inputFile, p, q):
    with open(inputFile) as file:
        for row, line in enumerate(file):
            if row == 0:
                num_users, num_items = line.strip().split('*')
                num_users = int(num_users)
                num_items = int(num_items)
                matrix = sparse.lil_matrix((num_users, num_items), dtype=float)
            else:
                glist = line.strip().split(' ')
                if len(glist) > 1:
                    for gi in glist:
                        gi = gi.split(':')
                        col = gi[0]
                        matrix[int(row - 1), int(col)] = gi[1]

    P, Q = ifmf.alternating_least_squares_cg(matrix, constant.mf_factors_count, regularization=0.01, iterations=15)

    print('start outputing P:')
    Pfile = open(p, 'w')
    xi, xj = P.shape
    for i in xrange(xi):
        for j in xrange(xj):
            print_value = P[i, j]
            if print_value >= 0:
                Pfile.write("%.15f" % print_value)
            else:
                Pfile.write("%.14f" % print_value)
            Pfile.write(' ')
        Pfile.write('\n')
    Pfile.close()

    print('start outputing Q:')
    Qfile = open(q, 'w')
    Q = Q.T
    yi, yj = Q.shape
    for i in xrange(yi):
        for j in xrange(yj):
            print_value = Q[i, j]
            if print_value >= 0:
                Qfile.write("%.15f" % print_value)
            else:
                Qfile.write("%.14f" % print_value)
            Qfile.write(' ')
        Qfile.write('\n')
    Qfile.close()

def run():
    processlist = []
    for index in xrange(constant.lda_topic_count):
        curInputFile = constant.mf_matrix + str(index)
        op = constant.mf_p + str(index)
        oq = constant.mf_q + str(index)
        p = Process(target=doMatrixF, args=(curInputFile, op, oq))
        print str(index) + ' matrix start', op, oq
        p.start()
        processlist.append(p)
        # doMatrixF(curInputFile, op, oq)
    for p in processlist:
        p.join()

if __name__ == '__main__':
    run()
