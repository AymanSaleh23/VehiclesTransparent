#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import cv2
import sys


# ## Object Detection Class

# In[2]:


class ObjectDetection:
    def __init__(self):
       
        print("Loading Object Detection")
        print("Running YOLOv5n")
        self.model = torch.hub.load('yolov5', 'yolov5n', source= 'local')
        self.model.classes_to_detect = [2, 5, 7]
        self.threshold = 0.6
#         self.x1, self.y1, self.x2, self.y2, self.text, self.conf = 0,0,0,0,'',0.0 

    def detect(self, frame):
        self.x1, self.y1, self.x2, self.y2, self.text, self.conf = 0,0,0,0,'',0.0 
        self.result = self.model(frame)
        self.df = self.result.pandas().xyxy[0]
        print('===========================================')
        print(self.df)
        if(not self.df.empty):
            # to get Just only one car. If you want to get all cars, just loop on index in detected_vehicles_data_frame.index.
            self.firstCarIndex = self.df.index[0]
            
            if(self.df['confidence'][self.firstCarIndex] >= self.threshold):
                self.x1, self.y1 = int(self.df['xmin'][self.firstCarIndex]), int(self.df['ymin'][self.firstCarIndex])
                self.x2, self.y2 = int(self.df['xmax'][self.firstCarIndex]), int(self.df['ymax'][self.firstCarIndex])
                self.label = self.df['name'][self.firstCarIndex]
                self.conf  = self.df['confidence'][self.firstCarIndex]
                self.text = self.label + ' , ' + str(self.conf.round(decimals= 2))
                
        return self.x1, self.y1, self.x2, self.y2, self.text, self.conf


# ## Object Tracking Class

# In[3]:


class ObjectTracking:
    def __init__(self):
       
        print("Loading Object Tracking")
        print("CV models for Tracking")
        self.tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.tracker_type = self.tracker_types[7]
        self.tracker = 0
        if self.tracker_type == 'BOOSTING':
            self.tracker = cv2.TrackerBoosting_create()
        elif self.tracker_type == 'MIL':
            self.tracker = cv2.TrackerMIL_create()
        elif self.tracker_type == 'KCF':
            self.tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == 'TLD':
            self.tracker = cv2.TrackerTLD_create()
        elif self.tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == 'GOTURN':
             self.tracker = cv2.TrackerGOTURN_create()
        elif self.tracker_type == 'MOSSE':
            self.tracker = cv2.TrackerMOSSE_create()
        elif self.tracker_type == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()


    def track_init(self,frame, bbox):
        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(frame, bbox)
        return ok
    
    def update_track(self,frame):
        # Update tracker
        ok, bbox = self.tracker.update(frame)
        bbox = bbox  if(bbox[0] > 0 and bbox[1]) else (0,0,1,1)
        return ok, bbox
    
     


# In[4]:


def run():
    import socket
    import cv2
    import pickle
    import struct
    import imutils
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(("192.168.1.11",10080))
    data = b""
    # Q: unsigned long long integer(8 bytes)
    payload_size = struct.calcsize("Q")
    # Some Initial  Parameters
    tracking_area = 0
    width, height = 700,380  # ReSize the Frame
    x1,y1,x2,y2,text,conf,bbox,fps = 0,0,0,0,'',0,0,0 # Initialize The x1,y1,x2,y2,text,conf,bbox
    timerLimit = 10 # periodic timer To make a new detection
    periodic_timer = 0 # Flag To Run Detection After 25 Frame
    isFirstFrame = True # Flag To Run Detection For The First Frame 
    streamedData  = None
    C_X,C_Y,tolerance =  int(width/2 ), int(height/2),120

    # Detection And Tracking Instances
    od = ObjectDetection()
    ot = ObjectTracking()
    
    video = cv2.VideoCapture("video2.mp4") # Read video
    
    
    S_video = cv2.VideoCapture("video2.mp4") # Read Straemed video

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    
    while True:
        ok,frame = video.read()    #read Frame by frame
        frame= cv2.resize(frame, (width, height))  # Resize the Frame
        

