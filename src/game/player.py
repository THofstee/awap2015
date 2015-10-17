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
    has_built_station = False
    hub_score = None
    edge_count = None
    centeredness = []
    lastid = -1
    gamest=0 #0 for early, 1 for mid, 2 for late
    early_pct=0.05
    early_thresh=

    stations=[]

    def hub_f(self,n):
        return 1.0/(n+1)

    def hub_init(self,state): 
        self.hub_score = [0]*GRAPH_SIZE
        G=state.get_graph()
        self.edge_count = [len(nx.edges(G,[i])) for i in xrange(GRAPH_SIZE)]
        shortest=nx.shortest_path_length(G)
        for i in xrange(GRAPH_SIZE):
            center=0
            for j in xrange(GRAPH_SIZE):
                center+=max(0,SCORE_MEAN-shortest[i][j]*DECAY_FACTOR)
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
                self.hub_score[i]+=self.hub_f(shortest[i])

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
        station = graph.nodes()[0]

        self.hub_update(state)
        if not self.has_built_station:
            commands.append(self.build_command(station))
            self.has_built_station = True
            self.num_stations_built += 1

        commands_sent = 0
        pending_orders = state.get_pending_orders()

        if len(pending_orders) != 0:
            min_length = sys.maxint
            min_path = None
            min_order = None
            for order in pending_orders:
                cur_length = nx.shortest_path_length(graph, station, order.get_node())
                if cur_length < min_length:
                    min_length = cur_length
                    min_path = nx.shortest_path(graph, station, order.get_node())
                    min_order = order
            if self.path_is_valid(state, min_path):
                commands.append(self.send_command(min_order, min_path))
                
        return commands
