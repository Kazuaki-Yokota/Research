#Nav_Control.py
#ナビゲーションメイン機能を保持する
import wx
import Recipe_Mode as RM
#from multiprocessing import Process, Value, Array,Queue,Pipe

def Main(now_state):

	receipe_text_data = RM.Recipe_Text()
	
	#print(type(receipe_text_data))

	#print(receipe_text_data[now_state])

	return receipe_text_data[now_state]
	

#print(Main("S1"))