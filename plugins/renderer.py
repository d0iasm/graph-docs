import boto3
import datetime
import graphviz
import os

# from . import parser
import parser


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self, new_text):
        self.dot = graphviz.Graph(format='png', engine='neato',
                                  node_attr={'shape': 'circle'})
        self.new = new_text
        # TODO: Bucket policy
        self.session = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                             aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                             region_name='ap-northeast-1')
        self.s3 = self.session.resource('s3')
        self.s3_bucket = os.environ['S3_BUCKET_NAME']
        print(self.dot, self.dot.engine)

    def add_edge(self, child, parent):
        """
        :param string child: a child name of a node.
        :param string parent: a parent name of a node.
        """
        self.dot.edge(child, parent)

    def add_edges(self, line):
        """
        :param string line: a natural language text for parsing.
        """
        for child, parent in parser.find_parent_child(line):
            self.dot.edge(child, parent)

    def add_node(self, name, label=None):
        """
        :param string name: a node name.
        :param string label: a visable node name. optional.
        """
        self.dot.node(name, label)

    def add_nodes(self, line):
        """
        :param string line: a natural language text for parsing.
        """
        for node in parser.find_nodes(line):
            self.dot.node(str(node[0]), str(node[0]), width=str(node[1]), fixedsize='true')

    def copy(self):
        self.s3.Object(self.s3_bucket, 'old').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'new'})

    def render(self, text):
        self.add_nodes(text)
        self.add_edges(text)
        name = 'results/result_' + datetime.datetime.now().strftime('%s') + '.png'
        print(self.dot.source)
        self.s3.Object(self.s3_bucket, name).put(
            Body=graphviz.Source(self.dot.source, format='png').pipe())
        return name, text

    def reset(self):
        self.s3.Object(self.s3_bucket, 'old').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'empty'})
        self.s3.Object(self.s3_bucket, 'new').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'empty'})

    def merge(self):
        old_text = self.s3.Object(
            self.s3_bucket, 'old').get()['Body'].read().decode('utf-8')

        return (old_text + self.new).strip()

    def save(self, text):
        self.s3.Object(self.s3_bucket, 'new').put(Body=text)

    def update_shape(self, shape):
        self.dot.attr('node', shape=shape)

    def debug(self, line):
        self.add_nodes(line)
        self.add_edges(line)
        self.dot.render('debug', view=True, cleanup=True)


if __name__ == '__main__':
    line = """Pythonタグが付けられた新着投稿 - Qiita APP [8:38 AM]
Mastodonで始めるPythonプログラミング！腕試しテスト50本ノック（初級編）
はじめてのQiita記事です。あれが近くにある。
2017年にMastodonで遊びたくて、苦手なプログラミングを克服して、Pythonを習得しました。
http://takulog.info/howto-programming-for-poor-people/
この経験からMastodonのAPIを使って練習するのは、下記の理由でプログラミング学習に有効だと感じました。 """
    r = Renderer(line)
    r.debug(line)
