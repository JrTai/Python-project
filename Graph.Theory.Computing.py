"""
2015/06/03 AT-I, Degree distributions for graphs
By Jr-Han Tai
"""
#Three constant graph dictionary claim
EX_GRAPH0 = {0: set([1, 2]), 
             1: set([]), 
             2: set([])}
EX_GRAPH1 = {0:set([1, 4, 5]),
             1:set([2, 6]),
             2:set([3]),
             3:set([0]),
             4:set([1]),
             5:set([2]),
             6:set([])}
EX_GRAPH2 = {0:set([1, 4, 5]),
             1:set([2, 6]),
             2:set([3, 7]),
             3:set([7]),
             4:set([1]),
             5:set([2]),
             7:set([3]),
             6:set([]),
             8:set([1, 2]),
             9:set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """
    Function to produce full directed graph of input nodes.
    """
    if num_nodes == 0:
        return {0: set([])}
    complete_dir_graph = {}
    for start_node in range(num_nodes):
        temp_list = []
        for edge_node in range(num_nodes):
            if start_node != edge_node:
                temp_list.append(edge_node)
        complete_dir_graph[start_node] = set(temp_list)
    return complete_dir_graph

def compute_in_degrees(digraph):
    """
    Compute the in-degree of the input directed graph
    """
    in_degree_dic = {}
    for start_node in digraph:
        for end_node in digraph[start_node]:
            if end_node in in_degree_dic:
                in_degree_dic[end_node] += 1
            else:
                in_degree_dic[end_node] = 1
    if len(in_degree_dic) == len(digraph):
        return in_degree_dic
    else:
        for node in digraph:
            if node not in in_degree_dic:
                in_degree_dic[node] = 0
        return in_degree_dic

def in_degree_distribution(digraph):
    """
    Compute the in-degree distribution of the input directed graph
    """
    in_degree_dic = compute_in_degrees(digraph)
    degree_distribution = {}
    for node in in_degree_dic:
        if in_degree_dic[node] not in degree_distribution:
            degree_distribution[in_degree_dic[node]] = 1
        else:
            degree_distribution[in_degree_dic[node]] += 1
    return degree_distribution
            
           
    