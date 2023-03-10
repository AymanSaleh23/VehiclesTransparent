import sys
import time

import cv2
import torch
import screeninfo

from mathematics.mathlib import map_values_ranges


"""
    1. Naming.
    2. each function does only one job.
    3. function length <= 10 lines.
    

"""


def calculate_area(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    """calculate area based on (top_left_corner) and (bottom_right_corner) coordinates"""
    width = round(abs(bottom_right_x - top_left_x))
    height = round(abs(bottom_right_y - top_left_y))
    return width * height


def calculate_rectangle_center(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    """Calculate center of a rectangle based on (top_left_corner) and (bottom_right_corner) coordinates"""
    center_x = round((top_left_x + bottom_right_x) / 2)
    center_y = round((top_left_y + bottom_right_y) / 2)
    center = (center_x, center_y)
    return center


class MultiCarsDetection:
    PREDICTION_THRESHOLD = 0.75
    CAR = 2
    BUS = 5
    TRUCK = 7
    TOP_LEFT_X = 'xmin'
    TOP_LEFT_Y = 'ymin'
    BOTTOM_RIGHT_X = 'xmax'
    BOTTOM_RIGHT_Y = 'ymax'
    def __init__(self, width, height):

        self.result = None
        self.detected_vehicles_data_frame = None
        print("Loading Object Detection")
        print("Running YOLOv5n")
        self.model = torch.hub.load(repo_or_dir='..\\GUI\\yolov5', model='yolov5n', source='local')

        self.model.classes_to_detect = [MultiCarsDetection.CAR, MultiCarsDetection.BUS, MultiCarsDetection.TRUCK]

        self.threshold = MultiCarsDetection.PREDICTION_THRESHOLD

        self.width = width
        self.height = height

        self.end_left_section = round(width / 3)
        self.end_middle_section = round(width / (3 / 2))
        self.end_right_section = width

    def detect(self, frame):
        """return list of the closest vehicle area for each section, 0 left, 1 middle, 2 right"""
        self.result = self.model(frame)

        self.detected_vehicles_data_frame = self.result.pandas().xyxy[0]

        # Delete detected vehicles which is under-prediction threshold
        self.detected_vehicles_data_frame = \
            self.detected_vehicles_data_frame[self.detected_vehicles_data_frame['confidence'] > self.threshold]

        if not self.detected_vehicles_data_frame.empty:
            self.add_vehicles_areas_to_data_frame()
        # LEFT CAR BOUNDING BOX
            left_section_vehicles = self.detected_vehicles_data_frame[
                self.detected_vehicles_data_frame[MultiCarsDetection.BOTTOM_RIGHT_X] <= self.end_left_section]
            middle_section_vehicles = self.detected_vehicles_data_frame[
                (self.detected_vehicles_data_frame[MultiCarsDetection.BOTTOM_RIGHT_X] > self.end_left_section) &
                (self.detected_vehicles_data_frame[MultiCarsDetection.BOTTOM_RIGHT_X] <= self.end_middle_section)]
            right_section_vehicles = self.detected_vehicles_data_frame[
                (self.detected_vehicles_data_frame[MultiCarsDetection.BOTTOM_RIGHT_X] > self.end_middle_section) &
                (self.detected_vehicles_data_frame[MultiCarsDetection.BOTTOM_RIGHT_X] <= self.end_right_section)]

            left_section_car_center = self.get_and_draw_closest_detected_vehicle_box_and_center(
                frame, left_section_vehicles, (0, 0, 255))
            middle_section_car_center = self.get_and_draw_closest_detected_vehicle_box_and_center(
                frame,  middle_section_vehicles, (0, 255, 0))
            right_section_car_center = self.get_and_draw_closest_detected_vehicle_box_and_center(
                frame, right_section_vehicles, (255, 0, 0))

            cars_sections = [left_section_car_center, middle_section_car_center,
                             right_section_car_center]
            return cars_sections  # return list of the closest vehicle area for each section, 0 left, 1 middle, 2 right
        else:
            return [(-1, 0), (-1, 0), (-1, 0)]

    def get_and_draw_closest_detected_vehicle_box_and_center(self, frame, section_vehicles, section_color=(0, 0, 255)):
        if not section_vehicles.empty:
            # GET CENTER
            left_section_closest_vehicle = self.detected_vehicles_data_frame.iloc[
                section_vehicles['area'].idxmax()]

            left_section_car_center = calculate_rectangle_center(left_section_closest_vehicle[MultiCarsDetection.TOP_LEFT_X],
                                                                 left_section_closest_vehicle[MultiCarsDetection.TOP_LEFT_Y],
                                                                 left_section_closest_vehicle[MultiCarsDetection.BOTTOM_RIGHT_X],
                                                                 left_section_closest_vehicle[MultiCarsDetection.BOTTOM_RIGHT_Y])

            top_left_corner = (round(left_section_closest_vehicle[MultiCarsDetection.TOP_LEFT_X]),
                               round(left_section_closest_vehicle[MultiCarsDetection.TOP_LEFT_Y]))

            bottom_right_corner = (round(left_section_closest_vehicle[MultiCarsDetection.BOTTOM_RIGHT_X]),
                                   round(left_section_closest_vehicle[MultiCarsDetection.BOTTOM_RIGHT_Y]))
            # DISPLAY BOUNDING BOX
            cv2.rectangle(frame, top_left_corner, bottom_right_corner, color=section_color, thickness=2)
            # DISPLAY CENTER DOT
            cv2.circle(frame, left_section_car_center, radius=1, color=section_color, thickness=2)

        else:
            left_section_closest_vehicle = 0
            left_section_car_center = (-1, 0)
        return left_section_car_center

    def add_vehicles_areas_to_data_frame(self):
        self.detected_vehicles_data_frame['area'] = self.detected_vehicles_data_frame.apply(
            lambda x: calculate_area(x[MultiCarsDetection.TOP_LEFT_X],
                                     x[MultiCarsDetection.TOP_LEFT_Y],
                                     x[MultiCarsDetection.BOTTOM_RIGHT_X],
                                     x[MultiCarsDetection.BOTTOM_RIGHT_Y]), axis=1
        )


class ComputerVisionFrontal:

    def __init__(self, source=0):
        self.screen = screeninfo.get_monitors()[0]
        self.width, self.height = self.screen.width, self.screen.height
        # Some Initial  Parameters
        # Detection Instances
        self.od = MultiCarsDetection(width=self.width, height=self.height)
        self.frame_to_send = None
        self.angle_to_send = None
        self.source = source
        self.video = cv2.VideoCapture(self.source)  # CAMERA - RECORDED VIDEO - SIMULATION
        # Read video

    def run_front(self, sock, frames_per_detect=10):
        frames_counter = 0
        first_frame = True

        # Exit if video not opened.
        while not self.video.isOpened():
            print("Could not open video")
            self.video = cv2.VideoCapture(self.source)  # CAMERA - RECORDED VIDEO - SIMULATION
            self.angle_to_send = [(-1, 0), (-1, 0), (-1, 0)]
            time.sleep(1)
            # sys.exit()

        while sock.connect_mechanism():
            # Read Frame by frame
            ok, frame = self.video.read()

            while frame is None:
                cv2.VideoCapture(self.source)

            frame = cv2.resize(frame, (self.width, self.height))  # Resize the Frame

            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                self.angle_to_send = [-1, -1, -1]
                sys.exit()
            if frames_counter >= frames_per_detect or first_frame:
                self.cars_sections = self.od.detect(frame=frame)
                frames_counter = 0
                first_frame = False

            frames_counter += 1

            # [ (451, 651) , (0,0) , (451, 651) ]
            position_angels = [
                map_values_ranges(input_value=c[0], input_range_min=0, input_range_max=self.width,
                                  output_range_min=0,
                                  output_range_max=180) for c in self.cars_sections]
            print('position_angels : ', position_angels)
            print('cars_sections : ', self.cars_sections)

            # CVFrontGlobalVariables.frame = frame
            self.frame_to_send = frame

            self.angle_to_send = position_angels

            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('Detected Left Car center  : ')
            print(self.cars_sections[0])
            print('Detected Middle Car center : ')
            print(self.cars_sections[1])
            print('Detected Right Car center : ')
            print(self.cars_sections[2])
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            # Showing The Video Frame
            window_name = 'Current Front'
            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, self.screen.x - 1, self.screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # if press q
                self.angle_to_send = [(-1, 0), (-1, 0), (-1, 0)]
                break
            time.sleep(0.01)

        self.video.release()
        cv2.destroyAllWindows()
