# CS 170 Project Fall 2020

## Instructions

Run `pip install -r requirements.txt` to install all dependencies used.

## Team - Undecided
Julian Meyn, John Le, Raymond Ji 

## Problem Statment
2020 has been a stressful year, and CS 170 course staff is trying to reduce student stress and increase student happiness
as much as possible. Since school has been reduced to a series of awkward Zoom breakout rooms, we figured this is
a good place to start. We noticed that student stress and happiness fluctuate greatly depending on how they are split
into breakout rooms, so we are looking to find a way to divide up stressed 170 students to make them a little happier.
However, this sounds like a really difficult task, so we decided to outsource this to you.

Project Spec: https://cs170.org/assets/pdf/project_spec.pdf

## Approach
We attempted to solve this NP-Hard problem using Mixed Integer Programming. 

## Inputs
We obtained our inputs by randomly generated inputs where the happiesness and stress is determined randomly between [0,5]. 
We ran these inputs through our solver repeatedly and chose the ones that took the longest amount of time. If we did not have
our solver ready, we would have tried to build our inputs from an output that we determine might be hard. 

## Algorithm 
We decided to bruteforce group sizes of 10 because it would lead to the optimal solution in a very quick time. 
We then reduced the problem to a linear programming problem to use the powerful freely available optimizers online.
However, we do brute force some break room sizes for group sizes of 20 and 50 because they have less than a million permutations.
We believe this is a good approach because the optimizers online are able to solve our linear program quickly

We tried to the reduce the problem to graph partitioning and found a software called METIS that we attempted to use. 
Nonetheless, we decided the LP route was a better option. 

## LP/MIP Solver
We used the Gurobi optimizer, which is freely available for students. 

## LP/MIP Construction
We created our LP based on the conditions seen in the constraints.pdf file.

## Computational Resources
We generated a Google Cloud Computer Engine using the free credits available to any student. 
We also used one instructional machine.

## What would we do different with more time?
We definitely try to come up with a better approximation algorithm for group sizes of 50. Some of their
computations took long amounts of time.  

## Files
solver.py  - Runs all files in samples/inputs and prints the highest valid Total Happiness of each graph

timeall.py - Same as solver.py, but also prints diagnostic data about speed and room distributions for each file

timetest.py (n) (k=10) - Randomly generates k graphs (default 10) with n nodes and prints diagnostic data about its performance. 
Useful to test/generate hard inputs

## Resources Used
https://arxiv.org/pdf/1802.07144.pdf

https://www.gurobi.com/

https://www.gurobi.com/documentation/9.1/refman/py_python_api_overview.html

https://codereview.stackexchange.com/questions/1526/

https://cs.stackexchange.com/questions/12102/express-boolean-logic-operations-in-zero-one-integer-linear-programming-ilp
