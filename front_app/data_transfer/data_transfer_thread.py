import threading


class DataTransferThread(threading.Thread):
    def __init__(self, server, port):
        super().__init__()
        self.server = server
        self.port = port

    def run(self):
        self.server.start(self.port)
