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

	
		
		#print(memory[name]["time_memory"][-1])
		for name in result:
			name = str(name)
			#print(name)
			if len(memory[name]["time_memory"]) == time_count:
				memory[name]["state"] = True
				#print("###########################################")
				#print(name)
				#print("mul",Find_Specific_Attribute_Node(G,"Multitasking",True))
				#print("now",memory[name]["time_memory"][-1])
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


	memory ={"work1":{"time_memory":work1_time_memory,"state":work1_time_state},
		  "work2":{"time_memory":work2_time_memory,"state":work2_time_state},
		  "IH1":{"time_memory":IH1_time_memory,"state":IH1_time_state},
		  "IH2":{"time_memory":IH2_time_memory,"state":IH2_time_state}}

	#調理者の状態
	user_state = True

	return memory


def Add_Record(G):
	pass
def Main():
	memory = init()
	G,All_state,Ready_state = SFC.Initialization()
	time_count = 0
	now_task =""
	mult_f =True
	#1回転を30秒タスク
	while True:

		memory,mult_f = Check_Time_Memory(G,memory,time_count,mult_f)
		pri_f_result = Find_Specific_Attribute_Node(G,"Priority_Flag",True)
		print("##############")
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
					print("#######################################")
					print("###########################################")
					print(type(now_task))
					Ready_state.remove(now_task)
					G = SFC.Control_State(G,All_state,now_task)
					G,result = SFC.Next_State(G,now_task)
					print("result",result)
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
						import time
						time.sleep(3)
				if now_task in Find_Specific_Attribute_Node(G,"Use_Resource","work"):
					if memory["work1"]["state"]:
						cost = G.nodes[now_task]["Cost_Time"]
						work_name ="work1"
						print(memory["work1"]["state"])
					
				#print("cost",cost)
				#別のタスクを並行しても大丈夫か？
				if not now_task in  Find_Specific_Attribute_Node(G,"Multitasking",True):
					print("並行タスクできません。シングルタスク処理を行います。")
					memory = Record_memory(memory,work_name,now_task,cost,False)
					mult_f = False

				else:
					print("並行タスク処理を行います。")
					memory = Record_memory(memory,work_name,now_task,cost,True)
				

				pprint.pprint(memory)
				print("################")


		
			except (ZeroDivisionError, TypeError) as e:
				print(e)
				break

		print()
		time_count +=1
		if not Ready_state :
			print(time_count)
			SFC.Control_State2(G,All_state,now_task)
			break
		

#
#
#Main()

a=[1,2]
b = [1,3,4]



if a in b:
	print("WW")
t = False

if not t:
	print("AS")