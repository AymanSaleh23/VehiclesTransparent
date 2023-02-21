import threading
import time
from comlib.com_socket import *
from cv_algorithm.multi_cars_detection import ComputerVisionFrontal
from front_app.cv_global_variables import CVFrontGlobalVariables

if __name__ == "__main__":
    # instance for run ComputerVisionFrontal class
    computer_vision_frontal_instance = ComputerVisionFrontal()
    in_cv2measure_sock_angle = Server(port=10051, ip='127.0.0.1')
    in_cv2comm_sock_frame = Server(port=10053, ip='127.0.0.1')

    thrd_asynch_send_angle = threading.Thread(target=in_cv2measure_sock_angle.send, args=[])
    thrd_asynch_send_angle.setDaemon(True)

    thrd_asynch_send_frame = threading.Thread(target=in_cv2comm_sock_frame.send, args=[])
    thrd_asynch_send_frame.setDaemon(True)

    thrd_asynch_run_front = threading.Thread(target=computer_vision_frontal_instance.run_front, args=[])
    thrd_asynch_run_front.setDaemon(True)

    thrd_asynch_send_angle.start()
    thrd_asynch_run_front.start()
    thrd_asynch_send_frame.start()

    while True:
        in_cv2measure_sock_angle.update_to_send(CVFrontGlobalVariables.detected_cars_centers_list)
        in_cv2comm_sock_frame.update_to_send(CVFrontGlobalVariables.frame)

        time.sleep(2)
