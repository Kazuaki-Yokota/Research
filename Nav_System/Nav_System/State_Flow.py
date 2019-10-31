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
Finsh_Action_Juge_Name ="Finsh_Action_Juge"
Priority_Flag = "Priority_Flag"
Cost_Time = "Cost_Time"
Use_Resource = "Use_Resource"
Multitasking = "Multitasking"
#フローグラフ初期化関数
def Create_State_transition_init():

	total_recipe_state_list,first_recipe_state_list,second_recipe_state_list,first_recipe_flow_edges_list,second_recipe_flow_edges_list,cost_time,use_resource,multitasking = RM.Recipe()
	G = nx.DiGraph()

	State_list = total_recipe_state_list
	G.add_nodes_from(first_recipe_state_list)
	G.add_nodes_from(second_recipe_state_list)
	G.add_edges_from(first_recipe_flow_edges_list)
	G.add_edges_from(second_recipe_flow_edges_list)

	####各ノードに情報を追加設定#################################################################################################################
	nx.set_node_attributes(G, name=Action_Juge_Name , values=False)
	nx.set_node_attributes(G, name= Finsh_Action_Juge_Name, values=False)
	nx.set_node_attributes(G, name= Set_Node_Color, values="y")
	nx.set_node_attributes(G, name= Priority_Flag, values=False)
	####料理iの最終調理作業jの設定######################
	End_Node =["S16","SS4"]
	for i in range(0,len(End_Node)):
		print(End_Node[i])
		nx.set_node_attributes(G, name="End_Node" , values={End_Node[i]:End_Node[i]})
	#####################################################
	
	####優先Flagを設定###################################
	priority_flag =["S9","SS1","S10","SS2"]
	for i in range(0,len(priority_flag)):
		#print(End_Node[i])
		nx.set_node_attributes(G, name=Priority_Flag , values={priority_flag[i]:True})
	#####################################################

	####各作業の時間#####################################
	for node_num,cost in cost_time.items():
		G.nodes[node_num][Cost_Time] = cost
	#####################################################

	####各作業で使用するリソース#########################
	for resource_name,node_num_list in use_resource.items():
		for node_num in node_num_list:
			G.nodes[node_num][Use_Resource] = resource_name
	#####################################################

	####各作業で使用するリソース#########################
	for multitasking_name,node_num_list in multitasking.items():
		for node_num in node_num_list:
			print(type(node_num))
			G.nodes[node_num][Multitasking] = True
	#####################################################


	###############################################################################################################################################
	position = nx.spring_layout(G)
	nx.draw_networkx_nodes(G,position)
	nx.draw_networkx_edges(G,position)
	nx.draw_networkx_labels(G,position)
	plt.show()
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

	position = nx.spring_layout(G,)

	nx.draw_networkx_nodes(G,position,node_color = color_list)
	nx.draw_networkx_edges(G,position)
	nx.draw_networkx_labels(G,position)
	plt.show()
	#return G

#遷移状態を記録する
def Control_State2(G,state_list,now_state):

	#現在のノードをTrueにしてノード色を変更する
	nx.set_node_attributes(G, name = Action_Juge_Name ,values ={now_state:True})
	nx.set_node_attributes(G, name = Set_Node_Color ,values ={now_state:"c"})

	color_list = []
	for key in state_list:
		color_list.append(nx.get_node_attributes(G, Set_Node_Color)[key])

	position = nx.spring_layout(G,)

	nx.draw_networkx_nodes(G,position,node_color = color_list)
	nx.draw_networkx_edges(G,position)
	nx.draw_networkx_labels(G,position)
	plt.show()
	return G

def Next_State(G,now_state):
	#print(list(G.predecessors(now_state)))
	#print(list(G.successors(now_state)))

	#状態s+1を取得
	next_s = list(G.successors(now_state))

	result = []
	#状態s+1先分for文を回す
	for i in range(len(next_s)):
		#状態s+1の親ノードのすべてがAction_JugeがTrueなら
		par_s = list(G.predecessors(next_s[i]))
		print(par_s)
		print(len(par_s))
		next_s_count = 0
		for name_s in par_s:
			if G.nodes[name_s][Action_Juge_Name]:
				next_s_count +=1
				print(next_s_count)
			if next_s_count==len(par_s):
				result.append(next_s[i])
	print(result)		
	return G,result
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
	return G,state_list,Start_Node_list

def Main(now_state):
	G,state_list,n = Initialization()

	
	G = Control_State(G,state_list,now_state)
	Next_State(G,now_state)
	#now_state = input("HOW")
	#現在の状態から次に行うべき状態情報収集
if __name__=="__main__":
	Main("S1")