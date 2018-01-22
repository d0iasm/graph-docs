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
        self.ok_type = ['形容詞', '名詞', '動詞']
        self.swapwords = self.__get_stopwords()

        
    def find_nodes(self):
        return self.words

    def find_parent_child(self):
        bnst_list = self.__get_bnstlist(self.line)
        bnst_dict = dict((x.bnst_id, x) for x in bnst_list)
        print()
    
        tuples = []
        for bnst in bnst_list:
            child = self.__find_original_word(bnst)
            if child[0] in self.swapwords or child[1] not in self.ok_type: continue
                
            if bnst.parent_id != -1:
                parent = self.__find_original_word(bnst_dict[bnst.parent_id])
                if parent[0] in self.swapwords or parent[1] not in self.ok_type: continue

                tuples.append((child[0], parent[0]))

        return tuples


    def set(self, text):
        self.line = self.__remove_marks(text)
        self.words = self.__find_words()
        print('[Debug] Parsed text: ', self.line)

    
    def __find_original_word(self, bunsetsu):
        """
        @param bunsetsu pyknp.knp.bunsetsu Class
        @return an original word and a part of speech
        """
        return (bunsetsu.mrph_list()[0].genkei, bunsetsu.mrph_list()[0].hinsi)


    def __find_words(self):
        bnst_list = self.__get_bnstlist(self.line)
        words = []
        for bnst in bnst_list:
            original = self.__find_original_word(bnst)
            if original[0] in self.swapwords or original[1] not in self.ok_type: continue
                
            words.append(original[0])
        return words


    def __get_bnstlist(self, line):
        bnst_list = []
        if len(line) > 250:
            lines = line.split("。")
            [bnst_list.extend(self.knp.parse(l).bnst_list()) for l in lines]
        else:
            bnst_list = self.knp.parse(line).bnst_list()
        return bnst_list
    

    def __get_stopwords(self):
        stopwords = '' 
        with open('stopwords.txt', 'r') as f:
            stopwords = f.read()
        return stopwords.split()

    
    def __remove_marks(self, line):
        line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', '', line)
        line = unicodedata.normalize('NFKC', line)
        line = re.sub(re.compile('[!-/:-@[-`{-~]', re.IGNORECASE), '', line)
        line = re.sub(re.compile('([+-]?[0-9]+\.?[0-9]*)'), '', line)
        line = line.replace(' ', '').replace('\n', '')
        return line

    
if __name__ == '__main__':
    line = """町というのはちいちゃくって、城壁がこう町全体をぐるっと回ってて、それが城壁の上を歩いても１時間ぐらいですよね。１時間かからないぐらいだね。４、５０分で。そうそう。
ほいでさあ、ずっと歩いていたんだけど、そうすと上から、なんか町の中が見れるじゃん。
あるよね。
ほいでさあ、なんか途中でワンちゃんに会ったんだね。
散歩をしてるワンちゃんに会ったんだ。
城壁の上をやっぱ観光客なんだけどワンちゃん連れてきてる人たち結構多くて。
で、こう、そのワンちゃんと２人を、なに、お父さんとお母さんと歩いて、ワンちゃんに会ったんだ。
途中で。ワンちゃーんとか言ってなでて、ほいで、この人たちはこっち行って、あたしらこっち行ったじゃん。
ずうーとこうやって回ってきてるの。
また会っちゃって。
ここで。
そうしたら。
おー、そら地球はやっぱり丸かったみたいだね。　
そうしたらそのワンちゃんがなんかか喜んじゃって、で、あたしの方に走ってきて、とびついてきちゃってさ。
別にあたしさあ、別にさっきなでただけなのにさあ、なんかすごーいなつかれちゃってね。　
さっきね、別に、そんなになでてもいないんだよ。
よしよしって言っただけなのに。
あらワンちゃんだーとか言ってすれ違ったんだよ。
普通に。
それでその次のとき、向こうの方からはーっといってかけてくるじゃん。
すごい勢いで走って。
私、あ、あーさっきの犬だとか私たちが言っとるじゃん。
あんで向こうの人たちも、あっ、さっき会った子たちねみたいな感じで気がついたじゃん。
犬も気がついたじゃん。
じゃははって走ってきちゃって、犬が。
そうなんだ。"""
    p = Parser()
    p.set(line)
    tuples = p.find_parent_child()
    # tuples = p.find_nodes()
    for t in tuples:
        print(t[0] + ' => ' + str(t[1]))
