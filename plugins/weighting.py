#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter


def weighting(nodes, edges):
    color_counters = Counter(nodes)
    childen = [e[0] for e in edges]
    parents = [e[1] for e in edges]
    size_counters = Counter(childen) + Counter(parents)
    
    w_nodes = []
    for node in nodes:
        attr = {'fillcolor': '1', 'fontsize': '16', 'width': '1'}
        if node in color_counters:
            attr['fillcolor'] = str(min(7, color_counters[node]))

        if node in size_counters:
            attr['fontsize'] = str(16 + size_counters[node]*3)
            attr['width'] = str(max(1, size_counters[node]//2))

        w_nodes.append((node, attr))
    return w_nodes
