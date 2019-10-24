from multiprocessing import Process, Value, Array,Queue

from time import sleep
def f(n,q):
	while True:
		sleep(1)
		print("A",n.value)
		
		q.put(["Hello"])
		q.put(["AAA"])
		q.put(["AAA"])
def ff(nn,q):
	
	while True:
		sleep(3)
		nn.value += nn.value
		print("B",nn.value)
		print(q.get())
		print(q.get())
if __name__=="__main__":


	count = Value("i")
	count.value = 1

	q = Queue()
	p = Process(target= f, args=[count,q])
	pp = Process(target = ff, args=[count,q])

	p.start()
	pp.start()


	f
	#pp.join()