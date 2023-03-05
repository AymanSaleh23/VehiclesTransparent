import time

from comlib.com_socket import Client
received_frames = Client(ip='192.168.1.11', port=10050, name="Frame Receive")

while True:
    received_frame = received_frames.receive_all(1024)
