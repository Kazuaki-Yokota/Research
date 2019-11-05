import Recipe_Mode as RM
import State_Flow as SFC
import pprint
import random
import networkx as nx
import copy
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
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


	work_name ={"work":["work1","work2"],"IH":["IH1","IH2"]}
	cost_memory ={"work1":[],"work2":[],"IH1":[],"IH2":[]}
	now_task_list =[]

	memory ={"work1":{"time_memory":work1_time_memory,"state":work1_time_state},
		  "work2":{"time_memory":work2_time_memory,"state":work2_time_state},
		  "IH1":{"time_memory":IH1_time_memory,"state":IH1_time_state},
		  "IH2":{"time_memory":IH2_time_memory,"state":IH2_time_state}}

	#調理者の状態
	user_state = True

	#学習回数
	episode = 5000
	#イプシロン値
	epsilon = 0.2
	#学習率
	alpha = 0.01
	return memory,cost_memory,now_task_list,work_name,epsilon,alpha,episode

def Resetting():
	#各ワークのタイムメモリーを格納するリスト
	work1_time_memory =[]
	work2_time_memory =[]
	IH1_time_memory =[]
	IH2_time_memory =[]

	#各ワークの状態遷移
	work1_time_state =True
	work2_time_state =True
	IH1_time_state = True
	IH2_time_state = True
	memory ={"work1":{"time_memory":work1_time_memory,"state":work1_time_state},
		  "work2":{"time_memory":work2_time_memory,"state":work2_time_state},
		  "IH1":{"time_memory":IH1_time_memory,"state":IH1_time_state},
		  "IH2":{"time_memory":IH2_time_memory,"state":IH2_time_state}}

	return memory

def Select_Action_R(G,Ready_State,epsilon):
	#確率epsilonでランダム。１－epsilonで報酬の最大値から
	#Reward ="Reward"
	
	print("Ready_State",Ready_State)
	
	probability = np.random.rand(1)
	

	if Ready_State:
		if probability <epsilon:
			now_task =random.choice(Ready_State)
		else:
			tmp = G.nodes[Ready_State[0]]["Reward"]
			now_task = Ready_State[0]
			for key in Ready_State:
				if tmp < G.nodes[key]["Reward"]:
					tmp = G.nodes[key]["Reward"]
					now_task = key
	else:
		now_task="pass"
	return G,now_task







def Select_Action(G,Ready_state):



	def R_Select(G,Ready_state,pri):
		Ready_S = Ready_state
		if pri:
			for i in pri:
				Ready_S.remove(i)
		now = random.choice(Ready_state)
		return now





	#優先作業の検出
	#Session 1
	pri_f_result = Find_Specific_Attribute_Node(G,"Priority_Flag",True)

	#Ready_State集合の中に優先作業があるか
	pri_result =[]
	for i in pri_f_result:
		if i in Ready_state:
			pri_result.append(i)

	#Session1-1
	if pri_result:
		#下の行をで行動を選択している
		now_task = random.choice(pri_result)

		#Session1-1-1
		juge_count = 0
		if list(G.predecessors(now_task)):
			for n in list(G.predecessors(now_task)):
				if G.nodes[n]["Finsh_Action_Juge"] == True:
					juge_count +=1
		#Session1-1-2
		if len(list(G.predecessors(now_task))) != juge_count:
			now_task = R_Select(G,Ready_state,pri_result)
	#Session1-2
	else:
		now_task = R_Select(G,Ready_state,pri_result)

	return G,now_task

def Select_WorkSpace(G,memory,now_task,work_name):
	#Session2
	
	for key_name in work_name:
		#print(key_name)
		if now_task in Find_Specific_Attribute_Node(G,"Use_Resource",key_name):
			for name in work_name[key_name]:
				if memory[name]["state"]:
					time_cost = G.nodes[now_task]["Cost_Time"]
					#print(name)
					memory[name]["state"] = False

					#3番をここに記述する
					return G,name,time_cost

	#print("すべて使用中")
	name ="Pass"
	time_cost =0
	return G,name,time_cost


def Multi_Juge(G,now_task):
	#状態Sでの作業はマルチタスクが可能かを判定
	if  now_task in  Find_Specific_Attribute_Node(G,"Multitasking",True):#マルチタスク可能
		return True
	else:#マルチタスク不可
		return False

def Record_Memory(G,memory,now_task,work_name,time_cost,Ready_state):
	
	#print(now_task,"の",time_cost)
	for i in range(time_cost):
		
		memory[work_name]["time_memory"].append(now_task)

	
	Ready_state.remove(now_task)
	return G,memory,Ready_state

def Time_Count(memory,time_count):

	time_count +=1

	for work_name in memory:
		if len(memory[work_name]["time_memory"]) == time_count:
			memory[work_name]["time_memory"].append("")
	return memory,time_count


