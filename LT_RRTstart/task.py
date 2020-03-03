# -*- coding: utf-8 -*-

from workspace import Workspace, get_label
from random import uniform
import numpy as np


class Task(object):
    """
    define the task specified in LTL
    """
    def __init__(self):
        """
        +----------------------------+
        |   Propositonal Symbols:    |
        |       true, false          |
        |	    any lowercase string |
        |                            |
        |   Boolean operators:       |
        |       !   (negation)       |
        |       ->  (implication)    |
        |       &&  (and)            |
        |       ||  (or)             |
        |                            |
        |   Temporal operators:      |
        |       []  (always)         |
        |       <>  (eventually)     |
        |       U   (until)          |
        +----------------------------+
        """
        workspace = Workspace()

        # task specification, e_i are subformulas, li_j means the j-th robot is at regions l_i
        # -----------------------------
        
        #---- Task 1 -------------------------------------
        #self.formula = '<> e1 && []<> (e2 && <>e3)'
        #self.subformula = {1: '(l1_1)',
        #                   2: '(l2_1)',
        #                   3: '(l3_1)'
        #                   }
        # --------------------------------- Tas>k 2 -------------------------------------
        self.formula = '[]<> e1 && []<> e3 && []<> e4 && (!e1 U e2)'
        self.subformula = { 1: '(l1_1)',
                            2: '(l2_1)',
                            3: '(l5_2)',
                            4: '(l4_2)'
                          }

        # --------------------------------- Task 3 -------------------------------------
        #randomly generate tasks
        #self.formula = '[]<> e1 && []<> e2 && []<> e3 && []<>(e4 && <>(e5 && <> e6)) && <> e7 && []<>e8 && (!e7 U e8)'
        #num_of_robot_in_one_group = 3
        #self.number_of_robots = 8*num_of_robot_in_one_group
        #group = np.array(range(1, self.number_of_robots + 1))
        #np.random.shuffle(group)
        #group = group.reshape(8, num_of_robot_in_one_group)
        #print('group', group)
        #formula = []
        #for i in range(8):
        #     subformula = []
        #     for j in range(num_of_robot_in_one_group):
        #         subformula.append('l' + str(np.random.randint(1, 7)) + '_' + str(group[i][j]))
        #     for j in range(num_of_robot_in_one_group//2):
        #         while True:
        #             g = np.random.randint(7)
        #             robot = group[g][np.random.randint(num_of_robot_in_one_group)]
        #             if robot not in group[i]:
        #                 break
        #         subformula.append('l' + str(np.random.randint(1, 7)) + '_' + str(robot))
        #     formula.append('(' + ' && '.join(subformula) + ')')
        #self.subformula = {i: formula[i-1] for i in range(1, 9)}
        #print('subformulas', self.subformula)
	    # --------------------------------- Task 4 -------------------------------------
        #self.formula = '[]<> e1 && []<> e2 && []<> e3 && []<>(e4 && <>(e5 && <> e6))'
        #self.subformula = {
        #	  1: '(l1_1 && l1_2)',
        #	  2: '(l2_2 && l2_3)',
        #     3: '(l3_3 && l3_4)',
        #     4: '(l4_1)',
        #     5: '(l5_4)',
        #      6: '(l6_3)'}

        # randomly generate initial locations of robots with empty atomic propositions
        self.number_of_robots = 2  # for task 3
  
        self.init = []  # initial locations
        self.init_label = []  # labels of initial locations
        for i in range(self.number_of_robots):
            while True:
                ini = [round(uniform(0, workspace.workspace[k]), 3) for k in range(len(workspace.workspace))]
                print('init', tuple(ini), '\n')
                ap = get_label(ini, workspace)
                if 'o' not in ap:
                    break
            self.init.append((0.921, 0.372))
            ap = ap + '_' + str(i + 1) if 'l' in ap else ''
            self.init_label.append(ap)
        self.init = tuple(self.init)          # in the form of ((x, y), (x, y), ...)
        self.threshold = 0.005                # minimum distance between any pair of robots

