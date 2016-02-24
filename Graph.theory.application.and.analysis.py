"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import simpleplot
import math
import random

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

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

def make_complete_graph2(num_nodes):
    """
    Function to produce full directed graph of input nodes.
    """
    if num_nodes == 0:
        return {0: set([])}
    complete_dir_graph = {}
    full_ls = [ node for node in range(num_nodes)]
    for start_node in range(num_nodes):
        temp_ls = list(full_ls)
        temp_ls.remove(start_node)
        complete_dir_graph[start_node] = set(temp_ls)
    return complete_dir_graph

def make_directed_graph(num_nodes, propability):
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
                random_var = random.random()
                if random_var < propability:
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


def DPA_directed_graph(n,m):
    current_graph_dic = make_complete_graph2(m)
    initial_node = DPATrial(m)
    for new_node in range(m, n):
        #pick_node = DPATrial(new_node)
        pick_node2 = initial_node.run_trial(m)
        current_graph_dic[new_node] = pick_node2
    return current_graph_dic

citation_graph = load_graph(CITATION_URL)
#DPA_graph = DPA_directed_graph(27770, 13)
    
in_degree = in_degree_distribution(citation_graph)
#in_degree = in_degree_distribution(DPA_graph)

#print DPA_graph

def compute_out_degrees(digraph):
    """
    Compute the out-degree of the input directed graph
    """
    out_degree_dic = {}
    for start_node in digraph:
        num = len(digraph[start_node])
        #print num
        if num in out_degree_dic:
            out_degree_dic[num] += 1
        else:
            out_degree_dic[num] = 1
    return out_degree_dic

#out = compute_out_degrees(citation_graph)
#print out
#score = 0
#student = 0
#for key in out:
#    score += out[key] * key
#    student += out[key]
#print score, student, float(score) / student    

nor_ls = []
for key in in_degree:
    nor_ls.append([math.log(key, 10), math.log(in_degree[key] / 27770., 10)])

#for key in in_degree:
#    nor_ls.append([key, in_degree[key]/27770.])

    
#nor_ls.pop(0)
#print nor_ls

#simpleplot.plot_scatter("Log/Log plot of the points of the normalized in_degree distribution (Question 1)", 600, 600, 
#                      "log of in_degree, base is 10", "log of number of nodes, base is 10", [nor_ls])

#simpleplot.plot_scatter("Log/Log plot of the points of the normalized in_degree distribution (Question 4 - DPA algorithm)", 600, 600, 
#                      "log of in_degree, base is 10", "log of number of nodes, base is 10", [nor_ls])


ran_graph = make_directed_graph(2000, 0.1)
#print ran_graph


in_ran_graph = in_degree_distribution(ran_graph)
#print in_ran_graph

in_ls = []
for key in in_ran_graph:
    in_ls.append([math.log(key, 10), math.log(in_ran_graph[key] / 2000., 10)])
    
    
#in_ls.pop(0)
#print nor_ls

simpleplot.plot_scatter("Log/Log plot of the points of the normalized in_degree distribution (Question 2, nodes = 2000, p = 0.1)", 600, 600, 
                        "log of in_degree, base is 10", "log of number of nodes, base is 10", [in_ls])

