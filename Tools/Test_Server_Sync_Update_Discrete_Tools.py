from threading import Thread
from comlib.com_socket import Server
import time
s1 = Server(ip="192.168.1.11", port=20029, name="Socket_Sender")
t1 = Thread(target=s1.send)
t1.setDaemon(True)
t1.start()
for i in range(0, 1000):
    s1.update_to_send(i)
    time.sleep(0.3)
s1.update_to_send("9834732.52")
s1.update_to_send([123, 2323, 353, 433, "43532", 292.32])
s1.update_to_send({"add": [123, 2323, 353, 433], "1": ["43532", 292.32]})
