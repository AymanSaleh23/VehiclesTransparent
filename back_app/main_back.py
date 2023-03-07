from threading import Thread
import time

from comlib.com_socket import *
from cv_algorithm.back_computer_vision_app import ComputerVisionBackApp
# uncomment to test on RPi
#from distances.dist_measure import *
#from distances.dist_angle import *

# uncomment this to test on PC
from Tools.Test_Measure_app_Front import *
from mathematics.mathlib import *

class BackMode:
    def __init__(self):
        '''
        - Create CV object.
        - Create one measurement unit.
        - run Cv_obj.run_back() in thread.
        - receive frame, discrete from Cv_obj's sockets (applied internally in CV_back_app)
        - read single distance
        - pass all parameters to mathematical model

        '''
        self.received_frames_sock = Client("127.0.0.1", 20070, timeout=0.1)

        # instance for run ComputerVisionFrontal class
        self.computer_vision_back_instance = None
        self.received_frame = None
        self.received_discrete = None
        self.received_fd = DataHolder()
        self.direct_distance = None

        self.servo_obj = Angles(servo_pin=11)
        self.us_obj = Measure(trig=22, echo=23)

        self.computer_vision_back_instance = ComputerVisionBackApp(width=500, height=300)

        # CV model run front in thread
        self.t_cv_back = Thread(target=self.computer_vision_back_instance.run_back, args=[], daemon=True)
        self.t_cv_back.start()

    def __call__(self):
        while True:
            received_frame, received_discrete = self.received_frames_sock.receive_all(1024)
            if received_frame is not None:
                # Update frames which is received from socket.
                self.computer_vision_back_instance.current_streamed_frame = received_frame
                self.received_fd.set_frame(received_frame)

            if received_discrete is not None and type(self.computer_vision_back_instance.front_vehicle_center) is list:
                self.received_fd.set_discrete(received_discrete)

                direct_distance = self.us_obj.distance_read()
                abs_dist = math_model(data=self.received_fd.get_discrete()[0],
                                      vehicle_length=self.received_fd.get_discrete()[1],
                                      direct_distance=direct_distance,
                                      theta=self.computer_vision_back_instance.front_vehicle_center[0])
                print(f"Front Vehicle Center: {self.computer_vision_back_instance.front_vehicle_center[0]}")
                print(f"Absolute Distances: {abs_dist}")

            print(f"received_fd.get_discrete(): {self.received_fd.get_discrete()}")
            print(f'Data: \n{self.received_fd.get_discrete()}')
            time.sleep(0.01)
            self.received_fd.reset_discrete()
