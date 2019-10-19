#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt


simple_graph = nx.Graph()
simple_graph = nx.DiGraph()
simple_graph.add_node(1)
simple_graph.add_nodes_from([2,3,4,5,6,7,8])

#simple_graph.add_edge(1,2)
simple_graph.add_edges_from([(2,3),(4,5),(6,7),(7,8),(3,1),(5,1),(8,1)])
print(list(simple_graph.pred[1]))
nx.draw_networkx(simple_graph)
plt.show()