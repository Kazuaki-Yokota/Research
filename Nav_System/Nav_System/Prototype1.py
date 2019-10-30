#################################################
import Recipe_Mode as RM
import State_Flow as SFC
import pprint
import random
import networkx as nx
import copy


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
		
	else:
		#print(cost)
		sub_cost =cost
		
	memory[work_name]["state"]=False
	for i in range(cost):
		memory[work_name]["time_memory"].append(node_name)


	for name in result:
		if  memory[name]["state"]:
			for i in range(sub_cost):
				memory[name]["time_memory"].append("")
	
	return memory


def Check_Time_Memory(G,memory,time_count,mult_f):
	if time_count > 0:
		result =[]
		for key in memory:
			result.append(key)

		r = copy.copy(result)
		
		#print(memory[name]["time_memory"][-1])
		for name in result:
			name = str(name)
			print("name",name)
			if len(memory[name]["time_memory"]) == time_count:
				memory[name]["state"] = True
				

				if memory[name]["time_memory"][-1] in Find_Specific_Attribute_Node(G,"Multitasking",True):
					print("調整を行います")
					r.remove(name)

					for n in r:
						if len(memory[name]["time_memory"]) < len(memory[n]["time_memory"]):
							
							sub =len(memory[n]["time_memory"]) - len(memory[name]["time_memory"])

							for i in range(sub):
								 memory[name]["time_memory"].append("")

				if not (memory[name]["time_memory"][-1] in Find_Specific_Attribute_Node(G,"Multitasking",True))and not (memory[name]["time_memory"][-1] in [""]):
					mult_f = True
				#	print("mult_fをTrueにします")
				#print(name,"をTrueにします。")
	return memory,mult_f


def init():
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

	cost_memory ={"work1":[],"work2":[],"IH1":[],"IH2":[]}

	memory ={"work1":{"time_memory":work1_time_memory,"state":work1_time_state},
		  "work2":{"time_memory":work2_time_memory,"state":work2_time_state},
		  "IH1":{"time_memory":IH1_time_memory,"state":IH1_time_state},
		  "IH2":{"time_memory":IH2_time_memory,"state":IH2_time_state}}

	#調理者の状態
	user_state = True

	return memory,cost_memory

def Main():
	memory,cost_memory = init()
	G,All_state,Ready_state = SFC.Initialization()
	time_count = 0
	now_task =""
	mult_f =True
	pass_f = False
	#1回転を30秒タスク
	while True:

		#やるべきタスクがなければ終了
		if not Ready_state :
			break



		memory,mult_f = Check_Time_Memory(G,memory,time_count,mult_f)

		pri_f_result = Find_Specific_Attribute_Node(G,"Priority_Flag",True)
		
		print("time_count",time_count)
		print("Mult_F",mult_f)
		if mult_f:
			print("Ready_state",Ready_state)
			try:
				#優先フラグか一般か？
				if pri_f_result:
					now_task = pri_f_result.pop(0)
				
					G.nodes[str(now_task)]["Priority_Flag"] = False
				else:
					if Ready_state:
						now_task = random.choice(Ready_state)


				if Ready_state:
					print("HIT")
					Ready_state.remove(str(now_task))
					G = SFC.Control_State(G,All_state,now_task)
					G,result = SFC.Next_State(G,now_task)
					Ready_state.extend(result)
					
					
				print("タスク状態",now_task)
				now_task = str(now_task)

			
				if now_task in Find_Specific_Attribute_Node(G,"Use_Resource","IH"):
					if memory["IH1"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="IH1"
					elif memory["IH2"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="IH2"
					else:
						print("Time_Pass")
						#Ready_state.append(now_task)
						#pass_f = True

				if now_task in Find_Specific_Attribute_Node(G,"Use_Resource","work"):
					if memory["work1"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="work1"
						print(memory["work1"]["state"])
					else:
						print("Time_Pass")
						#Ready_state.append(now_task)
						#pass_f = True

				if not pass_f:
					#別のタスクを並行しても大丈夫か？
					if not now_task in  Find_Specific_Attribute_Node(G,"Multitasking",True):
						print("並行タスクできません。シングルタスク処理を行います。")
						memory = Record_memory(memory,work_name,now_task,cost,False)
						mult_f = False

					else:
						print("並行タスク処理を行います。")
						memory = Record_memory(memory,work_name,now_task,cost,True)
				

					pprint.pprint(memory)
					
					
		
			except (ZeroDivisionError, TypeError) as e:
				print(e)
				break

		print(pass_f)
		print("####")


		time_count +=1
		pass_f = False
		
	
	print(time_count)

	a = []
	index_work = []
	for key in memory:
		index_work.append(str(key))
		print(str(key)+" ",len(memory[str(key)]["time_memory"]))
	SFC.Control_State2(G,All_state,now_task)

	import pandas as pd


	for i in range(len(index_work)):
		print(type(index_work[i]))
	df =pd.DataFrame([memory[index_work[0]]["time_memory"],memory[index_work[1]]["time_memory"],memory[index_work[2]]["time_memory"],memory[index_work[3]]["time_memory"]],
				  index =index_work)

	file_name = "test.xlsx"
	print(df)

	df.to_excel(file_name)
Main()