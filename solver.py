import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import glob
import os


import gurobipy as gp
from gurobipy import GRB
import bruteforce

def parse(f):
    """
    Args:
        f: File of inputs
    Returns:
        LP: File of LP constraints and variables 
    """
    # How will we set up the LP constraints?
    file = open(f, 'r')
    for line in file: 
        pass
    return None    

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
    if n <= 10: #brute force approach
        happiness = {}
        stress = {}
        for i in range(n):
            happiness[i] = {}
            stress[i]    = {}

        for i in range(n):
            for j in range(i + 1, n):
                happiness[i][j] = G.get_edge_data(i, j)['happiness']
                stress[i][j]    = G.get_edge_data(i, j)['stress']

        arr = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
        assignments = {}
        
        for i in range(len(arr)):
            for person in arr[i]:
                assignments[person] = i

        print("----------=====Output=====----------")
        print("Number of Nodes:", n)
        print("Number of Edges:", G.size())
        print("Assignments:", assignments)
        
        return assignments, len(arr)
    elif n == 20 or n == 50: #ILP 
        raise NotImplementedError
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
