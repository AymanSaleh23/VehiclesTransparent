from communication.com_socket import Server
import cv2, pickle, struct


s = Server("127.0.0.1", 10050)

vid = cv2.VideoCapture(0)
while(vid.isOpened()):
    img,frame = vid.read()
    cv2.imshow('SOCK_Sending This Frame...', frame)
    s.send_all(frame)
    key = cv2.waitKey(10)
