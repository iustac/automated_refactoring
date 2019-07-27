import networkx as nx
def get_output(classList,relation,critical,G,ent):
	#creating output file:
	f=open("output.txt",'w')
	i=0
	f.write("Number"+" "+"ID"+" "+"Name"+" "+"Degree-C."+" "+"In-Degree-C."+" "+"Out-Degree-C"+" "+"Betweeness-C."+" "+"Load-C."+" "+"Closeness-C."+" "+"IsCritical"+" "+"Entropy"+" "+"\n")
	for item in classList:
		if G.has_node(i):
			f.write(str(item[2])+ " "+str(item[0])+" "+str(item[1])+" "+str(nx.degree_centrality(G)[i])+" "+str(nx.in_degree_centrality(G)[i])+" "+str(nx.out_degree_centrality(G)[i])+" "+str(nx.betweenness_centrality(G,weight='weight')[i])+" "+str(nx.load_centrality(G,weight='weight')[i])+" "+ str(nx.closeness_centrality(G)[i]))
		if G.has_node(i)==False:
			f.write(str(item[2])+ " "+str(item[0])+" "+str(item[1])+" "+str(0)+" "+str(0)+" "+str(0)+" "+str(0)+" "+str(0)+" "+ str(0))
		if item[2] in critical:
			f.write(" "+"***")
		else:
			f.write(" "+"not")
		# f.write(" "+str(ent[i][1]))
		f.write("\n"+"\n")
		i=i+1
	# i=0
	# f.write("Relation"+" "+"ID-edge1"+" "+"ID-edge2"+" "+"Nr. Edge1"+" "+"Nr.Edge2"+"\n")
	# for item in relation:
	# 	f.write(str(item[0])+" "+str(item[1])+" "+str(item[2])+" "+str(item[3])+" "+ str(item[4])+"\n"+"\n")
	#f.write("###############################################\n\n")
	#f.write("Edge-Betweenness-C.: \n")
	#for item in relation:
	#	if G.has_node(i):
	#		f.write(str(nx.edge_betweenness_centrality(G).items()[i])+" "+"\n")
	#	else:
	#		f.write(str(0)+" "+"\n")
	#	i=i+1
	#f.write("\n###############################################\n\n")
	#f.write("Closeness Centrality of Graph:"+" "+ str(nx.closeness_centrality(G,True)))
	f.close() 







