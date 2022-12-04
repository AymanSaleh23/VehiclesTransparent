# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 20:30:16 2022

@author: as292
"""

import socket, threading, time

class server:
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
                print("Excpetion connection")
            
class client:
    def __init__(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data=None
        
    def rec(self, ip, port):
        while True:
            try:
                self.s.connect((ip, port))
                self.data=self.s.recv(1024)
                print("Received : "+ self.data.decode("utf-8"))
                
            except Exception:
                print("Excpetion connection")   
        self.s.close()



###########     APP      ##############
s1 = server("192.168.1.11",65022)
t1 = threading.Thread(target=s1.send, args = ['sssss'])
t1.setDaemon(True)
t1.start()

c = client()
t2 = threading.Thread(target=c.rec, args=["192.168.1.11",65022])
t2.setDaemon(True)
t2.start()
