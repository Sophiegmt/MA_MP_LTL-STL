# -*- coding: utf-8 -*-

import numpy as np
import math
from shapely.geometry import Point, LineString, shape
from shapely.ops import nearest_points
from buchi_parse import Buchi
from workspace import Workspace
from task import Task

workspace = Workspace()
task = Task()
buchi = Buchi(task)
obstacles = workspace.obs

def calculate_STL_cost(new_state, neighbor_state):

    (minVal, mobs, maxVal, Mobs )= max_min_distances_to_obs(new_state, neighbor_state)
    # min distance
    if mobs=='o1':
        qsi_min=minVal-0.1 # robot has to be at least 0.3m away from obstacles
        
    elif mobs=='o2':
        qsi_min=minVal-0.1

    """ 	# max distance
    if Mobs=='o1':
        qsi_max=0.5-maxVal # robot has to be less than 0.5m away from obstacles
        
    elif Mobs=='o2':
        qsi_max=0.4-maxVal 
    """
        
    #cost calculation for obs distance
    #qsi=min(qsi_min,qsi_max)


    stl_cost = max(math.exp(-10*(qsi_min)),1)
    #print('stl_cost',stl_cost, '\n')

    return stl_cost

def max_min_distances_to_obs(new_state, neighbor_state):
    """
    Verify and calculate cost according to the level of respect for STL formulas
    """
    nearest_obs=[]
    min_dist=math.inf
    max_dist=0

    line_str = LineString([Point(new_state), Point(neighbor_state)])
    #print('line_str',line_str)
    i=1
    for (obs, boundary) in iter(obstacles.items()):
        #Determine the minimum distance of the path to obstacles
    	for o in nearest_points(boundary, line_str):
    	
            if i%2!=0:
                nearest_obs=o.coords[0]

            elif i%2==0:
                nearest_path=o.coords[0]
                mdist = np.linalg.norm(np.subtract(nearest_obs, nearest_path))
                if mdist < min_dist:
                    nearest_o = np.array(nearest_obs)
                    min_dist = mdist
                    c_obstacle = obs
            i+=1
            
        #Determine the maximum distance of the path to obstacles
    	Mdist = line_str.distance(boundary)
    	if Mdist > max_dist:
            max_dist = Mdist
            f_obstacle = obs
            
            
    print('farthest obstacle', f_obstacle)
    print('max_dist', max_dist)
	    
    print('closest obstacle', c_obstacle)
    print('min_dist', min_dist)
    
    return (min_dist,c_obstacle,max_dist,f_obstacle)
