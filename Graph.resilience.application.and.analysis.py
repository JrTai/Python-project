"""
Provided code for Application portion of Module 2
Code by Jr-Han Tai for Module2 application 2015-06-25
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt
import gc


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

##########################################################
# Code for application 1

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

##########################################################
# UPA and DPA Trial

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

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

##########################################################
# Code for project 2

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
    
##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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

##########################################################
# Self write code

# compute edge for computer_network, ER graph, UPA graph
def compute_edge():
    #computer_network
    com_net = load_graph(NETWORK_URL)
    total_edge = 0
    for node in com_net:
        total_edge += len(com_net[node])
    print total_edge / 2, "computer network"
    # ER graph
    er_graph = make_undirected_graph(1239, 0.004)
    total_edge = 0
    for node in er_graph:
        total_edge += len(er_graph[node])
    print total_edge / 2, "ER"
    # UPA graph
    upa_graph = UPA_undirected_graph(1239,3)
    total_edge = 0
    for node in upa_graph:
        total_edge += len(upa_graph[node])
    print total_edge / 2, "UPA"

# create undirected ER graph
def make_undirected_graph(num_nodes, propability):
    """
    Function to produce propability undirected graph of input nodes.
    """
    if num_nodes == 0:
        return {0: set([])}
    complete_dir_graph = {}
    for start_node in range(num_nodes):
        temp_list = []
        for edge_node in range(num_nodes):
            if edge_node > start_node:
                random_var = random.random()
                if random_var < propability:
                    temp_list.append(edge_node)
                    if edge_node in complete_dir_graph:
                        complete_dir_graph[edge_node] = complete_dir_graph[edge_node].union(set([start_node]))
                    else:
                        complete_dir_graph[edge_node] = set([start_node])
        if start_node not in complete_dir_graph:
            complete_dir_graph[start_node] = set(temp_list)
        else:
            complete_dir_graph[start_node] = complete_dir_graph[start_node].union(set(temp_list))
    return complete_dir_graph 

# create UPA graph
def UPA_undirected_graph(node,m):
    current_graph_dic = make_complete_graph2(m)
    initial_node = UPATrial(m)
    for new_node in range(m, node):
        ##pick_node = DPATrial(new_node)
        pick_node2 = initial_node.run_trial(m)
        current_graph_dic[new_node] = pick_node2
        # compensate the new node to exist node
        for pick in pick_node2:
            current_graph_dic[pick] = current_graph_dic[pick].union(set([new_node]))
    return current_graph_dic

# random_order function
def random_order(ugraph):
    """
    take a graph, output a list of random order of node in the graph
    """
    random_ls = []
    for node in ugraph:
        random_ls.append(node)
    random.shuffle(random_ls)
    return random_ls

# compute resilience of graph under random attact 
def resilience_random():
    """
    Plot an example with two curves with legends
    """
    xvals = [x for x in range(1240)]
    computer_net_re = compute_resilience(com_net, random_order(com_net))
    er_re = compute_resilience(er_graph, random_order(er_graph))
    upa_re = compute_resilience(upa_graph, random_order(upa_graph))

    plt.plot(xvals, computer_net_re, '-b', label='Computer Network')
    plt.plot(xvals, er_re, '-r', label='ER Graph (p=0.004)')
    plt.plot(xvals, upa_re, '-g', label='UPA Graph (m=3)')
    plt.legend(loc='upper right')
    plt.ylabel('The size of the largest connect component')
    plt.xlabel('The number of nodes removed')
    plt.title('Resilience of graph (random attack)')
    plt.show()

# faster algorithm to generate target order from input ugraph
def fast_targeted_order(ugraph):
    new_ugraph = copy_graph(ugraph) 
    degree_sets = [set([]) for dummy_idx in range(len(new_ugraph))]
    for node in new_ugraph:
        degree = len(new_ugraph[node])
        degree_sets[degree].update(set([node])) 
    order_ls = []
    idx = 0
    reverse = [degree for degree in range(len(new_ugraph))]
    reverse.reverse()
    for degree in reverse:
        while len(degree_sets[degree]) != 0:
            random_node = random.choice(list(degree_sets[degree]))
            degree_sets[degree].difference_update(set([random_node]))
            for neighbor in new_ugraph[random_node]:
                #if neighbor in new_ugraph:
                nei_degree = len(new_ugraph[neighbor])
                degree_sets[nei_degree].difference_update(set([neighbor]))
                degree_sets[nei_degree - 1].update(set([neighbor]))
            order_ls.append(random_node)
            idx += 1
            #new_ugraph.pop(random_node)
            delete_node(new_ugraph, random_node)
    return order_ls

# output figure with running time and increaseed nodes number
def runtime_node_figure():
    xvals = [x for x in range(10, 1000, 10)]
    to_yvals = []
    fto_yvals = []
    for node in range(10, 1000, 10):
        upa_graph = UPA_undirected_graph(node,5)
        gc.disable()
        time1 = time.clock()
        targeted_order(upa_graph)
        time2 = time.clock()
        to_yvals.append(time2 - time1)
        time3 = time.clock()
        fast_targeted_order(upa_graph)
        time4 = time.clock() 
        fto_yvals.append(time4 - time3) 
        gc.enable()      
    
    plt.plot(xvals, to_yvals, '-b', label='Targeted_order')
    plt.plot(xvals, fto_yvals, '-r', label='Fast_targeted_order')
    plt.legend(loc='upper left')
    plt.ylabel('Running time')
    plt.xlabel('Number of nodes')
    plt.title('Desktop Python for runnung time versus number of nodes')
    plt.show()

# compute resilience of graph under target attact 
def resilience_target():
    """
    Plot an example with two curves with legends
    """
    xvals = [x for x in range(1240)]
    computer_net_re = compute_resilience(com_net, targeted_order(com_net))
    er_re = compute_resilience(er_graph, targeted_order(er_graph))
    upa_re = compute_resilience(upa_graph, targeted_order(upa_graph))

    plt.plot(xvals, computer_net_re, '-b', label='Computer Network')
    plt.plot(xvals, er_re, '-r', label='ER Graph (p=0.004)')
    plt.plot(xvals, upa_re, '-g', label='UPA Graph (m=3)')
    plt.legend(loc='upper right')
    plt.ylabel('The size of the largest connect component')
    plt.xlabel('The number of nodes removed')
    plt.title('Resilience of graph (target attack)')
    plt.show()            

##########################################################
# execute code
                                    
com_net = load_graph(NETWORK_URL)
er_graph = make_undirected_graph(1239,0.004)
upa_graph = UPA_undirected_graph(1239,3)
#runtime_node_figure()
#resilience_random()
resilience_target()
#compute_edge()
#time1 = time.time()
#print er_graph
#print upa_graph
#print len(targeted_order(upa_graph)) == len(fast_targeted_order(upa_graph))
#print targeted_order(upa_graph)
#print fast_targeted_order(upa_graph)
#time2 = time.time()
#print "time", time2 - time1
#print upa_graph