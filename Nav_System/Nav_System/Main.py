import wx
from multiprocessing import Process, Value, Array,Queue,Pipe


import Nav_Control as NC
import State_Flow as SFC
import Nav_GUI
import Connect 
import Sensing

import threading
import socket
import time
#ナビゲーションを行う画面に関する記述
def Nav_Window_Control():

	app = Nav_GUI.MainApp(0)
	app.MainLoop()
	
#Server
def Nav_Window_connect(text_q):
	IP = "localhost"
	Port =10001
	print("Nav_window")
	text = text_q.get()
	Connect.Server(IP,Port,text)

#ダミーセンシング結果
def Sensing(now_q):
	print("A1")
	while True:
		now_q.put(Connect.Client('127.0.0.1',50007))


	#while True:
	#	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	#		s.connect(("127.0.0.1",50007))
	#		s.sendall(b'hello')
	#		data = s.recv(1024)
	#		print(repr(data))
	#		now_q.put(data.decode('utf-8'))
		
	#		time.sleep(3)


#ナビゲーション内容を扱う
def F_Nav(now_q,next_q,SFC_to_Nav_q,text_q):

	while True:
		if not SFC_to_Nav_q.empty():
			print("A2")
			now_s = SFC_to_Nav_q.get()
			text = NC.Main(now_s)
			print(text)
			text_q.put(text)


#状態遷移を管理する
def F_SFC(now_q,next_q,SFC_to_Nav_q):
	while True:
		if not now_q.empty():
			print("A3")
			now_s = now_q.get()
			G,state_list = SFC.Initialization()
			
			SFC.Control_State(G,state_list,now_s)
			print(dict(G.nodes))
			SFC_to_Nav_q.put(now_s)

def Main():
	
	now_q = Queue()#From Sensing to SFC
	next_q = Queue()#From Sensing to SFC

	SFC_to_Nav_q = Queue()#From SFC to Nav
	
	text_q = Queue() # From Nav to Nav_window
	text_q.put("None")
	##センシング
	#Sen_Process = Process(target = Sensing,args=[now_q])
	
	##フローグラフ
	#SFC_Process = Process(target = F_SFC,args=[now_q,next_q,SFC_to_Nav_q])

	##ナビゲーション
	#Nav_Process = Process(target = F_Nav,args=[now_q,next_q,SFC_to_Nav_q,text_q])

	##Nav_Window
	Nav_windows_Process = Process(target = Nav_Window_Control)
	Nav_windows_connect_Process = Process(target = Nav_Window_connect ,args=[text_q])

	#Sen_Process.start()
	
	#SFC_Process.start()

	#Nav_Process.start()

	Nav_windows_Process.start()

	Nav_windows_connect_Process.start()
if __name__=="__main__":
	Main()