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
import pickle, struct, imutils, json

class Server:
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

    def __init__(self, ip, port):
        """
        #   method documentation:
        #       Name:           __init__
        #       Parameters:     {self} object reference, {ip} and {port} with no default values.
        #       Description:    A class constructor to create object of Server and create a stream socket
        #                       With 5 devices maximum listen and initial value to send stored in {to_send}.
        #       Return:         None
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((ip, port))
        self.s.listen(5)
        self.to_send = "initial..."


    def send(self):
        """
        #   method documentation:
        #       Name:           send
        #       Parameters:     {self} object reference.
        #       Description:    Method to accept a connection request from any client need to be handled.
        #                       Support exception handling and reconnect if exception occurred as a recursion feature.
        #       Return:         None
        #  >>>> Issue:          Only update String values,
        #                       can't update the object attribute {self.to_send} in runtime if socket is running
        """
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

                """>>>      Critical Section      <<<"""
                msg_json = ''
                msg_json = json.dumps(self.to_send)

                """>>>      End Critical Section      <<<"""
                #   Send data which is stored in {self.to_send} to the connected client
                self.clt.sendall(bytes(msg_json, "UTF-8"))

                # receive responses.
                #recv_data = self.s.recv(1024)
                # Handle responses.
                #notificationReply = recv_data.decode()
                # notification reply
                #print(notificationReply)
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
    def update_to_send(self, new_data):
        """
        #   method documentation:
        #       Name:           send
        #       Parameters:     {self} object reference.
        #       Description:    Method to accept a connection request from any client need to be handled.
        #                       Support exception handling and reconnect if exception occurred as a recursion feature.
        #       Return:         None
        #  >>>> Issue:          Only update String values,
        #                       can't update the object attribute {self.to_send} in runtime if socket is running
        """
        #>>>      Critical Section      <<<
        self.to_send = new_data
        #>>>      End Critical Section      <<<

class Client:
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

    def __init__(self):
        """
        #   method documentation:
        #       Name:           __init__
        #       Parameters:     {self} object reference.
        #       Description:    A class constructor to create object of Client and create a stream socket to receive data
        #                       and store it in {data}
        #       Return:         None
        """
        #   Create a socket to be receiver
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   Boolean variable for check if socket is created
        self.socket_created = True
        #   An object attribute to store the received value from the socket connection
        self.data_recv = None


    def recv(self, ip, port):
        """
        #   method documentation:
        #       Name:           recv
        #       Parameters:     {self} object reference, ip address of the server {ip}, application port {port}.
        #       Description:    Method to request connection from the server using the {ip}, {port},
        #                       Support exception handling and reconnect if exception occurred as a recursion feature.
        #       Return:         None
        """
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
                """>>>      Critical Section      <<<"""
                #   >>> @Issue Use Jason in data exchanging
                #   Receive data from the socket and store it in object attribute {self.data_recv}.
                raw_data_recv = self.s.recv(1024)
                decoded_data = raw_data_recv.decode("UTF-8")
                self.data_recv = json.loads(decoded_data)
                #   A debug print to console informs the received data from the connection
                print("> Received: " + self.data_recv, end=" >> ")
                #   A debug print to console informs the length of received data and its type
                print(f"Length :{len(self.data_recv)} , type {type(self.data_recv)}")
                self.s.sendall(b"> R:Received Successfully")
                #   Check if no data received which happen if server crashed.
                if len(self.data_recv) == 0:
                    #   Request a new connection from the same server {ip} address and {port} application
                    self.recv(ip, port)
                """>>>      End Critical Section      <<<"""
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
#from threading import Thread
#s1 = Server("192.168.1.11", 10080)
#s1.send()
#t1 = Thread(target=s1.send)
#t1.setDaemon(True)
#t1.start()
#
#c = Client()
#t2 = Thread(target=c.recv, args=["192.168.1.11", 10080])
#t2 = Thread(target=c.rec, args=["192.168.1.11", 10080])
#t2.setDaemon(True)
#t2.start()

#s1.update_to_send("9834732.52")
#s1.update_to_send([123,2323,353,433,"43532",292.32])
