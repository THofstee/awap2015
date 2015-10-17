import networkx as nx
import random
from base_player import BasePlayer
from settings import *
from copy import deepcopy
import sys

class Player(BasePlayer):
    """
    You will implement this class for the competition. DO NOT change the class
    name or the base class.
    """

    # You can set up static state here
    hub_score = None
    edge_count = None
    centeredness = []
    lastid = -1
    gamest=0 #0 for early, 1 for mid, 2 for late

    early_pct=0.05
    all_nodes_scalar=0.1

    station=-1

    stations=[]
    station=-1

    def hub_f(self,n):
        return max(0,SCORE_MEAN-n*DECAY_FACTOR)

    def hub_init(self,state): 
        self.hub_score = [0]*GRAPH_SIZE
        G=state.get_graph()
        self.edge_count = [len(nx.edges(G,[i])) for i in xrange(GRAPH_SIZE)]
        shortest=nx.shortest_path_length(G)
        for i in xrange(GRAPH_SIZE):
            center=0.0
            for j in xrange(GRAPH_SIZE):
                center+=self.hub_f(shortest[i][j])*self.all_nodes_scalar
            self.centeredness.append(center)

    def hub_update(self, state):
        orders=state.get_pending_orders()
        curri=0
        G=state.get_graph()
        for i in xrange(len(orders)):
            if orders[i].id>orders[curri].id:
                curri=i
        if orders[curri].id>self.lastid: 
            #then we have a new order
            shortest=nx.shortest_path_length(G,orders[curri].node)
            for i in xrange(GRAPH_SIZE):
                self.centeredness[i]+=self.hub_f(shortest[i])
                
    def expected_end(self, state):
        
        return
    
    def mid_best(self, state):
        c_out = 1
        c_ev = 1
        G = state.get_graph()
        max_v = 0
        max_n = -1
        paths = nx.shortest_path_length(G)
        for i in xrange(GRAPH_SIZE):
            min_d = paths[stations[0]][i]
            for j in xrange(len(stations)):
                min_d = min(min_d,paths[stations[j]][i])
            cur_v = 0.0
            cur_v -= (c_ev*self.centerdness[i]*self.centerdness[i]+c_out*G.degree(i))/(min_d+1)
            cur_v += c_out*G.degree(i)*ORDER_CHANCE
            cur_v += c_ev*self.centerdness[i]*self.centerdness[i]/(ORDER_VAR*ORDER_VAR+1)
            if (cur_v > max_v):
                max_v = cur_v
                max_n = id
        return max_n

    def __init__(self, state):
        """
        Initializes your Player. You can set up persistent state, do analysis
        on the input graph, engage in whatever pre-computation you need. This
        function must take less than Settings.INIT_TIMEOUT seconds.
        --- Parameters ---
        state : State
            The initial state of the game. See state.py for more information.
        """

        self.hub_init(state)

        return

    # Checks if we can use a given path
    def path_is_valid(self, state, path):
        graph = state.get_graph()
        for i in range(0, len(path) - 1):
            if graph.edge[path[i]][path[i + 1]]['in_use']:
                return False
        return True

    # Converts a list of nodes into a list of edge pairs
    # e.g. [0, 1, 2] -> [(0, 1), (1, 2)]
    def path_to_edges(self, path):
        return [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]

    def getOrders(self, state, commands):
        graph = state.get_graph()
        pending_orders = state.get_pending_orders()

        for station in self.stations:
            max_income = 0
            min_path = None
            min_order = None
            for order in pending_orders:
                cur_length = nx.shortest_path_length(graph, station, order.get_node())
                # if cur_length < min_length:
                #     min_length = cur_length
                #     min_path = nx.shortest_path(graph, station, order.get_node())
                #     min_order = order
                if order.get_money()-cur_length*DECAY_FACTOR>max_income:
                    max_income=order.get_money()-cur_length*DECAY_FACTOR
                    min_path = nx.shortest_path(graph, station, order.get_node())
                    min_order = order
            if self.path_is_valid(state, min_path):
                commands.append(self.send_command(min_order, min_path))
                pending_orders.remove(min_order)
                path_edges = self.path_to_edges(min_path)
                for edge in path_edges:
                    graph.remove_edge(*edge)

        return commands

    def step(self, state):
        """
        Determine actions based on the current state of the city. Called every
        time step. This function must take less than Settings.STEP_TIMEOUT
        seconds.
        --- Parameters ---
        state : State
            The state of the game. See state.py for more information.
        --- Returns ---
        commands : dict list
            Each command should be generated via self.send_command or
            self.build_command. The commands are evaluated in order.
        """

        # We have implemented a naive bot for you that builds a single station
        # and tries to find the shortest path from it to first pending order.
        # We recommend making it a bit smarter ;-)

        graph = state.get_graph()

        self.hub_update(state)

        commands=[]
        station = self.station

        commands_sent = 0
        pending_orders = state.get_pending_orders()

        if self.gamest==0:
            if state.get_time()>self.early_pct*GAME_LENGTH*ORDER_CHANCE/len(pending_orders):
                besti=0
                for i in xrange(GRAPH_SIZE):
                    if self.centeredness[i]*self.edge_count[i]>self.centeredness[besti]*self.edge_count[besti]:
                        besti=i
                commands.append(self.build_command(besti))
                self.stations.append(besti)
                self.station=besti
                self.gamest=1


        # if len(pending_orders) != 0 and self.station>=0:
        #     min_length = sys.maxint
        #     min_path = None
        #     min_order = None
        #     for order in pending_orders:
        #         cur_length = nx.shortest_path_length(graph, self.station, order.get_node())
        #         if cur_length < min_length:
        #             min_length = cur_length
        #             min_path = nx.shortest_path(graph, self.station, order.get_node())
        #             min_order = order
        #     if self.path_is_valid(state, min_path):
        #         commands.append(self.send_command(min_order, min_path))
        
        commands = self.getOrders(state,commands)

        return commands
