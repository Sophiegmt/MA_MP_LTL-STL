# -*- coding: utf-8 -*-

import numpy as np
import pyvisgraph as vg
from shapely.geometry import Point, LineString, shape
from STL import calculate_STL_cost
        
def construction_biased_tree(tree, n_max):
    """
    construction of the biased tree
    :param tree: biased tree
    :param n_max: maximum number of iterations
    :return: found path
    """
    # trivial suffix path, the initial state can transition to itself
    if tree.segment == 'suffix' and tree.check_transition_b(tree.init[1], tree.biased_tree.nodes[tree.init]['label'],
                                                            tree.init[1]):
        tree.goals.append(tree.init)
        if tree.buchi.buchi_graph.edges[(tree.init[1], tree.init[1])]['truth'] == '1':
            return {0: [0, []]}
        else:
            return {0: [0, [tree.init]]}

    for n in range(n_max):
        print("n:", n, "\n")
        # biased sample
        x_new, q_p_closest = tree.biased_sample()
        # couldn't find x_new
        if not x_new: continue
        # label of x_new
        label = []
        for i in range(tree.robot):
            ap = tree.get_label(x_new[i])
            ap = ap + '_' + str(i+1) if ap != '' else ap
            label.append(ap)
        # near state
        if tree.lite:
            # avoid near
            near_nodes = [q_p_closest]
        else:
            near_nodes = tree.near(tree.mulp2single(x_new))
            near_nodes = near_nodes + [q_p_closest] if q_p_closest not in near_nodes else near_nodes

        # check the line is obstacle-free
        obs_check = tree.obstacle_check(near_nodes, x_new, label)
        # not obstacle-free
        if tree.lite and not list(obs_check.items())[0][1]: continue

        # iterate over each buchi state
        for b_state in tree.buchi.buchi_graph.nodes:
            # new product state
            q_new = (x_new, b_state)
            # extend
            added = tree.extend(q_new, near_nodes, label, obs_check)
            # rewire
            if not tree.lite and added:
                tree.rewire(q_new, near_nodes, obs_check)

        # detect the first accepting state
        if n>25 and len(tree.goals): break

    return tree.find_path(tree.goals)

    

def path_via_visibility(tree, path):
    """
    using the visibility graph to find the shortest path
    :param tree: biased tree
    :param path: path found by the first step of the suffix part
    :return: a path in the free workspace (after treating all regions as obstacles) and its distance cost
    """	
    STL_cost = []
    paths = []
    max_len = 0
    # find a path for each robot using visibility graph method
    for i in range(tree.robot):
        init = path[-1][0][i]
        goal = path[0][0][i]
        shortest = tree.g.shortest_path(vg.Point(init[0], init[1]), vg.Point(goal[0], goal[1]))
        max_len = len(shortest) if len(shortest) > max_len else max_len
        paths.append([(point.x, point.y) for point in shortest])
    # append to the same length
    for i in range(tree.robot):
        paths[i] = paths[i] + [paths[i][-1]]*(max_len-len(paths[i]))
    # combine to one path of product state
    path_free = [(tuple([p[i] for p in paths]), '') for i in range(max_len)]  # second component serves as buchi state
    # calculate cost
    cost = 0

    for i in range(1, max_len):
        #print('STL_cost_connect_suf' ,STL_cost, '\n')
        STL_cost=calculate_STL_cost(tree.mulp2single(path_free[i][0]), tree.mulp2single(path_free[i-1][0]))
        cost = cost + np.linalg.norm(np.subtract(tree.mulp2single(path_free[i][0]), tree.mulp2single(path_free[i-1][0])))*STL_cost

    return cost, path_free
