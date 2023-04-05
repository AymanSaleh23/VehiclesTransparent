
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
        if not self.connected:
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

    def send_all(self, dict_to_send):

        if not self.connected:

            self.connect_mechanism(f"{self.name} :[send_frame()]")

        if self.connected:
            try:
                if self.client_socket:
                    a = pickle.dumps(dict_to_send)
                    message = struct.pack("Q", len(a)) + a
                    self.client_socket.sendall(message)
                    # cv2.imshow('SOCK_Sending This Frame...', dict_to_send["F"])
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

    def receive_all(self, size):

        """ Will be received from Socket"""
        while not self.connected:
            self.connect_mechanism(f"{self.name}:[receive_all()]")
            time.sleep(0.7)

        if self.connected:
            try:
                while len(self.data) < self.payload_size:
                    packet = self.s.recv(4*size)
                    if not packet:
                        break
                    self.data += packet
                packed_msg_size = self.data[:self.payload_size]
                self.data = self.data[self.payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(self.data) < msg_size:
                    self.data += self.s.recv(4*size)
                encoded_data = self.data[:msg_size]
                self.data = self.data[msg_size:]
                decoded_data = pickle.loads(encoded_data)
                # print(f'decoded_data["D"]: {decoded_data["D"]}')
                # self.last_received_data = decoded_data["F"], decoded_data["D"]
                return decoded_data["F"], decoded_data["D"]

            except Exception:
                self.connected = False
                #   A debug print to console shows the error
                print("> Receiver Frame Socket Connection Error.")
                #   A small wait for a new connection request
                self.s.close()
                self.recreate()
                time.sleep(0.5)

        return None, None

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
        return self.connected


class DataHolder:
    def __init__(self):
        self.frame_stack = []
        self.discrete_stack = []

    def get_frame(self):
        if len(self.frame_stack) != 0:
            return self.frame_stack[len(self.frame_stack)-1]
        else:
            pass

    def get_discrete(self):
        if len(self.discrete_stack) != 0:
            return self.discrete_stack[len(self.discrete_stack) - 1]
        else:
            pass

    def set_frame(self, frame):
        if frame is not None:
            self.frame_stack.append(frame)
        else:
            print("No Frame to set in Data Holder")

    def set_discrete(self, discrete):
        if discrete is not None:
            self.discrete_stack.append(discrete)
        else:
            print("No Discrete to set in Data Holder")

    def reset_discrete(self):
        if len(self.discrete_stack) != 0:
            self.discrete_stack = self.discrete_stack[len(self.discrete_stack)-1]

