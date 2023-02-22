import threading

from comlib.com_socket import Client, Server


class DataTransmitter(threading.Thread):
    """A Stand-alone module to receive data from different modules and serve them to requesters."""

    def __init__(self, source_host="127.0.0.1", source_port=10051,
                 server_host="127.0.0.1", server_port=10051, data_type="discrete"):
        super().__init__()
        self.source_host = source_host
        self.source_port = source_port

        self.server_host = server_host
        self.server_port = server_port

        self.data_type = data_type
        self.data_to_be_served = None

        self.receiver = Client(ip=self.source_host, port=self.source_port)
        self.server = Server(ip=self.server_host, port=self.server_port)

    def run(self):
        while True:
            if self.data_type == "discrete":
                self.data_to_be_served = self.receiver.recv_discrete()
                self.server.update_to_send(self.data_to_be_served)
                self.server.send()
            else:
                self.data_to_be_served = self.receiver.receive_frame(1024)
                self.server.update_to_send(self.data_to_be_served)
                self.server.send_frames()
