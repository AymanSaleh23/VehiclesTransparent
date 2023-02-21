import cv2
import sys
import torch

import mathematics.mathlib
from comlib import com_socket

DEF_VAL = 0
DEF_FLOAT = 0.0
DEF_TXT = ''
CONFIDENCE_THRESHOLD = 0.65
RECEIVED_FRAME_PORT = 10080
FRAME_SOURCE_IP = '192.168.1.11'
CURRENT_MACHINE_FRAME_SOURCE = "video2.mp4"


# Object Detection Class


class SingleCardDetection:

    def __init__(self):
        print("Loading Object Detection")
        print("Running YOLOv5n")
        self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
        # To detect specific categories, 2: car,5: bus,7: truck ,for more categories
        # 'https://github.com/ultralytics/yolov5/blob/master/data/coco128.yaml'
        self.model.classes = [2, 5, 7]
        # Reject any predictions with less than 60% confidence
        self.threshold = CONFIDENCE_THRESHOLD

    def calc_area(self, xmin, ymin, xmax, ymax):
        width = round(abs(xmax - xmin))
        height = round(abs(ymax - ymin))
        return width * height

    def detect(self, frame):
        x1, y1, x2, y2, text, conf, area = DEF_VAL, DEF_VAL, DEF_VAL, DEF_VAL, DEF_TXT, DEF_FLOAT, DEF_VAL
        result = self.model(frame)
        df = result.pandas().xyxy[0]
        df = df[df['confidence'] > self.threshold]

        if not df.empty:
            # add Area Column to data frame to get the highest car area
            df['area'] = df.apply(lambda x: self.calc_area(x['xmin'], x['ymin'], x['xmax'], x['ymax']),
                                  axis=1)
            # to get Just only one car with the highest area. If you want to get all cars, just loop on index in
            # df.index.
            highest_car_area = df.iloc[df['area'].idxmax()]

            # We make constraint over  the largest area car with acceptable confidence, and we can also add area
            # thresholding constraint 'Future plan'.

            x1, y1 = int(highest_car_area['xmin']), int(highest_car_area['ymin'])
            x2, y2 = int(highest_car_area['xmax']), int(highest_car_area['ymax'])
            label = highest_car_area['name']
            conf = highest_car_area['confidence']
            text = label + ' , ' + str(conf.round(decimals=2))
            area = highest_car_area['area']
        print('======================================================================================')
        print('===================================== Cars Detection ==================================')
        print('======================================================================================')
        print(df)
        print('======================================================================================')
        print('======================================================================================')
        return x1, y1, x2, y2, text, conf, area


# ## Object Tracking Class
class ObjectTracking:
    def __init__(self):
        print("Loading Object Tracking")
        print("CV models for Tracking")
        self.tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.tracker_type = self.tracker_types[7]
        self.tracker = DEF_VAL
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

    def track_init(self, frame, bbox):
        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(frame, bbox)
        return ok

    def update_track(self, frame):
        # Update tracker
        ok, bbox = self.tracker.update(frame)
        bbox = bbox if (bbox[0] > 0 and bbox[1]) else (0, 0, 1, 1)
        return ok, bbox


