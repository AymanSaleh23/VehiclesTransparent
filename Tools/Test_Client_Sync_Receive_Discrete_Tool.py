from threading import Thread
c = Client(ip="192.168.1.11", port=10050)
t2 = Thread(target=c.recv_discrete, args=[1024])
t2 = Thread(target=c.rec, args=["192.168.1.11", 10080])
t2.setDaemon(True)
t2.start()
