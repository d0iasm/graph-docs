import graphviz

graph = graphviz.Digraph(format='png')
graph.attr('node', shape='circle')

n = 15

for i in range(n):
    graph.node(str(i), str(i))

for i in range(n):
    print((i-1)//2)
    if(i - 1) // 2 >= 0:
        graph.edge(str((i-1)//2), str(i))

print(graph)
graph.render('graph')
