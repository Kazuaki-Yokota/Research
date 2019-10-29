#################################################
import Recipe_Mode as RM
import State_Flow as SFC
import pprint
import random
import networkx as nx

def Find_Specific_Attribute_Node(G,attr, value):
	result = []

	d = nx.get_node_attributes(G, attr)

	for key,v in d.items():
		if(v == value):
			result.append(key)

	return result



def Main():
	#各ワークのタイムメモリーを格納するリスト
	work1_time_memory =[]
	work2_time_memory =[]
	IH1_time_memory =[]
	IH2_time_memory =[]


	G,All_state,Ready_state = SFC.Initialization()

	print("入力されている料理のすべての状態集合",All_state)
	print("実行可能状態集合",Ready_state)
	print()




	pprint.pprint(dict(G.nodes))


	
	
	while True:
		pri_f_result = Find_Specific_Attribute_Node(G,"Priority_Flag",True)
		try:
			if pri_f_result:
				print("Find Priority_Flag")
				now_task = pri_f_result.pop(0)
				print(now_task)
				G.nodes[str(now_task)]["Priority_Flag"] = False
			else:
				print("Nothing Priority_Flag")
				now_task = random.choice(Ready_state)

			Ready_state.remove(now_task)
			print(now_task)
		except:
			print("ERROR")
			break



Main()