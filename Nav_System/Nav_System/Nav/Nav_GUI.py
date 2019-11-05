import wx

import socket
import time


class Client:
	def __init__(self):
		HOST = "localhost"
		PORT =50006
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST, PORT))
		
class MainFrame(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,title = "Nav",size = (500,500))

		p = wx.Panel(self)
		self.text = wx.TextCtrl(p,-1,"",size=(500,200),style = wx.TE_MULTILINE)

		font  = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
		self.text.SetFont(font)
		btn1 = wx.Button(p,-1,"Help")
		btn2 = wx.Button(p,-1,"NEXT")


		
		btn1.Bind(wx.EVT_BUTTON,self.Connect)
		#btn2.Bind(wx.EVT_BUTTON,self.Send)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.text,0,wx.ALL,5)
		sizer.Add(btn1,0,wx.ALL,5)
		sizer.Add(btn2,0,wx.ALL,5)
		p.SetSizer(sizer)
		self.working = 0

	def Connect(self,event):
		IP = "localhost"
		Port =50006
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
			s.connect((IP,Port))
			self.answ =s.recv(1024)
			print("Nav: ",self.answ.decode("utf-8"))
			if self.answ != None:
					self.text.Clear()
					self.text.SetValue(self.answ)
					self.answ = None

			print("Close Nav_GUI of TCP Client")
			s.sendall(b"end")
			s.close()
			

class MainApp(wx.App):
	def OnInit(self):
		self.frame = MainFrame(None,-1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__=="__main__":
	app = MainApp(0)
	app.MainLoop()