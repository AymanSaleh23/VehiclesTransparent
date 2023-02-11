import time
from threading import Thread
from comlib import com_init_ip, com_socket
from cv_algorithm import cv_detection_tracking_yolo
from mathematics import mathlib

#To be tested on RPi
#from distances import dist_angle, dist_measure
CURRENT_VEHICLE_LENGTH = 4
if __name__ == "__main__":
    """
    1- create CV object.
    2- Create single Ultrasonic object
    3- Create single Servo Object
    4- Create Single socket object (for Discrete data)
    5- make CV object run in thread
    6- make Ultrasonic and Servo work in infinite loop upon CV object attribute {front_vehicle_center}
        catch {direct_distance}, {theta} for model
    7- Calculate distance using the return of 4 and 6 using function {math_model}
    """
