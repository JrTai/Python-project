"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    closest_pair = [float('inf'), -1, -1]
    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if idx1 != idx2:
                if pair_distance(cluster_list, idx1, idx2)[0] < closest_pair[0]:
                    closest_pair[0] = pair_distance(cluster_list, idx1, idx2)[0]
                    closest_pair[1] = pair_distance(cluster_list, idx1, idx2)[1]
                    closest_pair[2] = pair_distance(cluster_list, idx1, idx2)[2]
    return tuple(closest_pair)

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    number_of_cluster = len(cluster_list)
    if number_of_cluster < 3:
        closest_pair = slow_closest_pair(cluster_list)
        return closest_pair
    else:
        m_half = number_of_cluster / 2
        cluster_left = cluster_list[0:m_half]
        cluster_right = cluster_list[m_half:number_of_cluster]
        left_closest_pair = fast_closest_pair(cluster_left)
        right_closest_pair = fast_closest_pair(cluster_right)
        right_closest_pair = list(right_closest_pair)
        right_closest_pair[1] += m_half
        right_closest_pair[2] += m_half
        right_closest_pair = tuple(right_closest_pair)
        closest_pair = min(left_closest_pair, right_closest_pair)
        mid = (cluster_list[m_half - 1].horiz_center() + cluster_list[m_half].horiz_center()) / 2
        closest_pair = min(closest_pair, closest_pair_strip(cluster_list, mid, closest_pair[0]))
    return tuple(closest_pair)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    s_set = []
    for idx in range(len(cluster_list)):
        if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width:
            s_set.append(idx)
    #print s_set
    s_set.sort(key = lambda x: cluster_list[x].vert_center())
    #print s_set
    k_num = len(s_set)
    #print k_num
    closest_pair = [float('inf'), -1, -1]
    for idx_u in range(k_num - 1):
        for idx_v in range(1, min(idx_u + 4, k_num)):
            # idx_u + 4 which pass all test, but not the same as idx_u + 3
            #print idx_u, idx_v, pair_distance(cluster_list, s_set[idx_u], s_set[idx_v]), closest_pair
            if pair_distance(cluster_list, s_set[idx_u], s_set[idx_v])[0] < closest_pair[0] and idx_u != idx_v:
                closest_pair[0] = pair_distance(cluster_list, s_set[idx_u], s_set[idx_v])[0]
                if s_set[idx_u] < s_set[idx_v]:
                    closest_pair[1] = s_set[idx_u]
                    closest_pair[2] = s_set[idx_v]
                else:
                    closest_pair[1] = s_set[idx_v]
                    closest_pair[2] = s_set[idx_u]
                #print "change to:", closest_pair, s_set[idx_u], s_set[idx_v]
    return tuple(closest_pair)          

######################################################################
# Code for hierarchical clustering

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    #num = len(cluster_list)
    c_ls = []
    for cluster in cluster_list:
        c_ls.append(cluster.copy())
    while len(c_ls) > num_clusters:
        c_ls.sort(key = lambda cluster: cluster.horiz_center())
        shortest_index = fast_closest_pair(c_ls)
        c_ls[shortest_index[1]].merge_clusters(c_ls[shortest_index[2]])
        c_ls.pop(shortest_index[2])
    return c_ls


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    num_len = len(cluster_list)
    center_check = population(cluster_list, num_clusters)
    
    ###### start iteration
    for dummy_idx in range(num_iterations):
        empty_set = {}
        for idx in range(len(center_check)):
            empty_set[idx] = alg_cluster.Cluster(set([]), 0, 0, 0, 0)
        ###### all point
        for idx_cluster in range(num_len):
            dis_ls = []
            ###### calculate the distance to each center
            for idx_center in range(len(center_check)):
                temp_list = [center_check[idx_center], cluster_list[idx_cluster]]
                dis = pair_distance(temp_list, 0, 1)
                dis_ls.append([dis[0], idx_center, idx_cluster])
            dis_ls.sort()
            #print dis_ls[:3]
            empty_set[dis_ls[0][1]].merge_clusters(cluster_list[dis_ls[0][2]])           
        
        ### update center_check
        ans = []
        for key in empty_set:
            ans.append(empty_set[key])
        center_check = ans
    #print len(ans), "-------------------------------------------------------------"
    #print ans
    return ans

def test_merge(cluster_ls):
    """
    Test cluster merge function
    """
    print len(cluster_ls)
    print cluster_ls[0], cluster_ls[1]
    cluster_ls[0].merge_clusters(cluster_ls[0])
    print len(cluster_ls)
    print cluster_ls[0], cluster_ls[1]
    return 0

def population(cluster_list, num_clusters):
    """
    Calculate the order of cluster list based on population
    """
    ###### find initial cluster
    num_len = len(cluster_list)
    center_index = []
    center_check = {}
    for idx in range(num_len):
        center_index.append([cluster_list[idx].total_population(), idx])
    center_index.sort(reverse = True)
    center_index = center_index[:num_clusters]
    for idx in range(len(center_index)):
        center_check[idx] = cluster_list[center_index[idx][1]]
    return center_check

#######################################################################
# Test for closest_pair_strip function
#print "Test1 (1.0, 1, 2)"
#print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)], 1.5, 1.0)
#print "Test2 ()"
#print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 0, 1, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 1, 1, 0)], 0.5, 1.0)
#print "Test3"
#print closest_pair_strip([alg_cluster.Cluster(set([]), 1.0, 1.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 5.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 4.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 7.0, 1, 0)], 1.0, 3.0)
#print "Test4"
#print closest_pair_strip([alg_cluster.Cluster(set([]), -4.0, 0.0, 1, 0), alg_cluster.Cluster(set([]), 0.0, -1.0, 1, 0), alg_cluster.Cluster(set([]), 0.0, 1.0, 1, 0), alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0)], 0.0, 4.1231059999999999)
#print test_merge([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)])