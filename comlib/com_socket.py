"""
####################################################
##############     DEC, 20th 2022     ##############
##############      v. 1.1.0          ##############
####################################################

File Descriptoin:
    - Second version of socket File in communication module
    - Issues:
        - A bug with disconnecting Server while client is connected.
        - A bug with changing the server socket value to send in background with threads.
"""

#   essential packages
import socket, time

"""
    Class:
      NAME:             Server
      DESCRIPTION:      A class to make dealing with Server Sockets easy and object oriented 
                        Provide a high dynamic code for any future use
      CLASS ATTRIBUTE:  None
      DUNDER METHODS:   __init__
      METHODS:          send
      MAX NO. Objects:  None      
"""
class Server:
    #   method documentation:
    #       Name:           __init__
    #       Parameters:     {self} object reference, {ip} and {port} with no default values.
    #       Description:    A class constructor to create object of Server and create a stream socket
    #                       With 5 devices maximum listen and initial value to send stored in {to_send}.
    #       Return:         None
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((ip, port))
        self.s.listen(5)
        self.to_send = "initial..."

    #   method documentation:
    #       Name:           send
    #       Parameters:     {self} object reference.
    #       Description:    Method to accept a connection request from any client need to be handled.
    #                       Support exception handling and reconnect if exception occurred as a recursion feature.
    #       Return:         None
    #  >>>> Issue:          can't update the object attribute {self.to_send} in runtime if socket is running
    def send(self):

        #   server socket accepts the connection request,
        #   saves the returned connection socket and client address in {self.clt}, {self.adr}
        self.clt, self.adr = self.s.accept()

        #   A debug print to console indicates a new connection is accepted
        print("> New Connection.")

        #   Infinite loop to send data which is stored in {to_send} to the connected receiver
        while True:
            #   Exception handling for protect code from crashing if a connection fail occurred
            try:
                #   A debug print to console informs the connected address which is saved in {self.addr}
                print(f"> Device with address \"{self.adr}\" connected.")
                #   Send data which is stored in {self.to_send} to the connected client
                self.clt.sendall(bytes(self.to_send, "utf-8 "))

                #   Simple wait for speed down the execution (optional and will be deleted in future)
                time.sleep(1)
            #   If exception occurred
            except Exception:
                #   A debug print to console informs that an exception occurred
                print("> Server Exception connection")
                #   Simple wait for speed down the execution (optional and will be deleted in future)
                time.sleep(1)
                #   Retry the connection by call {self.send()} to accept a new connection request from the Client.
                self.send()
"""
    Class:
      NAME:             Client
      DESCRIPTION:      A class to make dealing with Client Sockets easy and object oriented 
                        Provide a high dynamic code for any future use
      CLASS ATTRIBUTE:  None
      DUNDER METHODS:   __init__
      METHODS:          receive
      MAX NO. Objects:  None      
"""
class Client:
    #   method documentation:
    #       Name:           __init__
    #       Parameters:     {self} object reference.
    #       Description:    A class constructor to create object of Client and create a stream socket to receive data
    #                       and store it in {data}
    #       Return:         None
    def __init__(self):
        #   Create a socket to be receiver
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   Boolean variable for check if socket is created
        self.socket_created = True
        #   An object attribute to store the received value from the socket connection
        self.data_recv = None

    #   method documentation:
    #       Name:           recv
    #       Parameters:     {self} object reference, ip address of the server {ip}, application port {port}.
    #       Description:    Method to request connection from the server using the {ip}, {port},
    #                       Support exception handling and reconnect if exception occurred as a recursion feature.
    #       Return:         None
    def recv(self, ip, port):
        if not self.socket_created:
            #   Create a new socket to be receiver
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #   Counter for check number of created sockets
            self.socket_created = True
        #   Exception handling for protect code from crashing if a connection fail occurred.
        try:
            #   A client connection request using parameters server {ip} and application {port}.
            self.s.connect((ip, port))

            #   Infinite loop for receiving data continuously.
            while True:
                #   Receive data from the socket and store it in object attribute {self.data_recv}.
                self.data_recv = self.s.recv(1024)
                #   A debug print to console informs the received data from the connection
                print("> Received: " + self.data_recv.decode("utf-8"))
                #   A debug print to console informs the length of received data and its type
                print(f"Length :{len(self.data_recv.decode('utf-8'))} , type {type(self.data_recv.decode('utf-8'))}")

                #   Check if no data received which happen if server crashed.
                if len(self.data_recv.decode('utf-8')) == 0:
                    #   Request a new connection from the same server {ip} address and {port} application
                    self.recv(ip, port)
        #   If exception occurred
        except Exception:
            #   A debug print to console shows the error
            print("> Connection Issue !")
            #   A small wait for a new connection request
            time.sleep(0.2)
            #   Close the failed connection
            self.s.close()
            #   Update the status of the boolean variable indicates the socket is closed
            self.socket_created = False
            #   Request a new connection from the same server {ip} address and {port} application
            self.recv(ip, port)

# ###########     Test      ##############
"""import threading
s1 = Server("192.168.1.11", 10080)
#s1.send()
t1 = threading.Thread(target=s1.send)
t1.setDaemon(True)
t1.start()

c = Client()
t2 = threading.Thread(target=c.recv, args=["192.168.1.11", 10080])
#t2 = threading.Thread(target=c.rec, args=["192.168.1.11", 10080])
t2.setDaemon(True)
t2.start()
"""