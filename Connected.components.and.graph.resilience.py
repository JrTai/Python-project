"""
2015/06/21 AT-I, Connected components and graph resilience
By Jr-Han Tai
"""

# import module
import random

# project function
def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node and returns
    the set consisting of all nodes that are visited by a breadth-first 
    search that starts at start_node.
    """
    queue = []
    visited = [start_node]
    queue.append(start_node)
    while len(queue) != 0:
        de_node = queue.pop(0)
        for neighbor_node in ugraph[de_node]:
            if neighbor_node not in visited:
                visited.append(neighbor_node)
                queue.append(neighbor_node)
    return set(visited)                

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, where 
    each set consists of all the nodes (and nothing else) in a connected 
    component, and there is exactly one set in the list for each connected 
    component in ugraph and nothing else.
    """
    remaining_nodes = []
    for node in ugraph:
        remaining_nodes.append(node)
    remaining_nodes = set(remaining_nodes)
    conected_node = []
    while len(remaining_nodes) != 0:
        first_node = random.choice(list(remaining_nodes))
        conect_part_from_start_node = bfs_visited(ugraph, first_node)
        conected_node.append(conect_part_from_start_node)
        remaining_nodes.difference_update(set(conect_part_from_start_node))
    return conected_node

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer) of
    the largest connected component in ugraph.
    """
    conected_node = cc_visited(ugraph)
    max_size = -float("inf")
    for node_number in conected_node:
        if len(node_number) > max_size:
            max_size = len(node_number)
    if max_size == -float("inf"):
        return 0
    else:
        return max_size       
    
def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and
    iterates through the nodes in attack_order. For each node in the list,
    the function removes the given node and its edges from the graph and 
    then computes the size of the largest connected component for the 
    resulting graph.
    
    The function should return a list whose k+1th entry is the size of the
    largest connected component in the graph after the removal of the first
    k nodes in attack_order. The first entry (indexed by zero) is the size 
    of the largest connected component in the original graph.
    """      
    ls_size = []
    ls_size.append(largest_cc_size(ugraph))
    for att_node in attack_order:
        ugraph.pop(att_node)
        # check if node in other node's edge removed as well
        for left_node in ugraph:
            ugraph[left_node].difference_update(set([att_node]))
        ls_size.append(largest_cc_size(ugraph))
    return ls_size