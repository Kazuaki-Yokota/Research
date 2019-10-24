import networkx as nx
import matplotlib.pyplot as plt
import sys
import time
import threading

#################################################
import Recipe_Mode as RM


Start_Node_list =[]
Set_Node_Color = "Set_Node_Color"
Action_Juge_Name = 'Action_Juge'
#フローグラフ初期化関数
def Create_State_transition_init():

	total_recipe_state_list,first_recipe_state_list,second_recipe_state_list,first_recipe_flow_edges_list,second_recipe_flow_edges_list = RM.Recipe()
	G = nx.DiGraph()

	State_list = total_recipe_state_list
	G.add_nodes_from(first_recipe_state_list)
	G.add_nodes_from(second_recipe_state_list)
	G.add_edges_from(first_recipe_flow_edges_list)
	G.add_edges_from(second_recipe_flow_edges_list)

	End_Node =["S16","SS4"]
	for i in range(0,len(End_Node)-1):
		#print(End_Node[i])
		nx.set_node_attributes(G, name="End_Node" , values={End_Node[i]:End_Node[i]})
	#End_Node = "S16"
	#nx.set_node_attributes(G, name="End_Node" , values={"S16":End_Node})
	nx.set_node_attributes(G, name=Action_Juge_Name , values=False)
	nx.set_node_attributes(G, name= Set_Node_Color, values="y")

	
	#position = nx.spring_layout(G)
	#nx.draw_networkx_nodes(G,position)
	#nx.draw_networkx_edges(G,position)
	#nx.draw_networkx_labels(G,position)
	#plt.show()
	return G,State_list,End_Node

#フローグラフの深度の深いところから探索
def Check_Node_Status(G,target_state):
	f_state = G.pred[target_state]
	#print(f_state)
	if  not f_state:
		#print("END")
		Start_Node_list.append(target_state)
	else:
		for i_state in f_state:
			#print(i_state)
			Check_Node_Status(G,i_state)

#遷移状態を記録する
def Control_State(G,state_list,now_state):

	#現在のノードをTrueにしてノード色を変更する
	nx.set_node_attributes(G, name = Action_Juge_Name ,values ={now_state:True})
	nx.set_node_attributes(G, name = Set_Node_Color ,values ={now_state:"c"})

	color_list = []
	for key in state_list:
		color_list.append(nx.get_node_attributes(G, Set_Node_Color)[key])

	#position = nx.spring_layout(G,)

	#nx.draw_networkx_nodes(G,position,node_color = color_list)
	#nx.draw_networkx_edges(G,position)
	#nx.draw_networkx_labels(G,position)
	#plt.show()
	


def Initialization():
	#######初期化機能##############
	#フローグラフの初期化と生成
	G,state_list,End_node_num= Create_State_transition_init()

	#フローグラフの状態確認
	for num in End_node_num:
		Check_Node_Status(G,num)

	#初期状態候補
	#print(Start_Node_list)
	##################################
	return G,state_list

def Main(now_state):
	G,state_list = Initialization()
	Control_State(G,state_list,now_state)
	#現在の状態から次に行うべき状態情報収集
if __name__=="__main__":
	Main("S1")