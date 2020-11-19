import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import glob
import os

import gurobipy as gp
from gurobipy import GRB
import bruteforce
import lp
import random

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
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

    ####################Random Graph Generator####################
    if False: # Turn to False to run real files
        s = random.uniform(40, 60)
        for u in range(n):
            happiness[u] = {}
            stress[u] = {}
            for v in range(u + 1, n):
                happiness[u][v] = random.uniform(25, 75) #Uniform RV in [25, 75]
                stress[u][v]    = random.uniform(0, 30)  
    ##############################################################

    if n <= 10: #brute force approach
        bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
        lp_ans = 0
        for k in range(1, n + 1):
            val = lp.lp(happiness, stress, s, n, k)
            if val:
                lp_ans = max(lp_ans, val)
        bf_val = round(bf_val, 3)
        lp_ans = round(lp_ans, 3)
        assert bf_val == lp_ans, "Incorrect computation"
        assignments = {}
        
        for i in range(len(bf_arr)):
            for person in bf_arr[i]:
                assignments[person] = i

        return assignments, len(bf_arr)
    elif n == 20 or n == 50: #ILP 
        answer = 0
        for k in range(1, n + 1):
            val = lp.lp(happiness, stress, s, n, k)
            if val:
                answer = max(answer, val)
        print("Gurobi Answer:", answer)
        arr, val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
        return {}, 0
    else:
        return "Graph sizes that aren't 10, 20, or 50 nodes aren't accepted"


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('samples/inputs/*')
    for input_path in inputs:
        output_path = 'samples/outputs/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)))
        print("\n")
        write_output_file(D, output_path)
