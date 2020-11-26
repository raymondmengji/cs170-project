import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, order, prettyprint
import sys
import glob
import os
import gurobipy as gp
from gurobipy import GRB
import bruteforce
import lp
import random

def specific(G, best_val, k, s_max):
    n = G.order()

    happiness = {}
    stress = {}
    for i in range(n):
        happiness[i] = {}
        stress[i]    = {}
    for i in range(n):
        for j in range(i + 1, n):
            happiness[i][j] = G.get_edge_data(i, j)['happiness']
            stress[i][j]    = G.get_edge_data(i, j)['stress']

    answer = best_val
    best_k = -1
    rooms  = {}
    
    #prune
    pruned = {}
    for u in range(n):
        for v in range(u+1, n):
            if stress[u][v] > s_max / k:
                pruned[(u, v)] = stress[u][v] #add pair to pruned
    # print(pruned)
    print("(", end="", flush=True)
    #auto optimize
    val, arr, not_optimal = lp(happiness, stress, s_max, n, k, answer, pruned)
    if val > answer:
        print("*", end="", flush=True)
        answer = val
        rooms  = arr
        best_k = k
    else:
        print("X", end="", flush=True)   
    print(")", end=" ", flush=True)
    return answer, rooms, best_k

if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_path = sys.argv[1]
    output_path = 'medium_outputs/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
    G, s = read_input_file(path)
    orig_val = float(sys.argv[2])
    best_val = orig_val
    D = {}
    if len(sys.argv) == 3: #redo all values k for input
        for i in range(G.order()):
           val, rooms, k = specific(G, best_val, i, s)
           if val > best_val:
               best_val = val
               D = rooms
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        print(happiness, best_val)
        assert round(happiness, 2) == round(best_val, 2)
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)))
        if best_val > orig_val:
            write_output_file(D, output_path)
        else:
            print('Could not improve max happiness')
    elif len(sys.argv) > 3:
        vals = [int(k) for k in sys.argv[3:]]
        for i in vals:
           val, rooms, k = specific(G, best_val, i, s)
           if val > best_val:
               best_val = val
               D = rooms
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        print(happiness, best_val)
        assert round(happiness, 2) == round(best_val, 2)
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)))
        if best_val > orig_val:
            print("Improved max happiness, from", orig_val, "to", best_val)
            write_output_file(D, output_path)
        else:
            print('Could not improve max happiness')
    else:
        print("Syntax Error.")
        exit()