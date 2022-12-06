
#essential packages
import socket, time

class Server:
    def __init__(self, ip, port):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, port))          
        self.s.listen(5)
        
    def send (self,data):
        while True:
            try:
                self.clt, self.adr =self.s.accept()
                print(f"Connection to {self.adr}established")  
                self.clt.sendall(bytes(data,"utf-8 "))
            except Exception:
                print("Server Excpetion connection")
        self.s.close()
class Client:
    def __init__(self):
        
        self.data=None
        
    def rec(self, ip, port):
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((ip, port))
                self.data=self.s.recv(1024)
                print("Received : " + self.data.decode("utf-8"))
                self.s.close()  
                time.sleep(1)
            except Exception:
                print("Client Excpetion connection")

"""
###########     Test      ##############
s1 = Server("192.168.1.11",65000)
t1 = threading.Thread(target=s1.send, args = ['sssss'])
t1.setDaemon(True)
t1.start()

c = Client()
t2 = threading.Thread(target=c.rec, args=["192.168.1.11",65000])
t2.setDaemon(True)
t2.start()
"""
