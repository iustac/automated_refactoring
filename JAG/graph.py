from collections import defaultdict
import networkx as nx

class Graph:
  
	def __init__(self,vertices):
		self.V= vertices 
		self.graph = defaultdict(list) 
		self.Time = 0
  
	def addEdge(self,u,v):
		self.graph[u].append(v)
		self.graph[v].append(u)

	def APUtil(self,u, visited, ap, parent, low, disc):
		children =0
		visited[u]= True
		disc[u] = self.Time
		low[u] = self.Time
		self.Time += 1
		for v in self.graph[u]:
			if visited[v] == False :
				parent[v] = u
				children += 1
				self.APUtil(v, visited, ap, parent, low, disc)
				low[u] = min(low[u], low[v])
				if parent[u] == -1 and children > 1:
					ap[u] = True
				if parent[u] != -1 and low[v] >= disc[u]:
					ap[u] = True    
			elif v != parent[u]: 
				low[u] = min(low[u], disc[v])

	def AP(self):
		my_list=[]
		visited = [False] * (self.V)
		disc = [float("Inf")] * (self.V)
		low = [float("Inf")] * (self.V)
		parent = [-1] * (self.V)
		ap = [False] * (self.V) 
		for i in range(self.V):
			if visited[i] == False:
				self.APUtil(i, visited, ap, parent, low, disc)
 
		for index, value in enumerate (ap):
			if value == True: my_list.append(index)
		return my_list


def get_critical(relation,classList):
	#create Graph
	graph = Graph(len(classList))
	for i in relation:
		graph.addEdge(i[3],i[4])
	#Articulate points
	return graph.AP()
	
def get_graphAttributes(relation,classList):
	#create Graph
	max_value=0
	for i in relation:
		if i[7]>max_value:
			max_value=i[7]
	G = nx.DiGraph()
	for i in relation:
		G.add_edge(i[3],i[4],weight=(i[7]/float(max_value)))
		
		
	#calculate degree, betweenness and closeness-centrality
	
	#i=0
	#atr=[]
	#for item in classList:
	#	atr.append([])
	#	atr[i].append(item[2])
	#	atr[i].append(item[0])
	#	atr[i].append(item[1])
	#	if G.has_node(item[2]):
	#		atr[i].append(nx.degree_centrality(G)[i])
	#		atr[i].append(nx.in_degree_centrality(G)[i])
	#		atr[i].append(nx.out_degree_centrality(G)[i])
	#		atr[i].append(nx.betweenness_centrality(G)[i])
	#		atr[i].append(nx.load_centrality(G)[i])
	#		atr[i].append(nx.closeness_centrality(G)[i])
	#	else:
	#		atr[i].append(0)
	#		atr[i].append(0)
	#		atr[i].append(0)
	#		atr[i].append(0)
	#		atr[i].append(0)
	#		atr[i].append(0)
	#	i=i+1
	#i=0
	#rel=[]
	#for item in relation:
		#rel.append([])
		#rel[i].append(item[0])
		#rel[i].append(item[1])
		#rel[i].append(item[2])
		#rel[i].append(item[3])
		#rel[i].append(item[4])
		#rel[i].append(nx.edge_betweenness_centrality(G).items()[i])
		#i=i+1
	return G
	