class ComputerVisionBackApp:
    def __init__(self, width=1000, height=700):
        # Some Initial  Parameters
        self.tracking_area = DEF_VAL
        # ReSize the Frame
        self.width, self.height = width, height
        # Initialize The x1,y1,x2,y2,text,conf,bbox
        self.x1, self.y1, self.x2, self.y2, self.text, self.conf, self.area, self.bbox, self.fps = 0, 0, 0, 0, '', 0, 0, 0, 0
        # periodic timer To make a new detection
        self.timer_limit = 100
        # Flag To Run Detection After timerLimit times
        self.periodic_timer = DEF_VAL
        # Flag To Run Detection For The First Frame
        self.is_first_frame = True
        self.streamed_data = None
        # Selecting the center for ROI 'region of interest',and its left and right distance.
        self.C_X, self.C_Y, self.tolerance = int(self.width / 2), int(self.height / 2), 120

        # Detection And Tracking Instances
        self.od = SingleCardDetection()
        self.ot = ObjectTracking()
        self.front_vehicle_center = self.width / 2

    def run_back(self):

        # Flag To Run Detection After timerLimit times
        self.periodic_timer = DEF_VAL

        # Read video (emulates Camera)
        video = cv2.VideoCapture(CURRENT_MACHINE_FRAME_SOURCE)
        logo = cv2.imread('Valeo.png')
        received_frames = cv2.VideoCapture(CURRENT_MACHINE_FRAME_SOURCE)

        # received_frames = com_socket.Client(FRAME_SOURCE_IP, RECEIVED_FRAME_PORT)

        # Exit if video not opened.
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        if not received_frames.isOpened():
            print('Could not Open Received frames Video')

        while True:
            # read Frame by frame
            ok, frame = video.read()
            # Resize the Frame
            frame = cv2.resize(frame, (self.width, self.height))

            rec_ok, rec_frame = received_frames.read()  # read received Video
            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                sys.exit()

            # Replace The StreamedData with Streamed Frame if it's not None else make it take logo Image
            if not rec_ok:
                print('Cannot read Received frames Video')
                received_frames = logo
            else:
                # read received Video
                # received_frame = received_frames.receive_frame(4 * 1024)
                self.streamed_data = rec_frame

            # Adjust ROI 'Region of interest'
            # ROI bounding Box
            cv2.rectangle(frame, (self.C_X - self.tolerance, self.C_Y), (self.C_X + self.tolerance, self.height),
                          (0, 255,
                           0), 2)
            # ROI Center Point
            cv2.circle(frame, (self.C_X, self.C_Y), radius=0, color=(0, 0, 255), thickness=5)

            # To Make the detection and tracking Only for The ROI instead of the whole frame.
            roi_frame = frame[self.C_Y:self.height, self.C_X - self.tolerance: self.C_X + self.tolerance]

            # Detect the Car at the first frame and pass the result to the initial function of Tracking
            if self.is_first_frame:
                # detecting a car in ROI
                self.x1, self.y1, self.x2, self.y2, self.text, self.conf, self.area = self.od.detect(roi_frame)
                if self.conf != 0:
                    w = abs(self.x1 - self.x2)
                    h = abs(self.y1 - self.y2)
                    # Define an initial bounding box
                    self.bbox = (self.x1, self.y1, w, h)
                    ok = self.ot.track_init(roi_frame, self.bbox)
                    # Rais up the flag of detecting the first frame and getting the initial BBOX for
                    # tracking successfully.
                    self.is_first_frame = False
                    print('*********************** First Frame Detection  ***********************')
                    print('BBOX : ', self.bbox)
                    print('**********************************************************************')

            else:
                if self.periodic_timer % self.timer_limit == 0 or self.conf == 0:
                    self.x1, self.y1, self.x2, self.y2, self.text, self.conf, self.area = self.od.detect(roi_frame)
                    # So there is a car detected
                    if self.conf != 0:
                        w = abs(self.x1 - self.x2)
                        h = abs(self.y1 - self.y2)
                        # Define the bounding box and pass it for tracking
                        self.bbox = (self.x1, self.y1, w, h)
                        ok = self.ot.track_init(roi_frame, self.bbox)
                        print('############### Car Detection After A Periodic Timer ###############')
                        print('BBOX : ', self.bbox)
                        print("===================")
                        print("Metadata :  x1: ", self.x1, ' , y1: ', self.y1, ' , x2: ', self.x2, ' , y2: ', self.y2,
                              ' , text_conf: ', self.text)
                        print("===================")
                        print('####################################################################')

                    if self.periodic_timer % self.timer_limit == 0:
                        self.periodic_timer = 0
                    print('****************************************** Repeat Detection '
                          '******************************************')

            self.periodic_timer = self.periodic_timer + 1  # Increment the Counter of The Period_counter Flag

            print('========================================== TIME : ', self.periodic_timer,
                  '=============================================')

            # No detected Cars 'conf = 0 '
            if self.conf == 0:
                cv2.putText(frame, "No Detected Cars OR Holding After Timer period ", (23, 23), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 0, 255), 2)
                print("||||||||||||||||||||||||| No Detected Cars OR Holding After Timer period"
                      "|||||||||||||||||||||||||")
            else:
                # Start Tracking
                # Start timer To Calculate FPS
                timer = cv2.getTickCount()

                # Update tracker
                ok, bbox = self.ot.update_track(roi_frame)

                # Calculate Frames per second (FPS)
                self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

                # Tracking success
                if ok:
                    print('################### Car Tracking #####################')
                    print('BBOX : ', bbox)
                    print('######################################################')
                    row_data = [0, 0, 0, 0]
                    self.front_vehicle_center = mathematics.mathlib.frame_to_positions(
                        row_data=[bbox[0], bbox[1], bbox[2], bbox[3]], frame_size=[self.width, self.height],
                        mode="BACK")
                    # (x1,y1)
                    p1 = (int(bbox[0]), int(bbox[1]))
                    # (x2,y2)
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    # Blue Rectangle For Tracking
                    cv2.rectangle(roi_frame, p1, p2, (0, 0, 255), 3)
                    # The Tracked Part Of The original Frame
                    self.tracking_area = roi_frame[bbox[1]: (bbox[1] + bbox[3]), bbox[0]: (bbox[0] + bbox[2])]
                    # Resize the streamedData
                    if self.tracking_area.shape[1] == 0 or self.tracking_area.shape[0] == 0:
                        self.streamed_data = None
                    else:
                        self.streamed_data = cv2.resize(self.streamed_data,
                                                        (self.tracking_area.shape[1], self.tracking_area.shape[0]))

                        # The next instruction will put the streamed frame on the tracked car frame.
                        if self.tracking_area.shape[0] != 0 or self.tracking_area.shape[1] != 0:
                            roi_frame[bbox[1]: (bbox[1] + bbox[3]), bbox[0]: (bbox[0] + bbox[2])] = cv2.addWeighted(
                                roi_frame[bbox[1]: (bbox[1] + bbox[3]), bbox[0]: (bbox[0] + bbox[2])], 0.4,
                                self.streamed_data, 0.6, 0)
                        else:
                            roi_frame[bbox[1]: (bbox[1] + bbox[3]), bbox[0]: (bbox[0] + bbox[2])] = None
                else:
                    print('++++++++++++++++ Tracking Failed +++++++++++++++++')
                # End Tracking
                cv2.rectangle(roi_frame, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 255), 2)

            self.x1, self.y1, self.x2, self.y2, self.text = 0, 0, 0, 0, ''
            cv2.putText(frame, "{} {}".format("Frame NO : ", self.periodic_timer), (23, 50), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 255, 255), 2)
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(self.fps)), (23, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 255, 255),
                        2)
            cv2.imshow('Dashboard', frame)
            # cv2.waitKey(0)
            # Exit if ESC pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()


test = ComputerVisionBackApp()
test.run_back()
