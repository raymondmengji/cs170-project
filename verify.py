import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, order, prettyprint
import sys
import glob
import os
import gurobipy as gp
from gurobipy import GRB
import bruteforce
import lp
import random

"""
    verify.py

    looks into output folder and uses it as a cutoff value for the input value
    useful to check if the output graph really is the optimal solution
"""


#read output file, get happiness
#run lp with initial cutoff as CUTOFF
#write to output file if found new cutoff
#print verification if no new value found

def verify(G, s, cutoff):
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
        answer, rooms, best_k = lp_cutoff(happiness, stress, s, n, cutoff)
        return rooms, best_k, answer
    else:
        return "Graph sizes that aren't <=10, 20, or 50 nodes aren't accepted"


def lp_cutoff(happiness, stress, s_max, n, cutoff):
    answer = cutoff
    best_k = -1
    rooms  = {}

    #if n = 20, brute force 1,2,17,18,19
    #if n = 50, brute force 1,48,49
    #if n <= 10, don't brute force anything (for testing purposes)
    #always brute force k = 1, n
    bruteforce_nums = []
    suboptimal = []
    if n == 20:
        bruteforce_nums = [1,2,17,18,19]
    elif n == 50:
        bruteforce_nums = [1,48,49]
    
    nonbruteforce_nums = [i for i in range(1, n) if i not in bruteforce_nums]
    print("Bruteforce...", end=" ", flush=True)
    for k in bruteforce_nums:
        val, arr = bruteforce.bruteforce_k(happiness, stress, n, s_max, k)
        if val > answer:
            print("*", end="", flush=True)
            answer = val
            rooms = arr
            best_k = k
        print("", end=" ", flush=True)
    print()
    print("Gurobi...", end=" ", flush=True)
    for k in nonbruteforce_nums:
        #prune
        pruned = {}
        for u in range(n):
            for v in range(u+1, n):
                if stress[u][v] > s_max / k:
                    pruned[(u, v)] = stress[u][v] #add pair to pruned
        print("(", end="", flush=True)
        val, arr, not_optimal = lp.lp(happiness, stress, s_max, n, k, answer, pruned)
        if not_optimal:
            suboptimal.append(k)
        if val > answer:
            #print(val, arr)
            print("*", end="", flush=True)
            answer = val
            rooms  = arr
            best_k = k   
        print(")", end=" ", flush=True)
    print()
    print("SUBOPTIMAL K:", suboptimal)
    return answer, rooms, best_k

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    #skip these (already optimal)
    blacklist = [48, 75, 216, 173, 190, 239, 153, 149, 142, 160, 37, 32, 241, 238, 232, 231, 223, 221, 210, 199, 198, 192, 170, 150, 144, 82, 72, 30, 29, 17, 40, 179]

    inputs = glob.glob('medium/*')
    outputs = glob.glob('medium_outputs/*')
    inputs.sort()
    outputs.sort()
    tle = []
    redo = []
    num_inputs = len(inputs)
    for input_path in inputs:
        print("Filename:", input_path, "Input", i, "out of", str(num_inputs) + "...")
        i += 1
        output_path_num = int(os.path.basename(os.path.normpath(input_path))[:-3].split("-")[1])
        if output_path_num in blacklist:
            print("Skipping Blacklist Num...")
            continue
        
        G, s = read_input_file(input_path, 100)
        output_path = 'medium_outputs/' + os.path.basename(os.path.normpath(input_path))[:-3] + '.out'
        D = read_output_file(output_path, G, s)
        output_happiness = calculate_happiness(D, G)
        print("Current Happiness:", output_happiness)

        D_new, k_new, val_new = verify(G, s, output_happiness)
        print("Returned Happiness", val_new)
        if D_new and round(val_new, 3) > round(output_happiness, 3):
            new_happiness = calculate_happiness(D_new, G)
            print(new_happiness, val_new)
            assert round(new_happiness, 2) == round(val_new, 2)
            assert is_valid_solution(D_new, G, s, k_new)
            print("New Happiness Found:", new_happiness)
            print()
            write_output_file(D_new, output_path)
            redo.append(input_path)
        else:
            print("Could not improve happiness (already optimal)")
        print()
    print("Inputs Improved:", redo)
    print("TLE", tle)
