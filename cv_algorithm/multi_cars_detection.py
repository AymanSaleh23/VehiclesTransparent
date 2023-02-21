import sys

import cv2
import torch

from front_app.cv_global_variables import CVFrontGlobalVariables
from mathematics.mathlib import map_values_ranges


class MultiCarsDetection:
    def __init__(self, width, height):

        self.result = None
        print("Loading Object Detection")
        print("Running YOLOv5n")
        self.model = torch.hub.load('yolov5', 'yolov5n',
                                    source='local')  # You can select the size of your model as shown in the previous image.
        self.model.classes = [2, 5,
                              7]  # To detect specific categories, 2: car,5: bus,7: truck ,for more categories 'https://github.com/ultralytics/yolov5/blob/master/data/coco128.yaml'
        self.threshold = 0.65  # reject any predictions with less than 60% confidence
        self.end_left_section = round(width / 3)
        self.end_middle_section = round(width / (3 / 2))
        self.end_right_section = width
        self.width = width
        self.height = height

    def calc_area(self, xmin, ymin, xmax, ymax):
        """
        calculate detected car area after rounded it
        """
        width = round(abs(xmax - xmin))
        height = round(abs(ymax - ymin))
        return width * height

    def get_car_center(self, x1, y1, x2, y2, width, height):
        c_x = round((abs(abs(width - x1) - abs(width - x2)) / 2) + x1)
        c_y = round((abs(abs(height - y1) - abs(height - y2)) / 2) + y1)
        center = (c_x, c_y)
        return center

    def detect(self, frame):
        self.result = self.model(frame)
        self.df = self.result.pandas().xyxy[0]

        # First: set the therashould for whole dataframe
        self.df = self.df[self.df['confidence'] > self.threshold]

        if not self.df.empty:  # check if the dataframe is empty after applying therashould

            # add Area Column to data frame to get the highest car area
            self.df['area'] = self.df.apply(lambda x: self.calc_area(x['xmin'], x['ymin'], x['xmax'], x['ymax']),
                                            axis=1)

            print('======================================================================================')
            print('===================================== Cars Detection =================================')
            print('======================================================================================')
            print(self.df)
            # print('--------------------------------------------------------------------------------------')
            highest_left_car_area = self.df[self.df['xmax'] <= self.end_left_section]
            if not highest_left_car_area.empty:
                highest_left_car_area = self.df.iloc[highest_left_car_area['area'].idxmax()]
                #                 print('highest_left_car_area')
                #                 print("{}".format( highest_left_car_area))
                highest_left_car_area_center = self.get_car_center(x1=highest_left_car_area['xmin'],
                                                                   y1=highest_left_car_area['ymin'],
                                                                   x2=highest_left_car_area['xmax'],
                                                                   y2=highest_left_car_area['ymax'], width=self.width,
                                                                   height=self.height)
                x1y1 = (round(highest_left_car_area['xmin']), round(highest_left_car_area['ymin']))
                x2y2 = (round(highest_left_car_area['xmax']), round(highest_left_car_area['ymax']))
                cv2.rectangle(frame, x1y1, x2y2, (0, 0, 255), 2)
                cv2.circle(frame, highest_left_car_area_center, radius=1, color=(0, 0, 255), thickness=2)

            else:
                highest_left_car_area = 0
                highest_left_car_area_center = (-1, 0)
            #             print('--------------------------------------------------------------------------------------')
            highest_middle_car_area = self.df[
                (self.df['xmax'] > self.end_left_section) & (self.df['xmax'] <= self.end_middle_section)]
            if (not highest_middle_car_area.empty):
                highest_middle_car_area = self.df.iloc[highest_middle_car_area['area'].idxmax()]
                #                 print('highest_middle_car_area')
                #                 print("{}".format( highest_middle_car_area))
                highest_middle_car_area_center = self.get_car_center(x1=highest_middle_car_area['xmin'],
                                                                     y1=highest_middle_car_area['ymin'],
                                                                     x2=highest_middle_car_area['xmax'],
                                                                     y2=highest_middle_car_area['ymax'],
                                                                     width=self.width, height=self.height)
                x1y1 = (round(highest_middle_car_area['xmin']), round(highest_middle_car_area['ymin']))
                x2y2 = (round(highest_middle_car_area['xmax']), round(highest_middle_car_area['ymax']))
                cv2.rectangle(frame, x1y1, x2y2, (0, 255, 0), 2)
                cv2.circle(frame, highest_middle_car_area_center, radius=1, color=(0, 255, 0), thickness=2)

            else:
                highest_middle_car_area = 0
                highest_middle_car_area_center = (-1, 0)
            #             print('--------------------------------------------------------------------------------------')
            highest_right_car_area = self.df[
                (self.df['xmax'] > self.end_middle_section) & (self.df['xmax'] <= self.end_right_section)]
            if (not highest_right_car_area.empty):
                highest_right_car_area = self.df.iloc[highest_right_car_area['area'].idxmax()]
                #                 print('highest_right_car_area')
                #                 print("{}".format( highest_right_car_area))
                highest_right_car_area_center = self.get_car_center(x1=highest_right_car_area['xmin'],
                                                                    y1=highest_right_car_area['ymin'],
                                                                    x2=highest_right_car_area['xmax'],
                                                                    y2=highest_right_car_area['ymax'], width=self.width,
                                                                    height=self.height)
                x1y1 = (round(highest_right_car_area['xmin']), round(highest_right_car_area['ymin']))
                x2y2 = (round(highest_right_car_area['xmax']), round(highest_right_car_area['ymax']))
                cv2.rectangle(frame, x1y1, x2y2, (255, 0, 0), 2)
                cv2.circle(frame, highest_right_car_area_center, radius=1, color=(255, 0, 0), thickness=2)
            else:
                highest_right_car_area = 0
                highest_right_car_area_center = (-1, 0)

            cars_sections = [highest_left_car_area_center, highest_middle_car_area_center,
                             highest_right_car_area_center]
            return cars_sections  # return list of the highest car area for each section, 0 left, 1 middle, 2 right
        else:
            return [(-1, 0), (-1, 0), (-1, 0)]


