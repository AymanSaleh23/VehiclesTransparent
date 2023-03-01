from threading import Thread
import time
from comlib.com_socket import *
from cv_algorithm.frontal_computer_vision_app import ComputerVisionFrontal
from front_app.cv_global_variables import CVFrontGlobalVariables

if __name__ == "__main__":
    '''
    - Create CV object.
    - run Cv_obj.run_front() in thread.
    - Update frame, discrete from Cv_obj's attributes {frame_to_send}, {angle_to_send}
    - send discrete from Cv_obj's attributes {angle_to_send} to measurement module
    - send frame from Cv_obj's attributes {frame_to_send} to outer machine
    '''

    # instance for run ComputerVisionFrontal class
    computer_vision_frontal_instance = ComputerVisionFrontal()
    out_sock_frame = Server(ip="192.168.1.11", port=10050)
    in_sock_disc = Server(ip="127.0.0.1", port=10051)

    # CV model run front in thread
    t_cv_front = Thread(target=computer_vision_frontal_instance.run_front, args=[])
    t_cv_front.setDaemon(True)

    # send discrete run in thread
    t_disc_send = Thread(target=in_sock_disc.send, args=[])
    t_disc_send.setDaemon(True)

    t_cv_front.start()
    t_disc_send.start()


    while True:
        in_sock_disc.update_to_send(computer_vision_frontal_instance.angle_to_send)
        out_sock_frame.send_frame(computer_vision_frontal_instance.frame_to_send)
        time.sleep(0.3)