from threading import Thread
from comlib.com_socket import Server
s1 = Server("192.168.1.11", 10080)
t1 = Thread(target=s1.send)
t1.setDaemon(True)
t1.start()
s1.update_to_send("9834732.52")
s1.update_to_send([123, 2323, 353, 433, "43532", 292.32])
s1.update_to_send({"add": [123, 2323, 353, 433], "1": ["43532", 292.32]})
