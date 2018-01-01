import re
import sys
import urllib.request
import unicodedata
if '/app/plugins' not in sys.path:
    sys.path.append('/app/plugins')

import pyknp


def find_original_word(bunsetsu):
    """
    @param bunsetsu pyknp.knp.bunsetsu Class
    @return an original word
    """
    return bunsetsu.mrph_list()[0].genkei


def find_nodes(line):
    knp = pyknp.KNP()
    result = knp.parse(remove_marks(line))
    bnst_list = result.bnst_list()
    nodes = []
    for bnst in bnst_list:
        nodes.append(find_original_word(bnst))

    return nodes


def find_parent_child(line):
    knp = pyknp.KNP()
    result = knp.parse(remove_marks(line))
    bnst_list = result.bnst_list()
    bnst_dict = dict((x.bnst_id, x) for x in bnst_list)

    tuples = []
    for bnst in bnst_list:
        if bnst.parent_id != -1:
            tuples.append((find_original_word(bnst),
                           find_original_word(bnst_dict[bnst.parent_id])))

    return tuples


def get_swapwords(line):
    slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    slothlib_file = urllib.request.urlopen(slothlib_path)
    slothlib_stopwords = [l.decode("utf-8").strip() for l in slothlib_file]
    slothlib_stopwords = [ss for ss in slothlib_stopwords if ss]
    return slothlib_stopwords


def remove_marks(line):
    line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', line)
    line = unicodedata.normalize('NFKC', line)
    line = re.sub(re.compile('[!-/:-@[-`{-~]', re.IGNORECASE), '', line)
    line = line.replace(' ', '').replace('\n', '')
    print(line)
    return line


if __name__ == '__main__':
    line = """Pythonタグが付けられた新着投稿 - Qiita APP [8:38 AM]
Mastodonで始めるPythonプログラミング！腕試しテスト50本ノック（初級編）
はじめてのQiita記事です。あれが近くにある。
2017年にMastodonで遊びたくて、苦手なプログラミングを克服して、Pythonを習得しました。
http://takulog.info/howto-programming-for-poor-people/
この経験からMastodonのAPIを使って練習するのは、下記の理由でプログラミング学習に有効だと感じました。 """
    tuples = find_parent_child(line)
    for t in tuples:
        print(t[0] + ' => ' + t[1])
