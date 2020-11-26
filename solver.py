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

    #read graph from G
    happiness = {}
    stress = {}
    for i in range(n):
        happiness[i] = {}
        stress[i]    = {}
    for i in range(n):
        for j in range(i + 1, n):
            happiness[i][j] = G.get_edge_data(i, j)['happiness']
            stress[i][j]    = G.get_edge_data(i, j)['stress']

    if n <= 10:
        bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
        bf_val = bf_val
        assignments = {}
        for i in range(len(bf_arr)):
            for person in bf_arr[i]:
                assignments[person] = i
        return assignments, len(bf_arr), bf_val
    elif n == 20 or n == 50:
        answer, rooms, best_k = lp.lp_solve(happiness, stress, s, n)
        return rooms, best_k, answer
    else:
        return "Graph sizes that aren't <=10, 20, or 50 nodes aren't accepted"


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
    inputs = glob.glob('medium/*')
    inputs.sort()
    num_inputs = len(inputs)
    i = 40
    for input_path in inputs[40:80]:
        print("Filename:", input_path, "Input", i, "out of", str(num_inputs) + "...")
        i += 1
        output_path = 'medium_outputs/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path, 100)
        D, k, val = solve(G, s)
        happiness = calculate_happiness(D, G)
        assert round(happiness, 3) == round(val, 3)
        assert is_valid_solution(D, G, s, k)
        print("Total Happiness: {}".format(calculate_happiness(D, G)))
        print()

        write_output_file(D, output_path)
