# lets make the client code
"""	Importing the needed packages	"""
import socket,cv2, pickle,struct
""""	Class named clientClass		""""
class clientClass:

    """" class constructor """
    def __init__(self):
        """
	Object attributes  
		host_ip, port, payload_size, data, client_socket
	"""
	self.host_ip = '192.168.1.11' # paste your server ip address here
        self.port = 65000
        self.payload_size = struct.calcsize("Q")
        self.data = b""
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((self.host_ip,self.port)) # a tuple
        
    """ Dunder function for enable calling by object itself	"""
    def __call__(self):
	'''	Logic for repeatly get from camera	'''
        while True:
        	while len(self.data) < self.payload_size:
        		packet = self.client_socket.recv(4*1024) # 4K
        		if not packet: break
        		self.data+=packet
        	packed_msg_size = self.data[:self.payload_size]
        	self.data = self.data[self.payload_size:]
        	msg_size = struct.unpack("Q",packed_msg_size)[0]
        	
        	while len(self.data) < msg_size:
        		self.data += self.client_socket.recv(4*1024)
        	frame_data = self.data[:msg_size]
        	self.data  = self.data[msg_size:]
        	frame = pickle.loads(frame_data)
        	cv2.imshow("RECEIVING VIDEO",frame)
        	key = cv2.waitKey(1) & 0xFF
        	if key  == ord('q'):
        		break
        self.client_socket.close()
	
# for test only (should be cleared in future)
c = clientClass()
c()
