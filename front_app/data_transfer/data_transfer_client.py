import socket


class DataTransferClient:
    def __init__(self, remote_host, remote_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_host = remote_host
        self.remote_port = remote_port

    def send_data(self, data):
        self.socket.connect((self.remote_host, self.remote_port))
        self.socket.sendall(data.encode('utf-8'))
        response = self.socket.recv(1024)
        self.socket.close()
        return response
