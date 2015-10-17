import networkx as nx
import random
from base_player import BasePlayer
from settings import *
import sys

class Player(BasePlayer):
    """
    You will implement this class for the competition. DO NOT change the class
    name or the base class.
    """

    # You can set up static state here
    has_built_station = False
    num_stations_built = 0

    def __init__(self, state):
        """
        Initializes your Player. You can set up persistent state, do analysis
        on the input graph, engage in whatever pre-computation you need. This
        function must take less than Settings.INIT_TIMEOUT seconds.
        --- Parameters ---
        state : State
            The initial state of the game. See state.py for more information.
        """

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

        commands = []
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
