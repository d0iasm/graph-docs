import graphviz

import parser


class Renderer(object):
    """Image renderer from natural language. """
    def __init__(self):
        self.graph = graphviz.Digraph(format='png')
        self.graph.attr('node', shape='circle')

    def update_shape(self, shape):
        self.graph.attr('node', shape=shape)

    def add_node(self, name, label=None):
        self.graph.node(name, label)

    def add_edge(self, child, parent):
        self.graph.edge(child, parent)

    def output(self):
        print(self.graph)

    def render(self):
        self.graph.render('result')

       
if __name__ == '__main__':
    r = Renderer()
    # n = 15
    # for i in range(n):
        # g.add_node(str(i), str(i))

    # for i in range(n):
        # if(i - 1) // 2 >= 0:
            # g.add_edge(str((i-1)//2), str(i))

    # g.output()
    # g.render()

    line = '太郎は花子が読んでいる本を次郎に渡した'
    for n in parser.find_nodes(line):
        r.add_node(str(n), str(n))

    for t in parser.find_parent_child(line):
        r.add_edge(t[0], t[1])

    r.output()
    r.render()
