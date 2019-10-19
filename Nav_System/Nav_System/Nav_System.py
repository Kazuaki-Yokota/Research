import networkx as nx
import matplotlib.pyplot as plt
import sys

Action_Juge_Name = 'Action_Juge'
Finsh_State =[]
End_Node ="S16"
def Create_State_transition():
	G = nx.DiGraph()
	#G.add_node("S0")
	G.add_nodes_from(["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"])

	G.add_edges_from([("S2","S3"),("S4","S5"),("S7","S8"),("S9","S10"),
					  ("S6","S11"),("S8","S11"),("S11","S12"),("S12","S13"),
					  ("S1","S13"),("S3","S13"),("S5","S13"),("S13","S14"),("S10","S14"),
					  ("S14","S15"),("S15","S16")])
	nx.set_node_attributes(G, name=End_Node , values={"S16":End_Node})
	nx.set_node_attributes(G, name=Action_Juge_Name , values=False)
	return G

def Next_State(G,now_state):
	
	
	key = [k for k, v in nx.get_node_attributes(G, End_Node).items() if v == End_Node]
	#print(key)

	if now_state == End_Node:
		print("########")
		print("Finsh Task")
		sys.exit()
	

	print("Now State ",now_state)
	next_state_list = list(nx.all_neighbors(G,now_state))
	next_state = next_state_list[-1]
	print("Next State ", next_state)
	return next_state

def Check_Adjacent_Node_Status(G,target_state,now_state):
	f_state = G.pred[target_state]
	b_state = G.succ[target_state]
	print("Node adjacent to {0}  :front node {1}   back_node{2}".format(target_state,f_state,b_state))
	Check_Node_Status(G,target_state)

def Check_Node_Status(G,target_state):
	f_state = G.pred[target_state]

	if  not f_state:
		#print("END")
		pass
	else:
		for i_state in f_state:
			print(i_state)
			Check_Node_Status(G,i_state)
		

def Main():
	Status_Graph = Create_State_transition()
	nx.set_node_attributes(Status_Graph, name = Action_Juge_Name ,values ={"S1":True,"S2":True,"S8":True})
	next_state = Next_State(Status_Graph,"S1")
	
	Check_Adjacent_Node_Status(Status_Graph,next_state,"S1")
	#print(dict(Status_Graph.nodes))
	#nx.draw_networkx(Status_Graph)
	#plt.show()


Main()