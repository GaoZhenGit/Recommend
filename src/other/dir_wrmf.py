import constant
import constant.file
import os
import gc
import scipy.sparse as sparse


def read_matrix():
    relation = constant.file.get_relation()
    word_map = constant.file.get_wordmap()
    with open(constant.mf_matrix_dir + 'wrmf-matrix', 'w') as file:
        for i, glist in enumerate(relation):
            for it in glist:
                j = word_map[it]
                file.write(str(i) + ' ' + str(j) + '\n')


def mf(method='WRMF'):
    print 'start ' + method
    data_dir = '--data-dir=' + constant.mf_matrix_dir
    training_file = '--training-file=' + 'wrmf-matrix'
    recommender = '--recommender=' + method
    save_model = '--save-model=' + constant.mf_media_model
    param = data_dir + ' ' + training_file + ' ' + recommender + ' ' + save_model
    os.system('java -jar MyMediaLite.jar ' + param)


def multiply():
    print 'change model to p q'
    with open(constant.mf_media_model) as file:
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

    score = p.dot(q)
    del p
    del q
    gc.collect()

    word_list = constant.file.get_wordmap(True)
    doc_list = constant.file.get_docmap(True)

    edge = open(constant.other_dirwrmf_edges, 'w')
    for i in xrange(score.shape[0]):
        list = (score[i].toarray())[0].tolist()
        clist = sorted(list, reverse=True)[0:constant.recommend_count]
        doc_id = doc_list[i]
        for j in clist:
            word_id = word_list[list.index(j)]
            edge.write(doc_id + ' ' + word_id + '\n')
        del list
        del clist
    edge.close()

def clean():
    if os.path.exists(constant.mf_matrix_dir + 'wrmf-matrix'):
        os.remove(constant.mf_matrix_dir + 'wrmf-matrix')
    if os.path.exists(constant.mf_media_model):
        os.remove(constant.mf_media_model)

def run():
    read_matrix()
    # mf()
    # multiply()
    # clean()


if __name__ == '__main__':
    run()
