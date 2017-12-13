#-*- encoding: utf-8 -*-
# from pyknp import Juman
# import sys
# import codecs
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# Use Juman in subprocess mode
# juman = Juman()
# result = juman.analysis(u"これはペンです。")
# print(','.join(mrph.midasi for mrph in result))

# for mrph in result.mrph_list():
# print("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
# % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))

# Use Juman in server mode
# juman = Juman(server='localhost', port=12345)

# from pyknp import Juman
# import sys
# import codecs
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# JUMAN++をsubprocessモードで使用
# juman = Juman()
# result = juman.analysis(u"ケーキを食べる")
# for mrph in result.mrph_list():
# print(u"見出し:{0}".format(mrph.midasi))


import pyknp


def select_normalization_representative_notation(fstring):
    begin = fstring.find('正規化代表表記:')
    end = fstring.find('/', begin + 1)
    return fstring[begin + len('正規化代表表記:') : end]


def select_dependency_structure(line):
    knp = pyknp.KNP()
    result = knp.parse(line)
    bnst_list = result.bnst_list()
    bnst_dic = dict((x.bnst_id, x) for x in bnst_list)

    tuples = []
    for bnst in bnst_list:
        if bnst.parent_id != -1:
            # (from, to)
            tuples.append((select_normalization_representative_notation(bnst.fstring), select_normalization_representative_notation(bnst_dic[bnst.parent_id].fstring)))

    return tuples


if __name__ == '__main__' :
    line = '太郎は花子が読んでいる本を次郎に渡した'
    tuples = select_dependency_structure(line)
    for t in tuples:
        print(t[0] + ' => ' + t[1])
