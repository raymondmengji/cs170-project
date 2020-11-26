import gurobipy as gp
from gurobipy import GRB
import bruteforce

def lp_solve(happiness, stress, s_max, n, optimize=True):
    answer = 0 
    best_k = n
    rooms  = {i: i for i in range(n)}

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
        #print("value found", round(val, 3))
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
        # print(pruned)
        print("(", end="", flush=True)
        val, arr, not_optimal = lp(happiness, stress, s_max, n, k, answer, pruned, optimize_parameters=optimize)
        #print("value found", round(val, 3))
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
        
def lp(happiness, stress, s_max, n, room_num, cutoff, pruned, return_rooms=True, optimize_parameters=True):
    try:
        #model
        m = gp.Model("MIP")
        m.setParam("OutputFlag", 0)
        if optimize_parameters:
            m.setParam("Method", 1)
            m.setParam("FeasibilityTol", 1e-4)
            m.setParam("IntFeasTol", 1e-4)
            #m.setParam("Heuristics", 0)
            m.setParam("Cutoff", cutoff)
            m.setParam("Quad", 0)
            #m.setParam("Presolve", 2)
            #m.setParam("TuneCriterion", 0)
            #m.setParam("SolutionLimit", 1) #bad for some reason
            #m.setParam("MIPGapAbs", 0.1)
            m.setParam("DisplayInterval", 20)
            #m.setParam("Cuts", 0)
            m.setParam("TimeLimit", 300)
            #m.setParam("MIPGap", 1)
            #m.setParam("BarConvTol", 1e-3)
            #m.setParam("NodeMethod", 2)
            #m.setParam("Symmetry", 2)
            #m.setParam("Disconnected", 0)
            #m.setParam("SolutionNumber", 0)
            #m.setParam("Presolve", 1)
            #m.setParam("MIPFocus", 2)
        #m.setParam("OutputFlag", 1)
        constraintCounter = 0
        varCounter = 0

        # variables

        # students
        g = {}
        for k in range(room_num):
            g[k] = {}
            for v in range(n):
                g[k][v] = m.addVar(vtype=GRB.BINARY, name="g_" + str(v) + "," + str(k))

        # edges
        e = {}
        for u in range(n):
            e[u] = {}
            for v in range(u+1, n):
                if (u, v) in pruned:
                    e[u][v] = 0
                    continue
                e[u][v] = m.addVar(vtype=GRB.BINARY, name="e_" + str(u) + "," + str(v))
        
        temp_edge_indicators = {}
        for i in range(room_num):
            temp_edge_indicators[i] = {}

        for k in range(room_num):
            for u in range(n):
                temp_edge_indicators[k][u] = {}
                for v in range(u+1, n):
                    # if (u, v) in pruned:
                    #     temp_edge_indicators[k][u][v] = m.addVar(vtype=GRB.BINARY, name="e_" + str(k) + "-" + str(u) + "," + str(v))
                    #     temp = temp_edge_indicators[k][u][v]
                    #     m.addConstr(temp >= 0, "c" + str(constraintCounter))
                    #     constraintCounter += 1
                    #     m.addConstr(temp <= 0, "c" + str(constraintCounter))
                    #     constraintCounter += 1
                    #     continue
                    temp_edge_indicators[k][u][v] = m.addVar(vtype=GRB.BINARY, name="e_" + str(k) + "-" + str(u) + "," + str(v))
                    temp = temp_edge_indicators[k][u][v]
                    u_room_indicator = g[k][u]
                    v_room_indicator = g[k][v]
                    m.addConstr(temp >= u_room_indicator + v_room_indicator - 1, "c" + str(constraintCounter))
                    constraintCounter += 1
                    m.addConstr(temp <= u_room_indicator, "c" + str(constraintCounter))
                    constraintCounter += 1
                    m.addConstr(temp <= v_room_indicator, "c" + str(constraintCounter))
                    constraintCounter += 1
                    m.addConstr(temp >= 0, "c" + str(constraintCounter))
                    constraintCounter += 1
                    m.addConstr(temp <= 1, "c" + str(constraintCounter))
                    constraintCounter += 1

        for u in range(n):
            for v in range(u+1, n):
                # if (u, v) in pruned:
                #     continue
                indicators = []
                for k in range(room_num):
                    indicators.append(temp_edge_indicators[k][u][v])
                    m.addConstr(e[u][v] >= temp_edge_indicators[k][u][v], "c" + str(constraintCounter))
                    constraintCounter += 1
                m.addConstr(e[u][v] <= gp.quicksum(indicators))
                m.addConstr(e[u][v] >= 0, "c" + str(constraintCounter))
                constraintCounter += 1
                m.addConstr(e[u][v] <= 1, "c" + str(constraintCounter))
                constraintCounter += 1
        


        # h = {}
        # for u in happiness.keys():
        #     h[u] = {}
        #     for v in happiness[u].keys():
        #         h[u][v] = m.addVar(vtype=GRB.CONTINUOUS, name="h_" + str(u) + "," + str(v))
        #         m.addConstr(h[u][v] <= happiness[u][v], "c"+str(constraintCounter))
        #         constraintCounter += 1
        #         m.addConstr(h[u][v] >= happiness[u][v], "c"+str(constraintCounter))
        #         constraintCounter += 1
        
        # s = {}
        # for u in stress.keys():
        #     s[u] = {}
        #     for v in stress[u].keys():
        #         s[u][v] = m.addVar(vtype=GRB.CONTINUOUS, name="s_" + str(u) + "," + str(v))
        #         m.addConstr(s[u][v] <= stress[u][v], "c"+str(constraintCounter))
        #         constraintCounter += 1
        #         m.addConstr(s[u][v] >= stress[u][v], "c"+str(constraintCounter))
        #         constraintCounter += 1
        

        for v in range(n):
            room_arr = []
            for k in range(room_num):
                room_arr.append(g[k][v])
            m.addConstr(gp.quicksum(room_arr) >= 1, "c" + str(constraintCounter))
            constraintCounter += 1
            m.addConstr(gp.quicksum(room_arr) <= 1, "c" + str(constraintCounter))
            constraintCounter += 1

        # for k in g.keys():
        #     room_arr = []
        #     room = g[k]

        #     for u in range(n):
        #         for v in range(u+1, n):

        #             # want: u_room_indicator * v_room_indicator * edge_indicator * constant

        #             u_room_indicator = room[u]
        #             v_room_indicator = room[v]

        #             temp_u_room_indicator = m.addVar(vtype=GRB.BINARY, name="temp_"+str(varCounter)))
        #             varCounter += 1
        #             temp_v_room_indicator = m.addVar(vtype=GRB.BINARY, name="temp_"+str(varCounter))

        #             m.addConstr(u_room_indicator <= temp_u_room_indicator, "c" + str(constraintCounter))
        #             constraintCounter += 1
        #             m.addConstr(v_room_indicator <= temp_v_room_indicator, "c" + str(constraintCounter))
        #             constraintCounter += 1
        #             m.addConstr(temp_u_room_indicator+temp_v_room_indicator <= 2, "c" + str(constraintCounter))
                    

        #             edge_indicator = e[u][v]
        #             stressAmount = s[u][v]

        for k in range(room_num):
            room_arr = []
            for u in range(n):
                for v in range(u+1, n):
                    # if (u, v) in pruned:
                    #     continue
                    room_arr.append(stress[u][v]*temp_edge_indicators[k][u][v])
            m.addConstr(gp.quicksum(room_arr) <= s_max/room_num, "c"+str(constraintCounter))
            constraintCounter += 1


            # for u in list(room.keys()):
            #     room_indicator = room[u]
            #     edges_from_u = e[u]
            #     for v in edges_from_u.keys():
            #         edge_indicator = edges_from_u[v]
            #         stressAmount = s[u][v]
            #         room_arr.append(room_indicator*edge_indicator*stressAmount)
            # m.addConstr(sum(room_arr) <= s_max/room_num, "c"+str(constraintCounter))
            # constraintCounter += 1

        arr = []
        for u in e.keys():
            for v in e[u].keys():
                if (u, v) in pruned:
                    continue
                arr.append(e[u][v] * happiness[u][v])
        m.setObjective(gp.quicksum(arr), GRB.MAXIMIZE)

        #if (n == 20 and room_num == 3) \
        #    or (n == 50 and room_num == 2) \
        #    or (n <= 10 and room_num == 1):
        #    print("Gurobi...", end=" ", flush=True)
        
        print(room_num, end=",", flush=True)
        
        # print(m.printStats())
        status = m.optimize()
        #print("Presolve Done", flush=True)
        if GRB.OPTIMAL == m.status:
            print("O", end="", flush=True)
            #the variables are in m.getVars()
            all_vars = m.getVars()
            desired_vars = []
            for v in all_vars:
                if v.varName[0] == 'g' and int(round(v.x, 2)) == 1:
                    desired_vars.append(v.varName)
            #print(desired_vars)
            ans = {}
            for v in desired_vars:
                x = v.split('_', 1)[1].split(",")
                ans[int(x[0])] = int(x[1])
            #print(ans)
            if return_rooms:
                return m.objVal, ans, False
            return m.objVal, [], False
        elif m.status == GRB.SUBOPTIMAL: 
            print("S", end="", flush=True)
        elif m.status == GRB.CUTOFF:
            print("C", end="", flush=True)
            return 0, [], False
        elif GRB.TIME_LIMIT == m.status:
            print("T", m.objVal, end="", flush=True)
            return m.objVal, [], True
        else:
            print("I", end="", flush=True)
            return 0, [], False
        #the variables are in m.getVars()
        all_vars = m.getVars()
        desired_vars = []
        for v in all_vars:
            if v.varName[0] == 'g' and int(round(v.x, 2)) == 1:
                desired_vars.append(v.varName)
        #print(desired_vars)
        ans = {}
        for v in desired_vars:
            x = v.split('_', 1)[1].split(",")
            ans[int(x[0])] = int(x[1])
        #print()
        if return_rooms:
            return m.objVal, ans, True
        return m.objVal, [], True
    except gp.GurobiError as e:
        print("E!", end="", flush=True)
        #print("Error Code " + str(e.errno) + ": " + str(e))
        return 0, [], False
    except AttributeError:
        print("E", end="", flush=True)
        #print("Encountered an attribute error")
        return 0, [], False
