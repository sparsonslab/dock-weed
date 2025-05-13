"""
Summary
-------
Functions for topological sorting and display of directed graphs.


Extended Summary
----------------
A directed graph is represented as a dict with entries:
<node name>:[<list of nodes that feed either in or out of it>]
e.g.
incoming representation:
{'a':[], 'b':['a'], 'c':['a', 'b']}
outgoing representation:
{'a':['b', 'c'], 'b':['c'], 'c':[]}

Author
------
Sean Parsons @ Enthought Inc., March-April 2020.
"""

import copy

import random

import matplotlib.pyplot as plt


def reverse_directions(graph: dict) -> dict:
    """ Reverse edge directions on a directed graph.

    Extended Summary
    ----------------
    The dict representation of a directed graph has entries,
    <node name>:[<list of nodes that feed in/out of it>]
    For example:
    {'a':[],
     'b':['a'],
     'c':['a', 'b']}
     This function reverses the representation (out-of-place)
     from incoming to outgoing (or vise-versa).

    Parameters
    ----------
    graph: dict of list
        The graph representation.

    Returns
    -------
    dict of list
        The reversed graph representation.
    """
    graph_reversed = {}
    for k, v in graph.items():
        graph_reversed[k] = []
        for p, q in graph.items():
            if k in q:
                graph_reversed[k].append(p)
    return graph_reversed


def kahns_algorithm(graph: dict, incoming=True) -> list:
    """ Kahn's algorithm to get the topological order (sort) of a graph.

    Parameters
    ----------
    graph: dict of list
        The representation of the graph (see reverse_directions()).
    incoming: bool
        Is this an "incoming" representation (as against outgoing).

    Returns
    -------
    list of str
        The execution/run order of the nodes.
        An empty list if the algorithm detects that the graph is cyclic.

    Notes
    -----
    This is used to get the execution order for the optimization function.
    (see objective_function())

    References
    ----------
    This comes straight from the pseudo-code in the Wikipedia article,
    https://en.wikipedia.org/wiki/Topological_sorting
    But it works!
    """
    # reverse graph if connections are outgoing
    if not incoming:
        graph_incoming = reverse_directions(graph)
    else:
        graph_incoming = copy.deepcopy(graph)

    # transitive reduction
    # ???? don't need, but may reduce time

    # set of nodes with no incoming edges
    no_incoming_set = [node for node, edges in graph_incoming.items() if
                       not edges]

    # topological sort
    order_set = []
    while no_incoming_set:
        n = no_incoming_set.pop(0)
        order_set.append(n)
        for node, edges in graph_incoming.items():
            if edges:
                for i, m in reversed(list(enumerate(graph_incoming[node]))):
                    if m == n:
                        graph_incoming[node].pop(i)
                if not graph_incoming[node]:
                    no_incoming_set.append(node)

    # number of edges left in incoming graph
    # should be zero for an acyclic graph
    u = sum([len(x) for x in graph_incoming.values()])
    if u == 0:
        return order_set
    return []


def coffman_graham_algorithm(graph: dict, incoming=True,
                             layer_max=1000) -> list:
    """ Coffman-Graham algorithm for calculating execution layers of a graph.

    Parameters
    ----------
    graph: dict of list
        The representation of the graph (see reverse_directions()).
    incoming: bool
        Is this an "incoming" representation (as against outgoing)?
    layer_max: int
        The maximum number of nodes allowable in a layer.

    Returns
    -------
    list of list of str
        The ordered layers.
        Each layer is a list of the node names in that layer.

    Notes
    -----
    This is not actually used at present, but could be if we wanted to execute
    nodes in parallel. Of course this would also require implementing some
    kind of scheme to notify when all nodes in a layer have finished executing.
    If we used a framework like Spark, this would be built in.

    References
    ----------
    https://en.wikipedia.org/wiki/Coffman-Graham_algorithm
    """
    # reverse graph if connections are outgoing
    if not incoming:
        graph_incoming = reverse_directions(graph)
    else:
        graph_incoming = copy.deepcopy(graph)

    # topological order
    order_set = kahns_algorithm(graph_incoming)
    if not order_set:
        return []

    # create layers
    layers = [[]]
    for node in order_set:
        #    if current layer is larger than the size limit
        # OR if the node has an incoming edge from the current layer
        # -> start new layer
        if (len(layers[-1]) >= layer_max) or (
        [v for v in graph_incoming[node] if v in layers[-1]]):
            layers.append([node])
        # otherwise append to the current layer
        else:
            layers[-1].append(node)

    return layers


def plot_layers(graph: dict, incoming=True, layer_max=1000, layer_spread=0.2,
                fsize=(8, 5)):
    """ Plot graph as a series of execution layers.

    Extended Summary
    ----------------
    A minimal plot of a graph. Could be much improved!

    Parameters
    ----------
    graph: dict of list
        The representation of the graph (see reverse_directions()).
    incoming: bool
        Is this an "incoming" representation (as against outgoing)?
    layer_max: int
        The maximum number of nodes allowable in a layer.
    layer_spread: float
        The nodes of a single layer are spaced horizontally. This gives their
        x-coordinate a little random wiggle, so that edges do not pass through
        nodes they have nothing to do with.
    fsize: tuple
        Figure size.
    """
    # execution layers
    layers = coffman_graham_algorithm(
        graph,
        incoming=incoming,
        layer_max=layer_max)

    if not layers:
        print('graph is cyclic')
        return

    # (x, y) coordinates of nodes
    label = []
    xcoor = []
    ycoor = []
    for i, layer in enumerate(layers):
        for j, node in enumerate(layer):
            label.append(node)
            xcoor.append(
                j - len(layer) / 2 + random.normalvariate(0, layer_spread))
            ycoor.append(i)

    # figures
    fig = plt.figure(figsize=fsize)

    # plot nodes
    label_offset = 0.05
    plt.scatter(xcoor, ycoor)
    plt.ylabel('layer#', fontsize='large')
    plt.yticks([i for i in range(len(layers))])
    plt.xticks([])

    # plot edges and labels
    for i, txt in enumerate(label):
        for edge in graph[txt]:
            j = label.index(edge)
            plt.plot([xcoor[j], xcoor[i]], [ycoor[j], ycoor[i]], ':')
        plt.annotate(
            txt,
            (xcoor[i] + label_offset, ycoor[i]),
            fontsize='large'
        )
