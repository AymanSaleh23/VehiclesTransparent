import time
from comlib.com_socket import *
import cv2

serv = Server(ip="127.0.0.1", port=10080)
vid = cv2.VideoCapture(0)

while True:
    img, frame = vid.read()
    serv.send_frame(frame)
