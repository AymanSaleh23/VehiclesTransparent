
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

    def __init__(self, ip, port, timeout=3, name='sock_name'):
        """
        #   method documentation:
        #       Name:           __init__
        #       Parameters:     {self} object reference, {ip} and {port} with no default values.
        #       Description:    A class constructor to create object of Server and create a stream socket
        #                       With 5 devices maximum listen and initial value to send stored in {to_send}.
        #       Return:         None
        """
        self.ip, self.port, self.timeout, self.name = ip, port, timeout, name
        self.created, self.connected = False, False
        self.client_socket = socket.socket()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recreate()

    def recreate(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.ip, self.port))
        self.s.listen(5)
        self.connected = False
        self.created = True
        self.to_send = "initial..."
        return self.created

    def connect_mechanism(self, s_sock_name="Frame"):
        print(f"Socket: {s_sock_name}")
        try:

            self.s.settimeout(self.timeout)
            self.client_socket, self.addr = self.s.accept()
            self.connected = True
            print(f'Server {s_sock_name} Socket Successful Connection from: {self.addr}')

        except Exception:
            #   A debug print to console informs that an exception occurred
            print(f"> Server {s_sock_name} Socket Connection Error.")
            #   Simple wait for speed down the execution (optional and will be deleted in future)
            self.connected = False
            time.sleep(0.1)
        return self.connected

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
        while True:
            if not self.connected:
                self.connect_mechanism(f"{self.name} :[send()]")

            if self.connected:
                #   Infinite loop to send data which is stored in {to_send} to the connected receiver
                #   Exception handling for protect code from crashing if a connection fail occurred
                try:
                    """>>>      Critical Section      <<<"""
                    msg_pickle = ''
                    msg_pickle = pickle.dumps(self.to_send)

                    """>>>      End Critical Section      <<<"""
                    #   Send data which is stored in {self.to_send} to the connected client
                    self.client_socket.sendall(msg_pickle)

                    # receive responses.
                    #recv_data = self.s.recv(1024)
                    # Handle responses.
                    #notificationReply = recv_data.decode()
                    # notification reply
                    #print(notificationReply)
                    #   Simple wait for speed down the execution (optional and will be deleted in future)
                    time.sleep(2)
                    #   If exception occurred
                except Exception:
                    #   A debug print to console informs that an exception occurred
                    print(f"> Server Socket {self.name} Disconnected.")
                    #   Simple wait for speed down the execution (optional and will be deleted in future)
                    time.sleep(1)
                    self.connected = False
                    #   Retry the connection by call {self.send()} to accept a new connection request from the Client.
                    # self.send()

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

    def send_frame(self, frame_to_send):

        if not self.connected:

            self.connect_mechanism(f"{self.name} :[send_frame()]")

        if self.connected:
            try:
                if self.client_socket:
                    a = pickle.dumps(frame_to_send)
                    message = struct.pack("Q", len(a)) + a
                    self.client_socket.sendall(message)
                    cv2.imshow('SOCK_Sending This Frame...', frame_to_send)
                    key = cv2.waitKey(10)
                    if key == 13:
                        self.client_socket.close()
            except Exception:
                self.connected = False
                print("> Cant Send Frame.")
                time.sleep(0.01)
                #   Retry the connection by call {self.send()} to accept a new connection request from the Client.
                #self.send_frame(frame_to_send)


class Client:
    def __init__(self, ip, port, name='sock_name', timeout=3):
        self.ip, self.port, self.timeout, self.name = ip, port, timeout, name
        self.created, self.connected = False, False
        self.s = socket.socket()
        self.recreate()

    def recreate(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.created = True
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        self.data_recv = 0
        self.last_received_data = None
        return self.created

    def recv(self, size):

        if not self.connected:
            self.connect_mechanism(f"{self.name}: [recv()]")

        if self.connected:
            return self.s.recv(size)

    def receive_all(self, size):

        """ Will be received from Socket"""
        while not self.connected:
            self.connect_mechanism(f"{self.name}:[receive_frame()]")

        if self.connected:
            try:
                while len(self.data) < self.payload_size:
                    packet = self.recv(4*size)
                    if not packet:
                        break
                    self.data += packet
                packed_msg_size = self.data[:self.payload_size]
                self.data = self.data[self.payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(self.data) < msg_size:
                    self.data += self.recv(4*size)
                encoded_data = self.data[:msg_size]
                self.data = self.data[msg_size:]
                decoded_data = pickle.loads(encoded_data)
                self.last_received_data = decoded_data
                return decoded_data

            except Exception:
                self.connected = False
                #   A debug print to console shows the error
                print("> Receiver Frame Socket Connection Error.")
                #   A small wait for a new connection request
                self.s.close()
                self.recreate()
                time.sleep(0.5)

        return self.last_received_data

    def recv_discrete(self):
        """
        #   method documentation:
        #       Name:           recv
        #       Parameters:     {self} object reference, ip address of the server {ip}, application port {port}.
        #       Description:    Method to request connection from the server using the {ip}, {port},
        #                       Support exception handling and reconnect if exception occurred as a recursion feature.
        #       Return:         None
        """
        #   Exception handling for protect code from crashing if a connection fail occurred.
        #   A client connection request using parameters server {ip} and application {port}.
        self.data_recv = [[-1, 0]*3, [0], [0], [0]]

        if not self.connected:
            self.connect_mechanism(f"{self.name}: [recv_discrete()]")

        if self.connected:
            try:
                """>>>      Critical Section      <<<"""
                #   >>> @Issue Use Jason in data exchanging
                #   Receive data from the socket and store it in object attribute {self.data_recv}.
                raw_data_recv = b""
                raw_data_recv += self.s.recv(1024)

                decoded_data = pickle.loads(raw_data_recv)
                self.data_recv = decoded_data
                #   A debug print to console informs the received data from the connection
                # print("> Received: ", self.data_recv, end=" >> ")
                #   A debug print to console informs the length of received data and its type
                # print(f"Length :{len(self.data_recv)} , type {type(self.data_recv)}")
                #self.s.sendall(b"> R:Received Successfully")
                #   Check if no data received which happen if server crashed.
                if self.data_recv is None:
                    self.data_recv = [[-1, 0] * 3, [0], [0], [0]]
                    print(f"> Receiver Discrete Socket No Received data: {self.data_recv}")
                """>>>      End Critical Section      <<<"""
                time.sleep(1)

            except Exception:
                self.connected = False
                #   A debug print to console shows the error
                print("> Receiver Discrete Socket Connection Error.")
                #   A small wait for a new connection request
                self.s.close()
                self.recreate()
                self.data_recv = [[-1, 0] * 3, [0], [0], [0]]
                time.sleep(0.6)
        return self.data_recv

    def connect_mechanism(self, r_sock_tye="Frame"):
        if not self.connected:
            print(f"Socket: {self.name}")
            try:
                self.s.settimeout(self.timeout)
                self.s.connect((self.ip, self.port))
                self.connected = True
                print(f' Client {r_sock_tye} Socket Successful Connection ')

            except Exception:
                print(f"> Client {r_sock_tye} Socket Connection Error.")
                self.connected = False
                time.sleep(0.1)
