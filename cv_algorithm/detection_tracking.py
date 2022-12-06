import torch
import cv2
import sys
from mathematics import mathlib

########################################################################################################################
#######################################     Object Detection    ########################################################
########################################################################################################################

class ObjectDetection:
    def __init__(self):
        print("Loading Object Detection")
        print("Running YOLOv5n")
        self.model = torch.hub.load('yolov5', 'yolov5n', source= 'local')
        self.model.classes = [2,5,7]
        self.threshold = 0.6
        #   self.x1, self.y1, self.x2, self.y2, self.text, self.conf = 0,0,0,0,'',0.0

    def detect(self, frame):
        self.x1, self.y1, self.x2, self.y2, self.text, self.conf = 0,0,0,0,'',0.0 
        self.result = self.model(frame)
        self.df = self.result.pandas().xyxy[0]
        print('===========================================')
        print(self.df)
        if(not self.df.empty):
            # to get Just only one car. If you want to get all cars, just loop on index in df.index.
            self.firstCarIndex = self.df.index[0]
            
            if(self.df['confidence'][self.firstCarIndex] >= self.threshold):
                self.x1, self.y1 = int(self.df['xmin'][self.firstCarIndex]), int(self.df['ymin'][self.firstCarIndex])
                self.x2, self.y2 = int(self.df['xmax'][self.firstCarIndex]), int(self.df['ymax'][self.firstCarIndex])
                self.label = self.df['name'][self.firstCarIndex]
                self.conf  = self.df['confidence'][self.firstCarIndex]
                self.text = self.label + ' , ' + str(self.conf.round(decimals= 2))
                
        return self.x1, self.y1, self.x2, self.y2, self.text, self.conf


########################################################################################################################
#######################################     Object Tracking     ########################################################
########################################################################################################################

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
        return ok, bbox
    
    def calculate_fps(self,timer):
         # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        return fps


########################################################################################################################
#######################################     Computer Vision APP    #####################################################
########################################################################################################################

class ComputerVisionAPP:
    def __init__(self):
        self.data = 0

    def run_algorithm(self, width=1000, height=700, timer_limit=60):
        # Detection And Tracking Instances
        od = ObjectDetection()
        ot = ObjectTracking()

        x1, y1, x2, y2, text, conf, bbox = 0, 0, 0, 0, '', 0, 0  # Initialize The x1,y1,x2,y2,text,conf,bbox

        video = cv2.VideoCapture("video2.mp4")  # Read video

        # Exit if video not opened.
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        periodic_timer = 0  # Flag To Run Detection After 25 Frame

        isFirstFrame = True  # Flag To Run Detection For The First Frame

        while True:
            ok, frame = video.read()  # read Frame by frame

            frame = cv2.resize(frame, (width, height))  # Resize the Frame

            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                sys.exit()
                break

            # Detect the Car at the first frame only
            if (isFirstFrame):
                x1, y1, x2, y2, text, conf = od.detect(frame)
                if (conf != 0):
                    w = abs(x1 - x2)
                    h = abs(y1 - y2)
                    # Define an initial bounding box
                    bbox = (x1, y1, w, h)
                    ok = ot.track_init(frame, bbox)
                    print('############ GET The First Car ##################')
                    print('BBOX : ', bbox)
                    print('#########################################')

                periodic_timer = 0
                isFirstFrame = False
                print('*********************** First Frame Detection **************************')

            else:
                if (periodic_timer % timer_limit == 0 or conf == 0):
                    x1, y1, x2, y2, text, conf = od.detect(frame)
                    if (conf != 0):
                        w = abs(x1 - x2)
                        h = abs(y1 - y2)
                        bbox = (x1, y1, w, h)  # Define an initial bounding box
                        ok = ot.track_init(frame, bbox)
                        print('############### GET A Car After Timer ##############')
                        print('BBOX : ', bbox)
                        print('####################################################')

                    if (periodic_timer % timer_limit == 0):
                        periodic_timer = 0
                    print('*********************** Repeat Detection **************************')

            periodic_timer = periodic_timer + 1  # Counter The Period_counter Flag

            print('******** TIME : ', periodic_timer, ' ***********')

            # No detected Cars 'conf = 0 '
            if (conf == 0):
                cv2.putText(frame, "No Detected Cars OR Holding After Timer period ", (23, 23),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            else:
                # Start Trackng
                # Start timer
                timer = cv2.getTickCount()

                # Update tracker
                ok, bbox = ot.update_track(frame)

                # Calculate Frames per second (FPS)
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

                if ok:
                    # Tracking success
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 3)
                    print('################### GET A Car  #####################')
                    print('BBOX : ', bbox)
                    print('####################################################')
                else:
                    print('++++++++++++++++ Tracking Failed +++++++++++++++++')
                # End Traking
                print("===================")
                print("Data :  x1: ", x1, ' , y1: ', y1, ' , x2: ', x2, ' , y2: ', y2, ' , text_conf: ', text)
                print("===================")

                # Update data field which is read asynchronously
                self.data = mathlib.frame_to_positions(
                    row_data=[[bbox[0], bbox[1], bbox[2], bbox[3]], [bbox[0], bbox[1], bbox[2], bbox[3]],
                              [bbox[0], bbox[1], bbox[2], bbox[3]]], frame_size=[1000, 700])
                print("===================")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
            x1, y1, x2, y2, text = 0, 0, 0, 0, ''
            cv2.putText(frame, "{} {}".format("Frame NO : ", periodic_timer), (23, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 255), 2)
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (23, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
            cv2.imshow('Frame', frame)
            #     cv2.waitKey(0)
            # Exit if ESC pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):  # if press SPACE
                break
        video.release()
        cv2.destroyAllWindows()