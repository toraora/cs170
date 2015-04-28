#!/usr/bin/python2

import math
import random
import multiprocessing as mp

#import sys
#data = sys.stdin.readlines()

data = open('4.in', 'r').readlines()

# read / parse data
n = int(data[0])
graph = [[int(w) for w in data[i+1].strip().split(' ')] for i in range(n)]
color = data[n+1]
red_nodes = {k for k in range(n) if color[k] == 'R'}
blue_nodes = {k for k in range(n) if color[k] == 'B'}
if color[0] == 'B': # make starting color always red, for simplicity
    color = ['B' if color[i] == 'R' else 'R' for i in range(n)]

# algorithm parameters / variables (attractiveness already have power to alpha applied to it
iterations = 500
ants = 1000
alpha = 3
beta = 2
evap_const = 0.01
Q = n
attractiveness = [[(1./(0.1 + graph[i][j]))**alpha for j in range(n)] for i in range(n)]
trail_level = [[0 if i == j else 1 for j in range(n)] for i in range(n)]

# helper functions
def random_choice(dictionary):
    choices = dictionary.keys()
    total = math.fsum([dictionary[k] for k in choices])
    r = random.random() * total
    cur = 0
    k = 0
    for i in range(len(choices)):
        if cur + dictionary[choices[i]] >= r:
            k = i
            break
        cur += dictionary[choices[i]]
    return choices[k]

def max_choice(dictionary):
    choices = dictionary.items()
    return max(choices, key = lambda x: x[1])[0]

def update_trail_levels(paths):
    for i in range(n):
        for j in range(n):
            trail_level[i][j] *= (1-evap_const)

    for path in paths:
        for i in range(n-1):
            trail_level[path[0][i]][path[0][i+1]] += (0. + Q) / path[1] * graph[path[0][i]][path[0][i+1]]

def remove_longest_from_path(path):
    max_len = 0
    max_idx = 0
    for i in range(n-1):
        cur_len = graph[path[i]][path[i+1]]
        if cur_len > max_len:
            max_len = cur_len
            max_idx = i
    return ([path[(k + max_idx + 1) % n] for k in range(n)], max_len)

def simulate_ant(choice_fn = random_choice):
    red = set(list(red_nodes))
    blue = set(list(blue_nodes))
    red_left = (n+1)/2 - 1
    blue_left = (n+1)/2
    red.remove(0)
    path = [0]
    length = 0
    num_red_prefix = 0
    while red_left + blue_left:
        cur_node = path[-1]
        if len(path) == 3: # count number of red nodes in a row at the beginning
            for i in range(len(path)):
                if color[path[i]] == 'R':
                    num_red_prefix += 1
                else:
                    break
        if len(path) >= 3:
            # make sure we have enough blue nodes left; this also avoid three in a row on the boundary
            if blue_left == math.ceil((n - len(path) - 4 + num_red_prefix) / 3.):
                choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in red}
            # make sure we have enough red nodes left
            elif red_left == math.ceil((n - len(path) - 1) / 3.):
                choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in blue}
            else:
                if color[path[-1]] == color[path[-2]] == color[path[-3]]: # three nodes of same color, must switch
                    if color[path[-1]] == "R":
                        choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in blue}
                    else:
                        choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in red}
                else:
                    r_dict = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in red}
                    b_dict = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in blue}
                    r_dict.update(b_dict)
                    choices = r_dict
        else:
            r_dict = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in red}
            b_dict = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in blue}
            r_dict.update(b_dict)
            choices = r_dict
        assert (len(choices) != 0), "ant failed to make path"
        choice = choice_fn(choices)
        path.append(choice)
        length += graph[path[-2]][path[-1]]
        if color[choice] == 'R':
            red.remove(choice)
            red_left -= 1
        else:
            blue.remove(choice)
            blue_left -= 1
    length += graph[path[-1]][path[0]]
    return (path, length)


# make worker threads
threadpool = mp.Pool(4)

# main loop
for i in range(iterations):
    print "iteration %i..." %i
    paths = threadpool.map(simulate_ant, [random_choice] * ants)
    update_trail_levels(paths)

# best path as determined by ACO
best = simulate_ant(choice_fn = max_choice)
print best
best_path = remove_longest_from_path(best[0])
print best_path[0], best[1] - best_path[1]


