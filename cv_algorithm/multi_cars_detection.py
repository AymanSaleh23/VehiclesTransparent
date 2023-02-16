import torch
import cv2
import sys
import numpy as np

class MultiCarsdetection:
    def __init__(self):
       
        print("Loading Object Detection")
        print("Running YOLOv5n")
        # You can select the size of your model as shown in the previous image.
        self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
        # To detect specific categories, 2: car,5: bus,7: truck ,for more categories
        # 'https://github.com/ultralytics/yolov5/blob/master/data/coco128.yaml'
        self.model.classes = [2, 5, 7]
        # reject any predictions with less than 60% confidence
        self.threshold = 0.65
        
    def detect(self, frame,width):
        self.result = self.model(frame)
        self.df = self.result.pandas().xyxy[0]
        end_left_section = round(width/3)
        end_middle_section = round(width/(3/2))
        end_right_section = width

        if not self.df.empty:
            # First Create a 'Section' Column that contains each car section, 0 for Left,1 for Middle, 2 for Right
            # create a list of our conditions
            conditions = [
                (self.df['xmax'] <= end_left_section),
                (self.df['xmax'] > end_left_section) & (self.df['xmax'] <= end_middle_section),
                (self.df['xmax'] > end_middle_section) & (self.df['xmax'] <= end_right_section),
                ]
            # create a list of the values we want to assign for each condition
            values = ['0', '1', '2']
            # create a new column and use np.select to assign values to it using our lists as arguments
            self.df['section'] = np.select(conditions, values)

            # Left :0, Middle :1, Right :2 
            self.df['left'] = np.where(self.df['section'] == '0', 1, 0)
            self.df['middle'] = np.where(self.df['section'] == '1', 1, 0)
            self.df['right'] = np.where(self.df['section'] == '2', 1, 0)
            
            # set the therashould values
            self.df = self.df[self.df['confidence'] > self.threshold] 
            
            # looping over detected cars on the dataFrame and pass the detected cars coordinates to draw_bbox function
            self.result = [draw_bbox(frame=frame, x1=row[0], y1=row[1], x2=row[2], y2=row[3], section=row[4])
                           for row in self.df[['xmin', 'ymin', 'xmax', 'ymax', 'section']].to_numpy().astype(int)]
        print('======================================================================================')
        print('===================================== Cars Detection =================================')
        print('======================================================================================')
        print(self.df)
        print('--------------------------------------------------------------------------------------')
        left_section = get_sec_data(section='left', data_frame=self.df)
        print('Left Section')
        print("{}".format(left_section))
        print('----------------------------------------------------------------------------------')
        middle_section = get_sec_data(section='middle', data_frame=self.df)
        print('Middle Section')
        print("{}".format(middle_section))
        print('-----------------------------------------------------------------------------------')
        right_section = get_sec_data(section='right', data_frame=self.df)
        print('Right Section')
        print("{}".format(right_section))

        # return the meta-data for all detected cars
        return self.df


def draw_bbox(frame, x1, y1, x2, y2, section):
    if section == 0:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    elif section == 1:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    elif section == 2:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
   
    
def get_section_center(start_section_width,end_section_width):
    return round((abs(end_section_width - start_section_width))/2)+start_section_width


def get_sec_data(section,data_frame):
    if not data_frame.empty:
        return data_frame[data_frame[section] == 1].drop(['section', 'left',  'middle', 'right'], axis=1)
    else:
        print('No Cars')

class ComputerVisionFrontal:

    def __init__(self, width=1000, height=700):
        # Some Initial  Parameters
        self.width, self.height = width, height
        # Detection Instances
        self.od = MultiCarsdetection()

        # Read video
        self.video = cv2.VideoCapture("video2.mp4")

    def run_front(self):

        # ReSize the Frame

        # Exit if video not opened.
        if not self.video.isOpened():
            print("Could not open video")
            sys.exit()

        while True:
            # Read Frame by frame
            ok, frame = self.video.read()
            frame = cv2.resize(frame, (self.width, self.height))  # Resize the Frame

            # Exit if video not opened.
            if not ok:
                print('Cannot read video file')
                sys.exit()
                break

            self.data_frame = self.od.detect(frame=frame, width=self.width)

            # Divide Frame Into Sections
            # Left section
            cv2.line(frame, (round(self.width/3), 0), (round(self.width/3), self.height), (0, 0, 0), 1)
            cv2.putText(frame, "Left Section", (get_section_center(0, round(self.width/3)), 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # Middle section
            cv2.line(frame, (round(self.width/(3/2)), 0), (round(self.width/(3/2)), self.height), (0, 0, 0), 1)
            cv2.putText(frame, "Middle Section", (get_section_center(round(self.width/3), round(self.width/(3/2))), 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            # Right section
            cv2.putText(frame, "Right Section", (get_section_center(round(self.width/(3/2)), round(self.width)), 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
            # Showing The Video Frame
            cv2.imshow('test_Image', frame)

            # if press q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video.release()
        cv2.destroyAllWindows()