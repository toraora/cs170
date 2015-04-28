#!/usr/bin/python2

import math
import random

#import sys
#data = sys.stdin.readlines()

data = open('2.in', 'r').readlines()

# read / parse data
n = int(data[0])
graph = [[int(w) for w in data[i+1].strip().split(' ')] for i in range(n)]
color = data[n+1]
red_nodes = {k for k in range(n) if color[k] == 'R'}
blue_nodes = {k for k in range(n) if color[k] == 'B'}
if color[0] == 'B':
    color = ['B' if color[i] == 'R' else 'R' for i in range(n)]

# algorithm parameters / variables (attractiveness already have power to alpha applied to it
iterations = 1000
ants = 100
alpha = 1
beta = 1
evap_const = 0.5
Q = n
attractiveness = [[(1./(0.5 + graph[i][j]))**alpha for j in range(n)] for i in range(n)]
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

def update_trail_levels(paths):
    for i in range(n):
        for j in range(n):
            trail_level[i][j] *= (1-evap_const)

    for path in paths:
        for i in range(n-1):
            trail_level[path[0][i]][path[0][i+1]] += (0. + Q) / path[1]

def get_best_path():



# main loop
for _ in range(iterations):
    paths = [] 
    for k in range(ants):
        red = set(list(red_nodes))
        blue = set(list(blue_nodes))
        red_left = (n+1)/2 - 1
        blue_left = (n+1)/2
        red.remove(0)
        path = [0]
        length = 0
        while red_left + blue_left:
            cur_node = path[-1]
            if len(path) >= 3:
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
            choice = random_choice(choices)
            path.append(choice)
            length += graph[path[-2]][path[-1]]
            if color[choice] == 'R':
                red.remove(choice)
                red_left -= 1
            else:
                blue.remove(choice)
                blue_left -= 1
        paths.append([path, length])
    update_trail_levels(paths)



