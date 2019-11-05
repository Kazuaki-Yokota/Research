import networkx as nx
import matplotlib.pyplot as plt
import sys
import time
import threading
Action_Juge_Name = 'Action_Juge'
Start_Node_list =[]
End_Node ="S16"
Set_Node_Color = "Set_Node_Color"



#################状態遷移の関する記述部#######################################
def Create_State_transition():
	G = nx.DiGraph()
	#G.add_node("S0")
	#State_list = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
	State_list = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16","SS1","SS2","SS3","SS4"]
	G.add_nodes_from(["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"])
	G.add_nodes_from(["SS1","SS2","SS3","SS4"])
	G.add_edges_from([("S2","S3"),("S4","S5"),("S7","S8"),("S9","S10"),
					  ("S6","S11"),("S8","S11"),("S11","S12"),("S12","S13"),
					  ("S1","S13"),("S3","S13"),("S5","S13"),("S13","S14"),("S10","S14"),
					  ("S14","S15"),("S15","S16")])
	G.add_edges_from([("SS1","SS2"),("SS2","SS3"),("SS3","SS4")])
	nx.set_node_attributes(G, name=End_Node , values={"S16":End_Node})
	nx.set_node_attributes(G, name=Action_Juge_Name , values=False)
	nx.set_node_attributes(G, name= Set_Node_Color, values="y")
	return G,State_list

def Next_State(G,now_state):
	
	
	key = [k for k, v in nx.get_node_attributes(G, End_Node).items() if v == End_Node]
	#print(key)

	if now_state == End_Node:
		print("########")
		print("Finsh Task")
		sys.exit()
	

	#print("Now State ",now_state)
	next_state_list = list(nx.all_neighbors(G,now_state))
	next_state = next_state_list[-1]
	#print("Next State ", next_state)
	return next_state

def Check_Adjacent_Node_Status(G,target_state,now_state):
	f_state = G.pred[target_state]
	b_state = G.succ[target_state]
	#print("Node adjacent to {0}  :front node {1}   back_node{2}".format(target_state,f_state,b_state))
	Check_Node_Status(G,target_state)

def Check_Node_Status(G,target_state):
	f_state = G.pred[target_state]

	if  not f_state:
		#print("END")
		Start_Node_list.append(target_state)
		pass
	else:
		for i_state in f_state:
			print(i_state)
			Check_Node_Status(G,i_state)
		
#############################################################################################

#################センシングの関する記述部#####################################################
def Sensing():
	#return input("Sensing: ")
	return "S1"
#############################################################################################

#################ナビゲーションの関する記述部################################################

#############################################################################################
def Control_Nav():
	print("Thread2")
	
	while True:
		print("AAAA")
		time.sleep(2)



def Control_State(Status_Graph,State_list):
	print("Thread1")
	while(True):
		now_state = Sensing()
		nx.set_node_attributes(Status_Graph, name = Action_Juge_Name ,values ={now_state:True})
		nx.set_node_attributes(Status_Graph, name = Set_Node_Color ,values ={now_state:"c"})
		next_state = Next_State(Status_Graph,now_state)
	
		Check_Adjacent_Node_Status(Status_Graph,next_state,now_state)


		color_list = []
		for key in State_list:
			color_list.append(nx.get_node_attributes(Status_Graph, Set_Node_Color)[key])

		#print(color_list)
		#print(dict(Status_Graph.nodes))

		position = nx.spring_layout(Status_Graph,)

		nx.draw_networkx_nodes(Status_Graph,position,node_color = color_list)
		nx.draw_networkx_edges(Status_Graph,position)
		nx.draw_networkx_labels(Status_Graph,position)
		plt.show()

def Main():
	
	Status_Graph,State_list = Create_State_transition()
	Check_Node_Status(Status_Graph,"S16")
	print(Start_Node_list)


	thread_1 = threading.Thread(target = Control_State,args = (Status_Graph,State_list))
	thread_2 = threading.Thread(target =  Control_Nav)
	
	thread_1.start()
	thread_2.start()

def Debeg():
	
	Status_Graph,State_list = Create_State_transition()

	Check_Node_Status(Status_Graph,"S16")
	print(Start_Node_list)
	#now_state = Sensing()
	#now_state ="S1"
	#nx.set_node_attributes(Status_Graph, name = Action_Juge_Name ,values ={now_state:True})
	#nx.set_node_attributes(Status_Graph, name = Set_Node_Color ,values ={now_state:"c"})

	
	color_list = []
	for key in State_list:
		color_list.append(nx.get_node_attributes(Status_Graph, Set_Node_Color)[key])

	position = nx.spring_layout(Status_Graph)

	nx.draw_networkx_nodes(Status_Graph,position,node_color = color_list)
	nx.draw_networkx_edges(Status_Graph,position)
	nx.draw_networkx_labels(Status_Graph,position)
	#nx.draw_networkx(Status_Graph)
	plt.show()

Main()
#Debeg()