#!/usr/bin/env python3

import random
import copy
import math


def init_policy(problem):
    """
    Initialize random policy
    :param problem: problem - object, for us it will be kuimaze.Maze object
    :return: dictionary of (random) policy, indexed by states
    """
    policy = dict()
    for state in problem.get_all_states():
        if problem.is_goal_state(state):
            policy[state] = None
            continue
        actions = [action for action in problem.get_actions(state)]
        policy[state] = random.choice(actions)
    return policy


def init_utils(problem):
    """
    Initialize all state utilities to their rewards
    :param problem: problem - object, for us it will be kuimaze.Maze object
    :return: dictionary of utilities, indexed by states
    """
    utils = dict()
    for state in problem.get_all_states():
        utils[state] = problem.get_reward(state)
    return utils


def find_policy_via_policy_iteration(problem, discount_factor):
    """
    Find optimal policy using policy iteration method
    :param problem: problem - object, for us it will be kuimaze.Maze object
    :param discount_factor: determines the present value of future rewards
    :return: dictionary of optimal policy, indexed by states
    """
    base_policy = init_policy(problem)
    utils = init_utils(problem)

    while True:
        stable_policy = True
        policy = copy.deepcopy(base_policy)
        for state in problem.get_all_states():
            if problem.is_goal_state(state):
                continue

            policy_eval = 0

            action_info = problem.get_next_states_and_probs(state,policy[state])
            for i in range(len(action_info)):
                policy_eval += action_info[i][1] * utils[action_info[i][0]]

            utils[state] = problem.get_reward(state) + discount_factor * policy_eval

            max_action_value = -math.inf
            best_action = None
            actions = [action for action in problem.get_actions(state)]
            for action in actions:
                action_info = problem.get_next_states_and_probs(state, action)
                action_value = 0
                for i in range(len(action_info)):
                    action_value += action_info[i][1] * utils[action_info[i][0]]
                if action_value > max_action_value:
                    max_action_value = action_value
                    best_action = action

            if max_action_value > policy_eval:
                base_policy[state] = best_action
                stable_policy = False

        if stable_policy:
            break
    
    return policy


def find_policy_via_value_iteration(problem, discount_factor, epsilon):
    """
    Find optimal policy using value iteration method
    :param problem: problem - object, for us it will be kuimaze.Maze object
    :param discount_factor: determines the present value of future rewards
    :param epsilon: impacts accuracy of estimation
    :return: dictionary of optimal policy, indexed by states
    """
    policy = init_policy(problem)
    utils = init_utils(problem)
    theta = epsilon * (1 - discount_factor) / discount_factor

    while True:
        v = copy.deepcopy(utils)
        delta = 0

        for state in problem.get_all_states():
            if problem.is_goal_state(state):
                policy[state] = None
                continue

            max_action_value = -math.inf
            actions = [action for action in problem.get_actions(state)]
            for action in actions:
                action_info = problem.get_next_states_and_probs(state, action)
                action_value = 0
                for i in range(len(action_info)):
                    action_value += action_info[i][1] * v[action_info[i][0]]
                if action_value > max_action_value:
                    max_action_value = action_value
                    policy[state] = action

            utils[state] = problem.get_reward(state) + discount_factor * max_action_value
            delta = max(delta, abs(utils[state] - v[state]))

        if delta < theta:
            break

    return policy

