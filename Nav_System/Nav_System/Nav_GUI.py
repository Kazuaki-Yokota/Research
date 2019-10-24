import wx

import socket
import time


class Client:
	def __init__(self):
		HOST = "localhost"
		PORT =10001
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST, PORT))

class MainFrame(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,title = "Nav",size = (500,500))

		p = wx.Panel(self)
		self.text = wx.TextCtrl(p,-1,"",size=(200,200))
		btn1 = wx.Button(p,-1,"HELP")
		btn2 = wx.Button(p,-1,"NEXT")

		btn1.Bind(wx.EVT_BUTTON,self.Connect)
		btn2.Bind(wx.EVT_BUTTON,self.Send)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.text,0,wx.ALL,5)
		sizer.Add(btn1,0,wx.ALL,5)

		p.SetSizer(sizer)
		self.working = 0

	def Send(self,event):
		self.data = self.text.GetValue().encode('utf-8')
		print(type(self.data))
	def Connect(self,event):
		self.data = None
		self.answ = None

		if not self.working:
			self.working =1
			self.need_abort = 0

			self.c = Client()

			while 1:
				time.sleep(0.1)
				wx.Yield()

				if self.need_abort:
					break
				if self.data != None:
					self.c.s.send(self.data)
					self.data = None
					self.answ = self.c.s.recv(1024)
				if self.answ != None:
					self.text.SetValue(self.answ)
					self.answ = None
			self.working = 0

	def Disconnect(self,event):
		if self.working:
			self.c.s.close()
			self.need_abort = 1

class MainApp(wx.App):
	def OnInit(self):
		self.frame = MainFrame(None,-1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__=="__main__":
	app = MainApp(0)
	app.MainLoop()