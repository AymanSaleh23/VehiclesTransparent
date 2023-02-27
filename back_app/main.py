from threading import Thread
import time
from comlib.com_socket import *
from cv_algorithm.cv_back import ComputerVisionBackApp
# uncomment to test on RPi
#from distances.dist_measure import *
#from distances.dist_angle import *

# uncomment this to test on PC
from Tools.Test_Measure_app_Front import *
from mathematics.mathlib import *

if __name__ == "__main__":
    '''
    - Create CV object.
    - Create one measurement unit.
    - run Cv_obj.run_back() in thread.
    - receive frame, discrete from Cv_obj's sockets (applied internally in CV_back_app)
    - read single distance
    - pass all parameters to mathematical model 
    
    '''

    # instance for run ComputerVisionFrontal class
    computer_vision_back_instance = ComputerVisionBackApp()

    servo_obj = Angles(servo_pin=11)
    us_obj = Measure(trig=22, echo=23)

    #implemented internally in CV_back_app
    #out_sock_frame = Client(ip="192.168.1.11", port=10050)
    out_sock_disc = Client(ip="192.168.1.11", port=10052)

    # CV model run front in thread
    t_cv_back = Thread(target=computer_vision_back_instance.run_back, args=[])
    t_cv_back.setDaemon(True)
    t_cv_back.start()

    discrete = 0

    while True:
        discrete = out_sock_disc.recv_discrete()
        print(f"Received Discrete: {discrete}")
        abs_dist = math_model(data=discrete[0], vehicle_length=discrete[1],
                              direct_distance=us_obj.distance_read(), theta=90)
        print(f"Absolute Distances: {abs_dist}")
        time.sleep(0.3)