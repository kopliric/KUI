#!/usr/bin/python3
'''
Homework #02-Search for B3B33KUI
@author: Richard Köplinger
@contact: kopliric@fel.cvut.cz
@date: 2023-03-04
'''

import time
import kuimaze
import os
import heapq as hq

class Node:
    def __init__(self, parent=None, position=None, price=None):
        self.parent = parent
        self.position = position    # x,y coordinates
        if parent != None:
            self.price = parent.price + price
        else:
            self.price = price;
        self.estimate= 0      # total price from start + Manhattan distance to goal
    
    def get_estimate(self, goal):
        distance = abs(self.position[0] - goal.position[0]) + abs(self.position[1] - goal.position[1])
        self.estimate = self.price + distance
    
    def __lt__(self,nxt):   # overwrites the comparison operator in heapq
        return self.estimate <= nxt.estimate

class Agent(kuimaze.BaseAgent):
    def __init__(self, environment):
        self.environment = environment

    def find_path(self):
        '''
        searching for a path in the enviroment
        return: a path as a list of positions [(x1, y1), (x2, y2), ... ].
        '''
        observation = self.environment.reset()  # must be called first, it is necessary for maze initialization
        goal = observation[1][0:2]
        start = observation[0][0:2]             # initial state (x, y)
        
        goal_node = Node(None, goal, 0)
        start_node = Node(None, start, 0)
        
        opened = []     # store currently opened nodes
        visited = []    # store visited nodes
        hq.heapify(opened)
        start_node.get_estimate(goal_node)
        hq.heappush(opened, start_node)
        
        path = None
        print("Starting searching")
        while len(opened) > 0:      # search until no more nodes avalable
            current_node = hq.heappop(opened) 
            visited.append(current_node.position)

            if current_node.position == goal_node.position:
                print("goal reached")
                path = []
                while current_node != None:
                    path.insert(0, current_node.position) # create path as list of tuples in format: [(x1, y1), (x2, y2), ... ]
                    current_node = current_node.parent
                break
            
            new_positions = self.environment.expand(current_node.position)         # [[(x1, y1), cost], [(x2, y2), cost], ... ]
            for position in new_positions:
                if position[0] in visited:  # ignore already visited nodes
                    continue
                node = Node(current_node, position[0], position[1])
                node.get_estimate(goal_node)
                hq.heappush(opened, node)
            
            # self.environment.render()               # show enviroment's GUI       DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!      
            # time.sleep(0.1)                         # sleep for demonstartion     DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION! 

        return path


if __name__ == '__main__':

    MAP = 'maps/normal/normal11.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), MAP)
    GRAD = (0, 0)
    SAVE_PATH = False
    SAVE_EPS = False

    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)       # For using random map set: map_image=None
    agent = Agent(env) 

    path = agent.find_path()
    print(path)
    env.set_path(path)          # set path it should go from the init state to the goal state
    if SAVE_PATH:
        env.save_path()         # save path of agent to current directory
    if SAVE_EPS:
        env.save_eps()          # save rendered image to eps
    env.render(mode='human')
    time.sleep(3)

