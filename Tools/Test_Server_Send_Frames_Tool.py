from comlib.com_socket import Server
import cv2, pickle, struct

s = Server("192.168.1.11", 10050)

vid = cv2.VideoCapture(0)
while(vid.isOpened()):
    img,frame = vid.read()
    cv2.imshow('SOCK_Sending This Frame...', frame)
    s.send_frame(frame)
    key = cv2.waitKey(10)
