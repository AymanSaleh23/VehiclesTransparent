from threading import Thread
import time, cv2
from comlib.com_socket import *

# uncomment to test on RPi
# from distances.dist_measure import *
# from distances.dist_angle import *

# uncomment this to test on PC
from Tools.Test_Measure_app_Front import *

from comlib.com_socket import *
from threading import Thread

from cv_algorithm.frontal_computer_vision_app import ComputerVisionFrontal

# instance for run ComputerVisionFrontal class

out_sock_frame = Server(ip="192.168.1.11", port=20070, timeout=1, name="Frame Sender")

current_v_length = 5

computer_vision_frontal_instance = None


def update_all(send_fd):
    while True:
        to_send = {"F": send_fd.get_frame(),
                   "D": send_fd.get_discrete()}
        print(f'to send: {to_send["D"]}')
        out_sock_frame.send_frame(to_send)
        time.sleep(0.01)

if __name__ == "__main__":
    '''
    - Create CV object.
    - run Cv_obj.run_front() in thread.
    - Update frame, discrete from Cv_obj's attributes {frame_to_send}, {angle_to_send}
    - send discrete from Cv_obj's attributes {angle_to_send} to measurement module
    - send frame from Cv_obj's attributes {frame_to_send} to outer machine
    '''
    to_send_fd = DataHolder()
    computer_vision_frontal_instance = ComputerVisionFrontal()
    # CV model run front in thread
    t_cv_front = Thread(target=computer_vision_frontal_instance.run_front, args=[], daemon=True)

    t_update_f = Thread(target=update_all, args=[to_send_fd], daemon=True)
    t_update_f.start()

    servo_obj_list = [Angles(servo_pin=11), Angles(servo_pin=12), Angles(servo_pin=13)]
    us_obj_list = [Measure(trig=22, echo=23), Measure(trig=24, echo=25), Measure(trig=26, echo=27)]

    dist_list = [0] * 3
    cv_angle_list = last_angle_values = [0] * 3

    t_cv_front.start()

    while True:
        cv_angle_list = computer_vision_frontal_instance.angle_to_send
        print(f"Angle List received: {cv_angle_list}")
        if computer_vision_frontal_instance.angle_to_send is None:
            cv_angle_list = [45, 90, 135]

        # Check if the last received values is different
        for section in range(0, len(servo_obj_list)):
            servo_obj_list[section].set_angle(cv_angle_list[section])
            dist_list[section] = us_obj_list[section].distance_read()

        print(f"dist_list: {dist_list}")
        print(f"to_send_fd.get_discrete(): {to_send_fd.get_discrete()}")
        disc = [[dist_list[i], cv_angle_list[i]] for i in range(0, 3)]
        print(f'APP: to send: {to_send_fd.get_discrete()}')
        print(f'APP: disc: {disc}')
        print(f'APP: disc.append(current_v_length): {disc.append(current_v_length)}')
        # to_send_fd.set_discrete([ [dist_list[i], cv_angle_list[i]] for i in range(0, 3)].append(current_v_length))
        to_send_fd.set_discrete(disc)
        print(f'APP: to send: {to_send_fd.get_discrete()}')
        to_send_fd.set_frame(computer_vision_frontal_instance.frame_to_send)

        time.sleep(0.3)
