
import time, cv2

# uncomment to test on RPi
# from distances.dist_measure import *
# from distances.dist_angle import *

# uncomment this to test on PC
#from Tools.Test_Measure_app_Front import *
from communication.com_socket import *
from threading import Thread
from cv_algorithm.frontal_computer_vision_app import ComputerVisionFrontal
from communication.com_serial import SerialComm


class FrontMode:
    current_v_length = 5

    def __init__(self, ip="127.0.0.1", port=20070, timeout=1, source=0, name="Front Sender"):
        '''
        - Create CV object.
        - run Cv_obj.run_front() in thread.
        - Update frame, discrete from Cv_obj's attributes {frame_to_send}, {angle_to_send}
        - send discrete from Cv_obj's attributes {angle_to_send} to measurement module
        - send frame from Cv_obj's attributes {frame_to_send} to outer machine
        '''
        # instance for run ComputerVisionFrontal class
        self.ip, self.port, self.timeout, self.name = ip, port, timeout, name
        self.data_sock_send = Server(ip=self.ip, port=self.port, timeout=self.timeout, name=self.name)
        self.ser_get_distance = SerialComm(port="COM11", name="Receiver", baudrate=115200)

        self.source = source
        self.to_send_fd = DataHolder()
        #self.servo_obj_list = [Angles(servo_pin=11), Angles(servo_pin=12), Angles(servo_pin=13)]
        #self.us_obj_list = [Measure(trig=22, echo=23), Measure(trig=24, echo=25), Measure(trig=26, echo=27)]

        self.computer_vision_frontal_instance = ComputerVisionFrontal(source=self.source)
        # CV model run front in thread
        self.t_cv_front = Thread(target=self.computer_vision_frontal_instance.run_front,
                                 args=[self.data_sock_send], daemon=True)
        self.t_update_f = Thread(target=self.update_all, args=[self.to_send_fd, self.data_sock_send], daemon=True)
        self.t_get_dist_asynch = Thread(target=self.distance_fetcher, args=[], daemon=True)

        self.dist_list = [0] * 3
        self.cv_angle_list = self.last_angle_values = [0] * 3
        self.threads_activated = False

    def __call__(self, call_back):
        while self.data_sock_send.connect_mechanism():
            if not self.threads_activated:
                self.threads_activated = True
                self.t_update_f.start()
                self.t_cv_front.start()
                self.t_get_dist_asynch.start()
                time.sleep(3)
                call_back()

            self.cv_angle_list = self.computer_vision_frontal_instance.angle_to_send
            if self.computer_vision_frontal_instance.angle_to_send is None:
                self.cv_angle_list = [-1, -1, -1]

            self.ser_get_distance.send_query({"ORIENT": self.cv_angle_list})
            # Check if the last received values is different
            #for section in range(0, len(self.servo_obj_list)):
                # self.servo_obj_list[section].set_angle(self.cv_angle_list[section])
                # self.dist_list[section] = self.us_obj_list[section].distance_read()


            if self.dist_list is not None and len(self.dist_list) == 3:
                disc = [[[self.dist_list[i], self.cv_angle_list[i]] for i in range(0, 3)], FrontMode.current_v_length]
            self.to_send_fd.set_discrete(disc)
            self.to_send_fd.set_frame(self.computer_vision_frontal_instance.frame_to_send)

            #print(f'APP: to send: {self.to_send_fd.discrete_stack}')
            time.sleep(0.02)
        self.data_sock_send.s.close()
        self.data_sock_send.client_socket.close()

    def update_all(self, send_fd, data_sock):
        while self.data_sock_send.connect_mechanism():
            to_send = {"F": send_fd.get_frame(),
                       "D": send_fd.get_discrete()}
            data_sock.send_all(to_send)
            if to_send["F"] is not None:
                pass
                # cv2.imshow('SOCK_Sending This Frame...', to_send["F"])
            time.sleep(0.2)

    def distance_fetcher(self):
        while True:
            received = self.ser_get_distance.receive_query()
            if received:
                self.dist_list = received["DISTANCE"]
            time.sleep(0.3)
