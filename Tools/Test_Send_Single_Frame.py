import time
from comlib.com_socket import *
import cv2

serv = Server(ip="192.168.1.11", port=10050)
vid = cv2.VideoCapture(0)

while True:
    img, frame = vid.read()
    serv.send_all(frame)
