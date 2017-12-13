#-*- encoding: utf-8 -*-
from pyknp import Juman
import sys
import codecs
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# Use Juman in subprocess mode
juman = Juman()
result = juman.analysis(u"これはペンです。")
# print(','.join(mrph.midasi for mrph in result))

for mrph in result.mrph_list():
    pass
    # print("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
    # % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))

# Use Juman in server mode
# juman = Juman(server='localhost', port=12345)
