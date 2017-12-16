import graphviz

import parser


# Merge .dot files command
# gvpack -u result result2 | sed 's/_gv[0-9]\+//g' | dot -Tjpg -o gvsub.jpg


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self):
        self.dot = graphviz.Digraph(format='png')
        self.dot.attr('node', shape='circle')

    def add_edge(self, child, parent):
        self.dot.edge(child, parent)

    def add_node(self, name, label=None):
        self.dot.node(name, label)

    def output(self):
        print(self.dot)

    def read_dot(self, raw_dot):
        return graphviz.Source.from_file(raw_dot)

    def render(self):
        self.dot.render('result2', view=True)

    def update_shape(self, shape):
        self.dot.attr('node', shape=shape)


if __name__ == '__main__':
    r = Renderer()

    line = '太郎は猫と犬を飼っている。'
    for n in parser.find_nodes(line):
        r.add_node(str(n), str(n))

    for t in parser.find_parent_child(line):
        r.add_edge(t[0], t[1])

    r.output()
    r.render()
