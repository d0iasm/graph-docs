import boto3
import datetime
import graphviz
import os

from . import parser
# import parser


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self, new_text):
        self.dot = graphviz.Digraph(format='png')
        self.dot.attr('node', shape='circle')
        self.new = new_text
        # TODO: Bucket policy
        self.session = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                             aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                             region_name='ap-northeast-1')
        self.s3 = self.session.resource('s3')
        self.s3_bucket = os.environ['S3_BUCKET_NAME']

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
            self.dot.node(str(node), str(node))

    def copy(self):
        self.s3.Object(self.s3_bucket, 'old').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'new'})

    def render(self, text):
        self.add_nodes(text)
        self.add_edges(text)
        name = 'results/result_' + datetime.datetime.now().strftime('%s') + '.png'
        self.s3.Object(self.s3_bucket, name).put(
            Body=graphviz.Source(self.dot.source, format='png').pipe())
        return name

    def merge(self):
        old_text = self.s3.Object(
            self.s3_bucket, 'old').get()['Body'].read().decode('utf-8')

        return (old_text + self.new).strip()

    def save(self, text):
        self.s3.Object(self.s3_bucket, 'new').put(Body=text)

    def update_shape(self, shape):
        self.dot.attr('node', shape=shape)
