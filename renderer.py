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

    def add_node(self, name, label=None):
        self.dot.node(name, label)

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

    def create_img(self, src, img):
        graphviz.Source(open(src, 'r').read(), format='png').render(img, view=True)

    def output(self):
        print(self.dot)

    def render(self, name):
        self.dot.render(name, view=True)

    def update_shape(self, shape):
        self.dot.attr('node', shape=shape)


if __name__ == '__main__':
    r = Renderer()

    line = '太郎は花子が読んでいる本を次郎に渡した。'
    for n in parser.find_nodes(line):
        r.add_node(str(n), str(n))

    for t in parser.find_parent_child(line):
        r.add_edge(t[0], t[1])

    r.output()
    r.render('new.dot')

    r.merge('old.dot', 'new.dot', 'merge.dot')
    r.create_img('merge.dot', 'result')
