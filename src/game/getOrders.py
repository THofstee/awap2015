# Converts a list of nodes into a list of edge pairs
# e.g. [0, 1, 2] -> [(0, 1), (1, 2)]
def path_to_edges(self, path):
    return [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]

def getOrders(self, state):
    graph = state.get_graph()
    pending_orders = state.get_pending_orders()

    commands = []

    for station in self.stations:
        min_len = sys.maxint
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
            pending_orders.remove(min_order)
            path_edges = path_to_edges(min_path)
            for edge in path_edges
                graph.remove_edge(*edge)

    return commands