#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Simple agent for finding optimal policy by Q-learning
@author Richard Koeplinger
@contact: kopliric@fel.cvut.cz
"""

import numpy as np
import math


def walk_randomly(env, alpha, q_table):
    """
    Walking randomly and learning about given environment
    :param env: object, for us it will be kuimaze.Maze object
    :param alpha: learning rate
    :param q_table: initialized table for storing learnt Q values of states in environment
    """
    obv = env.reset()
    state = obv[0:2]
    is_done = False
    gamma = 1   # discount factor
    MAX_T = 1000  # max trials (for one episode)
    t = 0

    while not is_done and t < MAX_T:
        t += 1
        action = env.action_space.sample()
        obv, reward, is_done, _ = env.step(action)
        nextstate = obv[0:2]

        max_value = -math.inf
        for a in range(4):
            value = q_table[nextstate[0]][nextstate[1]][a]
            if value > max_value:
                max_value = value
        q_table[state[0]][state[1]][action] += alpha * (
                    reward + gamma * max_value - q_table[state[0]][state[1]][action])

        state = nextstate


def find_policy(q_table, maze_size):
    """
    Finds optimal policy in each state of environment
    :param q_table: learnt Q values of states in environment
    :param maze_size: dimensions of environment
    :return: dictionary of policy, indexed by state coordinates
    """
    policy = dict()
    for x in range(maze_size[0]):
        for y in range(maze_size[1]):
            state = (x, y)
            max_value = -math.inf
            action = None
            for a in range(4):
                value = q_table[state[0]][state[1]][a]
                if value > max_value:
                    max_value = value
                    action = a
            policy[state] = action
    return policy


def learn_policy(env):
    """
    Learn about environment and find optimal policy
    :param env: object, for us it will be kuimaze.Maze object
    :return: dictionary of policy, indexed by state coordinates
    """
    x_dims = env.observation_space.spaces[0].n
    y_dims = env.observation_space.spaces[1].n
    maze_size = tuple((x_dims, y_dims))
    num_actions = env.action_space.n

    q_table = np.zeros([maze_size[0], maze_size[1], num_actions], dtype=float)

    alpha = 1   # learning rate
    k = 50
    t = 0
    while t < 500 and alpha > 0.1:
        t += 1
        alpha = k / (k + t)
        walk_randomly(env, alpha, q_table)

    policy = find_policy(q_table, maze_size)
    return policy
