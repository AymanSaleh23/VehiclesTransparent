from threading import Thread
import time, cv2

from communication.com_socket import *
from cv_algorithm.back_computer_vision_app import ComputerVisionBackApp
# uncomment to test on RPi
#from distances.dist_measure import *
#from distances.dist_angle import *

# uncomment this to test on PC
#from Tools.Test_Measure_app_Front import *
from communication.com_serial import SerialComm

from mathematics.mathlib import *

class BackMode:
    def __init__(self, ip="127.0.0.1", port=20070, timeout=1, source=0, name="Receive Socket"):
        '''
        - Create CV object.
        - Create one measurement unit.
        - run Cv_obj.run_back() in thread.
        - receive frame, discrete from Cv_obj's sockets (applied internally in CV_back_app)
        - read single distance
        - pass all parameters to mathematical model
        '''
        self.ip, self.port, self.timeout, self.name, self.source = ip, port, timeout, name, source
        self.data_sock_receive = Client(ip=self.ip, port=self.port, timeout=self.timeout, name=self.name)
        self.ser_get_distance = SerialComm(port="COM10", name="Receiver", baudrate=115200)

        # instance for run ComputerVisionFrontal class
        self.computer_vision_back_instance = None
        self.received_frame = None
        self.received_discrete = None
        self.direct_distance = None
        self.direct_distance = None

        #self.servo_obj = Angles(servo_pin=11)
        #self.us_obj = Measure(trig=22, echo=23)

        self.computer_vision_back_instance = ComputerVisionBackApp(source=self.source)

        # CV model run front in thread
        self.t_cv_back = Thread(target=self.computer_vision_back_instance.run_back,
                                args=[self.data_sock_receive], daemon=True)
        self.t_get_dist_asynch = Thread(target=self.distance_fetcher, args=[], daemon=True)

        self.threads_activated = False

    def __call__(self, call_back):

        while self.data_sock_receive.connect_mechanism():
            if not self.threads_activated:
                self.threads_activated = True
                self.t_cv_back.start()
                self.t_get_dist_asynch.start()
                time.sleep(3)
                call_back()
            received_frame, received_discrete = self.data_sock_receive.receive_all(1024)
            # cv2.imshow("Informed Frame", frame)
            if received_frame is not None:
                self.computer_vision_back_instance.data_holder.set_frame(received_frame)

            if received_discrete is not None and type(self.computer_vision_back_instance.front_vehicle_center) is list:
                # Update frames which is received from socket.
                self.computer_vision_back_instance.data_holder.set_discrete(received_discrete)
                angles = [-1, self.computer_vision_back_instance.front_vehicle_center[0], -1]
                self.ser_get_distance.send_query({"ORIENT": angles})
                #direct_distance = self.us_obj.distance_read()
                if self.direct_distance is not None:
                    abs_dist = math_model(data=received_discrete[0],
                                          vehicle_length=received_discrete[1],
                                          direct_distance=self.direct_distance,
                                          theta=self.computer_vision_back_instance.front_vehicle_center[0])

                    print(f"Front Vehicle Center: {self.computer_vision_back_instance.front_vehicle_center[0]}")
                    print(f"Absolute Distances: {abs_dist}")

            print(f'Direct Distance: \n{self.direct_distance}')

            time.sleep(0.01)
            # self.computer_vision_back_instance.data_holder.reset_discrete()
            # self.received_fd.reset_discrete()
        self.data_sock_receive.s.close()

    def distance_fetcher(self):
        while True:
            received = self.ser_get_distance.receive_query()
            if received:
                self.dist_list = received["DISTANCE"]
            time.sleep(0.3)
