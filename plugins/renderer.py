import boto3
import graphviz
import os
import subprocess

# from . import parser
import parser


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self):
        self.dot = graphviz.Digraph(format='png')
        self.dot.attr('node', shape='circle')
        self.s3 = boto3.resource('s3')
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

    def copy(self, src, dest):
        subprocess.call(['cp', '-f', src, dest])
        self.s3.Object(self.s3_bucket, 'old.dot').copy_from(
            CopySource={'Bucket': self.s3_bucket, 'Key': 'merge.dot'})

    def render_from_dot(self, src, img):
        """
        :param string src: a dot file name in a source.
        :param string img: an image file name in a destination.
        """
        graphviz.Source(open(src, 'r').read(), format='png').render(img, view=True, cleanup=True)
        dot_data = self.s3.Object(
            self.s3_bucket, 'merge.dot').get()['Body'].read().decode('utf-8')

        self.s3.Object(self.s3_bucket, 'result.png').put(
            Body=graphviz.Source(dot_data, format='png').pipe())

    def merge(self, old, new, out):
        """
        :param string old: a old dot file name.
        :param string new: a new dot file name.
        :param string out: a merged dot file name.
        """
        # cmd = 'gvpack -u old.dot new.dot | sed \'s/_gv[0-9]\+//g\' | dot -Tpng -o result.png'
        # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        gvpack = subprocess.Popen(['gvpack', '-u', old, new],
                                  stdout=subprocess.PIPE)

        sed = subprocess.Popen(['sed', 's/_gv[0-9]\+//g'],
                               stdin=gvpack.stdout,
                               stdout=subprocess.PIPE)

        with open(out, 'wb+') as outstream:
            ps = subprocess.Popen(['dot'],
                                  stdin=sed.stdout,
                                  stdout=outstream)
            ps.wait()

    def save(self, name):
        """
        :param string name: a file name.
        """
        self.dot.save(filename=name)

        self.s3.Object(self.s3_bucket, 'new.dot').put(
            Body=self.dot.source.encode('UTF-8'))

    def update_shape(self, shape):
        self.dot.attr('node', shape=shape)


if __name__ == '__main__':
    old = './dest/old.dot'
    new = './dest/new.dot'
    merge = './dest/merge.dot'
    result = './dest/result'
    line = input('> ')
    r = Renderer()
    r.copy(merge, old)
    r.add_nodes(line)
    r.add_edges(line)
    r.save(new)
    r.merge(old, new, merge)
    r.render_from_dot(merge, result)
