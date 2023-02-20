from data_transfer_thread import DataTransferThread
from data_transfer_server import DataTransferServer
from data_transfer_client import DataTransferClient

# Configuration
LISTEN_PORT = 5000
TARGET_REMOTE_PORT = 6000
TARGET_REMOTE_HOST = "192.168.1.10"

# Create a DataTransferClient object and send data to a remote machine's socket
client = DataTransferClient(TARGET_REMOTE_HOST, TARGET_REMOTE_PORT)
response = client.send_data("Hello, world!")
print(response)

# Create a DataTransferServer object and start the listening thread
server = DataTransferServer(client)
thread = DataTransferThread(server, LISTEN_PORT)
thread.start()
