from threading import Thread
import time, screeninfo
import cv2

from comlib.com_socket import *
from cv_algorithm.back_computer_vision_app import ComputerVisionBackApp
# uncomment to test on RPi
#from distances.dist_measure import *
#from distances.dist_angle import *

# uncomment this to test on PC
from Tools.Test_Measure_app_Front import *
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

        # instance for run ComputerVisionFrontal class
        self.computer_vision_back_instance = None
        self.received_frame = None
        self.received_discrete = None
        self.received_fd = DataHolder()
        self.direct_distance = None

        self.servo_obj = Angles(servo_pin=11)
        self.us_obj = Measure(trig=22, echo=23)

        self.computer_vision_back_instance = ComputerVisionBackApp(source=self.source)

        # CV model run front in thread
        self.t_cv_back = Thread(target=self.computer_vision_back_instance.run_back,
                                args=[self.data_sock_receive], daemon=True)

        self.threads_activated = False

    def __call__(self, call_back):
        self.screen = screeninfo.get_monitors()[0]
        self.width, self.height = self.screen.width, self.screen.height

        while self.data_sock_receive.connect_mechanism():
            if not self.threads_activated:
                self.threads_activated = True
                self.t_cv_back.start()
                time.sleep(3)
                call_back()
            received_frame, received_discrete = self.data_sock_receive.receive_all(1024)
            # cv2.imshow("Informed Frame", frame)
            time.sleep(0.2)
            if received_frame is not None:
                # Update frames which is received from socket.
                self.computer_vision_back_instance.current_streamed_frame = received_frame
                self.received_fd.set_frame(received_frame)

                print(f"Width: {self.width}")
                print(f"Height: {self.height}")
                print(f"self.computer_vision_back_instance Width: {self.computer_vision_back_instance.width}")
                print(f"self.computer_vision_back_instance Height: {self.computer_vision_back_instance.height}")

                if self.computer_vision_back_instance.last_read_frame is not None:
                    self.computer_vision_back_instance.last_read_frame = \
                        self.update_warning(self.computer_vision_back_instance.last_read_frame, received_discrete)

                    self.computer_vision_back_instance.last_read_frame = \
                        cv2.resize(self.computer_vision_back_instance.last_read_frame,
                                   (self.computer_vision_back_instance.width,
                                   self.computer_vision_back_instance.height))

            if received_discrete is not None and type(self.computer_vision_back_instance.front_vehicle_center) is list:
                self.received_fd.set_discrete(received_discrete)

                direct_distance = self.us_obj.distance_read()
                abs_dist = math_model(data=received_discrete[0],
                                      vehicle_length=received_discrete[1],
                                      direct_distance=direct_distance,
                                      theta=self.computer_vision_back_instance.front_vehicle_center[0])
                print(f"Front Vehicle Center: {self.computer_vision_back_instance.front_vehicle_center[0]}")
                print(f"Absolute Distances: {abs_dist}")

            print(f"\n\n\n\nreceived_fd.get_discrete(): {received_discrete}\n\n\n\n")
            print(f'Data: \n{self.received_discrete}')
            window_name = 'Back View'
            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, self.screen.x - 1, self.screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, self.computer_vision_back_instance.last_read_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)
            # self.received_fd.reset_discrete()

        self.data_sock_receive.s.close()

    def update_warning(self, frame, disc):
        """
        asynchronously update flags in left and right to inform user not to pass
        """
        secure = [True, True]
        # while True:
        if self.data_sock_receive.connected:
            #   [[left_dist, ang], [center_dist, ang], [right_dist, ang]],[length] ]
            print(f"\n\n\nself.bm.received_fd.get_discrete(){disc}\n\n\n")

            if disc is not None:

                if disc[0][0][1] < 0:
                    secure[0] = False
                    cv2.arrowedLine(frame, (self.computer_vision_back_instance.width//4,
                                           self.computer_vision_back_instance.height*3//4),
                                    (10, self.computer_vision_back_instance.height * 3 // 4), (0, 0, 255), 5)
                    print("Don't Pass left is not Secure")

                if disc[0][2][1] < 0:
                    secure[1] = False
                    cv2.arrowedLine(frame, (self.computer_vision_back_instance.width * 3 // 4,
                                           self.computer_vision_back_instance.height * 3 // 4),
                                    (self.computer_vision_back_instance.width - 5,
                                     self.computer_vision_back_instance.height * 3 // 4),
                                    (0, 0, 255),
                                    10)
                    print("Don't Pass right is not Secure")

                if secure[0]:
                    cv2.arrowedLine(frame, (self.computer_vision_back_instance.width // 4,
                                           self.computer_vision_back_instance.height * 3 // 4),
                                    (10, self.computer_vision_back_instance.height * 3 // 4), (0, 255, 0), 5)

                    print("You Can Pass left it is Secure")

                if secure[1]:
                    cv2.arrowedLine(frame, (self.computer_vision_back_instance.width * 3 // 4,
                                           self.computer_vision_back_instance.height * 3 // 4),
                                    (self.computer_vision_back_instance.width - 5,
                                     self.computer_vision_back_instance.height * 3 // 4),
                                    (0, 255, 0),
                                    10)
                    print("You Can Pass right it is Secure")
        return frame
