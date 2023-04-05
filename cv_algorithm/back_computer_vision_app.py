import time

import torch, cv2, sys
import mathematics.mathlib
import screeninfo
from communication.com_socket import DataHolder
# Object Detection Class


class SingleCardDetection:
    DEF_VAL = 0
    DEF_FLOAT = 0.0
    DEF_TXT = ''
    CONFIDENCE_THRESHOLD = 0.6

    def __init__(self):
        self.screen = screeninfo.get_monitors()[0]
        self.width, self.height = self.screen.width, self.screen.height

        print("Loading Object Detection")
        print("Running YOLOv5n")
        # You can select the size of your model as shown in the previous image.
        self.model = torch.hub.load('..\\GUI\\yolov5', 'yolov5n', source='local')
        # To detect specific categories, 2: car,5: bus,7: truck ,for more categories 'https://github.com/ultralytics/yolov5/blob/master/data/coco128.yaml'
        self.model.classes_to_detect = [2, 5, 7]
        # Reject any predictions with less than 60% confidence
        self.threshold = SingleCardDetection.CONFIDENCE_THRESHOLD

    def detect(self, frame):
        self.x1, self.y1, self.x2, self.y2, self.text, self.conf = SingleCardDetection.DEF_VAL,\
                                                                    SingleCardDetection.DEF_VAL, \
                                                                    SingleCardDetection.DEF_VAL,\
                                                                    SingleCardDetection.DEF_VAL, \
                                                                    SingleCardDetection.DEF_TXT, \
                                                                    SingleCardDetection.DEF_FLOAT
        self.result = self.model(frame)
        self.df = self.result.pandas().xyxy[0]
        print('======================================================================================')
        print('===================================== Cars Detection ==================================')
        print('======================================================================================')
        print(self.df)
        print('======================================================================================')
        print('======================================================================================')

        if not self.df.empty:
            # to get Just only one car. If you want to get all cars, just loop on index in detected_vehicles_data_frame.index.
            self.first_car_index = self.df.index[0]

            if self.df['confidence'][self.first_car_index] >= self.threshold:
                self.x1, self.y1 = int(self.df['xmin'][self.first_car_index]),\
                    int(self.df['ymin'][self.first_car_index])
                self.x2, self.y2 = int(self.df['xmax'][self.first_car_index]), \
                    int(self.df['ymax'][self.first_car_index])
                self.label = self.df['name'][self.first_car_index]
                self.conf  = self.df['confidence'][self.first_car_index]
                self.text = self.label + ' , ' + str(self.conf.round(decimals=2))

        return self.x1, self.y1, self.x2, self.y2, self.text, self.conf


# ## Object Tracking Class
class ObjectTracking:
    def __init__(self):
        print("Loading Object Tracking")
        print("CV models for Tracking")
        self.tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.tracker_type = self.tracker_types[7]
        self.tracker = SingleCardDetection.DEF_VAL
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
        bbox = bbox if(bbox[0] > 0 and bbox[1]) else (0, 0, 1, 1)
        return ok, bbox


