
# socket サーバを作成

import socket

def Server(IP,Port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# IPアドレスとポートを指定
		s.bind((IP, Port))
		# 1 接続
		s.listen(1)
		# connection するまで待つ
		while True:
			# 誰かがアクセスしてきたら、コネクションとアドレスを入れる
			conn, addr = s.accept()
			with conn:
				while True:
					# データを受け取る
					data = conn.recv(1024)
					if not data:
						break
					print('data : {}, addr: {}'.format(data, addr))
					# クライアントにデータを返す(b -> byte でないといけない)
					data = input("HOW")
					#data ="S1"
					conn.sendall(data.encode('utf-8'))


if __name__ =="__main__":
	Server('127.0.0.1',50007)