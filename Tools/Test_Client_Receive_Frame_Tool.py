from comlib.com_socket import Client
received_frames = Client("192.168.1.11", 10080)

while True:
    received_frame = received_frames.receive_frame(4 * 1024)