class ComputerVisionBackApp:
    width_ratio = 0.15
    height_ratio = 0.3
    def __init__(self, source=0):
        self.screen = screeninfo.get_monitors()[0]
        self.width, self.height = self.screen.width, self.screen.height
        # Some Initial  Parameters
        self.tracking_area = SingleCardDetection.DEF_VAL
        # ReSize the Frame
        self.source = source
        # Initialize The x1,y1,x2,y2,text,conf,bbox
        self.x1, self.y1, self.x2, self.y2, self.text, self.conf, self.bbox, self.fps = 0, 0, 0, 0, '', 0, 0, 0

        self.timer_limit = SingleCardDetection.DEF_VAL
        # Flag To Run Detection After timerLimit times
        self.periodic_timer = SingleCardDetection.DEF_VAL
        # Flag To Run Detection For The First Frame
        self.is_first_frame = True
        self.last_read_frame = None
        #TO_DO: Valeo Icon/Logo as a default pic.
        self.last_streamed_frame = None
        self.last_disc = None
        self.data_holder = DataHolder()

        # Selecting the center for ROI 'region of interest',and its left and right distance.
        self.C_X, self.C_Y, self.tolerance = int(self.width // 2), int(self.height // 3), self.width//4

        # Detection And Tracking Instances
        self.od = SingleCardDetection()
        self.ot = ObjectTracking()
        # Read video (emulates Camera)
        self.video = cv2.VideoCapture(self.source)
        self.front_vehicle_center = self.width // 2
        self.data_holder.reset_discrete()
        # received_video = cv2.VideoCapture(0)

    def video_filling_coordinates(self, x1, y1, x2, y2, detected_car_width, detected_car_height):
        x1 = round(x1 + detected_car_width * ComputerVisionBackApp.width_ratio)
        y1 = round(y1 + detected_car_height * ComputerVisionBackApp.height_ratio)
        x2 = round(x2 - detected_car_width * ComputerVisionBackApp.width_ratio)
        y2 = round(y2 - detected_car_height * ComputerVisionBackApp.height_ratio)
        return x1, y1, x2, y2

    def crop_and_resize_streamed_video(self, frame_to_crop):
        x1, y1, x2, y2 = 1, 1, frame_to_crop.shape[1], frame_to_crop.shape[0]
        y1 = round(y2 * 0.5)
        frame_to_crop = frame_to_crop[y1:y2, x1: x2]
        return frame_to_crop

    def run_back(self, sock, timer_limit=30, detect_per_frame=10):
        # periodic timer To make a new detection
        self.timer_limit = timer_limit
        # Flag To Run Detection After timerLimit times
        self.periodic_timer = SingleCardDetection.DEF_VAL
        self.sock = sock

        frames_counter = 0
        first_frame = True
        # Exit if video not opened.
        while not self.video.isOpened():
            self.video = cv2.VideoCapture(self.source)  # CAMERA - RECORDED VIDEO - SIMULATION
            print("Could not open video")
            time.sleep(1)
            sys.exit()

        while sock.connect_mechanism():
            # read Frame by frame
            ok, cam_captured_frame = self.video.read()

            # Resize the Frame
            cam_captured_frame = cv2.resize(cam_captured_frame, (self.width, self.height))

            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                sys.exit()

            else:
                # read received Video
                pass

            # Adjust ROI 'Region of interest'
            # To Make the detection and tracking Only for The ROI instead of the whole frame.
            roi_frame = cam_captured_frame[self.C_Y:self.height, self.C_X - self.tolerance: self.C_X + self.tolerance]

            # Detect the Car at the first frame and pass the result to the initial function of Tracking
            if frames_counter >= detect_per_frame or first_frame:
                # detecting a car in ROI
                self.x1, self.y1, self.x2, self.y2, self.text, self.conf = self.od.detect(roi_frame)

                if self.conf != 0:
                    w = round(abs(self.x2 - self.x1))
                    h = round(abs(self.y2 - self.y1))
                    self.x1, self.y1, self.x2, self.y2 = self.video_filling_coordinates(self.x1, self.y1, self.x2, self.y2, w, h)

                    w = round(abs(self.x2 - self.x1))
                    h = round(abs(self.y2 - self.y1))

                    # Define an initial bounding box
                    self.bbox = (self.x1, self.y1, w, h)
                    ok = self.ot.track_init(roi_frame, self.bbox)
                    # Rais up the flag of detecting the first frame and getting the initial BBOX for
                    # tracking successfully.
                    frames_counter = 0
                    first_frame = False
                    print('############### Car Detection After A Periodic Timer ###############')
                    print('BBOX : ', self.bbox)
                    print("===================")
                    print("Metadata :  x1: ", self.x1, ' , y1: ', self.y1,
                                    ' , x2: ', self.x2, ' , y2: ', self.y2, ' , text_conf: ', self.text)
                    print("===================")
                    print('####################################################################')

                print('****************************************** Repeat Detection '
                      '******************************************')

            frames_counter += 1     # Increment the Counter of The Period_counter Flag

            print('========================================== TIME : ', self.periodic_timer,
                  '=============================================')

            if self.conf != 0:
                # Start Tracking
                # Start timer To Calculate FPS
                #timer = cv2.getTickCount()

                # Update tracker
                #ok, self.bbox = self.ot.update_track(roi_frame)

                # Calculate Frames per second (FPS)
                #self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

                # Tracking success
                if ok:
                    self.last_streamed_frame = self.data_holder.get_frame()
                    self.last_disc = self.data_holder.get_discrete()

                    print('################### Car Tracking #####################')
                    print('BBOX : ', self.bbox)
                    print('######################################################')

                    self.front_vehicle_center = mathematics.mathlib.frame_to_positions(
                        row_data=[self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]],
                        frame_size=[self.width, self.height], mode="BACK")

                    # (x1,y1)
                    p1 = (int(self.bbox[0]), int(self.bbox[1]))
                    # (x2,y2)
                    p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                    # Blue Rectangle For Tracking
                    cv2.rectangle(roi_frame, p1, p2, (0, 0, 255), 3)
                    # The Tracked Part Of The original Frame
                    self.tracking_area = roi_frame[self.bbox[1]: (self.bbox[1]+self.bbox[3]),
                                         self.bbox[0]: (self.bbox[0]+self.bbox[2])]
                    print('########################################## tracking_area SHAPE : ', self.tracking_area.shape)
                    # Resize the streamedData
                    if self.tracking_area.shape[1] == 0 or self.tracking_area.shape[0] == 0:
                        self.last_streamed_frame = None
                    else:
                        try:
                            # cv2.imshow("SOCK_RECEIVING VIDEO", self.last_streamed_frame)
                            self.last_streamed_frame = self.crop_and_resize_streamed_video(self.last_streamed_frame)
                            self.last_streamed_frame = cv2.resize(self.last_streamed_frame,
                                                                  (self.tracking_area.shape[1],
                                                                   self.tracking_area.shape[0]))

                            print('########################################### streamed Data SHAPE : ',
                                  self.last_streamed_frame.shape)
                            # The next instruction will put the streamed frame on the tracked car frame.
                            # In Future plans we cane use image blending or image superimposing concepts.
                            roi_frame[self.bbox[1]: (self.bbox[1]+self.bbox[3]), self.bbox[0]: (self.bbox[0]+self.bbox[2])] = \
                                self.last_streamed_frame if (self.tracking_area.shape[0] != 0 or self.tracking_area.shape[1] != 0) \
                                else None

                            cam_captured_frame = self.update_warning(cam_captured_frame, self.last_disc)
                        except Exception:
                            print("Frame have no Size to reshape")
                else:
                    print('++++++++++++++++ Tracking Failed +++++++++++++++++')

            # Showing The Video Frame
            window_name = 'Back View'
            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, self.screen.x - 1, self.screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, cam_captured_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)

        self.video.release()
        cv2.destroyAllWindows()

    def update_warning(self, frame, disc):
        """
        asynchronously update flags in left and right to inform user not to pass
        """
        secure = [True, True]
        # while True:

        #   [ [[left_dist, ang], [center_dist, ang], [right_dist, ang]],length ]
        print(f"\n\n\nself.bm.received_fd.get_discrete(){disc}\n\n\n")

        if disc is not None:
            if disc[0][0][1] > 0:
                s_img = cv2.imread("..\\GUI\\unsafe_left.png", -1)
                y_offset = self.height * 3 // 4
                x_offset = self.width // 4
                y1, y2 = y_offset, y_offset + s_img.shape[0]
                x1, x2 = x_offset - s_img.shape[1], x_offset

                alpha_s = s_img[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                frame[y1:y2, x1:x2, 0] = (alpha_s * s_img[:, :, 0] + alpha_l * frame[y1:y2, x1:x2, 0])
                frame[y1:y2, x1:x2, 1] = (alpha_s * s_img[:, :, 1] + alpha_l * frame[y1:y2, x1:x2, 1])
                frame[y1:y2, x1:x2, 2] = (alpha_s * s_img[:, :, 2] + alpha_l * frame[y1:y2, x1:x2, 2])
                print("Don't Pass left is not Secure")

            elif disc[0][0][1] < 0:
                s_img = cv2.imread("..\\GUI\\safe_left.png", -1)
                y_offset = self.height * 3 // 4
                x_offset = self.width // 4
                y1, y2 = y_offset, y_offset + s_img.shape[0]
                x1, x2 = x_offset - s_img.shape[1], x_offset

                alpha_s = s_img[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                frame[y1:y2, x1:x2, 0] = (alpha_s * s_img[:, :, 0] + alpha_l * frame[y1:y2, x1:x2, 0])
                frame[y1:y2, x1:x2, 1] = (alpha_s * s_img[:, :, 1] + alpha_l * frame[y1:y2, x1:x2, 1])
                frame[y1:y2, x1:x2, 2] = (alpha_s * s_img[:, :, 2] + alpha_l * frame[y1:y2, x1:x2, 2])
                print("Pass left is Secure")

            if disc[0][2][1] > 0:
                s_img = cv2.imread("..\\GUI\\unsafe_right.png", -1)
                y_offset = self.height * 3 // 4
                x_offset = self.width * 3 // 4
                y1, y2 = y_offset, y_offset + s_img.shape[0]
                x1, x2 = x_offset, x_offset + s_img.shape[1]

                alpha_s = s_img[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                frame[y1:y2, x1:x2, 0] = (alpha_s * s_img[:, :, 0] + alpha_l * frame[y1:y2, x1:x2, 0])
                frame[y1:y2, x1:x2, 1] = (alpha_s * s_img[:, :, 1] + alpha_l * frame[y1:y2, x1:x2, 1])
                frame[y1:y2, x1:x2, 2] = (alpha_s * s_img[:, :, 2] + alpha_l * frame[y1:y2, x1:x2, 2])
                print("Don't Pass right is not Secure")

            elif disc[0][2][1] < 0:
                s_img = cv2.imread("..\\GUI\\safe_right.png", -1)
                y_offset = self.height * 3 // 4
                x_offset = self.width * 3 // 4
                y1, y2 = y_offset, y_offset + s_img.shape[0]
                x1, x2 = x_offset, x_offset + s_img.shape[1]

                alpha_s = s_img[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                frame[y1:y2, x1:x2, 0] = (alpha_s * s_img[:, :, 0] + alpha_l * frame[y1:y2, x1:x2, 0])
                frame[y1:y2, x1:x2, 1] = (alpha_s * s_img[:, :, 1] + alpha_l * frame[y1:y2, x1:x2, 1])
                frame[y1:y2, x1:x2, 2] = (alpha_s * s_img[:, :, 2] + alpha_l * frame[y1:y2, x1:x2, 2])
                print("Pass right is Secure")

        return frame
