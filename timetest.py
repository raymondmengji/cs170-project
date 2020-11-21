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
import time
import numpy as np

"""
    timetest.py

    Randomly generates graphs of size ARGV[1], ARGV[2] times
    and prints out the stats of the graphs that took the longest amount of time
"""

def timeTest(n, num_repetitions=10):
    '''
        timeTest(n, num_repetitions)

        Runs NUM_REPETITIONS trials of our ILP solver on a randomly
        generated graph with N nodes. If N <= 10, the bruteforce
        method will also be called to verify optimality, though
        this can be changed by changing respective cases.
    '''
    happiness = {}
    stress = {}
    for i in range(n):
        happiness[i] = {}
        stress[i]    = {}

    average_diff = []
    error = []
    slowest_time = float("-inf")
    for i in range(num_repetitions):
        #generate graph
        s = round(random.uniform(90, 100), 3)
        #generate a random interval each time
        lower = 10#random.randrange(1, 10)
        upper = 20#random.randrange(10, 20)
        for u in range(n):
            happiness[u] = {}
            stress[u] = {}
            for v in range(u + 1, n):
                happiness[u][v] = round(random.uniform(10, 15), 3)  #URV [1, 5] is best
                #force everyone in their own groups by setting stress[u][v] to 101
                stress[u][v]    = round(random.uniform(5, 15), 3) #URV [1, 5] is best

        #ILP Time, optimized
        start_time = time.perf_counter()
        answer, groups, group_size = lp.lp_solve(happiness, stress, s, n)
        end_time = time.perf_counter()
        gurobi_time = end_time - start_time

        #ILP Time, unoptimized
        enable_unoptimized_ILP = False
        if enable_unoptimized_ILP:
            start_time = time.perf_counter()
            answer2, groups2, group_size2 = lp.lp_solve(happiness, stress, s, n, False)
            end_time = time.perf_counter()
            gurobi_time2 = end_time - start_time

        #Bruteforce Time
        if n <= 10:
            bf_arr = []
            start_time = time.perf_counter()
            bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
            end_time = time.perf_counter()
            bf_time = end_time - start_time
        
        if True or gurobi_time > slowest_time:
            print(n)
            print(s)
            print(prettyprint(happiness, stress))
            print("-------Stats-------")
            print("optimize happiness:", answer)
            if enable_unoptimized_ILP:
                print("normal   happiness:", answer2)
            if n <= 10:
                print("brutef   happiness:", bf_val)
            print("optimize groups:", order(groups)[0])
            if enable_unoptimized_ILP:
                print("normal   groups:", order(groups2)[0])
            if n <= 10:
                #assert round(bf_val, 3) == round(answer, 3), "Incorrect computation"
                print("brutef   groupings:", bf_arr)
            print("optimize time:", gurobi_time)
            if enable_unoptimized_ILP:
                print("normal   time:", gurobi_time2)
            if n <= 10:
                print("brutef   time:", bf_time)
            if enable_unoptimized_ILP:
                #Error between optimal and actual 
                error.append(round((answer - answer2) / ((answer + answer2) / 2) * 100, 3))
                #Percentage difference between optimized and normal speeds
                speedup = round(((gurobi_time2 - gurobi_time) / ((gurobi_time + gurobi_time2)/2)) * 100, 2)
                average_diff.append(speedup)
                print("Difference:", speedup, "%")
            print("\n\n")
            slowest_time = max(gurobi_time, slowest_time)
    if enable_unoptimized_ILP:
        print(error)
        print(average_diff)
        print("Average Error:    ", np.average(error))
        print("Variance of Error:", np.var(error))
        print("Average Difference:          ", np.average(average_diff))
        print("Variance of Speed Difference:", np.var(average_diff))
    print("Slowest Time:", slowest_time)

if __name__ == "__main__":
    assert len(sys.argv) >= 2, \
        "Must have at least two arguments (run python3 timetest.py #nodes (#repetitions))"
    if len(sys.argv) == 3:
        timeTest(int(sys.argv[1]), int(sys.argv[2]))
    else:
        timeTest(int(sys.argv[1]))