class ComputerVisionFrontal:

    def __init__(self, width=1000, height=700):
        # Some Initial  Parameters
        self.width, self.height = width, height
        # Detection Instances
        self.od = MultiCarsDetection(width=width, height=height)

        # Read video
        self.video = cv2.VideoCapture("video5.mp4")

    def run_front(self):

        # Exit if video not opened.
        if not self.video.isOpened():
            print("Could not open video")
            CVFrontGlobalVariables.detected_cars_centers_list = [(-1, 0), (-1, 0), (-1, 0)]
            sys.exit()

        while True:
            # Read Frame by frame
            ok, frame = self.video.read()
            CVFrontGlobalVariables.frame = frame
            frame = cv2.resize(frame, (self.width, self.height))  # Resize the Frame

            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                CVFrontGlobalVariables.detected_cars_centers_list = [(-1, 0), (-1, 0), (-1, 0)]
                sys.exit()

            cars_sections = self.od.detect(frame=frame)
            # [ (451, 651) , (0,0) , (451, 651) ]
            position_angels = [
                map_values_ranges(input_value=c[0], input_range_min=0, input_range_max=self.width,
                                  output_range_min=0,
                                  output_range_max=180) for c in cars_sections]
            print('position_angels : ', position_angels)
            print('cars_sections : ',cars_sections)
            CVFrontGlobalVariables.detected_cars_centers_list = position_angels

            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('Detected Left Car center  : ')
            print(cars_sections[0])
            print('Detected Middle Car center : ')
            print(cars_sections[1])
            print('Detected Right Car center : ')
            print(cars_sections[2])
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            # Divide Frame Into Sections
            # Left section
            cv2.line(frame, (round(self.width / 3), 0), (round(self.width / 3), self.height), (0, 0, 0), 1)
            cv2.putText(frame, "Left Section", (5, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # Middle section
            cv2.line(frame, (round(self.width / (3 / 2)), 0), (round(self.width / (3 / 2)), self.height), (0, 0, 0), 1)
            cv2.putText(frame, "Middle Section", (round(self.width / 3) + 5, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 255, 0), 2)
            # Right section
            cv2.putText(frame, "Right Section", (round(self.width / (3 / 2)) + 5, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (255, 0, 0), 2)
            # Showing The Video Frame
            cv2.imshow('test_Image', frame)

            #         cv2.waitKey(0)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # if press q
                CVFrontGlobalVariables.detected_cars_centers_list = [(-1, 0), (-1, 0), (-1, 0)]
                break

        self.video.release()
        cv2.destroyAllWindows()
