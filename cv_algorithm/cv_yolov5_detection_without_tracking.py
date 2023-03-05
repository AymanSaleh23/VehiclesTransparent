import sys

import cv2
import torch

DEF_VAL = 0
DEF_FLOAT = 0.0
DEF_TXT = ''
CONFIDENCE_THRESHOLD = 0.65
RECEIVED_FRAME_PORT = 10080
FRAME_SOURCE_IP = '192.168.1.11'
CURRENT_MACHINE_FRAME_SOURCE = "rear_1.mp4"


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
        print('===================================== Cars Detection =================================')
        print(df)
        return x1, y1, x2, y2, text, conf, area


class ComputerVisionBackAppWithoutTracking:
    def __init__(self, width=1440, height=900):
        # Some Initial  Parameters
        # ReSize the Frame
        self.width, self.height = width, height
        self.opacity = 0.2
        self.width_ratio, self.height_ratio = 0.15, 0.3
        # Initialize The x1,y1,x2,y2,text,conf,bbox
        self.x1, self.y1, self.x2, self.y2, self.text, self.conf, self.area, self.bbox, self.fps = 0, 0, 0, 0, '', 0, 0, 0, 0
        self.streamed_data = None
        # Selecting the center for ROI 'region of interest',and its left and right distance.
        self.C_X, self.C_Y, self.tolerance = int(self.width / 2), int(self.height / 3), int(self.width / 6)

        # Detection And Tracking Instances
        self.od = SingleCardDetection()
        self.front_vehicle_center = self.width / 2

    def video_filling_coordinates(self, x1, y1, x2, y2, detected_car_width, detected_car_height):
        x1 = round(x1 + detected_car_width * self.width_ratio)
        y1 = round(y1 + detected_car_height * self.height_ratio)
        x2 = round(x2 - detected_car_width * self.width_ratio)
        y2 = round(y2 - detected_car_height * self.height_ratio)
        return x1, y1, x2, y2

    # def crop_and_resize_streamed_video(self, streamed_data):
    #     x1, y1, x2, y2 = 1, 1, streamed_data.shape[1], streamed_data.shape[0]
    #     x1 = round(x1 + x2 * self.width_ratio)  # 96
    #     y1 = round(y1 + y2 * self.height_ratio)  # 324
    #     x2 = round(x2 - x2 * self.width_ratio)  # 1824
    #     y2 = round(y2 - y2 * self.height_ratio)  # 756
    #     streamed_data = streamed_data[y1:y2, x1: x2]

    def crop_and_resize_streamed_video(self, streamed_data):
        x1, y1, x2, y2 = 1, 1, streamed_data.shape[1], streamed_data.shape[0]
        y1 = round(y2 * 0.5)
        streamed_data = streamed_data[y1:y2, x1: x2]
        return streamed_data

    def run_back(self):

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

            if ok:
                frame = cv2.resize(frame, (self.width, self.height))  # Resize the Frame

                timer = cv2.getTickCount()  # Start timer To Calculate FPS

                # Adjust ROI 'Region of interest'
                cv2.rectangle(frame, (self.C_X - self.tolerance, self.C_Y), (self.C_X + self.tolerance, self.height),
                              (255, 255, 255), 1)  # ROI bounding Box
                cv2.circle(frame, (self.C_X, self.C_Y), radius=0, color=(0, 0, 255), thickness=3)  # ROI Center Point

                # To Make the detection Only for The ROI instead of the whole frame.
                ROI_Frame = frame[self.C_Y:self.height, self.C_X - self.tolerance:self.C_X + self.tolerance]

                self.x1, self.y1, self.x2, self.y2, self.text, self.conf, self.area = self.od.detect(
                    ROI_Frame)  # detecting a car in ROI
                detected_car_width = round(abs(self.x2 - self.x1))
                detected_car_height = round(abs(self.y2 - self.y1))
                self.x1, self.y1, self.x2, self.y2 = self.video_filling_coordinates(
                    self.x1, self.y1,
                    self.x2, self.y2,
                    detected_car_width,
                    detected_car_height)

                detected_car_width = round(abs(self.x2 - self.x1))
                detected_car_height = round(abs(self.y2 - self.y1))
                # Fill Streamed Video
                if self.area != 0:
                    print("streamed_data Shape : ", self.streamed_data.shape)
                    # crop the streamed_data Video and resize it over the cropped detected car
                    self.streamed_data = self.crop_and_resize_streamed_video(self.streamed_data)

                    self.streamed_data = cv2.resize(self.streamed_data, (detected_car_width, detected_car_height))

                    ROI_Frame[self.y1: self.y2, self.x1: self.x2] = cv2.addWeighted(
                        ROI_Frame[self.y1: self.y2, self.x1: self.x2], self.opacity, self.streamed_data,
                        1 - self.opacity, 0)
                    # ROI_Frame[self.y1: self.y2, self.x1: self.x2] =  self.streamed_data
                cv2.rectangle(ROI_Frame, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 255), 1)
                self.x1, self.y1, self.x2, self.y2, self.text, self.area = 0, 0, 0, 0, '', 0
                self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)  # Calculate Frames per second (FPS)
                # Display FPS on frame
                cv2.putText(frame, "FPS : " + str(int(self.fps)), (23, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (50, 255, 255), 2);
                cv2.imshow('Frame', frame)

            # cv2.waitKey(0)
            # Exit if ESC pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()


test = ComputerVisionBackAppWithoutTracking()
test.run_back()
