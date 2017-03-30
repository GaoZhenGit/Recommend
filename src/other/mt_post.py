# -*- coding: UTF-8 -*-
import time
import constant
import constant.file
import other.mosttop as mt


def make_mt_post(origin_result_file, recommend_count, output_result, post_count):
    mt_list = mt.get_mosttop(post_count)
    i = 0
    while i < post_count:
        mt_list[i] += '\n'
        i += 1
    del i
    print mt_list
    with open(origin_result_file) as ifile:
        with open(output_result, 'w') as ofile:
            count = 0
            user_recommends = []
            for line in ifile:
                count += 1
                user_recommends.append(line)
                if count == recommend_count:
                    count = 0
                    user_recommends = user_recommends[0:(recommend_count - post_count)]
                    for it in user_recommends:
                        ofile.write(it)
                    f_id = line.split(' ')[0]
                    for it in mt_list:
                        ofile.write(f_id + ' ' + it)
                    user_recommends = []
                else:
                    pass


def run():
    make_mt_post(constant.mf_edge, 15, 'test2.txt', 15)


if __name__ == '__main__':
    run()
