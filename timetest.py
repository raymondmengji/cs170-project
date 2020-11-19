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
import time


def prettyprint(happiness, stress):
    for key in happiness:
        for val in happiness[key]:
            print(key, val, happiness[key][val], stress[key][val])

n = 10
happiness = {}
stress = {}
for i in range(n):
    happiness[i] = {}
    stress[i]    = {}

slowest_time = float("-inf")
num = 200
for i in range(num):
    #generate graph
    s = round(random.uniform(40, 60), 3)
    for u in range(n):
        happiness[u] = {}
        stress[u] = {}
        for v in range(u + 1, n):
            happiness[u][v] = round(random.uniform(25, 75), 3) #Uniform RV in [25, 75]
            stress[u][v]    = round(random.uniform(0, 30), 3)  

    #ILP Time
    start_time = time.perf_counter()
    answer = 0
    for k in range(1, n + 1):
        val = lp.lp(happiness, stress, s, n, k)
        if val:
            answer = max(answer, val)
    end_time = time.perf_counter()
    gurobi_time = end_time - start_time
    #Bruteforce Time
    start_time = time.perf_counter()
    bf_arr, bf_val = bruteforce.bruteforce(happiness, stress, len(list(happiness.keys())), s)
    end_time = time.perf_counter()
    bf_time = end_time - start_time

    bf_val = round(bf_val, 3)
    answer = round(answer, 3)
    assert bf_val == answer, "Incorrect computation"
    if gurobi_time > slowest_time:
        print(10)
        print(s)
        print(prettyprint(happiness, stress))
        print("-----")
        print("max_happiness:", answer)
        print("gurobi_time:", gurobi_time)
        print("rooms:", bf_arr)
        print("\n\n")
        slowest_time = gurobi_time
    #print("BF_VAL:", bf_val, "GUROBI_VAL:", answer)
    #print("Times:", bf_time, gurobi_time)
    #print("Speed Difference:", bf_time / gurobi_time)
    #print("------------------------------------------\n")