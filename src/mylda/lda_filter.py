# -*- coding: UTF-8 -*-
import constant
import constant.file
import scipy.sparse as sparse


def filter_theta(theta_path=constant.lda_theta, theta_after_path=constant.lda_theta_after, theta_threadhold=0.05):
    with open(theta_path) as file:
        with open(theta_after_path, 'w') as output:
            for line in file:
                items = line.strip().split(' ')
                for it in items:
                    it = float(it)
                    if it < theta_threadhold:
                        output.write(str(0.0) + ' ')
                    else:
                        output.write(str(it) + ' ')
                output.write('\n')


def theta_sperator(theta_after_path=constant.lda_theta_after, sperator_path=constant.lda_fcn):
    topic_count = constant.lda_topic_count
    doc_count = constant.file.get_doc_count()
    theta = sparse.lil_matrix((doc_count, topic_count), dtype=float)
    with open(theta_after_path) as file:
        for i, line in enumerate(file):
            items = line.strip().split(' ')
            for j, item in enumerate(items):
                theta[i, j] = float(item)

    doc_list = constant.file.get_docmap(True)

    for j in xrange(topic_count):
        with open(sperator_path + str(j), 'w') as file:
            for i in xrange(doc_count):
                if theta[i, j] != 0:
                    file.write(doc_list[i] + ' ' + str(theta[i, j]) + '\n')
    return theta


def filter_phi(phi_path=constant.lda_phi, phi_after_path=constant.lda_phi_after, phi_threadhold=8):
    word_count = 0
    topic_count = 0
    with open(phi_path) as origin:
        for i, line in enumerate(origin):
            if i == 0:
                items = line.strip().split(' ')
                word_count = len(items)
            topic_count += 1
    phi = sparse.lil_matrix((topic_count, word_count), dtype=float)
    with open(phi_path) as origin:
        for i, line in enumerate(origin):
            items = line.strip().split()
            for j, it in enumerate(items):
                phi[i, j] = float(it)

    for j in xrange(word_count):
        origin_col = []
        for i in xrange(topic_count):
            origin_col.append(phi[i, j])
        slist = sorted(origin_col, reverse=True)[0:phi_threadhold]
        for i in xrange(topic_count):
            if origin_col[i] not in slist:
                phi[i, j] = 0
    with open(phi_after_path, 'w') as file:
        for i in xrange(topic_count):
            for j in xrange(word_count):
                file.write(str(phi[i, j]) + ' ')
            file.write('\n')


def process_phi():
    theta_list = []
    with open(constant.lda_theta_after) as file:
        for line in file:
            plist = line.strip().split(' ')
            plist = [float(it) for it in plist]
            theta_list.append(plist)

    glist = constant.file.get_wordmap(True)
    relation = constant.file.get_relation(False)
    fmap = constant.file.get_docmap()

    gcn_list = []
    for gi, g in enumerate(glist):
        flist = relation[g]
        t_tol_list = [0] * constant.lda_topic_count
        for f in flist:
            fi = fmap[f]
            tlist = theta_list[fi]
            for ti, t in enumerate(tlist):
                t_tol_list[ti] += t
        gtlist = []
        for it in t_tol_list:
            if it == 0:
                gtlist.append(0)
            else:
                gtlist.append(1)
        gcn_list.append(gtlist)

    del theta_list
    del relation
    del fmap

    gcn_files = []
    for t in xrange(constant.lda_topic_count):
        file = open(constant.lda_gcn + str(t), 'w')
        gcn_files.append(file)

    for i, line in enumerate(gcn_list):
        for t, item in enumerate(line):
            if item == 0:
                pass
            else:
                gcn_files[t].write(glist[i] + '\n')

    for file in gcn_files:
        file.close()

def run():
    filter_theta()
    theta_sperator()
    process_phi()

if __name__ == '__main__':
    run()
