import time

from comlib.com_socket import Client
received_frames = Client(ip='192.168.1.11', port=10050)

while True:
    received_frame = received_frames.receive_frame(1024)
    time.sleep(.5)
