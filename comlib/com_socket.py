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
import pickle, cv2, struct

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
                msg_pickle = ''
                msg_pickle = pickle.dumps(self.to_send)

                """>>>      End Critical Section      <<<"""
                #   Send data which is stored in {self.to_send} to the connected client
                self.clt.sendall(msg_pickle)

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

    def send_frames(self):
        while True:
            try:
                client_socket, addr = self.s.accept()
                print('Connection from:', addr)
                if client_socket:
                    vid = cv2.VideoCapture(0)
                    while True:
                        img, frame = vid.read()
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        client_socket.sendall(message)
                        cv2.imshow('Sending...', frame)
                        key = cv2.waitKey(10)
                        if key == 13:
                            client_socket.close()
            except Exception:
                #   A debug print to console informs that an exception occurred
                print("> Server Exception connection")
                #   Simple wait for speed down the execution (optional and will be deleted in future)
                time.sleep(1)
                #   Retry the connection by call {self.send()} to accept a new connection request from the Client.
                self.send_frames()

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_created = True
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        self.data_recv = 0
        self.is_connected = False

        try:
            self.s.connect((self.ip, self.port))
        except Exception:
            print("> Connection Issue !")
            time.sleep(0.2)
            self.s.close()
            self.socket_created = False
            self.__init__(ip, port)

    def recv(self, size):
        if not self.socket_created:
            self.__init__(self.ip, self.port)
            if self.is_connected == False:
                try:
                    self.s.connect((self.ip, self.port))
                except Exception:
                    print("> Connection Issue !")
                    time.sleep(0.2)
                    self.s.close()
                    self.socket_created = False
                    self.__init__(self.ip, self.port)
        return self.s.recv(size)
    def receive_frame(self, size):

        """ Will be received from Socket"""

        while len(self.data) < self.payload_size:
            packet = self.recv(1024)
            if not packet: break
            self.data += packet
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self.recv(1024)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)
        #cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        return frame

    def recv_discrete(self):
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

        #   A client connection request using parameters server {ip} and application {port}.
        if self.is_connected == False:
            try:
                self.s.connect((self.ip, self.port))
                #   Infinite loop for receiving data continuously.
                while True:
                    """>>>      Critical Section      <<<"""
                    #   >>> @Issue Use Jason in data exchanging
                    #   Receive data from the socket and store it in object attribute {self.data_recv}.
                    raw_data_recv = b""
                    raw_data_recv += self.s.recv(1024)

                    decoded_data = pickle.loads(raw_data_recv)
                    self.data_recv = decoded_data
                    #   A debug print to console informs the received data from the connection
                    print("> Received: ", self.data_recv, end=" >> ")
                    #   A debug print to console informs the length of received data and its type
                    print(f"Length :{len(self.data_recv)} , type {type(self.data_recv)}")
                    self.s.sendall(b"> R:Received Successfully")
                    #   Check if no data received which happen if server crashed.
                    if len(self.data_recv) == 0:
                        #   Request a new connection from the same server {ip} address and {port} application
                        self.recv(1024)
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
                self.recv(1024)