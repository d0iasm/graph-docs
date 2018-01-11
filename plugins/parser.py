from collections import Counter
import random
import re
import sys
import urllib.request
import unicodedata
if '/app/plugins' not in sys.path:
    sys.path.append('/app/plugins')

import pyknp


class Parser(object):
    def __init__(self):
        self.knp = pyknp.KNP()

        
    def find_nodes(self):
        nodes = []
        for word in self.words:
            nodes.append((word, self.__weighting(word)))
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


    def set(self, text):
        self.line = self.__remove_marks(text)
        self.words = self.__find_words()
        self.counters = Counter(self.words)

    
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
            return {'width': str(self.counters[word]), 'fillcolor': str(min(5, self.counters[word])),
                        'fontsize': str(16+self.counters[word]**2)}
        return {'width': str(1), 'fillcolor': '1'}

if __name__ == '__main__':
    line = """2017年11月に設立されたメルペイ。メルカリが金融関連の新規事業を行うために立ち上げた子会社だ。同社の代表取締役には元グリーCFOの青柳直樹氏が就任し、役員には元WebPayのCTOでLINE Pay事業を経験した曾川景介氏らが名を連ねるなど注目を集めている。

今まで事業の詳細については明らかになっていなかったが、年内にも仮想通貨交換業の登録申請をして、メルカリ内の決済手段としてビットコインを含む仮想通貨に対応していくようだ。

これについては最初にITproが報じている。同記事によるとメルカリではメルペイを通じて2018年中にも仮想通貨交換業の登録を目指し、主要な仮想通貨を決済手段としてフリマアプリに組み込む方針だという。ICOにも興味を示しているということだから、独自のトークン（コイン）を発行しメルカリ経済圏を広げていく狙いがあるのかもしれない。

メルカリ広報に今回の背景について聞いたところ「仮想通貨についてはまだ社会的なルールを整備している段階と認識している。ただ、メルペイでは新技術を取り入れ色々な可能性を検討したいので、申請しておこうと考えた。まずは簡単に使える環境づくりからと考えている」という回答があった。

本件については新たなプロダクトをリリースするのではなく、メルカリ内の決済手段として仮想通貨に対応する。また具体的な内容は検討中であるものの「国内で6000万強のダウンロード数を持つメルカリの顧客基盤と取引データを活かした金融サービスを展開する予定」（メルカリ広報）だという。

なお昨年12月26日時点で、bitFlyerやQUOINE、テックビューロなど16社が仮想通貨交換業者として登録が認められている。 """
    p = Parser(line)
    # tuples = p.find_parent_child()
    tuples = p.find_nodes()
    for t in tuples:
        print(t[0] + ' => ' + str(t[1]))