def End_Task_Juge(G,All_state,Ready_state,memory,Time,F_flag):

	#print("END_TASK_JUGE")
	#print("Now_TIME",Time)
	for work_name in memory:
		#print(work_name)
		#print(len(memory[work_name]["time_memory"])-1)
		if len(memory[work_name]["time_memory"])-1 == Time:
			#print()
			End_Task = memory[work_name]["time_memory"][-1]
			#print("End_Task")
			#print(End_Task)
			if End_Task != "":
				G.nodes[End_Task]["Action_Juge"] = True
				
				#G = SFC.Control_State2(G,All_state,End_Task)
				G,result = SFC.Next_State(G,End_Task)
				Ready_state.extend(result)
				#print("ADD",result)
				G.nodes[End_Task]["Finsh_Action_Juge"] = True
				memory[work_name]["state"] = True
				if not End_Task in Find_Specific_Attribute_Node(G,"Multitasking",True):
					F_flag = True
	return G,F_flag

def Finsh_Schedule(G):
	FJ = 0
	loop_count = 0
	for s in G:
		loop_count +=1
		if G.nodes[s]["Finsh_Action_Juge"]:
			FJ +=1
	if loop_count == FJ:
		return True
	return False


def Action_Evaluation(G,alpha,now_task,Ready_state,Time):
	import copy
	Next_stage = copy.copy(Ready_state)
	G,result = SFC.Next_State(G,now_task)
	Next_stage.extend(result)


	tmp = Next_stage[0]
	for key in Next_stage:
		if G.nodes[tmp]["Reward"] < G.nodes[key]["Reward"]:
			tmp = key

	gamma = 0.6
	
	reward =1/(Time+2)
	G.nodes[now_task]["Reward"] = (1-alpha)*float(G.nodes[now_task]["Reward"]) + alpha*(float(reward )+ gamma*float(G.nodes[tmp]["Reward"]))

	return G


def learing(G,memory,Ready_state,All_state,F_flag,Time,work_name_list,epsilon,alpha):

	while True:
		
		#Session 0
		if F_flag:
			#print("Ready_state",Ready_state)
			#1 行動の選択
			#G,now_task=Select_Action(G,Ready_state)
			G,now_task = Select_Action_R(G,Ready_state,epsilon)

			if now_task != "pass":
				G = Action_Evaluation(G,alpha,now_task,Ready_state,Time)
				
				#2 ワークスペースの選択
				G,work_name,time_cost = Select_WorkSpace(G,memory,now_task,work_name_list)
				#print(work_name)

				
				if work_name !="Pass":
					# 4 選ばれた行動が並行タスク可能かどうか
					F_flag = Multi_Juge(G,now_task)

					##3 タイムスケジュールに記録する
					G,memory,Ready_state = Record_Memory(G,memory,now_task,work_name,time_cost,Ready_state)
			
		memory,Time=Time_Count(memory,Time)

			#Session 6 タスクの終了判定
		G,F_flag = End_Task_Juge(G,All_state,Ready_state,memory,Time,F_flag)
		if Finsh_Schedule(G) == True:
			return G,memory,Time


def Main():
	#memory,cost_memory,now_tassk_list,work_name_list,episode,epsilon,alpha = init()
	memory,cost_memory,now_task_list,work_name_list,epsilon,alpha,episode = init()
	G,All_state,Ready_state = SFC.Initialization()
	
	print(Ready_state)
	Time = -1#時刻T
	F_flag = True
	
	try_count = 0
	RA_list =[]
	action_story=[]
	while episode > try_count:

		
		Time = -1#時刻T
		F_flag = True
		G,Ready_state = SFC.Resetting(G)
		memory = Resetting()
		G,memory,Time = learing(G,memory,Ready_state,All_state,F_flag,Time,work_name_list,epsilon,alpha)
		RA_list.append(Time)
		story =[]
		for key in memory:
			story.append(memory[key]["time_memory"])
		action_story.append(story)
		
		try_count +=1

	

	

	plt.show()

	#print(RA_list)
	sum = 0
	min = 1000000

	c_count =-1
	min_c =0
	for i in RA_list:
		sum +=i
		c_count+=1

		if min > i:
			min = i
			min_c=c_count

	ave = sum/len(RA_list)
	print("ave",ave)
	print("min",min)

	print(min_c)
	

	#print()
	#print(action_story)
	index_work = []
	for key in memory:
		index_work.append(str(key))
		
	#df =pd.DataFrame([memory[index_work[0]]["time_memory"],memory[index_work[1]]["time_memory"],memory[index_work[2]]["time_memory"],memory[index_work[3]]["time_memory"]],
	#			  index =index_work)

	df =pd.DataFrame([action_story[min_c][0],
				   action_story[min_c][1],
				   action_story[min_c][2],
				   action_story[min_c][3]],
				   index =index_work)
	plt.plot(RA_list)
	plt.show()
	
	print(len(df.columns))
	return df


df = Main()
tmp =  df
#c = 0
#tmp = 0
#for c in range(0,10):
#	df = Main()
#	print(df)
#	if c ==0:
#		tmp = df
#	if c !=0:
#		if len(df.columns) < len(tmp.columns):
#			tmp = df

print("最小行数：",len(tmp.columns))
file_name = "test.xlsx"
tmp.to_excel(file_name)