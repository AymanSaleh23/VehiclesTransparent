import socket
from data_transfer_client import DataTransferClient


class DataTransferServer:
    def __init__(self, client):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = client

    def start(self, port):
        self.socket.bind(('localhost', port))
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            data = conn.recv(1024)
            response = self.process_and_send(data)
            conn.sendall(response.encode('utf-8'))
            conn.close()

    def process_and_send(self, data):
        # Process the received data and return a response
        self.client.send_data(data)
        return "Response to " + data.decode()
