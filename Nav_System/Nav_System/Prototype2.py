
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
	now_task_list =[]

	memory ={"work1":{"time_memory":work1_time_memory,"state":work1_time_state},
		  "work2":{"time_memory":work2_time_memory,"state":work2_time_state},
		  "IH1":{"time_memory":IH1_time_memory,"state":IH1_time_state},
		  "IH2":{"time_memory":IH2_time_memory,"state":IH2_time_state}}

	#調理者の状態
	user_state = True

	return memory,cost_memory,now_task_list


def Select_Action(G,memory,Ready_state,Action_History,now_task_list):
	#優先作業の検出
	pri_f_result = Find_Specific_Attribute_Node(G,"Priority_Flag",True)


	#Ready_State集合の中に優先作業があるか
	pri_result =[]
	for i in pri_f_result:
		if i in Ready_state:
			pri_result.append(i)

	if pri_result:
		print(pri_result)
		now_task = random.choice(pri_result)
		for n in list(G.predecessors(now_task)):
			if not now_task in now_task_list:
				#優先作業flagをOFFにする
				G.nodes[str(now_task)]["Priority_Flag"] = False
			else:
				if Ready_state:
					Ready_state.remove(now_task)
					up_now_task = random.choice(Ready_state)
					Ready_state.append(now_task)
					now_task = up_now_task
	else:
		#Reay_Stateから行動を選択
		if Ready_state:
			print(Ready_state)
			now_task = random.choice(Ready_state)

	Ready_state.remove(now_task)
	now_task_list.append(now_task)
	return G,now_task,now_task_list

def Select_WorkSpace(G,memory,now_task):
	#作業場所の決定
	#IHを使用する作業の場合
	if now_task in Find_Specific_Attribute_Node(G,"Use_Resource","IH"):
		if memory["IH1"]["state"]:
			cost = G.nodes[now_task]["Cost_Time"]
			work_name ="IH1"
		elif memory["IH2"]["state"]:
			cost = G.nodes[now_task]["Cost_Time"]
			work_name ="IH2"
		else:
			print("Time_Pass")
			work_name ="Pass"
			cost = 0

	#ワークスペースを使用する作業の場合
	elif now_task in Find_Specific_Attribute_Node(G,"Use_Resource","work"):
		if memory["work1"]["state"]:
			cost = G.nodes[now_task]["Cost_Time"]
			work_name ="work1"
		elif memory["work2"]["state"]:
			cost = G.nodes[now_task]["Cost_Time"]
			work_name ="work2"
		else:
			print("Time_Pass")
			work_name ="Pass"
			cost = 0
	else:
		pass

	return G,work_name,cost
			
def Multi_Juge(G,now_task):
	
	#状態Sでの作業はマルチタスクが可能かを判定
	if  now_task in  Find_Specific_Attribute_Node(G,"Multitasking",True):#マルチタスク可能
		return True
	else:#マルチタスク不可
		return False

def Record_Memory(G,memory,now_task,work_name,cost,time,Multi):
	result = []
	for key in memory:
		result.append(key)

	result.remove(work_name)


	if Multi:#マルチタスクが可能な場合
		sub_cost =1
	else:
		sub_cost = cost

	#使用するワークスペース名を使えなくする
	memory[work_name]["state"]=False

	#使用するワークスペースのタイムメモリーに行動完了にかかる時間記録する
	for i in range(cost):
		memory[work_name]["time_memory"].append(now_task)
	#使用するワークスペース以外のタイムメモリーにコストを記録する
	for name in result:
		#ワークスペースが使用可能なら
		if memory[name]["state"]:
			for i in range(sub_cost):
				memory[name]["time_memory"].append("")
		elif memory[name]["state"] == False and Multi == True:
			pass
		elif memory[name]["state"]== False and Multi == False:

			F_memory_len = len(memory[name]["time_memory"])
			T_memory_len = len(memory[work_name]["time_memory"])

			
			if T_memory_len > F_memory_len:
				sub = abs(T_memory_len-F_memory_len)

				for i in range(sub):
					memory[name]["time_memory"].append("")


	return G,memory




def Check_Time(G,All_state,Ready_state,memory,time_count,mult_f,now_task_list):

	
	for key in memory:
		if len(memory[key]["time_memory"]) > 0:
			if len(memory[key]["time_memory"]) == time_count:
				memory[key]["state"] =True
				#if memory[key]["time_memory"][-1] !="":
					#G,Ready_state = Add_Next_State(G,All_state,Ready_state,memory[key]["time_memory"][-1])
				if memory[key]["time_memory"][-1] in now_task_list:
					now_task_list.remove(memory[key]["time_memory"][-1])
				if not memory[key]["time_memory"][-1] in Find_Specific_Attribute_Node(G,"Multitasking",True):
					mult_f = True


	return G,Ready_state,memory,mult_f,now_task_list







def Add_Next_State(G,All_state,Ready_state,now_task):

	print("%%%%%%%%%%%%%%%%%%%")
	print("END_TASK",now_task)
	#Ready_state.remove(now_task)
	G = SFC.Control_State(G,All_state,now_task)
	G,result = SFC.Next_State(G,now_task)
	Ready_state.extend(result)
	return G,Ready_state


def Main():
	memory,cost_memory,now_tassk_list = init()
	G,All_state,Ready_state = SFC.Initialization()
	time_count = 0
	now_task =""
	mult_f =True
	pass_f = False
	work_space_name =""
	Action_History=[]
	print("############################")
	print("Start",Ready_state)
	#1回転を30秒タスク
	while True:
		print("::::::::::::::::::::::::::::")
		for key in memory:
			print(key,memory[key]["state"])
		for key in memory:
			print(key,memory[key]["time_memory"])
		print("::::::::::::::::::::::::::::")

		
		G,Ready_state,memory,mult_f,now_tassk_list = Check_Time(G,All_state,Ready_state,memory,time_count,mult_f,now_tassk_list)
		if not Ready_state:
			break
		#行動Aを選択する
		if mult_f:
			G,now_task,now_tassk_list = Select_Action(G,memory,Ready_state,Action_History,now_tassk_list)
			print("タスク状態",now_task)
			#行動Aを行える場所を決定する
			G,work_space_name,cost = Select_WorkSpace(G,memory,now_task)
			print("タスク状態",now_task,"Cost",cost)

			if work_space_name != "Pass":
				mult_flag = Multi_Juge(G,now_task)
				mult_f = mult_flag
				G,memory = Record_Memory(G,memory,now_task,work_space_name,cost,time_count,mult_flag)

				G,Ready_state = Add_Next_State(G,All_state,Ready_state,now_task)



		print("\n ######################")
		print("Time ",time_count)
		if work_space_name != "Pass":
			time_count+=1






























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