#         logo = cv2.imread('Valeo.png')  #  Just Image Right Now , It will be a video stream from socket 

        # Exit if video not opened.
        if not ok:
            print ('Cannot read video file')
            sys.exit()
            break
        
        else:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            S_frame = pickle.loads(frame_data)
            streamedData = S_frame
        # Adjust ROI 'Region of interest'
        cv2.rectangle(frame,(C_X-tolerance,C_Y), (C_X+tolerance,height), (255,255,255),2)
        cv2.circle(frame, (C_X,C_Y), radius=0, color=(0, 0, 255), thickness=5)
        ROI_Frame = frame[C_Y:height,C_X-tolerance:C_X+tolerance]

        # Detect the Car at the first frame only
        if(isFirstFrame):
            x1,y1,x2,y2,text,conf = od.detect(ROI_Frame) # get x1,y1,x2,y2 at The ROI_Frame
            # Mapping The  x1,y1,x2,y2 from ROI_Frame to The Original Frame
            
            if(conf != 0):
                w = abs(x1 - x2)
                h = abs(y1 - y2)
                # Define an initial bounding box
                bbox = (x1, y1, w, h)
                ok = ot.track_init(ROI_Frame, bbox)
                print('############### GET A Car From The First Frame  ###############')
                print('BBOX : ', bbox)
                print('###############################################################')
                
            periodic_timer = 0
            isFirstFrame = False
            print('********************************************* First Frame Detection')

        else:
            if(periodic_timer % timerLimit == 0 or conf == 0 ):
                x1,y1,x2,y2,text,conf = od.detect(ROI_Frame)
                if(conf != 0):
                    w = abs(x1 - x2)
                    h = abs(y1 - y2)
                    bbox = (x1, y1, w, h)      # Define the bounding box
                    ok = ot.track_init(ROI_Frame, bbox)
                    print('############### GET A Car After A Periodic Timer ###########')
                    print('BBOX : ', bbox)
                    print('############################################################')

                if(periodic_timer % timerLimit == 0):
                    periodic_timer = 0
                print('*********************************************** Repeat Detection')

        periodic_timer = periodic_timer + 1     # Counter The Period_counter Flag

        print('===================== TIME : ',periodic_timer,'========================')

        # No detected Cars 'conf = 0 '
        if(conf == 0):
            cv2.putText(frame, "No Detected Cars OR Holding After Timer period ", (23, 23), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
        #Start Trackng
            timer = cv2.getTickCount()   # Start timer To Calculate FPS
            
            ok, bbox = ot.update_track(ROI_Frame)  # Update tracker

            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);  # Calculate Frames per second (FPS)

            if ok:   # Tracking success
                p1 = (int(bbox[0]), int(bbox[1])) # (x1,y1)
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])) #  (x2,y2)
                cv2.rectangle(ROI_Frame, p1, p2, (255,0,0),3)  # Blue Rectangel For Tracking
                tracking_area = ROI_Frame[ bbox[1]: (bbox[1]+bbox[3]) ,bbox[0]: (bbox[0]+bbox[2])]  # The Tracked Part Of The original Frame
                print('########################################## tracking_area SHAPE : ',tracking_area.shape[:2])
                streamedData = cv2.resize(streamedData, (tracking_area.shape[1], tracking_area.shape[0])) if (tracking_area.shape[1] !=0 or tracking_area.shape[0] != 0) else cv2.resize(streamedData, (1, 1))  # Resize the streamedData
                print('########################################### streamed Data SHAPE : ',streamedData.shape[:2])
                ROI_Frame[ bbox[1]: (bbox[1]+bbox[3]) ,bbox[0]: (bbox[0]+bbox[2])] = streamedData if (tracking_area.shape[0] != 0 or tracking_area.shape[1]!=0) else frame[ bbox[1]: (bbox[1]+bbox[3]) ,bbox[0]: (bbox[0]+bbox[2])]

                print('################### GET A Car  #####################')
                print('BBOX : ', bbox)
                print('####################################################')
            else:
                print('++++++++++++++++ Tracking Failed +++++++++++++++++')
        # End Traking
            print("===================")
            print("Metadata :  x1: " , x1,' , y1: ',y1,' , x2: ',x2,' , y2: ',y2,' , text_conf: ',text )
            print("===================")
            cv2.rectangle(ROI_Frame, (x1, y1), (x2, y2), (0, 255,255), 2)
            cv2.putText(ROI_Frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        x1,y1,x2,y2,text = 0,0,0,0,''
        cv2.putText(frame,"{} {}".format("Frame NO : ", periodic_timer), (23, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (23,70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,255,255), 2);
        cv2.imshow('Frame' , frame)
        S_frame= cv2.resize(S_frame, (500, 350))   # Resize the Streamed Video just To preview it as a result Data
        cv2.imshow('Streamed Data',S_frame)
        cv2.imshow("Tracking_area",tracking_area) 
#         cv2.waitKey(0)
#          Exit if ESC pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE 
            break

    video.release()
    cv2.destroyAllWindows()


# In[5]:


run()


# In[ ]:




