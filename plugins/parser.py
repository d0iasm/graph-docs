from collections import Counter
import re
import sys
import urllib.request
import unicodedata
if '/app/plugins' not in sys.path:
    sys.path.append('/app/plugins')

import pyknp


class Parser(object):
    def __init__(self, origin_text):
        self.knp = pyknp.KNP()
        self.line = self.__remove_marks(origin_text)
        self.words = self.__find_words()
        self.counters = Counter(self.words)

    
    def find_nodes(self):
        nodes = []
        for word in self.words:
            w = self.__weighting(word)
            nodes.append((word, w))
        return nodes


    def find_parent_child(self):
        bnst_list = self.knp.parse(self.line).bnst_list()
        bnst_dict = dict((x.bnst_id, x) for x in bnst_list)
    
        tuples = []
        for bnst in bnst_list:
            if bnst.parent_id != -1:
                tuples.append((self.__find_original_word(bnst),
                               self.__find_original_word(bnst_dict[bnst.parent_id])))

        return tuples

    
    def __find_original_word(self, bunsetsu):
        """
        @param bunsetsu pyknp.knp.bunsetsu Class
        @return an original word
        """
        return bunsetsu.mrph_list()[0].genkei


    def __find_words(self):
        bnst_list = self.knp.parse(self.line).bnst_list()
        words = []
        for bnst in bnst_list:
            words.append(self.__find_original_word(bnst))
        return words
    

    def __get_swapwords(self, line):
        slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
        slothlib_file = urllib.request.urlopen(slothlib_path)
        slothlib_stopwords = [l.decode("utf-8").strip() for l in slothlib_file]
        slothlib_stopwords = [ss for ss in slothlib_stopwords if ss]
        return slothlib_stopwords


    def __remove_marks(self, line):
        line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', line)
        line = unicodedata.normalize('NFKC', line)
        line = re.sub(re.compile('[!-/:-@[-`{-~]', re.IGNORECASE), '', line)
        line = line.replace(' ', '').replace('\n', '')
        return line

    
    def __weighting(self, word):
        if word in self.counters:
            return self.counters[word]
        return 1

if __name__ == '__main__':
    line = """Pythonタグが付けられた新着投稿 - Qiita APP [8:38 AM]
Mastodonで始めるPythonプログラミング！腕試しテスト50本ノック（初級編）
はじめてのQiita記事です。あれが近くにある。
2017年にMastodonで遊びたくて、苦手なプログラミングを克服して、Pythonを習得しました。
http://takulog.info/howto-programming-for-poor-people/
この経験からMastodonのAPIを使って練習するのは、下記の理由でプログラミング学習に有効だと感じました。 """
    p = Parser(line)
    # tuples = p.find_parent_child()
    tuples = p.find_nodes()
    for t in tuples:
        print(t[0] + ' => ' + str(t[1]))
