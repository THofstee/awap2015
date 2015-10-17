import networkx as nx
from settings import *

def detOrder(self, state, Stations):
	G = state.get_graph()

	for edge in G.edges_iter():
		if(edge['in_use']):
			n1 = edge[0]
			n2 = edge[1]
			G.remove_edge(n1,n2)

	listOrders = []

	for st in Stations:
		pending_orders = state.get_pending_orders()
		while (len(pending_orders) != 0):
			incomeDict = {}
	        for order in pending_orders:
	        	node = order.get_node()
	        	money = get_money(order)
	        	time_created = get_time_created(order)
	        	try:
		         	cur_length = nx.shortest_path_length(G, st, node)
		            max_Income = money - (self.get_time() - time_created + cur_length) * \
		            DECAY_FACTOR
		            incomeDict[max_Income] = order;
		     	except NetworkXError:
		     		continue
		     		# no possible paths
		    if(incomeDict.len() == 0):
		    	break
			incomeList = incomeDict.keys()
			sort(incomeList)
			bestOrder = incomeDict[incomeList.pop()]
			path = nx.shortest_path(G, st, bestOrder.node())
			listOrders.append((bestOrder,path))
			for (u, v) in self.path_to_edges(path):
                G.remove_edge(u,v)
                G.remove_edge(v,u)
            pending_orders.remove(bestOrder)

    return listOrders