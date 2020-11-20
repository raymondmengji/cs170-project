import gurobipy as gp
from gurobipy import GRB

        
def lp(happiness, stress, s_max, n, room_num, return_rooms=True, alternate_parameters=True):
    print("curr:", room_num)
    try:
        #model
        m = gp.Model("mip1")
        m.setParam("OutputFlag", 0)
        if alternate_parameters:
            m.setParam("Method", 3)
            m.setParam("FeasibilityTol", 1e-3)
            m.setParam("IntFeasTol", 1e-3)
            m.setParam("Heuristics", 0.01)
            m.setParam("MIPGapAbs", 0.5)
            m.setParam("MIPGap", 0.5)
            m.setParam("NodeMethod", 0)
        #m.setParam("Symmetry", 2)
        #m.setParam("Disconnected", 0)
        #m.setParam("MIPFocus", 2)
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
                e[u][v] = m.addVar(vtype=GRB.BINARY, name="e_" + str(u) + "," + str(v))
        
        temp_edge_indicators = {}
        for i in range(room_num):
            temp_edge_indicators[i] = {}

        for k in range(room_num):
            for u in range(n):
                temp_edge_indicators[k][u] = {}
                for v in range(u+1, n):
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
                indicators = []
                for k in range(room_num):
                    indicators.append(temp_edge_indicators[k][u][v])
                    m.addConstr(e[u][v] >= temp_edge_indicators[k][u][v], "c" + str(constraintCounter))
                    constraintCounter += 1
                m.addConstr(e[u][v] <= sum(indicators))
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
            m.addConstr(sum(room_arr) >= 1, "c" + str(constraintCounter))
            constraintCounter += 1
            m.addConstr(sum(room_arr) <= 1, "c" + str(constraintCounter))
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
                    room_arr.append(stress[u][v]*temp_edge_indicators[k][u][v])
            m.addConstr(sum(room_arr) <= s_max/room_num, "c"+str(constraintCounter))
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
                arr.append(e[u][v] * happiness[u][v])
        m.setObjective(sum(arr), GRB.MAXIMIZE)

        m.optimize()
        #the variables are in m.getVars()
        if return_rooms:
            all_vars = m.getVars()
            desired_vars = []
            for v in all_vars:
                if v.varName[0] == 'g' and int(v.x) == 1:
                    desired_vars.append(v.varName)
            ans = {}
            for v in desired_vars:
                x = v.split('_', 1)[1].split(",")
                ans[int(x[0])] = int(x[1])
            return m.objVal, ans
        return m.objVal, []
    except gp.GurobiError as e:
        #print("Error Code " + str(e.errno) + ": " + str(e))
        return None, None
    except AttributeError:
        #print("Encountered an attribute error")
        return None, None