#!/usr/bin/python2

import math
import random
import multiprocessing as mp

num_threads = 4

#import sys
#data = sys.stdin.readlines()

data = open('10.in', 'r').readlines()

# read / parse data
n = int(data[0])
graph = [[float(w) for w in data[i+1].strip().split(' ')] for i in range(n)]
color = data[n+1]
red_nodes = {k for k in range(n) if color[k] == 'R'}
blue_nodes = {k for k in range(n) if color[k] == 'B'}

# algorithm parameters / variables (attractiveness already have power to alpha applied to it
iterations = 2000
ants = 20
alpha = 2 
beta = 1
evap_const = 0.1
exploit_p = 0.95
Q = 1
tau = 1. / (48 * 40000)
attractiveness = [[(1./(1 + graph[i][j]))**alpha for j in range(n)] for i in range(n)]
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

def explore_choice(dictionary):
    return random.choice(dictionary.keys())

def max_choice(dictionary):
    choices = dictionary.items()
    return max(choices, key = lambda x: x[1])[0]

def update_trail_level(path):
    for i in range(n-1):
        trail_level[path[0][i]][path[0][i+1]] = trail_level[path[0][i]][path[0][i+1]] * (1. - evap_const) + (0. + Q) / path[1]
        trail_level[path[0][i+1]][path[0][i]] = trail_level[path[0][i+1]][path[0][i]] * (1. - evap_const) + (0. + Q) / path[1]
    trail_level[path[0][0]][path[0][-1]] = trail_level[path[0][0]][path[0][-1]] * (1. - evap_const) + (0. + Q) / path[1]
    trail_level[path[0][-1]][path[0][0]] = trail_level[path[0][-1]][path[0][0]] * (1. - evap_const) + (0. + Q) / path[1]

def update_trail_levels(paths):
    for i in range(n):
        for j in range(n):
            trail_level[i][j] *= (1.-evap_const)

    for path in paths:
        for i in range(n-1):
            trail_level[path[0][i]][path[0][i+1]] += (0. + Q) / path[1] #* graph[path[0][i]][path[0][i+1]]
            trail_level[path[0][i+1]][path[0][i]] += (0. + Q) / path[1] #* graph[path[0][i+1]][path[0][i]]
        trail_level[path[0][n-1]][path[0][0]] += (0. + Q) / path[1] #* graph[path[0][n-1]][path[0][0]]
        trail_level[path[0][0]][path[0][n-1]] += (0. + Q) / path[1] #* graph[path[0][0]][path[0][n-1]]

def remove_longest_from_path(path):
    max_len = 0
    max_idx = 0
    for i in range(n-1):
        cur_len = graph[path[i]][path[i+1]]
        if cur_len > max_len:
            max_len = cur_len
            max_idx = i
    return ([path[(k + max_idx + 1) % n] for k in range(n)], max_len)

def simulate_ant(choice_fn = random_choice, exploit = True):
    colors = color
    start = random.randint(0,n-1)
    red = set(list(red_nodes)) 
    blue = set(list(blue_nodes))
    nodes = set(list(range(n)))
    if colors[start] == 'B':
        red, blue = blue, red
        colors = ['B' if colors[i] == 'R' else 'R' for i in range(n)]
    red_left = (n+1)/2 - 1
    blue_left = (n+1)/2
    path = [start]
    red.remove(start)
    nodes.remove(start)
    length = 0
    num_red_prefix = 0
    while len(nodes): #red_left + blue_left:
        cur_node = path[-1]
        choices = 0
        if len(path) == 3: # count number of red nodes in a row at the beginning
            for i in range(len(path)):
                if colors[path[i]] == 'R':
                    num_red_prefix += 1
                else:
                    break
        if False and len(path) >= 3:
            # make sure we have enough blue nodes left; this also avoid three in a row on the boundary
            if blue_left == math.ceil((n - len(path) - 4 + num_red_prefix) / 3.):
                choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in red}
            # make sure we have enough red nodes left
            elif red_left == math.ceil((n - len(path) - 1) / 3.):
                choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in blue}
            else:
                if colors[path[-1]] == colors[path[-2]] == colors[path[-3]]: # three nodes of same color, must switch
                    if colors[path[-1]] == "R":
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
        choices = {node:attractiveness[cur_node][node]*trail_level[cur_node][node]**beta for node in nodes}
        if exploit and random.random() < exploit_p:
            choice = max_choice(choices)
        else:
            choice = choice_fn(choices)
        path.append(choice)
        trail_level[path[-1]][path[-2]] = trail_level[path[-1]][path[-2]] * (1. - evap_const) + (0. + tau)
        trail_level[path[-2]][path[-1]] = trail_level[path[-2]][path[-1]] * (1. - evap_const) + (0. + tau)
        nodes.remove(choice)
        length += graph[path[-2]][path[-1]]
        if colors[choice] == 'R':
            red.remove(choice)
            red_left -= 1
        else:
            blue.remove(choice)
            blue_left -= 1
    trail_level[path[-1]][path[0]] = trail_level[path[-1]][path[0]] * (1. - evap_const) + (0. + tau)
    trail_level[path[0]][path[-1]] = trail_level[path[0]][path[-1]] * (1. - evap_const) + (0. + tau)
    length += graph[path[-1]][path[0]]
    return (path, length)


# make worker threads
#threadpool = mp.Pool(num_threads)

# main loop
min_path = []
min_cost = 99999999999999
for i in range(iterations):
    if (i % (max(1, iterations / 100))) == 0:
        print "iteration %i..." %i
    #paths = threadpool.map(simulate_ant, [random_choice] * ants)
    #update_trail_levels(paths)
    paths = []
    for _ in range(ants):
        paths.append(simulate_ant(choice_fn = random_choice, exploit = True))
    paths.append(simulate_ant(choice_fn = max_choice, exploit = False))
    update_trail_level(min(paths, key = lambda x: x[1]))
    for path in paths:
        if path[1] < min_cost:
            min_path = path
            min_cost = path[1]
            print min_path

# best path as determined by ACO
best = simulate_ant(choice_fn = max_choice)
#print best
best_path = remove_longest_from_path(best[0])
#print best_path[0], best[1] - best_path[1]
out = ''
for i in best_path[0]:
    out += '%s ' %i
print out

