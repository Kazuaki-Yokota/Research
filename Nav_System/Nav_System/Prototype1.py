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


	
def Record_memory(memory,work_name,node_name,cost,Multitasking):
	result =[]
	for key in memory:
		result.append(key)

	result.remove(work_name)


	if Multitasking:
		sub_cost = 1
		mult_f = True
	else:
		print(cost)
		sub_cost =cost
		mult_f = False


	memory[work_name]["state"]=False
	for i in range(cost):
		memory[work_name]["time_memory"].append(node_name)


	for name in result:
		if  memory[name]["state"]:
			for i in range(sub_cost):
				memory[name]["time_memory"].append("")

	#pprint.pprint(memory)

	print("################")
	#print(memory)
	return memory,mult_f


def Check_Time_Memory(G,memory,time_count,mult_f):
	if time_count > 0:
		result =[]
		for key in memory:
			result.append(key)

	
	
		#print(memory[name]["time_memory"][-1])
		for name in result:
			name = str(name)
			if len(memory[name]["time_memory"]) == time_count:
				memory[name]["state"] = True
				print("AAAAAA")
				if memory[name]["time_memory"][-1] != Find_Specific_Attribute_Node(G,"Multitasking",True):
					mult_f = True
				print(name,"をTrueにします。")
	return memory,mult_f



def Main():
	#各ワークのタイムメモリーを格納するリスト
	work1_time_memory =[]
	work2_time_memory =[]
	IH1_time_memory =[]
	IH2_time_memory =[]

	time_memory_state =[work1_time_memory,work2_time_memory,IH1_time_memory,IH2_time_memory]
	#各ワークの状態遷移
	work1_time_state =True
	work2_time_state =True
	IH1_time_state = True
	IH2_time_state = True


	memory ={"work1":{"time_memory":work1_time_memory,"state":work1_time_state},
		  "work2":{"time_memory":work2_time_memory,"state":work2_time_state},
		  "IH1":{"time_memory":IH1_time_memory,"state":IH1_time_state},
		  "IH2":{"time_memory":IH2_time_memory,"state":IH2_time_state}}


	#Record_memory(memory,"IH1","S9",10,True)
	#Record_memory(memory,"IH2","SS1",10,True)
	#Record_memory(memory,"work1","S1",1,False)
	#調理者の状態
	user_state = True

	G,All_state,Ready_state = SFC.Initialization()

	print("入力されている料理のすべての状態集合",All_state)
	print("実行可能状態集合",Ready_state)
	print()




	#pprint.pprint(dict(G.nodes))


	
	time_count = 0

	now_task =""
	mult_f =True
	#1回転を30秒タスク
	while True:

		memory,mult_f = Check_Time_Memory(G,memory,time_count,mult_f)
		pri_f_result = Find_Specific_Attribute_Node(G,"Priority_Flag",True)


		if mult_f:
			try:
				#優先フラグか一般か？
				if pri_f_result:
					#print("Find Priority_Flag")
					now_task = pri_f_result.pop(0)
				
					G.nodes[str(now_task)]["Priority_Flag"] = False
				else:
					#print("Nothing Priority_Flag")
					now_task = random.choice(Ready_state)

				print("タスク状態",now_task)
				Ready_state.remove(now_task)
				now_task = str(now_task)

			
				if now_task in Find_Specific_Attribute_Node(G,"Use_Resource","IH"):
					if memory["IH1"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="IH1"
					elif memory["IH2"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="IH2"

				if now_task in Find_Specific_Attribute_Node(G,"Use_Resource","work"):
					if memory["work1"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="work1"
						print(memory["work1"]["state"])
					
				print("cost",cost)
				#別のタスクを並行しても大丈夫か？
				if not now_task in  Find_Specific_Attribute_Node(G,"Multitasking",True):
					print("並行タスクできません。シングルタスク処理を行います。")
					memory,mult_f = Record_memory(memory,work_name,now_task,cost,False)
				

				else:
					print("並行タスク処理を行います。")
					memory,mult_f = Record_memory(memory,work_name,now_task,cost,True)
				

				pprint.pprint(memory)
				print("################")


		
			except (ZeroDivisionError, TypeError) as e:
				print(e)
				break

		print()
		time_count +=1
		

Main()