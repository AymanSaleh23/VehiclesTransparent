from comlib.com_socket import Client
import time
c = Client(ip="192.168.1.11", port=10080)
while True:
    print(c.recv_discrete())
    time.sleep(1)

# from threading import Thread
# t2 = Thread(target=c.recv_discrete, args=[])
# t2.setDaemon(True)
# t2.start()
# while True:
#     if c.is_connected == True:
#         print(c.data_recv)
#         time.sleep(1)