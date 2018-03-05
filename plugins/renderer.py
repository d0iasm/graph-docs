#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import datetime
import graphviz
import os

from . import parser
# import parser
from . import weighting
# import weighting


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self, new_text):
        self.dot = graphviz.Graph(format='svg', engine='neato',
                                  edge_attr={
                                      'charset': 'UTF-8', 'color': 'white',
                                      'fontsize': '14', 'fontname': 'MS GOTHIC',
                                      'len': '2'
                                      },
                                  graph_attr={
                                      'bgcolor': '#343434', 'charset': 'UTF-8',
                                      'fontcolor': 'white', 'fontname': 'MS GOTHIC',
                                      'overlap': 'false', 'style': 'filled',
                                      },
                                  node_attr={
                                      'charset': 'UTF-8',
                                      'color': 'black', 'colorscheme': 'gnbu7',
                                      'fontcolor': 'black', 'fontname': 'MS GOTHIC',
                                      'fontsize': '16', 'fixedsize': 'true',
                                      'style': 'solid,filled', 'shape': 'circle',
                                      })
        self.parser = parser.Parser()
        # TODO: Bucket policy
        self.session = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                             aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                             region_name='ap-northeast-1')
        self.s3 = self.session.resource('s3')
        self.s3_bucket = os.environ['S3_BUCKET_NAME']


    def __add_edges(self):
        """
        :param string line: a natural language text for parsing.
        """
        for child, parent in self.parser.find_parent_child():
            self.dot.edge(child, parent)


    def __add_nodes(self):
        nodes = self.parser.find_nodes()
        edges = self.parser.find_parent_child()
        w_nodes = weighting.weighting(nodes, edges)
        for node in w_nodes:
            self.dot.node(node[0], label=node[0], **node[1])


    def render(self, text):
        self.parser.set(text)
        self.__add_nodes()
        self.__add_edges()
        print('Debug: dot file content ' + self.dot.source)

        name = 'results/result_' + datetime.datetime.now().strftime('%s') + '.svg'
        self.s3.Object(self.s3_bucket, name).put(
            Body=graphviz.Source(self.dot.source, engine='neato', format='svg').pipe())
        return name


    def debug(self, text):
        self.parser.set(text)
        self.add_nodes()
        self.add_edges()
        print(self.dot.source)
        self.dot.render('debug', view=True, cleanup=True)


if __name__ == '__main__':
    line = """テストメッセージ。"""
    print(len(line))
    r = Renderer(line)
    r.debug(line)
