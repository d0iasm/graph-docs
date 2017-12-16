import graphviz
import subprocess

import parser


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self):
        self.dot = graphviz.Digraph(format='png')
        self.dot.attr('node', shape='circle')

    def add_edge(self, child, parent):
        self.dot.edge(child, parent)

    def add_edges(self, line):
        for child, parent in parser.find_parent_child(line):
            self.dot.edge(child, parent)

    def add_node(self, name, label=None):
        self.dot.node(name, label)

    def add_nodes(self, line):
        for node in parser.find_nodes(line):
            self.dot.node(str(node), str(node))

    def render_from_dot(self, src, img):
        graphviz.Source(open(src, 'r').read(), format='png').render(img, view=True)

    def merge(self, old, new, out):
        # cmd = 'gvpack -u old.dot new.dot | sed \'s/_gv[0-9]\+//g\' | dot -Tpng -o result.png'
        # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        gvpack = subprocess.Popen(['gvpack', '-u', old, new],
                                  stdout=subprocess.PIPE)

        sed = subprocess.Popen(['sed', 's/_gv[0-9]\+//g'],
                               stdin=gvpack.stdout,
                               stdout=subprocess.PIPE)

        with open(out, 'wb') as outstream:
            ps = subprocess.Popen(['dot'],
                                  stdin=sed.stdout,
                                  stdout=outstream)
            ps.wait()

    def save(self, name):
        self.dot.save(filename=name)

    def update_shape(self, shape):
        self.dot.attr('node', shape=shape)


if __name__ == '__main__':
    old = 'dest/old.dot'
    new = 'dest/new.dot'
    merge = 'dest/merge.dot'
    result = 'dest/result'
    line = input('> ')
    r = Renderer()
    r.add_nodes(line)
    r.add_edges(line)
    r.save(new)
    r.merge(old, new, merge)
    r.render_from_dot(merge, result)
